"""User management — admin panel, multi-user support v5."""
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_DIR   = Path(__file__).parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"

# Built-in admin account — always present
_ADMIN_USER = "francis"
_ADMIN_PASS = "tomates"
_ADMIN_HASH = hashlib.sha256(_ADMIN_PASS.encode()).hexdigest()


def _hash(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()


def _ensure_users_file():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        _write([])


def _load() -> list:
    _ensure_users_file()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _write(users: list):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def authenticate(username: str, password: str) -> dict | None:
    """Returns user dict if valid credentials, else None.
    Admin 'francis' always works with built-in credentials."""
    username = username.strip().lower()
    password = password.strip()

    # Admin check
    if username == _ADMIN_USER and password == _ADMIN_PASS:
        return {
            "username": _ADMIN_USER,
            "role": "admin",
            "display_name": "Francis (Admin)",
            "visit_id": None,
            "space_name": "Administración LivLin",
        }

    # Regular users
    users = _load()
    ph = _hash(password)
    for u in users:
        if u.get("username", "").lower() == username and u.get("password_hash") == ph:
            return u
    return None


def list_spaces() -> list:
    """Return all registered spaces (for admin)."""
    return _load()


def create_space(username: str, password: str, space_name: str,
                 display_name: str = "", visit_id: str = "") -> dict:
    """Create a new space/user. Returns the created user dict."""
    users = _load()
    username = username.strip().lower()

    # Check duplicate
    if any(u.get("username") == username for u in users):
        raise ValueError(f"El usuario '{username}' ya existe.")

    user = {
        "username": username,
        "password_hash": _hash(password),
        "role": "user",
        "display_name": display_name or space_name,
        "space_name": space_name,
        "visit_id": visit_id,
        "created_at": datetime.now().isoformat(),
    }
    users.append(user)
    _write(users)
    return user


def update_space_visit(username: str, visit_id: str):
    """Link a username to a specific visit_id."""
    users = _load()
    for u in users:
        if u.get("username", "").lower() == username.lower():
            u["visit_id"] = visit_id
            break
    _write(users)


def update_password(username: str, new_password: str):
    users = _load()
    for u in users:
        if u.get("username", "").lower() == username.lower():
            u["password_hash"] = _hash(new_password)
            break
    _write(users)


def delete_space(username: str):
    users = _load()
    users = [u for u in users if u.get("username", "").lower() != username.lower()]
    _write(users)
