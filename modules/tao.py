"""Modulo Tao de la Regeneracion v2.0
Basado en 'El Tao de la Regeneracion' -- 5 dimensiones de sabiduria taoista.
Escala 1-5 por dimension. Radar de 5 ejes. Disclaimer interpretativo.

NOTE: Data constants and scoring functions are at module level (no streamlit dependency).
UI render functions use streamlit only when called.
"""

# ========================================================================
# CONTENIDO: 5 dimensiones del Tao de la Regeneracion
# ========================================================================

TAO_INTRO = (
    "El **Tao de la Regeneracion** es un marco de indagacion interior que usa "
    "el taoismo filosofico como guia para explorar la relacion del grupo con "
    "el espacio que habita y con los procesos regenerativos.\n\n"
    "Las leyes de la regeneracion son las mismas que las leyes del Tao: "
    "el retorno ciclico a lo esencial, la danza perpetua entre lo que muere "
    "y lo que nace, la confianza en que la vida, cuando se le da espacio, "
    "siempre retorna.\n\n"
    "Somos naturaleza. Al cuidarnos, facilitamos que la naturaleza se "
    "manifieste a traves nuestro. Cada dimension es una danza entre yin y "
    "yang: no se trata de elegir un polo sobre el otro, sino de reconocer "
    "cuando cada uno esta desequilibrado y permitir que su complemento "
    "restaure la armonia."
)

TAO_EPIGRAFE = (
    "Lo que buscas tambien esta aqui. Asi como lo que no buscas tambien esta "
    "aqui. Ambos, lo deseado y lo no deseado existen y asi sera siempre. "
    "Tranquiliza tu corazon que mientras parezca todo perdido, la llama de "
    "aquello deseado no se apagara."
)

TAO_DISCLAIMER = (
    "Las respuestas disponibles son siempre aproximaciones, nunca reflejo "
    "total de lo real. La respuesta genuina es la que cada persona o grupo "
    "logre construir para si mismo. Este modulo facilita una reflexion sobre "
    "la dimension interior del cambio transformativo que implica transicionar "
    "desde patrones degenerativos hacia patrones regenerativos. "
    "Desde la perspectiva del taoismo filosofico, cada paso hacia lo esencial "
    "es ya expresion de la virtud regenerativa en accion."
)

