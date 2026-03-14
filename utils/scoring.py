"""Lógica de puntaje regenerativo v6 — 7 pétalos oficiales Holmgren con descripciones extendidas."""

FLOWER_DOMAINS = {
    "Educación y Cultura": {
        "icon": "📚", "petal_num": 1, "color": "#7B61FF",
        "desc": "Educación viva, saberes locales, cultura regenerativa y transmisión intergeneracional",
        "long_desc": (
            "**El pétalo de Cultura y Educación** reconoce que toda transformación duradera comienza en la mente y el corazón. "
            "No se trata de la educación formal de los libros —aunque esa tiene su lugar— sino del aprendizaje vivo que ocurre "
            "en el jardín, en la cocina, compartiendo semillas, observando la lluvia o conversando alrededor de un compostero. "
            "Una comunidad que aprende junta, que valora los saberes locales y ancestrales, que transmite sus conocimientos entre "
            "generaciones, construye una cultura regenerativa resiliente. Este pétalo evalúa si el espacio es una fuente activa "
            "de aprendizaje, si sus conocimientos se comparten hacia afuera y si la educación ambiental es parte de la vida cotidiana. "
            "Recuerda: cada conversación sobre por qué compostar, cada niño que planta una semilla por primera vez, "
            "es un acto de cultura regenerativa."
        ),
        "areas": "Educación en contexto real · Saberes locales · Arte y música participativa · Intercambio de conocimiento",
        "indicators": [
            {"key": "fl_p1_conocimiento", "label": "Conocimiento permacultural activo",
             "help": "El grupo conoce y aplica principios de permacultura en su cotidiano"},
            {"key": "fl_p1_interes", "label": "Interés por aprendizaje colectivo",
             "help": "Disposición a aprender juntos/as sobre ecología, diseño y vida regenerativa"},
            {"key": "fl_p1_generacional", "label": "Transmisión intergeneracional",
             "help": "Participación de niños/as, jóvenes y adultos mayores en el aprendizaje del espacio"},
            {"key": "fl_p1_saberes_loc", "label": "Valoración de saberes locales",
             "help": "Reconocimiento y uso de conocimientos tradicionales, locales y ancestrales"},
            {"key": "fl_p1_formacion", "label": "Formación activa (talleres, cursos, lecturas)",
             "help": "Participación en talleres, cursos, grupos de estudio o lectura sobre temas regenerativos"},
            {"key": "fl_p1_compartir", "label": "Compartir y difundir aprendizajes",
             "help": "El grupo comparte sus experiencias con vecinos, redes o comunidades externas"},
        ]
    },
    "Entorno Construido": {
        "icon": "🏡", "petal_num": 2, "color": "#2D9596",
        "desc": "Bioarquitectura, bioclimática, materiales naturales y relación espacial con los ciclos vivos",
        "long_desc": (
            "**El pétalo del Entorno Construido** aborda la relación entre nuestros espacios físicos y los sistemas naturales. "
            "Los edificios y estructuras que habitamos pueden ser aliados o enemigos de la vida: consumen energía, generan residuos "
            "y fragmentan ecosistemas —o pueden captar agua, generar hábitat, regular la temperatura y albergar biodiversidad. "
            "El diseño bioclimático aprovecha el sol en invierno, la ventilación en verano, la inercia térmica de los muros. "
            "Los materiales naturales y locales —tierra, madera, piedra, bambú, adobe— tienen una huella de carbono mínima y "
            "se integran al ciclo de la vida. Los techos verdes, jardines verticales, pérgolas con plantas y muros vivos "
            "son extensiones del ecosistema hacia la ciudad. Este pétalo evalúa qué tan vivo está el espacio construido: "
            "si respira, si trabaja con el clima, si los materiales cuentan una historia local."
        ),
        "areas": "Bioarquitectura · Bioclimática · Materiales naturales · Autoconstrucción",
        "indicators": [
            {"key": "fl_p2_bioclimatica", "label": "Diseño bioclimático",
             "help": "Aprovechamiento pasivo de sol, viento y agua en el diseño del espacio construido"},
            {"key": "fl_p2_materiales", "label": "Materiales naturales y locales",
             "help": "Uso de tierra, madera, bambú, piedra u otros materiales de bajo impacto"},
            {"key": "fl_p2_infra_verde", "label": "Infraestructura verde integrada",
             "help": "Techos verdes, muros vivos, pérgolas vegetadas, jardines verticales"},
            {"key": "fl_p2_eficiencia", "label": "Eficiencia del uso del espacio",
             "help": "Zonificación, multifuncionalidad y aprovechamiento de todas las superficies"},
            {"key": "fl_p2_confort", "label": "Confort sin energía artificial",
             "help": "Temperatura y humedad agradables logradas por diseño, no por climatización"},
        ]
    },
    "Herramientas y Tecnología": {
        "icon": "🛠️", "petal_num": 3, "color": "#8B5E3C",
        "desc": "Tecnología apropiada, eficiencia energética, bicicletas, reutilización y redes de intercambio",
        "long_desc": (
            "**El pétalo de Herramientas y Tecnología** invita a preguntarse: ¿qué tecnologías nos sirven realmente y a qué costo? "
            "La permacultura no rechaza la tecnología —la cuestiona y selecciona. Prefiere la herramienta simple y duradera "
            "a la compleja y dependiente. Prioriza lo que puede ser reparado localmente, lo que no genera dependencias "
            "ni residuos tóxicos. Una bicicleta, un compostero bien diseñado, un sistema de captación de agua con cañerías "
            "de PVC reciclado, un panel solar de bajo consumo: esas son tecnologías apropiadas. "
            "Este pétalo también incluye las redes de intercambio —LETS, bancos de tiempo, grupos de trueque— que son "
            "tecnologías sociales de alta eficiencia. Evalúa si el grupo usa herramientas acordes a su escala, "
            "si reutiliza materiales, si comparte herramientas con vecinos/as, si prefiere lo manual cuando puede."
        ),
        "areas": "Tecnología apropiada · Herramientas manuales · Reutilizar/Reciclar · LETS · WWOOFing",
        "indicators": [
            {"key": "fl_p3_tec_apropiada", "label": "Tecnología apropiada al contexto",
             "help": "Herramientas acordes a la escala, necesidades y recursos disponibles"},
            {"key": "fl_p3_herramientas", "label": "Herramientas manuales y no motorizadas",
             "help": "Uso prioritario de herramientas manuales, bicicletas, tracción animal"},
            {"key": "fl_p3_reutilizar", "label": "Reutilización y reciclaje activo",
             "help": "Práctica concreta de reutilizar materiales, envases, pallets, telas, etc."},
            {"key": "fl_p3_energia", "label": "Eficiencia y energías renovables",
             "help": "Reducción activa del consumo energético; uso de solar, biomasa u otras fuentes"},
            {"key": "fl_p3_intercambio", "label": "Participación en redes de intercambio",
             "help": "LETS, bancos de tiempo, trueque, grupos de compra colectiva"},
        ]
    },
    "Salud y Bienestar Espiritual": {
        "icon": "🧘", "petal_num": 4, "color": "#A67C00",
        "desc": "Prevención, medicina holística, educación vital, artes y cuidado integral del ser",
        "long_desc": (
            "**El pétalo de Salud y Bienestar Espiritual** reconoce que no puede haber regeneración exterior sin bienestar interior. "
            "La salud, en este pétalo, no es solo la ausencia de enfermedad: es vitalidad, conexión, propósito y alegría. "
            "Incluye hábitos de vida saludable, alimentación consciente, movimiento, descanso y plantas medicinales. "
            "Pero también incluye la dimensión espiritual: la meditación, la contemplación, la gratitud, el ritual, la conexión "
            "con lo sagrado en la naturaleza. Las artes, la música, la danza, la expresión creativa son igualmente parte de "
            "este pétalo: nutren el alma y fortalecen los lazos comunitarios. "
            "En permacultura, el cuidado de las personas —incluyendo a una misma— es tan importante como el cuidado de la tierra. "
            "Este pétalo evalúa si el espacio nutre el bienestar integral: si las personas que lo habitan están bien, "
            "si hay alegría, creatividad y conexión profunda con la naturaleza como raíz de toda acción."
        ),
        "areas": "Medicina holística · Educación viva · Música y artes · Cuidado personal y comunitario",
        "indicators": [
            {"key": "fl_p4_prevencion", "label": "Prevención y hábitos saludables",
             "help": "Prácticas activas de alimentación, movimiento y descanso"},
            {"key": "fl_p4_medicina_hol", "label": "Medicina holística y plantas medicinales",
             "help": "Uso de plantas medicinales, remedios naturales u otras medicinas no convencionales"},
            {"key": "fl_p4_educacion", "label": "Educación viva y aprendizaje activo",
             "help": "Aprendizaje en contexto real, talleres prácticos, educación en casa"},
            {"key": "fl_p4_artes", "label": "Artes, música y expresión creativa",
             "help": "Presencia de artes participativas, música, artesanía en el espacio"},
            {"key": "fl_p4_bienestar", "label": "Bienestar emocional y espiritual",
             "help": "Prácticas activas de meditación, contemplación o conexión espiritual"},
        ]
    },
    "Finanzas y Economía": {
        "icon": "💚", "petal_num": 5, "color": "#2D6A4F",
        "desc": "Finanzas éticas, autosuficiencia, comercio justo y soberanía económica del grupo",
        "long_desc": (
            "**El pétalo de Economía y Finanzas** cuestiona la economía extractiva y propone un modelo basado en la abundancia "
            "real: alimentos propios, energía local, intercambio justo y ahorro genuino. La permacultura plantea que la "
            "verdadera riqueza es la autosuficiencia —no depender de sistemas que contaminan, explotan y concentran poder. "
            "Las finanzas éticas son aquellas que apoyan proyectos regenerativos: cooperativas de crédito, bancos éticos, "
            "inversiones en energía solar y agroecología. El comercio justo garantiza que los productores reciban un precio "
            "digno. La agricultura compartida (CSA) conecta directamente a productores y consumidores. "
            "El trueque y los mercados locales reducen la cadena de intermediarios. "
            "Este pétalo evalúa si el grupo está construyendo soberanía económica: si produce para autoabastecerse, "
            "si toma decisiones de consumo conscientes, si sus excedentes circulan en la comunidad en lugar de en el supermercado."
        ),
        "areas": "Contabilidad de la energía · Inversión ética · Comercio justo · Agricultura compartida",
        "indicators": [
            {"key": "fl_p5_autosufic", "label": "Autosuficiencia alimentaria",
             "help": "Producción propia de alimentos para el consumo del grupo"},
            {"key": "fl_p5_finanzas_eticas", "label": "Finanzas éticas e inversión consciente",
             "help": "Decisiones de consumo e inversión alineadas con valores ecológicos"},
            {"key": "fl_p5_comercio_justo", "label": "Comercio justo y consumo responsable",
             "help": "Compra de productos con certificación justa, apoyo a productores locales"},
            {"key": "fl_p5_excedentes", "label": "Gestión de excedentes productivos",
             "help": "Donación, intercambio o venta de excedentes de producción propia"},
            {"key": "fl_p5_autoproduccion", "label": "Reducción de dependencia del mercado",
             "help": "Nivel de autoabastecimiento: alimentos, energía, agua, materiales"},
        ]
    },
    "Tenencia de la Tierra y Gobernanza Comunitaria": {
        "icon": "🤝", "petal_num": 6, "color": "#1A6B6B",
        "desc": "Gobernanza colectiva, administración de la tierra, cooperativas y resolución de conflictos",
        "long_desc": (
            "**El pétalo de Tenencia de la Tierra y Comunidad** aborda una de las preguntas más profundas de la permacultura: "
            "¿quién tiene derecho a la tierra, cómo se decide, y cómo se cuida colectivamente? En un mundo donde la tierra "
            "es un activo financiero, la permacultura propone reconectarla con su función ecológica y comunitaria. "
            "Las ecoaldeas, los trusts de tierra, los huertos comunitarios, las cooperativas de vivienda y los cohousing "
            "son modelos concretos donde la tenencia colectiva permite la regeneración a largo plazo. "
            "La gobernanza no violenta —toma de decisiones por consenso, facilitación de conflictos, comunicación no violenta— "
            "es la base de cualquier comunidad regenerativa duradera. "
            "Este pétalo también incluye la investigación-acción: sistematizar y compartir lo aprendido para que otras "
            "comunidades puedan aprender de la experiencia. Evalúa si el espacio tiene acuerdos claros, si los conflictos "
            "se resuelven con sabiduría, si el vínculo con el territorio es de largo plazo y de cuidado mutuo."
        ),
        "areas": "Cooperativas · Ecoaldeas · Co-housing · Resolución de conflictos · Ecología Social",
        "indicators": [
            {"key": "fl_p6_gobernanza", "label": "Modelos de tenencia y gobernanza",
             "help": "Acuerdos formales o informales sobre el uso colectivo de la tierra"},
            {"key": "fl_p6_cooperativas", "label": "Cooperativas o gestión colectiva",
             "help": "Pertenencia o impulso a cooperativas, asociaciones de vecinos"},
            {"key": "fl_p6_conflictos", "label": "Resolución no violenta de conflictos",
             "help": "Procesos concretos y herramientas para resolver diferencias sin violencia"},
            {"key": "fl_p6_red_comunit", "label": "Vínculo comunitario activo",
             "help": "Relaciones sólidas con vecinos, barrio, red ecológica u otras comunidades"},
            {"key": "fl_p6_investigacion", "label": "Investigación-acción y documentación",
             "help": "Registro, sistematización y compartición de aprendizajes del proceso"},
        ]
    },
    "Administración de la Tierra y la Naturaleza": {
        "icon": "🌳", "petal_num": 7, "color": "#40916C",
        "desc": "Sistemas regenerativos: bosques comestibles, semillas, agua, agroforestería y lectura del paisaje",
        "long_desc": (
            "**El pétalo del Manejo de la Tierra y la Naturaleza** es el corazón productivo de la permacultura. "
            "Aquí se diseñan los sistemas que imitan los bosques naturales: stratificados, biodiversos, resilientes y "
            "autosuficientes. El bosque comestible es el modelo más alto: un sistema de árboles, arbustos, herbáceas, "
            "coberturas y enredaderas que produce alimentos, medicinas, madera y hábitat con mínima intervención humana. "
            "La agroforestería integra árboles en los sistemas agrícolas, mejorando el microclima, protegiendo el suelo "
            "y diversificando la producción. La cosecha de agua en el paisaje —swales, terrazas, jardines de lluvia, "
            "depósitos— captura el agua donde cae y la infiltra lentamente en el suelo. "
            "La conservación de semillas es un acto de soberanía: guardar, intercambiar y multiplicar variedades locales "
            "adaptadas al territorio. La lectura del paisaje —observar los flujos de agua, los corredores de viento, "
            "los microclimas— es la base de todo diseño regenerativo. "
            "Este pétalo evalúa si el espacio está diseñado para imitar la naturaleza: si los ciclos están cerrados, "
            "si hay diversidad funcional, si el suelo mejora cada año y si la tierra da más vida de la que recibe."
        ),
        "areas": "Agroforestería · Bosques comestibles · Semillas · Captación de agua · Lectura del paisaje",
        "indicators": [
            {"key": "fl_p7_agroforesteria", "label": "Agroforestería y sistemas multistrata",
             "help": "Integración de árboles, arbustos, herbáceas y coberturas en estratos funcionales"},
            {"key": "fl_p7_semillas", "label": "Conservación e intercambio de semillas",
             "help": "Guardado, intercambio y multiplicación de semillas propias o locales"},
            {"key": "fl_p7_agua_cosecha", "label": "Captación y cosecha de agua en el paisaje",
             "help": "Swales, líneas clave, terrazas, depósitos, jardines de lluvia"},
            {"key": "fl_p7_biodiversidad", "label": "Policultivos y biodiversidad funcional",
             "help": "Cultivos combinados, plantas compañeras, cobertura del suelo"},
            {"key": "fl_p7_suelo_vivo", "label": "Suelo vivo y ciclos cerrados",
             "help": "Compostaje, vermicompost, bokashi, cobertura permanente, lombrices"},
        ]
    },
}

