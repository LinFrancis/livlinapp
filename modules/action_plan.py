"""Módulo 9 — Síntesis Regenerativa + Plan de Acción (v5) — interpretaciones editables."""
import streamlit as st
import plotly.graph_objects as go
from utils.data_manager import save_visit
from utils.scoring import (compute_synthesis_potentials, compute_domain_scores,
                            compute_regenerative_score, score_label)
from utils.synthesis import generate_all
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status, tab_header, tab_nav_bottom, get_active_tab

TABS = ["🌱 Potencial Regenerativo", "📝 Síntesis Narrativa", "🗓️ Plan de Acción"]
MOD  = "m9"
ESTADOS = ["⏳ Pendiente", "🔄 En progreso", "✅ Completado", "❌ Cancelado"]

# ── Descripciones de cada dimensión ──────────────────────────────────────────
# ── Fuentes de las Dimensiones Regenerativas ─────────────────────────────────
# Las 8 dimensiones integran marcos complementarios:
# - Permacultura / 7 pétalos (Holmgren, 2002): Tierra, Construido, Herramientas,
#   Educación, Salud, Economía, Gobernanza.
# - Diseño Regenerativo (Mang & Reed, 2012): énfasis en salud ecosistémica y
#   capital natural como resultado del diseño.
# - Enfoque ecosocial (Mason, 2025): inclusión del bienestar interior y la
#   dimensión espiritual como base de la acción regenerativa sostenida.
# LivLin sintetiza estos marcos en 8 dimensiones operativas para el diagnóstico.

from utils.dim_content import DIM_DESC, DIM_INTERP, CLIMATE_REF


def _interp_auto(dim: str, val: float) -> str:
    d = DIM_INTERP.get(dim, [])
    if not d: return ""
    return d[min(5, max(0, round(val)))]


def render():
    st.markdown("## 🗺️ Módulo 9 — Síntesis Regenerativa + Plan de Acción")
    data = st.session_state.visit_data

    tab_header(MOD, TABS)
    active = get_active_tab(MOD)

    # ════════════════════════════════════════════════════════════════════════
    if active == 0:
        _render_potencial(data)
        tab_nav_bottom(MOD, TABS, 0)
        _save_button(data, "9a")

    elif active == 1:
        _render_sintesis(data)
        tab_nav_bottom(MOD, TABS, 1)
        _save_button(data, "9b")

    elif active == 2:
        _render_plan(data)
        tab_nav_bottom(MOD, TABS, 2)
        _save_button(data, "9c")