TAO_DIMENSIONES = [
    {
        "id": "tao_d1_wu_wei",
        "titulo": "Accion espontanea y oportuna",
        "subtitulo": "Wu wei, flexibilidad, oportunidad, no imposicion",
        "icono": "1",
        "cita_tao": "El sabio se ocupa de no actuar y ensena sin palabras. Las diez mil cosas surgen y el no las rechaza. Produce sin poseer. Actua sin esperar nada. Cuando la obra esta cumplida, no se apega a ella. Y precisamente por no apegarse, la obra perdura.",
        "cita_cap": "Tao Te Ching, Capitulo 2",
        "cita_extra": "Lo blando y lo flexible es discipulo de la vida. Lo duro y lo rigido es discipulo de la muerte.",
        "cita_extra_cap": "Capitulo 76",
        "descripcion": (
            "Quien camina por la via de la regeneracion reconoce que la naturaleza "
            "tiene su ritmo y actua en conciencia de ese ritmo, respetandolo y sin "
            "pretender controlarlo ni forzarlo. Sigue el Wu Wei, la no-accion: una "
            "forma de actuar que no empuja los acontecimientos, sino que los acompana "
            "como el agua que fluye desde la montana y con la constancia a traves del "
            "tiempo logra crear valles llenos de abundancia y vida.\n\n"
            "No-accion es lo contrario a permanecer paralizados. Es como la de quien "
            "navega y pone las velas en la posicion adecuada para tomar el viento a "
            "favor. Regenerar es doblarse sin romperse. Quien guia un proceso "
            "regenerativo no busca reconocimiento; su poder esta en la coherencia, "
            "en la capacidad de ceder el paso para que la tierra y las personas "
            "encuentren su propio equilibrio.\n\n"
            "En la practica, esto significa disenar sistemas de vida que se adapten "
            "a la variabilidad del clima y, en lo social, evitar la confrontacion "
            "esteril con quienes aun actuan desde la logica degenerativa. Como las "
            "abejas, que no actuan buscando reconocimiento: actuan siguiendo un "
            "impulso que les permite nutrir a sus nuevas generaciones mientras "
            "favorecen la polinizacion y el aumento de la biodiversidad."
        ),
        "pregunta": (
            "En que medida nuestras decisiones e intervenciones en el espacio surgen "
            "de la observacion paciente y se realizan en el momento oportuno, sin "
            "imponer ritmos externos ni forzar resultados?"
        ),
        "opciones": [
            "Forzamos continuamente; ignoramos los ciclos naturales, actuamos con prisa o fuera de tiempo.",
            "A veces observamos, pero predominan las imposiciones y los calendarios ajenos al lugar.",
            "Hay momentos de accion oportuna, pero tambien tensiones entre el querer hacer y el fluir.",
            "Generalmente respetamos los tiempos de la tierra y de las personas; intervenimos con suavidad.",
            "Actuamos desde una accion que no busca persuadir ni controlar (wu wei): guia desde el ejemplo y solo acompana cuando es necesario.",
        ],
    },
    {
        "id": "tao_d2_humildad",
        "titulo": "Humildad y suficiencia",
        "subtitulo": "Estar abajo, detenerse a tiempo, sencillez",
        "icono": "2",
        "cita_tao": "No hay mayor desgracia que no saber que es suficiente. No hay mayor defecto que el afan de obtener. Quien sabe que lo suficiente es suficiente, siempre tendra suficiente.",
        "cita_cap": "Tao Te Ching, Capitulo 46",
        "cita_extra": "Mejor es detenerse a tiempo que llenar hasta el borde. Retirarse cuando la obra esta cumplida: ese es el camino del cielo.",
        "cita_extra_cap": "Capitulo 9",
        "descripcion": (
            "La regeneracion surge desde abajo, desde el nivel de cada agente "
            "regenerativo que ejerce acciones concretas. Quien regenera se situa al "
            "servicio del territorio, aprende de los saberes ecologicos y de la "
            "naturaleza en general: de los ciclos del agua, de las plantas, del sol. "
            "No llega como un salvador externo, sino como un facilitador que escucha.\n\n"
            "Frente a la cultura del crecimiento infinito, en permacultura se promueve "
            "el descenso creativo: no acumular mas de lo necesario, saber cuando parar, "
            "reconocer los limites. Reducir lo superfluo, optar por lo local, lo manual, "
            "lo duradero, es un acto de liberacion.\n\n"
            "Los tres tesoros del Tao -- compasion, moderacion y humildad -- tienen "
            "aqui su anclaje: la moderacion permite vivir con lo justo y frenar la "
            "huella ecologica; la humildad impide pretender ser el primero y deja "
            "espacio a otros, a la naturaleza, a las futuras generaciones."
        ),
        "pregunta": (
            "En que medida practicamos la humildad -- escuchando mas que imponiendo -- "
            "y reconocemos lo suficiente, sin acumular mas de lo necesario, "
            "deteniendonos a tiempo?"
        ),
        "opciones": [
            "Actuamos desde la certeza de tener todas las respuestas; acumulamos sin limite ni reflexion.",
            "Escuchamos poco; la ambicion de crecimiento o de resultados nos impulsa a no detenernos.",
            "A veces nos detenemos, pero la cultura del tener mas suele ganar; aun cuesta ceder el protagonismo.",
            "Frecuentemente ponemos el saber de la naturaleza y del lugar por delante, y sabemos decir basta.",
            "Nuestra presencia es humilde y genuina; celebramos la suficiencia y nos retiramos cuando el sistema florece solo.",
        ],
    },
    {
        "id": "tao_d3_compasion",
        "titulo": "Compasion y no-juicio",
        "subtitulo": "Inclusividad, verdad sobria, compasion",
        "icono": "3",
        "cita_tao": "Tengo tres tesoros que guardo y atesoro. El primero es la compasion. El segundo, la moderacion. El tercero, no atreverme a ser el primero bajo el cielo. Por la compasion se puede ser valiente.",
        "cita_cap": "Tao Te Ching, Capitulo 67",
        "cita_extra": "El sabio es siempre buen salvador de las personas, por eso no abandona a nadie. La persona que no es buena es materia prima de la buena.",
        "cita_extra_cap": "Capitulo 27",
        "descripcion": (
            "La compasion es la primera joya del sabio taoista: actuar con cuidado "
            "hacia todos los seres, humanos y no humanos, sin danar. En la regeneracion, "
            "esto se traduce en no abandonar a nadie, incluso a quienes hoy actuan "
            "de modo degenerativo.\n\n"
            "Los seres humanos somos interdependientes: la presencia del otro y sus "
            "acciones tienen impacto en las nuestras. La persona que no camina por el "
            "sendero de la regeneracion no es un enemigo a combatir, sino materia prima "
            "de la transformacion. La tarea regenerativa no es solo condenar ni exigir "
            "cambios, sino ofrecer condiciones para que la semilla de retorno hacia una "
            "vida regenerativa germine en cada persona.\n\n"
            "La comunicacion en proyectos regenerativos huye de la retorica vacia y "
            "del marketing verde. Nombra las dificultades con transparencia, celebra "
            "los logros sin apropiarselos. Las palabras verdaderas no son hermosas; "
            "las hermosas no son verdaderas (Cap. 81)."
        ),
        "pregunta": (
            "En que medida somos capaces de relacionarnos sin juicios con quienes "
            "tienen practicas o perspectivas distintas, y de sostener una comunicacion "
            "honesta, sin manipulacion ni protagonismo?"
        ),
        "opciones": [
            "Predominan los prejuicios, las etiquetas y la comunicacion agresiva o enganosa.",
            "Con frecuencia separamos entre nosotros y ellos; la verdad se doblega ante la conveniencia.",
            "A veces logramos una mirada amplia, pero recaemos en la condena; la comunicacion es sincera solo en temas seguros.",
            "Mantenemos una postura de apertura y una comunicacion que busca la transparencia, incluso en los desacuerdos.",
            "No excluimos a nadie; nuestro dialogo es compasivo y honesto, sin necesidad de vendernos a nosotros mismos ni a nuestro proyecto.",
        ],
    },
    {
        "id": "tao_d4_esencial",
        "titulo": "Fortalecer lo esencial",
        "subtitulo": "Cuidar el interior, deseo reducido, raiz frente a apariencia",
        "icono": "4",
        "cita_tao": "Los cinco colores ciegan los ojos del hombre. Los cinco sabores estragan su paladar. Por eso el sabio se ocupa del vientre, no de los ojos. Elige lo interior y rechaza lo exterior.",
        "cita_cap": "Tao Te Ching, Capitulo 12",
        "cita_extra": "La virtud superior no actua y no tiene proposito. El hombre superior se ocupa de lo grueso, no de lo fino. Se atiene al fruto, no a la flor.",
        "cita_extra_cap": "Capitulo 38",
        "descripcion": (
            "La regeneracion no se agota en lo que se ve. Atiende a lo esencial "
            "-- la salud de las relaciones, la cohesion grupal, el bienestar interior -- "
            "antes que a las formas externas que deslumbran. Un proyecto es verdaderamente "
            "regenerativo si quienes participan se sienten mas vivos, mas conectados, "
            "mas en paz.\n\n"
            "Esto requiere un trabajo sobre el deseo: reducir lo superfluo para dejar "
            "espacio a lo que nutre. No se trata de ascetismo, sino de discernir entre "
            "lo accesorio y lo profundo. En lo colectivo, significa disenar soluciones "
            "pequenas y apropiadas antes que grandes infraestructuras; en lo personal, "
            "soltar el afan de poseer, controlar o acumular reconocimiento.\n\n"
            "Si la raiz esta sana, el fruto sera duradero. Por eso quien regenera "
            "cuida primero la calidad de su presencia, la escucha, la capacidad de "
            "estar presente sin forzar."
        ),
        "pregunta": (
            "En que medida priorizamos lo esencial -- cohesion, bienestar, calidad "
            "de las relaciones -- sobre lo superficial -- resultados visibles, "
            "infraestructura, reconocimiento externo?"
        ),
        "opciones": [
            "Solo nos importan los resultados externos; el bienestar interno se descuida o se ignora.",
            "Lo visible prima; lo esencial se atiende solo cuando surge una crisis.",
            "Hay conciencia de la importancia de las relaciones, pero lo externo suele llevarse la mayor atencion y energia.",
            "El cuidado de la raiz -- personas, relaciones, salud grupal -- es tan importante como los frutos visibles.",
            "Todo lo que hacemos nace de lo esencial; las formas externas son un reflejo natural de la armonia interior.",
        ],
    },
    {
        "id": "tao_d5_retorno",
        "titulo": "Retorno a la raiz",
        "subtitulo": "Anclaje en los ciclos naturales y comunitarios",
        "icono": "5",
        "cita_tao": "Todas las cosas florecen, y cada una retorna a su raiz. Retornar a la raiz es la quietud. La quietud es retornar al destino. Retornar al destino es lo constante. Conocer lo constante es la iluminacion.",
        "cita_cap": "Tao Te Ching, Capitulo 16",
        "cita_extra": "Cultiva la virtud en ti mismo y la virtud sera genuina. Cultivala en la familia y sera abundante. Cultivala en la aldea y sera duradera.",
        "cita_extra_cap": "Capitulo 54",
        "descripcion": (
            "Regenerar es volver a los patrones primordiales: el ciclo del agua, "
            "la sucesion ecologica, la red simbiotica, la comunidad de apoyo mutuo. "
            "La raiz es el Tao mismo, fuente inagotable de vida. Quien regenera "
            "actua como un canal de esa fuerza, sabiendo que no es el dueno, sino "
            "un humilde participante del retorno.\n\n"
            "Este retorno no es nostalgia, sino anclaje. En la practica, se expresa "
            "en la observacion de los ciclos: cuando sembrar, cuando podar, cuando "
            "esperar. Tambien en la memoria de los saberes locales y en la recuperacion "
            "de practicas tradicionales que han sostenido la vida durante siglos.\n\n"
            "Regenerar es plantar el Tao -- en la huerta, en el grupo, en la vida "
            "cotidiana -- para que su virtud florezca en todas las escalas. Cada "
            "accion regenerativa es un paso de retorno a lo esencial, una danza que "
            "alinea la voluntad humana con la inteligencia de la vida."
        ),
        "pregunta": (
            "En que medida nuestras actividades cotidianas y decisiones de diseno "
            "se basan en los ciclos de la naturaleza, los saberes del lugar y los "
            "procesos ecologicos de regeneracion?"
        ),
        "opciones": [
            "Ignoramos los ciclos naturales y la historia del lugar; nuestras practicas son ajenas al territorio.",
            "Tenemos cierta sensibilidad ecologica, pero aun funcionamos con logicas externas al lugar.",
            "Incorporamos algunos ciclos y saberes locales, pero de forma parcial o intermitente.",
            "La mayoria de nuestras decisiones se guian por los ritmos naturales y la memoria del lugar.",
            "Somos un canal de la inteligencia del lugar: cada accion honra los ciclos y profundiza el retorno a lo esencial.",
        ],
    },
]

