"""Persistencia v9 — Google Drive como fuente de verdad.

Flujo de datos:
  LECTURA:  Drive → st.session_state._visits_cache (caché en memoria de la sesión)
  ESCRITURA: → Drive directamente → actualiza caché local

  /tmp sólo se usa como último fallback offline.
  La app NO depende de /tmp para funcionar.
"""
import json, shutil
from datetime import datetime
from pathlib import Path

# /tmp como fallback local (no fuente de verdad)
_TMP_DIR  = Path("/tmp/livlin_data")
_TMP_FILE = _TMP_DIR / "visits.json"
MEDIA_DIR = _TMP_DIR / "media"
# Kept for admin panel compatibility
DATA_DIR  = _TMP_DIR
DATA_FILE = _TMP_FILE


def _cache_key() -> str:
    return "_visits_cache"


def _get_cached(default=None):
    try:
        import streamlit as st
        return st.session_state.get(_cache_key(), default)
    except Exception:
        return default


def _set_cached(visits: list):
    try:
        import streamlit as st
        st.session_state[_cache_key()] = visits
    except Exception:
        pass


def _write_tmp(visits: list):
    """Write to /tmp as offline backup."""
    try:
        _TMP_DIR.mkdir(parents=True, exist_ok=True)
        with open(_TMP_FILE, "w", encoding="utf-8") as f:
            json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_visits() -> list:
    """Load visits. Priority: session_state cache → Drive → /tmp fallback."""
    # 1. Session cache (fastest — same session)
    cached = _get_cached()
    if cached is not None:
        return cached

    # 2. Drive (source of truth)
    try:
        from utils.gdrive import is_configured, drive_load_visits
        if is_configured():
            visits = drive_load_visits()
            _set_cached(visits)
            _write_tmp(visits)
            return visits
    except Exception as e:
        print(f"[data_manager] Drive load error: {e}")

    # 3. /tmp fallback (offline / Drive unavailable)
    try:
        if _TMP_FILE.exists():
            with open(_TMP_FILE) as f:
                visits = json.load(f)
            if isinstance(visits, list):
                _set_cached(visits)
                return visits
    except Exception:
        pass

    visits = []
    _set_cached(visits)
    return visits


def _invalidate_cache():
    """Force next load_visits() to re-read from Drive."""
    try:
        import streamlit as st
        st.session_state.pop(_cache_key(), None)
    except Exception:
        pass


def save_visit(visit_data: dict) -> str:
    """Save or update a visit.
    Writes to Drive immediately (source of truth) + updates session cache.
    Returns visit id.
    """
    visits = load_visits()
    visit_data["updated_at"] = datetime.now().isoformat()

    # Serialize
    safe_data = {}
    for k, v in visit_data.items():
        if isinstance(v, (str, int, float, bool, type(None))):
            safe_data[k] = v
        elif isinstance(v, (list, dict)):
            safe_data[k] = v
        else:
            safe_data[k] = str(v)

    existing = next(
        (i for i, v in enumerate(visits) if v.get("id") == safe_data.get("id")), None)
    if existing is not None:
        visits[existing] = safe_data
    else:
        safe_data["created_at"] = datetime.now().isoformat()
        safe_data["id"] = f"visit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        visits.append(safe_data)

    # Update caches immediately
    _set_cached(visits)
    _write_tmp(visits)

    # ── Drive writes ────────────────────────────────────────────────────
    drive_errors = []
    try:
        from utils.gdrive import is_configured, drive_save_visits, drive_upload_space_files
        if is_configured():
            # 1. Master visits.json
            ok = drive_save_visits(visits)
            if not ok:
                drive_errors.append("visits.json no se pudo guardar")

            # 2. Per-project files (diagnostico + Excel + Word)
            results = drive_upload_space_files(safe_data)
            drive_errors.extend(results.get("errors", []))

            # Surface errors to UI (non-blocking)
            if drive_errors:
                try:
                    import streamlit as st
                    st.session_state["_drive_last_errors"] = drive_errors
                except Exception:
                    pass
            else:
                try:
                    import streamlit as st
                    st.session_state.pop("_drive_last_errors", None)
                except Exception:
                    pass
    except Exception as e:
        print(f"[data_manager] Drive save error: {e}")

    return safe_data["id"]


def get_visit(visit_id: str) -> dict | None:
    visits = load_visits()
    return next((v for v in visits if v.get("id") == visit_id), None)


def delete_visit(visit_id: str):
    visits = load_visits()
    visits = [v for v in visits if v.get("id") != visit_id]
    _set_cached(visits)
    _write_tmp(visits)
    # Drive: also update master
    try:
        from utils.gdrive import is_configured, drive_save_visits
        if is_configured():
            drive_save_visits(visits)
    except Exception:
        pass
    media_folder = MEDIA_DIR / visit_id
    if media_folder.exists():
        shutil.rmtree(media_folder)


def save_media_file(visit_id: str, file_bytes: bytes, filename: str,
                    label: str = "", space_name: str = "") -> str:
    """Save photo and upload to Drive fotos/ immediately. Returns local path."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    folder = MEDIA_DIR / visit_id
    folder.mkdir(parents=True, exist_ok=True)

    ts        = datetime.now().strftime("%H%M%S")
    safe_name = f"{ts}_{filename}"
    filepath  = folder / safe_name

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    # Local meta
    meta_file = folder / "meta.json"
    meta = {}
    if meta_file.exists():
        try:
            with open(meta_file) as mf:
                meta = json.load(mf)
        except Exception:
            meta = {}
    meta[safe_name] = {"label": label, "original": filename, "ts": ts}
    with open(meta_file, "w", encoding="utf-8") as mf:
        json.dump(meta, mf, ensure_ascii=False, indent=2)

    # Upload to Drive immediately
    try:
        from utils.gdrive import is_configured, upload_photo_to_space
        if is_configured():
            ext = filepath.suffix.lower()
            mime_map = {".jpg":"image/jpeg",".jpeg":"image/jpeg",
                        ".png":"image/png",".webp":"image/webp"}
            mime = mime_map.get(ext, "image/jpeg")
            ok, err = upload_photo_to_space(
                visit_id=visit_id,
                space_name=space_name or visit_id,
                filename=safe_name,
                file_bytes=file_bytes,
                mimetype=mime,
                label=label,
            )
            if not ok:
                print(f"[data_manager] photo upload failed: {err}")
    except Exception as e:
        print(f"[data_manager] photo upload exception: {e}")

    return str(filepath)


def list_media_files(visit_id: str) -> list:
    folder = MEDIA_DIR / visit_id
    if not folder.exists():
        return []
    meta_file = folder / "meta.json"
    meta = {}
    if meta_file.exists():
        try:
            with open(meta_file) as mf:
                meta = json.load(mf)
        except Exception:
            meta = {}
    files = []
    for f in sorted(folder.iterdir()):
        if f.name == "meta.json":
            continue
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            files.append({
                "filename": f.name,
                "path":     str(f),
                "label":    meta.get(f.name, {}).get("label", ""),
            })
    return files


def delete_media_file(visit_id: str, filename: str):
    folder   = MEDIA_DIR / visit_id
    filepath = folder / filename
    if filepath.exists():
        filepath.unlink()
    meta_file = folder / "meta.json"
    if meta_file.exists():
        try:
            with open(meta_file) as mf:
                meta = json.load(mf)
            meta.pop(filename, None)
            with open(meta_file, "w", encoding="utf-8") as mf:
                json.dump(meta, mf, ensure_ascii=False, indent=2)
        except Exception:
            pass
