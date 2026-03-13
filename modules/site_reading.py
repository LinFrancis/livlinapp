"""Módulo 2–3 — Observación Ecológica + Flujos + Cultivo (v6) — clickable tab_nav."""
import math
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status, tab_header, tab_nav_bottom, get_active_tab

NO_SOIL_TYPES  = ["Departamento con terraza","Departamento sin terraza","Balcón","Terraza comunitaria"]
PARTIAL_SOIL   = ["Casa con patio/jardín","Patio trasero","Comunidad / copropiedad",
                  "Escuela / jardín infantil","Espacio público","Centro comunitario"]
TABS = ["🌍 Suelo y Vegetación", "☀️ Flujos Naturales", "🥦 Potencial de Cultivo"]
MOD  = "m23"


def render():
    st.markdown("## 🔬 Módulos 2–3 — Observación Ecológica + Flujos + Cultivo")
    st.markdown('<p class="module-subtitle">Registro de las características del espacio, '
                'flujos naturales y potencial productivo.</p>', unsafe_allow_html=True)
    data = st.session_state.visit_data

    # ── Estado del módulo ─────────────────────────────────────────────────
    st.markdown("**Estado de este módulo:**")
    _mod_status = render_module_status(data, "mod_sitio")
    if not is_module_active(_mod_status):
        # Limpiar valores por defecto si el módulo no fue abordado
        save_col1, save_col2 = st.columns([1,1])
        with save_col1:
            if st.button("💾 Guardar como No Abordado", key="save_na_mod_sitio",
                         use_container_width=True):
                st.session_state.visit_data = data
                save_visit(data)
                st.success("✅ Módulo marcado como No Abordado.")
                show_drive_save_status()
        return
    if _mod_status == "inferido":
        st.info("🔍 **Modo inferido** — Las respuestas abajo son interpretaciones del facilitador, no de las personas del espacio.")
    st.markdown("---")

    tipo_espacio   = data.get("proyecto_tipo_espacio", "")
    only_containers = tipo_espacio in NO_SOIL_TYPES

    if only_containers:
        st.markdown('<div class="group-notice">🏢 <strong>Espacio principalmente construido</strong> — '
            'Sin suelo directo. Las secciones de suelo se adaptan para balcones, terrazas y macetas.</div>',
            unsafe_allow_html=True)

    tab_header(MOD, TABS)
    active = get_active_tab(MOD)

    if active == 0:
        _render_suelo_veg(data, only_containers)
        tab_nav_bottom(MOD, TABS, 0)
        _save_button(data, "23a")

    elif active == 1:
        _render_flujos(data)
        tab_nav_bottom(MOD, TABS, 1)
        _save_button(data, "23b")

    elif active == 2:
        _render_cultivo(data, only_containers)
        tab_nav_bottom(MOD, TABS, 2)
        _save_button(data, "23c")