TAO_INTEGRACION = (
    "Estas cinco dimensiones no son compartimentos estancos. La accion espontanea "
    "y oportuna solo es posible cuando se habita la humildad y la suficiencia; "
    "la compasion y el no-juicio encuentran su fuerza en fortalecer lo esencial; "
    "y todo ello confluye en el retorno a la raiz. Regenerar es, en el fondo, "
    "dejar que esa virtud actue a traves nuestro -- sin forzar, sin poseer, sin "
    "reclamar -- confiando en que la vida, cuando se le da espacio, siempre retorna."
)

TAO_INVITACION = (
    "Este diagnostico es solo un momento dentro de un proceso mucho mas amplio. "
    "Cada espacio tiene su propio ritmo de transformacion. "
    "A veces la regeneracion comienza con algo pequeno: un huerto, un sistema "
    "de compostaje, una conversacion comunitaria. Lo importante es seguir caminando.\n\n"
    "Si deseas continuar profundizando este proceso, puedes conocer mas sobre "
    "el trabajo de LivLin en www.livlin.cl."
)

TAO_DIM_LABELS = [d["titulo"] for d in TAO_DIMENSIONES]
TAO_DIM_IDS = [d["id"] for d in TAO_DIMENSIONES]


# ========================================================================
# FUNCION RENDER PRINCIPAL
# ========================================================================

