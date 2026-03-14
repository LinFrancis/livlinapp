"""Indagación Regenerativa v3.3 — LivLin · Multi-usuario · www.livlin.cl"""
import pandas as pd  # noqa: pre-load
from pathlib import Path
import streamlit as st
from utils.data_manager import load_visits, delete_visit, DATA_FILE, get_visit

st.set_page_config(
    page_title="Indagación Regenerativa · LivLin v3.3",
    page_icon="🌿", layout="wide",
    initial_sidebar_state="expanded")

CSS_FILE = Path(__file__).parent / "style.css"
if CSS_FILE.exists():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Pages ──────────────────────────────────────────────────────────────────
PAGES_USER = {
    "🌿 Inicio":                               "home",
    "📋 M1 · Información + Intención":         "client",
    "☯️ Tao de la Regeneración":               "tao",
    "📷 Registro Fotográfico":                 "media",
    "🔬 M2–3 · Ecología + Cultivo":            "site_reading",
    "🏙️ M4–6 · Contexto + Agua + Energía":    "systems",
    "🌸 M7 · Flor de la Permacultura":         "regenerative_potential",
    "🗺️ M9 · Síntesis + Plan":                "action_plan",
    "📊 Informe Final":                        "report",
}
PAGES_ADMIN = {**PAGES_USER, "⚙️ Administración": "admin"}


def _login_page():
    logo_path = Path(__file__).parent / "assets" / "logolivlin.png"
    _, cc, _ = st.columns([1.5, 1, 1.5])
    with cc:
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        st.markdown('<h2 style="text-align:center;color:#1B4332;font-family:Georgia;">Indagación Regenerativa</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#666;font-size:0.9rem;">Instrumento de diagnóstico · LivLin v5</p>', unsafe_allow_html=True)
        st.markdown("---")
        uname = st.text_input("👤 Usuario", placeholder="Ej: francis", key="login_user")
        pwd   = st.text_input("🔑 Contraseña", type="password", key="login_pwd")
        if st.button("🌿 Ingresar", use_container_width=True, type="primary", key="btn_login"):
            from utils.users import authenticate
            user = authenticate(uname.strip(), pwd.strip())
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user  = user
                st.session_state.username      = user["username"]
                # Invalidate visit cache to force reload from Drive on login
                st.session_state.pop("_visits_cache_v3.3", None)
                st.session_state.pop("_sb_status_cache", None)
                # Load user's visit if linked
                if user.get("visit_id"):
                    v = get_visit(user["visit_id"])
                    st.session_state.visit_data = v if v else {}
                else:
                    st.session_state.visit_data = {}
                # Force reload from Supabase on login
                st.session_state.pop("_visits_cache", None)
                st.session_state.pop("_db_status_cache", None)
                st.rerun()
            else:
                st.error("⚠️ Usuario o contraseña incorrectos.")
        st.markdown('<p style="text-align:center;font-size:0.72rem;color:#aaa;margin-top:1rem;">v3.3 · LivLin Permacultura Urbana</p>', unsafe_allow_html=True)


