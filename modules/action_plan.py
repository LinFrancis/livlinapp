"""Módulo 9 — Síntesis Regenerativa + Plan de Acción (v5) — interpretaciones editables."""
import streamlit as st
import plotly.graph_objects as go
from utils.data_manager import save_visit
from utils.scoring import (compute_synthesis_potentials, compute_domain_scores,
                            compute_regenerative_score, score_label)
from utils.synthesis import generate_all
from utils.tab_nav import tab_header, tab_nav_bottom, get_active_tab

TABS = ["🌱 Potencial Regenerativo", "📝 Síntesis Narrativa", "🗓️ Plan de Acción"]
MOD  = "m9"
ESTADOS = ["⏳ Pendiente", "🔄 En progreso", "✅ Completado", "❌ Cancelado"]

# ── Descripciones de cada dimensión ──────────────────────────────────────────
DIM_DESC = {
    "Producción alimentaria":  "Capacidad del espacio para producir alimentos frescos — cultivos, hierbas, frutales y hortalizas que contribuyen a la soberanía alimentaria del grupo.",
    "Biodiversidad urbana":    "Diversidad de especies vegetales y animales presentes — polinizadores, aves, plantas nativas, cobertura vegetal. Un espacio rico en biodiversidad es resiliente y saludable.",
    "Captación de agua":       "Gestión autónoma del agua: captación de lluvia, reutilización de aguas grises, eficiencia en el riego y reducción de la dependencia de la red pública.",
    "Regeneración del suelo":  "Salud biológica del suelo: materia orgánica, actividad microbiana, lombrices y hongos beneficiosos. El suelo vivo es la base de todo sistema regenerativo.",
    "Educación ambiental":     "Actividades de aprendizaje, transmisión de saberes y formación en ecología, permacultura y vida regenerativa que ocurren en el espacio o a partir de él.",
    "Bienestar comunitario":   "Calidad de los vínculos sociales: relaciones vecinales, participación comunitaria, redes de apoyo mutuo y capacidad de actuar colectivamente.",
    "Economía regenerativa":   "Prácticas de autosuficiencia, intercambio, comercio justo, trueque y economía circular que reducen la dependencia de mercados extractivos.",
    "Bienestar interior":      "Conexión del grupo con la naturaleza, prácticas de bienestar espiritual y emocional, silencio, contemplación y el cuidado de la dimensión interior como raíz de toda acción regenerativa.",
}