def render():
    import streamlit as st
    from utils.data_manager import save_visit
    from utils.module_status import render_module_status, is_module_active
    from utils.module_status import is_readonly as _is_ro, render_readonly_notice
    from utils.tab_nav import show_drive_save_status
    _readonly = _is_ro()
    if _readonly:
        render_readonly_notice()

    st.markdown("## Tao de la Regeneracion")
    st.markdown(
        '<p class="module-subtitle">Cinco dimensiones de sabiduria taoista para '
        'acompanar el camino de la virtud regenerativa.</p>', unsafe_allow_html=True)

    with st.expander("Que es el Tao de la Regeneracion? (clic para leer)", expanded=False):
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
            '📖 <a href="https://drive.google.com/file/d/1JAWwhCOyvZKrACoAk5bv5Jh2thxppLZh/view" target="_blank">Tao Te Ching — Texto completo en espanol (PDF)</a><br>'
            '📖 <a href="https://drive.google.com/file/d/1MLOLcIso_inxbpIaoJfcdrZimVl9xHgj/view?usp=sharing" target="_blank">Mason, F. (2026) El Tao para una vida regenerativa — LivLin</a><br>'
            '📖 <a href="https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing" target="_blank">Mason, F. (2025) Introduccion al enfoque de la regeneracion — LivLin</a>'
            '</div>', unsafe_allow_html=True)

    data = st.session_state.visit_data

    st.markdown("**Estado de este modulo:**")
    _mod_status = render_module_status(data, "mod_tao")
    if not is_module_active(_mod_status):
        from utils.module_status import render_not_addressed_notice
        render_not_addressed_notice(data, "mod_tao", _readonly)
        return


    if _mod_status == "inferido":
        st.info("**Modo inferido** -- Las respuestas abajo son interpretaciones del facilitador, no de las personas del espacio.")
    st.markdown("---")

    # -- Las 5 dimensiones --
    for i, dim in enumerate(TAO_DIMENSIONES):
        st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"### Dimension {dim['icono']}: {dim['titulo']}")
        st.markdown(f"*{dim['subtitulo']}*")

        # Primary quote
        st.markdown(
            f'<div style="background:#F0FFF4;border-radius:8px;padding:0.6rem 0.8rem;'
            f'margin:0.5rem 0;border-left:3px solid #40916C;">'
            f'<em style="color:#2D6A4F;font-size:0.85rem;">&laquo;{dim["cita_tao"]}&raquo;</em><br>'
            f'<span style="font-size:0.75rem;color:#666;">-- {dim["cita_cap"]}</span>'
            f'</div>', unsafe_allow_html=True)

        # Description (convert \n\n to paragraph breaks)
        desc_html = dim["descripcion"].replace("\n\n", "</p><p style='font-size:0.88rem;color:#333;margin:0.3rem 0;'>")
        st.markdown(
            f'<p style="font-size:0.88rem;color:#333;margin:0.5rem 0;">{desc_html}</p>',
            unsafe_allow_html=True)

        # Extra quote (if available)
        if dim.get("cita_extra"):
            st.markdown(
                f'<div style="background:#FAFAFA;border-radius:6px;padding:0.4rem 0.7rem;'
                f'margin:0.3rem 0;border-left:2px solid #A8D5B5;">'
                f'<em style="color:#555;font-size:0.8rem;">&laquo;{dim["cita_extra"]}&raquo;</em>'
                f' <span style="font-size:0.72rem;color:#888;">-- {dim.get("cita_extra_cap","")}</span>'
                f'</div>', unsafe_allow_html=True)

        # Reflection question
        st.markdown(
            f'<div style="background:#E8F5E9;border-radius:8px;padding:0.6rem 0.8rem;'
            f'margin:0.5rem 0;">'
            f'<strong style="color:#1B4332;">Pregunta de reflexion:</strong><br>'
            f'<em style="color:#2D6A4F;">{dim["pregunta"]}</em></div>',
            unsafe_allow_html=True)

        current_val = data.get(dim["id"], 0)
        if isinstance(current_val, str):
            try:
                current_val = int(current_val)
            except (ValueError, TypeError):
                current_val = 0

        opciones_display = [f"{j+1}. {opt}" for j, opt in enumerate(dim["opciones"])]
        opciones_con_nr = ["Sin responder"] + opciones_display

        idx = 0
        if 1 <= current_val <= 5:
            idx = current_val

        if not _readonly:
            sel = st.radio(
                f"Seleccione el nivel que mejor describe su situacion actual:",
                opciones_con_nr,
                index=idx,
                key=f"radio_{dim['id']}",
                horizontal=False,
            )
            if sel == "Sin responder":
                data[dim["id"]] = 0
            else:
                data[dim["id"]] = opciones_con_nr.index(sel)
        else:
            if current_val > 0:
                st.markdown(f"**Respuesta seleccionada:** {opciones_display[current_val-1]}")
            else:
                st.markdown("*Sin responder*")

        st.markdown("</div>", unsafe_allow_html=True)

    # -- Integracion --
    st.markdown("---")
    with st.expander("Integracion: el camino de la virtud regenerativa", expanded=False):
        st.markdown(TAO_INTEGRACION)

    # -- Radar preview --
    valores = [data.get(d["id"], 0) for d in TAO_DIMENSIONES]
    valores_int = []
    for v in valores:
        try:
            valores_int.append(int(v))
        except (ValueError, TypeError):
            valores_int.append(0)

    if any(v > 0 for v in valores_int):
        st.markdown("### Vista previa del Radar Tao")
        _render_tao_radar(valores_int, compact=False)

    # -- Notas --
    data["tao_notas"] = st.text_area(
        "Notas del Tao de la Regeneracion",
        value=data.get("tao_notas", ""), height=80)

    st.markdown("---")
    _, col_b, _ = st.columns([2, 1, 2])
    with col_b:
        if not _readonly:
            if st.button("Guardar Tao", use_container_width=True, type="primary"):
                vid = save_visit(data)
                data["id"] = vid
                st.session_state.visit_data = data
                st.success("Guardado.")


