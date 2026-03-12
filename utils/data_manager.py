"""Persistencia local en JSON + gestión de carpeta de medios — v4.1."""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR   = Path(__file__).parent.parent
DATA_FILE  = BASE_DIR / "data" / "visits.json"
MEDIA_DIR  = BASE_DIR / "data" / "media"


def _ensure_file():
    """Ensure visits.json exists and contains a valid list."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return
    # Validate: if file contains a dict or invalid JSON, reset to []
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
    """Save or update a visit. Always returns the visit id."""
    visits = load_visits()
    visit_data["updated_at"] = datetime.now().isoformat()

    # Serialize complex list-typed values to ensure JSON safety
    safe_data = {}
    for k, v in visit_data.items():
        if isinstance(v, (str, int, float, bool, type(None))):
            safe_data[k] = v
        elif isinstance(v, list):
            safe_data[k] = v  # keep lists as-is (JSON serializable)
        elif isinstance(v, dict):
            safe_data[k] = v  # keep dicts as-is
        else:
            safe_data[k] = str(v)

    existing = next(
        (i for i, v in enumerate(visits) if v.get("id") == safe_data.get("id")), None
    )
    if existing is not None:
        visits[existing] = safe_data
    else:
        safe_data["created_at"] = datetime.now().isoformat()
        safe_data["id"] = f"visit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        visits.append(safe_data)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)
    # Auto-sync to Drive if configured and autosync is on
    try:
        import streamlit as st
        if st.session_state.get("gdrive_autosync", False):
            from utils.gdrive import is_configured, sync_visits_to_drive
            if is_configured():
                sync_visits_to_drive(DATA_FILE)
    except Exception:
        pass
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


def save_media_file(visit_id: str, file_bytes: bytes, filename: str, label: str = "") -> str:
    folder = MEDIA_DIR / visit_id
    folder.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%H%M%S")
    safe_name = f"{ts}_{filename}"
    filepath = folder / safe_name
    with open(filepath, "wb") as f:
        f.write(file_bytes)
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
                "path": str(f),
                "label": meta.get(f.name, {}).get("label", ""),
            })
    return files


def delete_media_file(visit_id: str, filename: str):
    folder = MEDIA_DIR / visit_id
    filepath = folder / filename
    if filepath.exists():
        filepath.unlink()
    meta_file = folder / "meta.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
            meta.pop(filename, None)
            with open(meta_file, "w", encoding="utf-8") as mf:
                json.dump(meta, mf, ensure_ascii=False, indent=2)
        except Exception:
            pass
