"""Módulo 7 — Flor de la Permacultura v6 — tab_nav, descripciones extendidas por pétalo."""
import streamlit as st
import plotly.graph_objects as go
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status, tab_header, tab_nav_bottom, get_active_tab
from utils.scoring import (FLOWER_DOMAINS, ETHICAL_PRINCIPLES, SCORE_SCALE,
                            compute_domain_scores, compute_regenerative_score, score_label)

TABS = ["🌸 7 Pétalos + Prácticas", "⚖️ 3 Principios Éticos", "📊 Mapa de la Flor"]
MOD  = "m7"
SCALE_OPTIONS = list(range(6))


def render():
    st.markdown("## 🌸 Módulo 7 — Flor de la Permacultura")
    st.markdown(
        '<p class="module-subtitle">Los 7 pétalos de la permacultura de David Holmgren. '
        'Evalúa qué se practica hoy y qué puede florecer mañana.</p>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">🌸 <strong>Escala 0–5:</strong> '
        '0 = Sin práctica aún · 1 = Semilla · 2 = Brote · 3 = Crecimiento · 4 = Floreciendo · 5 = Abundancia. '
        'Marca <strong>N/A</strong> si el indicador no aplica al espacio.</div>', unsafe_allow_html=True)

    data = st.session_state.visit_data
    tab_header(MOD, TABS)
    active = get_active_tab(MOD)

    if active == 0:
        _render_petals(data)
        tab_nav_bottom(MOD, TABS, 0)
        _save_button(data, "7a")

    elif active == 1:
        _render_ethics(data)
        tab_nav_bottom(MOD, TABS, 1)
        _save_button(data, "7b")

    elif active == 2:
        _render_chart(data)
        tab_nav_bottom(MOD, TABS, 2)
        _save_button(data, "7c")


def _render_petals(data):
    for domain, meta in FLOWER_DOMAINS.items():
        d_color = meta["color"]
        d_icon  = meta["icon"]

        st.markdown(
            f'<div class="section-card" style="border-left:5px solid {d_color};margin-bottom:1rem;">',
            unsafe_allow_html=True)
        st.markdown(f"### {d_icon} Pétalo {meta['petal_num']}: {domain}")

        # Extended description in expandable section
        with st.expander(f"📖 ¿Qué es el pétalo de {domain}?", expanded=False):
            st.markdown(meta.get("long_desc", meta.get("desc", "")))
            st.markdown(
                f'<div style="background:rgba(82,183,136,0.1);border-radius:8px;padding:0.5rem 0.8rem;'
                f'margin-top:0.4rem;font-size:0.83rem;color:#2D6A4F;">'
                f'📐 <em>{meta.get("areas","")}</em></div>', unsafe_allow_html=True)

        st.caption(meta.get("desc", ""))

        # Indicators
        indicators = meta["indicators"]
        for i in range(0, len(indicators), 2):
            pair = indicators[i:i+2]
            cols = st.columns(len(pair))
            for j, ind in enumerate(pair):
                key    = ind["key"]
                na_key = f"{key}_na"
                with cols[j]:
                    is_na = st.checkbox("N/A — no aplica", value=bool(data.get(na_key, False)),
                                        key=f"na_{key}_{MOD}")
                    data[na_key] = is_na
                    if not is_na:
                        cur_v = data.get(key, 0)
                        if cur_v is None: cur_v = 0
                        val = st.select_slider(
                            ind["label"], options=SCALE_OPTIONS, value=int(cur_v),
                            key=f"sl_{key}_{MOD}", help=ind.get("help", ""),
                            format_func=lambda v: f"{v} — {SCORE_SCALE[v]['label']}")
                        data[key] = val
                        _score_badge(val, d_color)
                    else:
                        data[key] = None
                        st.markdown(
                            f'<div style="color:#9E9E9E;font-size:0.82rem;padding:0.4rem 0;'
                            f'font-style:italic;">⊘ {ind["label"]}</div>', unsafe_allow_html=True)

        # Practices
        pk_actual  = f"flower_practicas_actuales_{domain}"
        pk_futuras = f"flower_practicas_futuras_{domain}"
        c_p, c_f = st.columns(2)
        with c_p:
            data[pk_actual] = st.text_area(
                "✅ ¿Qué hacen actualmente en este pétalo?",
                value=data.get(pk_actual, ""), height=80, key=f"pact_{domain}_{MOD}",
                placeholder="Ej: Usamos materiales reciclados, tenemos pérgola de madera…")
        with c_f:
            data[pk_futuras] = st.text_area(
                "🚀 ¿Qué les gustaría hacer / desarrollar?",
                value=data.get(pk_futuras, ""), height=80, key=f"pfut_{domain}_{MOD}",
                placeholder="Ej: Instalar techo verde, mejorar el diseño bioclimático…")

        data[f"flower_notas_{domain}"] = st.text_area(
            "📝 Notas del pétalo", value=data.get(f"flower_notas_{domain}", ""),
            height=80, key=f"not_{domain}_{MOD}")

        st.markdown("</div>", unsafe_allow_html=True)


