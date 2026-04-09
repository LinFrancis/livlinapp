"""Modulo Informe Final — LivLin Indagación Regenerativa.
ERP (Estado Regenerativo Presente) + HRP (Horizonte Regenerativo Potencial).
Sidebar: Logo + Secciones + Descargas + Cerrar sesión.
Visión y Estado Regenerativo: 3 tabs (Perspectiva Comparada, ERP, HRP).
Cada sección con referencias bibliográficas.
Fotos restauradas desde v6.
Ecología y Sistemas exhaustivamente detallados.
Pétalos con explicación profunda (PETAL_DESC).
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
from utils.petal_content import (
    PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS, IPR_OBS_VS_POT,
    LIVLIN_URL, LIVLIN_TAGLINE, LIVLIN_DESC, LIVLIN_MODULES,
    LIVLIN_SERVICES_PITCH, LIVLIN_CLOSING, REGENERATION_FRAMEWORK, GLOBAL_REFS,
    TAO_REFLEXION_SHORT, TAO_INVITACION,
)
from utils.report_generator import generate_excel

MASON_URL = "https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing"

# ── Utility helpers (inline to avoid import chain issues) ────────────
def _safe_float(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default

def _val(data, key, default="No registrado"):
    v = data.get(key)
    if v in [None, "", [], 0, 0.0]: return default
    return v

def _show_field(label, value, empty_msg=""):
    if not value or value in [None, "", [], 0, 0.0, "No registrado"]: return
    st.markdown(
        f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
        f'<span style="font-size:0.75rem;color:#52B788;text-transform:uppercase;">{label}</span><br>'
        f'<span style="font-size:0.88rem;color:#1B4332;">{value}</span></div>',
        unsafe_allow_html=True)

def _card(label, value, bg="#F0FFF4", fg="#1B4332", border="#52B788"):
    if not value or value in [None, "", [], 0, 0.0, "No registrado"]: return
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.6rem 0.8rem;'
        f'margin-bottom:0.5rem;border-left:3px solid {border};">'
        f'<div style="font-size:0.72rem;color:{border};text-transform:uppercase;margin-bottom:0.2rem;">{label}</div>'
        f'<div style="font-size:0.88rem;color:{fg};line-height:1.5;">{value}</div></div>',
        unsafe_allow_html=True)

def _ref_box(refs):
    if not refs: return
    lines = "".join(
        f'<div style="font-size:0.78rem;color:#555;padding:2px 0;">'
        f'📖 {auth} — <em>{title}</em> '
        f'<a href="{url}" target="_blank" style="color:#1565C0;font-size:0.75rem;">↗</a></div>'
        for auth, title, url in refs
    )
    # st.markdown(
    #     f'<div style="background:#FAFAFA;border-radius:8px;padding:0.6rem 0.8rem;margin-top:0.8rem;'
    #     f'border-top:2px solid #D8F3DC;">'
    #     f'<div style="font-size:0.7rem;color:#40916C;font-weight:700;margin-bottom:0.3rem;">📚 Referencias de esta seccion</div>'
    #     f'{lines}</div>', unsafe_allow_html=True)

def _list_from_semicolon(text):
    if not text: return []
    return [item.strip() for item in text.split(";") if item.strip()]

def _render_sintesis_list(items_text, label, bg, fg):
    if not items_text: return
    items = _list_from_semicolon(items_text)
    if not items:
        st.markdown(f'<div style="background:{bg};border-radius:8px;padding:0.7rem;border-left:3px solid {fg};margin-bottom:0.5rem;">'
                    f'<div style="font-size:0.8rem;font-weight:700;color:{fg};">{label}</div>'
                    f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{items_text}</div></div>', unsafe_allow_html=True)
        return
    rows = "".join(f'<div style="padding:0.25rem 0;border-bottom:1px solid rgba(0,0,0,0.06);font-size:0.85rem;color:#333;">{item}</div>' for item in items)
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.7rem;border-left:3px solid {fg};margin-bottom:0.5rem;">'
        f'<div style="font-size:0.8rem;font-weight:700;color:{fg};margin-bottom:0.4rem;">{label}</div>{rows}</div>',
        unsafe_allow_html=True)


# ── Radar charts ─────────────────────────────────────────────────────
def _radar_erp(domain_obs, height=380, title=""):
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_obs = [domain_obs[p] for p in PETAL_ORDER] + [domain_obs[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r_obs, theta=theta, name="ERP — Estado regenerativo presente",
        fill="toself", fillcolor="rgba(27,67,50,0.22)", line=dict(color="#1B4332", width=2.5), marker=dict(size=7, color="#1B4332")))
    fig.update_layout(polar=dict(bgcolor="rgba(240,255,244,0.4)",
        radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10], tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
        angularaxis=dict(tickfont=dict(size=10,color="#1B4332"))),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
        title=dict(text=title, font=dict(size=14, color="#1B4332"), x=0.5) if title else None)
    return fig

def _radar_hrp(domain_tot, height=380, title=""):
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_tot = [domain_tot[p] for p in PETAL_ORDER] + [domain_tot[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r_tot, theta=theta, name="HRP — Horizonte regenerativo potencial",
        fill="toself", fillcolor="rgba(82,183,136,0.15)", line=dict(color="#52B788", width=2, dash="dash")))
    fig.update_layout(polar=dict(bgcolor="rgba(240,255,244,0.4)",
        radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10], tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
        angularaxis=dict(tickfont=dict(size=10,color="#1B4332"))),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
        title=dict(text=title, font=dict(size=14, color="#2D6A4F"), x=0.5) if title else None)
    return fig

def _dual_radar(domain_obs, domain_tot, height=400, title=""):
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_obs = [domain_obs[p] for p in PETAL_ORDER] + [domain_obs[PETAL_ORDER[0]]]
    r_tot = [domain_tot[p] for p in PETAL_ORDER] + [domain_tot[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r_tot, theta=theta, name="HRP · Horizonte regenerativo potencial",
        fill="toself", fillcolor="rgba(82,183,136,0.10)", line=dict(color="#52B788", width=2, dash="dash")))
    fig.add_trace(go.Scatterpolar(r=r_obs, theta=theta, name="ERP · Estado presente",
        fill="toself", fillcolor="rgba(27,67,50,0.22)", line=dict(color="#1B4332", width=2.5), marker=dict(size=7, color="#1B4332")))
    fig.update_layout(polar=dict(bgcolor="rgba(240,255,244,0.4)",
        radialaxis=dict(visible=True, range=[0,10], tickvals=[2,4,6,8,10], tickfont=dict(size=9,color="#2D6A4F"), gridcolor="rgba(45,106,79,0.2)"),
        angularaxis=dict(tickfont=dict(size=10,color="#1B4332"))),
        legend=dict(orientation="h",yanchor="bottom",y=1.05,font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=60,r=60,t=50,b=30), height=height,
        title=dict(text=title, font=dict(size=14, color="#1B4332"), x=0.5) if title else None)
    return fig


def _render_report_map(lat, lon, data, map_key="rpt_map"):
    """Mapa del espacio con selector de vistas y zoom satelital alto."""
    # Tile options
    _tile_options = {
        "🛰️ Satélite (Google)": {
            "tiles": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            "attr": "© Google",
        },
        "🗺️ Híbrido (Satélite + calles)": {
            "tiles": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            "attr": "© Google",
        },
        "📍 OpenStreetMap": {
            "tiles": "OpenStreetMap",
            "attr": "© OpenStreetMap",
        },
        "🌑 CartoDB Dark": {
            "tiles": "CartoDB dark_matter",
            "attr": "© CartoDB",
        },
    }
    sel_tile = st.radio(
        "Vista del mapa",
        list(_tile_options.keys()),
        index=0,  # Satélite por defecto
        horizontal=True,
        key=f"{map_key}_tile",
    )
    tile_cfg = _tile_options[sel_tile]

    try:
        import folium
        from streamlit_folium import st_folium

        if tile_cfg["tiles"] in ("OpenStreetMap", "CartoDB dark_matter", "CartoDB positron"):
            m = folium.Map(location=[lat, lon], zoom_start=19,
                           tiles=tile_cfg["tiles"])
        else:
            m = folium.Map(location=[lat, lon], zoom_start=19,
                           tiles=tile_cfg["tiles"],
                           attr=tile_cfg["attr"])

        # Marker del espacio
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(
                f"<b>{data.get('proyecto_nombre','Espacio')}</b><br>"
                f"Lat: {lat:.6f}  Lon: {lon:.6f}<br>"
                f"{data.get('proyecto_direccion','')}",
                max_width=260),
            tooltip=data.get("proyecto_nombre", "Espacio"),
            icon=folium.Icon(color="green", icon="leaf", prefix="fa")
        ).add_to(m)

        # Lugares cercanos
        nearby_raw = data.get("entorno_lugares_cercanos")
        if nearby_raw:
            try:
                import ast as _a
                places = _a.literal_eval(nearby_raw) if isinstance(nearby_raw, str) else nearby_raw
                color_map = {"parques": "green", "ferias": "orange", "mercados": "blue",
                             "bibliotecas": "purple", "escuelas": "red", "huertas": "darkgreen"}
                for p in (places or [])[:12]:
                    c = "gray"
                    for k, v in color_map.items():
                        if k in p.get("categoria", "").lower():
                            c = v; break
                    folium.CircleMarker(
                        [p["lat"], p["lon"]], radius=8,
                        color=c, fill=True, fill_color=c, fill_opacity=0.7,
                        popup=folium.Popup(f"<b>{p['name']}</b><br>{p.get('categoria','')}<br>{p.get('dist_m',0)} m", max_width=180),
                        tooltip=f"{p['name']} ({p.get('dist_m',0)}m)"
                    ).add_to(m)
            except:
                pass

        st_folium(m, width="100%", height=480, returned_objects=[], key=map_key)

    except ImportError:
        import pandas as pd
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=18)
        st.caption("Para mapa interactivo completo instala: pip install folium streamlit-folium")


# ── Stacked bar chart helper ─────────────────────────────────────────
def _stacked_bar(names, erp_vals, gap_vals, title="", height=420):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="ERP (estado regenerativo presente)", y=names, x=erp_vals, orientation="h",
        marker_color="#1B4332", text=[f"{v:.0f}" for v in erp_vals], textposition="inside",
        textfont=dict(color="white", size=11)))
    fig.add_trace(go.Bar(name="Brecha → HRP", y=names, x=gap_vals, orientation="h",
        marker_color="rgba(255,167,38,0.45)", text=[f"+{v:.0f}" if v>0 else "" for v in gap_vals],
        textposition="inside", textfont=dict(color="#E65100", size=10)))
    fig.update_layout(barmode="stack", xaxis=dict(title="Puntuación (0-10)", range=[0,10.5]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
        height=height, margin=dict(l=180, r=20, t=30, b=30), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,255,248,0.4)", title=title if title else None)
    return fig


# ── Section registry ────────────────────────────────────────────────
# Orden: Resultados generales → Síntesis/Plan → Descriptivos → Referencias
REPORT_SECTIONS = {
    # ── RESULTADOS ─────────────────────────────────────────────────
    "vision":           ("🌸 Potencial Regenerativo",      "mod_potencial"),
    "sintesis":         ("🗺️ Síntesis y Plan de Acción",   "mod_plan"),
    # ── DESCRIPTIVOS DEL ESPACIO ───────────────────────────────────
    "datos":            ("📋 Datos del Proyecto",           "mod_cliente"),
    "registro":         ("📍 Lectura del Lugar",            "mod_sitio"),
    "tao":              ("🌀 Tao Vida Regenerativa",        "mod_tao"),
    "eco_conciencia":   ("🌍 Conciencia Ecológica",         "mod_eco"),
    "analisis_sectores":("🗂️ Análisis de Sectores",         "mod_sistemas"),
    "fotos":            ("📷 Registro Fotográfico",         "mod_fotos"),
    # ── REFERENCIAS ────────────────────────────────────────────────
    "metodologia":      ("📐 Metodología",                  None),
    "glosario":         ("📚 Glosario de Acciones",         None),
    "biblio":           ("🔗 Recursos",                     None),
}



# ══════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════
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

    # Check if a module is addressed
    def _is_addressed(mod_key):
        if not mod_key: return True
        if isinstance(mod_key, list):
            return any(data.get(k, "respondido") != "no_abordado" for k in mod_key)
        return data.get(mod_key, "respondido") != "no_abordado"

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

    # ── Sidebar for client view ──────────────────────────────────────
    if "report_section" not in st.session_state:
        st.session_state.report_section = "all"

    if readonly:
        with st.sidebar:
            # ═══ A) LOGO (use st.image like admin — handles transparency) ═══
            from pathlib import Path as _P
            _logo_path = _P(__file__).parent.parent / "assets" / "logolivlin.png"
            if _logo_path.exists():
                st.image(str(_logo_path), use_container_width=True)
            st.markdown(
                '<div style="text-align:center;padding:0.1rem 0 0.5rem;">'
                '<div style="font-size:0.9rem;font-weight:800;color:#1B4332;">LivLin</div>'
                '<div style="font-size:0.65rem;color:#40916C;font-style:italic;">Indagación Regenerativa</div>'
                '</div>', unsafe_allow_html=True)

            # Nombre del diagnóstico
            st.markdown(
                f'<div style="background:linear-gradient(135deg,rgba(82,183,136,0.12),rgba(45,106,79,0.08));'
                f'border-radius:10px;padding:0.5rem 0.7rem;margin-bottom:0.5rem;border:1px solid #A8D5B5;">'
                f'<div style="font-size:0.58rem;color:#40916C;text-transform:uppercase;letter-spacing:0.08em;">Espacio diagnosticado</div>'
                f'<div style="font-weight:700;font-size:0.85rem;color:#1B4332;">{nombre}</div>'
                f'<div style="font-size:0.68rem;color:#2D6A4F;">{cliente} · {ciudad}</div></div>',
                unsafe_allow_html=True)
            st.markdown("---")

            # ═══ B) SECCIONES DEL INFORME ═══
            st.markdown('<div style="font-size:0.72rem;color:#1B4332;font-weight:700;margin-bottom:0.4rem;">SECCIONES DEL INFORME</div>', unsafe_allow_html=True)
            if st.button("📖 Ver informe completo", use_container_width=True, key="rpt_nav_all",
                         type="primary" if st.session_state.report_section == "all" else "secondary"):
                st.session_state.report_section = "all"; st.rerun()

            # Group labels for visual separation
            _group_headers = {
                "vision":           ("🎯 RESULTADOS",              "#1B4332"),
                "datos":            ("📂 DESCRIPTIVOS DEL ESPACIO","#0D47A1"),
                "metodologia":      ("📌 REFERENCIAS",             "#4A148C"),
            }
            for sec_key, (sec_label, mod_key) in REPORT_SECTIONS.items():
                if not _is_addressed(mod_key):
                    continue
                # Print group header if this key starts a group
                if sec_key in _group_headers:
                    gh_label, gh_color = _group_headers[sec_key]
                    st.markdown(
                        f'<div style="font-size:0.66rem;color:{gh_color};font-weight:700;'
                        f'margin:0.5rem 0 0.2rem;letter-spacing:0.05em;">{gh_label}</div>',
                        unsafe_allow_html=True)
                active = st.session_state.report_section == sec_key
                if st.button(sec_label, use_container_width=True, key=f"rpt_nav_{sec_key}",
                             type="primary" if active else "secondary"):
                    st.session_state.report_section = sec_key; st.rerun()

            st.markdown("---")

            # ═══ C) DESCARGAR INFORME ═══
            _is_demo = st.session_state.get("demo_mode", False)

            # Demo mode: profile switcher
            if _is_demo:
                st.markdown(
                    '<div style="background:#FFF3E0;border-radius:8px;padding:0.5rem;margin-bottom:0.5rem;'
                    'text-align:center;border:1px solid #FFB74D;">'
                    '<div style="font-size:0.7rem;font-weight:700;color:#E65100;">MODO DEMOSTRACION</div>'
                    '<div style="font-size:0.65rem;color:#BF360C;">Este informe es un ejemplo ficticio</div>'
                    '</div>', unsafe_allow_html=True)
                try:
                    from utils.demo_profiles import list_demo_profiles, get_demo_profile
                    profiles = list_demo_profiles()
                    current_id = data.get("id", "")
                    opciones = [f"{n}" for _, n, _, _, _ in profiles]
                    current_idx = 0
                    for j, (pid, *_) in enumerate(profiles):
                        if pid == current_id:
                            current_idx = j
                            break
                    sel_demo = st.selectbox("Cambiar perfil demo", opciones, index=current_idx, key="demo_switch")
                    sel_idx = opciones.index(sel_demo)
                    sel_pid = profiles[sel_idx][0]
                    if sel_pid != current_id:
                        new_profile = get_demo_profile(sel_pid)
                        if new_profile:
                            st.session_state.visit_data = new_profile
                            st.session_state.current_user["space_name"] = new_profile.get("proyecto_nombre", "Demo")
                            st.session_state.current_user["display_name"] = new_profile.get("proyecto_cliente", "Demo")
                            st.rerun()
                except Exception:
                    pass
                st.markdown("---")

            if not _is_demo:
                st.markdown('<div style="font-size:0.72rem;color:#1B4332;font-weight:700;margin-bottom:0.4rem;">💾 DESCARGAR INFORME</div>', unsafe_allow_html=True)
                safe_n = nombre.replace(" ", "_")
                try:
                    xlsx_bytes = generate_excel(data)
                    st.download_button("📊 Descargar Excel", data=xlsx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True, key="rpt_dl_xlsx")
                except Exception as e:
                    st.caption(f"Excel no disponible: {e}")
                try:
                    from utils.docx_generator import generate_docx
                    docx_bytes = generate_docx(data)
                    st.download_button("📝 Descargar Word", data=docx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True, key="rpt_dl_docx")
                except Exception as e:
                    st.caption(f"Word no disponible: {e}")
                st.markdown("---")

            # ═══ D) CERRAR SESIÓN / SALIR DEMO ═══
            if _is_demo:
                st.markdown(
                    '<div style="text-align:center;margin:0.5rem 0;">'
                    '<a href="https://www.livlin.cl" target="_blank" style="font-size:0.78rem;'
                    'color:#1B4332;font-weight:700;text-decoration:none;">Contacta a LivLin →</a></div>',
                    unsafe_allow_html=True)
                if st.button("Salir del modo demo", use_container_width=True, key="rpt_logout"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()
            else:
                st.markdown('<div style="font-size:0.72rem;color:#1B4332;font-weight:700;margin-bottom:0.4rem;">🔒 SESION</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.7rem;color:#555;margin-bottom:0.3rem;">👤 {data.get("proyecto_cliente","Usuario")}</div>', unsafe_allow_html=True)
                if st.button("Cerrar sesion", use_container_width=True, key="rpt_logout"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()

    active_sec = st.session_state.get("report_section", "all")
    def _show(sec_key):
        # Must be either "all" or the selected section
        if not (active_sec == "all" or active_sec == sec_key):
            return False
        # MUST also be addressed
        mod_key = REPORT_SECTIONS.get(sec_key, (None, None))[1]
        return _is_addressed(mod_key)

    # ── Header ────────────────────────────────────────────────────────
    st.markdown("## Informe de la Indagación Regenerativa")
    st.markdown('<p class="module-subtitle">Resultados claves para el diseño de ecosistemas regenerativos</p>', unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN 1 — VISIÓN Y ESTADO REGENERATIVO (3 TABS)
    # ══════════════════════════════════════════════════════════════════
    if _show("vision"):
        st.markdown(f"#### Potencial regenerativo &nbsp; {_status_badge('mod_potencial')}", unsafe_allow_html=True)

        # ── Guidance Expander (solo en sección Potencial Regenerativo) ────────
        with st.expander("📖 ¿Cómo leer estos resultados? (clic para aprender más)", expanded=False):
            if readonly and st.session_state.get("demo_mode", False):
                st.markdown(
                    '<div style="background:linear-gradient(135deg,#FFF3E0,#FFE0B2);border-radius:12px;'
                    'padding:0.8rem 1.2rem;margin-bottom:0.8rem;border:1px solid #FFB74D;">'
                    '<div style="font-size:0.85rem;font-weight:700;color:#E65100;margin-bottom:0.3rem;">'
                    'Modo Demostración</div>'
                    '<div style="font-size:0.82rem;color:#BF360C;line-height:1.6;">'
                    f'Este es un informe de ejemplo para <strong>{nombre}</strong>. '
                    'Los datos son ficticios. '
                    'Esta es la vista de resultados para quienes contratan el servicio de indagación regenerativa para el diseño de ecosistemas regenerativos en Livlin.'
                    '</div></div>', unsafe_allow_html=True)

            st.markdown(
                f'<div style="background:linear-gradient(135deg,#F0FFF4,#E8F5E9);border:2px solid #52B788;border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">'
                f'<div style="font-size:1.1rem;font-weight:800;color:#1B4332;margin-bottom:0.5rem;">¿Qué significa regenerar un espacio?</div>'
                f'<div style="font-size:0.9rem;color:#2D6A4F;line-height:1.8;margin-bottom:1.2rem;">'
                f'Este informe es el resultado de una <strong>Indagación Regenerativa</strong> de LivLin para <strong>{nombre}</strong>. '
                f'En LivLin, regenerar es volver a lo esencial de lo esencial. <em>Cuando el planeta enferma, regenerar es mejorar la salud y celebrar la vida</em>.<br><br>'
                'Regenerar es activar los procesos vivos que permiten a un espacio evolucionar hacia mayor vitalidad, biodiversidad y conexión.'
                'Aquí encontrarás un análisis detallado basado en dos indicadores complementarios:'
                '</div>'
                '<div style="display:flex;flex-wrap:wrap;gap:0.8rem;margin-bottom:0.8rem;">'
                '  <div style="flex:1;min-width:260px;background:white;border-radius:10px;padding:1rem;border-left:4px solid #1B4332;">'
                '    <div style="font-weight:800;color:#1B4332;font-size:0.9rem;">🌍 ERP — Estado Regenerativo Presente</div>'
                '    <div style="font-size:0.82rem;color:#333;line-height:1.6;margin-top:0.4rem;">'
                '      Es la <strong>fotografía actual</strong>: las prácticas y ciclos que ya están activos. '
                '      Se calcula sumando la <strong>Flor de la Permacultura</strong> (observada) + indicadores de <strong>análisis de sectores</strong>.'
                '    </div>'
                '  </div>'
                '  <div style="flex:1;min-width:260px;background:white;border-radius:10px;padding:1rem;border-left:4px solid #52B788;">'
                '    <div style="font-weight:800;color:#2D6A4F;font-size:0.9rem;">🌱 HRP — Horizonte Regenerativo Potencial</div>'
                '    <div style="font-size:0.82rem;color:#333;line-height:1.6;margin-top:0.4rem;">'
                '      Es la <strong>proyección a futuro</strong>: lo que tu espacio puede llegar a ser si se activan todas las prácticas '
                '      potenciales identificadas. Es el techo máximo de regeneración del lugar.'
                '    </div>'
                '  </div>'
                '</div>'
                '<div style="background:rgba(255,167,38,0.08);border-radius:10px;padding:0.8rem 1rem;border:1px dashed #FFA726;">'
                '  <div style="font-weight:800;color:#E65100;font-size:0.9rem;">🌀 Brecha = HRP − ERP → Tu Campo de Acción</div>'
                '  <div style="font-size:0.82rem;color:#5D4037;line-height:1.6;margin-top:0.4rem;">'
                '    Indica exactamente <em>cuánto potencial hay por activar</em>. Una brecha grande significa que hay mucho espacio para crecer. '
                '    Una brecha pequeña indica que estás cerca de tu máximo potencial identificado.'
                '  </div>'
                '</div>'
                '<div style="margin-top:1rem;font-size:0.82rem;color:#555;text-align:center;">'
                'Navega las secciones usando el menú lateral para profundizar en cada aspecto.'
                '</div>'
                '</div>', unsafe_allow_html=True)

            st.markdown(
                f'<div style="text-align:center;margin-top:0.5rem;">'
                f'<a href="{MASON_URL}" target="_blank" style="display:inline-block;background:#1B4332;color:white;border-radius:8px;padding:0.5rem 1rem;font-weight:700;font-size:0.85rem;text-decoration:none;">📄 Leer Introducción al Enfoque de la Regeneración · Mason (2025)</a>'
                f'</div>', unsafe_allow_html=True)


        # # ── Tarjetas de resultado ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#F0FFF4,#D8F3DC);border:2px solid #52B788;border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                <div>
                    <div style="font-size:1rem;color:#52B788;text-transform:uppercase;">Resultados</div>
                    <div style="font-size:1.5rem;font-weight:800;color:#1B4332;margin:0.2rem 0;">{nombre}</div>
                    <div style="color:#555;font-size:0.88rem;">{cliente} · {ciudad} · {fecha}</div>
                </div>
                <div style="display:flex;gap:0.8rem;flex-wrap:wrap;">
                    <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px solid #D8F3DC;min-width:120px;">
                        <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌍 Estado Regenerativo Presente (ERP) </div>
                        <div style="font-size:2.8rem;font-weight:900;color:#1B4332;line-height:1;">{erp_score}</div>
                        <div style="color:#52B788;font-size:0.75rem;">/10</div>
                        <div style="font-size:0.72rem;color:{color_erp};font-weight:600;">{label_erp}</div>
                    </div>
                    <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px dashed #52B788;min-width:120px;">
                        <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌱 Horizonte Regenerativo Potencial (HRP)</div>
                        <div style="font-size:2.8rem;font-weight:900;color:#52B788;line-height:1;">{hrp_score}</div>
                        <div style="color:#52B788;font-size:0.75rem;">/10</div>
                        <div style="font-size:0.72rem;color:{color_hrp};font-weight:600;">{label_hrp}</div>
                    </div>
                    <div style="text-align:center;background:white;border-radius:12px;padding:0.8rem 1.2rem;border:2px solid #FFA726;min-width:120px;">
                        <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">🌀 Brecha</div>
                        <div style="font-size:2.8rem;font-weight:900;color:#FFA726;line-height:1;">{brecha}</div>
                        <div style="color:#FFA726;font-size:0.75rem;">pts</div>
                        <div style="font-size:0.72rem;color:#E65100;font-weight:600;">Campo de acción</div>
                    </div>
                </div>
            </div>
            <div style="margin-top:0.8rem;padding:0.7rem;background:rgba(255,167,38,0.08);border-radius:8px;">
                <div style="font-size:0.88rem;color:#E65100;font-weight:700;margin-bottom:0.3rem;">¿Qué significa esta brecha para tu espacio?</div>
                <div style="font-size:0.85rem;color:#5D4037;line-height:1.6;">🌀 {brecha_txt}</div>
            </div>
        </div>""", unsafe_allow_html=True)

          # ── Motivacional ──
        # st.markdown(
        #     f'<div style="background:linear-gradient(135deg,#E8F5E9,#D8F3DC);border-radius:12px;padding:1rem;margin-top:1rem;text-align:center;">'
        #     f'<div style="font-size:1rem;font-weight:800;color:#1B4332;">🌿 Tu espacio tiene un camino claro hacia la regeneración</div>'
        #     f'<div style="font-size:0.88rem;color:#2D6A4F;margin-top:0.4rem;line-height:1.6;">'
        #     f'Con un ERP de <strong>{erp_score}/10</strong> y un HRP de <strong>{hrp_score}/10</strong>, '
        #     f'hay <strong>{brecha} puntos de potencial por activar</strong>. '
        #     f'Cada práctica nueva que incorpores acerca tu espacio a su máximo potencial regenerativo. '
        #     f'LivLin te acompaña en este camino. 🌱</div>'
        #     f'</div>', unsafe_allow_html=True)

        

        # ── 3 TABS ────────────────────────────────────────────────────
        tab_comp, tab_erp, tab_hrp = st.tabs(["📊 Perspectiva Comparada", "🌍 ERP — Estado Presente", "🌱 HRP — Horizonte Potencial"])

        # ── TAB: Perspectiva Comparada (contains ALL info) ────────────
        with tab_comp:
            st.markdown("#### 📊 Perspectiva Comparada — Visión Integral")

            # ── Dual radar ──
            st.markdown("##### 🕸️ Radar — Flor de la Permacultura")
            st.markdown(
                '<div style="background:#F0FFF4;border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.5rem;font-size:0.84rem;color:#2D6A4F;line-height:1.6;">'
                'La <strong>Flor de la Permacultura</strong> (Holmgren, 2002) organiza la vida cotidiana en '
                '<strong>7 pétalos o dominios de acción</strong>. Cada eje del radar representa un pétalo. '
                'El área verde sólida es el <strong>ERP</strong> (lo que ya existe); la línea verde discontinua es el <strong>HRP</strong> '
                '(lo que puede llegar a ser). La diferencia entre ambas áreas es tu <strong>campo de acción</strong>.</div>', unsafe_allow_html=True)
            st.plotly_chart(_dual_radar(domain_obs, domain_tot, title="Flor de la Permacultura — ERP vs HRP"), use_container_width=True, key="r_comp_dual")

            # # ── Barras 7 pétalos ──
            # petal_names = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
            # p_erp = [domain_obs[p] for p in PETAL_ORDER]
            # p_gap = [max(0, round(domain_tot[p] - domain_obs[p], 1)) for p in PETAL_ORDER]
            # st.plotly_chart(_stacked_bar(petal_names, p_erp, p_gap, title="7 Pétalos — ERP + Brecha → HRP", height=350), use_container_width=True, key="bar_comp_pet")

            # ── Detalle pétalo a pétalo con definición + prácticas ──
            st.markdown("---")
            st.markdown("##### 🌸 Detalle por Pétalo — Definición, Estado y Potencial")
            st.markdown(
                '<div style="background:#F0FFF4;border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.8rem;font-size:0.84rem;color:#2D6A4F;line-height:1.6;">'
                'Cada pétalo representa un ámbito de la vida cotidiana donde las prácticas regenerativas '
                'pueden transformar el espacio. A continuación se presenta cada pétalo con su <strong>definición</strong>, '
                'su <strong>puntuación ERP y HRP</strong>, y las <strong>prácticas observadas y potenciales</strong>. '
                'Los pétalos con mayor brecha representan las mayores oportunidades de transformación.</div>', unsafe_allow_html=True)

            # Load petals data
            import json
            from pathlib import Path as _Path
            try:
                _jf = _Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
                with open(_jf, encoding="utf-8") as _f:
                    _petalos_data = json.load(_f)["petalos"]
            except Exception:
                _petalos_data = []

            for i, p_name in enumerate(PETAL_ORDER):
                icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
                e_score = domain_obs.get(p_name, 0)
                h_score = domain_tot.get(p_name, 0)
                lv_e, _ = _score_to_level(e_score)
                lv_h, _ = _score_to_level(h_score)
                gap = round(h_score - e_score, 1)
                petal_info = PETAL_DESC.get(p_name, {})
                interp_e = get_petal_interp(p_name, e_score, "erp")
                interp_h = get_petal_interp(p_name, h_score, "hrp")
                obs_data = data.get(f"petalo_{i}_obs", {})
                new_data = data.get(f"petalo_{i}_pot_new", {})
                otros_obs = data.get(f"petalo_{i}_otros_obs", [])
                otros_new = data.get(f"petalo_{i}_otros_new", [])

                # ── Encabezado del pétalo ──────────────────────────
                subtitulo = petal_info.get("subtitulo", "") if petal_info else ""
                resumen   = petal_info.get("resumen", "")   if petal_info else ""
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#F0FFF4,#E8F5E9);border:2px solid #52B788;
                            border-radius:14px;padding:1rem 1.2rem;margin:1.2rem 0 0;
                            box-shadow:0 2px 6px rgba(40,120,80,0.07);">
                  <div style="font-size:1rem;font-weight:800;color:#1B4332;margin-bottom:0.3rem;">
                    {icon} {p_name}
                  </div>
                  {f'<div style="font-size:0.82rem;color:#40916C;margin-bottom:0.5rem;font-style:italic;">{subtitulo}</div>' if subtitulo else ''}
                  <div style="display:flex;gap:0.6rem;flex-wrap:wrap;margin-bottom:{'0.6rem' if resumen else '0'};">
                    <span style="background:white;border-radius:20px;padding:0.25rem 0.7rem;
                                 border:1px solid #D8F3DC;font-size:0.8rem;color:#1B4332;">
                      🌍 ERP <strong>{e_score:.0f}/10</strong> — {lv_e}</span>
                    <span style="background:white;border-radius:20px;padding:0.25rem 0.7rem;
                                 border:1px dashed #52B788;font-size:0.8rem;color:#2D6A4F;">
                      🌱 HRP <strong>{h_score:.0f}/10</strong> — {lv_h}</span>
                    <span style="background:#FFF8E1;border-radius:20px;padding:0.25rem 0.7rem;
                                 border:1px solid #FFD54F;font-size:0.8rem;color:#E65100;">
                      🌀 Brecha <strong>+{gap:.0f} pts</strong></span>
                  </div>
                  {f'<div style="font-size:0.84rem;color:#2D6A4F;line-height:1.65;border-top:1px solid #D8F3DC;padding-top:0.5rem;">{resumen}</div>' if resumen else ''}
                </div>""", unsafe_allow_html=True)

             
                # ── Prácticas activas + potencial en columnas ──────
                obs_items = [(k.replace("_"," ").title(), v) for k, v in obs_data.items() if v]
                if otros_obs: obs_items.append(("Otras prácticas", otros_obs))
                new_items = [(k.replace("_"," ").title(), v) for k, v in new_data.items() if v]
                if otros_new: new_items.append(("Otras oportunidades", otros_new))

                if obs_items or new_items:
                    st.markdown(
                        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin:0.8rem 0;">',
                        unsafe_allow_html=True)
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown(
                            '<div style="font-size:0.78rem;font-weight:700;color:#1B4332;'                            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;'                            'padding-bottom:0.2rem;border-bottom:2px solid #52B788;">✅ Lo que ya está activo</div>',
                            unsafe_allow_html=True)
                        if obs_items:
                            for cat, items in obs_items:
                                items_str = " · ".join(items) if isinstance(items, list) else str(items)
                                st.markdown(
                                    f'<div style="background:#F0FFF4;border-radius:8px;padding:0.45rem 0.7rem;'                                    f'margin-bottom:0.35rem;border-left:3px solid #52B788;">'                                    f'<div style="font-size:0.72rem;color:#40916C;text-transform:uppercase;'                                    f'font-weight:700;margin-bottom:0.15rem;">{cat}</div>'                                    f'<div style="font-size:0.84rem;color:#1B4332;">{items_str}</div></div>',
                                    unsafe_allow_html=True)
                        else:
                            st.markdown(
                                '<div style="font-size:0.82rem;color:#888;padding:0.5rem 0;font-style:italic;">'                                'Aún no hay prácticas activas registradas.</div>', unsafe_allow_html=True)
                    with pc2:
                        st.markdown(
                            '<div style="font-size:0.78rem;font-weight:700;color:#E65100;'                            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;'                            'padding-bottom:0.2rem;border-bottom:2px solid #FFA726;">🌱 Potencial identificado</div>',
                            unsafe_allow_html=True)
                        if new_items:
                            for cat, items in new_items:
                                items_str = " · ".join(items) if isinstance(items, list) else str(items)
                                st.markdown(
                                    f'<div style="background:#FFFDE7;border-radius:8px;padding:0.45rem 0.7rem;'                                    f'margin-bottom:0.35rem;border-left:3px solid #FFA726;">'                                    f'<div style="font-size:0.72rem;color:#E65100;text-transform:uppercase;'                                    f'font-weight:700;margin-bottom:0.15rem;">{cat}</div>'                                    f'<div style="font-size:0.84rem;color:#5D4037;">{items_str}</div></div>',
                                    unsafe_allow_html=True)
                        else:
                            st.markdown(
                                '<div style="font-size:0.82rem;color:#888;padding:0.5rem 0;font-style:italic;">'                                'Sin acciones potenciales identificadas.</div>', unsafe_allow_html=True)

                # ── Detalle ampliado (expander compacto al pie) ────
                if petal_info and (petal_info.get("detalle") or petal_info.get("holmgren_name")):
                    with st.expander(f"📖 Profundizar en «{p_name}»", expanded=False):
                        if petal_info.get("holmgren_name"):
                            st.markdown(f"**Nombre original (Holmgren, 2002):** *{petal_info['holmgren_name']}*")
                        if petal_info.get("detalle"):
                            st.markdown(petal_info["detalle"])
                        petal_refs = petal_info.get("referencias", [])
                        if petal_refs:
                            _ref_box(petal_refs)

                st.markdown("<hr style='border:none;border-top:1px solid #E8F5E9;margin:0.3rem 0 0;'>",
                            unsafe_allow_html=True)

            # ── Sub-indicadores M2-6 ──
            if cross:
                
                with st.expander("📈 Sub-indicadores ecológicos M2-6 (aportan 20% al ERP)", expanded=False):
                    st.markdown(
                        '<div style="font-size:0.84rem;color:#2D6A4F;margin-bottom:0.5rem;">'
                        'Estos indicadores provienen de los módulos de observación ecológica (🔬 M2-3) y sistemas (🏙️ M4-6). '
                        'Complementan la Flor de la Permacultura con datos concretos del sitio.</div>', unsafe_allow_html=True)
                    for name, info in cross.items():
                        st.markdown(f"**{info.get('icono','')} {name}:** {info['score']}/10 — _{info['fuente']}_")
                    st.markdown("---")
                    st.markdown("**Transparencia: variables y escalas**")
                    for name, detail in CROSS_MODULE_DETAIL.items():
                        st.markdown(f"**{detail.get('icono','')} {name}:** `{detail['formula']}`")
                        for vn, vs in detail["variables"]:
                            st.caption(f"  • {vn}: {vs}")

           
          

        # ── TAB: ERP ──────────────────────────────────────────────────
        with tab_erp:
            st.markdown("#### 🌍 ERP — Estado Regenerativo Presente")
            st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.88rem;color:#2D6A4F;line-height:1.6;">'
                f'<strong>Definición:</strong> El ERP es la fotografía del momento actual. Refleja lo que ya existe: las prácticas activas, los ciclos en marcha, '
                f'las relaciones entre elementos del espacio. Se compone de <strong>80% del MFP observado</strong> '
                f'+ <strong>20% de sub-indicadores M2-M6</strong>.'
                f'<br><br>📖 <em>Para el detalle completo con barras apiladas, sub-indicadores y metodología, consulta la pestaña "📊 Perspectiva Comparada".</em></div>', unsafe_allow_html=True)
            st.plotly_chart(_radar_erp(domain_obs, title="Radar ERP — Estado Presente"), use_container_width=True, key="r_erp_solo")
            # Petal detail for ERP
            for i, p in enumerate(PETAL_ORDER):
                e = domain_obs[p]; lv, _ = _score_to_level(e)
                interp_e = get_petal_interp(p, e, "erp")
                st.markdown(f"**{FLOWER_DOMAINS[p]['icon']} {p}:** {e:.0f}/10 — {lv}")
                if interp_e:
                    st.markdown(f'<div style="background:#E8F5E9;border-radius:6px;padding:0.4rem 0.6rem;margin:0.2rem 0 0.5rem;font-size:0.82rem;color:#1B4332;border-left:3px solid #1B4332;">{interp_e}</div>', unsafe_allow_html=True)
            _ref_box([("Mason, F. (2025)", "Introducción al enfoque de la regeneración", MASON_URL)])

        # ── TAB: HRP ──────────────────────────────────────────────────
        with tab_hrp:
            st.markdown("#### 🌱 HRP — Horizonte Regenerativo Potencial")
            st.markdown(f'<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.88rem;color:#5D4037;line-height:1.6;">'
                f'<strong>Definición:</strong> El HRP proyecta lo que el espacio puede llegar a ser si se activan las prácticas potenciales identificadas. '
                f'Se compone de <strong>100% del MFP proyectado</strong> (observado + potencial). '
                f'No incluye sub-indicadores M2-6 porque la visión futura ya está contenida en las prácticas potenciales de cada pétalo.'
                f'<br><br>📖 <em>Ver la pestaña "📊 Perspectiva Comparada" para el detalle de prácticas por pétalo y "🗺️ Síntesis y Plan" para la hoja de ruta.</em></div>', unsafe_allow_html=True)
            st.plotly_chart(_radar_hrp(domain_tot, title="Radar HRP — Horizonte Potencial"), use_container_width=True, key="r_hrp_solo")
            for i, p in enumerate(PETAL_ORDER):
                h = domain_tot[p]; lv, _ = _score_to_level(h)
                interp_h = get_petal_interp(p, h, "hrp")
                st.markdown(f"**{FLOWER_DOMAINS[p]['icon']} {p}:** {h:.0f}/10 — {lv}")
                if interp_h:
                    st.markdown(f'<div style="background:#FFFDE7;border-radius:6px;padding:0.4rem 0.6rem;margin:0.2rem 0 0.5rem;font-size:0.82rem;color:#5D4037;border-left:3px solid #FFA726;">{interp_h}</div>', unsafe_allow_html=True)
            _ref_box([("Mason, F. (2025)", "Introducción al enfoque de la regeneración", MASON_URL)])



    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN 2 — SÍNTESIS Y PLAN (va justo después de Potencial Regenerativo)
    # ══════════════════════════════════════════════════════════════════
    if _show("sintesis"):
        st.markdown(f"### 🗺️ Síntesis y Planificación &nbsp; {_status_badge('mod_plan')}", unsafe_allow_html=True)
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
            'Integración de los hallazgos del diagnóstico en fortalezas, oportunidades, desafíos y '
            'un plan de acción en 3 horizontes temporales (Mason, 2025).</div>', unsafe_allow_html=True)

        st.markdown("#### 🔍 Síntesis del Diagnóstico")
        st.caption("Resumen integrado de hallazgos del diagnóstico regenerativo.")

        for key, lbl, bg, fg in [("sint_fortalezas","💚 Fortalezas","#E8F5E9","#2E7D32"),
                                  ("sint_oportunidades","🌱 Oportunidades","#F0FFF4","#40916C"),
                                  ("sint_limitaciones","⚡ Desafíos","#FFF3E0","#E65100")]:
            _render_sintesis_list(data.get(key,""), lbl, bg, fg)

        st.markdown("---")
        st.markdown("#### 🗺️ Plan de Acción — Hoja de Ruta en 3 Horizontes")
        st.caption("Intervenciones ordenadas por horizonte temporal, del corto al largo plazo (Mason, 2025).")

        fases = [("plan_inmediatas","⚡ Fase 1 (0-3 meses)","Acciones inmediatas de bajo costo.","#52B788"),
                 ("plan_estacionales","🌱 Fase 2 (3-12 meses)","Intervenciones estacionales.","#2D6A4F"),
                 ("plan_estructurales","🌳 Fase 3 (1-5 años)","Transformaciones estructurales.","#1B4332")]
        st.markdown("")
        for pk, fase, desc, color in fases:
            st.markdown(f"##### {fase}")
            st.caption(desc)
            v = data.get(pk, "")
            if v:
                if isinstance(v, list):
                    for item in v:
                        txt = item.get("titulo","") if isinstance(item, dict) else str(item)
                        if txt: st.markdown(f"→ {txt}")
                else:
                    st.markdown(str(v))

        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN 3 — DATOS DEL PROYECTO (descriptivos)
    # ══════════════════════════════════════════════════════════════════
    if _show("datos"):
        st.markdown(f"#### 📋 Información General del Espacio &nbsp; {_status_badge('mod_cliente')}", unsafe_allow_html=True)
        for lbl, key in [("Nombre del espacio","proyecto_nombre"),("Contacto","proyecto_cliente"),
                         ("Ciudad","proyecto_ciudad"),("Dirección","proyecto_direccion"),
                         ("Fecha","proyecto_fecha"),("Tipo de espacio","proyecto_tipo_espacio"),
                         ("Superficie (m²)","proyecto_superficie"),("Habitantes","proyecto_habitantes"),
                         ("Mascotas y animales","proyecto_mascotas")]:
            v = data.get(key)
            if v: _card(lbl, str(v))
        for k, lbl in [("intencion_motivo","Motivo del diagnóstico"),("intencion_vision5","Visión a 5 años"),
                       ("intencion_suenos","Sueños regenerativos")]:
            v = data.get(k)
            if v: _card(lbl, str(v), bg="#E8F5E9", border="#2D6A4F")
        # (El mapa se muestra en Lectura del Lugar)

    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN 2b — LECTURA DEL LUGAR (M2-3)
    # ══════════════════════════════════════════════════════════════════
    if _show("registro"):
        st.markdown(f"#### 🌍 Lectura del Lugar (M2-3) &nbsp; {_status_badge('mod_sitio')}", unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:1rem;'
            'font-size:0.85rem;color:#2D6A4F;line-height:1.7;">'
            'La lectura del lugar integra la observación del suelo, la vegetación, la fauna y los flujos naturales '
            'del espacio. Es el punto de partida indispensable para cualquier diseño regenerativo.</div>', unsafe_allow_html=True)

        # ── Mapa del espacio (satélite, alta resolución) ───────────
        _lat_r = _safe_float(data.get("geo_lat"))
        _lon_r = _safe_float(data.get("geo_lon"))
        if _lat_r and _lon_r:
            st.markdown("##### 🗺️ Ubicación del Espacio")
            addr_str = data.get("proyecto_direccion", "") or data.get("geo_display", "")
            if addr_str:
                st.caption(f"📍 {addr_str}")
            _render_report_map(_lat_r, _lon_r, data, map_key="rpt_registro_map")
            _gc1, _gc2 = st.columns(2)
            with _gc1:
                st.markdown(
                    f'<a href="https://www.google.com/maps/@{_lat_r},{_lon_r},19z/data=!3m1!1e3" '
                    f'target="_blank" style="font-size:0.82rem;">🌍 Abrir en Google Maps satélite</a>',
                    unsafe_allow_html=True)
            with _gc2:
                st.markdown(
                    f'<a href="https://shademap.app/@{_lat_r},{_lon_r},19z" '
                    f'target="_blank" style="font-size:0.82rem;">☀️ Ver sombras en ShadowMap</a>',
                    unsafe_allow_html=True)

            # ── Cuenca Hidrográfica (dentro de Ubicación del Espacio) ─────
            cuenca_nombre = data.get("cuenca_nombre", "")
            if cuenca_nombre:
                st.markdown("##### 🌊 Cuenca Hidrográfica")
                _lat_d = _safe_float(data.get("geo_lat"))
                _lon_d = _safe_float(data.get("geo_lon"))
                _elev_d = _safe_float(data.get("geo_elevation"))
                if _lat_d and _lon_d:
                    _gc1b, _gc2b, _gc3b = st.columns(3)
                    with _gc1b: st.metric("📍 Latitud",  f"{_lat_d:.4f}")
                    with _gc2b: st.metric("📍 Longitud", f"{_lon_d:.4f}")
                    with _gc3b:
                        if _elev_d > 0: st.metric("⛰️ Elevación", f"{_elev_d:.0f} m.s.n.m.")

                st.markdown(
                    '<div style="background:#E3F2FD;border-radius:8px;padding:0.5rem 0.7rem;margin-bottom:0.5rem;'
                    'font-size:0.82rem;color:#1A237E;line-height:1.6;">'
                    'La cuenca hidrográfica define el territorio del agua: de dónde viene, por dónde fluye '
                    'y hacia dónde va. Conocer la cuenca del espacio es fundamental para entender el ciclo '
                    'del agua y diseñar soluciones regenerativas apropiadas.</div>', unsafe_allow_html=True)

                subcuenca_nombre    = data.get("subcuenca_nombre", "")
                subsubcuenca_nombre = data.get("subsubcuenca_nombre", "")

                def _wiki_badge(nivel, nombre, cod, link, bg, border, icon):
                    if not nombre: return ""
                    link_tag = (f'<a href="{link}" target="_blank" '
                                f'style="color:{border};font-weight:700;text-decoration:none;">'
                                f'{nombre} 🔗</a>') if link else f'<strong>{nombre}</strong>'
                    return (
                        f'<div style="background:{bg};border-left:4px solid {border};'
                        f'border-radius:8px;padding:0.55rem 0.8rem;margin-bottom:0.4rem;">'
                        f'<span style="font-size:0.72rem;color:#555;text-transform:uppercase;'
                        f'letter-spacing:0.05em;">{icon} {nivel}</span><br>'
                        f'<span style="font-size:0.88rem;">{link_tag}</span>'
                        + (f'<span style="font-size:0.75rem;color:#888;"> &nbsp;({cod})</span>' if cod else '')
                        + '</div>'
                    )

                badges_html = (
                    _wiki_badge("Cuenca", cuenca_nombre,
                                data.get("cuenca_cod",""), data.get("cuenca_wiki_link",""),
                                "#E3F2FD", "#1565C0", "🌊") +
                    _wiki_badge("Subcuenca", subcuenca_nombre,
                                data.get("subcuenca_cod",""), data.get("subcuenca_wiki_link",""),
                                "#E8F5E9", "#2E7D32", "🏖️") +
                    _wiki_badge("Subsubcuenca", subsubcuenca_nombre,
                                data.get("subsubcuenca_cod",""), data.get("subsubcuenca_wiki_link",""),
                                "#FFF8E1", "#F57F17", "🏔️")
                )
                st.markdown(badges_html, unsafe_allow_html=True)

                wiki_summary = data.get("cuenca_wiki_summary", "")
                wiki_source  = data.get("cuenca_wiki_source", cuenca_nombre)
                wiki_link    = data.get("cuenca_wiki_link", "")
                if wiki_summary:
                    st.markdown(
                        f'<div style="background:#EEF2FF;border-radius:10px;padding:0.75rem 1rem;'
                        f'margin-top:0.4rem;border-left:4px solid #3949AB;">'
                        f'<span style="font-size:0.72rem;color:#3949AB;text-transform:uppercase;'
                        f'letter-spacing:0.06em;">📖 Wikipedia — {wiki_source}</span><br>'
                        f'<span style="font-size:0.84rem;color:#1A237E;line-height:1.7;">{wiki_summary}</span><br>'
                        + (f'<a href="{wiki_link}" target="_blank" style="font-size:0.8rem;color:#3949AB;">'
                           f'Leer más en Wikipedia →</a>' if wiki_link else '')
                        + '</div>', unsafe_allow_html=True)

                sub_wiki  = data.get("subcuenca_wiki_summary", "")
                ssub_wiki = data.get("subsubcuenca_wiki_summary", "")
                if sub_wiki or ssub_wiki:
                    with st.expander("📚 Más información de subcuenca y subsubcuenca", expanded=False):
                        if sub_wiki and subcuenca_nombre:
                            st.markdown(f"**🏖️ {subcuenca_nombre}**")
                            sc_link = data.get("subcuenca_wiki_link","")
                            st.markdown(sub_wiki + (f"\n\n[Leer en Wikipedia ↗]({sc_link})" if sc_link else ""))
                        if ssub_wiki and subsubcuenca_nombre:
                            st.markdown("---")
                            st.markdown(f"**🏔️ {subsubcuenca_nombre}**")
                            ssc_link = data.get("subsubcuenca_wiki_link","")
                            st.markdown(ssub_wiki + (f"\n\n[Leer en Wikipedia ↗]({ssc_link})" if ssc_link else ""))

            st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            # Suelo
            suelo_fields = [("suelo_tipo","Tipo de suelo"),("suelo_compactacion","Compactación"),
                          ("suelo_materia_organica","Materia orgánica"),("suelo_drenaje","Drenaje"),
                          ("suelo_color","Color"),("suelo_olor","Olor"),("suelo_notas","Notas")]
            if any(data.get(k) for k,_ in suelo_fields):
                st.markdown("**🌱 Suelo y Sustrato**")
                for k, l in suelo_fields: _card(l, data.get(k))

            # Vegetación
            veg_types = data.get("veg_tipos", [])
            if veg_types or data.get("veg_especies") or data.get("veg_invasoras"):
                st.markdown("**🌿 Vegetación**")
                if veg_types: _card("Tipos presentes", ", ".join(veg_types))
                _card("Especies identificadas", data.get("veg_especies"))
                _card("Invasoras/Problemáticas", data.get("veg_invasoras"))

        with c2:
            # Flujos
            st.markdown("**☀️ Sol y Viento**")
            _card("Horas sol/día (promedio)", data.get("sol_horas"))
            _card("Sol Invierno", data.get("sol_horas_invierno"))
            _card("Sol Verano", data.get("sol_horas_verano"))
            _card("Orientación", data.get("sol_orientacion"))
            _card("Dirección del viento", data.get("viento_direccion"))
            _card("Zonas protegidas", data.get("viento_protegidas"))
            
            # Biodiversidad
            st.markdown("**🦋 Biodiversidad y Fauna**")
            _card("Polinizadores", data.get("fauna_polinizadores"))
            _card("Aves", data.get("fauna_aves"))
            _card("Especies de aves", data.get("fauna_aves_especies"))
            _card("Lombrices/Suelo", data.get("fauna_lombrices"))

        # --- CALCULADORA DE CULTIVO ---
        st.markdown("---")
        st.markdown("### 🥦 Zonas de Cultivo y Calculadora de Sustrato")
        
        bancales = data.get("bancales", [])
        if not bancales:
            st.info("No se han registrado zonas de cultivo específicas aún.")
        else:
            # ── Totales base ──────────────────────────────────────────
            v_tot = sum(b.get("vol", 0) for b in bancales)
            l_tot = v_tot * 1000
            b_obs = [b for b in bancales if b.get("estado") == "observado"]
            b_pot = [b for b in bancales if b.get("estado") == "potencial"]
            a_obs = sum(b.get("area", 0) for b in b_obs)
            a_pot = sum(b.get("area", 0) for b in b_pot)

            mc1, mc2, mc3 = st.columns(3)
            with mc1: st.metric("✅ Área Activa",    f"{a_obs:.2f} m²")
            with mc2: st.metric("🌱 Área Potencial", f"{a_pot:.2f} m²")
            with mc3: st.metric("💧 Volumen total",  f"{l_tot:,.0f} L", f"{v_tot:.3f} m³")

            st.markdown(f'<div style="font-size:0.8rem;color:#555;margin-bottom:0.8rem;">'
                        f'Detalle de las <strong>{len(bancales)}</strong> zonas registradas:</div>',
                        unsafe_allow_html=True)

            # Grid de bancales (sin saco fijo aún)
            cols_b = st.columns(min(len(bancales), 3))
            for i, b in enumerate(bancales):
                is_pot = b.get("estado") == "potencial"
                bg = "#FFFDE7" if is_pot else "#F0FFF4"
                brd = "#FFA726" if is_pot else "#52B788"
                txt = "#5D4037" if is_pot else "#1B4332"
                icon = "🌱" if is_pot else "✅"
                with cols_b[i % 3]:
                    st.markdown(
                        f'<div style="background:{bg};border:1.5px solid {brd};border-radius:12px;padding:0.8rem;margin-bottom:0.8rem;">'
                        f'<div style="font-size:0.75rem;color:{brd};font-weight:700;text-transform:uppercase;">{icon} {b.get("estado","").title()}</div>'
                        f'<div style="font-size:1rem;font-weight:800;color:{txt};margin:0.2rem 0;">{b.get("nombre","Zona")}</div>'
                        f'<div style="font-size:0.85rem;color:{txt};line-height:1.4;">'
                        f'📏 {b.get("dim","")}<br>'
                        f'📐 Área: <strong>{b.get("area",0):.2f} m²</strong><br>'
                        f'📦 Vol: <strong>{b.get("vol",0):.3f} m³</strong> ({b.get("litros",0):,} L)'
                        f'</div></div>', unsafe_allow_html=True)

            st.markdown("---")

            # ── Calculadora de sustrato premium ──────────────────────
            st.markdown("#### 🧪 Calculadora de Sustrato Premium")

            # Selector de tamaño de saco
            sacol1, sacol2 = st.columns([2, 3])
            with sacol1:
                _saco_opciones = {
                    "20 L  (saco pequeño)":  20,
                    "40 L  (saco estándar)": 40,
                    "50 L  (saco jumbo)":    50,
                    "80 L  (medio metro³)":  80,
                    "Ingresar tamaño personalizado →": None,
                }
                _saco_sel = st.selectbox(
                    "🛍️ Tamaño del saco",
                    list(_saco_opciones.keys()),
                    index=1,  # default 40L
                    key="rpt_saco_sel",
                )
            _saco_base = _saco_opciones[_saco_sel]
            with sacol2:
                saco_l = st.number_input(
                    "Litros por saco (editable)",
                    min_value=1, max_value=500,
                    value=int(_saco_base) if _saco_base else 40,
                    step=5,
                    key="rpt_saco_litros",
                    help="Tamaño de los sacos de sustrato que usarás para rellenar los bancales.",
                )
            sacos_tot = l_tot / saco_l if saco_l > 0 else 0
            st.metric("📦 Sacos necesarios (total)", f"~{sacos_tot:.1f} sacos de {saco_l} L",
                      f"{l_tot:,.0f} litros en total")

            st.markdown("---")

            # ── Receta de sustrato premium ────────────────────────────
            with st.expander("📖 Receta de Sustrato Premium — ver ingredientes y proporciones", expanded=False):
                st.markdown("""
