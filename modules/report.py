"""Módulo Informe Final v5.0 — LivLin Indagación Regenerativa.
Vista completa para cliente y admin. Solo lectura para clientes.
IPR dual (observado/potencial), toda la información del diagnóstico.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.data_manager import save_visit
from utils.scoring import (
    FLOWER_DOMAINS, PETAL_ORDER,
    compute_domain_scores, compute_domain_scores_total,
    compute_regenerative_score, compute_regenerative_score_potential,
    score_label, _score_to_level,
    compute_synthesis_potentials, compute_synthesis_potentials_obs,
    compute_cross_module_score,
    get_interp_text, get_petal_interp,
    IPR_METODOLOGIA, _ipr_obs_counts, _ipr_tot_counts,
)
from utils.report_generator import generate_excel


def _safe_float(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default


def _val(data, key, default="No registrado"):
    v = data.get(key)
    if v in [None, "", [], 0, 0.0]: return default
    return v


def _show_field(label: str, value, empty_msg="No registrado"):
    """Display a labeled field only if it has content."""
    if value in [None, "", [], 0, 0.0]:
        return
    st.markdown(
        f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
        f'<span style="font-size:0.75rem;color:#52B788;text-transform:uppercase;">{label}</span><br>'
        f'<span style="font-size:0.88rem;color:#1B4332;">{value}</span></div>',
        unsafe_allow_html=True)


def _card(label: str, value: str, bg: str = "#F0FFF4", fg: str = "#1B4332", border: str = "#52B788"):
    if not value or value == "No registrado":
        return
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.6rem 0.8rem;'
        f'margin-bottom:0.5rem;border-left:3px solid {border};">'
        f'<div style="font-size:0.72rem;color:{border};text-transform:uppercase;margin-bottom:0.2rem;">{label}</div>'
        f'<div style="font-size:0.88rem;color:{fg};line-height:1.5;">{value}</div></div>',
        unsafe_allow_html=True)


def _list_from_semicolon(text: str) -> list:
    """Split text by semicolons, return clean list."""
    if not text: return []
    return [item.strip() for item in text.split(";") if item.strip()]


def _render_sintesis_list(items_text: str, label: str, bg: str, fg: str):
    """Render semicolon-separated text as a clean list (no emojis)."""
    if not items_text: return
    items = _list_from_semicolon(items_text)
    if not items:
        st.markdown(f'<div style="background:{bg};border-radius:8px;padding:0.7rem;'
                    f'border-left:3px solid {fg};margin-bottom:0.5rem;">'
                    f'<div style="font-size:0.8rem;font-weight:700;color:{fg};">{label}</div>'
                    f'<div style="font-size:0.85rem;color:#333;margin-top:0.3rem;">{items_text}</div></div>',
                    unsafe_allow_html=True)
        return
    rows = "".join(
        f'<div style="padding:0.25rem 0;border-bottom:1px solid rgba(0,0,0,0.06);'
        f'font-size:0.85rem;color:#333;">{item}</div>'
        for item in items)
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.7rem;'
        f'border-left:3px solid {fg};margin-bottom:0.5rem;">'
        f'<div style="font-size:0.8rem;font-weight:700;color:{fg};margin-bottom:0.4rem;">{label}</div>'
        f'{rows}</div>',
        unsafe_allow_html=True)


def _dual_radar(domain_obs, domain_tot, height=400):
    """Dual radar chart: observed (dark) + potential (dashed). Escala 0-10."""
    labels = [f"{FLOWER_DOMAINS[p]['icon']} {p}" for p in PETAL_ORDER]
    r_obs = [domain_obs[p] for p in PETAL_ORDER] + [domain_obs[PETAL_ORDER[0]]]
    r_tot = [domain_tot[p] for p in PETAL_ORDER] + [domain_tot[PETAL_ORDER[0]]]
    theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_tot, theta=theta, name="Con potencial adicional",
        fill="toself", fillcolor="rgba(82,183,136,0.10)",
        line=dict(color="#52B788", width=2, dash="dash"),
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_obs, theta=theta, name="Estado actual",
        fill="toself", fillcolor="rgba(27,67,50,0.22)",
        line=dict(color="#1B4332", width=2.5),
        marker=dict(size=7, color="#1B4332"),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(240,255,244,0.4)",
            radialaxis=dict(
                visible=True, range=[0, 10],
                tickvals=[2, 4, 6, 8, 10],
                tickfont=dict(size=9, color="#2D6A4F"),
                gridcolor="rgba(45,106,79,0.2)"),
            angularaxis=dict(tickfont=dict(size=10, color="#1B4332")),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=50, b=30),
        height=height,
    )
    return fig


def render():
    from utils.data_manager import get_visit
    visit_id = st.session_state.get("visit_data", {}).get("id")
    if visit_id:
        fresh = get_visit(visit_id)
        if fresh:
            st.session_state.visit_data = fresh
    data = st.session_state.get("visit_data", {})

    # Check read-only
    user = st.session_state.get("current_user", {})
    readonly = user.get("role", "user") != "admin"

    if not data.get("id"):
        st.warning("Carga o crea un diagnóstico primero.")
        return

    # ── Compute scores ────────────────────────────────────────────────────
    domain_obs   = compute_domain_scores(data)
    domain_tot   = compute_domain_scores_total(data)
    regen_obs    = compute_regenerative_score(data)
    regen_pot    = compute_regenerative_score_potential(data)
    label_obs, color_obs = score_label(regen_obs)
    label_pot, color_pot = score_label(regen_pot)
    potenciales_pot = compute_synthesis_potentials(data)
    potenciales_obs = compute_synthesis_potentials_obs(data)
    cross = compute_cross_module_score(data)
    ipr_obs_counts = _ipr_obs_counts(data)
    ipr_tot_counts = _ipr_tot_counts(data)

    nombre  = data.get("proyecto_nombre", "Diagnóstico")
    cliente = data.get("proyecto_cliente", "—")
    ciudad  = data.get("proyecto_ciudad",  "—")
    fecha   = data.get("proyecto_fecha",   "—")

    # ── Header ────────────────────────────────────────────────────────────
    st.markdown("## Informe Final del Diagnóstico Regenerativo")
    st.markdown('<p class="module-subtitle">Visión completa del diagnóstico · LivLin v5.0</p>',
                unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#F0FFF4,#D8F3DC);
                    border:2px solid #52B788;border-radius:14px;
                    padding:1.2rem 1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:1rem;">
                <div>
                    <div style="font-size:0.72rem;color:#52B788;
                                text-transform:uppercase;letter-spacing:0.1em;">
                        Diagnóstico Regenerativo · LivLin v5.0</div>
                    <div style="font-size:1.5rem;font-weight:800;
                                color:#1B4332;margin:0.2rem 0;">{nombre}</div>
                    <div style="color:#555;font-size:0.88rem;">
                        {cliente} &nbsp;·&nbsp; {ciudad} &nbsp;·&nbsp; {fecha}</div>
                </div>
                <div style="display:flex;gap:0.8rem;flex-wrap:wrap;">
                    <div style="text-align:center;background:white;border-radius:12px;
                                padding:0.8rem 1.2rem;border:2px solid #D8F3DC;min-width:120px;">
                        <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">Estado actual</div>
                        <div style="font-size:2.8rem;font-weight:900;color:#1B4332;line-height:1;">{regen_obs}</div>
                        <div style="color:#52B788;font-size:0.75rem;">/10</div>
                        <div style="font-size:0.75rem;color:{color_obs};font-weight:600;margin-top:0.2rem;">{label_obs}</div>
                    </div>
                    <div style="text-align:center;background:white;border-radius:12px;
                                padding:0.8rem 1.2rem;border:2px dashed #52B788;min-width:120px;">
                        <div style="font-size:0.65rem;color:#888;text-transform:uppercase;">Con potencial</div>
                        <div style="font-size:2.8rem;font-weight:900;color:#52B788;line-height:1;">{regen_pot}</div>
                        <div style="color:#52B788;font-size:0.75rem;">/10</div>
                        <div style="font-size:0.75rem;color:{color_pot};font-weight:600;margin-top:0.2rem;">{label_pot}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # IPR methodology explanation (collapsible)
    with st.expander("Como se calcula el Indice de Potencial Regenerativo (IPR)", expanded=False):
        st.markdown(f'<div style="background:#F0FFF4;border-radius:8px;padding:1rem;'
                    f'font-size:0.85rem;color:#1B4332;white-space:pre-line;">{IPR_METODOLOGIA}</div>',
                    unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 1 — DATOS DEL PROYECTO
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 1. Datos del Proyecto")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Información general del espacio diagnosticado y del grupo habitante que participa en el proceso.</div>',
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        _show_field("Nombre del proyecto", data.get("proyecto_nombre"))
        _show_field("Grupo / familia / organización", data.get("proyecto_cliente"))
        _show_field("Dirección", data.get("proyecto_direccion"))
        _show_field("Ciudad", data.get("proyecto_ciudad"))
        _show_field("País", data.get("proyecto_pais"))
        _show_field("Fecha del diagnóstico", data.get("proyecto_fecha"))
    with c2:
        _show_field("Tipo de espacio", data.get("proyecto_tipo_espacio"))
        _show_field("Área total (m²)", data.get("proyecto_area") or data.get("proyecto_superficie"))
        _show_field("Composición del grupo", data.get("proyecto_composicion"))
        adultos = data.get("proyecto_n_adultos")
        ninos   = data.get("proyecto_n_ninos")
        if adultos or ninos:
            _show_field("Habitantes", f"{adultos or 0} adultos, {ninos or 0} niños/as")
        _show_field("Descripción del grupo", data.get("proyecto_habitantes"))
    if data.get("geo_display"):
        _show_field("Ubicación geolocalizada", data.get("geo_display"))

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 2 — TAO DE LA REGENERACIÓN
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 2. Tao de la Regeneración")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'El Tao de la Regeneración explora la dimensión interior del proceso: la motivación profunda del grupo, '
        'su relación con la naturaleza, y su conciencia sobre las crisis planetarias. '
        'Es el punto de partida filosófico y espiritual del diagnóstico.</div>',
        unsafe_allow_html=True)

    # Solo muestra campos con información
    tao_fields = [
        ("tao_sensacion", "Sensación al estar en el espacio"),
        ("tao_deseado", "Lo que desean para este espacio"),
        ("tao_no_deseado", "Lo que no desean para este espacio"),
        ("tao_llama", "Lo que los llama hacia la regeneración"),
        ("tao_ritmo", "Ritmo de vida actual"),
        ("tao_tiempo_libre", "Tiempo disponible para el espacio"),
        ("tao_actividades", "Actividades que los nutren en el espacio"),
        ("tao_sencillez", "Relación con la sencillez"),
        ("tao_consumo", "Relación con el consumo material"),
        ("tao_descanso_creativo", "Descanso creativo"),
        ("tao_naturaleza_ext", "Cómo ven su relación con la naturaleza"),
        ("tao_cuerpo_tierra", "Cuerpo y tierra"),
        ("tao_agua_virtud", "El agua como virtud"),
        ("tao_bienestar", "Nivel de bienestar general"),
        ("tao_naturaleza_rel", "Relación con la naturaleza"),
        ("tao_aprender", "Lo que desean aprender"),
        ("tao_justicia", "Reflexión sobre justicia ambiental"),
        ("tao_palabra_esencial", "Palabra esencial del proceso"),
    ]
    c1, c2 = st.columns(2)
    for i, (key, label) in enumerate(tao_fields):
        with (c1 if i % 2 == 0 else c2):
            _card(label, str(data.get(key, "")) if data.get(key) else "", "#F0FFF4", "#1B4332", "#40916C")

    # Crisis planetaria
    tao_crisis = [
        ("tao_cc_conciencia", "Conciencia sobre el cambio climático"),
        ("tao_cc_impacto", "Impacto percibido del cambio climático"),
        ("tao_cc_respuesta", "Respuesta al cambio climático"),
        ("tao_bio_conciencia", "Conciencia sobre pérdida de biodiversidad"),
        ("tao_bio_local", "Biodiversidad local observada"),
        ("tao_bio_accion", "Acciones de apoyo a la biodiversidad"),
        ("tao_cont_conciencia", "Conciencia sobre contaminación"),
        ("tao_cont_respuesta", "Respuesta frente a la contaminación"),
    ]
    any_crisis = any(data.get(k) for k, _ in tao_crisis)
    if any_crisis:
        st.markdown("**Conciencia sobre las crisis planetarias**")
        c1, c2 = st.columns(2)
        for i, (key, label) in enumerate(tao_crisis):
            with (c1 if i % 2 == 0 else c2):
                _card(label, str(data.get(key, "")) if data.get(key) else "", "#FFFDE7", "#1B4332", "#A67C00")

    tao_tipos = data.get("tao_cont_tipos", [])
    if isinstance(tao_tipos, list) and tao_tipos:
        st.markdown(f'<div style="font-size:0.82rem;color:#555;padding:0.3rem 0;">'
                    f'Tipos de contaminación identificados: {", ".join(tao_tipos)}</div>', unsafe_allow_html=True)

    if data.get("tao_notas"):
        _card("Notas del facilitador", data["tao_notas"], "#FDF6EC", "#333", "#A67C00")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 3 — OBSERVACIÓN ECOLÓGICA (M2-3)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 3. Observación Ecológica y Potencial de Cultivo")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Registro de las características físicas y ecológicas del espacio: suelo, vegetación, flujos naturales '
        '(sol, viento, agua) y potencial productivo. Sigue el principio de Holmgren: observar e interactuar '
        'antes de diseñar.</div>',
        unsafe_allow_html=True)

    # Superficie y cultivo — siempre mostrar
    area_tot  = _safe_float(data.get("proyecto_area") or data.get("proyecto_superficie"))
    area_cult = _safe_float(data.get("cultivo_m2"))
    pct_cult  = round(area_cult / area_tot * 100) if area_tot > 0 and area_cult > 0 else 0

    m1, m2, m3 = st.columns(3)
    def _metric_card(col, value, label, show_zero=False):
        display = str(int(value)) if value and (value > 0 or show_zero) else "No registrado"
        with col:
            st.markdown(
                f'<div style="background:white;border-radius:8px;padding:0.7rem;'
                f'box-shadow:0 2px 8px rgba(27,67,50,0.07);border-left:3px solid #52B788;">'
                f'<div style="font-size:1.4rem;font-weight:800;color:#1B4332;">{display}</div>'
                f'<div style="font-size:0.7rem;color:#52B788;text-transform:uppercase;">{label}</div></div>',
                unsafe_allow_html=True)

    _metric_card(m1, area_tot, "m² totales")
    _metric_card(m2, area_cult, "m² cultivables")
    with m3:
        pct_display = f"{pct_cult}%" if pct_cult > 0 else "No registrado"
        st.markdown(
            f'<div style="background:white;border-radius:8px;padding:0.7rem;'
            f'box-shadow:0 2px 8px rgba(27,67,50,0.07);border-left:3px solid #2D6A4F;">'
            f'<div style="font-size:1.4rem;font-weight:800;color:#1B4332;">{pct_display}</div>'
            f'<div style="font-size:0.7rem;color:#52B788;text-transform:uppercase;">% cultivable</div></div>',
            unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Suelo**")
        for k, l in [("suelo_tipo","Tipo de suelo"),("suelo_compactacion","Compactación"),
                     ("suelo_materia_organica","Materia orgánica"),("suelo_drenaje","Drenaje"),
                     ("suelo_color","Color"),("suelo_olor","Olor"),("suelo_notas","Notas del suelo")]:
            _card(l, data.get(k,""), "#F0FFF4","#1B4332","#40916C")

        st.markdown("**Vegetación**")
        veg_tipos = data.get("veg_tipos",[])
        if isinstance(veg_tipos, list) and veg_tipos:
            st.markdown(f'<div style="font-size:0.85rem;color:#1B4332;padding:0.3rem 0;">Tipos: {", ".join(veg_tipos)}</div>', unsafe_allow_html=True)
        for k, l in [("veg_especies","Especies identificadas"),("veg_invasoras","Invasoras o problemáticas"),("eco_notas","Notas ecológicas")]:
            _card(l, data.get(k,""), "#F0FFF4","#1B4332","#40916C")

    with c2:
        st.markdown("**Flujos naturales**")
        for k, l in [("sol_horas","Horas de sol (promedio/día)"),("sol_horas_invierno","Horas de sol invierno"),
                     ("sol_horas_verano","Horas de sol verano"),("sol_orientacion","Orientación"),
                     ("sol_zonas_max","Zonas más soleadas"),("sol_sombra_perm","Zonas de sombra permanente"),
                     ("viento_direccion","Dirección del viento"),("viento_protegidas","Zonas protegidas del viento"),
                     ("agua_flujo_lluvia","Flujo del agua de lluvia"),("agua_acumulacion","Acumulación de agua"),
                     ("flujos_notas","Notas de flujos")]:
            _card(l, str(data.get(k,"")) if data.get(k) else "", "#E3F2FD","#1B4332","#1565C0")

        st.markdown("**Cultivo**")
        for k, l in [("cultivo_produce_hoy","Produce alimentos hoy"),("cultivo_interes","Interés en producir"),
                     ("cultivo_frutales","Espacio para frutales"),("cultivo_verticales","Espacio para verticales"),
                     ("cultivo_plantas_actuales","Plantas actuales"),("cultivo_notas","Notas de cultivo")]:
            _card(l, str(data.get(k,"")) if data.get(k) else "", "#F0FFF4","#1B4332","#40916C")

    # Fauna
    fauna_fields = [("fauna_lombrices","Lombrices / organismos del suelo"),("fauna_plagas","Plagas observadas"),("fauna_aves_especies","Aves identificadas")]
    if any(data.get(k) for k,_ in fauna_fields):
        st.markdown("**Fauna**")
        cf1, cf2, cf3 = st.columns(3)
        for col, (k, l) in zip([cf1,cf2,cf3], fauna_fields):
            with col:
                _card(l, str(data.get(k,"")) if data.get(k) else "", "#F0FFF4","#1B4332","#40916C")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 4 — SISTEMAS (M4-6)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 4. Contexto, Agua, Energía y Materiales")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Análisis de los flujos vitales del espacio: contexto urbano y comunitario, gestión del agua, '
        'energía y manejo de materiales. Identificar y cerrar estos ciclos es la base de la autonomía regenerativa.</div>',
        unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Contexto urbano**")
        _card("Percepción del entorno verde", data.get("ctx_ind_verde",""), "#F0FFF4","#1B4332","#40916C")
        parques = data.get("ctx_parques_lista",[])
        if isinstance(parques, list) and parques:
            pq_text = "; ".join(f"{p.get('nombre','')} ({p.get('dist','')}m)" for p in parques)
            _card("Parques y áreas verdes cercanas", pq_text, "#F0FFF4","#1B4332","#40916C")
        _card("Cuenca hidrográfica", data.get("ctx_cuenca",""), "#F0FFF4","#1B4332","#40916C")
        _card("Relación con vecinos", str(data.get("ctx_vecinos","")) if data.get("ctx_vecinos") else "", "#F0FFF4","#1B4332","#40916C")
        _card("Participación en iniciativas barriales", str(data.get("ctx_participacion","")) if data.get("ctx_participacion") else "", "#F0FFF4","#1B4332","#40916C")
        actores = data.get("ctx_actores",[])
        if isinstance(actores, list) and actores:
            act_text = "; ".join(f"{a.get('nombre','')} ({a.get('tipo','')})" for a in actores)
            _card("Actores del territorio", act_text, "#F0FFF4","#1B4332","#40916C")

        st.markdown("**Materiales y residuos**")
        _card("Notas de materiales", data.get("mat_notas",""), "#F0FFF4","#1B4332","#40916C")

    with c2:
        st.markdown("**Gestión del agua**")
        _card("Percepción del agua", data.get("agua_ind_general",""), "#E3F2FD","#1B4332","#1565C0")
        for k, l in [("agua_fuente","Fuente de agua"),("agua_captacion_lluvia","Captación lluvia"),
                     ("agua_grises","Reutilización de grises"),("agua_riego_sistema","Sistema de riego"),
                     ("agua_fugas","Fugas o pérdidas")]:
            _card(l, str(data.get(k,"")) if data.get(k) else "", "#E3F2FD","#1B4332","#1565C0")
        prec = _safe_float(data.get("agua_prec_anual"))
        techo = _safe_float(data.get("agua_techo_m2"))
        cap = round(prec * techo * 0.8) if prec > 0 and techo > 0 else 0
        if cap > 0:
            _card("Potencial de captación lluvia (L/año)", f"{cap:,}", "#E3F2FD","#1B4332","#1565C0")

        st.markdown("**Energía**")
        _card("Percepción del uso energético", data.get("ene_ind_general",""), "#FFF8E1","#1B4332","#F57C00")
        for k, l in [("ene_fuente","Fuente de energía"),("ene_led","Iluminación LED"),("ene_solar_interes","Interés en solar")]:
            _card(l, str(data.get(k,"")) if data.get(k) else "", "#FFF8E1","#1B4332","#F57C00")
        kwh = _safe_float(data.get("ene_kwh_dia_calc"))
        if kwh > 0:
            _card("Consumo estimado (kWh/día)", f"{kwh}", "#FFF8E1","#1B4332","#F57C00")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 5 — FLOR DE LA PERMACULTURA + IPR DUAL
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 5. Flor de la Permacultura — Indice de Potencial Regenerativo")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Los 7 pétalos de la Flor de la Permacultura (Holmgren, 2002) representan los ámbitos que deben '
        'transformarse para transitar hacia una cultura sostenible. El radar muestra dos perspectivas: '
        'el estado actual (prácticas observadas hoy) y el potencial proyectado (incorporando prácticas adicionales '
        'identificadas por el facilitador). La escala es de 0 a 10.</div>',
        unsafe_allow_html=True)

    # Botones de perspectiva de interpretación
    if "ipr_perspective" not in st.session_state:
        st.session_state.ipr_perspective = "actual"

    col_btn1, col_btn2, _ = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("Estado actual",
                     type="primary" if st.session_state.ipr_perspective == "actual" else "secondary",
                     use_container_width=True, key="btn_ipr_actual"):
            st.session_state.ipr_perspective = "actual"
            st.rerun()
    with col_btn2:
        if st.button("Potencial proyectado",
                     type="primary" if st.session_state.ipr_perspective == "potencial" else "secondary",
                     use_container_width=True, key="btn_ipr_pot"):
            st.session_state.ipr_perspective = "potencial"
            st.rerun()

    perspective = st.session_state.ipr_perspective
    active_scores = domain_obs if perspective == "actual" else domain_tot

    col_radar, col_ipr = st.columns([1.3, 0.7])
    with col_radar:
        fig = _dual_radar(domain_obs, domain_tot)
        st.plotly_chart(fig, use_container_width=True, key="radar_informe")

    with col_ipr:
        score_actual = regen_obs if perspective == "actual" else regen_pot
        label_curr, color_curr = score_label(score_actual)
        st.markdown(
            f'<div style="background:white;border:2px solid #D8F3DC;border-radius:10px;'
            f'padding:0.8rem;text-align:center;margin-bottom:0.8rem;">'
            f'<div style="font-size:0.68rem;color:#888;text-transform:uppercase;">'
            f'IPR {"actual" if perspective=="actual" else "proyectado"}</div>'
            f'<div style="font-size:3rem;font-weight:900;color:#1B4332;line-height:1;">{score_actual}</div>'
            f'<div style="color:#52B788;font-size:0.8rem;">/10</div>'
            f'<div style="font-size:0.78rem;color:{color_curr};font-weight:600;margin-top:0.2rem;">{label_curr}</div></div>',
            unsafe_allow_html=True)

        st.markdown("**Detalle por pétalo:**")
        for i, p in enumerate(PETAL_ORDER):
            n_o  = ipr_obs_counts[i]
            n_t  = ipr_tot_counts[i]
            s_o  = domain_obs[p]
            s_t  = domain_tot[p]
            icon = FLOWER_DOMAINS[p]["icon"]
            col  = FLOWER_DOMAINS[p]["color"]
            s_show = s_o if perspective == "actual" else s_t
            lv, _ = _score_to_level(s_show)
            pct = int(s_show / 10 * 100)
            delta = f"+{n_t-n_o}" if n_t > n_o else ""
            st.markdown(
                f'<div style="padding:4px 0;border-bottom:1px solid #D8F3DC;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;">'
                f'<span style="color:#1B4332;">{icon} {p[:26]}</span>'
                f'<span style="background:{col};color:white;border-radius:4px;padding:1px 6px;font-size:0.7rem;">'
                f'{s_show:.0f} {"obs" if perspective=="actual" else "pot"} {delta}</span>'
                f'</div>'
                f'<div style="background:#E8F5E9;height:5px;border-radius:3px;margin-top:2px;">'
                f'<div style="background:{col};width:{min(pct,100)}%;height:5px;border-radius:3px;"></div></div>'
                f'</div>',
                unsafe_allow_html=True)

    # Interpretaciones por pétalo
    st.markdown("**Interpretación por pétalo:**")
    for i, p in enumerate(PETAL_ORDER):
        s_o = domain_obs[p]
        s_t = domain_tot[p]
        icon = FLOWER_DOMAINS[p]["icon"]
        interp_actual = get_petal_interp(p, s_o, "actual")
        interp_pot    = get_petal_interp(p, s_t, "potencial")
        with st.expander(f"{icon} {p}", expanded=False):
            col_a, col_p = st.columns(2)
            with col_a:
                st.markdown(
                    f'<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem;border-left:3px solid #1B4332;">'
                    f'<div style="font-size:0.72rem;font-weight:700;color:#1B4332;margin-bottom:0.3rem;">Estado actual · {s_o:.0f}/10</div>'
                    f'<div style="font-size:0.85rem;color:#333;">{interp_actual}</div>'
                    f'</div>',
                    unsafe_allow_html=True)
                # Prácticas observadas
                obs_data = data.get(f"petalo_{i}_obs", {})
                obs_list = [a for v in obs_data.values() if isinstance(v,list) for a in v]
                obs_list += data.get(f"petalo_{i}_otros_obs", [])
                if obs_list:
                    st.markdown('<div style="font-size:0.75rem;color:#2D6A4F;margin-top:0.4rem;font-weight:600;">Prácticas observadas:</div>', unsafe_allow_html=True)
                    for a in obs_list:
                        st.markdown(f'<div style="font-size:0.8rem;color:#333;padding:0.1rem 0 0.1rem 0.5rem;">— {a}</div>', unsafe_allow_html=True)
            with col_p:
                st.markdown(
                    f'<div style="background:#FFFDE7;border-radius:8px;padding:0.7rem;border-left:3px dashed #52B788;">'
                    f'<div style="font-size:0.72rem;font-weight:700;color:#2D6A4F;margin-bottom:0.3rem;">Potencial proyectado · {s_t:.0f}/10</div>'
                    f'<div style="font-size:0.85rem;color:#333;">{interp_pot}</div>'
                    f'</div>',
                    unsafe_allow_html=True)
                # Prácticas potenciales
                new_data = data.get(f"petalo_{i}_pot_new", {})
                new_list = [a for v in new_data.values() if isinstance(v,list) for a in v]
                new_list += data.get(f"petalo_{i}_otros_new", [])
                if new_list:
                    st.markdown('<div style="font-size:0.75rem;color:#52B788;margin-top:0.4rem;font-weight:600;">Prácticas potenciales identificadas:</div>', unsafe_allow_html=True)
                    for a in new_list:
                        st.markdown(f'<div style="font-size:0.8rem;color:#333;padding:0.1rem 0 0.1rem 0.5rem;">— {a}</div>', unsafe_allow_html=True)
            if data.get(f"petalo_{i}_notas"):
                st.markdown(f'<div style="font-size:0.8rem;color:#666;margin-top:0.4rem;font-style:italic;">Notas: {data[f"petalo_{i}_notas"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 6 — POTENCIALES DEL SITIO + SUB-INDICADORES
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 6. Potenciales del Sitio")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Ocho dimensiones de potencial regenerativo derivadas de los 7 pétalos del Modelo Flor de la Permacultura, '
        'mostradas en perspectiva dual. Los sub-indicadores integran además información de los módulos 2 a 6.</div>',
        unsafe_allow_html=True)

    # Botones perspectiva potenciales
    if "pot_perspective" not in st.session_state:
        st.session_state.pot_perspective = "actual"

    pb1, pb2, _ = st.columns([1, 1, 3])
    with pb1:
        if st.button("Estado actual",
                     type="primary" if st.session_state.pot_perspective == "actual" else "secondary",
                     use_container_width=True, key="btn_pot_actual"):
            st.session_state.pot_perspective = "actual"
            st.rerun()
    with pb2:
        if st.button("Potencial proyectado",
                     type="primary" if st.session_state.pot_perspective == "potencial" else "secondary",
                     use_container_width=True, key="btn_pot_pot"):
            st.session_state.pot_perspective = "potencial"
            st.rerun()

    pot_persp = st.session_state.pot_perspective
    pot_show  = potenciales_obs if pot_persp == "actual" else potenciales_pot

    col_bar, col_cross = st.columns([1.2, 0.8])
    with col_bar:
        if any(v > 0 for v in pot_show.values()):
            fig2 = px.bar(
                x=list(pot_show.values()),
                y=list(pot_show.keys()),
                orientation="h",
                color=list(pot_show.values()),
                color_continuous_scale=["#D8F3DC","#52B788","#2D6A4F","#1B4332"],
                range_color=[0, 10],
                text=[f"{v:.1f}" for v in pot_show.values()],
            )
            fig2.update_traces(textposition="outside", textfont_size=12)
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(240,255,244,0.3)",
                showlegend=False, coloraxis_showscale=False,
                xaxis=dict(range=[0, 12], tickfont=dict(size=10)),
                yaxis=dict(tickfont=dict(size=11)),
                margin=dict(l=10, r=40, t=10, b=10),
                height=320,
            )
            st.plotly_chart(fig2, use_container_width=True, key=f"bar_pot_{pot_persp}")
        else:
            st.info("Completa el Módulo 7 para ver los potenciales.")

        # Interpretaciones de dimensiones
        for dim, val in pot_show.items():
            interp = get_interp_text(dim, val, pot_persp)
            if interp:
                lv, col_lv = _score_to_level(val)
                st.markdown(
                    f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
                    f'<span style="font-size:0.72rem;font-weight:700;color:{col_lv};">{dim} · {val:.0f}/10 · {lv}</span><br>'
                    f'<span style="font-size:0.82rem;color:#333;">{interp}</span></div>',
                    unsafe_allow_html=True)

    with col_cross:
        # Métricas del sitio
        cap_lluvia = round(_safe_float(data.get("agua_prec_anual")) * _safe_float(data.get("agua_techo_m2")) * 0.8)
        metrics = [
            (int(area_tot),  "m² totales",     "#52B788"),
            (int(area_cult), "m² cultivables", "#40916C"),
            (pct_cult,       "% cultivable",   "#2D6A4F", True),
            (cap_lluvia,     "L/año captables", "#1B4332"),
        ]
        for m in metrics:
            val_m  = m[0]
            lab_m  = m[1]
            col_m  = m[2]
            is_pct = len(m) > 3
            disp   = f"{val_m}%" if is_pct else (f"{val_m:,}" if val_m > 0 else "No registrado")
            st.markdown(
                f'<div style="background:white;border-radius:8px;padding:0.7rem;'
                f'box-shadow:0 2px 8px rgba(27,67,50,0.07);border-left:3px solid {col_m};margin-bottom:0.5rem;">'
                f'<div style="font-size:1.4rem;font-weight:800;color:#1B4332;">{disp}</div>'
                f'<div style="font-size:0.7rem;color:#52B788;text-transform:uppercase;">{lab_m}</div></div>',
                unsafe_allow_html=True)

        # Sub-indicadores módulos 2-6
        if cross:
            st.markdown("**Sub-indicadores (M2-6):**")
            for name, info in cross.items():
                s = info["score"]
                lv, cl = _score_to_level(s)
                st.markdown(
                    f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:0.78rem;">'
                    f'<span style="color:#1B4332;">{name}</span>'
                    f'<span style="background:{cl};color:white;border-radius:4px;padding:1px 5px;font-size:0.7rem;">{s}/10</span>'
                    f'</div>'
                    f'<div style="font-size:0.7rem;color:#666;">{info["fuente"]}</div></div>',
                    unsafe_allow_html=True)

        destacadas = data.get("pot_practicas_destacadas","")
        if destacadas:
            st.markdown("<br>", unsafe_allow_html=True)
            _card("Prácticas más destacadas del espacio", destacadas, "#F0FFF4","#1B4332","#52B788")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 7 — SÍNTESIS DEL DIAGNÓSTICO
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 7. Sintesis del Diagnóstico")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'La síntesis narrativa integra los hallazgos del diagnóstico en cuatro dimensiones clave: '
        'fortalezas del espacio, oportunidades de mejora, desafíos a enfrentar y primeros pasos concretos. '
        'Cada dimensión se presenta como lista de ítems separados por punto y coma en el proceso de registro.</div>',
        unsafe_allow_html=True)

    s_items = [
        ("sint_fortalezas",    "Fortalezas",         "#D8F3DC", "#1B4332"),
        ("sint_oportunidades", "Oportunidades",      "#E3F2FD", "#1565C0"),
        ("sint_limitaciones",  "Desafios",           "#FFF3E0", "#E65100"),
        ("sint_quick_wins",    "Primeros pasos",      "#F3E5F5", "#6A1B9A"),
    ]
    c1s, c2s = st.columns(2)
    for i, (key, label, bg, fg) in enumerate(s_items):
        with (c1s if i % 2 == 0 else c2s):
            content = data.get(key, "")
            if content:
                _render_sintesis_list(content, label, bg, fg)
            else:
                st.markdown(
                    f'<div style="background:{bg};border-radius:8px;padding:0.7rem;'
                    f'border-left:3px solid {fg};margin-bottom:0.5rem;">'
                    f'<div style="font-size:0.8rem;font-weight:700;color:{fg};">{label}</div>'
                    f'<div style="font-size:0.82rem;color:#999;font-style:italic;">Sin información registrada</div></div>',
                    unsafe_allow_html=True)

    obs = data.get("sint_observaciones","")
    if obs:
        _card("Observaciones del facilitador", obs, "#FDF6EC","#333","#A67C00")

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 8 — PLAN DE ACCIÓN
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 8. Plan de Accion")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'La hoja de ruta regenerativa organiza las acciones en tres horizontes temporales: '
        'acciones inmediatas (0-3 meses), estacionales (3-12 meses) y estructurales (1-5 años). '
        'Cada acción tiene un estado de avance asociado.</div>',
        unsafe_allow_html=True)

    fases = [
        ("plan_inmediatas",    "Inmediatas (0-3 meses)",   "#52B788"),
        ("plan_estacionales",  "Estacionales (3-12 meses)","#2D6A4F"),
        ("plan_estructurales", "Estructurales (1-5 años)", "#1B4332"),
    ]
    cols_p = st.columns(3)
    for i, (key, label, color) in enumerate(fases):
        acciones = data.get(key, [])
        with cols_p[i]:
            header = (f'<div style="background:rgba(82,183,136,0.07);'
                      f'border-radius:10px;padding:0.8rem;border-top:3px solid {color};">'
                      f'<div style="font-weight:700;color:{color};margin-bottom:0.6rem;font-size:0.88rem;">{label}</div>')
            if isinstance(acciones, list) and acciones:
                rows = ""
                for a in acciones:
                    estado = a.get("estado","") if isinstance(a,dict) else ""
                    titulo = a.get("titulo","") if isinstance(a,dict) else str(a)
                    rows += (f'<div style="padding:0.3rem 0;border-bottom:1px solid rgba(82,183,136,0.2);'
                             f'font-size:0.82rem;color:#333;">{estado} {titulo[:80]}</div>')
                st.markdown(header + rows + "</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    header + '<div style="color:#999;font-size:0.82rem;font-style:italic;">Sin acciones registradas</div></div>',
                    unsafe_allow_html=True)

    st.markdown("---")

    # ══════════════════════════════════════════════════════════════════════
    # SECCIÓN 9 — EXPORTAR
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("### 9. Descargar Informe")
    st.markdown(
        '<div style="background:#F0FFF4;border-radius:8px;padding:0.7rem 1rem;'
        'margin-bottom:0.8rem;font-size:0.85rem;color:#2D6A4F;">'
        'Descarga el informe completo en formato Excel (.xlsx) con todas las secciones del diagnóstico, '
        'o en Word (.docx) con texto formateado, gráficos e imágenes. El informe incluye toda la '
        'información registrada con explicaciones de contexto y las interpretaciones del IPR.</div>',
        unsafe_allow_html=True)

    _, cdl, _ = st.columns([1, 2, 1])
    with cdl:
        if not data.get("proyecto_nombre"):
            st.warning("Completa al menos el Módulo 1 antes de exportar.")
        else:
            safe_n = data.get("proyecto_nombre","Diagnostico").replace(" ","_")

            facilitador = st.text_input(
                "Nombre del facilitador",
                value=data.get("proyecto_facilitador",""),
                placeholder="Nombre completo del facilitador",
                key="facilitador_dl")
            if facilitador:
                data["proyecto_facilitador"] = facilitador

            fecha_emision = st.date_input("Fecha de emisión", key="fecha_emision_dl")
            if fecha_emision:
                data["informe_fecha_emision"] = str(fecha_emision)

            st.markdown("---")
            col_xl, col_wd = st.columns(2)
            with col_xl:
                try:
                    xlsx_bytes = generate_excel(data)
                    st.download_button(
                        "Descargar Excel (.xlsx)", data=xlsx_bytes,
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
                        "Descargar Word (.docx)", data=docx_bytes,
                        file_name=f"LivLin_IR_{safe_n}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                except Exception as e:
                    st.caption(f"Word: {e}")

            st.markdown(
                '<div style="margin-top:0.8rem;background:#F0FFF4;border-radius:8px;'
                'padding:0.8rem;font-size:0.82rem;color:#1B4332;">'
                'Este diagnóstico es el primer paso de un proceso mayor. Con él tienes claridad sobre '
                'dónde está el potencial regenerativo de tu espacio y qué prácticas pueden transformarlo. '
                'Para las transformaciones más profundas, el equipo de LivLin puede acompañarte con servicios '
                'especializados de diseño, implementación y seguimiento. '
                '<a href="https://www.livlin.cl" target="_blank">www.livlin.cl</a></div>',
                unsafe_allow_html=True)