# ========================================================================
# RADAR CHART (reutilizable desde report.py)
# ========================================================================

def _render_tao_radar(valores, compact=True):
    """Render radar chart for the 5 Tao dimensions. valores = list of 5 ints (0-5)."""
    import streamlit as st
    import plotly.graph_objects as go

    labels = [d["titulo"] for d in TAO_DIMENSIONES]
    vals = list(valores) + [valores[0]]
    cats = list(labels) + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor='rgba(45,105,78,0.15)',
        line=dict(color='#2D6A4F', width=2),
        marker=dict(size=6, color='#1B4332'),
        name='Estado actual',
    ))
    fig.add_trace(go.Scatterpolar(
        r=[5]*6, theta=cats, fill=None,
        line=dict(color='#A8D5B5', width=1, dash='dot'),
        name='Maximo',
    ))

    height = 320 if compact else 420
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickvals=[1,2,3,4,5],
                            tickfont=dict(size=9), gridcolor='#E8F5E9'),
            angularaxis=dict(tickfont=dict(size=10 if compact else 11)),
            bgcolor='rgba(255,255,255,0)',
        ),
        showlegend=False,
        margin=dict(l=60, r=60, t=30, b=30),
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    filled = [v for v in valores if v > 0]
    if filled:
        avg = sum(filled) / len(filled)
        total = sum(valores)
        label = get_tao_label(total)
        st.markdown(
            f'<div style="text-align:center;padding:0.4rem;background:#F0FFF4;'
            f'border-radius:8px;font-size:0.85rem;color:#1B4332;">'
            f'Puntaje total: <strong>{total}/25</strong> &nbsp; | &nbsp; '
            f'Promedio: <strong>{avg:.1f}/5</strong> &nbsp; | &nbsp; '
            f'Nivel: <strong>{label}</strong></div>',
            unsafe_allow_html=True)


def get_tao_scores(data):
    """Return dict with scores for external use."""
    scores = {}
    for dim in TAO_DIMENSIONES:
        v = data.get(dim["id"], 0)
        try:
            scores[dim["id"]] = int(v)
        except (ValueError, TypeError):
            scores[dim["id"]] = 0
    return scores


def get_tao_total(data):
    """Return total Tao score (0-25)."""
    return sum(get_tao_scores(data).values())


def get_tao_label(total):
    """Return interpretive label for total score."""
    if total == 0:
        return "Sin evaluar"
    if total <= 5:
        return "Inicio del camino"
    if total <= 10:
        return "Semilla interior"
    if total <= 15:
        return "Brote consciente"
    if total <= 20:
        return "Crecimiento armonico"
    return "Virtud regenerativa"
