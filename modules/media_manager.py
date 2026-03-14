"""Módulo de Registro Fotográfico v2.0 — fotos guardadas en Supabase + galería + zip."""
import io
import base64
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st
from utils.data_manager import save_visit
from utils.supabase_db import is_configured

PHOTO_CATEGORIES = [
    "General del espacio", "Suelo / tierra", "Vegetación existente",
    "Agua / riego", "Energía / instalaciones", "Materiales disponibles",
    "Fauna observada", "Problemas / desafíos", "Oportunidades identificadas",
    "Antes de la intervención", "Durante el proceso", "Después de la intervención",
    "Otro",
]

# ── Supabase photo helpers ────────────────────────────────────────────────────

def _sb_save_photo(visit_id: str, filename: str, label: str,
                   file_bytes: bytes, mimetype: str) -> bool:
    """Save photo as base64 in Supabase photos table."""
    try:
        from utils.supabase_db import _get_config
        import requests
        url, key = _get_config()
        headers = {
            "apikey": key, "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=representation",
        }
        ts = datetime.now().strftime("%H%M%S")
        photo_id = f"{visit_id}_{ts}_{filename[:30]}"
        payload = {
            "id":       photo_id,
            "visit_id": visit_id,
            "filename": f"{ts}_{filename}",
            "label":    label,
            "mimetype": mimetype,
            "data":     base64.b64encode(file_bytes).decode("utf-8"),
            "created_at": datetime.now().isoformat(),
        }
        r = requests.post(f"{url}/rest/v1/photos", headers=headers,
                          json=payload, timeout=15)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[photos] save error: {e}")
        return False