ETHICAL_PRINCIPLES = [
    {
        "key": "cuidado_tierra", "title": "🌍 Cuidado de la Tierra",
        "desc": "Toda vida en el planeta —suelo, agua, aire, plantas, animales— merece cuidado activo. No somos dueños de la tierra: somos parte de ella.",
        "questions": [
            ("eth_tierra_practicas",  "¿Qué hacen concretamente para cuidar la tierra en su espacio?",
             "Ej: Compostar, evitar pesticidas, plantar nativas, regenerar el suelo…"),
            ("eth_tierra_limitaciones", "¿Qué les impide cuidar más la tierra?",
             "Ej: Tiempo, recursos económicos, conocimiento técnico, espacio…"),
        ]
    },
    {
        "key": "cuidado_personas", "title": "💚 Cuidado de las Personas",
        "desc": "El bienestar de cada persona —empezando por uno mismo y el círculo más cercano— es la base de cualquier comunidad regenerativa.",
        "questions": [
            ("eth_personas_practicas", "¿Cómo cuidan el bienestar de las personas en el espacio?",
             "Ej: Espacios de descanso, prácticas compartidas, escucha activa, apoyo mutuo…"),
            ("eth_personas_desafios",  "¿Qué desafíos relacionales o comunitarios enfrentan?",
             "Ej: Diferencias de visión, falta de tiempo compartido, comunicación difícil…"),
        ]
    },
    {
        "key": "distribucion_justa", "title": "⚖️ Distribución Justa",
        "desc": "Los excedentes de producción —alimentos, energía, conocimiento, recursos— se comparten equitativamente dentro y fuera de la comunidad.",
        "questions": [
            ("eth_distribucion_excedentes", "¿Comparten excedentes con vecinos/as u otras comunidades?",
             "Ej: Regalamos tomates, compartimos semillas, prestamos herramientas…"),
            ("eth_distribucion_vision",     "¿Cómo les gustaría profundizar la distribución justa?",
             "Ej: Crear una caja común, organizar trueques, donar a olla comunitaria…"),
        ]
    },
]

