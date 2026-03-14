"""Módulo de Reporte — Dashboard de resumen y descarga Excel."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_manager import save_visit
from utils.scoring import (
    FLOWER_DOMAINS, compute_domain_scores, compute_regenerative_score,
    score_label, compute_synthesis_potentials
)
from utils.report_generator import generate_excel


def render():
    st.markdown("## 📊 Informe Final del Diagnóstico")
    st.markdown(
        '<p class="module-subtitle">Resumen completo del diagnóstico regenerativo y exportación del informe.</p>',
        unsafe_allow_html=True,
    )
    # Always reload data fresh from disk to reflect all saved changes
    from utils.data_manager import get_visit
    visit_id = st.session_state.visit_data.get("id")
    if visit_id:
        fresh = get_visit(visit_id)
        if fresh:
            st.session_state.visit_data = fresh
    data = st.session_state.visit_data

    # ── Header del informe ─────────────────────────────────────────────────
    proyecto = data.get("proyecto_nombre", "Diagnóstico sin nombre")
    cliente  = data.get("proyecto_cliente", "—")
    ciudad   = data.get("proyecto_ciudad", "—")
    fecha    = data.get("proyecto_fecha", "—")

    global_score = compute_regenerative_score(data)
    label, color = score_label(global_score)

    st.markdown(f"""
        <div class="report-header">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                <div>
                    <div style="font-size:0.8rem; color:#52B788; text-transform:uppercase;
                                letter-spacing:0.1em; margin-bottom:0.3rem;">Diagnóstico Regenerativo LivLin</div>
                    <div style="font-size:1.6rem; font-weight:800; color:#1B4332;">{proyecto}</div>
                    <div style="color:#666; font-size:0.95rem; margin-top:0.3rem;">
                        👤 {cliente}  ·  📍 {ciudad}  ·  📅 {fecha}
                    </div>
                </div>
                <div style="text-align:center; background:rgba(255,255,255,0.7);
                            border-radius:16px; padding:1rem 2rem; border:2px solid #D8F3DC;">
                    <div style="font-size:0.75rem; color:#888; text-transform:uppercase;">Regenerative Score</div>
                    <div style="font-size:3.5rem; font-weight:900; color:#1B4332; line-height:1;">{global_score}</div>
                    <div style="color:#52B788; font-size:0.9rem;">/5.0</div>
                    <div style="font-size:0.8rem; color:{color}; font-weight:600; margin-top:0.3rem;">{label}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 3 columnas: Radar + Potenciales + Métricas clave ──────────────────
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown("#### 🌸 Flor de la Permacultura")
        domain_scores = compute_domain_scores(data)
        categories = [f"{FLOWER_DOMAINS[d]['icon']} {d}" for d in domain_scores]
        values = list(domain_scores.values())

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(82,183,136,0.2)",
            line=dict(color="#2D6A4F", width=2.5),
            marker=dict(size=7, color="#1B4332"),
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(240,255,244,0.4)",
                radialaxis=dict(visible=True, range=[0, 5],
                                tickfont=dict(size=9, color="#2D6A4F"),
                                gridcolor="rgba(45,106,79,0.2)"),
                angularaxis=dict(tickfont=dict(size=10, color="#1B4332")),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=50, r=50, t=20, b=20),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Potenciales del Sitio")
        potenciales = compute_synthesis_potentials(data)
        if any(v > 0 for v in potenciales.values()):
            fig2 = px.bar(
                x=list(potenciales.values()),
                y=list(potenciales.keys()),
                orientation="h",
                color=list(potenciales.values()),
                color_continuous_scale=["#D8F3DC", "#52B788", "#2D6A4F", "#1B4332"],
                range_color=[0, 5],
                text=list(potenciales.values()),
            )
            fig2.update_traces(textposition="outside", textfont_size=13)
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(240,255,244,0.3)",
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(range=[0, 5.5], tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=10)),
                margin=dict(l=10, r=30, t=10, b=10),
                height=330,
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Completa el Módulo 9 para ver los potenciales.")

        # Métricas rápidas
        area = data.get("proyecto_area", 0)
        m2_cult = data.get("cultivo_m2", 0)
        pct_cult = round((float(m2_cult) / float(area)) * 100) if float(area) > 0 else 0
        st.markdown(f"""
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.5rem;">
                <div class="metric-mini">
                    <div class="metric-val">{int(area)} m²</div>
                    <div class="metric-lbl">Área total</div>
                </div>
                <div class="metric-mini">
                    <div class="metric-val">{int(m2_cult)} m²</div>
                    <div class="metric-lbl">M² cultivables</div>
                </div>
                <div class="metric-mini">
                    <div class="metric-val">{pct_cult}%</div>
                    <div class="metric-lbl">Del área cultivable</div>
                </div>
                <div class="metric-mini">
                    <div class="metric-val">{global_score}/5</div>
                    <div class="metric-lbl">Reg. Score</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ── Síntesis narrativa ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📝 Síntesis del Diagnóstico")
    col3, col4 = st.columns(2)

    sintesis_items = [
        ("sint_fortalezas",    "💪 Fortalezas",            "#D8F3DC", "#1B4332"),
        ("sint_oportunidades", "🚀 Oportunidades",          "#E3F2FD", "#1565C0"),
        ("sint_limitaciones",  "⚠️ Limitaciones",           "#FFF3E0", "#E65100"),
        ("sint_quick_wins",    "⚡ Quick Wins",             "#F3E5F5", "#6A1B9A"),
    ]
    for i, (key, label, bg, fg) in enumerate(sintesis_items):
        with col3 if i % 2 == 0 else col4:
            content = data.get(key, "")
            st.markdown(f"""
                <div style="background:{bg}; border-radius:12px; padding:1rem; margin-bottom:0.75rem;
                            border-left:4px solid {fg}; min-height:80px;">
                    <div style="font-weight:700; color:{fg}; margin-bottom:0.4rem; font-size:0.9rem;">{label}</div>
                    <div style="color:#333; font-size:0.88rem; line-height:1.5;">
                        {content if content else '<em style="color:#999;">Sin información</em>'}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    obs = data.get("sint_observaciones", "")
    if obs:
        st.markdown(f"""
            <div style="background:#FDF6EC; border-radius:12px; padding:1rem; margin-top:0.5rem;
                        border-left:4px solid #A67C00;">
                <div style="font-weight:700; color:#A67C00; margin-bottom:0.4rem;">🌿 Observaciones finales</div>
                <div style="color:#333; font-size:0.9rem; line-height:1.6;">{obs}</div>
            </div>
        """, unsafe_allow_html=True)

    # ── Plan de acción resumen ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🗓️ Plan de Acción")

    fases = [
        ("plan_inmediatas",    "⚡ Inmediatas (0–3 meses)",     "#52B788"),
        ("plan_estacionales",  "🌱 Estacionales (3–12 meses)",  "#2D6A4F"),
        ("plan_estructurales", "🏗 Estructurales (1–5 años)",   "#1B4332"),
    ]
    cols_plan = st.columns(3)
    for i, (key, label, color) in enumerate(fases):
        acciones = data.get(key, [])
        with cols_plan[i]:
            st.markdown(f"""
                <div style="background:rgba(82,183,136,0.07); border-radius:12px; padding:1rem;
                            border-top:3px solid {color};">
                    <div style="font-weight:700; color:{color}; margin-bottom:0.75rem;">{label}</div>
            """, unsafe_allow_html=True)
            if isinstance(acciones, list) and acciones:
                for accion in acciones:
                    estado = accion.get("estado", "")
                    st.markdown(f"""
                        <div style="padding:0.4rem 0; border-bottom:1px solid rgba(82,183,136,0.2);
                                    font-size:0.85rem; color:#333;">
                            {estado} {accion.get('titulo', '')[:80]}{'…' if len(accion.get('accion',''))>80 else ''}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#999; font-size:0.85rem; font-style:italic;">Sin acciones registradas</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Exportar ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📥 Exportar Diagnóstico")

    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        st.markdown('<div class="download-box">', unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align:center; padding:0.5rem 0 1rem;">
                <div style="font-size:2rem;">📊</div>
                <div style="font-weight:700; color:#1B4332; font-size:1.1rem;">Informe Excel Completo</div>
                <div style="color:#666; font-size:0.85rem; margin:0.5rem 0;">
                    9 hojas · Todos los módulos · Diseño profesional LivLin
                </div>
            </div>
        """, unsafe_allow_html=True)

        if not data.get("proyecto_nombre"):
            st.warning("⚠️ Completa al menos el Módulo 1 antes de exportar.")
        else:
            safe_n = data.get('proyecto_nombre','Diagnostico').replace(' ','_')

            st.markdown("**Antes de descargar — Datos del informe:**")
            facilitador = st.text_input(
                "👤 Nombre del facilitador/a",
                value=data.get("proyecto_facilitador",""),
                placeholder="Nombre completo del facilitador que realizó la visita",
                key="facilitador_dl")
            if facilitador:
                data["proyecto_facilitador"] = facilitador

            fecha_emision = st.date_input(
                "📅 Fecha de emisión del informe",
                key="fecha_emision_dl")
            if fecha_emision:
                data["informe_fecha_emision"] = str(fecha_emision)

            st.markdown("---")

            xlsx_bytes = generate_excel(data)
            col_xl, col_wd = st.columns(2)
            with col_xl:
                st.download_button(
                    label="⬇️ Descargar Excel (.xlsx)",
                    data=xlsx_bytes,
                    file_name=f"LivLin_IR_{safe_n}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary",
                )
            with col_wd:
                try:
                    from utils.docx_generator import generate_docx
                    docx_bytes = generate_docx(data)
                    st.download_button(
                        label="⬇️ Descargar Informe Word (.docx)",
                        data=docx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.caption(f"⚠️ Word no disponible: {e}")
            st.caption("💡 Datos guardados en Supabase. Descarga los archivos desde aquí.")
            st.markdown(
                '<div class="info-box">🌿 <strong>¿Quieres llevar este proceso más lejos?</strong><br>'
                'LivLin ofrece servicios de diseño regenerativo, talleres e implementación '
                'para transformar el potencial de este diagnóstico en realidad. '
                '<a href="https://www.livlin.cl" target="_blank">www.livlin.cl</a> · '
                '<em>Potencial para una vida regenerativa</em></div>',
                unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