def _sb_load_photos(visit_id: str) -> list:
    """Load all photos for a visit from Supabase."""
    try:
        from utils.supabase_db import _get_config
        import requests
        url, key = _get_config()
        headers = {"apikey": key, "Authorization": f"Bearer {key}"}
        r = requests.get(
            f"{url}/rest/v1/photos",
            headers=headers,
            params={"visit_id": f"eq.{visit_id}",
                    "select": "id,filename,label,mimetype,data,created_at",
                    "order": "created_at.asc"},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[photos] load error: {e}")
        return []


def _sb_delete_photo(photo_id: str) -> bool:
    try:
        from utils.supabase_db import _get_config
        import requests
        url, key = _get_config()
        headers = {"apikey": key, "Authorization": f"Bearer {key}"}
        r = requests.delete(
            f"{url}/rest/v1/photos",
            headers=headers,
            params={"id": f"eq.{photo_id}"},
            timeout=10,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[photos] delete error: {e}")
        return False


def _tmp_save(visit_id: str, file_bytes: bytes, filename: str, label: str) -> str:
    """Fallback: save to /tmp."""
    from utils.data_manager import save_media_file
    return save_media_file(visit_id, file_bytes, filename, label=label)


def render():
    st.markdown("## 📷 Registro Fotográfico del Espacio")
    st.markdown(
        '<p class="module-subtitle">Documenta el espacio. Las fotos quedan '
        "guardadas en la base de datos del diagnóstico.</p>",
        unsafe_allow_html=True,
    )

    data     = st.session_state.get("visit_data", {})
    visit_id = data.get("id", "")
    if not visit_id:
        st.warning("⚠️ Primero crea o carga un diagnóstico desde el panel de administración.")
        return

    use_supabase = is_configured()

    # ── Tab layout ────────────────────────────────────────────────────────
    tab_cap, tab_gal = st.tabs(["📸 Capturar / Subir", "🖼️ Galería"])

    # ══════════════════════════════════════════════════════════════════════
    with tab_cap:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        up_cat   = st.selectbox("Categoría", PHOTO_CATEGORIES, key="up_cat")
        up_label = st.text_input("Etiqueta adicional (opcional)", key="up_label",
                                 placeholder="Ej: Muro norte, bancal tomates…")
        full_label = up_cat + (f" — {up_label}" if up_label else "")

        col_cam, col_up = st.columns(2)

        with col_cam:
            st.markdown("**📷 Cámara del dispositivo**")
            cam = st.camera_input("Tomar foto", key="cam_input",
                                  label_visibility="collapsed")
            if cam:
                mime = "image/jpeg"
                if st.button("💾 Guardar foto de cámara", type="primary",
                             key="save_cam", use_container_width=True):
                    _do_save(visit_id, cam.getvalue(), "camara.jpg",
                             full_label, mime, use_supabase)
                    st.success("✅ Foto guardada.")
                    st.rerun()

        with col_up:
            st.markdown("**📁 Subir desde dispositivo**")
            uploaded = st.file_uploader(
                "Seleccionar imágenes",
                type=["jpg","jpeg","png","webp"],
                accept_multiple_files=True,
                key="file_uploader",
                label_visibility="collapsed",
            )
            if uploaded:
                if st.button(f"💾 Guardar {len(uploaded)} imagen(es)",
                             type="primary", key="save_up",
                             use_container_width=True):
                    for uf in uploaded:
                        ext  = Path(uf.name).suffix.lower()
                        mime = {"jpg":"image/jpeg","jpeg":"image/jpeg",
                                "png":"image/png","webp":"image/webp"}.get(
                                    ext.lstrip("."), "image/jpeg")
                        _do_save(visit_id, uf.getvalue(), uf.name,
                                 full_label, mime, use_supabase)
                    st.success(f"✅ {len(uploaded)} imagen(es) guardada(s).")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        if not use_supabase:
            st.info("ℹ️ Supabase no configurado — las fotos se guardan temporalmente "
                    "en /tmp y se perderán al reiniciar la app.")

    # ══════════════════════════════════════════════════════════════════════
    with tab_gal:
        photos = _sb_load_photos(visit_id) if use_supabase else _tmp_photos(visit_id)

        if not photos:
            st.info("📭 Sin fotos registradas para este diagnóstico todavía.")
        else:
            st.markdown(f"**{len(photos)} foto(s) registrada(s)**")

            # ── Zip download ──────────────────────────────────────────────
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for ph in photos:
                    raw = base64.b64decode(ph["data"]) if use_supabase else _read_tmp_photo(ph)
                    if raw:
                        zf.writestr(ph["filename"], raw)
            zip_buf.seek(0)
            space_name = (data.get("proyecto_nombre","espacio")
                         .replace(" ","_").replace("/","_"))
            st.download_button(
                "⬇️ Descargar todas las fotos (.zip)",
                data=zip_buf.getvalue(),
                file_name=f"fotos_{space_name}.zip",
                mime="application/zip",
                use_container_width=True,
            )

            st.markdown("---")

            # ── Gallery grid ──────────────────────────────────────────────
            cols = st.columns(3)
            for idx, ph in enumerate(photos):
                raw = base64.b64decode(ph["data"]) if use_supabase else _read_tmp_photo(ph)
                if not raw:
                    continue
                with cols[idx % 3]:
                    st.image(raw, caption=ph.get("label",""), use_container_width=True)
                    created = str(ph.get("created_at",""))[:16].replace("T"," ")
                    st.caption(f"🕐 {created}")
                    if st.button("🗑️", key=f"del_{ph['id']}_{idx}",
                                 help="Eliminar foto"):
                        if use_supabase:
                            _sb_delete_photo(ph["id"])
                        st.rerun()


def _do_save(visit_id, file_bytes, filename, label, mime, use_supabase):
    if use_supabase:
        _sb_save_photo(visit_id, filename, label, file_bytes, mime)
    else:
        _tmp_save(visit_id, file_bytes, filename, label)


def _tmp_photos(visit_id: str) -> list:
    """Load photos from /tmp for offline mode."""
    from utils.data_manager import MEDIA_DIR
    folder = MEDIA_DIR / visit_id
    if not folder.exists():
        return []
    photos = []
    for f in sorted(folder.iterdir()):
        if f.suffix.lower() in (".jpg",".jpeg",".png",".webp"):
            try:
                raw = f.read_bytes()
                photos.append({
                    "id":       f.name,
                    "filename": f.name,
                    "label":    "",
                    "mimetype": "image/jpeg",
                    "data":     base64.b64encode(raw).decode(),
                    "created_at": "",
                })
            except Exception:
                pass
    return photos


def _read_tmp_photo(ph: dict) -> bytes | None:
    try:
        return base64.b64decode(ph["data"])
    except Exception:
        return None