# ── Interpretaciones positivas por dimensión (índice 0-5) ────────────────────
DIM_INTERP = {
    "Producción alimentaria": [
        "El espacio se encuentra al inicio de su viaje productivo. Con pequeños pasos como una maceta o un bancal, la producción puede comenzar. Cada kilo producido localmente reduce la huella de carbono y fortalece la soberanía alimentaria frente al cambio climático.",
        "El espacio está despertando hacia la producción alimentaria. Existe una primera intención o pequeños cultivos. Desde aquí se puede expandir progresivamente incorporando más diversidad.",
        "El espacio ya produce algunos alimentos. Hay potencial claro para escalar y diversificar, contribuyendo activamente a la seguridad alimentaria local y a la reducción de emisiones.",
        "El espacio tiene producción alimentaria activa y variada. Está construyendo autonomía frente a sistemas alimentarios industriales que generan altas emisiones y contaminación.",
        "Excelente producción alimentaria. El espacio es fuente relevante de alimentos frescos — un modelo de soberanía alimentaria local.",
        "El espacio es un ejemplo de abundancia alimentaria urbana. Produce, comparte y regenera — demostrando que las ciudades pueden alimentarse a sí mismas.",
    ],
    "Biodiversidad urbana": [
        "El espacio está listo para acoger vida. Plantar nativas, crear un rincón sin intervenir o poner flores puede transformarlo en refugio de biodiversidad urbana — respondiendo directamente a la crisis global de pérdida de especies.",
        "Hay señales de vida emergente. Con intención y diseño, el espacio puede convertirse en un corredor ecológico que apoya a polinizadores, aves e insectos beneficiosos.",
        "El espacio alberga diversidad vegetal y animal. Tiene potencial de convertirse en nodo de biodiversidad que contribuya a revertir la pérdida de especies en el entorno urbano.",
        "El espacio es un refugio de biodiversidad activo. Los polinizadores y aves presentes son indicadores de salud ecológica — un ejemplo de ciudad como hogar de vida.",
        "Alta biodiversidad funcional. Demuestra que los entornos urbanos pueden sustentar ecosistemas ricos y resilientes.",
        "El espacio es un santuario de biodiversidad urbana — un modelo regenerativo que inspira a transformar la ciudad en un bosque vivo.",
    ],
    "Captación de agua": [
        "El espacio depende actualmente del agua de red. Un barril bajo la canaleta o reutilizar agua de la ducha son primeros pasos. Cada litro capturado reduce presión sobre los sistemas hídricos amenazados por el cambio climático.",
        "Hay conciencia sobre el agua y primeras intenciones. El potencial de implementar cosecha de lluvia y reutilización de grises es alto — cada avance reduce la vulnerabilidad ante las sequías.",
        "Existe un sistema parcial de gestión hídrica. Con optimizaciones, este espacio puede alcanzar soberanía hídrica significativa, especialmente relevante con el estrés hídrico creciente.",
        "Buen manejo del agua. El espacio ya capta lluvia o reutiliza grises — modelo de eficiencia que contribuye a la resiliencia frente a sequías.",
        "Sistema hídrico robusto. El espacio gestiona el agua como un recurso precioso — soberanía hídrica en construcción.",
        "Soberanía hídrica completa. El espacio es referente de gestión regenerativa del agua — captando, reciclando y cuidando cada gota.",
    ],
    "Regeneración del suelo": [
        "El suelo está esperando ser despertado. Compost, cobertura vegetal y materia orgánica pueden transformarlo en suelo vivo. 1 cm de suelo sano secuestra carbono durante décadas — aliado directo frente al cambio climático.",
        "El suelo está comenzando a regenerarse. Cada cucharada de compost es un paso hacia la vida. Con perseverancia, la transformación es inevitable.",
        "El suelo está mejorando. Hay señales de vida biológica y la materia orgánica avanza — el suelo se convierte en aliado del clima y la producción.",
        "Buen suelo biológicamente activo. Materia orgánica y organismos vivos trabajan para el espacio y para el clima.",
        "Suelo saludable y regenerado. Alta actividad biológica — un ejemplo de cómo regenerar el suelo urbano.",
        "Suelo vivo y abundante. Cada metro cuadrado cuenta en la lucha contra el cambio climático.",
    ],
    "Educación ambiental": [
        "El espacio tiene potencial para convertirse en lugar de aprendizaje vivo. La educación ambiental es clave para construir la cultura regenerativa que el planeta necesita para enfrentar las tres crisis.",
        "Hay interés y apertura al aprendizaje. Con pequeñas actividades compartidas, el espacio puede convertirse en escuela a cielo abierto.",
        "El espacio ya genera aprendizaje activo. Hay conocimiento que se practica y comparte — el siguiente paso es ampliar su alcance.",
        "El espacio es fuente activa de educación ambiental. Las personas aprenden y enseñan, construyendo la cultura del cuidado.",
        "El espacio educa e inspira a toda su comunidad — referente de aprendizaje regenerativo con efecto multiplicador.",
        "El espacio es una escuela viva de permacultura. Su influencia educativa trasciende sus límites físicos.",
    ],
    "Bienestar comunitario": [
        "El espacio está comenzando a tejer sus lazos. Con pequeñas iniciativas compartidas puede convertirse en nodo de cohesión social y resiliencia comunitaria frente a las crisis.",
        "Existen algunos vínculos comunitarios. El espacio puede fortalecer estas relaciones y convertirse en punto de encuentro alrededor del cuidado del territorio.",
        "El espacio muestra una red comunitaria en desarrollo. Con actividades más frecuentes, puede consolidarse como centro de bienestar colectivo.",
        "Buena red comunitaria activa. El espacio genera encuentros y colaboraciones — factor clave de resiliencia ante crisis.",
        "Excelente bienestar comunitario. Un nodo de cohesión social que genera confianza, colaboración y apoyo mutuo.",
        "El espacio es un corazón comunitario — modelo de cómo los espacios urbanos pueden transformarse en fuente de bienestar colectivo.",
    ],
    "Economía regenerativa": [
        "El espacio está al inicio de su transición económica. Compartir semillas, intercambiar productos, reducir compras son contribuciones a una economía más circular — alternativa a sistemas extractivos que generan contaminación.",
        "Hay primeras prácticas de economía alternativa emergiendo. El espacio puede convertirse en nodo de intercambio local.",
        "El espacio practica algunas formas de economía regenerativa. Hay autoproducción, intercambio o consumo más consciente.",
        "Buenas prácticas de economía regenerativa. El espacio produce excedentes, los comparte y contribuye a economías más justas.",
        "El espacio es modelo de economía regenerativa — combina autosuficiencia, intercambio justo y finanzas éticas.",
        "El espacio es referente de economía circular y regenerativa.",
    ],
    "Bienestar interior": [
        "El espacio tiene gran potencial para nutrir la dimensión interior. Un rincón de silencio o tiempo en contacto con la tierra puede ser el comienzo. Sanar nuestra relación con la naturaleza es el primer paso para regenerar.",
        "Hay primeras señales de conexión interior. Este vínculo puede profundizarse y convertirse en fuente de bienestar, calma y propósito.",
        "El espacio ya nutre el bienestar interior. Hay prácticas de conexión con la naturaleza que vale la pena cultivar.",
        "Buen nivel de bienestar interior. El espacio genera conexión, calma y sentido — base fundamental para una vida regenerativa.",
        "El espacio es fuente activa de bienestar interior y conexión profunda con la naturaleza.",
        "El espacio es un santuario interior — la conexión del grupo con la naturaleza es profunda y transformadora.",
    ],
}

CLIMATE_REF = {
    "Producción alimentaria":  "🌡️ Cada kilo producido localmente evita emisiones de transporte y fortalece la soberanía alimentaria frente al cambio climático.",
    "Biodiversidad urbana":    "🦋 Cada planta nativa y polinizador apoyado es una acción directa contra la crisis global de pérdida de especies.",
    "Captación de agua":       "💧 Gestionar el agua de forma autónoma reduce la vulnerabilidad ante las sequías cada vez más frecuentes por el cambio climático.",
    "Regeneración del suelo":  "🌍 El suelo vivo es el mayor sumidero de carbono disponible — regenerar el suelo es combatir el cambio climático desde tu patio.",
    "Educación ambiental":     "📚 La educación ambiental construye la conciencia colectiva necesaria para enfrentar las tres crisis: clima, biodiversidad y contaminación.",
    "Bienestar comunitario":   "🤝 Las comunidades resilientes responden mejor colectivamente al cambio climático y sus consecuencias sociales.",
    "Economía regenerativa":   "🌾 Economías locales y circulares reducen emisiones, contaminación y dependencia de sistemas extractivos que agravan las crisis planetarias.",
    "Bienestar interior":      "☯️ Sanar nuestra relación interior con la naturaleza es la raíz desde la que nace toda acción regenerativa sostenida en el tiempo.",
}


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
