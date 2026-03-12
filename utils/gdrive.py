"""Google Drive integration v8 — carpeta por proyecto con subcarpetas estructuradas.

Estructura en Drive:
  livlin-datos/                                   ← carpeta raíz compartida
  ├── visits.json                                 ← JSON maestro (todos los diagnósticos)
  └── [NombreEspacio] — [visit_id]/               ← carpeta por proyecto
      ├── fotos/                                  ← imágenes del espacio
      │   ├── 120000_fachada.jpg
      │   └── 130000_jardín.jpg
      ├── diagnostico/                            ← datos del diagnóstico
      │   └── diagnostico.json
      ├── excel/                                  ← informe Excel
      │   └── diagnostico_NombreEspacio.xlsx
      └── informe/                                ← documento Word
          └── informe_NombreEspacio.docx
"""
import json
import io
import re
from pathlib import Path

BASE_DIR    = Path(__file__).parent.parent
CRED_FILE   = BASE_DIR / "credentials" / "gdrive_sa.json"
CONFIG_FILE = BASE_DIR / "credentials" / "gdrive_config.json"

_folder_cache: dict = {}


def is_configured() -> bool:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            return True
    except Exception:
        pass
    return CRED_FILE.exists() and CONFIG_FILE.exists()


def _get_service():
    """Build Drive API service. Returns (service, root_folder_id)."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError("Instala: pip install google-auth google-api-python-client")

    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            cred_dict = dict(st.secrets["gdrive"]["credentials"])
            if "private_key" in cred_dict:
                cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
            folder_id = st.secrets["gdrive"]["folder_id"]
            creds = service_account.Credentials.from_service_account_info(
                cred_dict, scopes=["https://www.googleapis.com/auth/drive"])
            from googleapiclient.discovery import build
            service = build("drive", "v3", credentials=creds, cache_discovery=False)
            return service, folder_id
    except Exception as e:
        print(f"[GDrive] secrets error: {e}")

    if not CRED_FILE.exists():
        raise FileNotFoundError(f"Credenciales no encontradas: {CRED_FILE}")
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config no encontrada: {CONFIG_FILE}")

    with open(CONFIG_FILE) as f:
        config = json.load(f)
    folder_id = config.get("folder_id", "")

    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        str(CRED_FILE), scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    return service, folder_id


def _safe_name(name: str, max_len: int = 80) -> str:
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name).strip()
    return clean[:max_len] if clean else "espacio"


def _get_or_create_folder(service, parent_id: str, name: str) -> str:
    cache_key = f"{parent_id}::{name}"
    if cache_key in _folder_cache:
        return _folder_cache[cache_key]
    q = (f"name='{name}' and '{parent_id}' in parents "
         f"and mimeType='application/vnd.google-apps.folder' and trashed=false")
    resp = service.files().list(q=q, fields="files(id)").execute()
    files = resp.get("files", [])
    if files:
        fid = files[0]["id"]
    else:
        meta = {"name": name, "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id]}
        fid = service.files().create(body=meta, fields="id").execute()["id"]
    _folder_cache[cache_key] = fid
    return fid


def _find_file(service, folder_id: str, filename: str) -> str | None:
    safe_fname = filename.replace("'", "\\'")
    q = f"name='{safe_fname}' and '{folder_id}' in parents and trashed=false"
    resp = service.files().list(q=q, fields="files(id)").execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def _upload_bytes(service, folder_id: str, filename: str,
                  data: bytes, mimetype: str) -> str:
    """Upload or update a file in folder. Returns file ID."""
    from googleapiclient.http import MediaIoBaseUpload
    media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mimetype)
    existing = _find_file(service, folder_id, filename)
    if existing:
        service.files().update(fileId=existing, media_body=media).execute()
        return existing
    meta = {"name": filename, "parents": [folder_id]}
    result = service.files().create(body=meta, media_body=media, fields="id").execute()
    return result["id"]


def _project_folder_name(space_name: str, visit_id: str) -> str:
    safe = _safe_name(space_name or "espacio")
    short = visit_id[-15:] if len(visit_id) > 15 else visit_id
    return f"{safe} — {short}"


def _get_project_subfolders(service, root_id: str,
                             space_name: str, visit_id: str) -> dict:
    """Get or create project folder + all 4 subfolders. Returns dict of folder IDs."""
    proj_name = _project_folder_name(space_name, visit_id)
    proj_id   = _get_or_create_folder(service, root_id, proj_name)
    return {
        "project":     proj_id,
        "fotos":       _get_or_create_folder(service, proj_id, "fotos"),
        "diagnostico": _get_or_create_folder(service, proj_id, "diagnostico"),
        "excel":       _get_or_create_folder(service, proj_id, "excel"),
        "informe":     _get_or_create_folder(service, proj_id, "informe"),
    }


# ── Public API ──────────────────────────────────────────────────────────────

def upload_photo_to_space(visit_id: str, space_name: str,
                          filename: str, file_bytes: bytes,
                          mimetype: str = "image/jpeg",
                          label: str = "") -> str | None:
    """Upload a photo to fotos/ subfolder. Returns Drive file ID."""
    try:
        service, root_id = _get_service()
        folders  = _get_project_subfolders(service, root_id, space_name, visit_id)
        file_id  = _upload_bytes(service, folders["fotos"], filename, file_bytes, mimetype)
        return file_id
    except Exception as e:
        print(f"[GDrive] upload_photo error: {e}")
        return None


def upload_space_json(visit_data: dict) -> bool:
    """Upload diagnostico.json to diagnostico/ subfolder."""
    try:
        service, root_id = _get_service()
        space_name = visit_data.get("proyecto_nombre") or visit_data.get("id", "sin-nombre")
        visit_id   = visit_data.get("id", "")
        if not visit_id:
            return False
        folders  = _get_project_subfolders(service, root_id, space_name, visit_id)
        content  = json.dumps(visit_data, ensure_ascii=False, indent=2).encode("utf-8")
        _upload_bytes(service, folders["diagnostico"], "diagnostico.json",
                      content, "application/json")
        return True
    except Exception as e:
        print(f"[GDrive] upload_space_json error: {e}")
        return False


def upload_space_excel(visit_data: dict) -> bool:
    """Generate Excel report and upload to excel/ subfolder."""
    try:
        from utils.report_generator import generate_excel
        service, root_id = _get_service()
        space_name = visit_data.get("proyecto_nombre") or "espacio"
        visit_id   = visit_data.get("id", "")
        if not visit_id:
            return False
        xlsx_bytes = generate_excel(visit_data)
        safe_sp    = _safe_name(space_name, 40)
        filename   = f"diagnostico_{safe_sp}.xlsx"
        folders    = _get_project_subfolders(service, root_id, space_name, visit_id)
        _upload_bytes(service, folders["excel"], filename, xlsx_bytes,
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return True
    except Exception as e:
        print(f"[GDrive] upload_space_excel error: {e}")
        return False


def upload_space_docx(visit_data: dict) -> bool:
    """Generate Word report and upload to informe/ subfolder."""
    try:
        from utils.docx_generator import generate_docx
        service, root_id = _get_service()
        space_name = visit_data.get("proyecto_nombre") or "espacio"
        visit_id   = visit_data.get("id", "")
        if not visit_id:
            return False
        docx_bytes = generate_docx(visit_data)
        safe_sp    = _safe_name(space_name, 40)
        filename   = f"informe_{safe_sp}.docx"
        folders    = _get_project_subfolders(service, root_id, space_name, visit_id)
        _upload_bytes(service, folders["informe"], filename, docx_bytes,
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        return True
    except Exception as e:
        print(f"[GDrive] upload_space_docx error: {e}")
        return False


def upload_json(data, filename: str = "visits.json") -> bool:
    """Upload/update JSON file to root Drive folder."""
    try:
        service, folder_id = _get_service()
        content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        _upload_bytes(service, folder_id, filename, content, "application/json")
        return True
    except Exception as e:
        print(f"[GDrive] upload_json error: {e}")
        return False


def download_json(filename: str = "visits.json"):
    try:
        service, folder_id = _get_service()
        file_id = _find_file(service, folder_id, filename)
        if not file_id:
            return None
        content = service.files().get_media(fileId=file_id).execute()
        return json.loads(content.decode("utf-8"))
    except Exception as e:
        print(f"[GDrive] download_json error: {e}")
        return None


def sync_visits_to_drive(visits_file: Path) -> bool:
    try:
        with open(visits_file) as f:
            data = json.load(f)
        return upload_json(data, "visits.json")
    except Exception:
        return False


def sync_visits_from_drive(visits_file: Path) -> bool:
    data = download_json("visits.json")
    if data is None:
        return False
    visits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(visits_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def list_space_folders() -> list:
    """List all project folders in the root Drive folder."""
    try:
        service, root_id = _get_service()
        q = (f"'{root_id}' in parents and "
             f"mimeType='application/vnd.google-apps.folder' and trashed=false")
        resp = service.files().list(
            q=q, fields="files(id,name,createdTime)", orderBy="createdTime desc"
        ).execute()
        return resp.get("files", [])
    except Exception as e:
        print(f"[GDrive] list_folders error: {e}")
        return []
