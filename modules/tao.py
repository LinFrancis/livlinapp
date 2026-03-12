"""Módulo Tao de la Regeneración — entre Módulo 1 y Módulo 2.
Estructura: de lo yin (interior) a lo yang (exterior).
Preguntas redactadas directamente a las personas del grupo.
"""
import streamlit as st
from utils.data_manager import save_visit
from utils.tab_nav import tab_header, tab_nav_bottom, get_active_tab


def render():
    st.markdown("## ☯️ Tao de la Regeneración")
    st.markdown(
        '<p class="module-subtitle">Exploración interior opcional — desde lo que sienten '
        'hacia lo que quieren crear. De lo yin a lo yang.</p>', unsafe_allow_html=True)

    # ── Introducción ──────────────────────────────────────────────────────
    with st.expander("📖 ¿Qué es el Tao de la Regeneración? (clic para leer)", expanded=False):
        st.markdown("""
El **Tao de la Regeneración** es un marco de indagación interior que usa el taoísmo filosófico
— especialmente a **Lao Tse** y **Chuang Tse** — como guía para explorar la relación
del grupo con el espacio que habita y con los procesos regenerativos.

En la permacultura, el principio de *observar antes de actuar* tiene un paralelo profundo
en el Tao: **no forzar**, fluir con los patrones naturales, encontrar el camino del menor
esfuerzo que produce el mayor bien. El Tao no es una filosofía de inacción — es una filosofía
de acción alineada con los ritmos de la naturaleza.

La triple crisis planetaria — cambio climático, pérdida de biodiversidad y contaminación —
puede ser abordada también desde adentro: ¿cómo nos relacionamos interiormente con esta
realidad? ¿Nos paraliza? ¿Nos moviliza? ¿Cómo este espacio puede ser una respuesta pequeña
pero real?

> *«Las leyes de la regeneración son las mismas que las leyes del Tao: volver a lo esencial
de lo esencial. Regenerar es simplemente fluir de regreso a la fuente.»*
> — Reflexiones frente a Lao Tse, Hua Dao (2025)

Este módulo es **completamente opcional**. Cada pregunta puede ser respondida,
saltada, o explorada con la profundidad que el grupo sienta apropiada.
        """)

    st.markdown(
        '<div class="info-box">🕊️ Este módulo puede responderse en conversación grupal '
        'o de forma individual. No hay respuestas correctas. '
        'Tómense el tiempo que necesiten — o vuelvan a él más tarde.</div>',
        unsafe_allow_html=True)

    data = st.session_state.visit_data

    # ── T.1 Presencia y relación con el espacio ───────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌿 T.1 · Presencia y Relación con el Espacio")
    st.markdown(
        '<div class="tao-quote-sm">«El Tao que puede ser nombrado no es el Tao eterno.» '
        '— Lao Tse, cap. 1<br>'
        '<em>Antes de cualquier proyecto, el espacio ya tiene su propio ritmo y su propia historia.</em>'
        '</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        data["tao_tiempo_aire"]= st.select_slider(
            "¿Cuánto tiempo pasan al aire libre?",
            options=["Casi nada","15–30 min","30–60 min","1–2 horas","Más de 2 horas"],
            value=data.get("tao_tiempo_aire","15–30 min"))
        data["tao_silencio"]= st.radio(
            "¿Practican momentos de silencio u observación tranquila aquí?",
            ["No","Rara vez","A veces","Regularmente"],
            index=["No","Rara vez","A veces","Regularmente"].index(data.get("tao_silencio","No")), horizontal=True)
        data["tao_conexion"]= st.slider(
            "¿Qué tan conectados/as se sienten con este lugar? (0=ninguna — 5=profunda)",
            0,5, int(data.get("tao_conexion",3)))
    with col2:
        data["tao_contemplacion"]= st.radio(
            "¿Existe en el espacio algún rincón para la contemplación o el silencio?",
            ["No","Informal / espontáneo","Sí, intencionado"],
            index=["No","Informal / espontáneo","Sí, intencionado"].index(data.get("tao_contemplacion","No")), horizontal=True)
        data["tao_sensacion"]= st.text_area(
            "¿Qué sensación les genera estar en este espacio hoy?",
            value=data.get("tao_sensacion",""), height=100,
            placeholder="Ej: Hay caos pero también potencial. Nos pide atención…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── T.2 Lo deseado y lo no deseado ───────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ☯️ T.2 · Lo Deseado y lo No Deseado")
    st.markdown(
        '<div class="tao-quote-sm">'
        '«Lo que buscas también está aquí. Así como lo que no buscas también está aquí. '
        'Ambos, lo deseado y lo no deseado, existen y así será siempre.<br>'
        'Tranquiliza tu corazón: mientras parezca todo perdido, la llama de aquello deseado '
        'no se apagará.»<br>'
        '<span style="font-size:0.8rem;">— Reflexiones frente a Lao Tse, Hua Dao (2025)</span>'
        '</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        data["tao_deseado"]= st.text_area("¿Qué desean para este espacio?", value=data.get("tao_deseado",""), height=90,
            placeholder="Ej: Abundancia, colores, vida, el canto de pájaros, cosechas, silencio…")
        data["tao_acepta_nod"]= st.radio(
            "¿Qué situaciones, dinámicas o resultados definitivamente NO quieren en este espacio?",
            ["No todavía","Con dificultad","Sí, en parte","Sí, profundamente"],
            index=["No todavía","Con dificultad","Sí, en parte","Sí, profundamente"].index(data.get("tao_acepta_nod","Con dificultad")))
    with col4:
        data["tao_no_deseado"]= st.text_area("¿Qué no desean para este espacio?", value=data.get("tao_no_deseado",""), height=90,
            placeholder="Ej: Maleza invasora, suciedad, ruido, soledad, desorden…")
        data["tao_llama"]= st.text_area(
            "¿Hay algo que desean pero que parece inalcanzable? ¿Cuál es la llama que no se apaga?",
            value=data.get("tao_llama",""), height=90,
            placeholder="Ej: Siempre quisimos un árbol grande, pero el espacio es pequeño…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── T.3 Ritmo de vida y descenso creativo ────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🍃 T.3 · Ritmo de Vida y Descenso Creativo")
    st.markdown(
        '<div class="tao-quote-sm">«El sabio actúa sin actuar, enseña sin palabras.» — Lao Tse, cap. 2<br>'
        '<em>El descenso creativo — hacer más con menos, encontrar plenitud en lo simple — '
        'es una expresión viviente del Tao y del principio permacultural de "producción sin residuos".</em>'
        '</div>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        data["tao_ritmo"]= st.select_slider("¿Cómo es su ritmo de vida actualmente?",
            options=["Muy acelerado","Acelerado","Equilibrado","Tranquilo","Muy tranquilo"],
            value=data.get("tao_ritmo","Acelerado"))
        data["tao_sencillez"]= st.radio(
            "¿Existe en el grupo una tendencia hacia la sencillez y lo esencial?",
            ["No, somos más de acumular","A veces","Sí, aunque con altibajos","Sí, como valor central"],
            index=["No, somos más de acumular","A veces","Sí, aunque con altibajos","Sí, como valor central"].index(data.get("tao_sencillez","A veces")))
        data["tao_consumo"]= st.text_area("¿Qué relación tienen con el consumo material?", value=data.get("tao_consumo",""), height=80,
            placeholder="Ej: Intentamos reducir pero es difícil en la ciudad…")
    with col6:
        data["tao_tiempo_libre"]= st.select_slider("¿Cuánto tiempo libre tienen para este espacio?",
            options=["Muy poco","Fines de semana","Varios momentos/semana","Varios días","Mucho tiempo"],
            value=data.get("tao_tiempo_libre","Fines de semana"))
        data["tao_actividades"]= st.text_area("¿Qué actividades los nutren y recargan en este lugar?", value=data.get("tao_actividades",""), height=80,
            placeholder="Ej: Leer, cultivar, jugar con los niños, tomar sol…")
        data["tao_descanso_creativo"]= st.text_area(
            "¿Han experimentado el 'descenso creativo' — bajar el ritmo y encontrar más en menos?",
            value=data.get("tao_descanso_creativo",""), height=80,
            placeholder="Ej: Cuando dejamos de correr tanto, el jardín empezó a florecer…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── T.4 Somos naturaleza ──────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌊 T.4 · Somos Naturaleza")
    st.markdown(
        '<div class="tao-quote-sm">'
        '«No intentar salvar la naturaleza como si fuera algo exterior a mí — eso reproduce el dual. '
        'Somos naturaleza. Al cuidarme, facilito que la naturaleza se manifieste a través de mí.»<br>'
        '<span style="font-size:0.8rem;">— Reflexiones frente a Lao Tse, Hua Dao (2025)</span>'
        '</div>', unsafe_allow_html=True)

    col7, col8 = st.columns(2)
    with col7:
        data["tao_naturaleza_ext"]= st.radio(
            "¿Tienden a sentir la naturaleza como algo exterior que hay que proteger, o como algo de lo que son parte?",
            ["Como algo exterior que hay que proteger","Ambas perspectivas coexisten","Como algo de lo que somos parte"],
            index=["Como algo exterior que hay que proteger","Ambas perspectivas coexisten","Como algo de lo que somos parte"].index(data.get("tao_naturaleza_ext","Ambas perspectivas coexisten")))
        data["tao_cuerpo_tierra"]= st.text_area(
            "¿Tienen contacto físico con la tierra en este espacio? (manos, pies descalzos, sembrar, cavar…)",
            value=data.get("tao_cuerpo_tierra",""), height=80,
            placeholder="Ej: A veces los niños juegan en la tierra, pero los adultos casi no…")
    with col8:
        data["tao_agua_virtud"]= st.text_area(
            "Lao Tse habla de la virtud del agua: fluye sin forzar, nutre todo. "
            "¿Qué parte de su grupo o espacio se parece al agua? ¿Qué bloquea ese flujo?",
            value=data.get("tao_agua_virtud",""), height=120,
            placeholder="Ej: Cuando no planificamos tanto y dejamos fluir, el espacio responde mejor…")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── T.5 Triple crisis planetaria ─────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌍 T.5 · La Triple Crisis Planetaria")
    st.markdown(
        '<div class="tao-quote-sm">'
        '«Regenerar es simplemente volver a lo esencial de lo esencial. '
        'Las leyes de la regeneración son las mismas que las leyes del Tao.»<br>'
        '<span style="font-size:0.8rem;">— Reflexiones frente a Lao Tse, Hua Dao (2025)</span>'
        '</div>', unsafe_allow_html=True)

    # ── Triple crisis: session-state tabs ─────────────────────────────
    CRISIS_TABS = ["🌡️ Cambio Climático", "🦋 Pérdida de Biodiversidad", "🧪 Contaminación"]
    tab_header("tao_crisis", CRISIS_TABS)
    crisis_active = get_active_tab("tao_crisis")

    if crisis_active == 0:
        data["tao_cc_conciencia"]= st.radio(
            "¿Qué tan presente está el cambio climático en su vida cotidiana?",
            ["No lo pensamos mucho","Lo conocemos pero parece lejano","Lo sentimos como una amenaza real","Es parte de nuestra motivación de acción"],
            index=["No lo pensamos mucho","Lo conocemos pero parece lejano","Lo sentimos como una amenaza real","Es parte de nuestra motivación de acción"].index(data.get("tao_cc_conciencia","Lo conocemos pero parece lejano")))
        data["tao_cc_impacto"]= st.text_area(
            "¿Han sentido el cambio climático en este lugar? (sequías, lluvias intensas, calor inusual…)",
            value=data.get("tao_cc_impacto",""), height=80, placeholder="Ej: Los últimos veranos han sido más secos…")
        data["tao_cc_respuesta"]= st.text_area(
            "¿Qué acciones han tomado o piensan tomar frente al cambio climático?",
            value=data.get("tao_cc_respuesta",""), height=80, placeholder="Ej: Guardar más agua, plantar árboles de sombra…")

    elif crisis_active == 1:
        data["tao_bio_conciencia"]= st.radio(
            "¿Tienen conciencia de la crisis de biodiversidad?",
            ["No la conocíamos","Sabemos que existe pero parece distante","La vemos en nuestro barrio","Es algo que sentimos profundamente"],
            index=["No la conocíamos","Sabemos que existe pero parece distante","La vemos en nuestro barrio","Es algo que sentimos profundamente"].index(data.get("tao_bio_conciencia","Sabemos que existe pero parece distante")))
        data["tao_bio_local"]= st.text_area(
            "¿Han notado cambios en la biodiversidad local? (menos aves, menos insectos, desaparición de especies…)",
            value=data.get("tao_bio_local",""), height=80, placeholder="Ej: Antes había muchas más mariposas en el barrio…")
        data["tao_bio_accion"]= st.text_area(
            "¿Qué podrían hacer en este espacio para contribuir a la biodiversidad local?",
            value=data.get("tao_bio_accion",""), height=80, placeholder="Ej: Plantar nativas, dejar un rincón sin intervenir…")

    elif crisis_active == 2:
        data["tao_cont_conciencia"]= st.radio(
            "¿Qué tan presente está la contaminación en su vida cotidiana?",
            ["No lo pensamos","Es algo lejano","La vivimos en el barrio","Es una preocupación activa"],
            index=["No lo pensamos","Es algo lejano","La vivimos en el barrio","Es una preocupación activa"].index(data.get("tao_cont_conciencia","Es algo lejano")))
        data["tao_cont_tipos"]= st.multiselect(
            "¿Qué tipos de contaminación identifican cerca o en este espacio?",
            ["Aire / smog","Suelo contaminado","Ruido","Luz artificial excesiva","Plásticos y residuos","Agua contaminada","Ninguna visible"],
            default=data.get("tao_cont_tipos",[]))
        data["tao_cont_respuesta"]= st.text_area(
            "¿Qué hacen o podrían hacer para reducir la contaminación desde este espacio?",
            value=data.get("tao_cont_respuesta",""), height=80, placeholder="Ej: Reducir plásticos, usar productos naturales de limpieza…")
    tab_nav_bottom("tao_crisis", CRISIS_TABS, crisis_active)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── T.6 Propósito y visión interior ──────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔮 T.6 · Propósito y Visión Interior")
    st.markdown(
        '<div class="tao-quote-sm">'
        '«知人者智，自知者明。» — Lao Tse, cap. 33<br>'
        '<em>«El conocimiento de los demás es sabiduría. El conocimiento de uno mismo es iluminación.» '
        'Chuang Tse añade: el sabio sigue el hilo natural de las cosas y no se afana en aparentar lo que no es.</em>'
        '</div>', unsafe_allow_html=True)

    data["tao_bienestar"]= st.radio(
        "¿Desean que este espacio apoye su bienestar interior, no solo su productividad?",
        ["No especialmente","Algo","Sí, mucho","Es lo más importante"],
        index=["No especialmente","Algo","Sí, mucho","Es lo más importante"].index(data.get("tao_bienestar","Sí, mucho")), horizontal=True)
    c11, c12 = st.columns(2)
    with c11:
        data["tao_naturaleza_rel"]= st.text_area(
            "¿Qué tipo de relación con la naturaleza desean cultivar?",
            value=data.get("tao_naturaleza_rel",""), height=90,
            placeholder="Ej: Producir alimentos, tener silencio, que los niños sean parte de algo vivo…")
        data["tao_aprender"]= st.text_area(
            "¿Qué les gustaría aprender en conexión con este espacio?",
            value=data.get("tao_aprender",""), height=90,
            placeholder="Ej: Permacultura, compostaje, plantas medicinales…")
    with c12:
        data["tao_justicia"]= st.text_area(
            "Buscar justicia sin reproducir lo que queremos cambiar es parte del Tao. "
            "¿Practican alguna forma de transformación sin violencia? (persuadir, crear, modelar…)",
            value=data.get("tao_justicia",""), height=90,
            placeholder="Ej: Preferimos mostrar con el ejemplo antes que predicar…")
        data["tao_palabra_esencial"]= st.text_area(
            "Si resumieran en una o dos palabras lo más esencial de lo que buscan con este espacio, ¿cuáles serían?",
            value=data.get("tao_palabra_esencial",""), height=90,
            placeholder="Ej: Raíces. Abundancia simple. Conexión. Hogar vivo…")

    data["tao_notas"]= st.text_area("📝 Notas del Tao de la Regeneración", value=data.get("tao_notas",""), height=80)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    _, col_b, _ = st.columns([2,1,2])
    with col_b:
        if st.button("💾 Guardar Tao", use_container_width=True, type="primary"):
            vid = save_visit(data)
            data["id"] = vid
            st.session_state.visit_data = data
            st.success("✅ Guardado.")