**🌿 Sustrato Premium para Bancales de Cultivo**

| Ingrediente | % | Función |
|---|---|---|
| 🍂 Compost maduro | 30 % | Fuente principal de N, P, K. Aporta microbiología activa y mejora la fertilidad. |
| 🪱 Humus de lombriz | 10 % | Refuerzo biológico, rico en enzimas. Mejora la retención de nutrientes y agua. |
| 🍃 Tierra de hoja | 40 % | Estructura ligera, rica en materia orgánica. Favorece retención de humedad y aireación. |
| 🪨 Perlita / Vermiculita | 15 % | Aporta aireación, evita compactación. Regula humedad y mejora el drenaje. |
| 🥥 Fibra de coco / Arena | 5 % | Ajusta la textura, mantiene el sustrato suelto. Equilibra humedad y drenaje. |

> 💡 **Tip:** El compost debe estar **completamente maduro** (no fresco) para evitar quemar las raíces.  
> La perlita puede reemplazarse por vermiculita si buscas mayor retención de humedad (climas secos).
""")

            # ── Porcentajes editables ─────────────────────────────────
            st.markdown("**🎛️ Ajustar proporciones del sustrato**")
            st.caption("Edita los porcentajes según tus materiales disponibles. La suma debe ser 100%.")

            _ingredientes = [
                ("🍂 Compost maduro",       "pct_compost",    30, "#A5D6A7", "#2E7D32"),
                ("🪱 Humus de lombriz",      "pct_humus",      10, "#FFF9C4", "#F9A825"),
                ("🍃 Tierra de hoja",        "pct_tierra",     40, "#C8E6C9", "#1B5E20"),
                ("🪨 Perlita / Vermiculita", "pct_perlita",    15, "#B3E5FC", "#0277BD"),
                ("🥥 Fibra de coco / Arena", "pct_fibra",       5, "#FFE0B2", "#E65100"),
            ]

            pcts = {}
            ing_cols = st.columns(len(_ingredientes))
            for col, (label, key, default, bg, color) in zip(ing_cols, _ingredientes):
                with col:
                    pcts[key] = st.number_input(
                        label,
                        min_value=0, max_value=100,
                        value=default, step=1,
                        key=f"rpt_{key}",
                    )

            total_pct = sum(pcts.values())
            diff = total_pct - 100

            # Balance indicator
            if total_pct == 100:
                st.success("✅ Mezcla perfecta — la suma es exactamente 100%.")
            elif diff > 0:
                st.warning(f"⚠️ La mezcla suma **{total_pct}%** — tienes **{diff}% de sobra**. Reduce algún ingrediente.")
            else:
                st.error(f"❌ La mezcla suma **{total_pct}%** — te faltan **{abs(diff)}%** para completar. Aumenta algún ingrediente.")

            # ── Desglose por ingrediente ──────────────────────────────
            st.markdown("**📊 Sustrato necesario por ingrediente**")

            for label, key, default, bg, color in _ingredientes:
                pct  = pcts[key] / 100
                litros_ing = l_tot * pct
                sacos_ing  = litros_ing / saco_l if saco_l > 0 else 0
                bar_w = int(pcts[key])
                st.markdown(
                    f'<div style="background:{bg};border-left:4px solid {color};border-radius:8px;'
                    f'padding:0.5rem 0.9rem;margin-bottom:0.4rem;display:flex;align-items:center;gap:0.8rem;">'
                    f'<div style="flex:1;">'
                    f'<span style="font-weight:700;color:{color};font-size:0.88rem;">{label}</span> '
                    f'<span style="font-size:0.8rem;color:#555;">— {pcts[key]}%</span><br>'
                    f'<div style="background:#00000015;border-radius:4px;height:6px;margin:3px 0;">'
                    f'<div style="background:{color};border-radius:4px;height:6px;width:{bar_w}%;"></div></div>'
                    f'</div>'
                    f'<div style="text-align:right;min-width:110px;">'
                    f'<strong style="font-size:0.92rem;color:{color};">{litros_ing:,.0f} L</strong><br>'
                    f'<span style="font-size:0.78rem;color:#555;">~{sacos_ing:.1f} sacos</span>'
                    f'</div></div>', unsafe_allow_html=True)

            # Resumen final
            if total_pct == 100:
                st.markdown(
                    f'<div style="background:#E8F5E9;border-radius:10px;padding:0.8rem 1.1rem;margin-top:0.6rem;">'
                    f'<strong style="color:#1B4332;">🛒 Lista de compra estimada</strong><br>'
                    + "".join(
                        f'• {lbl}: <strong>{l_tot * pcts[k] / 100:,.0f} L</strong> (~{l_tot * pcts[k] / 100 / saco_l:.1f} sacos de {saco_l}L)<br>'
                        for lbl, k, *_ in _ingredientes
                    )
                    + f'<br><strong>Total sacos a comprar: ~{sacos_tot:.0f} sacos de {saco_l} L</strong>'
                    + '</div>', unsafe_allow_html=True)


        _ref_box([("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
                  ("Mason, F. (2025)", "Introducción al enfoque de la regeneración", MASON_URL)])

        # ── Clima histórico del lugar ─────────────────────────────

        geo_clima = data.get("geo_clima_anual")
        if geo_clima:
            try:
                import ast as _ast_c
                climate_d = _ast_c.literal_eval(geo_clima) if isinstance(geo_clima, str) else geo_clima
                if isinstance(climate_d, dict) and climate_d.get("months"):
                    st.markdown("---")
                    st.markdown("#### 🌦️ Clima e Hidrografía del Lugar")
                    
                    st.markdown(
                        '<div style="background:#E3F2FD;border-radius:8px;padding:0.5rem 0.8rem;'
                        'margin-bottom:0.6rem;font-size:0.82rem;color:#1A237E;line-height:1.6;">'
                        'Datos climáticos históricos (promedio 5 años) provistos por '
                        '<strong>Open-Meteo Historical Weather API</strong> para las coordenadas exactas '
                        'del espacio. Las líneas muestran temperaturas máximas (rojo) y mínimas (azul); '
                        'las barras muestran precipitación mensual promedio.</div>',
                        unsafe_allow_html=True)

                    # Gráfico temperatura + precipitación
                    fig_clima = go.Figure()
                    fig_clima.add_trace(go.Bar(
                        name="Precipitación (mm)", x=climate_d["months"],
                        y=climate_d.get("prec", []), yaxis="y2",
                        marker_color="rgba(30,136,229,0.45)", offsetgroup=1))
                    fig_clima.add_trace(go.Scatter(
                        name="T° Máx", x=climate_d["months"],
                        y=climate_d.get("t_max", []),
                        line=dict(color="#E53935", width=2.5), mode="lines+markers",
                        marker=dict(size=6)))
                    fig_clima.add_trace(go.Scatter(
                        name="T° Mín", x=climate_d["months"],
                        y=climate_d.get("t_min", []),
                        line=dict(color="#1565C0", width=2.5), mode="lines+markers",
                        marker=dict(size=6)))
                    fig_clima.update_layout(
                        yaxis=dict(title="Temperatura (°C)", side="left"),
                        yaxis2=dict(title="Precipitación (mm)", side="right", overlaying="y"),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
                        height=320, margin=dict(l=40, r=40, t=30, b=30),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,255,248,0.5)")
                    st.plotly_chart(fig_clima, use_container_width=True, key="clima_datos_proyecto")

                    # Métricas clave en 5 columnas
                    st.markdown("**📊 Indicadores climáticos clave**")
                    km1, km2, km3, km4, km5 = st.columns(5)
                    anio_ref = climate_d.get("anio_referencia", "")
                    with km1:
                        mes_cal = data.get("clima_mes_caluroso") or climate_d.get("mes_mas_caluroso", "—")
                        st.metric("🌡️ Mes más cálido", mes_cal,
                                  f"Máx prom: {climate_d.get('t_max_media', '?')}°C")
                    with km2:
                        mes_frio = data.get("clima_mes_frio") or climate_d.get("mes_mas_frio", "—")
                        st.metric("🥶 Mes más frío", mes_frio,
                                  f"Mín prom: {climate_d.get('t_min_media', '?')}°C")
                    with km3:
                        t_max_abs = data.get("clima_t_max_abs") or climate_d.get("abs_max_ultimo_anio")
                        st.metric("🔴 T° máxima registrada",
                                  f"{t_max_abs}°C" if t_max_abs is not None else "—",
                                  f"Año {anio_ref}" if anio_ref else "")
                    with km4:
                        t_min_abs = data.get("clima_t_min_abs") or climate_d.get("abs_min_ultimo_anio")
                        st.metric("🔵 T° mínima registrada",
                                  f"{t_min_abs}°C" if t_min_abs is not None else "—",
                                  f"Año {anio_ref}" if anio_ref else "")
                    with km5:
                        prec_total = _safe_float(data.get("agua_prec_anual")) or round(
                            sum(p for p in climate_d.get("prec", []) if p))
                        st.metric("💧 Precipitación anual", f"{prec_total:.0f} mm", "promedio histórico")

                    # Mes más lluvioso y meses secos
                    prec_vals = [(i, v) for i, v in enumerate(climate_d.get("prec", [])) if v]
                    if prec_vals:
                        idx_lluv = max(prec_vals, key=lambda x: x[1])
                        months_list = climate_d.get("months", [])
                        mes_lluv = months_list[idx_lluv[0]] if idx_lluv[0] < len(months_list) else "—"
                        meses_secos = sum(1 for v in climate_d.get("prec", []) if v is not None and v < 5)
                        st.markdown(
                            f'<div style="background:#E3F2FD;border-radius:8px;padding:0.5rem 0.8rem;'
                            f'margin-top:0.3rem;font-size:0.82rem;color:#1A237E;line-height:1.7;">'
                            f'🌧️ <strong>Mes más lluvioso:</strong> {mes_lluv} '
                            f'({idx_lluv[1]:.1f} mm prom.) &nbsp;·&nbsp; '
                            f'☀️ <strong>Meses secos (&lt;5 mm):</strong> {meses_secos} al año'
                            f'</div>', unsafe_allow_html=True)

                    st.caption("📡 Fuente: Open-Meteo Historical Weather API (open-meteo.com) · "
                               "Nominatim OpenStreetMap para geocodificación.")

            except Exception:
                pass

        # ── Energía Solar del Lugar (independiente de geo_clima) ─────
        sol_data_raw = data.get("geo_solar")
        if sol_data_raw:
            try:
                import ast as _ast_s
                sol_data = _ast_s.literal_eval(sol_data_raw) if isinstance(sol_data_raw, str) else sol_data_raw
                if not isinstance(sol_data, dict):
                    sol_data = None
            except Exception:
                sol_data = None
        else:
            sol_data = None

        if sol_data:
            st.markdown("---")
            st.markdown("#### ☀️ Energía Solar del Lugar")
            # Derive metrics from the real keys (monthly_kwh_m2, annual_avg_kwh_m2)
            monthly_vals = sol_data.get("monthly_kwh_m2", [])
            months_list  = sol_data.get("months", [])
            ann_avg = sol_data.get("annual_avg_kwh_m2", 0)
            if not ann_avg and monthly_vals:
                ann_avg = round(sum(monthly_vals) / len(monthly_vals), 2)
            # Best / worst month
            best_val, best_name, worst_val, worst_name = 0, "—", 0, "—"
            if monthly_vals:
                idx_best  = monthly_vals.index(max(monthly_vals))
                idx_worst = monthly_vals.index(min(monthly_vals))
                best_val  = monthly_vals[idx_best]
                worst_val = monthly_vals[idx_worst]
                best_name  = months_list[idx_best]  if idx_best  < len(months_list) else "—"
                worst_name = months_list[idx_worst] if idx_worst < len(months_list) else "—"

            st.markdown(
                '<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem 1rem;'
                'margin-bottom:0.8rem;font-size:0.85rem;color:#827717;line-height:1.6;border:1px solid #FFF176;">'
                'La radiación solar (GHI) indica la energía disponible para fotosíntesis y sistemas fotovoltaicos. '
                'Valores en <strong>kWh/m²/día</strong>.</div>', unsafe_allow_html=True)

            skm1, skm2, skm3 = st.columns(3)
            with skm1: st.metric("☀️ Promedio Anual", f"{ann_avg:.2f} kWh/m²/día")
            with skm2: st.metric("🔥 Mejor Mes", f"{best_val:.2f} kWh/m²/día", delta=best_name, delta_color="off")
            with skm3: st.metric("❄️ Peor Mes", f"{worst_val:.2f} kWh/m²/día", delta=worst_name, delta_color="off")

            # ── Selector de panel + producción estimada ──────────────
            st.markdown("**🔧 Simulador de panel solar**")
            _panel_opciones = {
                "100 W  (pequeño — iluminación + celulares)": 100,
                "200 W  (balcón / terraza pequeña)":          200,
                "300 W  (uso doméstico básico)":              300,
                "400 W  (uso doméstico estándar ✅ más común)": 400,
                "500 W  (sistema robusto)":                   500,
            }
            _sel_panel_label = st.selectbox(
                "Selecciona el tipo de panel solar",
                list(_panel_opciones.keys()),
                index=3,
                key="rpt_panel_selector",
            )
            _panel_w  = _panel_opciones[_sel_panel_label]
            _panel_kw = _panel_w / 1000
            _efi      = 0.80  # eficiencia del sistema (80%)

            # Producción mensual del panel seleccionado = monthly_kwh_m2 × kW × eficiencia
            _panel_monthly = [round(v * _panel_kw * _efi, 2) for v in monthly_vals] if monthly_vals else []
            _panel_avg     = round(sum(_panel_monthly) / len(_panel_monthly), 2) if _panel_monthly else 0
            _panel_best    = max(_panel_monthly) if _panel_monthly else 0
            _panel_worst   = min(_panel_monthly) if _panel_monthly else 0

            pm1, pm2, pm3 = st.columns(3)
            with pm1: st.metric(f"⚡ Producción media ({_panel_w}W)", f"{_panel_avg:.2f} kWh/día")
            with pm2: st.metric("☀️ Mes con más sol", f"{_panel_best:.2f} kWh/día", delta=best_name,  delta_color="off")
            with pm3: st.metric("❄️ Mes con menos sol", f"{_panel_worst:.2f} kWh/día", delta=worst_name, delta_color="off")

            # ── Selector de precio kWh ────────────────────────────────
            st.markdown("**💰 Tarifa eléctrica ($/kWh)**")
            st.markdown(
                '<div style="background:#F3E5F5;border-radius:8px;padding:0.5rem 0.9rem;'
                'margin-bottom:0.5rem;font-size:0.8rem;color:#4A148C;line-height:1.7;">'
                '📋 <strong>Tarifas BT1 referenciales — Enel, Abril 2026</strong> '
                '(<a href="https://cuentadelaluz.cl/" target="_blank" style="color:#7B1FA2;">cuentadelaluz.cl</a>):<br>'
                '&nbsp;&nbsp;• <strong>T1</strong> ≤ 200 kWh/mes → <strong>$226/kWh</strong> &nbsp;·&nbsp; '
                '<strong>T2</strong> 201–350 kWh → <strong>$260/kWh</strong> &nbsp;·&nbsp; '
                '<strong>T3</strong> 351–450 kWh → <strong>$280/kWh</strong> &nbsp;·&nbsp; '
                '<strong>T4</strong> 451–650 kWh → <strong>$310/kWh</strong><br>'
                '&nbsp;&nbsp;Cargo fijo mensual: $709 (independiente del consumo).'
                '</div>', unsafe_allow_html=True)

            _tarifa_presets = {
                "T1 — ≤ 200 kWh/mes  →  $226/kWh  (más común hogares pequeños)": 226,
                "T2 — 201–350 kWh/mes →  $260/kWh": 260,
                "T3 — 351–450 kWh/mes →  $280/kWh": 280,
                "T4 — 451–650 kWh/mes →  $310/kWh": 310,
                "Ingresar precio personalizado →": None,
            }
            tc1, tc2, tc3 = st.columns([3, 1, 1])
            with tc1:
                _tarifa_sel = st.selectbox(
                    "Selecciona tu tramo tarifario",
                    list(_tarifa_presets.keys()),
                    index=0,
                    key="rpt_tarifa_selector",
                )
            _precio_base = _tarifa_presets[_tarifa_sel]
            with tc2:
                _precio_kwh = st.number_input(
                    "$/kWh",
                    min_value=50, max_value=800,
                    value=int(_precio_base) if _precio_base else 226,
                    step=5,
                    key="rpt_precio_kwh",
                    help="Costo variable por kWh consumido. Fuente: cuentadelaluz.cl",
                )
            with tc3:
                _cargo_fijo = st.number_input(
                    "Cargo fijo $/mes",
                    min_value=0, max_value=5000,
                    value=709,
                    step=10,
                    key="rpt_cargo_fijo",
                    help="Costo fijo mensual de conexión a la red (BT1 Enel Abril 2026: $709). No se reduce con paneles solares.",
                )

            # Texto interpretativo con precio seleccionado
            _ahorro_mes = round(_panel_avg * 30 * _precio_kwh)
            _ahorro_año = _ahorro_mes * 12
            _cuenta_sin_paneles = _cargo_fijo + round(_panel_avg * 30 * _precio_kwh)  # lo que se paga sin paneles
            # nota: el cargo fijo se sigue pagando con paneles

            st.markdown(
                f'<div style="background:#E8F5E9;border-radius:10px;padding:0.8rem 1.1rem;'
                f'margin:0.6rem 0 0.8rem;font-size:0.88rem;color:#1B4332;line-height:1.85;">'
                f'☀️ Un panel de <strong>{_panel_w} W</strong> en este espacio generaría en promedio '
                f'<strong>{_panel_avg:.2f} kWh/día</strong> — es decir, '
                f'<strong>{round(_panel_avg*30, 1)} kWh/mes</strong>.<br>'
                f'💰 A <strong>${_precio_kwh}/kWh</strong>, el ahorro en energía variable es de '
                f'<strong>${_ahorro_mes:,}/mes</strong> · <strong>${_ahorro_año:,}/año</strong>.<br>'
                f'<span style="font-size:0.8rem;color:#555;">'
                f'📌 Cargo fijo: <strong>${_cargo_fijo:,}/mes</strong> — este costo de conexión a la red '
                f'<em>se sigue pagando aunque tengas paneles</em>. &nbsp;'
                f'⚙️ Cálculo: {_panel_w}W × {ann_avg:.2f} GHI × 80% eficiencia del sistema.'
                f'</span></div>', unsafe_allow_html=True)

            # ── Gráfico mensual GHI + producción del panel ────────────
            if monthly_vals and months_list:
                fig_sol = go.Figure()
                fig_sol.add_trace(go.Bar(
                    name=f"Producción panel {_panel_w}W (kWh/día)",
                    x=months_list, y=_panel_monthly,
                    marker_color="rgba(255,167,38,0.75)",
                    text=[f"{v:.2f}" for v in _panel_monthly],
                    textposition="outside", textfont=dict(size=9, color="#E65100"),
                ))
                fig_sol.add_trace(go.Scatter(
                    name="Radiación GHI (kWh/m²/día)",
                    x=months_list, y=monthly_vals,
                    mode="lines+markers",
                    line=dict(color="#FDD835", width=2.5),
                    marker=dict(size=7, color="#F57F17"),
                    yaxis="y2",
                ))
                fig_sol.update_layout(
                    yaxis=dict(title=f"Producción panel {_panel_w}W (kWh/día)", range=[0, max(_panel_monthly or [1]) * 1.3]),
                    yaxis2=dict(title="GHI kWh/m²/día", overlaying="y", side="right",
                                range=[0, max(monthly_vals or [1]) * 1.3]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=10)),
                    height=300, margin=dict(l=40, r=40, t=30, b=30),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,253,231,0.4)",
                    barmode="group",
                )
                st.plotly_chart(fig_sol, use_container_width=True, key="rpt_solar_chart")


        # ── Potencial de captación de agua de lluvia ───────────────
        prec_v  = _safe_float(data.get("agua_prec_anual"))
        techo_v = _safe_float(data.get("agua_techo_m2"))
        efic_v  = _safe_float(data.get("agua_efic_captacion", 80))
        litros_cap = _safe_float(data.get("agua_litros_captacion_anual"))
        if litros_cap == 0 and prec_v > 0 and techo_v > 0:
            litros_cap = round(prec_v * techo_v * efic_v / 100)

        if prec_v > 0 and techo_v > 0:
            st.markdown("---")
            st.markdown("#### ☔ Potencial de Captación de Agua de Lluvia")
            st.markdown(
                '<div style="background:#E3F2FD;border-radius:8px;padding:0.6rem 0.9rem;'
                'margin-bottom:0.6rem;font-size:0.82rem;color:#1A237E;line-height:1.6;">'
                'La captación de agua de lluvia es una de las estrategias más accesibles y '
                'regenerativas para reducir el consumo de agua potable y mejorar la autonomía '
                'hídrica del espacio. La fórmula es simple: '
                '<strong>Litros = Precipitación anual × Área de techo × Eficiencia de captación</strong>.'
                '</div>', unsafe_allow_html=True)

            wc1, wc2, wc3, wc4 = st.columns(4)
            with wc1: st.metric("🌧️ Precipitación anual", f"{prec_v:.0f} mm")
            with wc2: st.metric("🏠 Área de techo", f"{techo_v:.0f} m²")
            with wc3: st.metric("⚙️ Eficiencia", f"{efic_v:.0f}%")
            with wc4: st.metric("💧 Captación estimada", f"{litros_cap:,.0f} L/año")

            # Contexto en equivalencias útiles
            litros_dia = round(litros_cap / 365)
            meses_agua = round(litros_cap / 4000) if litros_cap > 0 else 0
            st.markdown(
                f'<div style="background:#E8F5E9;border-radius:8px;padding:0.7rem 1rem;'
                f'margin-top:0.4rem;font-size:0.85rem;color:#1B4332;line-height:1.8;">'
                f'📌 <strong>¿Qué significa esto?</strong><br>'
                f'• <strong>{litros_dia} litros por día</strong> en promedio anual disponibles para riego u otros usos no potables.<br>'
                f'• Equivale aproximadamente a <strong>{meses_agua} meses</strong> de agua para un hogar de 4 personas (consumo riego ~350 L/día).<br>'
                f'</div>', unsafe_allow_html=True)

        _ref_box([("Mason, F. (2025)", "Introducción al enfoque de la regeneración", MASON_URL)])
        st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # SECCION 3 -- TAO DE LA REGENERACION (v2 -- 5 dimensiones)
    # ==================================================================
    if _show("tao"):
        st.markdown(f"#### ☯️ Tao para una vida regenerativa &nbsp; {_status_badge('mod_tao')}", unsafe_allow_html=True)
        st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">{TAO_REFLEXION_SHORT}</div>', unsafe_allow_html=True)

        # Import Tao module functions
        try:
            from modules.tao import (
                TAO_DIMENSIONES, TAO_DISCLAIMER, TAO_INTRO, TAO_EPIGRAFE,
                _render_tao_radar,
                get_tao_scores, get_tao_total, get_tao_label
            )

            # ── Introduccion: que es el Tao de la Regeneracion ──────────
            with st.expander("¿Cómo ayuda el Tao para la regeneración? (clic para leer)", expanded=False):
                st.markdown(
                    f'<div style="background:#F0FFF4;border-radius:8px;padding:0.8rem;'
                    f'margin-bottom:0.5rem;border-left:3px solid #2D6A4F;">'
                    f'<em style="color:#555;font-size:0.85rem;">'
                    f'&laquo;{TAO_EPIGRAFE}&raquo;</em><br>'
                    f'<span style="font-size:0.75rem;color:#888;">-- Reflexiones frente a Lao Tse, Hua Dao (2025)</span>'
                    f'</div>', unsafe_allow_html=True)
                st.markdown(TAO_INTRO)
                st.info(TAO_DISCLAIMER)
                st.markdown(
                    '<div style="font-size:0.8rem;color:#555;margin-top:0.5rem;line-height:1.6;">'
                    '<strong>Referencias:</strong><br>'
                    '📖 <a href="https://drive.google.com/file/d/1JAWwhCOyvZKrACoAk5bv5Jh2thxppLZh/view" target="_blank">Tao Te Ching — Texto completo en español (PDF)</a><br>'
                    '📖 <a href="https://drive.google.com/file/d/1MLOLcIso_inxbpIaoJfcdrZimVl9xHgj/view?usp=sharing" target="_blank">Mason, F. (2026) El Tao para una vida regenerativa — LivLin</a><br>'
                    '📖 <a href="https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing" target="_blank">Mason, F. (2025) Introducción al enfoque de la regeneración — LivLin</a>'
                    '</div>', unsafe_allow_html=True)

            scores = get_tao_scores(data)
            valores = [scores[d["id"]] for d in TAO_DIMENSIONES]
            total = get_tao_total(data)

            if any(v > 0 for v in valores):
                # Radar
                st.markdown("##### 5 dimensiones de sabiduría taoísta para la regeneración")
                _render_tao_radar(valores, compact=True)

                # Score total
                if total > 0:
                    lv_tao = "Semilla" if total < 10 else "Brote" if total < 15 else "Crecimiento" if total < 20 else "Abundancia"
                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#F0FFF4,#E8F5E9);'
                        f'border-radius:10px;padding:0.6rem 1rem;margin:0.5rem 0 1rem;'
                        # f'border-left:4px solid #2D6A4F;font-size:0.88rem;color:#1B4332;">'
                        # f'<strong>Puntaje total Tao:</strong> {total}/25 — {lv_tao}'
                        f'</div>', unsafe_allow_html=True)

                # st.markdown("---")

                # Una tarjeta unificada por dimensión
                for dim in TAO_DIMENSIONES:
                    v = scores.get(dim["id"], 0)
                    opt_text = dim["opciones"][v-1] if 1 <= v <= 5 else "Sin responder"
                    nivel_color = ["#E53935","#FB8C00","#FDD835","#43A047","#1B5E20"][v-1] if 1 <= v <= 5 else "#999"
                    nivel_bg    = ["#FFEBEE","#FFF3E0","#FFFDE7","#E8F5E9","#E8F5E9"][v-1] if 1 <= v <= 5 else "#F5F5F5"
                    estrellas   = "●" * v + "○" * (5 - v) if v > 0 else "○○○○○"

                    # Cita principal inline
                    cita_html = (
                        f'<div style="border-left:3px solid #A8D5B5;padding:0.4rem 0.7rem;'
                        f'margin:0.6rem 0;background:#F9FFFC;border-radius:0 6px 6px 0;">'
                        f'<em style="color:#2D6A4F;font-size:0.83rem;">&laquo;{dim["cita_tao"]}&raquo;</em>'
                        f'<span style="font-size:0.72rem;color:#888;display:block;margin-top:0.15rem;">— {dim["cita_cap"]}</span>'
                        f'</div>'
                    )

                    # Descripción (primer párrafo visible, resto en expander)
                    parrafos = [p.strip() for p in dim["descripcion"].split("\n\n") if p.strip()]
                    desc_visible = parrafos[0] if parrafos else ""
                    desc_resto   = "\n\n".join(parrafos[1:]) if len(parrafos) > 1 else ""

                    # Tarjeta principal
                    st.markdown(
                        f'<div style="border:1.5px solid #B7E4C7;border-radius:12px;'
                        f'margin:0.8rem 0 0;overflow:hidden;">'

                        # Header: número + título + subtítulo + badge nivel
                        f'<div style="background:linear-gradient(135deg,#D8F3DC,#E8F5E9);'
                        f'padding:0.7rem 1rem;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;">'
                        f'<span style="font-size:1.3rem;font-weight:900;color:#1B4332;'
                        f'min-width:1.8rem;text-align:center;">{dim["icono"]}</span>'
                        f'<div style="flex:1;">'
                        f'<div style="font-size:0.95rem;font-weight:800;color:#1B4332;">{dim["titulo"]}</div>'
                        f'<div style="font-size:0.78rem;color:#40916C;font-style:italic;">{dim["subtitulo"]}</div>'
                        f'</div>'
                        f'<div style="background:{nivel_bg};border:1px solid {nivel_color};'
                        f'border-radius:20px;padding:0.2rem 0.8rem;text-align:center;">'
                        f'<div style="font-size:0.95rem;color:{nivel_color};letter-spacing:2px;">{estrellas}</div>'
                        f'<div style="font-size:0.72rem;color:{nivel_color};font-weight:700;">{v}/5</div>'
                        f'</div>'
                        f'</div>'

                        # Nivel seleccionado
                        f'<div style="background:{nivel_bg};border-bottom:1px solid #D8F3DC;'
                        f'padding:0.45rem 1rem;font-size:0.83rem;color:#333;">'
                        f'<strong style="color:{nivel_color};">Nivel {v}:</strong> {opt_text}'
                        f'</div>'

                        # Cita + primer párrafo descripción
                        f'<div style="padding:0.7rem 1rem 0.2rem;">{cita_html}'
                        f'<p style="font-size:0.85rem;color:#333;line-height:1.7;margin:0.4rem 0 0.6rem;">{desc_visible}</p>'
                        f'</div>'

                        # Pregunta de reflexión al pie
                        f'<div style="background:#F0FFF4;border-top:1px solid #D8F3DC;'
                        f'padding:0.55rem 1rem;font-size:0.83rem;color:#2D6A4F;">'
                        f'<strong>💭 Pregunta de reflexión:</strong> <em>{dim["pregunta"]}</em>'
                        f'</div>'

                        f'</div>',
                        unsafe_allow_html=True)

                    # Expander solo si hay párrafos adicionales o cita extra
                    has_more = desc_resto or dim.get("cita_extra")
                    if has_more:
                        with st.expander("Leer más sobre esta dimensión", expanded=False):
                            if desc_resto:
                                for p in desc_resto.split("\n\n"):
                                    if p.strip():
                                        st.markdown(
                                            f'<p style="font-size:0.86rem;color:#333;line-height:1.7;margin:0.3rem 0;">{p.strip()}</p>',
                                            unsafe_allow_html=True)
                            if dim.get("cita_extra"):
                                st.markdown(
                                    f'<div style="background:#FAFAFA;border-radius:6px;padding:0.4rem 0.8rem;'
                                    f'margin-top:0.5rem;border-left:2px solid #A8D5B5;">'
                                    f'<em style="color:#555;font-size:0.82rem;">&laquo;{dim["cita_extra"]}&raquo;</em>'
                                    f'<span style="font-size:0.72rem;color:#888;display:block;margin-top:0.1rem;">'
                                    f'— {dim.get("cita_extra_cap","")}</span>'
                                    f'</div>', unsafe_allow_html=True)

                # Disclaimer al pie
                st.markdown(
                    f'<div style="background:#FFFDE7;border-radius:8px;padding:0.6rem 0.9rem;'
                    f'margin-top:1rem;font-size:0.8rem;color:#5D4037;border-left:3px solid #F9A825;">'
                    f'📌 <strong>Nota interpretativa:</strong> {TAO_DISCLAIMER}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="background:#F5F5F5;border-radius:8px;padding:0.8rem 1rem;'
                    'font-size:0.85rem;color:#777;font-style:italic;">'
                    'Las dimensiones del Tao no han sido evaluadas en este diagnóstico.</div>',
                    unsafe_allow_html=True)

            # Notas del facilitador
            notas = data.get("tao_notas", "")
            if notas:
                st.markdown(
                    f'<div style="background:#E8F5E9;border-radius:8px;padding:0.6rem 0.9rem;'
                    f'margin-top:0.8rem;border-left:3px solid #2D6A4F;">'
                    f'<div style="font-size:0.72rem;color:#52B788;text-transform:uppercase;'
                    f'font-weight:700;margin-bottom:0.2rem;">Notas del facilitador/a</div>'
                    f'<div style="font-size:0.85rem;color:#1B4332;">{notas}</div></div>',
                    unsafe_allow_html=True)

        except Exception as e:
            st.caption(f"Tao de la Regeneracion: {e}")

        # Health/wellbeing data (complementary to Petalo 5)
        salud_fields = [
            ("Alimentacion", "sal_alimentacion"),
            ("Alimentos locales", "sal_alim_local"),
            ("Base vegetal", "sal_alim_plantas"),
            ("Actividad fisica", "sal_ejercicio"),
            ("Contacto naturaleza", "sal_contacto_naturaleza"),
            ("Descanso", "sal_descanso"),
            ("Practicas de bienestar", "sal_practicas_text"),
        ]
        sal_has_data = any(data.get(k) and data.get(k) != "No registrado" for _, k in salud_fields)
        if sal_has_data:
            st.markdown("#### 🍎 Salud y Bienestar")
            for lbl, key in salud_fields:
                v = data.get(key)
                if v and v != "No registrado":
                    _card(lbl, str(v), bg="#FFF8E1", border="#A67C00")

        _ref_box([("Mason, F. (2026)", "El Tao para una vida regenerativa — LivLin", "https://drive.google.com/file/d/1MLOLcIso_inxbpIaoJfcdrZimVl9xHgj/view?usp=sharing"),
                  ("Lao Tse (s. VI a.C.)", "Tao Te Ching — Texto completo en espanol (PDF)", "https://drive.google.com/file/d/1JAWwhCOyvZKrACoAk5bv5Jh2thxppLZh/view"),])
        st.markdown("---")

    # ==================================================================
    # SECCION 3b -- CONCIENCIA ECOLOGICA
    # ==================================================================
    if _show("eco_conciencia"):
        eco_has_data = any(data.get(k) for k in ["eco_cc_conciencia", "eco_bio_conciencia", "eco_cont_conciencia"])
        if eco_has_data:
            st.markdown(f"#### ♻️ Conciencia Ecologica &nbsp; {_status_badge('mod_eco')}", unsafe_allow_html=True)
            st.markdown(
                '<div style="background:#FFF3E0;border-radius:8px;padding:0.6rem;margin-bottom:0.8rem;'
                'font-size:0.85rem;color:#4E342E;">'
                'La triple crisis planetaria -- cambio climatico, perdida de biodiversidad '
                'y contaminacion -- es el contexto en el que toda accion regenerativa se situa.</div>',
                unsafe_allow_html=True)
            for lbl, key in [("Cambio climatico", "eco_cc_conciencia"),
                             ("Impacto local del clima", "eco_cc_impacto"),
                             ("Respuesta al clima", "eco_cc_respuesta"),
                             ("Biodiversidad", "eco_bio_conciencia"),
                             ("Biodiversidad local", "eco_bio_local"),
                             ("Acciones biodiversidad", "eco_bio_accion"),
                             ("Contaminacion", "eco_cont_conciencia"),
                             ("Tipos contaminacion", "eco_cont_tipos"),
                             ("Respuesta contaminacion", "eco_cont_respuesta")]:
                v = data.get(key)
                if v:
                    if isinstance(v, list):
                        v = ", ".join(v)
                    _card(lbl, str(v), bg="#FFF8E1", border="#F57F17")
            st.markdown("---")


    # ==================================================================
    # SECCION 4 -- ANALISIS DE SECTORES (Ecologia + Contexto + Sistemas)
    # ==================================================================
    if _show("analisis_sectores"):
        st.markdown("#### 🔎 Analisis de Sectores")
        st.markdown(
            '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:1rem;'
            'font-size:0.85rem;color:#2D6A4F;line-height:1.7;">'
            'Al aplicar el analisis de sectores, se integra la observacion del espacio y el comportamiento '
            'de los sistemas que lo sustentan (Agua, Energía y Ciclo de Materiales).</div>', unsafe_allow_html=True)

        # ── 4b. Contexto, Agua, Energia y Materiales ──
        st.markdown(f"##### Entorno Urbano, Agua, Energia y Materiales &nbsp; {_status_badge('mod_sistemas')}", unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#E8F5E9;border-radius:6px;padding:0.5rem;margin-bottom:0.8rem;font-size:0.82rem;color:#2D6A4F;">'
            'Analisis de los flujos vitales del espacio: entorno urbano, gestion del agua, consumo energetico '
            'y ciclos de materiales. Cerrar estos ciclos es la base de la autonomia regenerativa.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Contexto del entorno**")
            st.caption("Relacion con el barrio, vecinos, actores locales y acceso a areas verdes.")
            for k,l in [("ctx_ind_verde","Percepción entorno verde"),("ctx_cuenca","Cuenca hidrográfica"),
                        ("ctx_vecinos","Relación con vecinos"),("ctx_participacion","Participación barrial"),
                        ("ctx_distancia_parques","Distancia al parque más cercano (m)")]:
                v = data.get(k)
                if v: _card(l, str(v))

            # Parques cercanos
            parques = data.get("ctx_parques_lista", [])
            if isinstance(parques, list) and parques:
                parks_text = "; ".join(f"{p.get('nombre','')} ({p.get('dist',0)}m — {p.get('uso','')})" for p in parques)
                _card("Parques y áreas verdes cercanas", parks_text, bg="#E8F5E9", border="#2E7D32")

            # Actores territoriales
            actores = data.get("ctx_actores", [])
            if isinstance(actores, list) and actores:
                act_text = "; ".join(f"{a.get('nombre','')} ({a.get('tipo','')}, {a.get('relacion','')})" for a in actores)
                _card("Actores territoriales identificados", act_text, bg="#E8F5E9", border="#2E7D32")

        with c2:
            st.markdown("**Gestion del agua**")
            st.caption("Fuentes, consumo, captacion de lluvia, reutilizacion de aguas grises y riego.")
            for k,l in [("agua_ind_general","Percepción agua"),("agua_fuente","Fuente principal"),
                        ("agua_captacion_lluvia","Captación lluvia"),("agua_grises","Aguas grises"),
                        ("agua_riego_sistema","Sistema riego"),("agua_fugas","Fugas"),
                        ("agua_sequias","Experiencia sequías"),("agua_sequias_impacto","Impacto de la sequía")]:
                v = data.get(k)
                if v and str(v) not in ["No registrado",""]: _card(l, str(v), bg="#E3F2FD", border="#1565C0")

            # Consumo de agua calculado
            consumo_l = _safe_float(data.get("agua_consumo_estimado_ldia"))
            consumo_m3 = _safe_float(data.get("agua_consumo"))
            if consumo_l > 0:
                _card("Consumo estimado de agua", f"{consumo_l:.0f} L/día · {consumo_m3:.1f} m³/mes", bg="#E3F2FD", border="#1565C0")

            # Potencial captación lluvia
            prec = _safe_float(data.get("agua_prec_anual"))
            techo = _safe_float(data.get("agua_techo_m2"))
            efic = _safe_float(data.get("agua_efic_captacion", 80))
            cap = round(prec * techo * efic / 100) if prec > 0 and techo > 0 else 0
            litros_cap = _safe_float(data.get("agua_litros_captacion_anual", cap))
            if litros_cap > 0:
                _card("☔ Potencial captación lluvia",
                      f"{litros_cap:,.0f} L/año · Techo: {techo:.0f} m² · Precip: {prec:.0f} mm · Efic: {efic:.0f}%",
                      bg="#E3F2FD", border="#1565C0")

            # =========================================================
            # 🔌 BLOQUE ENERGÍA — DIAGNÓSTICO + SIMULACIÓN
            # =========================================================

        

        # =========================================================
        # 🔌 BLOQUE ENERGÍA — MODELO REGENERATIVO + ECONÓMICO
        # =========================================================

        st.markdown("**Energia**")
        st.caption("Fuente, consumo, eficiencia y potencial de transición a renovables.")

        # ---------------------------------------------------------
        # 🧾 1. CONSUMO
        # ---------------------------------------------------------

        cuenta_kwh = _safe_float(data.get("ene_consumo_cuenta_kwh"))
        kwh = _safe_float(data.get("ene_kwh_dia_calc"))

        consumo_dia = None
        if kwh > 0:
            consumo_dia = kwh
        elif cuenta_kwh > 0:
            consumo_dia = cuenta_kwh / 30

        if consumo_dia:
            _card(
                "🔌 Consumo del espacio",
                f"{round(consumo_dia,1)} kWh/día · {round(consumo_dia*30):,} kWh/mes",
                bg="#FFF8E1", border="#F57C00"
            )

        # ---------------------------------------------------------
        # 💰 2. PRECIO ELECTRICIDAD (EDITABLE)
        # ---------------------------------------------------------

        precio_kwh = st.slider(
            "💰 Precio electricidad ($/kWh)",
            100, 400, 230,
            help="Puedes ajustarlo según tu tarifa real (ver enlace abajo)"
        )

        # ---------------------------------------------------------
        # ☀️ 3. RECURSO SOLAR
        # ---------------------------------------------------------

        sol_horas = _safe_float(data.get("sol_horas", 0))

        if sol_horas > 0:

            recurso_solar = round(sol_horas, 2)  # kWh/m²/día

            st.markdown("**☀️ Energía Solar del Lugar**")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Recurso solar", f"{recurso_solar} kWh/m²/día")

            with col2:
                st.metric("Horas sol pico", f"{sol_horas:.1f} h/día")

            # -----------------------------------------------------
            # 🔧 4. CONFIGURACIÓN DEL SISTEMA
            # -----------------------------------------------------

            potencia_panel_w = st.selectbox(
                "🔧 Tamaño de panel solar",
                [200, 300, 400, 500],
                index=2,
                help="Selecciona el tipo de panel que usarías en un sistema real"
            )

            potencia_panel_kw = potencia_panel_w / 1000

            eficiencia = 0.8  # pérdidas del sistema

            # -----------------------------------------------------
            # ⚡ 5. CÁLCULOS ENERGÉTICOS
            # -----------------------------------------------------

            sistema_kw = None
            energia_panel_dia = None
            paneles_necesarios = None
            cobertura = None

            if consumo_dia:
                sistema_kw = consumo_dia / (sol_horas * eficiencia)

            energia_panel_dia = potencia_panel_kw * sol_horas * eficiencia

            if sistema_kw:
                paneles_necesarios = sistema_kw / potencia_panel_kw

            if consumo_dia:
                cobertura = (energia_panel_dia / consumo_dia) * 100

            # -----------------------------------------------------
            # 💸 6. CÁLCULOS ECONÓMICOS
            # -----------------------------------------------------

            ahorro_panel_mes = None
            ahorro_total_mes = None

            if energia_panel_dia:
                ahorro_panel_mes = energia_panel_dia * precio_kwh * 30

            if consumo_dia:
                ahorro_total_mes = consumo_dia * precio_kwh * 30

            # -----------------------------------------------------
            # 🧠 7. VISUALIZACIÓN CLAVE (TARJETAS)
            # -----------------------------------------------------

            cols = st.columns(3)

            with cols[0]:
                st.metric("Sistema requerido", f"{round(sistema_kw,2)} kW" if sistema_kw else "—")

            with cols[1]:
                st.metric("Paneles necesarios", f"{round(paneles_necesarios)}" if paneles_necesarios else "—")

            with cols[2]:
                st.metric("Cobertura por panel", f"{round(cobertura,1)}%" if cobertura else "—")

            # -----------------------------------------------------
            # 🧾 8. TEXTO EXPLICATIVO CLARO
            # -----------------------------------------------------

            # Build explanation text safely — only include lines where values exist
            _lineas = [
                f'Este espacio recibe aproximadamente <strong>{sol_horas:.1f} horas de sol pico al día</strong>, '
                f'equivalente a <strong>{recurso_solar} kWh/m²/día</strong> de energía disponible.',
            ]
            if energia_panel_dia is not None:
                _lineas.append(
                    f'Cada panel de <strong>{potencia_panel_w} W</strong> genera cerca de '
                    f'<strong>{round(energia_panel_dia, 2)} kWh/día</strong>.'
                )
            if consumo_dia is not None and sistema_kw is not None:
                _lineas.append(
                    f'Para cubrir el consumo actual (~<strong>{round(consumo_dia, 1)} kWh/día</strong>) '
                    f'se requeriría un sistema de aproximadamente <strong>{round(sistema_kw, 2)} kW</strong> '
                    f'({round(paneles_necesarios) if paneles_necesarios else "?"} paneles de {potencia_panel_w} W).'
                )
            if ahorro_panel_mes is not None:
                _lineas.append(
                    f'El ahorro estimado por panel es de <strong>${round(ahorro_panel_mes):,}/mes</strong>.'
                )
            if ahorro_total_mes is not None:
                _lineas.append(
                    f'Cubrir el 100% del consumo podría significar un ahorro de '
                    f'<strong>${round(ahorro_total_mes):,}/mes</strong>.'
                )
            _lineas.append(
                'La radiación varía durante el año — considera el mes más crítico para dimensionar el sistema.'
            )
            _texto_solar = ' '.join(_lineas)

            st.markdown(
                f'<div style="background:#FFFDE7;border-radius:8px;padding:0.8rem;border-left:4px solid #F57C00;">'                f'<div style="font-weight:700;color:#E65100;margin-bottom:0.4rem;">☀️ Potencial de energía solar</div>'                f'<div style="font-size:0.85rem;color:#5D4037;line-height:1.75;">{_texto_solar}</div>'                f'<div style="font-size:0.78rem;color:#666;margin-top:0.6rem;">'                f'🔧 <strong>Herramientas útiles:</strong><br>'                f'☀️ <a href="https://solar.minenergia.cl/inicio" target="_blank">Explorador Solar Minenergía</a> — Generación real según ubicación<br>'                f'💡 <a href="https://cuentadelaluz.cl/" target="_blank">Cuenta de la Luz</a> — Tarifas eléctricas por comuna'                f'</div></div>',
                unsafe_allow_html=True
            )



        st.markdown("**Materiales y Residuos**")
        st.caption("Compostaje, tipos de residuos, volumen de organicos y oportunidades de cierre de ciclos.")
        for k,l in [("res_compostan","Compostan residuos organicos"),("res_compost_tipo","Tipo de compostaje"),
                    ("res_organico_kg","Residuos organicos (kg/semana)"),("res_tipos_generados","Tipos de residuos"),
                    ("res_intentos_fallidos","Intentos fallidos de compostaje"),
                    ("res_jardin_kg","Residuos de jardin (kg/semana)"),
                    ("mat_notas","Notas sobre materiales")]:
            v = data.get(k)
            if v and str(v) not in ["No registrado",""]:
                if isinstance(v, list):
                    v = ", ".join(str(x) for x in v)
                _card(l, str(v), bg="#F3E5F5", border="#7B1FA2")

    _ref_box([("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
                ("Mollison, B. (1988)", "Permaculture: A Designers' Manual", "https://tagari.com"),
                ("Mason, F. (2025)", "Introducción al enfoque de la regeneración", MASON_URL)])
    st.markdown("---")


    # ══════════════════════════════════════════════════════════════════
    # SECCIÓN 6 — REGISTRO FOTOGRÁFICO (restored from v6)
    # ══════════════════════════════════════════════════════════════════
    if _show("fotos"):
        st.markdown(f"#### 📷 Registro Fotografico &nbsp; {_status_badge('mod_fotos')}", unsafe_allow_html=True)
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
            'Fotografias registradas durante el diagnostico del espacio. '
            'Documentan el estado actual, las condiciones ecologicas y las oportunidades identificadas.</div>', unsafe_allow_html=True)

        _photos_shown = False

        # Demo mode: load placeholder images from assets/demo/
        if st.session_state.get("demo_mode", False):
            try:
                from pathlib import Path as _P
                demo_dir = _P(__file__).parent.parent / "assets" / "demo"
                demo_photos = [
                    ("demo_foto_1.png", "Vista general del espacio"),
                    ("demo_foto_2.png", "Detalle del suelo y vegetacion"),
                    ("demo_foto_3.png", "Contexto urbano y entorno"),
                ]
                existing = [(demo_dir / fn, cap) for fn, cap in demo_photos if (demo_dir / fn).exists()]
                if existing:
                    _photos_shown = True
                    st.markdown(f"**{len(existing)} foto(s) del diagnostico:**")
                    cols_ph = st.columns(min(3, len(existing)))
                    for idx, (fpath, caption) in enumerate(existing):
                        with cols_ph[idx % 3]:
                            st.image(str(fpath), caption=caption, use_container_width=True)
                    st.caption("*Imagenes de referencia — seran reemplazadas con fotos reales del espacio.*")
            except Exception:
                pass
        else:
            # Real mode: load from Supabase
            visit_id = data.get("id", "")
            if visit_id:
                try:
                    from utils.supabase_db import is_configured
                    import base64
                    use_sb = is_configured()
                    if use_sb:
                        from modules.media_manager import _sb_load_photos
                        photos = _sb_load_photos(visit_id)
                    else:
                        from modules.media_manager import _tmp_photos
                        photos = _tmp_photos(visit_id)
                    if photos:
                        _photos_shown = True
                        st.markdown(f"**{len(photos)} foto(s) del diagnostico:**")
                        n_cols = min(3, len(photos))
                        cols_ph = st.columns(n_cols)
                        for idx, ph in enumerate(photos):
                            try:
                                raw = base64.b64decode(ph["data"])
                                with cols_ph[idx % n_cols]:
                                    st.image(raw, caption=ph.get("label",""), use_container_width=True)
                                    created = str(ph.get("created_at",""))[:16].replace("T"," ")
                                    if created: st.caption(f"{created}")
                            except Exception: pass
                except Exception as e:
                    st.caption(f"No se pudieron cargar las fotos: {e}")
        if not _photos_shown:
            st.markdown('<div style="color:#999;font-style:italic;font-size:0.88rem;">No hay fotos registradas para este diagnostico.</div>', unsafe_allow_html=True)
        st.markdown("---")


    # (Flor + Potenciales están integrados en Visión y Estado Regenerativo → Perspectiva Comparada)


    # (Síntesis y Plan movida al inicio — ver bloque SECCIÓN 2 más arriba)

  
    # ══════════════════════════════════════════════════════════════════
    # SECCION 9 -- METODOLOGIA
    if _show("metodologia"):
        st.markdown("#### 📐 Metodología — Cómo funciona este diagnóstico")
        st.markdown(
            '<div style="background:#F0FFF4;border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:1rem;'
            'font-size:0.88rem;color:#2D6A4F;line-height:1.75;">'
            'La <strong>Herramienta de Indagación Regenerativa</strong> de LivLin evalúa el potencial '
            'regenerativo de un espacio a través de múltiples dimensiones interconectadas. '
            'El diagnóstico se realiza mediante una visita presencial de una persona facilitadora '
            'certificada que observa, conversa y registra. '
            'A continuación se explica cómo se construyen los indicadores, qué mide cada uno '
            'y cómo se traducen a la escala de niveles. '
            'Toda la metodología se basa en Mason (2025) y en el modelo de la Flor de la Permacultura (Holmgren, 2002).'
            '</div>', unsafe_allow_html=True)

        with st.expander("🌸 ¿Qué es la Flor de la Permacultura?", expanded=False):
            st.markdown(
                'La **Flor de la Permacultura** (Holmgren, 2002) organiza la vida cotidiana '
                'en **7 dominios de acción regenerativa** (pétalos). Cada pétalo representa un ámbito '
                'donde las prácticas pueden transformar sistemas extractivos en regenerativos:\n')
            for i, p in enumerate(PETAL_ORDER):
                icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
                pinfo = PETAL_DESC.get(p, {})
                sub = pinfo.get("subtitulo", "")
                st.markdown(f"- **{icon} {p}** — {sub}")
            st.markdown(
                '\nPara cada pétalo se registran las **prácticas ya activas** (observadas) '
                'y las **prácticas con potencial concreto de realización** (potenciales). '
                'Solo se registra como potencial aquello que la facilitadora evalúa como '
                'razonablemente factible para ese espacio.\n\n'
                'El centro de la flor son los principios éticos: cuidado de la tierra, '
                'cuidado de las personas y distribución justa de los excedentes.')

        with st.expander("🌍 ¿Cómo se calcula el ERP (Estado Regenerativo Presente)?", expanded=False):
            st.markdown(
                '**ERP = 80% Flor de la Permacultura observada + 20% Sub-indicadores M2-6**\n\n'
                '**MFP observado (80%):** Se cuentan las prácticas actualmente activas en cada uno de los '
                '7 pétalos. El total se traduce a una escala 0–10 según esta tabla:\n\n'
                '| Prácticas observadas | Puntuación |\n|---|---|\n'
                '| 0 | 0/10 |\n| 1–2 | 2/10 |\n| 3–5 | 4/10 |\n'
                '| 6–9 | 6/10 |\n| 10–14 | 8/10 |\n| 15+ | 10/10 |\n\n'
                '**Sub-indicadores M2-6 (20%):** Datos ecológicos y sistémicos de los módulos de observación:')
            if cross:
                for name, info in cross.items():
                    st.markdown(f"  - **{info.get('icono','')} {name}:** {info['score']}/10 — _{info['fuente']}_")
                st.markdown("\n**Detalle de fórmulas y variables:**")
                for name, detail in CROSS_MODULE_DETAIL.items():
                    st.markdown(f"**{detail.get('icono','')} {name}** — `{detail['formula']}`")
                    for vn, vs in detail["variables"]:
                        st.caption(f"  • {vn}: {vs}")

        with st.expander("🌱 ¿Cómo se calcula el HRP (Horizonte Regenerativo Potencial)?", expanded=False):
            st.markdown(
                '**HRP = 100% Flor proyectada (observadas + potenciales)**\n\n'
                'El HRP suma todas las prácticas de la Flor: las ya activas más las identificadas '
                'como potenciales. Se aplica la misma tabla de puntuación que el ERP. '
                'No incluye sub-indicadores M2-6 porque la visión futura ya está contenida '
                'en las prácticas potenciales de cada pétalo.\n\n'
                'El HRP representa el techo alcanzable si se activan todas las prácticas '
                'potenciales identificadas en el diagnóstico.')

        with st.expander("🌀 ¿Qué es la Brecha?", expanded=False):
            st.markdown(
                '**Brecha = HRP − ERP**\n\n'
                'La brecha indica cuánto potencial hay por activar. No es negativa — una brecha '
                'grande significa mucho espacio para crecer. Una brecha pequeña indica que el '
                'espacio ya está cerca de su máximo potencial identificado.\n\n'
                f'En este diagnóstico, la brecha es de **{brecha} puntos**: {brecha_txt}')

        with st.expander("📊 Escala de niveles (0–10)", expanded=False):
            st.markdown(
                'Todos los indicadores se expresan en una escala 0–10 con 5 niveles narrativos:\n\n'
                '| Rango | Nivel | Significado |\n|---|---|---|\n'
                '| 0–2 | 🔴 Sin inicio | El camino regenerativo está por comenzar |\n'
                '| 2–4 | 🟠 Semilla | Primeras prácticas activas, la semilla germina |\n'
                '| 4–6 | 🟡 Brote | Prácticas en marcha, el espacio crece |\n'
                '| 6–8 | 🟢 Crecimiento | Prácticas consolidadas, regenera con fuerza |\n'
                '| 8–10 | 🌿 Abundancia | Referente vivo de regeneración |\n')

        with st.expander("🌿 ¿Qué son las 10 Dimensiones de análisis?", expanded=False):
            st.markdown(
                'Las 10 dimensiones ofrecen una lectura más granular del potencial regenerativo, '
                'combinando los 7 pétalos con los sub-indicadores ecológicos (M2-6):\n')
            for dim_name, dim_info in DIM_WHAT_MEASURES.items():
                if isinstance(dim_info, str):
                    dim_info = {"que_mide": dim_info, "icono": "📊", "fuentes": ""}
                st.markdown(
                    f"- **{dim_info.get('icono','📊')} {dim_name}:** "
                    f"{dim_info.get('que_mide','')} "
                    f"*(Fuentes: {dim_info.get('fuentes','')})*")

        with st.expander("🔵 Tao de la Regeneración — 5 dimensiones de sabiduría taoísta", expanded=False):
            st.markdown(
                'El **Tao de la Regeneración** complementa la Flor con una dimensión interior: '
                'la disposición interna del grupo para el cambio transformativo. '
                'Se evalúan 5 dimensiones desde la filosofía taoísta (escala 1–5 c/u):\n\n'
                '1. **Wu Wei** — Acción espontánea y oportuna; no-imposición de ritmos externos\n'
                '2. **Humildad y suficiencia** — Estar al servicio, detenerse a tiempo, sencillez\n'
                '3. **Compasión y no-juicio** — Inclusividad, verdad sobria, cuidado de todos\n'
                '4. **Fortalecer lo esencial** — Raíz, substancia, enfoque en lo que nutre vida\n'
                '5. **Retorno a la raíz** — Ciclos, memoria del lugar, regeneración natural\n\n'
                'El resultado se visualiza en un radar de 5 ejes. Total: 5–25 puntos.')

    st.markdown("---")
       

    # SECCION 9b -- GLOSARIO DE ACCIONES
    if _show("glosario"):
        st.markdown("#### 📘 Glosario de Acciones Regenerativas")
        st.markdown(
            '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:1rem;'
            'font-size:0.85rem;color:#2D6A4F;line-height:1.7;">'
            'Este glosario describe las <strong>208 acciones regenerativas</strong> incluidas en la '
            'Herramienta de Indagación Regenerativa, organizadas por los 7 petalos de la '
            'Flor de la Permacultura. Si encuentras una accion en tu informe que no conoces, '
            'aqui puedes saber de que se trata.</div>', unsafe_allow_html=True)

        try:
            from modules.regenerative_potential import _PETALOS_DATA
            from modules.regenerative_potential import PETAL_ICONS as _GLOSS_ICONS
            from utils.glosario import get_description
            for i, petalo in enumerate(_PETALOS_DATA):
                icon = _GLOSS_ICONS[i] if i < len(_GLOSS_ICONS) else ""
                with st.expander(f"{icon} {petalo['nombre']}", expanded=False):
                    if petalo.get("subtitulo"):
                        st.caption(petalo["subtitulo"])
                    for cat_key, actions in petalo["categorias"].items():
                        cat_name = cat_key.replace("_", " ").title()
                        st.markdown(f"**{cat_name}**")
                        for action in actions:
                            desc = get_description(action)
                            st.markdown(
                                f'<div style="padding:0.2rem 0 0.2rem 0.8rem;border-left:2px solid #A8D5B5;'
                                f'margin:0.15rem 0;font-size:0.82rem;">'
                                f'<strong style="color:#1B4332;">{action}</strong><br>'
                                f'<span style="color:#555;">{desc}</span></div>',
                                unsafe_allow_html=True)
        except Exception as e:
            st.caption(f"Glosario: {e}")
        st.markdown("---")

    if _show("biblio"):
        st.markdown("#### 📚 Bibliografía y Recursos")
        st.markdown('<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
            'Referencias utilizadas en la construcción del marco teórico y metodológico de LivLin.</div>', unsafe_allow_html=True)
        for auth, title, url in GLOBAL_REFS:
            st.markdown(f'<div style="padding:0.4rem 0;border-bottom:1px solid #E8F5E9;">'
                f'<span style="font-weight:700;color:#1B4332;">{auth}</span> — '
                f'<em style="color:#333;">{title}</em> '
                f'<a href="{url}" target="_blank" style="color:#1565C0;font-size:0.82rem;">↗ Acceder</a></div>', unsafe_allow_html=True)

    


    # ── Downloads (admin view, bottom of page) ────────────────────────
    if not readonly:
        st.markdown("---")
        st.markdown("### 💾 Descargar informes")
        dc1, dc2 = st.columns(2)
        with dc1:
            try:
                xlsx_bytes = generate_excel(data)
                st.download_button("📊 Descargar Excel", data=xlsx_bytes,
                    file_name=f"livlin_{nombre.replace(' ','_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True, key="dl_xlsx_admin")
            except Exception as e:
                st.error(f"Error Excel: {e}")
        with dc2:
            try:
                from utils.docx_generator import generate_docx
                docx_bytes = generate_docx(data)
                st.download_button("📝 Descargar Word", data=docx_bytes,
                    file_name=f"livlin_{nombre.replace(' ','_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True, key="dl_docx_admin")
            except Exception as e:
                st.error(f"Error Word: {e}")

    # ── Demo CTA at bottom ────────────────────────────────────────────
    if st.session_state.get("demo_mode", False):
        st.markdown("---")
        st.markdown(
            '<div style="background:linear-gradient(135deg,#D8F3DC,#E8F5E9);border-radius:14px;'
            'padding:1.5rem 2rem;margin:1rem 0;text-align:center;border:1px solid #A8D5B5;">'
            '<div style="font-size:1.1rem;font-weight:800;color:#1B4332;margin-bottom:0.5rem;">'
            '¿Quieres un diagnostico como este para tu espacio?</div>'
            '<div style="font-size:0.9rem;color:#2D6A4F;line-height:1.7;margin-bottom:0.8rem;">'
            'LivLin realiza diagnosticos regenerativos para hogares, organizaciones, '
            'escuelas y comunidades. Cada espacio tiene un potencial unico esperando ser activado.'
            '</div>'
            '<a href="https://www.livlin.cl" target="_blank" style="display:inline-block;'
            'background:#1B4332;color:white;padding:0.6rem 2rem;border-radius:8px;'
            'text-decoration:none;font-weight:700;font-size:0.9rem;">Contacta a LivLin</a>'
            '<div style="font-size:0.75rem;color:#40916C;margin-top:0.5rem;">'
            'www.livlin.cl · Potencial para una vida regenerativa</div>'
            '</div>', unsafe_allow_html=True)
