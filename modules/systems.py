"""Módulos 4–6 — Contexto · Agua · Energía · Materiales (v5) — clickable tab nav."""
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status, tab_header, tab_nav_bottom, get_active_tab

TABS = ["🏙️ Contexto Urbano", "💧 Gestión del Agua", "⚡ Energía", "♻️ Materiales"]
MOD  = "systems"


def _ind_q(data, key, label, placeholder=""):
    data[key] = st.text_area(f"💬 {label}", value=data.get(key, ""), height=80,
                             placeholder=placeholder, key=f"ind_{key}")


def render():
    st.markdown("## 🏙️ Módulos 4–6 — Contexto · Agua · Energía · Materiales")
    st.markdown('<p class="module-subtitle">Contexto del espacio, recursos y sistemas existentes.</p>',
                unsafe_allow_html=True)
    data = st.session_state.visit_data

    # ── Estado del módulo ─────────────────────────────────────────────────
    st.markdown("**Estado de este módulo:**")
    _mod_status = render_module_status(data, "mod_sistemas")
    if not is_module_active(_mod_status):
        # Limpiar valores por defecto si el módulo no fue abordado
        save_col1, save_col2 = st.columns([1,1])
        with save_col1:
            if st.button("💾 Guardar como No Abordado", key="save_na_mod_sistemas",
                         use_container_width=True):
                st.session_state.visit_data = data
                save_visit(data)
                st.success("✅ Módulo marcado como No Abordado.")
                show_drive_save_status()
        return
    if _mod_status == "inferido":
        st.info("🔍 **Modo inferido** — Las respuestas abajo son interpretaciones del facilitador, no de las personas del espacio.")
    st.markdown("---")

    tab_header(MOD, TABS)
    active = get_active_tab(MOD)

    # ════════════════════════════════════════════════════════════════════════
    if active == 0:
        st.markdown("### 🏙️ 4.1 · Entorno Verde y Natural")
        _render_contexto(data)
        tab_nav_bottom(MOD, TABS, 0)
        _save_button(data, "4a")

    elif active == 1:
        st.markdown("### 💧 5.1–5.3 · Gestión del Agua")
        _render_agua(data)
        tab_nav_bottom(MOD, TABS, 1)
        _save_button(data, "4b")

    elif active == 2:
        st.markdown("### ⚡ 5.4 · Energía y Electricidad")
        _render_energia(data)
        tab_nav_bottom(MOD, TABS, 2)
        _save_button(data, "4c")

    elif active == 3:
        st.markdown("### ♻️ 6.1–6.2 · Materiales y Residuos")
        _render_materiales(data)
        tab_nav_bottom(MOD, TABS, 3)
        _save_button(data, "4d")


