"""Google Drive integration v9 — Drive como fuente de verdad.

Arquitectura:
  - Drive ES la base de datos. Toda lectura/escritura va a Drive.
  - st.session_state actúa como caché en memoria durante la sesión.
  - Estructura por proyecto:
      livlin-datos/
      ├── visits.json                     ← JSON maestro de todos los diagnósticos
      └── [NombreEspacio] — [visit_id]/   ← carpeta por proyecto
          ├── fotos/                      ← fotos (subidas al instante)
          ├── diagnostico/diagnostico.json
          ├── excel/diagnostico_*.xlsx
          └── informe/informe_*.docx
"""
import json, io, re, traceback
from pathlib import Path

BASE_DIR    = Path(__file__).parent.parent
CRED_FILE   = BASE_DIR / "credentials" / "gdrive_sa.json"
CONFIG_FILE = BASE_DIR / "credentials" / "gdrive_config.json"

_folder_cache: dict = {}
_service_cache = None   # module-level cache of (service, root_id)


def is_configured() -> bool:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            return True
    except Exception:
        pass
    return CRED_FILE.exists() and CONFIG_FILE.exists()


def _get_service():
    """Build & cache Drive API service. Returns (service, root_folder_id)."""
    global _service_cache
    if _service_cache is not None:
        return _service_cache

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError("Instala: pip install google-auth google-api-python-client")

    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            cred_dict = dict(st.secrets["gdrive"]["credentials"])
            # Fix escaped newlines in private_key (common Streamlit secrets issue)
            if "private_key" in cred_dict:
                pk = cred_dict["private_key"]
                if "\\n" in pk and "\n" not in pk:
                    pk = pk.replace("\\n", "\n")
                cred_dict["private_key"] = pk
            folder_id = st.secrets["gdrive"]["folder_id"]
            creds   = service_account.Credentials.from_service_account_info(
                cred_dict, scopes=["https://www.googleapis.com/auth/drive"])
            service = build("drive", "v3", credentials=creds, cache_discovery=False)
            _service_cache = (service, folder_id)
            return _service_cache
    except Exception as e:
        raise RuntimeError(f"Error cargando credenciales de Streamlit secrets: {e}")

    # Local files fallback
    if not CRED_FILE.exists():
        raise FileNotFoundError(f"Credenciales no encontradas: {CRED_FILE}")
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config no encontrada: {CONFIG_FILE}")
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    folder_id = config.get("folder_id", "")
    creds   = service_account.Credentials.from_service_account_file(
        str(CRED_FILE), scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    _service_cache = (service, folder_id)
    return _service_cache


def get_drive_status() -> dict:
    """Test Drive connection. Returns {ok, folder_id, error}."""
    try:
        service, root_id = _get_service()
        service.files().get(fileId=root_id, fields="id,name").execute()
        return {"ok": True, "folder_id": root_id, "error": None}
    except Exception as e:
        return {"ok": False, "folder_id": None, "error": str(e)}


# ── Folder helpers ───────────────────────────────────────────────────────────

def _safe_name(name: str, max_len: int = 80) -> str:
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', str(name)).strip()
    return clean[:max_len] if clean else "espacio"


def _get_or_create_folder(service, parent_id: str, name: str) -> str:
    cache_key = f"{parent_id}::{name}"
    if cache_key in _folder_cache:
        return _folder_cache[cache_key]
    escaped = name.replace("'", "\\'")
    q = (f"name='{escaped}' and '{parent_id}' in parents "
         f"and mimeType='application/vnd.google-apps.folder' and trashed=false")
    resp  = service.files().list(q=q, fields="files(id)").execute()
    files = resp.get("files", [])
    if files:
        fid = files[0]["id"]
    else:
        meta = {"name": name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id]}
        fid = service.files().create(body=meta, fields="id").execute()["id"]
    _folder_cache[cache_key] = fid
    return fid


def _find_file(service, folder_id: str, filename: str) -> str | None:
    escaped = filename.replace("'", "\\'")
    q = f"name='{escaped}' and '{folder_id}' in parents and trashed=false"
    resp  = service.files().list(q=q, fields="files(id)").execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def _upload_bytes(service, folder_id: str, filename: str,
                  data: bytes, mimetype: str) -> str:
    """Upload or overwrite file in folder. Returns file ID. Raises on failure."""
    from googleapiclient.http import MediaIoBaseUpload
    media    = MediaIoBaseUpload(io.BytesIO(data), mimetype=mimetype, resumable=False)
    existing = _find_file(service, folder_id, filename)
    if existing:
        service.files().update(
            fileId=existing, media_body=media).execute()
        return existing
    meta   = {"name": filename, "parents": [folder_id]}
    result = service.files().create(
        body=meta, media_body=media, fields="id").execute()
    return result["id"]


def _project_folder_name(space_name: str, visit_id: str) -> str:
    safe  = _safe_name(space_name or "espacio")
    short = visit_id[-15:] if len(visit_id) > 15 else visit_id
    return f"{safe} — {short}"


