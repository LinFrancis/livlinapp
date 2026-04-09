"""Herramienta de Indagación Regenerativa — LivLin · Multi-usuario · www.livlin.cl"""
import pandas as pd  # noqa: pre-load
from pathlib import Path
import streamlit as st
from utils.data_manager import load_visits, delete_visit, DATA_FILE, get_visit

_FAVICON = Path(__file__).parent / "assets" / "favicon.png"

st.set_page_config(
    page_title="LivLin — Indagación Regenerativa APP",
    page_icon=str(_FAVICON) if _FAVICON.exists() else "🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS_FILE = Path(__file__).parent / "style.css"
if CSS_FILE.exists():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Pages ──────────────────────────────────────────────────────────────────
PAGES_ADMIN = {
    "Inicio":                               "home",
    "M1 · Información + Intención":         "client",
    "Tao Vida Regenerativa":               "tao",
    "Conciencia Ecológica":                 "conciencia_ecologica",
    "Registro Fotográfico":                 "media",
    "M2–3 · Ecología + Cultivo":            "site_reading",
    "M4–6 · Contexto + Agua + Energía":    "systems",
    "M7 · Flor de la Permacultura":         "regenerative_potential",
    "M9 · Síntesis + Plan":                "action_plan",
    "Informe Final":                        "report",
    "⚙️ Administración":                       "admin",
}
# Cliente SOLO ve el informe final
PAGES_CLIENT = {
    "📊 Informe Final":  "report",
}


def _login_page():
    # ── 1. HERO IMAGE (Foto Asociada) ──
    # Significantly narrower columns to reduce size by half
    _, hcc, _ = st.columns([2.5, 2, 2.5])
    with hcc:
        foto_path  = Path(__file__).parent / "data" / "foto_intro.png"
        if foto_path.exists():
            st.image(str(foto_path), use_container_width=True)
        else:
            st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)

    # ── 2. MAIN TITLE & SUBTITLE ───────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; margin-top:1rem; margin-bottom:1rem;">
            <h1 style="color:#1B4332; font-family:'Georgia', serif; font-size:2rem; font-weight:800; line-height:1.1;">
                Herramienta de <span style="color:#52B788;">Indagación</span> Regenerativa
            </h1>
            <p style="color:#6B705C; font-size:0.95rem; font-weight:400; margin-top:0.4rem; letter-spacing:0.02em;">
                Bases para el diseño de ecosistemas regenerativos · LivLin
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # ── 3. INTRODUCTORY VIDEO (Inside Expander) ───────────────────────
    video_path = Path(__file__).parent / "data" / "video_intro_3_min.mp4"
    if video_path.exists():
        _, vcc, _ = st.columns([2.5, 3, 2.5])
        with vcc:
            with st.expander("🎞️ Ver Video Introductorio", expanded=False):
                st.video(str(video_path))
                st.markdown('<p style="text-align:center;font-size:0.7rem;color:#999;margin-top:0.3rem;">El Enfoque de LivLin · 3 min</p>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)

    # ── 4. ACCESS SECTIONS (DEMO & LOGIN) ──────────────────────────────
    # Centered and slightly more compact cards
    _, m_col, _ = st.columns([1, 4, 1])
    with m_col:
        col_demo, col_login = st.columns([1, 1], gap="medium")

        with col_demo:
            st.markdown(
                '<div style="background:#F8F9FA; border-radius:12px; padding:1.5rem; border:1px solid #E9ECEF; height:100%;">'
                '<h3 style="color:#1B4332; font-size:1.1rem; font-weight:700; margin-bottom:0.6rem;">Modo Demostración</h3>'
                '<p style="color:#666; font-size:0.82rem; margin-bottom:1.2rem;">'
                'Explora informes aplicables y conoce potenciales regenerativos.'
                '</p>',
                unsafe_allow_html=True
            )
            
            try:
                from utils.demo_profiles import list_demo_profiles, get_demo_profile
                profiles = list_demo_profiles()
                opciones = ["Selecciona un perfil..."] + [
                    nombre for _, nombre, _, _, _ in profiles
                ]
                sel = st.selectbox("Perfil", opciones, index=0, key="demo_select", label_visibility="collapsed")
                if sel != opciones[0]:
                    idx = opciones.index(sel) - 1
                    pid = profiles[idx][0]
                    if st.button("Explorar Perfil", use_container_width=True, type="primary", key="btn_demo_go"):
                        profile = get_demo_profile(pid)
                        if profile:
                            st.session_state.authenticated = True
                            st.session_state.current_user = {
                                "username": "demo", "role": "user",
                                "display_name": profile.get("proyecto_cliente", "Demo"),
                                "space_name": profile.get("proyecto_nombre", "Demo"),
                            }
                            st.session_state.visit_data = profile
                            st.session_state.demo_mode = True
                            st.session_state.page = "report"
                            st.rerun()
            except Exception:
                pass
            
            st.markdown(
                '<div style="margin-top:1rem; border-top:1px solid #E9ECEF; padding-top:0.8rem;">'
                '<a href="https://www.livlin.cl" target="_blank" style="font-size:0.78rem; color:#1B4332; font-weight:700; text-decoration:none;">'
                'Contacta a LivLin →</a></div></div>',
                unsafe_allow_html=True
            )

        with col_login:
            st.markdown(
                '<div style="background:#FFFFFF; border-radius:12px; padding:1.5rem; border:1px solid #E9ECEF; height:100%;">'
                '<h3 style="color:#1B4332; font-size:1.1rem; font-weight:700; margin-bottom:0.6rem;">Acceso Miembros</h3>'
                '<p style="color:#666; font-size:0.82rem; margin-bottom:1rem;">Inicia sesión para tus diagnósticos.</p>',
                unsafe_allow_html=True
            )
            uname = st.text_input("Usuario", placeholder="Tu usuario", key="login_user")
            pwd   = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pwd")
            
            if st.button("Iniciar Sesión", use_container_width=True, type="secondary", key="btn_login"):
                from utils.users import authenticate, refresh_from_supabase
                try:
                    refresh_from_supabase()
                except Exception:
                    pass
                user = authenticate(uname.strip(), pwd.strip())
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user  = user
                    st.session_state.username      = user["username"]
                    st.session_state.pop("_cache", None)
                    if user.get("visit_id"):
                        v = get_visit(user["visit_id"])
                        st.session_state.visit_data = v if v else {}
                    else:
                        st.session_state.visit_data = {}
                    role = user.get("role", "user")
                    st.session_state.page = "home" if role == "admin" else "report"
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
            
            st.markdown(
                '<div style="margin-top:0.8rem; text-align:center;">'
                '<p style="font-size:0.68rem; color:#AAA;">LivLin · Vida Regenerativa</p></div></div>',
                unsafe_allow_html=True
            )




def _sidebar():
    """Sidebar ONLY for admin users. Client sidebar lives in report.py."""
    user     = st.session_state.get("current_user", {})
    is_admin = user.get("role") == "admin"

    # ── ABSOLUTE GUARD: clients NEVER render this sidebar ──
    if not is_admin:
        return

    PAGES = PAGES_ADMIN
    data  = st.session_state.get("visit_data", {})

    with st.sidebar:
        logo_path = Path(__file__).parent / "assets" / "logolivlin.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;padding:0.5rem 0;">'
                '<span style="font-family:Georgia;font-size:1.3rem;font-weight:800;color:#1B4332;"> LivLin</span></div>',
                unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;padding:0 0 0.4rem;">'
            '<span style="font-size:0.72rem;color:#40916C;font-style:italic;">Servicios para una vida regenerativa</span></div>',
            unsafe_allow_html=True)
        st.markdown("---")

        if data.get("proyecto_nombre"):
            st.markdown(
                f'<div style="padding:0.4rem 0.7rem;background:rgba(82,183,136,0.15);'
                f'border-radius:8px;margin-bottom:0.4rem;border:1px solid #A8D5B5;">'
                f'<div style="font-size:0.62rem;color:#40916C;text-transform:uppercase;">DIAGNÓSTICO</div>'
                f'<div style="font-weight:700;font-size:0.82rem;color:#1B4332;">{data["proyecto_nombre"]}</div>'
                f'<div style="font-size:0.7rem;color:#2D6A4F;">{data.get("proyecto_cliente","")}</div></div>',
                unsafe_allow_html=True)

        progress = _module_progress(data)

        for label, key in PAGES.items():
            is_active = st.session_state.get("page") == key
            btn_label = label
            if progress:
                pct = progress.get(key, 0)
                if pct == 100:
                    btn_label = f"{label} ✅"
                elif pct > 0:
                    btn_label = f"{label} ({pct}%)"
            if is_active:
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"admin_nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
            if is_active:
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Admin downloads (only on report page) ──
        current_page = st.session_state.get("page", "")
        if current_page == "report" and data.get("proyecto_nombre"):
            st.markdown('<div style="font-size:0.75rem;color:#40916C;font-weight:700;margin-bottom:0.3rem;">Descargar informe</div>', unsafe_allow_html=True)
            safe_n = data.get("proyecto_nombre", "Diagnostico").replace(" ", "_")
            try:
                from utils.report_generator import generate_excel
                xlsx_bytes = generate_excel(data)
                st.download_button(
                    "Excel (.xlsx)", data=xlsx_bytes,
                    file_name=f"LivLin_IR_{safe_n}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True, type="primary", key="admin_dl_xlsx")
            except Exception as e:
                st.caption(f"Excel no disponible: {e}")
            try:
                from utils.docx_generator import generate_docx
                docx_bytes = generate_docx(data)
                st.download_button(
                    "Word (.docx)", data=docx_bytes,
                    file_name=f"LivLin_IR_{safe_n}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True, key="admin_dl_docx")
            except Exception as e:
                st.caption(f"Word no disponible: {e}")
            st.markdown("---")

        # ── Visit management ──
        st.caption("Todos los diagnósticos")
        visits = load_visits()
        if visits:
            visit_names = {v.get("id",""): f"{v.get('proyecto_nombre','?')} ({str(v.get('updated_at',v.get('created_at','?')))[:10]})"
                           for v in visits}
            sel = st.selectbox("", list(visit_names.keys()),
                format_func=lambda x: visit_names.get(x,x), key="admin_visit_sel",
                label_visibility="collapsed")
            cl, dl = st.columns(2)
            with cl:
                if st.button("Cargar", use_container_width=True, key="admin_btn_load"):
                    v = get_visit(sel)
                    if v: st.session_state.visit_data = v; st.session_state.page = "client"; st.rerun()
            with dl:
                if st.button("Borrar", use_container_width=True, key="admin_btn_del"):
                    st.session_state["_confirm_del"] = sel
                    st.rerun()

            if st.session_state.get("_confirm_del") == sel:
                st.warning(f"Confirmar eliminación de **{visit_names.get(sel,'?')}**")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("Si, eliminar", key="admin_btn_del_confirm", type="primary",
                                 use_container_width=True):
                        delete_visit(sel)
                        st.session_state.pop("_confirm_del", None)
                        if st.session_state.get("visit_data",{}).get("id") == sel:
                            st.session_state.visit_data = {}
                        st.rerun()
                with cc2:
                    if st.button("Cancelar", key="admin_btn_del_cancel",
                                 use_container_width=True):
                        st.session_state.pop("_confirm_del", None)
                        st.rerun()

        if st.button("Nuevo diagnóstico", use_container_width=True, key="admin_btn_new"):
            st.session_state.visit_data = {}; st.session_state.page = "client"; st.rerun()
        st.markdown("---")

        space = user.get("space_name", "")
        st.markdown(f'<div style="font-size:0.75rem;color:#40916C;">Admin: {user.get("display_name","")}'
                    + (f'<br>Espacio: {space}' if space else '')
                    + '</div>', unsafe_allow_html=True)

        # Supabase status
        try:
            from utils.supabase_db import is_configured, test_connection as get_status
            if is_configured():
                sb_status = st.session_state.get("_sb_status_cache")
                if sb_status is None:
                    sb_status = get_status()
                    st.session_state["_sb_status_cache"] = sb_status
                if sb_status["ok"]:
                    st.markdown(
                        '<div style="background:#D8F3DC;border-radius:8px;padding:0.35rem 0.6rem;'
                        'font-size:0.72rem;color:#1B4332;text-align:center;margin-top:0.5rem;">'
                        'Supabase conectado</div>', unsafe_allow_html=True)
        except Exception:
            pass

        if st.button("Cerrar sesión", use_container_width=True, key="admin_btn_logout"):
            st.session_state.authenticated = False
            st.session_state.current_user  = {}
            st.session_state.visit_data    = {}
            st.rerun()
        st.caption("LivLin · Servicios para una vida regenerativa")


def _home():
    st.markdown(
        '<div class="app-header">'
        '<h1>Herramienta de Indagación Regenerativa</h1>'
        '<p>Potencial para una vida regenerativa  ·  LivLin  ·  www.livlin.cl</p>'
        '</div>', unsafe_allow_html=True)
    _, cc, _ = st.columns([1, 3, 1])
    with cc:
        st.markdown(
            '<p style="text-align:center;font-size:0.95rem;color:#338B85;line-height:1.8;">'
            'Cada espacio alberga un <strong>potencial regenerativo</strong> que todavía no ha sido activado. '
            'Esta herramienta te ayuda a reconocer lo que ya está floreciendo en tu espacio '
            'y a trazar una ruta hacia lo que puede llegar a ser.'
            '</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, [
        ("🌸", "Flor de la Permacultura", "Mapea las prácticas activas y el potencial en los 7 pétalos de la flor de la permacultura. Genera indicadores ERP y HRP."),
        ("🌍", "Análisis de Sectores",   "Lee el sitio antes de diseñar: suelo, agua, sol, viento, biodiversidad."),
        ("🗺️", "Plan de Acción",          "Hoja de ruta en 3 horizontes: acciones inmediatas, estacionales y estructurales."),
    ]):
        with col:
            st.markdown(f'<div class="section-card" style="text-align:center;min-height:140px;">'
                        f'<div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>'
                        f'<strong style="color:#005954;font-size:0.88rem;">{title}</strong>'
                        f'<p style="font-size:0.78rem;color:#338B85;margin-top:0.4rem;">{desc}</p></div>',
                        unsafe_allow_html=True)
    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        if st.button("Comenzar diagnóstico", use_container_width=True, type="primary"):
            st.session_state.page = "client"; st.rerun()


def _module_progress(data: dict) -> dict:
    checks = {
        "client":    [("proyecto_nombre",""), ("proyecto_cliente",""), ("geo_lat",None)],
        "tao":       [("tao_d1_wu_wei",0), ("tao_d2_humildad",0), ("tao_d3_compasion",0)],
        "conciencia_ecologica": [("eco_cc_conciencia",""), ("eco_bio_conciencia","")],
        "media":     [("media_count", 0)],
        "site_reading": [("suelo_tipo",""), ("sol_horas",None), ("cultivo_m2",None)],
        "systems":   [("ctx_cuenca",""), ("agua_consumo",None), ("ene_kwh_dia_calc",None)],
        "regenerative_potential": [("ipr_obs",None)],
        "action_plan": [("sint_fortalezas",""), ("plan_inmediatas",None)],
        "report":    [],
    }
    result = {}
    for page, fields in checks.items():
        if not fields: result[page] = 100; continue
        filled = sum(1 for k, empty in fields if data.get(k) not in [empty, None, [], ""])
        result[page] = round(filled / len(fields) * 100)
    return result


def main():
    if "page"          not in st.session_state: st.session_state.page = "home"
    if "visit_data"    not in st.session_state: st.session_state.visit_data = {}
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if "current_user"  not in st.session_state: st.session_state.current_user = {}

    if not st.session_state.authenticated:
        _login_page(); return

    user     = st.session_state.get("current_user", {})
    is_admin = user.get("role") == "admin"

    # Sidebar: _sidebar() has internal guard — only renders for admin
    _sidebar()

    page = st.session_state.get("page", "home")

    # Clients can ONLY access the report page
    if not is_admin and page != "report":
        page = "report"
        st.session_state.page = "report"

    dispatch = {
        "home":                   _home,
        "client":                 lambda: __import__("modules.client",             fromlist=["render"]).render(),
        "tao":                    lambda: __import__("modules.tao",                fromlist=["render"]).render(),
        "conciencia_ecologica":   lambda: __import__("modules.conciencia_ecologica", fromlist=["render"]).render(),
        "media":                  lambda: __import__("modules.media_manager",      fromlist=["render"]).render(),
        "site_reading":           lambda: __import__("modules.site_reading",       fromlist=["render"]).render(),
        "systems":                lambda: __import__("modules.systems",            fromlist=["render"]).render(),
        "regenerative_potential": lambda: __import__("modules.regenerative_potential", fromlist=["render"]).render(),
        "action_plan":            lambda: __import__("modules.action_plan",        fromlist=["render"]).render(),
        "report":                 lambda: __import__("modules.report",             fromlist=["render"]).render(),
        "admin":                  lambda: __import__("modules.admin",              fromlist=["render"]).render(),
    }
    dispatch.get(page, _home)()


if __name__ == "__main__":
    main()