# ── Contexto ─────────────────────────────────────────────────────────────────
def _render_contexto(data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    _ind_q(data, "ctx_ind_verde", "¿Cómo perciben el entorno verde del barrio? ¿Qué les gustaría mejorar?",
           "Ej: El barrio tiene pocos árboles pero hay una plaza a 3 cuadras que usamos mucho…")

    st.markdown("**🌳 Parques y áreas verdes cercanos:**")
    if "ctx_parques_lista" not in data or not isinstance(data.get("ctx_parques_lista"), list):
        data["ctx_parques_lista"] = []
    with st.expander("➕ Agregar parque / área verde"):
        p_nombre = st.text_input("Nombre", placeholder="Ej: Parque Bustamante…", key="p_nombre")
        p_dist   = st.number_input("Distancia (metros)", min_value=0, value=100, step=50, key="p_dist")
        p_uso    = st.text_input("¿Lo usan? ¿Para qué?", key="p_uso")
        if st.button("✅ Agregar parque", key="btn_parque"):
            if p_nombre.strip():
                data["ctx_parques_lista"].append({"nombre": p_nombre, "dist": p_dist, "uso": p_uso})
                st.session_state.visit_data = data
                st.rerun()
    for i, p in enumerate(data["ctx_parques_lista"]):
        cp, cd = st.columns([5, 1])
        with cp: st.markdown(f"🌳 **{p['nombre']}** — {p['dist']} m · {p.get('uso','')}")
        with cd:
            if st.button("🗑️", key=f"del_p_{i}"): data["ctx_parques_lista"].pop(i); st.session_state.visit_data = data; st.rerun()
    if data["ctx_parques_lista"]:
        data["ctx_distancia_parques"] = min(p["dist"] for p in data["ctx_parques_lista"])

    data["ctx_cuenca"]     = st.text_area("🌊 ¿Conocen la cuenca hidrográfica del espacio?",
                                          value=data.get("ctx_cuenca",""), height=80)
    data["ctx_vecinos"]    = st.select_slider("Relación general con vecinos",
                                              options=["Ninguna","Escasa","Moderada","Buena","Excelente"],
                                              value=data.get("ctx_vecinos","Moderada"))
    data["ctx_participacion"] = st.radio("¿Participan en iniciativas de barrio?",
                                         ["No","A veces","Regularmente"],
                                         index=["No","A veces","Regularmente"].index(data.get("ctx_participacion","No")),
                                         horizontal=True)

    st.markdown("**🤝 Mapeo de Actores Comunitarios:**")
    ACTOR_TYPES = ["Junta de vecinos","Club deportivo","Biblioteca","Huerto comunitario",
                   "Organización ambiental","Vecino/a aliado/a","Escuela / jardín","Mercado / feria","Otro"]
    if "ctx_actores" not in data or not isinstance(data.get("ctx_actores"), list):
        data["ctx_actores"] = []
    with st.expander("➕ Agregar actor comunitario"):
        a_tipo    = st.selectbox("Tipo", ACTOR_TYPES, key="a_tipo")
        a_nombre  = st.text_input("Nombre", key="a_nombre")
        a_relacion= st.text_input("Relación / potencial", key="a_relacion")
        if st.button("✅ Agregar actor", key="btn_actor"):
            if a_nombre.strip():
                data["ctx_actores"].append({"tipo": a_tipo, "nombre": a_nombre, "relacion": a_relacion})
                st.session_state.visit_data = data
                st.rerun()
    for i, a in enumerate(data["ctx_actores"]):
        ca, cb = st.columns([5, 1])
        with ca: st.markdown(f"🤝 **{a['tipo']}** · {a['nombre']} — {a.get('relacion','')}")
        with cb:
            if st.button("🗑️", key=f"del_act_{i}"): data["ctx_actores"].pop(i); st.session_state.visit_data = data; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ── Agua ─────────────────────────────────────────────────────────────────────
def _render_agua(data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    _ind_q(data, "agua_ind_general",
           "¿Cómo entienden el buen uso del recurso hídrico? ¿Qué les gustaría mejorar?",
           "Ej: Queremos reducir el consumo pero no sabemos cómo…")

    c1, c2 = st.columns(2)
    with c1:
        data["agua_fuente"] = st.selectbox("Fuente de agua principal",
            ["Red pública","Pozo","Agua reciclada","Mixta"],
            index=["Red pública","Pozo","Agua reciclada","Mixta"].index(data.get("agua_fuente","Red pública")))
        data["agua_riego_sistema"] = st.selectbox("Sistema de riego",
            ["No existe","Manual","Por goteo","Automático"],
            index=["No existe","Manual","Por goteo","Automático"].index(data.get("agua_riego_sistema","No existe")))
    with c2:
        for key, label, opts in [
            ("agua_captacion_lluvia","¿Existe captación de agua lluvia?",["No","Parcial","Sí"]),
            ("agua_grises","¿Se reutiliza agua gris?",["No","Parcialmente","Sí"]),
            ("agua_fugas","¿Hay pérdidas o fugas?",["No","Posibles","Sí"]),
        ]:
            data[key] = st.radio(label, opts, index=opts.index(data.get(key, opts[0])),
                                 horizontal=True, key=f"r_{key}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Estimador de consumo hídrico ─────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🚿 Estimador de Consumo Hídrico")
    st.markdown(
        '<div class="info-box">💧 Agrega cada fuente de agua del hogar. '
        'Puedes medir con cronómetro (flujo en 30s) <strong>o</strong> '
        'con un recipiente (cuánto tarda en llenarse). '
        'Al final verás el consumo total diario estimado.</div>',
        unsafe_allow_html=True)

    if "fuentes_agua" not in data or not isinstance(data.get("fuentes_agua"), list):
        data["fuentes_agua"] = []

    with st.expander("➕ Agregar fuente de agua"):
        fa_nombre = st.text_input("Fuente de agua", key="fa_nombre",
                                  placeholder="Ej: Ducha, WC, Lavamanos, Riego…")
        fa_metodo = st.radio("Método de medición",
                             ["⏱️ Flujo en 30 segundos", "🪣 Tiempo en llenar un recipiente",
                              "📦 Volumen fijo por uso (WC, lavadora…)"],
                             horizontal=False, key="fa_metodo")

        fa_lit_dia = 0.0
        if fa_metodo == "⏱️ Flujo en 30 segundos":
            fa_l30s  = st.number_input("Litros recogidos en 30 segundos", min_value=0.1, value=6.0, step=0.5, key="fa_l30s")
            fa_mins  = st.number_input("Minutos de uso al día (total de personas)", min_value=0.1, value=5.0, step=0.5, key="fa_mins")
            fa_lit_dia = round(fa_l30s * 2 * fa_mins, 1)
            st.caption(f"Caudal: {fa_l30s*2:.1f} L/min → **{fa_lit_dia} L/día**")

        elif fa_metodo == "🪣 Tiempo en llenar un recipiente":
            fa_vol_cc  = st.number_input("Capacidad del recipiente (ml / cc)", min_value=100, value=1000, step=100, key="fa_vol_cc")
            fa_seg_lle = st.number_input("Segundos que tarda en llenarse", min_value=1, value=10, step=1, key="fa_seg_lle")
            fa_mins_uso= st.number_input("Minutos totales de uso al día (todas las personas)", min_value=0.1, value=5.0, step=0.5, key="fa_mins_uso")
            caudal_lmin = round((fa_vol_cc / 1000) / (fa_seg_lle / 60), 2)
            fa_lit_dia  = round(caudal_lmin * fa_mins_uso, 1)
            st.caption(f"Caudal: {caudal_lmin} L/min (basado en {fa_vol_cc}cc en {fa_seg_lle}s) → **{fa_lit_dia} L/día**")

        elif fa_metodo == "📦 Volumen fijo por uso (WC, lavadora…)":
            fa_vol_uso = st.number_input("Litros por uso (ej: WC ≈ 6L, lavadora ≈ 50L)", min_value=0.1, value=6.0, step=0.5, key="fa_vol_uso")
            fa_usos_d  = st.number_input("Usos totales por día (todas las personas)", min_value=1, value=4, step=1, key="fa_usos_d")
            fa_lit_dia = round(fa_vol_uso * fa_usos_d, 1)
            st.caption(f"→ **{fa_lit_dia} L/día**")

        if st.button("✅ Agregar fuente", key="btn_add_fuente"):
            if fa_nombre.strip():
                data["fuentes_agua"].append({"nombre": fa_nombre, "lit_dia": fa_lit_dia, "metodo": fa_metodo})
                st.session_state.visit_data = data
                st.rerun()

    if data["fuentes_agua"]:
        total_l_dia = sum(f.get("lit_dia", 0) for f in data["fuentes_agua"])
        total_l_mes = round(total_l_dia * 30)
        total_m3    = round(total_l_mes / 1000, 2)
        for i, f in enumerate(data["fuentes_agua"]):
            cf, cd = st.columns([5, 1])
            with cf: st.markdown(f"🚿 **{f['nombre']}** — {f.get('lit_dia',0)} L/día")
            with cd:
                if st.button("🗑️", key=f"del_f_{i}"): data["fuentes_agua"].pop(i); st.session_state.visit_data = data; st.rerun()
        st.markdown(
            f'<div style="background:rgba(33,150,243,0.1);border:1px solid #90CAF9;border-radius:10px;padding:0.8rem 1rem;">'
            f'💧 <strong>Consumo estimado: {round(total_l_dia)} L/día · {total_l_mes} L/mes · {total_m3} m³/mes</strong>'
            f'</div>', unsafe_allow_html=True)
        data["agua_consumo_estimado_ldia"] = round(total_l_dia)
        data["agua_consumo"] = total_m3
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Captación de lluvia ───────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌧️ Captación de Agua Lluvia")
    # Get precipitation: prefer stored value, fallback to parsing climate data
    prec_anual = 0
    if data.get("agua_prec_anual") and float(data.get("agua_prec_anual", 0)) > 0:
        prec_anual = int(data["agua_prec_anual"])
    elif data.get("geo_clima_anual"):
        try:
            import ast
            clima = ast.literal_eval(data["geo_clima_anual"]) if isinstance(data["geo_clima_anual"], str) else data["geo_clima_anual"]
            prec_anual = round(sum(p for p in clima.get("prec", []) if p))
            if prec_anual > 0:
                data["agua_prec_anual"] = float(prec_anual)  # cache it
        except Exception: pass

    c3, c4 = st.columns(2)
    with c3:
        data["agua_techo_m2"]         = st.number_input("Área de techo disponible (m²)", min_value=0.0, value=float(data.get("agua_techo_m2", 0)), step=5.0)
        data["agua_efic_captacion"]   = st.slider("Eficiencia del sistema (%)", 50, 95, int(data.get("agua_efic_captacion", 80)), step=5)
    with c4:
        prec_in = st.number_input("Precipitación anual (mm/año) — se obtiene automáticamente de la API al cargar el mapa en M1",
                                   min_value=0.0, value=float(prec_anual if prec_anual > 0 else data.get("agua_prec_anual", 0)),
                                   step=10.0, key="prec_anual_input")
        data["agua_prec_anual"] = prec_in
        if prec_anual > 0:
            st.caption(f"✅ Precipitación cargada desde la API climática: {prec_anual} mm/año")
        else:
            st.caption("💡 La precipitación se carga automáticamente al usar 'Buscar' en Módulo 1. También puedes ingresarla manualmente.")

    if data.get("agua_techo_m2", 0) > 0 and data.get("agua_prec_anual", 0) > 0:
        lits  = round(data["agua_techo_m2"] * data["agua_prec_anual"] * (data.get("agua_efic_captacion",80)/100))
        st.markdown(f'<div class="info-box">🌧️ Captación potencial: <strong>{lits:,} L/año</strong> · {round(lits/12):,} L/mes · {round(lits/365)} L/día</div>', unsafe_allow_html=True)
        data["agua_litros_captacion_anual"] = lits
    data["agua_sequias"]        = st.radio("¿Han experimentado restricciones o escasez hídrica?",
        ["No","Alguna vez","Regularmente en verano","Es un problema grave"],
        index=["No","Alguna vez","Regularmente en verano","Es un problema grave"].index(data.get("agua_sequias","No")), horizontal=True)
    data["agua_sequias_impacto"] = st.text_area("¿Cómo les afecta la sequía?", value=data.get("agua_sequias_impacto",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)


# ── Energía ──────────────────────────────────────────────────────────────────
def _render_energia(data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    _ind_q(data, "ene_ind_general", "¿Cómo entienden el uso de energía? ¿Qué les gustaría reducir o cambiar?",
           "Ej: Consumimos mucho en invierno. Nos gustaría tener paneles solares…")
    c1, c2 = st.columns(2)
    with c1:
        data["ene_fuente"]       = st.selectbox("Fuente energética principal",
            ["Red eléctrica","Panel solar","Gas + eléctrico","Mixta"],
            index=["Red eléctrica","Panel solar","Gas + eléctrico","Mixta"].index(data.get("ene_fuente","Red eléctrica")))
        data["ene_solar_interes"] = st.radio("¿Interés en instalar energía solar?",
            ["No","Mediano plazo","Sí, pronto"],
            index=["No","Mediano plazo","Sí, pronto"].index(data.get("ene_solar_interes","No")), horizontal=True)
    with c2:
        data["ene_led"] = st.radio("¿Iluminación 100% LED?", ["No","Parcialmente","Sí"],
            index=["No","Parcialmente","Sí"].index(data.get("ene_led","Parcialmente")), horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### 🔌 Calculadora de Consumo Eléctrico")
    with st.expander("📘 Metodología y conceptos clave — energía solar"):
        st.markdown("""
**¿Cómo funciona un sistema solar fotovoltaico?**

Un panel solar produce electricidad según su potencia (Watts) y las **horas de sol pico (HSP)** del lugar:

`Producción diaria = Watts × HSP × 85% (eficiencia del sistema)`

- **Santiago (Chile):** ~4.5–5 HSP promedio · invierno: ~2.5 HSP · verano: ~6.5 HSP
- **Panel 100W** produce aprox. **0.38–0.43 kWh/día** (promedio anual en Santiago)
- **Panel 400W** produce aprox. **1.5–1.7 kWh/día**

**Baterías de almacenamiento:**
| Tipo | Capacidad útil (100Ah/12V) | Ventajas |
|------|---------------------------|----------|
| LiFePO4 (litio hierro) | ~1.0 kWh | Larga vida, liviana, segura ✅ |
| Plomo-ácido | ~0.6 kWh | Económica, pero pesada |
| LiNMC (litio) | ~1.0 kWh | Compacta, más cara |

**Regla práctica:**
- 1 panel 100W + 1 batería LiFePO4 → iluminación LED + celulares + pequeños aparatos
- 4 paneles 400W + 2 baterías → refrigerador + iluminación + TV
- 10+ paneles + inversor → hogar con consumo moderado autónomo
        """)

    if "equipos_electricos" not in data or not isinstance(data.get("equipos_electricos"), list):
        data["equipos_electricos"] = []

    with st.expander("➕ Agregar equipo / electrodoméstico"):
        eq_n = st.text_input("Nombre del equipo", key="eq_n", placeholder="Ej: Refrigerador, TV, computador…")
        eq_w = st.number_input("Consumo (Watts)", min_value=1, value=100, step=10, key="eq_w")
        eq_h = st.number_input("Horas de uso por día", min_value=0.1, value=4.0, step=0.5, key="eq_h")
        eq_c = st.number_input("Cantidad de unidades", min_value=1, value=1, step=1, key="eq_c")
        eq_kwh = round(eq_w * eq_h * eq_c / 1000, 3)
        st.caption(f"→ **{eq_kwh} kWh/día** · {round(eq_kwh*30,1)} kWh/mes")
        if st.button("✅ Agregar equipo", key="btn_eq"):
            if eq_n.strip():
                data["equipos_electricos"].append({"nombre": eq_n,"watts": eq_w,"horas": eq_h,"cant": eq_c,"kwh_dia": eq_kwh})
                st.session_state.visit_data = data
                st.rerun()

    if data["equipos_electricos"]:
        total_kwh = sum(e.get("kwh_dia", 0) for e in data["equipos_electricos"])
        total_mes = round(total_kwh * 30, 1)
        for i, e in enumerate(data["equipos_electricos"]):
            ce, cd = st.columns([5, 1])
            with ce: st.markdown(f"🔌 **{e['nombre']}** — {e['watts']}W × {e['horas']}h × {e['cant']}u = **{e['kwh_dia']} kWh/día**")
            with cd:
                if st.button("🗑️", key=f"del_eq_{i}"): data["equipos_electricos"].pop(i); st.session_state.visit_data = data; st.rerun()

        # Get solar hours from geo data
        hsp_prom, hsp_inv, hsp_ver = 4.5, 2.5, 6.5
        if data.get("geo_solar"):
            try:
                import ast
                sol = ast.literal_eval(data["geo_solar"]) if isinstance(data["geo_solar"],str) else data["geo_solar"]
                vals = [v for v in sol.get("monthly_kwh_m2",[]) if v]
                if vals: hsp_prom = round(sum(vals)/len(vals),1); hsp_inv = round(min(vals),1); hsp_ver = round(max(vals),1)
            except Exception: pass

        data["ene_kwh_dia_calc"] = round(total_kwh, 2)

        st.markdown(f'<div style="background:rgba(255,215,0,0.12);border:1px solid #FDD835;border-radius:10px;padding:0.8rem 1rem;">'
                    f'⚡ <strong>{round(total_kwh,2)} kWh/día</strong> · {total_mes} kWh/mes · '
                    f'HSP lugar: prom {hsp_prom}h · inv {hsp_inv}h · ver {hsp_ver}h</div>', unsafe_allow_html=True)

        EFI = 0.85; BATT_LI = 1.0; BATT_PB = 0.6
        st.markdown("**☀️ Escenarios solares:**")
        for watts, label in [(100,"1 panel 100W"),(200,"2 paneles 100W"),(400,"1 panel 400W"),
                              (800,"2 paneles 400W"),(1000,"1 kW"),(2000,"2 kW"),(4000,"4 kW")]:
            kw = watts / 1000
            p_p = round(kw*hsp_prom*EFI, 2); p_i = round(kw*hsp_inv*EFI, 2); p_v = round(kw*hsp_ver*EFI, 2)
            cob = min(100, round(p_p/max(0.01,total_kwh)*100))
            icon = "✅" if cob >= 100 else ("⚡" if cob >= 60 else "🌱")
            st.markdown(f'<div style="margin:3px 0;padding:0.5rem 0.8rem;background:white;border:1px solid #E8F5E9;border-radius:8px;font-size:0.83rem;">'
                        f'{icon} <strong>{label}</strong> → {p_p} kWh/día prom · {p_i} inv · {p_v} ver · '
                        f'<span style="font-weight:600;color:{"#2D6A4F" if cob>=100 else "#40916C"}">cubre {cob}%</span></div>',
                        unsafe_allow_html=True)

        st.markdown("**🔋 Baterías para autonomía (sin sol):**")
        for dias in [1, 2, 3]:
            en = total_kwh * dias
            n_li = max(1, round(en/BATT_LI + 0.4)); n_pb = max(1, round(en/BATT_PB + 0.4))
            st.markdown(f"- **{dias} día{'s' if dias>1 else ''}**: {n_li} batería{'s' if n_li>1 else ''} LiFePO4 ó {n_pb} plomo-ácido")
    st.markdown("</div>", unsafe_allow_html=True)


# ── Materiales ────────────────────────────────────────────────────────────────
def _render_materiales(data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    _ind_q(data, "res_ind_general", "¿Cómo entienden la gestión de residuos? ¿Qué les gustaría mejorar?")
    data["res_intentos_fallidos"] = st.text_area("🔄 ¿Han intentado compostar antes y no funcionó? ¿Por qué falló?",
        value=data.get("res_intentos_fallidos",""), height=100,
        placeholder="Ej: Se murieron las lombrices · Se llenó de moscas · Olía mal…")
    c1, c2 = st.columns(2)
    with c1:
        data["res_compost_tipo"]  = st.selectbox("Sistema de compostaje",
            ["Ninguno","Compost básico","Vermicompost","Bokashi","Compost + lombrices","Avanzado"],
            index=["Ninguno","Compost básico","Vermicompost","Bokashi","Compost + lombrices","Avanzado"].index(data.get("res_compost_tipo","Ninguno")))
        data["res_compostan"]     = st.radio("¿Compostan residuos?", ["No","Parcialmente","Sí"],
            index=["No","Parcialmente","Sí"].index(data.get("res_compostan","No")), horizontal=True)
    with c2:
        for key, label, opts in [
            ("res_separan","¿Separan reciclables?",["No","A veces","Siempre"]),
            ("res_reutilizan","¿Reutilizan materiales?",["No","A veces","Regularmente"]),
            ("res_segunda_mano","¿Compran de segunda mano?",["No","A veces","Regularmente"]),
        ]:
            data[key] = st.radio(label, opts, index=opts.index(data.get(key, opts[0])),
                                 horizontal=True, key=f"rm_{key}")
    data["mat_notas"] = st.text_area("📝 Notas de materiales y residuos", value=data.get("mat_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)


def _save_button(data, suffix=""):
    _, c, _ = st.columns([2, 1, 2])
    with c:
        if st.button("💾 Guardar módulos 4–6", use_container_width=True,
                     type="primary", key=f"save_sys_{suffix}"):
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            # Sync to Drive if configured
            try:
                from utils.gdrive import is_configured, sync_visits_to_drive
                from utils.data_manager import DATA_FILE
                if is_configured(): sync_visits_to_drive(DATA_FILE)
            except Exception: pass
            st.success("✅ Guardado correctamente.")
