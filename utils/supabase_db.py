"""Supabase backend v12 — fuente de verdad para diagnósticos LivLin.

Tabla: visits
  id         text PRIMARY KEY   — visit id, e.g. "visit_20250313_143022"
  data       jsonb              — diagnóstico completo
  updated_at timestamptz        — auto-updated

Todas las operaciones usan la REST API de Supabase (sin SDK extra).
Solo requiere: requests (ya en requirements.txt)
"""
import json
import requests
from datetime import datetime, timezone

# ── Configuración ────────────────────────────────────────────────────────────

def _get_config() -> tuple[str, str]:
    """Returns (url, key). Raises if not configured."""
    try:
        import streamlit as st
        cfg = st.secrets.get("supabase", {})
        url = cfg.get("url", "").rstrip("/")
        key = cfg.get("key", "")
        if url and key:
            return url, key
    except Exception:
        pass
    raise RuntimeError("Supabase no configurado. Agrega [supabase] url y key en Streamlit secrets.")


def is_configured() -> bool:
    try:
        _get_config()
        return True
    except Exception:
        return False


def _headers(key: str) -> dict:
    return {
        "apikey":        key,
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
        "Prefer":        "return=representation",
    }


# ── CRUD ─────────────────────────────────────────────────────────────────────

def load_all_visits() -> list:
    """Load all visits from Supabase. Returns list of visit dicts."""
    try:
        url, key = _get_config()
        r = requests.get(
            f"{url}/rest/v1/visits",
            headers=_headers(key),
            params={"select": "data", "order": "updated_at.desc"},
            timeout=10,
        )
        r.raise_for_status()
        rows = r.json()
        return [row["data"] for row in rows if row.get("data")]
    except Exception as e:
        print(f"[Supabase] load_all_visits error: {e}")
        return []


def upsert_visit(visit_data: dict) -> bool:
    """Insert or update a single visit. Returns True on success."""
    try:
        url, key = _get_config()
        visit_id = visit_data.get("id", "")
        if not visit_id:
            return False
        payload = {
            "id":         visit_id,
            "data":       visit_data,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        hdrs = _headers(key)
        hdrs["Prefer"] = "resolution=merge-duplicates,return=representation"
        r = requests.post(
            f"{url}/rest/v1/visits",
            headers=hdrs,
            json=payload,
            timeout=10,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[Supabase] upsert_visit error: {e}")
        return False


def delete_visit_db(visit_id: str) -> bool:
    try:
        url, key = _get_config()
        r = requests.delete(
            f"{url}/rest/v1/visits",
            headers=_headers(key),
            params={"id": f"eq.{visit_id}"},
            timeout=10,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[Supabase] delete_visit error: {e}")
        return False


def get_visit_db(visit_id: str) -> dict | None:
    try:
        url, key = _get_config()
        r = requests.get(
            f"{url}/rest/v1/visits",
            headers=_headers(key),
            params={"id": f"eq.{visit_id}", "select": "data"},
            timeout=10,
        )
        r.raise_for_status()
        rows = r.json()
        return rows[0]["data"] if rows else None
    except Exception as e:
        print(f"[Supabase] get_visit error: {e}")
        return None


def test_connection() -> dict:
    """Test Supabase connection. Returns {ok, url, count, error}."""
    try:
        url, key = _get_config()
        r = requests.get(
            f"{url}/rest/v1/visits",
            headers={**_headers(key), "Prefer": "count=exact"},
            params={"select": "id", "limit": "1"},
            timeout=8,
        )
        r.raise_for_status()
        count_hdr = r.headers.get("content-range", "?")
        return {"ok": True, "url": url, "count": count_hdr, "error": None}
    except Exception as e:
        return {"ok": False, "url": "", "count": 0, "error": str(e)}