def _render_ethics(data):
    st.markdown(
        '<div class="tao-quote">⚖️ Los tres principios éticos de la Permacultura son el corazón '
        'de toda acción regenerativa. No son solo conceptos — son prácticas concretas.</div>',
        unsafe_allow_html=True)

    for principle in ETHICAL_PRINCIPLES:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### {principle['title']}")
        st.markdown(
            f'<div style="background:rgba(166,124,0,0.08);border-left:3px solid #A67C00;'
            f'border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.7rem;'
            f'font-size:0.88rem;color:#5A4400;font-style:italic;">'
            f'{principle["desc"]}</div>', unsafe_allow_html=True)

        for key, label, ph in principle["questions"]:
            data[key] = st.text_area(label, value=data.get(key, ""), height=80,
                                     placeholder=ph, key=f"eth_{key}_{MOD}")

        eth_score_key = f"eth_score_{principle['key']}"
        data[eth_score_key] = st.select_slider(
            f"¿En qué nivel practican activamente '{principle['title']}'?",
            options=SCALE_OPTIONS, value=data.get(eth_score_key, 0),
            key=f"ethsl_{principle['key']}_{MOD}",
            format_func=lambda v: f"{v} — {SCORE_SCALE[v]['label']}")
        _score_badge(data[eth_score_key], "#A67C00")
        st.markdown("</div>", unsafe_allow_html=True)


