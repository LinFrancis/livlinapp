"""Módulo de Registro Fotográfico — cámara, subida de archivos y galería.

Permite tomar fotos directamente desde el celular (usando st.camera_input),
subir imágenes existentes, y organizarlas con etiquetas por visita.

Opcional: integración con Google Drive (requiere archivo credentials/gdrive_sa.json).
"""
import io
import os
from pathlib import Path

import streamlit as st

from utils.data_manager import (
    save_media_file,
    list_media_files,
    delete_media_file,
    save_visit,
)

# Etiquetas de categorías para las fotos
PHOTO_CATEGORIES = [
    "General del espacio",
    "Suelo / tierra",
    "Vegetación existente",
    "Agua / riego",
    "Energía / instalaciones",
    "Materiales disponibles",
    "Fauna observada",
    "Problemas / desafíos",
    "Oportunidades identificadas",
    "Antes de la intervención",
    "Durante el proceso",
    "Después de la intervención",
    "Otro",
]

GDRIVE_CREDS = Path(__file__).parent.parent / "credentials" / "gdrive_sa.json"


def render():
    st.markdown("## 📷 Registro Fotográfico del Espacio")
    st.markdown(
        '<p class="module-subtitle">Documenta el espacio con fotos tomadas desde el celular '
        "o subidas desde el dispositivo. Las imágenes quedan registradas junto al diagnóstico.</p>",
        unsafe_allow_html=True,
    )

    data = st.session_state.visit_data
    visit_id = data.get("id", "sin_guardar")

    if visit_id == "sin_guardar":
        st.warning(
            "⚠️ Primero guarda al menos el **Módulo 1** para asociar las fotos a esta visita."
        )
        return

    tab1, tab2, tab3 = st.tabs(
        ["📸 Tomar foto", "📁 Subir archivo", "🖼️ Galería"]
    )

    # ── TAB 1: Cámara ──────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Tomar foto con el celular o cámara")
        st.caption(
            "Desde el celular, al presionar el ícono de cámara se abrirá la cámara. "
            "Desde el computador, usará la cámara web."
        )

        cam_cat = st.selectbox(
            "Categoría de la foto",
            PHOTO_CATEGORIES,
            key="cam_category",
        )
        cam_label = st.text_input(
            "Descripción (opcional)",
            placeholder="Ej: Esquina noroeste con suelo compactado y sin vegetación…",
            key="cam_label",
        )

        camera_image = st.camera_input(
            "Capturar imagen",
            key="camera_widget",
        )

        if camera_image is not None:
            fname = f"camara_{cam_cat.lower().replace(' ', '_')}.jpg"
            full_label = f"{cam_cat}" + (f" — {cam_label}" if cam_label else "")
            filepath = save_media_file(
                visit_id,
                camera_image.getvalue(),
                fname,
                label=full_label,
            )
            st.success(f"✅ Foto guardada: {full_label}")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 2: Subir archivo ───────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Subir fotos desde el dispositivo")

        up_cat = st.selectbox(
            "Categoría de las fotos",
            PHOTO_CATEGORIES,
            key="upload_category",
        )
        up_label = st.text_input(
            "Descripción (opcional)",
            placeholder="Ej: Vista aérea desde el balcón…",
            key="upload_label",
        )

        uploaded_files = st.file_uploader(
            "Seleccionar imágenes (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            key="file_uploader",
        )

        if uploaded_files:
            if st.button("💾 Guardar imágenes seleccionadas", type="primary"):
                full_label = f"{up_cat}" + (f" — {up_label}" if up_label else "")
                n_saved = 0
                for uf in uploaded_files:
                    save_media_file(
                        visit_id,
                        uf.getvalue(),
                        uf.name,
                        label=full_label,
                    )
                    n_saved += 1
                st.success(f"✅ {n_saved} imagen(es) guardada(s) correctamente.")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Google Drive opcional ──────────────────────────────────────────
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### ☁️ Sincronizar con Google Drive *(opcional)*")

        if GDRIVE_CREDS.exists():
            gdrive_status = "✅ Credenciales configuradas"
            gdrive_ok = True
        else:
            gdrive_status = "⚙️ No configurado"
            gdrive_ok = False

        st.caption(f"Estado: {gdrive_status}")

        if gdrive_ok:
            gdrive_folder_id = st.text_input(
                "ID de la carpeta de Drive de destino",
                value=data.get("gdrive_folder_id", ""),
                placeholder="Ej: 1A2B3C4D5E6F7G…",
                key="gdrive_folder",
            )
            data["gdrive_folder_id"] = gdrive_folder_id
            if st.button("☁️ Subir fotos a Google Drive", type="primary"):
                _upload_to_drive(visit_id, gdrive_folder_id)
        else:
            st.markdown(
                """
                **Para activar la sincronización con Google Drive:**

                1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
                2. Crea un proyecto → activa la *Google Drive API*
                3. Crea una **cuenta de servicio** y descarga el JSON de credenciales
                4. Renómbralo a `gdrive_sa.json` y colócalo en la carpeta `credentials/`
                5. Comparte la carpeta de Drive con el email de la cuenta de servicio
                6. Reinicia la aplicación

                Las fotos locales siempre quedan guardadas en `data/media/{id_visita}/`
                """
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: Galería ─────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🖼️ Galería de fotos de esta visita")

        media_files = list_media_files(visit_id)

        if not media_files:
            st.info("No hay fotos registradas aún para este diagnóstico.")
        else:
            st.caption(f"{len(media_files)} foto(s) registrada(s)")
            cols_per_row = 3
            rows = [
                media_files[i : i + cols_per_row]
                for i in range(0, len(media_files), cols_per_row)
            ]
            for row in rows:
                row_cols = st.columns(cols_per_row)
                for j, item in enumerate(row):
                    with row_cols[j]:
                        try:
                            with open(item["path"], "rb") as f:
                                img_bytes = f.read()
                            st.image(img_bytes, use_container_width=True)
                            st.caption(item["label"] or item["filename"])
                            if st.button(
                                "🗑️ Eliminar",
                                key=f"del_{item['filename']}",
                                use_container_width=True,
                            ):
                                delete_media_file(visit_id, item["filename"])
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)


def _upload_to_drive(visit_id: str, folder_id: str):
    """Intenta subir las fotos locales a Google Drive via service account."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = service_account.Credentials.from_service_account_file(
            str(GDRIVE_CREDS),
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        service = build("drive", "v3", credentials=creds)

        files = list_media_files(visit_id)
        if not files:
            st.info("No hay fotos para subir.")
            return

        progress = st.progress(0)
        for i, item in enumerate(files):
            file_metadata = {
                "name": item["filename"],
                "parents": [folder_id],
            }
            media = MediaFileUpload(item["path"], mimetype="image/jpeg")
            service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
            progress.progress((i + 1) / len(files))

        st.success(f"✅ {len(files)} foto(s) subida(s) a Google Drive.")
    except ImportError:
        st.error(
            "Instala las dependencias: `pip install google-auth google-api-python-client`"
        )
    except Exception as e:
        st.error(f"Error al subir a Drive: {e}")
