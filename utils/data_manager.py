"""Persistencia v12 — Supabase como fuente de verdad.

Flujo:
  LECTURA:  Supabase → st.session_state._visits_cache (caché de sesión)
  ESCRITURA: → Supabase inmediatamente → actualiza caché

  /tmp como backup offline únicamente.
"""
import json, shutil
from datetime import datetime
from pathlib import Path

_TMP_DIR  = Path("/tmp/livlin_data")
_TMP_FILE = _TMP_DIR / "visits.json"
MEDIA_DIR = _TMP_DIR / "media"
DATA_DIR  = _TMP_DIR
DATA_FILE = _TMP_FILE


# ── Cache helpers ────────────────────────────────────────────────────────────

def _get_cached():
    try:
        import streamlit as st
        return st.session_state.get("_visits_cache")
    except Exception:
        return None


def _set_cached(visits: list):
    try:
        import streamlit as st
        st.session_state["_visits_cache"] = visits
    except Exception:
        pass


def _invalidate_cache():
    try:
        import streamlit as st
        st.session_state.pop("_visits_cache", None)
    except Exception:
        pass


def _write_tmp(visits: list):
    try:
        _TMP_DIR.mkdir(parents=True, exist_ok=True)
        with open(_TMP_FILE, "w", encoding="utf-8") as f:
            json.dump(visits, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ── Public API ───────────────────────────────────────────────────────────────

def load_visits() -> list:
    """Priority: session cache → Supabase → /tmp fallback."""
    cached = _get_cached()
    if cached is not None:
        return cached

    # Supabase (source of truth)
    try:
        from utils.supabase_db import is_configured, load_all_visits
        if is_configured():
            visits = load_all_visits()
            _set_cached(visits)
            _write_tmp(visits)
            return visits
    except Exception as e:
        print(f"[data_manager] Supabase load error: {e}")

    # /tmp fallback
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


def save_visit(visit_data: dict) -> str:
    """Save/update visit. Writes to Supabase + updates cache. Returns visit id."""
    visits = load_visits()
    visit_data["updated_at"] = datetime.now().isoformat()

    # Serialize safely
    safe_data = {}
    for k, v in visit_data.items():
        if isinstance(v, (str, int, float, bool, type(None), list, dict)):
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

    _set_cached(visits)
    _write_tmp(visits)

    # ── Supabase write ───────────────────────────────────────────────────
    errors = []
    try:
        from utils.supabase_db import is_configured, upsert_visit
        if is_configured():
            ok = upsert_visit(safe_data)
            if not ok:
                errors.append("No se pudo guardar en Supabase")
    except Exception as e:
        errors.append(f"Supabase: {e}")

    # Surface errors to UI
    try:
        import streamlit as st
        if errors:
            st.session_state["_db_last_errors"] = errors
        else:
            st.session_state.pop("_db_last_errors", None)
    except Exception:
        pass

    return safe_data["id"]


def get_visit(visit_id: str) -> dict | None:
    visits = load_visits()
    return next((v for v in visits if v.get("id") == visit_id), None)


def delete_visit(visit_id: str):
    visits = load_visits()
    visits = [v for v in visits if v.get("id") != visit_id]
    _set_cached(visits)
    _write_tmp(visits)
    try:
        from utils.supabase_db import is_configured, delete_visit_db
        if is_configured():
            delete_visit_db(visit_id)
    except Exception:
        pass
    media_folder = MEDIA_DIR / visit_id
    if media_folder.exists():
        shutil.rmtree(media_folder)


def save_media_file(visit_id: str, file_bytes: bytes, filename: str,
                    label: str = "", space_name: str = "") -> str:
    """Save photo locally in /tmp (photos not in Supabase plan)."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    folder = MEDIA_DIR / visit_id
    folder.mkdir(parents=True, exist_ok=True)

    ts        = datetime.now().strftime("%H%M%S")
    safe_name = f"{ts}_{filename}"
    filepath  = folder / safe_name

    with open(filepath, "wb") as f:
        f.write(file_bytes)

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
