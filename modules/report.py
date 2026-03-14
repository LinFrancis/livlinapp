"""Módulo Informe Final v4.2 — LivLin Indagación Regenerativa.
Dashboard completo: Flor IPR, potenciales, métricas, plan, exportación.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.data_manager import save_visit
from utils.scoring import (
    FLOWER_DOMAINS, PETAL_ORDER,
    compute_domain_scores, compute_domain_scores_total,
    compute_regenerative_score, score_label,
    compute_synthesis_potentials, compute_wellbeing_score,
)
from utils.report_generator import generate_excel


def _safe_float(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default


def render():
    st.markdown("## 📊 Informe Final del Diagnóstico")
    st.markdown(
        '<p class="module-subtitle">Dashboard · Flor de la Permacultura · '
        'Potenciales · Plan · Exportación</p>',
        unsafe_allow_html=True)

    # ── Reload fresh data ───────────────────────────────────────────────
    from utils.data_manager import get_visit
    visit_id = st.session_state.get("visit_data", {}).get("id")
    if visit_id:
        fresh = get_visit(visit_id)
        if fresh:
            st.session_state.visit_data = fresh
    data = st.session_state.get("visit_data", {})

    if not data.get("id"):
        st.warning("⚠️ Carga o crea un diagnóstico primero.")
        return

    # ── Compute all scores (index-based, never fails) ───────────────────
    domain_obs   = compute_domain_scores(data)          # observed
    domain_tot   = compute_domain_scores_total(data)    # obs + potential
    regen_score  = compute_regenerative_score(data)
    label_g, color_g = score_label(regen_score)
    potenciales  = compute_synthesis_potentials(data)
    wb_score     = compute_wellbeing_score(data)
    ipr_obs      = [domain_obs[p]  for p in PETAL_ORDER]
    ipr_tot      = [domain_tot[p]  for p in PETAL_ORDER]

    # ── Header ─────────────────────────────────────────────────────────
    nombre  = data.get("proyecto_nombre", "Diagnóstico sin nombre")
    cliente = data.get("proyecto_cliente", "—")
    ciudad  = data.get("proyecto_ciudad",  "—")
    fecha   = data.get("proyecto_fecha",   "—")

    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#F0FFF4,#D8F3DC);
                    border:2px solid #52B788;border-radius:14px;
                    padding:1.2rem 1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                <div>
                    <div style="font-size:0.72rem;color:#52B788;
                                text-transform:uppercase;letter-spacing:0.1em;">
                        Diagnóstico Regenerativo · LivLin v4.2</div>
                    <div style="font-size:1.5rem;font-weight:800;
                                color:#1B4332;margin:0.2rem 0;">{nombre}</div>
                    <div style="color:#555;font-size:0.88rem;">
                        👤 {cliente} &nbsp;·&nbsp; 📍 {ciudad} &nbsp;·&nbsp; 📅 {fecha}</div>
                </div>
                <div style="text-align:center;background:white;border-radius:12px;
                            padding:0.8rem 1.5rem;border:2px solid #D8F3DC;min-width:130px;">
                    <div style="font-size:0.68rem;color:#888;
                                text-transform:uppercase;">Score Regenerativo</div>
                    <div style="font-size:3rem;font-weight:900;
                                color:#1B4332;line-height:1;">{regen_score}</div>
                    <div style="color:#52B788;font-size:0.82rem;">/5.0</div>
                    <div style="font-size:0.78rem;color:{color_g};
                                font-weight:600;margin-top:0.2rem;">{label_g}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 1 — FLOR DE LA PERMACULTURA (radar dual)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 🌸 Flor de la Permacultura — Índice de Potencial Regenerativo")

    col_radar, col_ipr = st.columns([1.3, 0.7])

    with col_radar:
        labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
        labels_short = [f"{FLOWER_DOMAINS[p]['icon']} P{FLOWER_DOMAINS[p]['petal_num']}"
                        for p in PETAL_ORDER]
        # Close radar by repeating first point
        r_obs  = ipr_obs  + [ipr_obs[0]]
        r_tot  = ipr_tot  + [ipr_tot[0]]
        theta  = labels   + [labels[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_tot, theta=theta, name="🌟 Obs. + Potencial",
            fill="toself", fillcolor="rgba(82,183,136,0.10)",
            line=dict(color="#52B788", width=2, dash="dash"),
        ))
        fig.add_trace(go.Scatterpolar(
            r=r_obs, theta=theta, name="✅ Observado",
            fill="toself", fillcolor="rgba(27,67,50,0.22)",
            line=dict(color="#1B4332", width=2.5),
            marker=dict(size=7, color="#1B4332"),
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(240,255,244,0.4)",
                radialaxis=dict(
                    visible=True, range=[0, 5],
                    tickvals=[1, 2, 3, 4, 5],
                    tickfont=dict(size=9, color="#2D6A4F"),
                    gridcolor="rgba(45,106,79,0.2)"),
                angularaxis=dict(tickfont=dict(size=10, color="#1B4332")),
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.05,
                        font=dict(size=10)),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=60, t=50, b=30),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_ipr:
        st.markdown("**IPR por pétalo:**")
        for i, p in enumerate(PETAL_ORDER):
            n_o  = ipr_obs[i]
            n_t  = ipr_tot[i]
            icon = FLOWER_DOMAINS[p]["icon"]
            col  = FLOWER_DOMAINS[p]["color"]
            lv, _, _ = _score_level(n_o)
            pct = int(n_o / 5 * 100) if n_o <= 5 else 100
            st.markdown(
                f'<div style="padding:4px 0;border-bottom:1px solid #D8F3DC;">'
                f'<div style="display:flex;justify-content:space-between;'
                f'align-items:center;font-size:0.78rem;">'
                f'<span style="color:#1B4332;">{icon} {p[:28]}</span>'
                f'<span style="background:{col};color:white;border-radius:4px;'
                f'padding:1px 6px;font-size:0.7rem;">{n_o} obs +{n_t-n_o}</span>'
                f'</div>'
                f'<div style="background:#E8F5E9;height:5px;border-radius:3px;margin-top:2px;">'
                f'<div style="background:{col};width:{min(pct,100)}%;'
                f'height:5px;border-radius:3px;"></div></div>'
                f'</div>',
                unsafe_allow_html=True)

        # Completitud
        filled = sum(1 for v in ipr_obs if v > 0)
        st.markdown(f"""
            <div style="margin-top:0.8rem;padding:0.6rem;background:#F0FFF4;
                        border-radius:8px;border-left:3px solid #40916C;
                        font-size:0.8rem;color:#1B4332;">
                <strong>{filled}/7 pétalos</strong> con prácticas observadas<br>
                <span style="color:#52B788;">{regen_score}/5.0 — {label_g}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 2 — POTENCIALES (bar chart + síntesis)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 📊 Potenciales del Sitio")

    col_bar, col_meta = st.columns([1.2, 0.8])

    with col_bar:
        if any(v > 0 for v in potenciales.values()):
            fig2 = px.bar(
                x=list(potenciales.values()),
                y=list(potenciales.keys()),
                orientation="h",
                color=list(potenciales.values()),
                color_continuous_scale=["#D8F3DC", "#52B788", "#2D6A4F", "#1B4332"],
                range_color=[0, 5],
                text=[f"{v:.1f}" for v in potenciales.values()],
            )
            fig2.update_traces(textposition="outside", textfont_size=12)
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(240,255,244,0.3)",
                showlegend=False, coloraxis_showscale=False,
                xaxis=dict(range=[0, 6.0], tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=11)),
                margin=dict(l=10, r=40, t=10, b=10),
                height=320,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Completa el Módulo 7 (Flor de la Permacultura) para ver los potenciales.")

    with col_meta:
        area   = _safe_float(data.get("proyecto_superficie"))
        m2cult = _safe_float(data.get("cultivo_m2"))
        pct_c  = round(m2cult / area * 100) if area > 0 else 0
        prec   = _safe_float(data.get("agua_prec_anual"))
        techo  = _safe_float(data.get("agua_techo_m2"))
        cap_lluvia = round(prec * techo * 0.8) if prec > 0 and techo > 0 else 0

        metrics_html = f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
            <div style="background:white;border-radius:8px;padding:0.7rem;
                        box-shadow:0 2px 8px rgba(27,67,50,0.07);
                        border-left:3px solid #52B788;">
                <div style="font-size:1.4rem;font-weight:800;color:#1B4332;">
                    {int(area)}</div>
                <div style="font-size:0.7rem;color:#52B788;
                            text-transform:uppercase;">m² totales</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.7rem;
                        box-shadow:0 2px 8px rgba(27,67,50,0.07);
                        border-left:3px solid #40916C;">
                <div style="font-size:1.4rem;font-weight:800;color:#1B4332;">
                    {int(m2cult)}</div>
                <div style="font-size:0.7rem;color:#52B788;
                            text-transform:uppercase;">m² cultivables</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.7rem;
                        box-shadow:0 2px 8px rgba(27,67,50,0.07);
                        border-left:3px solid #2D6A4F;">
                <div style="font-size:1.4rem;font-weight:800;color:#1B4332;">
                    {pct_c}%</div>
                <div style="font-size:0.7rem;color:#52B788;
                            text-transform:uppercase;">% cultivable</div>
            </div>
            <div style="background:white;border-radius:8px;padding:0.7rem;
                        box-shadow:0 2px 8px rgba(27,67,50,0.07);
                        border-left:3px solid #1B4332;">
                <div style="font-size:1.4rem;font-weight:800;color:#1B4332;">
                    {cap_lluvia:,}</div>
                <div style="font-size:0.7rem;color:#52B788;
                            text-transform:uppercase;">L/año captables</div>
            </div>
        </div>"""
        st.markdown(metrics_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        destacadas = data.get("pot_practicas_destacadas", "")
        if destacadas:
            st.markdown(
                f'<div style="background:#F0FFF4;border-radius:8px;padding:0.8rem;'
                f'border-left:4px solid #52B788;font-size:0.85rem;color:#1B4332;">'
                f'<strong>✨ Prácticas destacadas:</strong><br>{destacadas}</div>',
                unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 3 — SÍNTESIS NARRATIVA
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 📝 Síntesis del Diagnóstico")

    s_items = [
        ("sint_fortalezas",    "💪 Fortalezas",      "#D8F3DC", "#1B4332"),
        ("sint_oportunidades", "🚀 Oportunidades",    "#E3F2FD", "#1565C0"),
        ("sint_limitaciones",  "⚠️ Desafíos",         "#FFF3E0", "#E65100"),
        ("sint_quick_wins",    "⚡ Primeros pasos",   "#F3E5F5", "#6A1B9A"),
    ]
    c1s, c2s = st.columns(2)
    for i, (key, label, bg, fg) in enumerate(s_items):
        with (c1s if i % 2 == 0 else c2s):
            content = data.get(key, "")
            display = content if content else '<em style="color:#999;">Sin información — completa el Módulo 9</em>'
            st.markdown(
                f'<div style="background:{bg};border-radius:10px;padding:0.9rem;'
                f'margin-bottom:0.7rem;border-left:4px solid {fg};min-height:80px;">'
                f'<div style="font-weight:700;color:{fg};margin-bottom:0.3rem;'
                f'font-size:0.88rem;">{label}</div>'
                f'<div style="color:#333;font-size:0.85rem;line-height:1.5;">'
                f'{display}</div></div>',
                unsafe_allow_html=True)

    obs = data.get("sint_observaciones", "")
    if obs:
        st.markdown(
            f'<div style="background:#FDF6EC;border-radius:10px;padding:0.9rem;'
            f'border-left:4px solid #A67C00;">'
            f'<strong style="color:#A67C00;">🌿 Observaciones del facilitador</strong><br>'
            f'<span style="font-size:0.88rem;color:#333;">{obs}</span></div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 4 — PLAN DE ACCIÓN
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 🗓️ Plan de Acción")

    fases = [
        ("plan_inmediatas",    "⚡ Inmediatas (0–3 meses)",    "#52B788"),
        ("plan_estacionales",  "🌱 Estacionales (3–12 meses)", "#2D6A4F"),
        ("plan_estructurales", "🏗 Estructurales (1–5 años)",  "#1B4332"),
    ]
    cols_p = st.columns(3)
    for i, (key, label, color) in enumerate(fases):
        acciones = data.get(key, [])
        with cols_p[i]:
            header = (f'<div style="background:rgba(82,183,136,0.07);'
                      f'border-radius:10px;padding:0.8rem;border-top:3px solid {color};">'
                      f'<div style="font-weight:700;color:{color};margin-bottom:0.6rem;'
                      f'font-size:0.88rem;">{label}</div>')
            if isinstance(acciones, list) and acciones:
                rows = ""
                for a in acciones:
                    estado = a.get("estado","") if isinstance(a,dict) else ""
                    titulo = a.get("titulo","") if isinstance(a,dict) else str(a)
                    rows += (f'<div style="padding:0.3rem 0;border-bottom:1px solid '
                             f'rgba(82,183,136,0.2);font-size:0.82rem;color:#333;">'
                             f'{estado} {titulo[:80]}</div>')
                st.markdown(header + rows + "</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    header + '<div style="color:#999;font-size:0.82rem;'
                    'font-style:italic;">Sin acciones — completa el Módulo 9</div></div>',
                    unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 5 — EXPORTAR
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 📥 Exportar Diagnóstico")

    _, cdl, _ = st.columns([1, 2, 1])
    with cdl:
        st.markdown(
            '<div style="background:white;border:2px solid #D8F3DC;border-radius:12px;'
            'padding:1.2rem 1.5rem;">', unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;padding-bottom:0.8rem;">'
            '<div style="font-size:1.8rem;">📊</div>'
            '<div style="font-weight:700;color:#1B4332;font-size:1.05rem;">'
            'Informe Completo LivLin</div>'
            '<div style="color:#666;font-size:0.82rem;margin-top:0.3rem;">'
            'Excel (8 hojas) + Word — Diseño institucional</div></div>',
            unsafe_allow_html=True)

        if not data.get("proyecto_nombre"):
            st.warning("⚠️ Completa al menos el Módulo 1 antes de exportar.")
        else:
            safe_n = data.get("proyecto_nombre", "Diagnostico").replace(" ","_")

            facilitador = st.text_input(
                "👤 Nombre del facilitador/a",
                value=data.get("proyecto_facilitador",""),
                placeholder="Nombre completo del/la facilitador/a",
                key="facilitador_dl")
            if facilitador:
                data["proyecto_facilitador"] = facilitador

            fecha_emision = st.date_input(
                "📅 Fecha de emisión", key="fecha_emision_dl")
            if fecha_emision:
                data["informe_fecha_emision"] = str(fecha_emision)

            st.markdown("---")
            col_xl, col_wd = st.columns(2)
            with col_xl:
                try:
                    xlsx_bytes = generate_excel(data)
                    st.download_button(
                        "⬇️ Excel (.xlsx)", data=xlsx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True, type="primary")
                except Exception as e:
                    st.error(f"Excel: {e}")
            with col_wd:
                try:
                    from utils.docx_generator import generate_docx
                    docx_bytes = generate_docx(data)
                    st.download_button(
                        "⬇️ Word (.docx)", data=docx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                except Exception as e:
                    st.caption(f"Word: {e}")

            st.markdown(
                '<div class="info-box" style="margin-top:0.8rem;font-size:0.8rem;">'
                '🌿 ¿Quieres llevar este proceso más lejos? LivLin ofrece servicios de '
                'diseño regenerativo e implementación. '
                '<a href="https://www.livlin.cl" target="_blank">www.livlin.cl</a></div>',
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _score_level(n: int):
    """Return (label, emoji, color) for a practice count."""
    if n == 0: return "Sin inicio",   "○",  "#9E9E9E"
    if n == 1: return "Iniciando",    "🌱", "#74C69D"
    if n == 2: return "Avanzando",    "🌿", "#52B788"
    if n == 3: return "Consolidado",  "🌳", "#40916C"
    if n <= 5: return "Destacado",    "🌸", "#2D6A4F"
    return     "Referente",           "✨", "#1B4332"