# ── Tab 1: Potencial Regenerativo ─────────────────────────────────────────────
def _render_potencial(data):
    st.markdown(
        '<div class="info-box">🌱 <strong>Perspectiva regenerativa:</strong> '
        'Un puntaje bajo no indica carencia — indica el enorme potencial de transformación del espacio. '
        'Cada dimensión tiene una interpretación automática que puedes editar y personalizar.</div>',
        unsafe_allow_html=True)

    potenciales  = compute_synthesis_potentials(data)
    global_score = compute_regenerative_score(data)
    label_g, color_g = score_label(global_score)
    domain_scores = compute_domain_scores(data)
    from utils.scoring import FLOWER_DOMAINS

    # ── Radar + Score global ──────────────────────────────────────────────
    col_r, col_s = st.columns([3, 2])
    with col_r:
        st.markdown("**🌸 Flor de la Permacultura**")
        cats = list(domain_scores.keys())
        vals = [domain_scores[d] for d in cats]
        short = [f"P{FLOWER_DOMAINS[d]['petal_num']} {FLOWER_DOMAINS[d]['icon']}" for d in cats]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=short + [short[0]], fill="toself",
            fillcolor="rgba(82,183,136,0.2)", line=dict(color="#2D6A4F", width=2.5),
            marker=dict(size=8, color="#1B4332")))
        fig.update_layout(
            polar=dict(bgcolor="rgba(240,255,244,0.5)",
                radialaxis=dict(visible=True, range=[0,5], tickvals=[1,2,3,4,5],
                    tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
                angularaxis=dict(tickfont=dict(size=10,color="#1B4332"))),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            margin=dict(l=50,r=50,t=30,b=30), height=340)
        st.plotly_chart(fig, use_container_width=True)

    with col_s:
        prom = round(sum(v for v in potenciales.values() if v) /
                     max(1, sum(1 for v in potenciales.values() if v)), 1)
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#E8F5E9,#D8F3DC);'
            f'border:2px solid #52B788;border-radius:14px;padding:1.2rem;text-align:center;margin-bottom:0.8rem;">'
            f'<div style="font-size:0.75rem;color:#40916C;text-transform:uppercase;letter-spacing:0.1em;">Potencial Regenerativo</div>'
            f'<div style="font-size:3.5rem;font-weight:800;color:#1B4332;line-height:1;">{prom}</div>'
            f'<div style="color:#52B788;">/5.0</div>'
            f'<div style="font-size:0.88rem;font-weight:600;color:{color_g};margin:0.3rem 0;">{label_g}</div>'
            f'</div>', unsafe_allow_html=True)

        if prom <= 1.5:
            ig = "El espacio está al inicio de su viaje regenerativo. Cada pequeña acción tiene un impacto enorme. El potencial de transformación es máximo."
        elif prom <= 2.5:
            ig = "El espacio está germinando. Hay prácticas regenerativas naciendo en varias dimensiones. Con constancia, la transformación se acelera."
        elif prom <= 3.5:
            ig = "El espacio está creciendo con fuerza. Varias dimensiones están activas. Es el momento de consolidar y expandir."
        elif prom <= 4.5:
            ig = "El espacio florece. La mayoría de las dimensiones regenerativas están activas y consolidadas — un referente en construcción."
        else:
            ig = "El espacio es un ejemplo vivo de abundancia regenerativa. Sus prácticas inspiran a otros."

        st.markdown(f'<div class="info-box" style="font-size:0.82rem;">{ig}</div>', unsafe_allow_html=True)

    # ── Dimensiones con interpretaciones editables ────────────────────────
    st.markdown("---")

    # ── Estado del módulo ─────────────────────────────────────────────────
    st.markdown("**Estado de este módulo:**")
    _mod_status = render_module_status(data, "mod_plan")
    if not is_module_active(_mod_status):
        # Limpiar valores por defecto si el módulo no fue abordado
        save_col1, save_col2 = st.columns([1,1])
        with save_col1:
            if st.button("💾 Guardar como No Abordado", key="save_na_mod_plan",
                         use_container_width=True):
                st.session_state.visit_data = data
                save_visit(data)
                st.success("✅ Módulo marcado como No Abordado.")
                show_drive_save_status()
        return
    if _mod_status == "inferido":
        st.info("🔍 **Modo inferido** — Las respuestas abajo son interpretaciones del facilitador, no de las personas del espacio.")
    st.markdown("---")
    st.markdown("### 🌱 Dimensiones Regenerativas — Interpretación y Análisis")

    # View mode toggle
    view_mode = st.radio("Modo de vista:",
                         ["🤖 Interpretación automática", "✏️ Editar interpretaciones"],
                         horizontal=True, key="pot_view_mode")

    for dim, val in potenciales.items():
        desc      = DIM_DESC.get(dim, "")
        interp_a  = _interp_auto(dim, val)
        climate   = CLIMATE_REF.get(dim, "")
        edit_key  = f"interp_edit_{dim.replace(' ','_')}"
        saved_key = f"interp_saved_{dim.replace(' ','_')}"
        pct = int((val/5)*100) if val else 0

        if val >= 4: bar_col, bg_col = "#1B4332", "rgba(27,67,50,0.08)"
        elif val >= 3: bar_col, bg_col = "#2D6A4F", "rgba(45,106,79,0.08)"
        elif val >= 2: bar_col, bg_col = "#40916C", "rgba(64,145,108,0.08)"
        elif val >= 1: bar_col, bg_col = "#52B788", "rgba(82,183,136,0.08)"
        else: bar_col, bg_col = "#74C69D", "rgba(116,198,157,0.08)"

        lbl, _ = score_label(val)
        st.markdown(
            f'<div style="background:{bg_col};border:1px solid {bar_col}40;'
            f'border-left:4px solid {bar_col};border-radius:10px;padding:0.7rem 1rem;margin:6px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;">'
            f'<strong style="color:#1B4332;font-size:0.95rem;">{dim}</strong>'
            f'<span style="background:{bar_col};color:white;padding:2px 12px;border-radius:10px;font-size:0.82rem;font-weight:700;">{val}/5</span>'
            f'</div>'
            f'<div style="font-size:0.78rem;color:#666;font-style:italic;margin-bottom:4px;">{desc}</div>'
            f'<div style="background:rgba(255,255,255,0.6);border-radius:4px;height:7px;margin-bottom:6px;overflow:hidden;">'
            f'<div style="background:{bar_col};width:{pct}%;height:100%;border-radius:4px;"></div>'
            f'</div>',
            unsafe_allow_html=True)

        if view_mode == "🤖 Interpretación automática":
            # Show auto text + climate ref
            current_text = data.get(saved_key, interp_a)
            st.markdown(
                f'<div style="font-size:0.82rem;color:#2D5A3D;line-height:1.5;">{current_text}</div>'
                + (f'<div style="font-size:0.77rem;color:#666;margin-top:4px;font-style:italic;">{climate}</div>' if climate else '')
                + '</div>', unsafe_allow_html=True)
        else:
            st.markdown("</div>", unsafe_allow_html=True)  # close the outer div first
            # Edit mode: pre-filled text area
            current_text = data.get(saved_key, interp_a)
            with st.container():
                edited = st.text_area(
                    f"✏️ Interpretación de {dim}",
                    value=current_text,
                    height=120,
                    key=edit_key,
                    help=f"Texto automático: {interp_a[:100]}…")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(f"✅ Aceptar", key=f"accept_{dim.replace(' ','_')}", use_container_width=True):
                        data[saved_key]    = edited
                        data[f"interp_auto_{dim.replace(' ','_')}"] = interp_a
                        save_visit(data)
                        st.session_state.visit_data = data
                        st.success("Guardado.")
                with c2:
                    if st.button(f"🔄 Restaurar automático", key=f"restore_{dim.replace(' ','_')}", use_container_width=True):
                        data[saved_key] = interp_a
                        save_visit(data)
                        st.session_state.visit_data = data
                        st.rerun()
            continue  # skip closing div (already closed above)

        # (closed inside the if block for auto mode)