def _sidebar():
    user  = st.session_state.get("current_user", {})
    is_admin = user.get("role") == "admin"
    PAGES = PAGES_ADMIN if is_admin else PAGES_USER

    with st.sidebar:
        logo_path = Path(__file__).parent / "assets" / "logolivlin.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;padding:0.5rem 0;">'
                '<span style="font-family:Georgia;font-size:1.3rem;font-weight:800;color:#1B4332;">🌿 LivLin</span></div>',
                unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;padding:0 0 0.4rem;">'
            '<span style="font-size:0.72rem;color:#40916C;font-style:italic;">Potencial para una vida regenerativa</span></div>',
            unsafe_allow_html=True)
        st.markdown("---")

        data = st.session_state.get("visit_data", {})
        if data.get("proyecto_nombre"):
            st.markdown(
                f'<div style="padding:0.4rem 0.7rem;background:rgba(82,183,136,0.15);'
                f'border-radius:8px;margin-bottom:0.4rem;border:1px solid #A8D5B5;">'
                f'<div style="font-size:0.62rem;color:#40916C;text-transform:uppercase;">VISITA ACTIVA</div>'
                f'<div style="font-weight:700;font-size:0.82rem;color:#1B4332;">{data["proyecto_nombre"]}</div>'
                f'<div style="font-size:0.7rem;color:#2D6A4F;">{data.get("proyecto_cliente","")}</div></div>',
                unsafe_allow_html=True)

        progress = _module_progress(st.session_state.get("visit_data", {}))
        for label, key in PAGES.items():
            is_active = st.session_state.get("page") == key
            pct = progress.get(key, 0)
            btn_label = label
            if pct == 100:
                btn_label = f"{label} ✅"
            elif pct > 0:
                btn_label = f"{label} ({pct}%)"
            if is_active:
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
            if is_active:
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Visit management (admin sees all, user sees only theirs)
        if is_admin:
            st.caption("📂 Todos los diagnósticos")
            visits = load_visits()
            if visits:
                visit_names = {v.get("id",""): f"{v.get('proyecto_nombre','?')} ({str(v.get('updated_at',v.get('created_at','?')))[:10]})"
                               for v in visits}
                sel = st.selectbox("", list(visit_names.keys()),
                    format_func=lambda x: visit_names.get(x,x), key="visit_sel",
                    label_visibility="collapsed")
                cl, dl = st.columns(2)
                with cl:
                    if st.button("📂 Cargar", use_container_width=True, key="btn_load"):
                        v = get_visit(sel)
                        if v: st.session_state.visit_data = v; st.session_state.page = "client"; st.rerun()
                with dl:
                    if st.button("🗑️ Borrar", use_container_width=True, key="btn_del"):
                        st.session_state["_confirm_del"] = sel
                        st.rerun()

            if st.session_state.get("_confirm_del") == sel:
                st.warning(f"⚠️ ¿Confirmar eliminación de **{visit_names.get(sel,'?')}**?")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("✅ Sí, eliminar", key="btn_del_confirm", type="primary",
                                 use_container_width=True):
                        delete_visit(sel)
                        st.session_state.pop("_confirm_del", None)
                        if st.session_state.get("visit_data",{}).get("id") == sel:
                            st.session_state.visit_data = {}
                        st.rerun()
                with cc2:
                    if st.button("❌ Cancelar", key="btn_del_cancel",
                                 use_container_width=True):
                        st.session_state.pop("_confirm_del", None)
                        st.rerun()
                if st.button("➕ Nuevo diagnóstico", use_container_width=True, key="btn_new"):
                    st.session_state.visit_data = {}; st.session_state.page = "client"; st.rerun()

        space = user.get("space_name", "")
        st.markdown("---")
        st.markdown(f'<div style="font-size:0.75rem;color:#40916C;">👤 {user.get("display_name","")}'
                    + (f'<br>🏡 {space}' if space else '')
                    + '</div>', unsafe_allow_html=True)

        # ── Supabase status indicator ───────────────────────
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
                        '🗄️ Supabase conectado</div>', unsafe_allow_html=True)
                else:
                    err_short = str(sb_status.get("error",""))[:55]
                    st.markdown(
                        f'<div style="background:#FFE0E0;border-radius:8px;padding:0.35rem 0.6rem;'
                        f'font-size:0.7rem;color:#B00020;margin-top:0.5rem;">'
                        f'⚠️ DB: {err_short}</div>', unsafe_allow_html=True)
                errs = st.session_state.get("_db_last_errors")
                if errs:
                    with st.expander("⚠️ Errores DB", expanded=False):
                        for err in errs:
                            st.caption(f"• {err}")
        except Exception:
            pass

        if st.button("🚪 Cerrar sesión", use_container_width=True, key="btn_logout"):
            st.session_state.authenticated = False
            st.session_state.current_user  = {}
            st.session_state.visit_data    = {}
            st.rerun()
        st.caption("🌿 LivLin · Permacultura Urbana")


