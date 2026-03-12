"""Persistencia local en JSON + gestión de medios — v8.
Streamlit Cloud es solo-lectura: detectamos esto y usamos /tmp automáticamente.
Al guardar, sube a Drive: JSON maestro + diagnostico.json + Excel + Word por proyecto.
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def _resolve_data_dir() -> Path:
    """Return a writable data directory. Falls back to /tmp on read-only filesystems."""
    local = Path(__file__).parent.parent / "data"
    try:
        local.mkdir(parents=True, exist_ok=True)
        probe = local / ".writable"
        probe.write_text("ok")
        probe.unlink()
        return local
    except (OSError, PermissionError):
        fallback = Path("/tmp/livlin_data")
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


DATA_DIR  = _resolve_data_dir()
DATA_FILE = DATA_DIR / "visits.json"
MEDIA_DIR = DATA_DIR / "media"


def _ensure_file():
    """Ensure visits.json exists and contains a valid list. Auto-restores from Drive."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        try:
            from utils.gdrive import is_configured, sync_visits_from_drive
            if is_configured():
                sync_visits_from_drive(DATA_FILE)
                if DATA_FILE.exists():
                    return
        except Exception:
            pass
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = json.load(f)
        if not isinstance(content, list):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    except (json.JSONDecodeError, ValueError):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_visits() -> list:
    _ensure_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_visit(visit_data: dict) -> str:
    """Save or update a visit. Returns the visit id.
    Also uploads to Drive: visits.json master + per-project diagnostico.json + Excel + Word.
    """
    visits = load_visits()
    visit_data["updated_at"] = datetime.now().isoformat()

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

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)

    # ── Drive sync (non-blocking) ────────────────────────────────────────
    try:
        from utils.gdrive import (is_configured, sync_visits_to_drive,
                                   upload_space_json, upload_space_excel,
                                   upload_space_docx)
        if is_configured():
            sync_visits_to_drive(DATA_FILE)   # master visits.json
            upload_space_json(safe_data)       # diagnostico/diagnostico.json
            upload_space_excel(safe_data)      # excel/diagnostico_*.xlsx
            upload_space_docx(safe_data)       # informe/informe_*.docx
    except Exception as e:
        print(f"[data_manager] Drive sync error (non-fatal): {e}")

    return safe_data["id"]


def get_visit(visit_id: str) -> dict | None:
    visits = load_visits()
    return next((v for v in visits if v.get("id") == visit_id), None)


def delete_visit(visit_id: str):
    visits = load_visits()
    visits = [v for v in visits if v.get("id") != visit_id]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)
    media_folder = MEDIA_DIR / visit_id
    if media_folder.exists():
        shutil.rmtree(media_folder)


def save_media_file(visit_id: str, file_bytes: bytes, filename: str,
                    label: str = "", space_name: str = "") -> str:
    """Save photo locally (or in /tmp) and upload to Drive fotos/ immediately."""
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    folder = MEDIA_DIR / visit_id
    folder.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%H%M%S")
    safe_name = f"{ts}_{filename}"
    filepath  = folder / safe_name

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    # Update local meta
    meta_file = folder / "meta.json"
    meta = {}
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
        except Exception:
            meta = {}
    meta[safe_name] = {"label": label, "original": filename, "ts": ts}
    with open(meta_file, "w", encoding="utf-8") as mf:
        json.dump(meta, mf, ensure_ascii=False, indent=2)

    # Upload to Drive fotos/ immediately
    try:
        from utils.gdrive import is_configured, upload_photo_to_space
        if is_configured():
            ext = filepath.suffix.lower()
            mime_map = {".jpg":"image/jpeg",".jpeg":"image/jpeg",
                        ".png":"image/png",".webp":"image/webp"}
            mime = mime_map.get(ext, "image/jpeg")
            upload_photo_to_space(
                visit_id=visit_id,
                space_name=space_name or visit_id,
                filename=safe_name,
                file_bytes=file_bytes,
                mimetype=mime,
                label=label,
            )
    except Exception as e:
        print(f"[data_manager] photo upload error (non-fatal): {e}")

    return str(filepath)


def list_media_files(visit_id: str) -> list:
    folder = MEDIA_DIR / visit_id
    if not folder.exists():
        return []
    meta_file = folder / "meta.json"
    meta = {}
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as mf:
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
    folder    = MEDIA_DIR / visit_id
    filepath  = folder / filename
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