def _render_chart(data):
    domain_scores = compute_domain_scores(data)
    global_score  = compute_regenerative_score(data)
    label_g, color_g = score_label(global_score)

    st.markdown("### 📊 Mapa de la Flor Regenerativa")
    st.markdown(
        '<div class="info-box">Los puntajes se calculan automáticamente desde los indicadores respondidos. '
        'Los pétalos más cubiertos aparecen más grandes en el radar.</div>', unsafe_allow_html=True)

    col_chart, col_score = st.columns([2, 1])
    with col_chart:
        cats  = list(domain_scores.keys())
        vals  = [domain_scores[d] for d in cats]
        short = [f"P{FLOWER_DOMAINS[d]['petal_num']} {FLOWER_DOMAINS[d]['icon']}" for d in cats]
        r_v = vals + [vals[0]] if vals else [0]
        t_c = short + [short[0]] if short else [""]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_v, theta=t_c, fill="toself",
            fillcolor="rgba(82,183,136,0.2)", line=dict(color="#2D6A4F", width=2.5),
            marker=dict(size=8, color="#1B4332"), name="Pétalos"))
        fig.update_layout(
            polar=dict(bgcolor="rgba(240,255,244,0.5)",
                radialaxis=dict(visible=True, range=[0, 5], tickvals=[1,2,3,4,5],
                    tickfont=dict(size=10, color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
                angularaxis=dict(tickfont=dict(size=11, color="#1B4332", family="Georgia"))),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(l=60, r=60, t=40, b=40), height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col_score:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#E8F5E9,#D8F3DC);'
            f'border:2px solid #52B788;border-radius:14px;padding:1.5rem;text-align:center;">'
            f'<div style="font-size:0.75rem;color:#40916C;text-transform:uppercase;letter-spacing:0.1em;">Regenerative Score</div>'
            f'<div style="font-size:4rem;font-weight:800;color:#1B4332;line-height:1;">{global_score}</div>'
            f'<div style="color:#52B788;">/5.0</div>'
            f'<div style="font-size:0.85rem;color:{color_g};font-weight:600;'
            f'background:rgba(82,183,136,0.15);border-radius:8px;padding:0.3rem 0.6rem;margin-top:0.5rem;">'
            f'{label_g}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Desarrollo por pétalo:**")
        sorted_d = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        for domain, score in sorted_d:
            meta  = FLOWER_DOMAINS[domain]
            pct   = int((score / 5) * 100)
            d_col = meta["color"]
            d_ico = meta["icon"]
            st.markdown(
                f'<div style="margin-bottom:6px;">'
                f'<div style="font-size:0.76rem;color:#333;">{d_ico} P{meta["petal_num"]} {domain[:22]}</div>'
                f'<div style="background:#E8F5E9;border-radius:4px;height:9px;overflow:hidden;">'
                f'<div style="background:{d_col};width:{pct}%;height:100%;border-radius:4px;"></div></div>'
                f'<div style="font-size:0.7rem;color:#666;text-align:right;">{score}/5</div></div>',
                unsafe_allow_html=True)


def _score_badge(val, color="#2D6A4F"):
    if val is None: return
    val = int(val)
    labels = {0:"Sin práctica",1:"🌱 Semilla",2:"🌿 Brote",3:"🌳 Crecimiento",4:"🌸 Floreciendo",5:"🌺 Abundancia"}
    bgcols = {0:"#9E9E9E",1:"#74C69D",2:"#52B788",3:"#40916C",4:"#2D6A4F",5:"#1B4332"}
    c = bgcols.get(val, "#9E9E9E")
    l = labels.get(val, "")
    st.markdown(
        f'<div style="text-align:center;margin:2px 0;">'
        f'<span style="background:{c};color:white;padding:2px 12px;border-radius:12px;'
        f'font-size:0.76rem;font-weight:600;">{l}</span></div>', unsafe_allow_html=True)


def _save_button(data, suffix=""):
    st.markdown("---")

    # ── Estado del módulo ─────────────────────────────────────────────────
    st.markdown("**Estado de este módulo:**")
    _mod_status = render_module_status(data, "mod_potencial")
    if not is_module_active(_mod_status):
        # Limpiar valores por defecto si el módulo no fue abordado
        save_col1, save_col2 = st.columns([1,1])
        with save_col1:
            if st.button("💾 Guardar como No Abordado", key="save_na_mod_potencial",
                         use_container_width=True):
                st.session_state.visit_data = data
                save_visit(data)
                st.success("✅ Módulo marcado como No Abordado.")
                show_drive_save_status()
        return
    if _mod_status == "inferido":
        st.info("🔍 **Modo inferido** — Las respuestas abajo son interpretaciones del facilitador, no de las personas del espacio.")
    st.markdown("---")
    _, c, _ = st.columns([2, 1, 2])
    with c:
        if st.button("💾 Guardar módulo 7", use_container_width=True,
                     type="primary", key=f"save_m7_{suffix}"):
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            try:
                from utils.gdrive import is_configured, sync_visits_to_drive
                from utils.data_manager import DATA_FILE
                if is_configured(): sync_visits_to_drive(DATA_FILE)
            except Exception: pass
            st.success("✅ Módulo 7 guardado.")
            show_drive_save_status()