def _home():
    st.markdown(
        '<div class="app-header">'
        '<h1>Indagación Regenerativa</h1>'
        '<p>Potencial para una vida regenerativa  ·  LivLin v3.3  ·  www.livlin.cl</p>'
        '</div>', unsafe_allow_html=True)

    _, cc, _ = st.columns([1, 3, 1])
    with cc:
        st.markdown(
            '<p style="text-align:center;font-size:0.95rem;color:#338B85;line-height:1.8;'
            'font-family:Montserrat,sans-serif;margin:1rem 0;">'
            'Cada espacio urbano alberga un <strong>potencial regenerativo</strong> que todavía no ha sido activado. '
            'Esta herramienta co-diseñada con el enfoque de la permacultura y el diseño regenerativo '
            'te ayuda a reconocer lo que ya está floreciendo en tu espacio '
            'y a trazar una ruta hacia lo que puede llegar a ser.'
            '</p>', unsafe_allow_html=True)

    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, [
        ("🌸", "Flor de la Permacultura",
         "Mapea las prácticas activas de tu espacio y el potencial adicional en los 7 pétalos de Holmgren. "
         "Genera el Índice de Potencial Regenerativo (IPR)."),
        ("🌍", "Observación Ecológica",
         "Lee el sitio antes de diseñar: suelo, agua, sol, viento, biodiversidad y clima histórico. "
         "La base de todo proceso regenerativo bien fundamentado."),
        ("🗺️", "Plan de Acción",
         "Hoja de ruta en 3 horizontes temporales: acciones inmediatas, estacionales y estructurales "
         "para el descenso creativo de tu espacio."),
    ]):
        with col:
            st.markdown(
                f'<div class="section-card" style="text-align:center;min-height:150px;">'
                f'<div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>'
                f'<strong style="color:#005954;font-size:0.88rem;font-family:Montserrat,sans-serif;">{title}</strong>'
                f'<p style="font-size:0.78rem;color:#338B85;margin-top:0.4rem;line-height:1.5;">{desc}</p></div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="tao-quote" style="max-width:720px;margin:1.2rem auto;text-align:center;">'
        '<strong style="font-size:1.05rem;color:#1B4332;display:block;margin-bottom:0.5rem;">'
        '«Cuando el planeta enferma, regenerar es mejorar la salud y celebrar la vida.»</strong>'
        'Frente a los desafíos globales del cambio climático, la pérdida de biodiversidad '
        'y la contaminación, ofrecemos soluciones locales y prácticas que regeneran los '
        'ecosistemas que sostienen la vida de las presentes y futuras generaciones.<br><br>'
        '<span style="font-size:0.78rem;color:#40916C;font-style:normal;font-weight:600;">'
        '— Mason, F. (2025). Introducción al enfoque de la regeneración. LivLin. '
        '· www.livlin.cl</span></div>',
        unsafe_allow_html=True)

    with st.expander("💚 ¿Por qué LivLin? — Nuestra propuesta", expanded=False):
        from utils.petal_content import LIVLIN_NARRATIVE_INTRO
        st.markdown(
            f'<div class="tao-quote" style="white-space:pre-line;">{LIVLIN_NARRATIVE_INTRO}</div>',
            unsafe_allow_html=True)

    _, cb, _ = st.columns([2, 1, 2])
    with cb:
        if st.button("🌿 Comenzar diagnóstico", use_container_width=True, type="primary"):
            st.session_state.page = "client"; st.rerun()



def _module_progress(data: dict) -> dict:
    """Calculate completion % for each module."""
    checks = {
        "client":    [("proyecto_nombre",""), ("proyecto_cliente",""), ("geo_lat",None)],
        "tao":       [("tao_motivacion",""), ("tao_presencia",""), ("tao_cc_conciencia","")],
        "media":     [("media_count", 0)],
        "site_reading": [("suelo_tipo",""), ("sol_horas",None), ("cultivo_m2",None)],
        "systems":   [("ctx_cuenca",""), ("agua_consumo",None), ("ene_kwh_dia_calc",None)],
        "regenerative_potential": [("fl_p1_conocimiento",None), ("fl_p7_biodiversidad",None)],
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
    if "page"            not in st.session_state: st.session_state.page = "home"
    if "visit_data"      not in st.session_state: st.session_state.visit_data = {}
    if "authenticated"   not in st.session_state: st.session_state.authenticated = False
    if "current_user"    not in st.session_state: st.session_state.current_user = {}

    if not st.session_state.authenticated:
        _login_page(); return

    _sidebar()
    page = st.session_state.get("page", "home")

    dispatch = {
        "home":                 _home,
        "client":               lambda: __import__("modules.client",             fromlist=["render"]).render(),
        "tao":                  lambda: __import__("modules.tao",                fromlist=["render"]).render(),
        "media":                lambda: __import__("modules.media_manager",      fromlist=["render"]).render(),
        "site_reading":         lambda: __import__("modules.site_reading",       fromlist=["render"]).render(),
        "systems":              lambda: __import__("modules.systems",            fromlist=["render"]).render(),
        "regenerative_potential":lambda: __import__("modules.regenerative_potential", fromlist=["render"]).render(),
        "action_plan":          lambda: __import__("modules.action_plan",        fromlist=["render"]).render(),
        "report":               lambda: __import__("modules.report",             fromlist=["render"]).render(),
        "admin":                lambda: __import__("modules.admin",              fromlist=["render"]).render(),
    }
    dispatch.get(page, _home)()


if __name__ == "__main__":
    main()
