"""Módulo Informe Final v7.0 — LivLin Indagación Regenerativa.
ERP (Estado Regenerativo Presente) + HRP (Horizonte Regenerativo Potencial).
Vista con navegación por secciones (sidebar show/hide).
Escala 0-10, 5 niveles narrativos.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.data_manager import save_visit
from utils.scoring import (
    FLOWER_DOMAINS, PETAL_ORDER,
    compute_domain_scores, compute_domain_scores_total,
    compute_erp, compute_hrp,
    compute_regenerative_score, compute_regenerative_score_potential,
    score_label, _score_to_level, _score_to_level_idx,
    compute_synthesis_potentials, compute_synthesis_potentials_obs,
    compute_cross_module_score, CROSS_MODULE_DETAIL,
    get_interp_text, get_petal_interp,
    ERP_HRP_METODOLOGIA, _ipr_obs_counts, _ipr_tot_counts,
    DIM_WHAT_MEASURES, brecha_texto, brecha_valor,
)
from utils.report_generator import generate_excel


def _safe_float(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default

def _val(data, key, default="No registrado"):
    v = data.get(key)
    if v in [None, "", [], 0, 0.0]: return default
    return v

def _show_field(label, value, empty_msg="No registrado"):
    if value in [None, "", [], 0, 0.0]: return
    st.markdown(
        f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
        f'<span style="font-size:0.75rem;color:#52B788;text-transform:uppercase;">{label}</span><br>'
        f'<span style="font-size:0.88rem;color:#1B4332;">{value}</span></div>',
        unsafe_allow_html=True)

def _card(label, value, bg="#F0FFF4", fg="#1B4332", border="#52B788"):
    if not value or value == "No registrado": return
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.6rem 0.8rem;'
        f'margin-bottom:0.5rem;border-left:3px solid {border};">'
        f'<div style="font-size:0.72rem;color:{border};text-transform:uppercase;margin-bottom:0.2rem;">{label}</div>'
        f'<div style="font-size:0.88rem;color:{fg};line-height:1.5;">{value}</div></div>',
        unsafe_allow_html=True)

def _list_from_semicolon(text):
    if not text: return []
    return [item.strip() for item in text.split(";") if item.strip()]

def _render_sintesis_list(items_text, label, bg, fg):
    if not items_text: return
    items = _list_from_semicolon(items_text)
    if not items:
        st.markdown(f'<div style="background:{bg};border-radius:8px;padding:0.7rem;'
                    f'border-left:3px solid {fg};margin-bottom:0.5rem;">'
                    f'<div style="font-size:0.8rem;font-weight:700;color:{fg};">{label}</div>'
                    f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{items_text}</div></div>',
                    unsafe_allow_html=True)
        return
    rows = "".join(f'<div style="padding:0.25rem 0;border-bottom:1px solid rgba(0,0,0,0.06);font-size:0.85rem;color:#333;">{item}</div>' for item in items)
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.7rem;'
        f'border-left:3px solid {fg};margin-bottom:0.5rem;">'
        f'<div style="font-size:0.8rem;font-weight:700;color:{fg};margin-bottom:0.4rem;">{label}</div>'
        f'{rows}</div>', unsafe_allow_html=True)


def _radar_erp(domain_obs, height=380):
    """Radar ERP: solo observado. Escala 0-10."""
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_obs = [domain_obs[p] for p in PETAL_ORDER] + [domain_obs[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_obs, theta=theta, name="ERP — Estado presente",
        fill="toself", fillcolor="rgba(27,67,50,0.22)",
        line=dict(color="#1B4332", width=2.5),
        marker=dict(size=7, color="#1B4332"),
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(240,255,244,0.4)",
            radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10],
                tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
            angularaxis=dict(tickfont=dict(size=10,color="#1B4332")),
        ),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
    )
    return fig

def _radar_hrp(domain_tot, height=380):
    """Radar HRP: observado+potencial. Escala 0-10."""
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_tot = [domain_tot[p] for p in PETAL_ORDER] + [domain_tot[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_tot, theta=theta, name="HRP — Horizonte potencial",
        fill="toself", fillcolor="rgba(82,183,136,0.15)",
        line=dict(color="#52B788", width=2, dash="dash"),
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(240,255,244,0.4)",
            radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10],
                tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
            angularaxis=dict(tickfont=dict(size=10,color="#1B4332")),
        ),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
    )
    return fig

def _dual_radar(domain_obs, domain_tot, height=400):
    """Dual radar: ERP (dark) + HRP (dashed). Escala 0-10."""
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_obs = [domain_obs[p] for p in PETAL_ORDER] + [domain_obs[PETAL_ORDER[0]]]
    r_tot = [domain_tot[p] for p in PETAL_ORDER] + [domain_tot[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_tot, theta=theta, name="HRP · Horizonte potencial",
        fill="toself", fillcolor="rgba(82,183,136,0.10)",
        line=dict(color="#52B788", width=2, dash="dash"),
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_obs, theta=theta, name="ERP · Estado presente",
        fill="toself", fillcolor="rgba(27,67,50,0.22)",
        line=dict(color="#1B4332", width=2.5),
        marker=dict(size=7, color="#1B4332"),
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(240,255,244,0.4)",
            radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10],
                tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
            angularaxis=dict(tickfont=dict(size=10,color="#1B4332")),
        ),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
    )
    return fig


def _render_report_map(lat, lon, data):
    try:
        import folium
        from streamlit_folium import st_folium
        m = folium.Map(location=[lat,lon], zoom_start=16, tiles="CartoDB positron")
        folium.Marker([lat,lon],
            popup=folium.Popup(f"<b>{data.get('proyecto_nombre','Espacio')}</b><br>Lat: {lat:.6f}  Lon: {lon:.6f}", max_width=250),
            tooltip=data.get("proyecto_nombre","Espacio"),
            icon=folium.Icon(color="green",icon="leaf",prefix="fa"),
        ).add_to(m)
        nearby_raw = data.get("entorno_lugares_cercanos")
        if nearby_raw:
            try:
                import ast as _a
                places = _a.literal_eval(nearby_raw) if isinstance(nearby_raw,str) else nearby_raw
                for p in (places or [])[:12]:
                    folium.CircleMarker([p["lat"],p["lon"]], radius=7, color="#1565C0",
                        fill=True, fill_color="#1565C0", fill_opacity=0.6,
                        popup=f"{p['name']} ({p.get('dist_m',0)} m)", tooltip=p["name"],
                    ).add_to(m)
            except: pass
        st_folium(m, width="100%", height=380, returned_objects=[])
    except ImportError:
        import pandas as pd
        st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}), zoom=15)


# ── Section registry for client sidebar navigation ────────────────────
REPORT_SECTIONS = {
    "vision":      "🌱 Visión y Estado Regenerativo",
    "comparada":   "📊 Perspectiva Comparada",
    "erp":         "🌍 ERP — Estado Presente",
    "hrp":         "🌱 HRP — Horizonte Potencial",
    "datos":       "📋 Datos del Proyecto",
    "tao":         "☯️ Tao de la Regeneración",
    "ecologia":    "🔬 Observación Ecológica",
    "sistemas":    "🏙️ Contexto, Agua y Energía",
    "fotos":       "📷 Registro Fotográfico",
    "flor":        "🌸 Flor de la Permacultura",
    "potenciales": "🌿 Potenciales del Sitio",
    "sintesis":    "🗺️ Síntesis y Plan",
    "biblio":      "📚 Bibliografía",
}

def render():
    from utils.data_manager import get_visit
    visit_id = st.session_state.get("visit_data",{}).get("id")
    if visit_id:
        fresh = get_visit(visit_id)
        if fresh: st.session_state.visit_data = fresh
    data = st.session_state.get("visit_data", {})
    user = st.session_state.get("current_user", {})
    readonly = user.get("role","user") != "admin"

    if not data.get("id"):
        st.warning("Carga o crea un diagnóstico primero.")
        return

    # ── Compute scores ────────────────────────────────────────────────
    domain_obs = compute_domain_scores(data)
    domain_tot = compute_domain_scores_total(data)
    erp_score  = compute_erp(data)
    hrp_score  = compute_hrp(data)
    label_erp, color_erp = score_label(erp_score)
    label_hrp, color_hrp = score_label(hrp_score)
    brecha = brecha_valor(erp_score, hrp_score)
    brecha_txt = brecha_texto(erp_score, hrp_score)
    potenciales_hrp = compute_synthesis_potentials(data)
    potenciales_erp = compute_synthesis_potentials_obs(data)
    cross = compute_cross_module_score(data)
    ipr_obs_counts = _ipr_obs_counts(data)
    ipr_tot_counts = _ipr_tot_counts(data)

    nombre  = data.get("proyecto_nombre","Diagnóstico")
    cliente = data.get("proyecto_cliente","—")
    ciudad  = data.get("proyecto_ciudad","—")
    fecha   = data.get("proyecto_fecha","—")

    STATUS_BADGE = {
        "respondido":  '<span style="background:#D8F3DC;color:#1B4332;border-radius:4px;padding:1px 8px;font-size:0.72rem;font-weight:600;">Respondido</span>',
        "inferido":    '<span style="background:#FFF3CD;color:#856404;border-radius:4px;padding:1px 8px;font-size:0.72rem;font-weight:600;">Inferido</span>',
        "no_abordado": '<span style="background:#F5F5F5;color:#757575;border-radius:4px;padding:1px 8px;font-size:0.72rem;">No abordado</span>',
        "":            '<span style="background:#F5F5F5;color:#757575;border-radius:4px;padding:1px 8px;font-size:0.72rem;">Sin estado</span>',
    }
    def _status_badge(mod_key):
        s = data.get(mod_key, "respondido")
        return STATUS_BADGE.get(s, STATUS_BADGE[""])

    # ── Sidebar section navigation (for clients) ─────────────────────
    if "report_section" not in st.session_state:
        st.session_state.report_section = "all"

    if readonly:
        with st.sidebar:
            st.markdown('<div style="font-size:0.75rem;color:#40916C;font-weight:700;margin-bottom:0.3rem;">Secciones del informe</div>', unsafe_allow_html=True)
            if st.button("📖 Ver informe completo", use_container_width=True, key="nav_all",
                         type="primary" if st.session_state.report_section == "all" else "secondary"):
                st.session_state.report_section = "all"; st.rerun()
            for sec_key, sec_label in REPORT_SECTIONS.items():
                active = st.session_state.report_section == sec_key
                if st.button(sec_label, use_container_width=True, key=f"nav_{sec_key}",
                             type="primary" if active else "secondary"):
                    st.session_state.report_section = sec_key; st.rerun()

    active_sec = st.session_state.get("report_section", "all")
    def _show(sec_key):
        return active_sec == "all" or active_sec == sec_key


    # ── Header ────────────────────────────────────────────────────────
    st.markdown("## Informe Final del Diagnóstico Regenerativo")
    st.markdown('<p class="module-subtitle">Visión completa · LivLin v7.0 · ERP + HRP</p>', unsafe_allow_html=True)

    # ── Lectura introductoria Mason (2025) ────────────────────────────
    if _show("vision"):
        st.markdown(
            '<div style="background:linear-gradient(135deg,#F0FFF4,#E8F5E9);border:2px solid #52B788;'
            'border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;">'
            '<div style="font-size:0.72rem;color:#52B788;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">Antes de leer este informe</div>'
            '<div style="font-size:1.1rem;font-weight:800;color:#1B4332;margin-bottom:0.5rem;">¿Qué significa regenerar?</div>'
            '<div style="font-size:0.9rem;color:#2D6A4F;line-height:1.7;margin-bottom:0.8rem;">'
            'Este informe describe el potencial regenerativo de tu espacio usando dos indicadores: el Estado Regenerativo Presente (ERP) y el Horizonte Regenerativo Potencial (HRP). '
            'La diferencia entre ambos señala el camino: cómo pasar de lo que ya tenemos a lo que podemos llegar a ser.</div>',
            unsafe_allow_html=True)
        col_m1, col_m2, col_m3 = st.columns([1,1,1])
        with col_m1:
            st.markdown('<a href="https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing" target="_blank" style="display:block;background:#1B4332;color:white;border-radius:8px;padding:0.7rem 1rem;text-align:center;font-weight:700;font-size:0.88rem;text-decoration:none;">Leer en Google Drive</a>', unsafe_allow_html=True)
        with col_m2:
            st.markdown('<a href="https://doi.org/10.17605/OSF.IO/UCDEH" target="_blank" style="display:block;background:#2D6A4F;color:white;border-radius:8px;padding:0.7rem 1rem;text-align:center;font-weight:700;font-size:0.88rem;text-decoration:none;">Ver en OSF</a>', unsafe_allow_html=True)
        with col_m3:
            st.markdown('<div style="font-size:0.8rem;color:#555;padding:0.5rem 0;">Mason, F. (2025). <em>Introducción al enfoque de la regeneración.</em> LivLin.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        # ── ERP + HRP header cards ────────────────────────────────────
        st.markdown(f"""
            <div style="background:linear-gradient(135deg,#F0FFF4,#D8F3DC);border:2px solid #52B788;border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                    <div>
                        <div style="font-size:0.72rem;color:#52B788;text-transform:uppercase;letter-spacing:0.1em;">Diagnóstico Regenerativo · LivLin v7.0</div>
                        <div style="font-size:1.5rem;font-weight:800;color:#1B4332;margin:0.2rem 0;">{nombre}</div>
                        <div style="color:#555;font-size:0.88rem;">{cliente} · {ciudad} · {fecha}</div>
                    </div>
                    <div style="display:flex;gap:0.8rem;flex-wrap:wrap;">
                        <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px solid #D8F3DC;min-width:120px;">
                            <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌍 ERP</div>
                            <div style="font-size:2.8rem;font-weight:900;color:#1B4332;line-height:1;">{erp_score}</div>
                            <div style="color:#52B788;font-size:0.75rem;">/10</div>
                            <div style="font-size:0.72rem;color:{color_erp};font-weight:600;margin-top:0.2rem;">{label_erp}</div>
                        </div>
                        <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px dashed #52B788;min-width:120px;">
                            <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌱 HRP</div>
                            <div style="font-size:2.8rem;font-weight:900;color:#52B788;line-height:1;">{hrp_score}</div>
                            <div style="color:#52B788;font-size:0.75rem;">/10</div>
                            <div style="font-size:0.72rem;color:{color_hrp};font-weight:600;margin-top:0.2rem;">{label_hrp}</div>
                        </div>
                        <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px solid #FFA726;min-width:120px;">
                            <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌀 Brecha</div>
                            <div style="font-size:2.8rem;font-weight:900;color:#FFA726;line-height:1;">{brecha}</div>
                            <div style="color:#FFA726;font-size:0.75rem;">pts</div>
                            <div style="font-size:0.72rem;color:#E65100;font-weight:600;margin-top:0.2rem;">Campo de acción</div>
                        </div>
                    </div>
                </div>
                <div style="margin-top:0.8rem;padding:0.6rem;background:rgba(255,167,38,0.08);border-radius:8px;font-size:0.85rem;color:#E65100;">
                    🌀 {brecha_txt}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Methodology expander
        with st.expander("Cómo se calculan el ERP y HRP", expanded=False):
            st.markdown('<div style="background:#F0FFF4;border-radius:12px;padding:1.2rem;">', unsafe_allow_html=True)
            st.markdown("#### Estado Regenerativo Presente (ERP)")
            st.markdown("Es la fotografía del momento actual. Refleja lo que ya existe y podemos constatar.")
            st.markdown("**Composición:** 80% Modelo Flor de la Permacultura (MFP observado) + 20% Sub-indicadores M2-6")
            st.markdown("#### Horizonte Regenerativo Potencial (HRP)")
            st.markdown("Es la visión de lo que el espacio puede llegar a ser si se activan procesos regenerativos.")
            st.markdown("**Composición:** 100% MFP proyectado (observado + potencial identificado)")
            st.markdown("#### Brecha (HRP − ERP)")
            st.markdown("El espacio entre ERP y HRP es el campo de acción donde se definen estrategias y prioridades.")
            st.markdown("#### Escala 0-10, 5 niveles")
            st.markdown("0-2 Sin inicio | 2-4 Semilla | 4-6 Brote | 6-8 Crecimiento | 8-10 Abundancia")
            st.markdown("#### Puntuación MFP por prácticas")
            st.markdown("0=0 | 1-2=2 | 3-5=4 | 6-9=6 | 10-14=8 | 15+=10")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # PERSPECTIVA COMPARADA
    # ══════════════════════════════════════════════════════════════════
    if _show("comparada"):
        st.markdown("### 📊 Perspectiva Comparada — ERP vs HRP")
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
                    'Vista integrada de ambos indicadores. Las barras apiladas muestran el estado presente (ERP) y el potencial adicional hasta el horizonte (HRP) para cada dimensión.</div>', unsafe_allow_html=True)

        # Stacked bar chart — 10 dimensions
        dims = list(potenciales_erp.keys())
        erp_vals = [potenciales_erp[d] for d in dims]
        hrp_vals = [potenciales_hrp[d] for d in dims]
        gap_vals = [max(0, round(h - e, 1)) for e, h in zip(erp_vals, hrp_vals)]

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name="ERP (presente)", y=dims, x=erp_vals, orientation="h",
            marker_color="#1B4332", text=[f"{v:.1f}" for v in erp_vals], textposition="inside"))
        fig_comp.add_trace(go.Bar(name="Brecha → HRP", y=dims, x=gap_vals, orientation="h",
            marker_color="rgba(82,183,136,0.5)", text=[f"+{v:.1f}" if v > 0 else "" for v in gap_vals], textposition="inside"))
        fig_comp.update_layout(barmode="stack", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(240,255,244,0.3)", showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(range=[0,11], tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)), margin=dict(l=10,r=30,t=30,b=10), height=380)
        st.plotly_chart(fig_comp, use_container_width=True, key="bar_comparada")

        # Stacked bar chart — 7 petals
        st.markdown("**Pétalos de la Flor de la Permacultura:**")
        petal_names = [f"{FLOWER_DOMAINS[p]['icon']} {p[:25]}" for p in PETAL_ORDER]
        erp_pet = [domain_obs[p] for p in PETAL_ORDER]
        hrp_pet = [domain_tot[p] for p in PETAL_ORDER]
        gap_pet = [max(0, round(h-e,1)) for e,h in zip(erp_pet, hrp_pet)]

        fig_pet = go.Figure()
        fig_pet.add_trace(go.Bar(name="ERP", y=petal_names, x=erp_pet, orientation="h",
            marker_color="#1B4332", text=[f"{v:.0f}" for v in erp_pet], textposition="inside"))
        fig_pet.add_trace(go.Bar(name="→ HRP", y=petal_names, x=gap_pet, orientation="h",
            marker_color="rgba(82,183,136,0.5)", text=[f"+{v:.0f}" if v>0 else "" for v in gap_pet], textposition="inside"))
        fig_pet.update_layout(barmode="stack", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(240,255,244,0.3)", showlegend=True,
            legend=dict(orientation="h",yanchor="bottom",y=1.02),
            xaxis=dict(range=[0,11]), margin=dict(l=10,r=30,t=30,b=10), height=320)
        st.plotly_chart(fig_pet, use_container_width=True, key="bar_pet_comp")

        # Interpretations for all dimensions — both ERP and HRP
        st.markdown("**Interpretación de resultados:**")
        for dim in dims:
            e_val = potenciales_erp[dim]
            h_val = potenciales_hrp[dim]
            interp_e = get_interp_text(dim, e_val, "erp")
            interp_h = get_interp_text(dim, h_val, "hrp")
            lv_e, cl_e = _score_to_level(e_val)
            lv_h, cl_h = _score_to_level(h_val)
            dim_info = DIM_WHAT_MEASURES.get(dim, {})
            icono = dim_info.get("icono","")
            with st.expander(f"{icono} {dim} — ERP {e_val}/10 → HRP {h_val}/10", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;border-left:3px solid #1B4332;">'
                                f'<div style="font-size:0.72rem;font-weight:700;color:#1B4332;">🌍 ERP · {e_val}/10 · {lv_e}</div>'
                                f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{interp_e}</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem;border-left:3px dashed #52B788;">'
                                f'<div style="font-size:0.72rem;font-weight:700;color:#2D6A4F;">🌱 HRP · {h_val}/10 · {lv_h}</div>'
                                f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{interp_h}</div></div>', unsafe_allow_html=True)
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # ERP — ESTADO REGENERATIVO PRESENTE
    # ══════════════════════════════════════════════════════════════════
    if _show("erp"):
        st.markdown("### 🌍 Estado Regenerativo Presente (ERP)")
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
                    'Es la fotografía del momento actual: el nivel de regeneración que el espacio ya manifiesta hoy. '
                    'Genera confianza porque se basa en datos observables. Permite reconocer logros y fortalezas existentes.</div>', unsafe_allow_html=True)

        col_radar, col_info = st.columns([1.3, 0.7])
        with col_radar:
            fig_erp = _radar_erp(domain_obs)
            st.plotly_chart(fig_erp, use_container_width=True, key="radar_erp")
        with col_info:
            st.markdown(f'<div style="background:white;border:2px solid #D8F3DC;border-radius:10px;padding:0.8rem;text-align:center;margin-bottom:0.8rem;">'
                        f'<div style="font-size:0.68rem;color:#888;text-transform:uppercase;">🌍 ERP</div>'
                        f'<div style="font-size:3rem;font-weight:900;color:#1B4332;line-height:1;">{erp_score}</div>'
                        f'<div style="color:#52B788;font-size:0.8rem;">/10</div>'
                        f'<div style="font-size:0.78rem;color:{color_erp};font-weight:600;margin-top:0.2rem;">{label_erp}</div></div>', unsafe_allow_html=True)
            st.markdown("**Composición:** 80% MFP obs. + 20% M2-6")
            for i, p in enumerate(PETAL_ORDER):
                s = domain_obs[p]
                lv, cl = _score_to_level(s)
                icon = FLOWER_DOMAINS[p]["icon"]
                pct = int(s / 10 * 100)
                st.markdown(f'<div style="padding:3px 0;border-bottom:1px solid #D8F3DC;">'
                            f'<div style="display:flex;justify-content:space-between;font-size:0.78rem;">'
                            f'<span style="color:#1B4332;">{icon} {p[:26]}</span>'
                            f'<span style="background:{cl};color:white;border-radius:4px;padding:1px 6px;font-size:0.7rem;">{s:.0f}</span></div>'
                            f'<div style="background:#E8F5E9;height:5px;border-radius:3px;margin-top:2px;">'
                            f'<div style="background:{cl};width:{min(pct,100)}%;height:5px;border-radius:3px;"></div></div></div>', unsafe_allow_html=True)

        # Sub-indicadores M2-6 with transparency expander
        if cross:
            st.markdown("**Sub-indicadores M2-6 (aportan 20% al ERP):**")
            for name, info in cross.items():
                s = info["score"]
                lv, cl = _score_to_level(s)
                st.markdown(f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
                            f'<div style="display:flex;justify-content:space-between;font-size:0.78rem;">'
                            f'<span style="color:#1B4332;">{name}</span>'
                            f'<span style="background:{cl};color:white;border-radius:4px;padding:1px 5px;font-size:0.7rem;">{s}/10</span></div>'
                            f'<div style="font-size:0.7rem;color:#666;">{info["fuente"]}</div></div>', unsafe_allow_html=True)

            with st.expander("🔍 Transparencia: qué variables evalúa cada sub-indicador y su escala", expanded=False):
                for name, detail in CROSS_MODULE_DETAIL.items():
                    actual_score = cross.get(name, {}).get("score", "—")
                    st.markdown(f"**{detail.get('icono','')} {name}** — Puntaje: {actual_score}/10")
                    st.markdown(f"*Fórmula: {detail['formula']}* · Fuente: {detail['fuente']}")
                    for var_name, var_scale in detail["variables"]:
                        st.markdown(f"- {var_name}: {var_scale}")
                    st.markdown("---")
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # HRP — HORIZONTE REGENERATIVO POTENCIAL
    # ══════════════════════════════════════════════════════════════════
    if _show("hrp"):
        st.markdown("### 🌱 Horizonte Regenerativo Potencial (HRP)")
        st.markdown('<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
                    'Es la visión de lo que el espacio puede llegar a ser si se activan procesos regenerativos. '
                    'Inspira y moviliza hacia un futuro deseable. Funciona como brújula estratégica.</div>', unsafe_allow_html=True)

        col_radar2, col_info2 = st.columns([1.3, 0.7])
        with col_radar2:
            fig_hrp = _radar_hrp(domain_tot)
            st.plotly_chart(fig_hrp, use_container_width=True, key="radar_hrp")
        with col_info2:
            st.markdown(f'<div style="background:white;border:2px dashed #52B788;border-radius:10px;padding:0.8rem;text-align:center;margin-bottom:0.8rem;">'
                        f'<div style="font-size:0.68rem;color:#888;text-transform:uppercase;">🌱 HRP</div>'
                        f'<div style="font-size:3rem;font-weight:900;color:#52B788;line-height:1;">{hrp_score}</div>'
                        f'<div style="color:#52B788;font-size:0.8rem;">/10</div>'
                        f'<div style="font-size:0.78rem;color:{color_hrp};font-weight:600;margin-top:0.2rem;">{label_hrp}</div></div>', unsafe_allow_html=True)
            st.markdown("**Composición:** 100% MFP proyectado")
            for i, p in enumerate(PETAL_ORDER):
                s_o = domain_obs[p]
                s_t = domain_tot[p]
                icon = FLOWER_DOMAINS[p]["icon"]
                delta = f"+{s_t-s_o:.0f}" if s_t > s_o else ""
                lv, cl = _score_to_level(s_t)
                pct = int(s_t / 10 * 100)
                st.markdown(f'<div style="padding:3px 0;border-bottom:1px solid #D8F3DC;">'
                            f'<div style="display:flex;justify-content:space-between;font-size:0.78rem;">'
                            f'<span style="color:#1B4332;">{icon} {p[:26]}</span>'
                            f'<span style="background:{cl};color:white;border-radius:4px;padding:1px 6px;font-size:0.7rem;">{s_t:.0f} {delta}</span></div>'
                            f'<div style="background:#E8F5E9;height:5px;border-radius:3px;margin-top:2px;">'
                            f'<div style="background:{cl};width:{min(pct,100)}%;height:5px;border-radius:3px;"></div></div></div>', unsafe_allow_html=True)

        # Brecha summary
        st.markdown(f'<div style="background:rgba(255,167,38,0.08);border:2px solid #FFA726;border-radius:12px;padding:1rem;margin-top:0.5rem;">'
                    f'<div style="font-size:0.88rem;font-weight:700;color:#E65100;">🌀 Brecha: {brecha} puntos</div>'
                    f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{brecha_txt}</div></div>', unsafe_allow_html=True)

        # Petal interpretations
        st.markdown("**Interpretación por pétalo (HRP):**")
        for i, p in enumerate(PETAL_ORDER):
            s_t = domain_tot[p]
            icon = FLOWER_DOMAINS[p]["icon"]
            interp_h = get_petal_interp(p, s_t, "hrp")
            with st.expander(f"{icon} {p}", expanded=False):
                st.markdown(f'<div style="font-size:0.85rem;color:#333;">{interp_h}</div>', unsafe_allow_html=True)
                new_data = data.get(f"petalo_{i}_pot_new", {})
                new_list = [a for v in new_data.values() if isinstance(v,list) for a in v]
                new_list += data.get(f"petalo_{i}_otros_new", [])
                if new_list:
                    st.markdown('<div style="font-size:0.75rem;color:#52B788;font-weight:600;margin-top:0.4rem;">Prácticas potenciales:</div>', unsafe_allow_html=True)
                    for a in new_list:
                        st.markdown(f'<div style="font-size:0.8rem;color:#333;padding:0.1rem 0 0.1rem 0.5rem;">— {a}</div>', unsafe_allow_html=True)
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN — DATOS DEL PROYECTO
    # ══════════════════════════════════════════════════════════════════
    if _show("datos"):
        st.markdown(f"### 1. Datos del Proyecto &nbsp; {_status_badge('mod_cliente')}", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            _show_field("Nombre del proyecto", data.get("proyecto_nombre"))
            _show_field("Grupo / familia", data.get("proyecto_cliente"))
            _show_field("Dirección", data.get("proyecto_direccion"))
            _show_field("Ciudad", data.get("proyecto_ciudad"))
            _show_field("País", data.get("proyecto_pais"))
            _show_field("Fecha", data.get("proyecto_fecha"))
        with c2:
            _show_field("Tipo de espacio", data.get("proyecto_tipo_espacio"))
            _show_field("Área total (m²)", data.get("proyecto_area") or data.get("proyecto_superficie"))
            _show_field("Composición del grupo", data.get("proyecto_composicion"))
            adultos = data.get("proyecto_n_adultos")
            ninos = data.get("proyecto_n_ninos")
            if adultos or ninos:
                _show_field("Habitantes", f"{adultos or 0} adultos, {ninos or 0} niños/as")
            _show_field("Descripción del grupo", data.get("proyecto_habitantes"))
            _show_field("🐾 Mascotas y animales", data.get("proyecto_mascotas"))

        if data.get("geo_display"):
            _show_field("Ubicación", data.get("geo_display"))
        lat = data.get("geo_lat")
        lon = data.get("geo_lon")
        if lat and lon:
            lat_f, lon_f = float(lat), float(lon)
            st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:0.6rem 1rem;border-left:3px solid #52B788;margin-bottom:0.5rem;font-size:0.85rem;"><strong>Coordenadas:</strong> {lat_f:.6f}, {lon_f:.6f}</div>', unsafe_allow_html=True)
            _render_report_map(lat_f, lon_f, data)

        # Intención
        intencion_fields = [("intencion_motivo","Motivo"),("intencion_cambios","Cambios deseados"),("intencion_vision5","Visión 5 años"),
            ("intencion_intentado","Intentos previos"),("intencion_mejor","Lo que funciona"),("intencion_frustracion","Frustraciones"),
            ("intencion_recursos","Recursos disponibles"),("intencion_suenos","Sueños"),("intencion_notas","Notas del facilitador")]
        has_int = any(data.get(k) for k,_ in intencion_fields)
        if has_int:
            st.markdown("**Intención del grupo habitante:**")
            c1i, c2i = st.columns(2)
            for i, (key, label) in enumerate(intencion_fields):
                v = data.get(key, "")
                if v and str(v).strip():
                    with (c1i if i%2==0 else c2i):
                        _card(label, str(v).strip())
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # TAO DE LA REGENERACIÓN
    # ══════════════════════════════════════════════════════════════════
    if _show("tao"):
        st.markdown(f"### 2. Tao de la Regeneración &nbsp; {_status_badge('mod_tao')}", unsafe_allow_html=True)
        mod_tao = data.get("mod_tao","")
        if mod_tao == "no_abordado":
            st.markdown('<div style="color:#999;font-style:italic;">No abordado.</div>', unsafe_allow_html=True)
        else:
            tao_text_fields = [("tao_sensacion","Sensación"),("tao_deseado","Deseado"),("tao_no_deseado","No deseado"),
                ("tao_llama","Lo que llama"),("tao_consumo","Consumo"),("tao_actividades","Actividades"),
                ("tao_naturaleza_rel","Relación naturaleza"),("tao_aprender","Aprender"),("tao_justicia","Justicia"),
                ("tao_palabra_esencial","Palabra esencial"),("tao_cc_impacto","Impacto CC"),("tao_cc_respuesta","Respuesta CC")]
            items = [(l, str(data.get(k,""))) for k,l in tao_text_fields if data.get(k)]
            if items:
                c1,c2 = st.columns(2)
                for i,(label,val) in enumerate(items):
                    with (c1 if i%2==0 else c2): _card(label, val)
            sal_fields = [("sal_alimentacion","Alimentación"),("sal_ejercicio","Actividad física"),("sal_contacto_naturaleza","Contacto naturaleza")]
            has_sal = any(data.get(k) for k,_ in sal_fields)
            if has_sal:
                st.markdown("**Alimentación y actividad física:**")
                cs1,cs2 = st.columns(2)
                for i,(key,label) in enumerate(sal_fields):
                    v = data.get(key,"")
                    if v: 
                        with (cs1 if i%2==0 else cs2): _card(label, str(v), "#E8F5E9","#1B4332","#2E7D32")
        st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # OBSERVACIÓN ECOLÓGICA
    # ══════════════════════════════════════════════════════════════════
    if _show("ecologia"):
        st.markdown(f"### 3. Observación Ecológica &nbsp; {_status_badge('mod_sitio')}", unsafe_allow_html=True)
        area_tot = _safe_float(data.get("proyecto_area") or data.get("proyecto_superficie"))
        area_cult_act = _safe_float(data.get("cultivo_m2"))
        area_cult_fut = _safe_float(data.get("cultivo_m2_futuro"))

        eco_fields = [("suelo_tipo","Tipo de suelo"),("suelo_compactacion","Compactación"),("suelo_materia_organica","Materia orgánica"),
            ("suelo_drenaje","Drenaje"),("suelo_color","Color"),("sol_horas","Horas sol"),("sol_orientacion","Orientación"),
            ("viento_direccion","Viento dominante")]
        c1,c2 = st.columns(2)
        for i,(key,label) in enumerate(eco_fields):
            v = data.get(key)
            if v: 
                with (c1 if i%2==0 else c2): _show_field(label, v)
        veg_tipos = data.get("veg_tipos",[])
        if isinstance(veg_tipos,list) and veg_tipos:
            _show_field("Tipos de vegetación", ", ".join(veg_tipos))
        cultivo_fields = [("cultivo_produce_hoy","Produce hoy"),("cultivo_frutales","Frutales"),("cultivo_verticales","Cultivo vertical")]
        for key,label in cultivo_fields:
            v = data.get(key)
            if v: _show_field(label, v)
        st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # SISTEMAS
    # ══════════════════════════════════════════════════════════════════
    if _show("sistemas"):
        st.markdown(f"### 4. Contexto, Agua, Energía &nbsp; {_status_badge('mod_sistemas')}", unsafe_allow_html=True)
        sys_fields = [("ctx_cuenca","Cuenca/barrio"),("ctx_vecinos","Relación vecinal"),("ctx_participacion","Participación"),
            ("agua_consumo","Consumo agua L/día"),("agua_captacion_lluvia","Captación lluvia"),("agua_grises","Aguas grises"),
            ("agua_riego_sistema","Sistema riego"),("ene_fuente","Fuente energía"),("ene_led","LED"),
            ("ene_kwh_dia_calc","kWh/día estimado"),("ene_solar_interes","Interés solar")]
        c1,c2 = st.columns(2)
        for i,(key,label) in enumerate(sys_fields):
            v = data.get(key)
            if v: 
                with (c1 if i%2==0 else c2): _show_field(label, v)
        st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # FOTOS
    # ══════════════════════════════════════════════════════════════════
    if _show("fotos"):
        st.markdown("### 5. Registro Fotográfico")
        media_count = data.get("media_count", 0)
        if media_count and int(media_count) > 0:
            st.info(f"{media_count} fotografías registradas en el diagnóstico.")
        else:
            st.markdown('<div style="color:#999;font-style:italic;">Sin fotografías registradas.</div>', unsafe_allow_html=True)
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # FLOR DE LA PERMACULTURA
    # ══════════════════════════════════════════════════════════════════
    if _show("flor"):
        st.markdown(f"### 6. Flor de la Permacultura &nbsp; {_status_badge('mod_potencial')}", unsafe_allow_html=True)
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
                    'Los 7 pétalos de Holmgren (2002). El radar muestra ERP (línea sólida) y HRP (línea punteada). Escala 0-10.</div>', unsafe_allow_html=True)

        fig_dual = _dual_radar(domain_obs, domain_tot)
        st.plotly_chart(fig_dual, use_container_width=True, key="radar_flor_dual")

        st.markdown("**Interpretación por pétalo:**")
        for i, p in enumerate(PETAL_ORDER):
            s_o = domain_obs[p]
            s_t = domain_tot[p]
            icon = FLOWER_DOMAINS[p]["icon"]
            interp_e = get_petal_interp(p, s_o, "erp")
            interp_h = get_petal_interp(p, s_t, "hrp")
            with st.expander(f"{icon} {p}", expanded=False):
                col_a, col_p = st.columns(2)
                with col_a:
                    st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;border-left:3px solid #1B4332;">'
                                f'<div style="font-size:0.72rem;font-weight:700;color:#1B4332;">🌍 ERP · {s_o:.0f}/10</div>'
                                f'<div style="font-size:0.85rem;color:#333;">{interp_e}</div></div>', unsafe_allow_html=True)
                    obs_data = data.get(f"petalo_{i}_obs", {})
                    obs_list = [a for v in obs_data.values() if isinstance(v,list) for a in v]
                    obs_list += data.get(f"petalo_{i}_otros_obs", [])
                    if obs_list:
                        st.markdown('<div style="font-size:0.75rem;color:#2D6A4F;margin-top:0.4rem;font-weight:600;">Prácticas observadas:</div>', unsafe_allow_html=True)
                        for a in obs_list:
                            st.markdown(f'<div style="font-size:0.8rem;color:#333;padding:0.1rem 0 0.1rem 0.5rem;">— {a}</div>', unsafe_allow_html=True)
                with col_p:
                    st.markdown(f'<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem;border-left:3px dashed #52B788;">'
                                f'<div style="font-size:0.72rem;font-weight:700;color:#2D6A4F;">🌱 HRP · {s_t:.0f}/10</div>'
                                f'<div style="font-size:0.85rem;color:#333;">{interp_h}</div></div>', unsafe_allow_html=True)
                    new_data = data.get(f"petalo_{i}_pot_new", {})
                    new_list = [a for v in new_data.values() if isinstance(v,list) for a in v]
                    new_list += data.get(f"petalo_{i}_otros_new", [])
                    if new_list:
                        st.markdown('<div style="font-size:0.75rem;color:#52B788;margin-top:0.4rem;font-weight:600;">Prácticas potenciales:</div>', unsafe_allow_html=True)
                        for a in new_list:
                            st.markdown(f'<div style="font-size:0.8rem;color:#333;padding:0.1rem 0 0.1rem 0.5rem;">— {a}</div>', unsafe_allow_html=True)
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # POTENCIALES DEL SITIO
    # ══════════════════════════════════════════════════════════════════
    if _show("potenciales"):
        st.markdown("### 7. Potenciales del Sitio")
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
                    'Diez dimensiones de potencial regenerativo. Los sub-indicadores M2-6 aportan al ERP; el HRP refleja el MFP proyectado.</div>', unsafe_allow_html=True)

        for dim, val_e in potenciales_erp.items():
            val_h = potenciales_hrp.get(dim, 0)
            interp = get_interp_text(dim, val_e, "erp")
            lv, col_lv = _score_to_level(val_e)
            dim_info = DIM_WHAT_MEASURES.get(dim, {})
            icono = dim_info.get("icono","")
            que_mide = dim_info.get("que_mide","")
            st.markdown(
                f'<div style="padding:0.5rem 0;border-bottom:1px solid #E8F5E9;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.15rem;">'
                f'<span style="font-size:0.78rem;font-weight:700;color:#1B4332;">{icono} {dim}</span>'
                f'<span style="font-size:0.72rem;">ERP <span style="background:{col_lv};color:white;border-radius:4px;padding:1px 5px;">{val_e}/10</span>'
                f' → HRP <span style="background:#52B788;color:white;border-radius:4px;padding:1px 5px;">{val_h}/10</span></span></div>'
                + (f'<div style="font-size:0.75rem;color:#2D6A4F;font-style:italic;">{que_mide}</div>' if que_mide else '')
                + (f'<div style="font-size:0.82rem;color:#333;">{interp}</div>' if interp else '')
                + f'</div>', unsafe_allow_html=True)

        # Sub-indicadores with transparency
        if cross:
            st.markdown("**Sub-indicadores M2-6:**")
            for name, info in cross.items():
                s = info["score"]
                lv, cl = _score_to_level(s)
                st.markdown(f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;"><div style="display:flex;justify-content:space-between;font-size:0.78rem;"><span style="color:#1B4332;">{name}</span><span style="background:{cl};color:white;border-radius:4px;padding:1px 5px;font-size:0.7rem;">{s}/10</span></div><div style="font-size:0.7rem;color:#666;">{info["fuente"]}</div></div>', unsafe_allow_html=True)

            with st.expander("🔍 Transparencia: variables y escalas de puntuación", expanded=False):
                for name, detail in CROSS_MODULE_DETAIL.items():
                    actual = cross.get(name,{}).get("score","—")
                    st.markdown(f"**{detail.get('icono','')} {name}** — Puntaje: {actual}/10 · {detail['formula']}")
                    for vn, vs in detail["variables"]:
                        st.markdown(f"- {vn}: {vs}")
                    st.markdown("---")
        st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # SÍNTESIS + PLAN
    # ══════════════════════════════════════════════════════════════════
    if _show("sintesis"):
        st.markdown("### 8. Síntesis y Plan de Acción")
        s_items = [("sint_fortalezas","Fortalezas","#D8F3DC","#1B4332"),("sint_oportunidades","Oportunidades","#E3F2FD","#1565C0"),
                   ("sint_limitaciones","Desafíos","#FFF3E0","#E65100"),("sint_quick_wins","Primeros pasos","#F3E5F5","#6A1B9A")]
        has_s = any(data.get(k) for k,_,_,_ in s_items)
        if has_s:
            c1s,c2s = st.columns(2)
            for i,(key,label,bg,fg) in enumerate(s_items):
                txt = data.get(key,"")
                if txt: 
                    with (c1s if i%2==0 else c2s): _render_sintesis_list(txt, label, bg, fg)

        obs = data.get("sint_observaciones","")
        if obs: _card("Observaciones del facilitador", obs, "#FDF6EC","#333","#A67C00")

        st.markdown("#### Plan de Acción")
        fases = [("plan_inmediatas","Inmediatas (0-3 meses)","#52B788"),("plan_estacionales","Estacionales (3-12 meses)","#2D6A4F"),("plan_estructurales","Estructurales (1-5 años)","#1B4332")]
        cols_p = st.columns(3)
        for i,(key,label,color) in enumerate(fases):
            acciones = data.get(key,[])
            with cols_p[i]:
                header = f'<div style="background:rgba(82,183,136,0.07);border-radius:10px;padding:0.8rem;border-top:3px solid {color};"><div style="font-weight:700;color:{color};margin-bottom:0.6rem;font-size:0.88rem;">{label}</div>'
                if isinstance(acciones, list) and acciones:
                    rows = ""
                    for a in acciones:
                        estado = a.get("estado","") if isinstance(a,dict) else ""
                        titulo = a.get("titulo","") if isinstance(a,dict) else str(a)
                        rows += f'<div style="padding:0.3rem 0;border-bottom:1px solid rgba(82,183,136,0.2);font-size:0.82rem;color:#333;">{estado} {titulo[:100]}</div>'
                    st.markdown(header + rows + "</div>", unsafe_allow_html=True)
                else:
                    st.markdown(header + '<div style="color:#999;font-size:0.82rem;font-style:italic;">Sin acciones</div></div>', unsafe_allow_html=True)
        st.markdown("---")

    # ══════════════════════════════════════════════════════════════════
    # BIBLIOGRAFÍA
    # ══════════════════════════════════════════════════════════════════
    if _show("biblio"):
        st.markdown("### 9. Bibliografía y Recursos")
        from utils.petal_content import GLOBAL_REFS
        REFS_GROUPED = [
            ("Permacultura y diseño regenerativo", [
                ("Holmgren, D. (2002)","Permacultura: Principios y senderos","https://permacultureprinciples.com/es/","Base directa de la Flor de la Permacultura."),
                ("Mollison, B. (1988)","Permaculture: A Designers\' Manual","https://www.permaculturenews.org","Fuente primaria de la permacultura."),
                ("Mason, F. (2025)","Introducción al enfoque de la regeneración","https://doi.org/10.17605/OSF.IO/UCDEH","Marco teórico base de LivLin."),
            ]),
            ("Economía y gobernanza", [
                ("Ostrom, E. (1990)","Governing the Commons","https://wtf.tw/ref/ostrom_1990.pdf","Gestión de recursos comunes."),
                ("Raworth, K. (2017)","Doughnut Economics","https://doughnuteconomics.org","Economía dentro de límites planetarios."),
            ]),
        ]
        for group, refs in REFS_GROUPED:
            with st.expander(f"{group} ({len(refs)} fuentes)", expanded=False):
                for auth, title, url, desc in refs:
                    st.markdown(f'<div style="padding:0.6rem 0;border-bottom:1px solid #E8F5E9;"><div style="font-weight:700;color:#1B4332;font-size:0.83rem;">{auth}</div><div style="font-size:0.82rem;color:#333;font-style:italic;">{title}</div><div style="font-size:0.8rem;color:#555;">{desc}</div><a href="{url}" target="_blank" style="font-size:0.78rem;color:#2D6A4F;">{url}</a></div>', unsafe_allow_html=True)

    # Closing
    if _show("biblio") or active_sec == "all":
        st.markdown(
            '<div style="background:linear-gradient(135deg,#F0FFF4,#D8F3DC);border:1px solid #A8D5B5;border-radius:12px;padding:1.2rem 1.5rem;font-size:0.88rem;color:#1B4332;line-height:1.7;">'
            '<strong>Este diagnóstico es el primer paso de un proceso mayor.</strong><br><br>'
            'Hoy, el espacio muestra un Estado Regenerativo Presente (ERP) que refleja su vitalidad actual. '
            'Al mismo tiempo, identificamos un Horizonte Regenerativo Potencial (HRP) que abre posibilidades de transformación. '
            'La diferencia entre ambos nos señala el camino: cómo pasar de lo que ya tenemos a lo que podemos llegar a ser.<br><br>'
            '<strong><a href="https://www.livlin.cl" target="_blank">www.livlin.cl</a></strong>'
            '</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:0.8rem;background:#F0FFF4;border-radius:8px;padding:0.8rem;font-size:0.82rem;color:#40916C;text-align:center;">'
                    'Los botones de descarga (Excel y Word) están disponibles en el panel lateral izquierdo.</div>', unsafe_allow_html=True)

