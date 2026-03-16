"""User management v6.0 — Supabase como fuente de verdad para usuarios.
Fallback a users.json local si Supabase no está disponible.
Los usuarios persisten entre redeploys en Streamlit Cloud.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime

BASE_DIR   = Path(__file__).parent.parent
USERS_FILE = BASE_DIR / "data" / "users.json"

_ADMIN_USER = "francis"
_ADMIN_PASS = "tomates"


def _hash(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()


# ── Supabase backend ──────────────────────────────────────────────────────────

def _sb_configured() -> bool:
    try:
        from utils.supabase_db import is_configured
        return is_configured()
    except Exception:
        return False


def _sb_load_all() -> list:
    """Load all users from Supabase users table."""
    try:
        from utils.supabase_db import _get_config, _headers
        import requests
        url, key = _get_config()
        r = requests.get(
            f"{url}/rest/v1/users",
            headers=_headers(key),
            params={"select": "*", "order": "created_at.asc"},
            timeout=8,
        )
        r.raise_for_status()
        rows = r.json()
        # Convert DB rows to user dicts
        users = []
        for row in rows:
            users.append({
                "username":      row.get("username", ""),
                "password_hash": row.get("password_hash", ""),
                "role":          row.get("role", "user"),
                "display_name":  row.get("display_name", ""),
                "space_name":    row.get("space_name", ""),
                "visit_id":      row.get("visit_id"),
                "created_at":    str(row.get("created_at", "")),
            })
        return users
    except Exception as e:
        print(f"[users] Supabase load error: {e}")
        return []


def _sb_upsert(user: dict) -> bool:
    """Insert or update a user in Supabase."""
    try:
        from utils.supabase_db import _get_config, _headers
        import requests
        url, key = _get_config()
        payload = {
            "username":      user["username"],
            "password_hash": user["password_hash"],
            "role":          user.get("role", "user"),
            "display_name":  user.get("display_name", ""),
            "space_name":    user.get("space_name", ""),
            "visit_id":      user.get("visit_id"),
            "updated_at":    datetime.now().isoformat(),
        }
        hdrs = _headers(key)
        hdrs["Prefer"] = "resolution=merge-duplicates,return=representation"
        r = requests.post(
            f"{url}/rest/v1/users",
            headers=hdrs,
            json=payload,
            timeout=8,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[users] Supabase upsert error: {e}")
        return False


def _sb_delete(username: str) -> bool:
    try:
        from utils.supabase_db import _get_config, _headers
        import requests
        url, key = _get_config()
        r = requests.delete(
            f"{url}/rest/v1/users",
            headers=_headers(key),
            params={"username": f"eq.{username}"},
            timeout=8,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[users] Supabase delete error: {e}")
        return False


# ── Local JSON fallback ───────────────────────────────────────────────────────

def _local_load() -> list:
    try:
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if USERS_FILE.exists():
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        pass
    return []


def _local_write(users: list):
    try:
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _get_cache() -> list | None:
    try:
        import streamlit as st
        return st.session_state.get("_users_cache")
    except Exception:
        return None


def _set_cache(users: list):
    try:
        import streamlit as st
        st.session_state["_users_cache"] = users
    except Exception:
        pass


def _invalidate_cache():
    try:
        import streamlit as st
        st.session_state.pop("_users_cache", None)
    except Exception:
        pass


# ── Public API ────────────────────────────────────────────────────────────────

def _load() -> list:
    """Load users. Priority: session cache → Supabase → local JSON."""
    cached = _get_cache()
    if cached is not None:
        return cached
    if _sb_configured():
        users = _sb_load_all()
        if users:
            _set_cache(users)
            _local_write(users)  # keep local copy as backup
            return users
    # Fallback to local
    users = _local_load()
    _set_cache(users)
    return users


def authenticate(username: str, password: str) -> dict | None:
    """Returns user dict if valid credentials, else None."""
    username = username.strip().lower()
    password = password.strip()

    # Built-in admin (always works)
    if username == _ADMIN_USER and password == _ADMIN_PASS:
        return {
            "username":     _ADMIN_USER,
            "role":         "admin",
            "display_name": "Francis (Admin)",
            "visit_id":     None,
            "space_name":   "Administración LivLin",
        }

    ph = _hash(password)
    users = _load()
    for u in users:
        if u.get("username", "").lower() == username and u.get("password_hash") == ph:
            return u
    return None


def list_spaces() -> list:
    """Return all registered spaces."""
    return _load()


def create_space(username: str, password: str, space_name: str,
                 display_name: str = "", visit_id: str = "") -> dict:
    """Create a new space/user. Saves to Supabase + local."""
    _invalidate_cache()
    users = _load()
    username = username.strip().lower()

    if any(u.get("username") == username for u in users):
        raise ValueError(f"El usuario '{username}' ya existe.")

    user = {
        "username":      username,
        "password_hash": _hash(password),
        "role":          "user",
        "display_name":  display_name or space_name,
        "space_name":    space_name,
        "visit_id":      visit_id,
        "created_at":    datetime.now().isoformat(),
    }

    # Save to Supabase first (source of truth)
    if _sb_configured():
        ok = _sb_upsert(user)
        if not ok:
            raise ValueError("No se pudo guardar el usuario en Supabase. Verifica la conexión.")

    # Save to local JSON as backup
    users.append(user)
    _local_write(users)
    _set_cache(users)
    return user


def update_space_visit(username: str, visit_id: str):
    """Link a username to a specific visit_id."""
    _invalidate_cache()
    users = _load()
    for u in users:
        if u.get("username", "").lower() == username.lower():
            u["visit_id"] = visit_id
            if _sb_configured():
                _sb_upsert(u)
            break
    _local_write(users)
    _set_cache(users)


def update_password(username: str, new_password: str):
    _invalidate_cache()
    users = _load()
    for u in users:
        if u.get("username", "").lower() == username.lower():
            u["password_hash"] = _hash(new_password)
            if _sb_configured():
                _sb_upsert(u)
            break
    _local_write(users)
    _set_cache(users)


def delete_space(username: str):
    _invalidate_cache()
    users = _load()
    users = [u for u in users if u.get("username", "").lower() != username.lower()]
    if _sb_configured():
        _sb_delete(username)
    _local_write(users)
    _set_cache(users)


def refresh_from_supabase():
    """Force reload users from Supabase (call after login or admin actions)."""
    _invalidate_cache()
    if _sb_configured():
        users = _sb_load_all()
        _set_cache(users)
        _local_write(users)
        return users
    return _local_load()