def _get_project_subfolders(service, root_id: str,
                             space_name: str, visit_id: str) -> dict:
    """Get or create the 4 subfolders for a project. Returns dict of folder IDs."""
    proj_name = _project_folder_name(space_name, visit_id)
    proj_id   = _get_or_create_folder(service, root_id, proj_name)
    return {
        "project":     proj_id,
        "fotos":       _get_or_create_folder(service, proj_id, "fotos"),
        "diagnostico": _get_or_create_folder(service, proj_id, "diagnostico"),
        "excel":       _get_or_create_folder(service, proj_id, "excel"),
        "informe":     _get_or_create_folder(service, proj_id, "informe"),
    }


# ── Primary data operations (Drive as source of truth) ──────────────────────

def drive_load_visits() -> list:
    """Load visits list directly from Drive. Returns [] on any error."""
    try:
        service, root_id = _get_service()
        file_id = _find_file(service, root_id, "visits.json")
        if not file_id:
            return []
        raw = service.files().get_media(fileId=file_id).execute()
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[GDrive] drive_load_visits error: {e}")
        return []


def drive_save_visits(visits: list) -> bool:
    """Write visits list to Drive visits.json. Returns True on success."""
    try:
        service, root_id = _get_service()
        content = json.dumps(visits, ensure_ascii=False, indent=2).encode("utf-8")
        _upload_bytes(service, root_id, "visits.json", content, "application/json")
        return True
    except Exception as e:
        print(f"[GDrive] drive_save_visits error: {e}")
        traceback.print_exc()
        return False


def drive_upload_space_files(visit_data: dict) -> dict:
    """Upload diagnostico.json + Excel + Word for a single project.
    Returns dict: {json: bool, excel: bool, docx: bool, errors: [str]}
    """
    results = {"json": False, "excel": False, "docx": False, "errors": []}
    if not visit_data.get("id"):
        results["errors"].append("visit_data sin 'id'")
        return results

    space_name = visit_data.get("proyecto_nombre") or visit_data.get("id", "espacio")
    visit_id   = visit_data["id"]

    try:
        service, root_id = _get_service()
        folders = _get_project_subfolders(service, root_id, space_name, visit_id)
    except Exception as e:
        results["errors"].append(f"Error conectando Drive: {e}")
        return results

    # 1. diagnostico.json
    try:
        content = json.dumps(visit_data, ensure_ascii=False, indent=2).encode("utf-8")
        _upload_bytes(service, folders["diagnostico"],
                      "diagnostico.json", content, "application/json")
        results["json"] = True
    except Exception as e:
        results["errors"].append(f"diagnostico.json: {e}")

    # 2. Excel
    try:
        from utils.report_generator import generate_excel
        xlsx = generate_excel(visit_data)
        safe_sp = _safe_name(space_name, 40)
        _upload_bytes(service, folders["excel"],
                      f"diagnostico_{safe_sp}.xlsx", xlsx,
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        results["excel"] = True
    except Exception as e:
        results["errors"].append(f"Excel: {e}")

    # 3. Word
    try:
        from utils.docx_generator import generate_docx
        docx = generate_docx(visit_data)
        safe_sp = _safe_name(space_name, 40)
        _upload_bytes(service, folders["informe"],
                      f"informe_{safe_sp}.docx", docx,
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        results["docx"] = True
    except Exception as e:
        results["errors"].append(f"Word: {e}")

    return results


def upload_photo_to_space(visit_id: str, space_name: str,
                          filename: str, file_bytes: bytes,
                          mimetype: str = "image/jpeg",
                          label: str = "") -> tuple[bool, str]:
    """Upload photo to fotos/ subfolder. Returns (success, error_msg)."""
    try:
        service, root_id = _get_service()
        folders = _get_project_subfolders(service, root_id, space_name, visit_id)
        _upload_bytes(service, folders["fotos"], filename, file_bytes, mimetype)
        return True, ""
    except Exception as e:
        msg = str(e)
        print(f"[GDrive] upload_photo error: {msg}")
        return False, msg


def list_space_folders() -> list:
    try:
        service, root_id = _get_service()
        q = (f"'{root_id}' in parents and "
             f"mimeType='application/vnd.google-apps.folder' and trashed=false")
        resp = service.files().list(
            q=q, fields="files(id,name,createdTime)",
            orderBy="createdTime desc").execute()
        return resp.get("files", [])
    except Exception as e:
        print(f"[GDrive] list_folders error: {e}")
        return []


# ── Legacy helpers (kept for admin manual sync buttons) ─────────────────────

def sync_visits_to_drive(visits_file: Path) -> bool:
    try:
        with open(visits_file) as f:
            data = json.load(f)
        return drive_save_visits(data)
    except Exception:
        return False


def sync_visits_from_drive(visits_file: Path) -> bool:
    visits = drive_load_visits()
    if not visits and visits != []:
        return False
    visits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(visits_file, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)
    return True