def _render_suelo_veg(data, only_containers):
    if only_containers:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🪴 2.1 · Características del Espacio Construido")
        st.caption("Para departamentos, terrazas y balcones — sin suelo natural.")
        c1, c2 = st.columns(2)
        with c1:
            data["esp_tipo_piso"]  = st.selectbox("Tipo de piso/superficie",
                ["Cerámica","Hormigón","Madera","Metal","Otro"],
                index=["Cerámica","Hormigón","Madera","Metal","Otro"].index(data.get("esp_tipo_piso","Cerámica")))
            data["esp_exposicion"] = st.radio("¿Qué orientación tiene el espacio?",
                ["Norte","Sur","Este","Oeste","Noreste","Noroeste","Sureste","Suroeste"],
                index=["Norte","Sur","Este","Oeste","Noreste","Noroeste","Sureste","Suroeste"].index(data.get("esp_exposicion","Norte")),
                horizontal=True)
            data["esp_sol_horas"]  = st.slider("Horas de sol directo/día (promedio anual)", 0, 12, int(data.get("esp_sol_horas", 4)))
        with c2:
            data["esp_piso_numero"] = st.number_input("Piso número (si aplica)", min_value=0, value=int(data.get("esp_piso_numero", 0)), step=1)
            data["esp_viento"]      = st.radio("¿El espacio está expuesto al viento?",
                ["Muy protegido","Algo protegido","Expuesto","Muy expuesto"],
                index=["Muy protegido","Algo protegido","Expuesto","Muy expuesto"].index(data.get("esp_viento","Algo protegido")),
                horizontal=True)
            data["esp_estructura"]  = st.text_area("¿Qué estructuras existen para cultivar?",
                value=data.get("esp_estructura",""), height=80, placeholder="Ej: Una pérgola metálica, muros de bloque…")
        data["esp_contenedores"] = st.text_area("¿Con qué contenedores cuentan actualmente?",
            value=data.get("esp_contenedores",""), height=80, placeholder="Ej: 5 macetas grandes de barro, 2 cajones de madera…")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🌍 2.1 · Características del Suelo")
        c1, c2 = st.columns(2)
        with c1:
            data["suelo_tipo"]           = st.selectbox("Tipo de suelo",
                ["Desconocido","Arcilloso","Arenoso","Franco","Limoso","Mixto","Relleno urbano"],
                index=["Desconocido","Arcilloso","Arenoso","Franco","Limoso","Mixto","Relleno urbano"].index(data.get("suelo_tipo","Desconocido")))
            data["suelo_compactacion"]   = st.select_slider("Compactación", options=["Baja","Media","Alta"],
                value=data.get("suelo_compactacion","Media"))
            data["suelo_materia_organica"] = st.select_slider("Materia orgánica", options=["Bajo","Medio","Alto"],
                value=data.get("suelo_materia_organica","Bajo"))
        with c2:
            data["suelo_drenaje"] = st.select_slider("Drenaje", options=["Deficiente","Moderado","Bueno"],
                value=data.get("suelo_drenaje","Moderado"))
            data["suelo_color"]   = st.text_input("Color del suelo", value=data.get("suelo_color",""),
                placeholder="Ej: Marrón oscuro, gris claro…")
            data["suelo_olor"]    = st.text_input("Olor al cavarlo", value=data.get("suelo_olor",""),
                placeholder="Ej: Tierra húmeda, sin olor, ácido…")
        data["suelo_notas"] = st.text_area("📝 Notas del suelo", value=data.get("suelo_notas",""), height=80)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌿 2.2 · Vegetación Existente")
    veg_opts_soil = ["Árboles nativos","Árboles introducidos","Arbustos","Hierbas / pastos",
                     "Cultivos activos","Plantas ornamentales","Trepadoras / enredaderas"]
    veg_opts_cont = ["Plantas en macetas","Hierbas aromáticas en contenedores","Cultivos en cajones",
                     "Plantas colgantes","Trepadoras","Sin vegetación actual"]
    veg_opts = veg_opts_cont if only_containers else veg_opts_soil
    data["veg_tipos"]   = st.multiselect("Tipos de vegetación presentes", veg_opts,
        default=[v for v in data.get("veg_tipos",[]) if v in veg_opts])
    c3, c4 = st.columns(2)
    with c3:
        data["veg_especies"]  = st.text_area("Especies identificadas", value=data.get("veg_especies",""), height=80,
            placeholder="Ej: Romero, perejil, tomate, lechuga…")
    with c4:
        if not only_containers:
            data["veg_invasoras"] = st.text_area("Plantas invasoras o problemáticas",
                value=data.get("veg_invasoras",""), height=80, placeholder="Ej: Zarzamora, pasto bermuda, cardos…")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🦋 2.3 · Fauna y Biodiversidad")
    c5, c6 = st.columns(2)
    with c5:
        for key, label in [
            ("fauna_polinizadores","¿Observan insectos polinizadores? (abejas, mariposas…)"),
            ("fauna_aves","¿Observan aves frecuentemente?"),
        ]:
            data[key] = st.radio(label, ["No observado","Ocasionalmente","Frecuentemente"],
                index=["No observado","Ocasionalmente","Frecuentemente"].index(data.get(key,"No observado")),
                horizontal=True, key=f"bio_{key}")
        if not only_containers:
            data["fauna_lombrices"] = st.radio("¿Observan lombrices / organismos del suelo?",
                ["No observado","Pocas","Abundantes"],
                index=["No observado","Pocas","Abundantes"].index(data.get("fauna_lombrices","No observado")),
                horizontal=True)
    with c6:
        data["fauna_plagas"]        = st.text_input("Plagas o problemas fitosanitarios observados",
            value=data.get("fauna_plagas",""), placeholder="Ej: Pulgones, caracoles, mosca blanca…")
        data["fauna_aves_especies"] = st.text_input("Especies de aves identificadas",
            value=data.get("fauna_aves_especies",""), placeholder="Ej: Chincol, tordos, palomas…")
    data["eco_notas"] = st.text_area("📝 Notas ecológicas", value=data.get("eco_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_flujos(data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ☀️ 3.1 · Flujos Solares")
    st.markdown(
        '<div class="info-box">☀️ <strong>Nota:</strong> Las horas de sol varían según la estación. '
        'Registra el patrón anual, no solo el momento de la visita.</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        data["sol_horas"]         = st.slider("Horas de sol/día — zona más soleada (anual)", 0, 12, int(data.get("sol_horas",4)))
        data["sol_horas_invierno"]= st.slider("Horas de sol en invierno", 0, 12, int(data.get("sol_horas_invierno",2)))
        data["sol_horas_verano"]  = st.slider("Horas de sol en verano", 0, 14, int(data.get("sol_horas_verano",8)))
        data["sol_zonas_max"]     = st.text_area("Zonas con mayor exposición solar", value=data.get("sol_zonas_max",""), height=80,
            placeholder="Ej: Terraza sur, ventana este de cocina…")
    with c2:
        data["sol_orientacion"]   = st.selectbox("Orientación principal del espacio",
            ["Norte (Hemisferio Sur = máx. sol)","Sur (sombra en HS)","Este (sol mañana)","Oeste (sol tarde)","Mixta"],
            index=["Norte (Hemisferio Sur = máx. sol)","Sur (sombra en HS)","Este (sol mañana)","Oeste (sol tarde)","Mixta"].index(data.get("sol_orientacion","Mixta")))
        data["sol_sombra_perm"]   = st.text_area("Zonas de sombra permanente", value=data.get("sol_sombra_perm",""), height=80)
        data["sol_obstaculos"]    = st.text_area("Obstáculos que generan sombra", value=data.get("sol_obstaculos",""), height=80,
            placeholder="Ej: Edificio de 4 pisos al norte, árbol grande al este…")

    lat_val = data.get("geo_lat")
    if lat_val:
        st.markdown(
            f'<div class="info-box">📐 Con la latitud registrada ({lat_val:.2f}°):<br>'
            f'• <a href="https://app.shadowmap.org/?lat={lat_val}&lng={data.get("geo_lon",0)}&zoom=17" target="_blank">ShadowMap — Sombras en tiempo real</a><br>'
            f'• <a href="https://pvwatts.nrel.gov/" target="_blank">PVWatts (NREL) — Potencial fotovoltaico</a><br>'
            f'• <a href="https://re.jrc.ec.europa.eu/pvg_tools/es/" target="_blank">PVGIS (Europa) — Herramienta solar gratuita</a>'
            f'</div>', unsafe_allow_html=True)
    data["sol_notas"] = st.text_area("📝 Notas solares", value=data.get("sol_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 💨 3.2 · Flujos de Viento y Agua")
    c3, c4 = st.columns(2)
    with c3:
        data["viento_direccion"] = st.selectbox("Dirección predominante del viento",
            ["No determinada","Norte","Noreste","Este","Sureste","Sur","Suroeste","Oeste","Noroeste"],
            index=["No determinada","Norte","Noreste","Este","Sureste","Sur","Suroeste","Oeste","Noroeste"].index(data.get("viento_direccion","No determinada")))
        data["viento_protegidas"]= st.text_area("Zonas protegidas del viento", value=data.get("viento_protegidas",""), height=80)
    with c4:
        data["viento_expuestas"] = st.text_area("Zonas expuestas al viento", value=data.get("viento_expuestas",""), height=80)
        data["agua_flujo_lluvia"]= st.text_area("¿Cómo fluye el agua de lluvia en el sitio?",
            value=data.get("agua_flujo_lluvia",""), height=80, placeholder="Ej: Escurre hacia el fondo, se acumula en…")
    data["agua_acumulacion"] = st.text_input("¿Se acumula agua en algún punto? ¿Dónde?", value=data.get("agua_acumulacion",""))
    data["flujos_notas"]     = st.text_area("📝 Notas de flujos naturales", value=data.get("flujos_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_cultivo(data, only_containers):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🥦 3.3 · Potencial de Cultivo Alimentario")
    c1, c2 = st.columns(2)
    with c1:
        areas_opts = ["Suelo directo","Macetas","Bancales elevados","Terrazas","Balcones","Azoteas",
                      "Muros / cultivo vertical","Growbags / sacos"]
        data["cultivo_areas_tipo"]   = st.multiselect("Áreas potenciales para cultivo", areas_opts,
            default=[v for v in data.get("cultivo_areas_tipo",[]) if v in areas_opts])
        data["cultivo_riego_acceso"] = st.select_slider("Acceso al agua para riego",
            options=["Difícil","Moderado","Fácil"], value=data.get("cultivo_riego_acceso","Moderado"))
        data["cultivo_produce_hoy"]  = st.radio("¿Se producen alimentos actualmente?",
            ["No","En proceso","Sí"],
            index=["No","En proceso","Sí"].index(data.get("cultivo_produce_hoy","No")), horizontal=True)
    with c2:
        data["cultivo_sustrato_calidad"] = st.select_slider("Calidad del sustrato/tierra",
            options=["Muy baja","Baja","Media","Alta","Muy alta"],
            value=data.get("cultivo_sustrato_calidad","Media"))
        if not only_containers:
            data["cultivo_sustrato_drenaje"]   = st.select_slider("Drenaje del sustrato",
                options=["Deficiente","Moderado","Bueno"], value=data.get("cultivo_sustrato_drenaje","Moderado"))
            data["cultivo_sustrato_reutilizar"]= st.radio("¿Se puede reutilizar/mejorar el sustrato existente?",
                ["No","Con trabajo","Sí, fácilmente"],
                index=["No","Con trabajo","Sí, fácilmente"].index(data.get("cultivo_sustrato_reutilizar","Con trabajo")),
                horizontal=True)
        else:
            data["cultivo_sustrato_disponible"]= st.text_area("¿Qué sustrato/tierra tienen disponible?",
                value=data.get("cultivo_sustrato_disponible",""), height=80,
                placeholder="Ej: Mezcla de tierra con compost, perlita, turba…")

    data["cultivo_plantas_actuales"] = st.text_area("Plantas que actualmente crecen en el espacio",
        value=data.get("cultivo_plantas_actuales",""), height=80, placeholder="Ej: Romero, salvia, pasto…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Calculadora de áreas de cultivo ─────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### 📐 Calculadora de Áreas de Cultivo")
    st.caption("Agrega cada zona, maceta o bancal para calcular el área total y el sustrato necesario.")

    if "bancales" not in data or not isinstance(data.get("bancales"), list):
        data["bancales"] = []

    with st.expander("➕ Agregar zona / bancal / maceta", expanded=False):
        b_nombre = st.text_input("Nombre de la zona", placeholder="Ej: Bancal 1, Terraza sur…", key="b_nombre")
        b_tipo   = st.radio("Forma", ["Rectangular","Circular","Área libre (m²)"], horizontal=True, key="b_tipo")
        if b_tipo == "Rectangular":
            bc1, bc2, bc3 = st.columns(3)
            b_largo = bc1.number_input("Largo (m)", min_value=0.1, value=1.0, step=0.1, key="b_largo")
            b_ancho = bc2.number_input("Ancho (m)", min_value=0.1, value=0.5, step=0.1, key="b_ancho")
            b_alto  = bc3.number_input("Profundidad (m)", min_value=0.05, value=0.3, step=0.05, key="b_alto")
            b_area = round(b_largo * b_ancho, 2); b_vol = round(b_area * b_alto, 3)
        elif b_tipo == "Circular":
            bc1, bc2 = st.columns(2)
            b_radio = bc1.number_input("Radio (m)", min_value=0.1, value=0.3, step=0.05, key="b_radio")
            b_alto  = bc2.number_input("Profundidad (m)", min_value=0.05, value=0.3, step=0.05, key="b_alto_c")
            b_area = round(math.pi * b_radio**2, 2); b_vol = round(b_area * b_alto, 3)
        else:
            b_area = st.number_input("Área (m²)", min_value=0.01, value=0.5, step=0.1, key="b_area_libre")
            b_alto = st.number_input("Profundidad (m)", min_value=0.05, value=0.3, step=0.05, key="b_alto_l")
            b_vol  = round(b_area * b_alto, 3)
        st.caption(f"Área: **{b_area} m²** · Volumen: **{b_vol} m³** · Litros: **{round(b_vol*1000)} L** · Sacos 50L: **~{round(b_vol*1000/50,1)}**")
        if st.button("✅ Agregar zona", key="btn_add_bancal"):
            if b_nombre.strip():
                data["bancales"].append({"nombre": b_nombre, "tipo": b_tipo,
                    "area": b_area, "vol": b_vol, "litros": round(b_vol*1000)})
                st.session_state.visit_data = data  # sync before rerun
                st.rerun()

    if data.get("bancales"):
        total_area = round(sum(b["area"]   for b in data["bancales"]), 2)
        total_vol  = round(sum(b["vol"]    for b in data["bancales"]), 3)
        total_lit  = round(sum(b["litros"] for b in data["bancales"]))
        st.markdown(
            f'<div style="background:rgba(82,183,136,0.15);border:1px solid #52B788;'
            f'border-radius:10px;padding:0.8rem 1rem;margin:0.5rem 0;">'
            f'<strong>📊 Totales:</strong> Área: <strong>{total_area} m²</strong> · '
            f'Volumen: <strong>{total_vol} m³</strong> · Litros: <strong>{total_lit} L</strong> · '
            f'Sacos 50L: <strong>~{round(total_lit/50,1)}</strong></div>', unsafe_allow_html=True)
        data["cultivo_m2"] = total_area
        for i, b in enumerate(data["bancales"]):
            cb, cd = st.columns([4, 1])
            with cb: st.markdown(f"**{b['nombre']}** — {b['area']} m² · {b['vol']} m³ · {b['litros']} L")
            with cd:
                if st.button("🗑️", key=f"del_bancal_{i}"):
                    data["bancales"].pop(i)
                    st.session_state.visit_data = data
                    st.rerun()
    else:
        data["cultivo_m2"] = st.number_input("Área cultivable estimada total (m²)",
            min_value=0.0, value=float(data.get("cultivo_m2", 0)), step=0.5)

    c3, c4 = st.columns(2)
    with c3:
        data["cultivo_frutales"] = st.radio("¿Hay espacio para árboles frutales?", ["No","Posiblemente","Sí"],
            index=["No","Posiblemente","Sí"].index(data.get("cultivo_frutales","No")), horizontal=True)
        data["cultivo_interes"]  = st.text_area("¿Existe interés en producir alimentos? ¿Qué?",
            value=data.get("cultivo_interes",""), height=80, placeholder="Ej: Hierbas aromáticas y tomates…")
    with c4:
        data["cultivo_verticales"] = st.radio("¿Hay espacio para cultivos verticales?", ["No","Posiblemente","Sí"],
            index=["No","Posiblemente","Sí"].index(data.get("cultivo_verticales","No")), horizontal=True)
        data["cultivo_notas"]      = st.text_area("📝 Notas de potencial productivo",
            value=data.get("cultivo_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)


def _save_button(data, suffix=""):
    _, c, _ = st.columns([2, 1, 2])
    with c:
        if st.button("💾 Guardar módulos 2–3", use_container_width=True,
                     type="primary", key=f"save_m23_{suffix}"):
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            try:
                from utils.gdrive import is_configured, sync_visits_to_drive
                from utils.data_manager import DATA_FILE
                if is_configured(): sync_visits_to_drive(DATA_FILE)
            except Exception: pass
            st.success("✅ Módulos 2–3 guardados.")
            show_drive_save_status()
