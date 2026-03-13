"""Google Drive integration v10 — OAuth con cuenta de usuario como fuente de verdad.

Soporta dos modos de autenticación (detectado automáticamente desde secrets):
  - auth_type = "oauth"          → refresh_token del usuario (RECOMENDADO)
  - auth_type = "service_account"→ cuenta de servicio (solo lectura de carpetas funciona)

Estructura en Drive:
  livlin-datos/
  ├── visits.json
  └── [NombreEspacio] — [visit_id]/
      ├── fotos/
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
_service_cache = None


def is_configured() -> bool:
    try:
        import streamlit as st
        cfg = st.secrets.get("gdrive", {})
        if cfg.get("enabled"):
            return True
    except Exception:
        pass
    return CRED_FILE.exists() and CONFIG_FILE.exists()


def _get_auth_type() -> str:
    """Returns 'oauth', 'service_account', or 'local'."""
    try:
        import streamlit as st
        cfg = st.secrets.get("gdrive", {})
        if cfg.get("enabled"):
            return cfg.get("auth_type", "service_account")
    except Exception:
        pass
    if CRED_FILE.exists():
        return "local_service_account"
    return "none"


def _build_oauth_credentials():
    """Build credentials from OAuth refresh token stored in secrets."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    import streamlit as st

    oauth = dict(st.secrets["gdrive"]["oauth"])
    creds = Credentials(
        token=None,
        refresh_token=oauth["refresh_token"],
        token_uri=oauth.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=oauth["client_id"],
        client_secret=oauth["client_secret"],
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    # Refresh to get a valid access token
    creds.refresh(Request())
    return creds


def _build_service_account_credentials():
    """Build credentials from service account stored in secrets."""
    from google.oauth2 import service_account
    import streamlit as st

    cred_dict = dict(st.secrets["gdrive"]["credentials"])
    if "private_key" in cred_dict:
        pk = cred_dict["private_key"]
        if "\\n" in pk and "\n" not in pk:
            pk = pk.replace("\\n", "\n")
        cred_dict["private_key"] = pk
    return service_account.Credentials.from_service_account_info(
        cred_dict, scopes=["https://www.googleapis.com/auth/drive"])


def _get_service():
    """Build and cache Drive API service. Returns (service, root_folder_id)."""
    global _service_cache
    if _service_cache is not None:
        # Refresh OAuth token if needed
        try:
            creds = _service_cache[2]  # stored as (service, folder_id, creds)
            if hasattr(creds, "expired") and creds.expired:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
        except Exception:
            pass
        return _service_cache[0], _service_cache[1]

    try:
        from googleapiclient.discovery import build
        import streamlit as st
        cfg = st.secrets.get("gdrive", {})
        folder_id = cfg.get("folder_id", "")
        auth_type = cfg.get("auth_type", "service_account")

        if auth_type == "oauth":
            creds = _build_oauth_credentials()
        else:
            creds = _build_service_account_credentials()

        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        _service_cache = (service, folder_id, creds)
        return service, folder_id

    except Exception as e:
        # Local file fallback
        if CRED_FILE.exists() and CONFIG_FILE.exists():
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            with open(CONFIG_FILE) as f:
                config = json.load(f)
            folder_id = config.get("folder_id", "")
            creds = service_account.Credentials.from_service_account_file(
                str(CRED_FILE), scopes=["https://www.googleapis.com/auth/drive"])
            service = build("drive", "v3", credentials=creds, cache_discovery=False)
            _service_cache = (service, folder_id, creds)
            return service, folder_id
        raise RuntimeError(f"No se pudo conectar a Drive: {e}")


def get_drive_status() -> dict:
    """Test Drive connection. Returns {ok, folder_id, auth_type, email, error}."""
    try:
        auth_type = _get_auth_type()
        service, root_id = _get_service()
        about = service.about().get(fields="user,storageQuota").execute()
        email = about.get("user", {}).get("emailAddress", "?")
        quota = about.get("storageQuota", {})
        used  = round(int(quota.get("usage", 0)) / (1024**3), 2)
        total = round(int(quota.get("limit", 1)) / (1024**3), 0)
        return {
            "ok": True, "folder_id": root_id,
            "auth_type": auth_type, "email": email,
            "used_gb": used, "total_gb": total, "error": None
        }
    except Exception as e:
        return {"ok": False, "folder_id": None,
                "auth_type": _get_auth_type(), "error": str(e)}


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
    """Upload or overwrite a file. Raises on failure."""
    from googleapiclient.http import MediaIoBaseUpload
    media    = MediaIoBaseUpload(io.BytesIO(data), mimetype=mimetype, resumable=False)
    existing = _find_file(service, folder_id, filename)
    if existing:
        service.files().update(fileId=existing, media_body=media).execute()
        return existing
    meta   = {"name": filename, "parents": [folder_id]}
    result = service.files().create(body=meta, media_body=media, fields="id").execute()
    return result["id"]


def _project_folder_name(space_name: str, visit_id: str) -> str:
    safe  = _safe_name(space_name or "espacio")
    short = visit_id[-15:] if len(visit_id) > 15 else visit_id
    return f"{safe} — {short}"


def _get_project_subfolders(service, root_id: str,
                             space_name: str, visit_id: str) -> dict:
    proj_name = _project_folder_name(space_name, visit_id)
    proj_id   = _get_or_create_folder(service, root_id, proj_name)
    return {
        "project":     proj_id,
        "fotos":       _get_or_create_folder(service, proj_id, "fotos"),
        "diagnostico": _get_or_create_folder(service, proj_id, "diagnostico"),
        "excel":       _get_or_create_folder(service, proj_id, "excel"),
        "informe":     _get_or_create_folder(service, proj_id, "informe"),
    }


# ── Primary data operations ──────────────────────────────────────────────────

def drive_load_visits() -> list:
    try:
        service, root_id = _get_service()
        file_id = _find_file(service, root_id, "visits.json")
        if not file_id:
            return []
        raw  = service.files().get_media(fileId=file_id).execute()
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[GDrive] drive_load_visits error: {e}")
        return []


def drive_save_visits(visits: list) -> bool:
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
    """Upload diagnostico.json + Excel + Word. Returns {json, excel, docx, errors}."""
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
        xlsx    = generate_excel(visit_data)
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
        docx    = generate_docx(visit_data)
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
                          label: str = "") -> tuple:
    try:
        service, root_id = _get_service()
        folders = _get_project_subfolders(service, root_id, space_name, visit_id)
        _upload_bytes(service, folders["fotos"], filename, file_bytes, mimetype)
        return True, ""
    except Exception as e:
        return False, str(e)


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


# ── Legacy compat ─────────────────────────────────────────────────────────────

def sync_visits_to_drive(visits_file: Path) -> bool:
    try:
        with open(visits_file) as f:
            data = json.load(f)
        return drive_save_visits(data)
    except Exception:
        return False


def sync_visits_from_drive(visits_file: Path) -> bool:
    visits = drive_load_visits()
    if visits is None:
        return False
    visits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(visits_file, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)
    return True