# ── Tab 2: Síntesis Narrativa ─────────────────────────────────────────────────
def _render_sintesis(data):
    st.markdown(
        '<div class="info-box">✨ Síntesis generada automáticamente con lenguaje positivo y regenerativo. '
        'Editable libremente.</div>', unsafe_allow_html=True)

    auto = generate_all(data)
    _, c_btn, _ = st.columns([2, 1, 2])
    with c_btn:
        if st.button("🔄 Regenerar síntesis", type="primary", use_container_width=True, key="btn_regen"):
            for k, v in auto.items():
                data[k] = v
            save_visit(data)
            st.session_state.visit_data = data
            st.success("✅ Síntesis regenerada.")
            st.rerun()

    for k, v in auto.items():
        if not data.get(k):
            data[k] = v

    for key, label, ph in [
        ("sint_fortalezas",    "💪 Fortalezas y prácticas activas",        "Lo que ya funciona bien…"),
        ("sint_oportunidades", "🚀 Potencial de transformación regenerativa","Áreas donde la regeneración puede florecer…"),
        ("sint_limitaciones",  "🌱 Desafíos a transformar en oportunidad",  "Condiciones que requieren atención…"),
        ("sint_quick_wins",    "⚡ Primeros pasos — acciones de alto impacto","Acciones de bajo costo y gran impacto…"),
        ("sint_observaciones", "🌿 Reflexión del/la facilitador/a",          "Observaciones sobre el potencial del espacio…"),
    ]:
        data[key] = st.text_area(label, value=data.get(key, ""), height=120,
                                 placeholder=ph, key=f"s9_{key}")


# ── Tab 3: Plan de Acción ─────────────────────────────────────────────────────
def _render_plan(data):
    st.markdown("### 🗓️ Plan de Acción en 3 Fases")
    st.markdown('<div class="info-box">🌱 Cada acción es un paso en la épica de la regeneración.</div>',
                unsafe_allow_html=True)

    for plan_key, fase_title, fase_desc in [
        ("plan_inmediatas",  "⚡ Fase 1 — Primeros Pasos (0–3 meses)",  "Alta visibilidad, bajo costo, ¡para comenzar ya!"),
        ("plan_estacionales","🌱 Fase 2 — Construyendo (3–12 meses)",    "Instalación de sistemas, conexiones comunitarias"),
        ("plan_estructurales","🌳 Fase 3 — Transformación (1–5 años)",   "Cambios profundos del espacio hacia la regeneración"),
    ]:
        st.markdown(f"#### {fase_title}")
        st.caption(fase_desc)
        if not isinstance(data.get(plan_key), list):
            data[plan_key] = []
        with st.expander(f"➕ Agregar acción"):
            t = st.text_input("Acción", key=f"{plan_key}_t", placeholder="Ej: Instalar compostero")
            r = st.text_input("Responsable/s", key=f"{plan_key}_r")
            c = st.text_input("Recursos necesarios", key=f"{plan_key}_c")
            e = st.selectbox("Estado", ESTADOS, key=f"{plan_key}_e")
            if st.button("✅ Agregar", key=f"btn_{plan_key}"):
                if t.strip():
                    data[plan_key].append({"titulo": t, "resp": r, "costo": c, "estado": e})
                    save_visit(data); st.session_state.visit_data = data; st.rerun()
        for i, acc in enumerate(data.get(plan_key, [])):
            cp, cs = st.columns([5, 1])
            with cp: st.markdown(f"- {acc.get('estado','⏳')} **{acc.get('titulo','')}** — {acc.get('resp','')} · {acc.get('costo','')}")
            with cs:
                if st.button("🗑️", key=f"del_{plan_key}_{i}"):
                    data[plan_key].pop(i); save_visit(data); st.session_state.visit_data = data; st.rerun()


def _save_button(data, suffix=""):
    st.markdown("---")
    _, c, _ = st.columns([2, 1, 2])
    with c:
        if st.button("💾 Guardar módulo 9", use_container_width=True,
                     type="primary", key=f"save_m9_{suffix}"):
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            try:
                from utils.gdrive import is_configured, sync_visits_to_drive
                from utils.data_manager import DATA_FILE
                if is_configured(): sync_visits_to_drive(DATA_FILE)
            except Exception: pass
            st.success("✅ Módulo 9 guardado.")
            show_drive_save_status()