SCORE_SCALE = {
    0: {"label": "Sin práctica aún — gran potencial",        "color": "#9E9E9E"},
    1: {"label": "🌱 Semilla — intención presente",           "color": "#52B788"},
    2: {"label": "🌿 Brote — iniciando el proceso",           "color": "#74C69D"},
    3: {"label": "🌳 Crecimiento — avanzando con fuerza",     "color": "#40916C"},
    4: {"label": "🌸 Florecer — práctica consolidada",        "color": "#2D6A4F"},
    5: {"label": "🌺 Abundancia — referente regenerativo",    "color": "#1B4332"},
}


def score_label(score: float) -> tuple:
    if score == 0:    return "🌱 Inicio del viaje — potencial enorme por revelar", "#9E9E9E"
    if score < 1.5:  return "🌱 Semilla — el terreno está listo para regenerar", "#52B788"
    if score < 2.5:  return "🌿 Brote — primeros pasos regenerativos en marcha", "#74C69D"
    if score < 3.5:  return "🌳 Crecimiento — el espacio florece hacia la regeneración", "#40916C"
    if score < 4.5:  return "🌸 Florecimiento — espacio regenerativo sólido y activo", "#2D6A4F"
    return "🌺 Abundancia — referente vivo de permacultura urbana", "#1B4332"


