"""Google Drive integration — save/load JSON data and media files v5.

Setup:
1. Create a Google Cloud project and enable the Drive API.
2. Create a Service Account and download the credentials JSON.
3. Place the JSON as credentials/gdrive_sa.json
4. Share the target Drive folder with the service account email.
5. Set GDRIVE_FOLDER_ID in credentials/gdrive_config.json:
   {"folder_id": "your_folder_id_here"}

OR use Streamlit Secrets (for cloud deployment):
   [gdrive]
   enabled = true
   folder_id = "your_folder_id"
   [gdrive.credentials]  <- paste the service account JSON content here
"""
import json
import io
import os
from pathlib import Path

BASE_DIR    = Path(__file__).parent.parent
CRED_FILE   = BASE_DIR / "credentials" / "gdrive_sa.json"
CONFIG_FILE = BASE_DIR / "credentials" / "gdrive_config.json"


def is_configured() -> bool:
    """Check if Google Drive is configured and credentials exist."""
    # Check Streamlit secrets first
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            return True
    except Exception:
        pass
    # Check local files
    return CRED_FILE.exists() and CONFIG_FILE.exists()


def _get_service():
    """Build and return the Drive API service object."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "Google API libraries not installed. Run:\n"
            "pip install google-auth google-api-python-client"
        )

    # Try Streamlit secrets first
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets.get("gdrive", {}).get("enabled"):
            cred_dict = dict(st.secrets["gdrive"]["credentials"])
            folder_id = st.secrets["gdrive"]["folder_id"]
            creds = service_account.Credentials.from_service_account_info(
                cred_dict, scopes=["https://www.googleapis.com/auth/drive"])
            service = build("drive", "v3", credentials=creds)
            return service, folder_id
    except Exception:
        pass

    # Fall back to local files
    if not CRED_FILE.exists():
        raise FileNotFoundError(f"Credenciales no encontradas: {CRED_FILE}")
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config no encontrada: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    folder_id = config.get("folder_id", "")

    creds = service_account.Credentials.from_service_account_file(
        str(CRED_FILE), scopes=["https://www.googleapis.com/auth/drive"])
    service = build("drive", "v3", credentials=creds)
    return service, folder_id


def _find_file(service, folder_id: str, filename: str) -> str | None:
    """Return file ID if filename exists in folder, else None."""
    q = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    resp = service.files().list(q=q, fields="files(id,name)").execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def upload_json(data: dict, filename: str = "visits.json") -> bool:
    """Upload/update a JSON file to Drive. Returns True on success."""
    try:
        service, folder_id = _get_service()
        from googleapiclient.http import MediaIoBaseUpload
        content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        media = MediaIoBaseUpload(io.BytesIO(content), mimetype="application/json")
        file_id = _find_file(service, folder_id, filename)
        if file_id:
            service.files().update(fileId=file_id, media_body=media).execute()
        else:
            meta = {"name": filename, "parents": [folder_id]}
            service.files().create(body=meta, media_body=media,
                                   fields="id").execute()
        return True
    except Exception as e:
        print(f"[GDrive] Upload error: {e}")
        return False


def download_json(filename: str = "visits.json") -> list | None:
    """Download and parse a JSON file from Drive. Returns None on failure."""
    try:
        service, folder_id = _get_service()
        file_id = _find_file(service, folder_id, filename)
        if not file_id:
            return None
        content = service.files().get_media(fileId=file_id).execute()
        return json.loads(content.decode("utf-8"))
    except Exception as e:
        print(f"[GDrive] Download error: {e}")
        return None


def upload_bytes(data: bytes, filename: str, mimetype: str = "application/octet-stream") -> str | None:
    """Upload binary file (e.g. photo). Returns Drive file ID or None."""
    try:
        service, folder_id = _get_service()
        from googleapiclient.http import MediaIoBaseUpload
        media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mimetype)
        file_id = _find_file(service, folder_id, filename)
        if file_id:
            service.files().update(fileId=file_id, media_body=media).execute()
            return file_id
        meta = {"name": filename, "parents": [folder_id]}
        result = service.files().create(body=meta, media_body=media, fields="id").execute()
        return result.get("id")
    except Exception as e:
        print(f"[GDrive] Upload bytes error: {e}")
        return None


def sync_visits_to_drive(visits_file: Path) -> bool:
    """Sync local visits.json to Google Drive."""
    try:
        with open(visits_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return upload_json(data, "visits.json")
    except Exception:
        return False


def sync_visits_from_drive(visits_file: Path) -> bool:
    """Download visits.json from Drive to local file."""
    data = download_json("visits.json")
    if data is None:
        return False
    visits_file.parent.mkdir(parents=True, exist_ok=True)
    with open(visits_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True
