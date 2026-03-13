"""Panel de Administración v6 — Gestión de espacios, primera acción = crear espacio."""
import streamlit as st
from utils.users import list_spaces, create_space, delete_space, update_password
from utils.data_manager import save_visit, load_visits, DATA_FILE, get_visit, _invalidate_cache
from utils.gdrive import (is_configured, get_drive_status, sync_visits_to_drive,
                           sync_visits_from_drive, drive_load_visits, drive_save_visits,
                           drive_upload_space_files, list_space_folders)


def render():
    st.markdown("## ⚙️ Panel de Administración — LivLin")
    st.markdown('<p class="module-subtitle">Gestión de espacios, usuarios y sincronización con Google Drive.</p>',
                unsafe_allow_html=True)

    user = st.session_state.get("current_user", {})
    if user.get("role") != "admin":
        st.error("⚠️ Acceso restringido — solo administradores.")
        return

    # ── PRIMERA ACCIÓN: Crear nuevo espacio ──────────────────────────────
    st.markdown(
        '<div style="background:linear-gradient(135deg,#E8F5E9,#D8F3DC);border:2px solid #52B788;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;">'
        '<div style="font-size:1.1rem;font-weight:800;color:#1B4332;margin-bottom:0.3rem;">🌿 Nuevo Diagnóstico / Espacio</div>'
        '<div style="font-size:0.85rem;color:#2D6A4F;">Crea un nuevo perfil de espacio antes de comenzar la visita. '
        'Esto genera el diagnóstico y el acceso para el grupo.</div>'
        '</div>', unsafe_allow_html=True)

    with st.expander("➕ Crear nuevo espacio y usuario", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            new_space   = st.text_input("🏡 Nombre del espacio *", placeholder="Ej: Casa de Felipe y familia",
                                        key="new_space")
            new_user    = st.text_input("👤 Nombre de usuario *", placeholder="Ej: primofelipe",
                                        key="new_user",
                                        help="Solo minúsculas, sin espacios. El grupo usará esto para entrar.")
        with c2:
            new_pass    = st.text_input("🔑 Contraseña *", placeholder="Ej: familia123", key="new_pass",
                                        help="El grupo usará esta contraseña para acceder a su diagnóstico.")
            new_display = st.text_input("📛 Nombre para mostrar", placeholder="Ej: Felipe, María y Tomás",
                                        key="new_display")
            new_ciudad  = st.text_input("📍 Ciudad / barrio", placeholder="Ej: Santiago, Barrio Italia",
                                        key="new_ciudad")

        col_btn, col_tip = st.columns([1, 2])
        with col_btn:
            crear = st.button("✅ Crear espacio", type="primary", use_container_width=True, key="btn_create_space")
        with col_tip:
            st.caption("Después de crear el espacio, podrás ir a 📋 M1 para comenzar el diagnóstico de ese espacio.")

        if crear:
            if not new_user.strip() or not new_pass.strip() or not new_space.strip():
                st.error("⚠️ Nombre del espacio, usuario y contraseña son obligatorios.")
            elif " " in new_user.strip():
                st.error("⚠️ El nombre de usuario no puede contener espacios.")
            else:
                try:
                    blank = {
                        "proyecto_nombre": new_space.strip(),
                        "proyecto_cliente": new_display.strip() or new_user.strip(),
                        "proyecto_ciudad": new_ciudad.strip(),
                    }
                    vid = save_visit(blank)
                    blank["id"] = vid
                    create_space(
                        username=new_user.strip().lower(),
                        password=new_pass.strip(),
                        space_name=new_space.strip(),
                        display_name=new_display.strip(),
                        visit_id=vid,
                    )
                    st.success(f"✅ Espacio **{new_space}** creado. Usuario: `{new_user}` · ID: `{vid}`")
                    # Load this new visit
                    st.session_state.visit_data = blank
                    st.markdown(
                        '<div class="info-box">💡 Espacio cargado. Ve a <strong>📋 M1 · Información + Intención</strong> '
                        'para comenzar el diagnóstico.</div>', unsafe_allow_html=True)
                    if st.button("📋 Ir al Módulo 1 →", type="primary", key="goto_m1_after_create"):
                        st.session_state.page = "client"
                        st.rerun()
                except ValueError as e:
                    st.error(str(e))

    st.markdown("---")

    # ── Tabs: Espacios | Drive | Diagnósticos ────────────────────────────
    tab1, tab2, tab3 = st.tabs(["👥 Espacios y Usuarios", "☁️ Google Drive", "📊 Todos los Diagnósticos"])

    with tab1:
        spaces = list_spaces()
        if not spaces:
            st.info("Sin espacios registrados aún. Crea el primero arriba.")
        else:
            st.markdown(f"**{len(spaces)} espacio(s) registrado(s):**")
            for sp in spaces:
                with st.expander(f"🏡 **{sp.get('space_name','?')}** · `{sp.get('username','?')}`"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"**Usuario:** `{sp.get('username','')}`")
                        st.markdown(f"**Espacio:** {sp.get('space_name','')}")
                        st.markdown(f"**Display:** {sp.get('display_name','')}")
                    with c2:
                        st.markdown(f"**Visit ID:** `{sp.get('visit_id','')}`")
                        st.markdown(f"**Creado:** {str(sp.get('created_at',''))[:10]}")
                    with c3:
                        new_pw = st.text_input("Nueva contraseña", key=f"npw_{sp['username']}",
                                               placeholder="Nueva contraseña")
                        cc1, cc2, cc3 = st.columns(3)
                        with cc1:
                            if st.button("🔑", key=f"chpw_{sp['username']}", help="Cambiar contraseña"):
                                if new_pw.strip():
                                    update_password(sp["username"], new_pw.strip())
                                    st.success("✅")
                        with cc2:
                            if st.button("📂", key=f"load_{sp['username']}", help="Cargar este diagnóstico"):
                                v = get_visit(sp.get("visit_id",""))
                                if v:
                                    st.session_state.visit_data = v
                                    st.session_state.page = "client"
                                    st.rerun()
                        with cc3:
                            if st.button("🗑️", key=f"del_{sp['username']}", help="Eliminar espacio"):
                                delete_space(sp["username"])
                                st.rerun()

    with tab2:
        st.markdown("### ☁️ Sincronización con Google Drive")
        gdrive_ok = is_configured()

        if gdrive_ok:
            status = get_drive_status()
            if status["ok"]:
                auth_label = "🔑 OAuth (cuenta personal)" if status.get("auth_type") == "oauth" else "🤖 Cuenta de servicio"
                st.success(f"✅ Google Drive conectado — {auth_label}")
                st.caption(f"Cuenta: {status.get('email','?')} · {status.get('used_gb',0)} GB usados / {status.get('total_gb',0)} GB")
                st.caption(f"Carpeta raíz ID: `{status['folder_id']}`")
                if status.get("auth_type") != "oauth":
                    st.warning("⚠️ Estás usando cuenta de servicio. Las cuentas de servicio NO pueden crear archivos (sin cuota de almacenamiento). Debes migrar a OAuth. Ejecuta `get_oauth_token.py` y actualiza los secrets.")
            else:
                st.error(f"❌ Error de conexión: {status['error']}")
            st.markdown(
                '<div class="info-box">📁 Cada espacio tiene su propia carpeta en Drive con '
                'su <code>diagnostico.json</code> y subcarpeta <code>fotos/</code>. '
                'Además se mantiene un <code>visits.json</code> maestro en la raíz.</div>',
                unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("⬆️ Forzar subida", use_container_width=True, type="primary",
                             help="Sube el visits.json local a Drive"):
                    visits = load_visits()
                    ok = drive_save_visits(visits)
                    st.success("✅ Subido correctamente.") if ok else st.error("❌ Error al subir.")
            with c2:
                if st.button("⬇️ Recargar desde Drive", use_container_width=True,
                             help="Descarga datos de Drive y actualiza la sesión"):
                    visits = drive_load_visits()
                    if visits is not None:
                        _invalidate_cache()
                        st.session_state["_visits_cache"] = visits
                        st.success(f"✅ {len(visits)} diagnóstico(s) cargado(s) desde Drive.")
                    else:
                        st.error("❌ No se pudo leer desde Drive.")
            with c3:
                if st.button("🔄 Limpiar caché", use_container_width=True,
                             help="Fuerza recarga desde Drive en próxima acción"):
                    _invalidate_cache()
                    st.session_state.pop("_drive_status_cache", None)
                    st.success("✅ Caché limpiado. Se recargará desde Drive.")

            st.markdown("---")
            st.markdown(
                '<div class="info-box">📁 <strong>Estructura por proyecto en Drive:</strong><br>'
                '<code>[Nombre Espacio] — [visit_id]/</code><br>'
                '&nbsp;&nbsp;├── <code>fotos/</code> — fotos subidas automáticamente<br>'
                '&nbsp;&nbsp;├── <code>diagnostico/diagnostico.json</code> — datos del diagnóstico<br>'
                '&nbsp;&nbsp;├── <code>excel/diagnostico_*.xlsx</code> — informe Excel<br>'
                '&nbsp;&nbsp;└── <code>informe/informe_*.docx</code> — informe Word<br>'
                'Todo se actualiza automáticamente al guardar cualquier módulo.</div>',
                unsafe_allow_html=True)
            st.markdown("**📂 Proyectos en Drive:**")
            try:
                from utils.gdrive import list_space_folders
                folders = list_space_folders()
                if folders:
                    for folder in folders:
                        fecha = str(folder.get("createdTime",""))[:10]
                        st.markdown(f"📁 **{folder['name']}** · {fecha}")
                else:
                    st.caption("Aún no hay carpetas de proyectos. Se crean automáticamente al guardar el primer diagnóstico.")
            except Exception as e:
                st.caption(f"No se pudo listar carpetas: {e}")
        else:
            st.markdown(
                '<div class="warning-box">⚠️ <strong>Google Drive no configurado.</strong> '
                'Para activarlo en Streamlit Cloud, agrega los secrets en la configuración de tu app.</div>',
                unsafe_allow_html=True)
            with st.expander("📖 Instrucciones de configuración"):
                st.markdown("""
**Streamlit Cloud Secrets** (recomendado):

```toml
[gdrive]
enabled = true
folder_id = "ID_DE_TU_CARPETA_EN_DRIVE"

[gdrive.credentials]
type = "service_account"
project_id = "tu-proyecto"
private_key_id = "..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\\n...\\n-----END RSA PRIVATE KEY-----\\n"
client_email = "cuenta@proyecto.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```

**Pasos:**
1. [Google Cloud Console](https://console.cloud.google.com) → Habilitar **Google Drive API**
2. Crear **Cuenta de servicio** → Descargar JSON de credenciales
3. En Google Drive: crear carpeta → compartir con el email de la cuenta de servicio
4. Copiar el ID de la carpeta desde la URL y pegarlo como `folder_id`
5. En Streamlit Cloud → Settings → Secrets → pegar la configuración TOML
                """)

    with tab3:
        st.markdown("### 📊 Todos los Diagnósticos")
        visits = load_visits()
        if not visits:
            st.info("No hay diagnósticos guardados aún.")
        else:
            for v in sorted(visits, key=lambda x: x.get("updated_at",""), reverse=True):
                nombre  = v.get("proyecto_nombre", "Sin nombre")
                cliente = v.get("proyecto_cliente", "")
                vid     = v.get("id", "")
                fecha   = str(v.get("updated_at", ""))[:10]
                with st.expander(f"🌿 **{nombre}** · {cliente} · {fecha}"):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        info = {k: v[k] for k in ["proyecto_nombre","proyecto_cliente",
                                "proyecto_ciudad","proyecto_fecha","id","updated_at"]
                                if k in v}
                        st.json(info)
                    with c2:
                        if st.button("📂 Cargar", key=f"load_admin_{vid}", use_container_width=True):
                            st.session_state.visit_data = v
                            st.session_state.page = "client"
                            st.rerun()
