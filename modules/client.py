"""Módulo 1 — Información del proyecto + Intención del grupo habitante."""
import streamlit as st
from utils.data_manager import save_visit
from utils.tab_nav import show_drive_save_status

TIPOS_ESPACIO = [
    "Casa con patio/jardín","Departamento con terraza","Departamento sin terraza",
    "Patio trasero","Balcón","Terraza comunitaria","Huerto comunitario",
    "Comunidad / copropiedad","Escuela / jardín infantil","Espacio público",
    "Finca rural","Centro comunitario","Otro",
]
COMPOSICION_GRUPO = [
    "Persona viviendo sola","Pareja sin hijos/as","Familia con hijos/as menores",
    "Familia con hijos/as adultos/as","Compañeros/as de casa",
    "Comunidad intencional","Grupo comunitario / vecinos","Organización o institución","Otro",
]

def render():
    st.markdown("## 🌿 Módulo 1 — Información del Proyecto")
    st.markdown('<p class="module-subtitle">Datos generales del espacio e intención colectiva del grupo habitante.</p>', unsafe_allow_html=True)
    st.markdown('<div class="group-notice">👥 <strong>Diagnóstico colectivo:</strong> Las respuestas reflejan la conversación y acuerdo del grupo habitante. No es un cuestionario individual — es una exploración compartida.</div>', unsafe_allow_html=True)

    data = st.session_state.visit_data

    # ── 1.1 Datos generales ──────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📋 1.1 · Datos Generales del Espacio")
    col1, col2 = st.columns(2)
    with col1:
        data["proyecto_nombre"]   = st.text_input("Nombre del proyecto *", value=data.get("proyecto_nombre",""), placeholder="Ej: Diagnóstico Casa Familia Soto")
        data["proyecto_cliente"]  = st.text_input("Grupo / familia / organización *", value=data.get("proyecto_cliente",""))
        data["proyecto_direccion"]= st.text_input("Dirección completa del espacio", value=data.get("proyecto_direccion",""), placeholder="Ej: Los Aromos 234, Ñuñoa, Santiago")
    with col2:
        data["proyecto_ciudad"]   = st.text_input("Ciudad *", value=data.get("proyecto_ciudad",""))
        data["proyecto_pais"]     = st.text_input("País", value=data.get("proyecto_pais","Chile"))
        try:
            import datetime
            data["proyecto_fecha"]= st.date_input("Fecha", value=datetime.date.today()).strftime("%d/%m/%Y")
        except Exception:
            data["proyecto_fecha"]= st.text_input("Fecha", value=data.get("proyecto_fecha",""))

    col3, col4 = st.columns(2)
    with col3:
        data["proyecto_area"]= st.number_input("Área total aproximada (m²)", min_value=0.0, value=float(data.get("proyecto_area",0)), step=1.0)
    with col4:
        tipo_idx = TIPOS_ESPACIO.index(data["proyecto_tipo_espacio"]) if data.get("proyecto_tipo_espacio") in TIPOS_ESPACIO else 0
        data["proyecto_tipo_espacio"]= st.selectbox("Tipo de espacio *", TIPOS_ESPACIO, index=tipo_idx)

    data["proyecto_composicion"]= st.selectbox("Composición del grupo habitante", COMPOSICION_GRUPO,
        index=COMPOSICION_GRUPO.index(data["proyecto_composicion"]) if data.get("proyecto_composicion") in COMPOSICION_GRUPO else 0)
    c5, c6 = st.columns(2)
    with c5: data["proyecto_n_adultos"]= st.number_input("Adultos/as", min_value=0, value=int(data.get("proyecto_n_adultos",1)), step=1)
    with c6: data["proyecto_n_ninos"]  = st.number_input("Niños/as o jóvenes", min_value=0, value=int(data.get("proyecto_n_ninos",0)), step=1)
    data["proyecto_habitantes"]= st.text_area("Descripción libre del grupo", value=data.get("proyecto_habitantes",""), height=80, placeholder="Ej: Somos pareja con dos hijos, un perro y tres gallinas…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 1.2 Geolocalización ─────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ 1.2 · Geolocalización del Espacio")
    st.caption("La dirección ingresada arriba se usa automáticamente. Haz clic en 'Buscar' para obtener mapa, clima y datos del lugar.")

    # Auto-fill from address above
    search_address = data.get("proyecto_direccion","")
    addr_display = st.text_input("Dirección a geolocalizar", value=search_address,
        placeholder="Ingresa la dirección arriba (sección 1.1) y presiona Buscar", key="geo_input")
    
    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1: geo_click = st.button("🔍 Buscar en mapa", use_container_width=True)
    with col_btn2: sat_mode  = st.checkbox("🛰️ Ver modo satélite", value=data.get("geo_sat_mode", False), key="sat_toggle")
    data["geo_sat_mode"] = sat_mode

    if geo_click and addr_display.strip():
        with st.spinner("Buscando ubicación y clima…"):
            from utils.geo_api import geocode_address, get_weather_now, wmo_weather_description, wind_direction_label, get_lunar_phase
            geo = geocode_address(addr_display)
        if geo:
            data.update({"geo_lat": geo["lat"], "geo_lon": geo["lon"],
                         "geo_display": geo["display_name"],
                         "geo_city": geo["city"], "geo_country": geo["country"]})
            st.success(f"📍 {geo['display_name']}")
        else:
            st.warning("No se encontró la dirección. Intenta ser más específico/a.")

    if data.get("geo_lat"):
        lat, lon = data["geo_lat"], data["geo_lon"]
        import pandas as pd
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})

        if sat_mode:
            # Satellite tile via stacked info
            st.markdown(f'<div class="geo-info-box">📍 {data.get("geo_display","")}<br>'
                f'🌐 Lat: {lat:.5f}  Lon: {lon:.5f}<br>'
                f'<a href="https://www.google.com/maps/@{lat},{lon},17z/data=!3m1!1e3" target="_blank">'
                f'🛰️ Ver en Google Maps Satélite</a> &nbsp;|&nbsp; '
                f'<a href="https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}" target="_blank">'
                f'🗺️ Ver en OpenStreetMap</a></div>', unsafe_allow_html=True)
        else:
            st.map(map_df, zoom=15)
            st.caption(f'🛰️ [Ver en satélite Google Maps](https://www.google.com/maps/@{lat},{lon},17z/data=!3m1!1e3) | [OpenStreetMap](https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon})')

        # ── Buscar lugares cercanos ──────────────────────────────────────
        st.markdown("**🔎 Buscar en el entorno:**")
        from utils.geo_api import search_nearby_places
        cat_options = ["parques","ferias","mercados","bibliotecas","escuelas","huertas"]
        cat_labels  = ["🌳 Parques","🛒 Ferias/Mercados","🏪 Tiendas alimentos","📚 Bibliotecas","🏫 Escuelas","🌱 Huertas"]
        sel_cats = st.multiselect("Buscar categorías:", cat_options,
            format_func=lambda x: dict(zip(cat_options,cat_labels)).get(x, x), key="nearby_cats")
        radius_km = st.slider("Radio de búsqueda (km)", 1, 20, 3, step=1, key="nearby_radius")
        if sel_cats and st.button("🔍 Buscar lugares cercanos", key="nearby_btn"):
            all_places = []
            with st.spinner("Buscando…"):
                for cat in sel_cats:
                    places = search_nearby_places(lat, lon, cat, radius_km*1000)
                    for p in places:
                        p["categoria"] = dict(zip(cat_options, cat_labels)).get(cat, cat)
                        all_places.append(p)
            if all_places:
                all_places.sort(key=lambda x: x["dist_m"])
                for p in all_places[:12]:
                    st.markdown(f"- {p['categoria']} **{p['name']}** — {p['dist_m']} m")
                data["entorno_lugares_cercanos"] = str(all_places[:12])
            else:
                st.info("No se encontraron lugares en ese radio.")

        # ── Clima actual ─────────────────────────────────────────────────
        with st.spinner("Cargando datos climáticos…"):
            from utils.geo_api import get_weather_now, wmo_weather_description, wind_direction_label, get_lunar_phase
            wx = get_weather_now(lat, lon)
            lunar = get_lunar_phase()

        if wx and "current" in wx:
            cur = wx["current"]
            st.markdown("---")
            st.markdown("**🌡️ Condiciones actuales**")
            wc1, wc2, wc3, wc4, wc5 = st.columns(5)
            with wc1: st.metric("Temperatura", f"{cur.get('temperature_2m','?')}°C", f"Sensación {cur.get('apparent_temperature','?')}°C")
            with wc2: st.metric("Humedad", f"{cur.get('relative_humidity_2m','?')}%")
            with wc3: st.metric("Precipitación", f"{cur.get('precipitation','?')} mm")
            with wc4: 
                ws = cur.get("wind_speed_10m","?")
                wd = wind_direction_label(cur.get("wind_direction_10m",0))
                st.metric("Viento", f"{ws} km/h {wd}")
            with wc5: st.metric(f"{lunar['icon']} Fase lunar", lunar["phase_name"], f"{lunar['phase_frac']}% ciclo")
            st.caption(f"☀️ {wmo_weather_description(cur.get('weather_code',0))}  ·  UV: {cur.get('uv_index','?')}")

            # Pronóstico 7 días
            if "daily" in wx:
                daily = wx["daily"]
                days  = daily.get("time",[])
                t_max = daily.get("temperature_2m_max",[])
                t_min = daily.get("temperature_2m_min",[])
                prec  = daily.get("precipitation_sum",[])
                fc_cols = st.columns(min(7, len(days)))
                for i, col in enumerate(fc_cols):
                    if i < len(days):
                        with col:
                            st.markdown(f"<div style='text-align:center;font-size:0.72rem;color:#555;'>"
                                f"{days[i][-5:]}<br>"
                                f"<span style='color:#E53935'>{t_max[i] if i<len(t_max) else '?'}°</span> / "
                                f"<span style='color:#1565C0'>{t_min[i] if i<len(t_min) else '?'}°</span><br>"
                                f"💧{prec[i] if i<len(prec) else '?'}mm</div>", unsafe_allow_html=True)

        # ── Clima Anual ───────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**📅 Patrones Climáticos Anuales**")
        st.caption("Promedios históricos (últimos 5 años). Cargando datos…")
        with st.spinner("Obteniendo clima anual…"):
            from utils.geo_api import get_annual_climate, get_solar_radiation
            climate = get_annual_climate(lat, lon)
            solar   = get_solar_radiation(lat, lon)

        if climate:
            try:
                import plotly.graph_objects as go
                fig = go.Figure()
                fig.add_trace(go.Bar(name="Precipitación (mm)", x=climate["months"],
                    y=climate["prec"], yaxis="y2", marker_color="rgba(30,136,229,0.5)", offsetgroup=1))
                fig.add_trace(go.Scatter(name="T° Máx", x=climate["months"],
                    y=climate["t_max"], line=dict(color="#E53935", width=2), mode="lines+markers"))
                fig.add_trace(go.Scatter(name="T° Mín", x=climate["months"],
                    y=climate["t_min"], line=dict(color="#1565C0", width=2), mode="lines+markers"))
                fig.update_layout(
                    yaxis=dict(title="Temperatura (°C)", side="left"),
                    yaxis2=dict(title="Precipitación (mm)", side="right", overlaying="y"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                    height=320, margin=dict(l=40,r=40,t=30,b=30),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,255,248,0.5)",
                )
                st.plotly_chart(fig, use_container_width=True)
                data["geo_clima_anual"] = str(climate)
                # Pre-populate annual precipitation for water module
                try:
                    prec_sum = round(sum(p for p in climate.get("prec", []) if p))
                    if prec_sum > 0:
                        data["agua_prec_anual"] = float(prec_sum)
                except Exception:
                    pass
            except Exception as e:
                st.caption(f"No se pudo graficar el clima: {e}")

        if solar:
            st.markdown("**☀️ Energía Solar del Lugar**")
            cols_sol = st.columns(3)
            with cols_sol[0]: st.metric("Promedio anual", f"{solar.get('annual_avg_kwh_m2','?')} kWh/m²/día")
            best_month = solar["months"][solar["monthly_kwh_m2"].index(max(x for x in solar["monthly_kwh_m2"] if x))] if solar.get("monthly_kwh_m2") else "?"
            with cols_sol[1]: st.metric("Mejor mes", best_month)
            panel_avg = sum(x for x in solar.get("panel_100w_kwh_day",[]) if x) / max(1, sum(1 for x in solar.get("panel_100w_kwh_day",[]) if x))
            with cols_sol[2]: st.metric("Panel 100W", f"~{round(panel_avg,2)} kWh/día prom.")
            st.markdown(
                '<div class="info-box">📘 <strong>Cómo interpretar:</strong> '
                f"Un panel solar de 100 Watts genera en promedio <strong>{round(panel_avg,2)} kWh por día</strong> "
                f"en este lugar, asumiendo 80% de eficiencia del sistema. "
                f"Para cubrir un consumo hogareño típico (5–10 kWh/día) necesitarías entre "
                f"{round(5/max(0.01,panel_avg))} y {round(10/max(0.01,panel_avg))} paneles de 100W. "
                "La radiación es mayor en verano y menor en invierno — considera el mes más crítico para dimensionar tu sistema.</div>",
                unsafe_allow_html=True)
            data["geo_solar"] = str(solar)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── 1.3 Intención del grupo ─────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 💭 1.3 · Intención del Grupo Habitante")
    st.caption("Respondan juntos/as — estas preguntas abren la conversación colectiva del diagnóstico.")

    for key, label, ph in [
        ("intencion_motivo",     "¿Qué motivó al grupo a realizar este diagnóstico?",
         "Ej: Queremos transformar el patio…"),
        ("intencion_cambios",    "¿Qué cambios les gustaría ver en este espacio?",
         "Ej: Más verde, producción de alimentos…"),
        ("intencion_vision5",    "¿Cómo imagina el grupo este lugar en 5 años?",
         "Ej: Un jardín productivo con árboles frutales…"),
        ("intencion_intentado",  "¿Qué han intentado hacer para mejorar el espacio? ¿Qué resultó? ¿Qué no?",
         "Ej: Plantamos hierbas pero se murieron…"),
        ("intencion_mejor",      "¿Qué parte del espacio funciona mejor actualmente?",
         "Ej: La terraza sur recibe mucho sol…"),
        ("intencion_frustracion","¿Qué parte genera más frustración?",
         "Ej: La esquina trasera siempre húmeda y sin uso…"),
        ("intencion_recursos",   "¿Con qué recursos cuenta el grupo? (tiempo, dinero, manos, conocimiento)",
         "Ej: Fines de semana, algo de presupuesto mensual…"),
        ("intencion_suenos",     "¿Hay algún sueño específico que el grupo quisiera ver realizado?",
         "Ej: Los niños cosechan tomates; un árbol de palto…"),
    ]:
        data[key]= st.text_area(label, value=data.get(key,""), height=80, placeholder=ph, key=f"inp_{key}")

    data["intencion_notas"]= st.text_area("📝 Observaciones adicionales del facilitador/a", value=data.get("intencion_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    _save_button(data)


def _save_button(data):
    st.markdown("---")
    _, col_b, _ = st.columns([2,1,2])
    with col_b:
        if st.button("💾 Guardar módulo 1", use_container_width=True, type="primary"):
            if not data.get("proyecto_nombre") or not data.get("proyecto_cliente"):
                st.error("⚠️ Nombre del proyecto y del grupo son obligatorios.")
                return
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            st.success("✅ Módulo 1 guardado.")
            show_drive_save_status()