def compute_domain_scores(data: dict) -> dict:
    scores = {}
    for domain, meta in FLOWER_DOMAINS.items():
        vals = []
        for ind in meta["indicators"]:
            key = ind["key"]
            if data.get(f"{key}_na", False):
                continue
            v = data.get(key)
            if v is not None:
                try:
                    vals.append(float(v))
                except (ValueError, TypeError):
                    pass
        scores[domain] = round(sum(vals) / len(vals), 2) if vals else 0.0
    return scores


def compute_wellbeing_score(data: dict) -> float:
    keys = ["fl_p4_bienestar", "fl_p4_artes", "fl_p4_medicina_hol",
            "fl_p4_prevencion", "tao_conexion_tierra", "tao_practicas_bienestar"]
    vals = [float(data[k]) for k in keys if data.get(k) is not None]
    return round(sum(vals) / len(vals), 2) if vals else 0.0


def compute_regenerative_score(data: dict) -> float:
    domain_scores = compute_domain_scores(data)
    vals = [v for v in domain_scores.values() if v > 0]
    wb   = compute_wellbeing_score(data)
    if wb > 0:
        vals.append(wb)
    return round(sum(vals) / len(vals), 2) if vals else 0.0


def compute_synthesis_potentials(data: dict) -> dict:
    """Compute synthesis potentials from manually set values OR auto-calculated ones."""
    domain_sc = compute_domain_scores(data)
    wb_score  = compute_wellbeing_score(data)

    def _pot(key, domain=None, default=None):
        manual = data.get(key)
        if manual is not None:
            try:
                return float(manual)
            except (ValueError, TypeError):
                pass
        if domain and domain in domain_sc:
            return domain_sc[domain]
        return default or 0.0

    return {
        "Producción alimentaria":  _pot("sint_pot_alimentaria",  "Administración de la Tierra y la Naturaleza"),
        "Biodiversidad urbana":    _pot("sint_pot_biodiversidad", "Administración de la Tierra y la Naturaleza"),
        "Captación de agua":       _pot("sint_pot_agua",         "Herramientas y Tecnología"),
        "Regeneración del suelo":  _pot("sint_pot_suelo",        "Administración de la Tierra y la Naturaleza"),
        "Educación ambiental":     _pot("sint_pot_educacion",    "Educación y Cultura"),
        "Bienestar comunitario":   _pot("sint_pot_bienestar",    "Tenencia de la Tierra y Gobernanza Comunitaria"),
        "Economía regenerativa":   _pot("sint_pot_economia",     "Finanzas y Economía"),
        "Bienestar interior":      _pot("sint_pot_interior",     None, wb_score),
    }
