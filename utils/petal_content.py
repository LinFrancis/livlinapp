"""Contenido LivLin v3.3 — 7 pétalos Holmgren + marco regenerativo.
Fuentes: Holmgren (2002, 2020), Mason (2025), Mang & Reed (2012).
"""

# 7 pétalos oficiales de la Flor de la Permacultura (Holmgren, 2002)
PETAL_ICONS = ["🌳", "🏡", "🛠️", "📚", "🧘", "💚", "🤝"]

LIVLIN_URL     = "https://www.livlin.cl"
LIVLIN_TAGLINE = "Potencial para una vida regenerativa"
TOOL_NAME      = "Indagación Regenerativa"

LIVLIN_DESC = (
    "LivLin acompaña procesos de transformación regenerativa de espacios — urbanos, periurbanos y rurales —, "
    "guiando a personas, familias y comunidades hacia formas de vida más conectadas "
    "con los ciclos naturales, más autónomas y más significativas. "
    "A través de diagnósticos participativos, diseño regenerativo y acompañamiento "
    "continuo, trabajamos para convertir el potencial latente de cada espacio en "
    "prácticas concretas que mejoran la calidad de vida hoy y construyen resiliencia "
    "para las generaciones futuras."
)

LIVLIN_SERVICES_PITCH = (
    "Este diagnóstico es el primer paso de un proceso mayor. Con él en mano, tienes "
    "claridad sobre dónde está el potencial regenerativo de tu espacio y qué prácticas "
    "pueden transformarlo. Algunas puedes comenzarlas hoy mismo con tus propios recursos. "
    "Para las transformaciones más profundas — diseño integral, bioconstrucción, sistemas "
    "de captación de agua, instalaciones solares, formación comunitaria — el equipo de "
    "LivLin puede acompañarte con servicios especializados de diseño, implementación "
    "y seguimiento. Visítanos en www.livlin.cl"
)

LIVLIN_CLOSING = (
    "Cada práctica que sumas no solo transforma tu entorno: contribuye a la red de "
    "espacios regenerativos que van configurando nuevas formas de habitar la ciudad. "
    "El camino regenerativo es un proceso gradual, persistente y colectivo. "
    "LivLin te acompaña en ese proceso.\n"
    "www.livlin.cl · Potencial para una vida regenerativa."
)

REGENERATION_FRAMEWORK = (
    "La permacultura propone el 'diseño consciente de paisajes que imitan los patrones "
    "y relaciones de la naturaleza, mientras suministran alimento, fibras y energía "
    "para satisfacer las necesidades locales' (Holmgren, 2002). En contextos urbanos, "
    "este enfoque abre posibilidades extraordinarias: transformar patios, terrazas y "
    "espacios comunitarios en sistemas productivos que regeneran suelo, conservan agua "
    "y fortalecen los vínculos entre las personas y su entorno."
)

LIVLIN_MODULES = [
    ("📋 M1 · Intención y Contexto",
     "Registra los datos del espacio y explora la motivación regenerativa de quienes "
     "lo habitan. Define el horizonte de sentido que guiará todo el proceso."),
    ("🌍 M2-3 · Observación Ecológica",
     "'Observar e interactuar' — primer principio de Holmgren. Lee el sitio antes de "
     "diseñar: suelo, agua, sol, viento, vegetación y fauna son el punto de partida."),
    ("🏙️ M4-6 · Sistemas del Espacio",
     "Analiza los flujos vitales: agua, energía y materiales. Identificar y cerrar "
     "estos ciclos es la base de la autonomía regenerativa del espacio."),
    ("🌸 M7 · Flor de la Permacultura",
     "Registro de prácticas activas (Observado) y potencial adicional (Potencial) "
     "en los 7 pétalos de Holmgren. Genera el Índice de Potencial Regenerativo (IPR)."),
    ("🗺️ M9 · Síntesis y Plan de Acción",
     "Hoja de ruta en 3 horizontes: acciones inmediatas (0-3 meses), estacionales "
     "(3-12 meses) y estructurales (1-5 años)."),
    ("📷 Registro Fotográfico",
     "Documentación visual del espacio por categorías. "
     "Las fotos se almacenan permanentemente en la base de datos del diagnóstico."),
]

# 7 pétalos oficiales — Holmgren (2002), adaptados al contexto urbano
PETAL_DESC = {
    "Administración de la Tierra y la Naturaleza": {
        "holmgren_name": "Land & Nature Stewardship",
        "subtitulo": "Agricultura urbana · suelo vivo · biodiversidad · agua",
        "resumen": (
            "Punto de partida de la permacultura: diseñar sistemas productivos que "
            "imitan los patrones naturales. Incluye huertos, "
            "compostaje, captación de agua lluvia y creación de hábitat para fauna "
            "benéfica. Históricamente es el pétalo central de la práctica permacultural "
            "(Holmgren, 2002; Mollison, 1988)."
        ),
        "detalle": (
            "Este pétalo reconoce que incluso en los entornos urbanos más densos es "
            "posible crear sistemas alimentarios locales y regenerar la base ecológica. "
            "El compostaje doméstico convierte residuos orgánicos en suelo vivo; los "
            "huertos en macetas, balcones y patios producen alimentos frescos sin "
            "cadenas industriales; la captación de lluvia reduce la dependencia de "
            "la red de agua potable. Cada práctica en este pétalo acerca el espacio "
            "al ideal de la 'cultura permanente': un sistema que se sostiene y mejora "
            "con el tiempo (Holmgren, 2002)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos más allá de la sustentabilidad", "https://permacultureprinciples.com/es/"),
            ("Mollison, B. (1988)", "Permaculture: A Designers' Manual. Tagari Publications", "https://www.permaculturenews.org"),
            ("Lawton, G.", "Introducción a la Permacultura (video)", "https://youtu.be/-5N9Q8KtB5w"),
        ],
    },
    "Entorno Construido": {
        "holmgren_name": "Built Environment",
        "subtitulo": "Bioconstrucción · diseño bioclimático · espacios regenerativos",
        "resumen": (
            "El diseño del entorno construido con criterios bioclimáticos y bajo impacto "
            "ambiental. Las decisiones sobre cómo construimos y habitamos nuestros "
            "espacios determinan décadas de consumo energético y calidad de vida "
            "(Holmgren, 2002; Reed & Moff, 2007)."
        ),
        "detalle": (
            "Desde el diseño solar pasivo que reduce la necesidad de calefacción y "
            "refrigeración artificial, hasta el uso de materiales naturales locales y "
            "la integración de vegetación en los edificios (techos y muros verdes, "
            "jardines interiores), este pétalo transforma los edificios de consumidores "
            "de energía en sistemas que colaboran con los ciclos naturales. Pequeñas "
            "intervenciones — una pérgola verde, aislación natural, una ventana orientada "
            "al norte — pueden tener un impacto significativo en el bienestar y el "
            "consumo energético del espacio (Minke, 2006)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("Reed, B. & Moff, S. (2007)", "Regenerative Development and Design. Wiley", "https://youtu.be/pBuN9CtUVAw"),
            ("Minke, G. (2006)", "Building with Earth: Design and Technology. Birkhäuser", "https://birkhauser.com"),
        ],
    },
    "Herramientas y Tecnología": {
        "holmgren_name": "Tools & Technology",
        "subtitulo": "Energía renovable · tecnología simple · movilidad sostenible",
        "resumen": (
            "La selección crítica de herramientas y tecnologías que sirven a las personas "
            "y al ecosistema. La tecnología apropiada no es la más sofisticada, sino la "
            "más adecuada al contexto: accesible, reparable y de bajo impacto "
            "(Holmgren, 2002; Schumacher, 1973)."
        ),
        "detalle": (
            "Paneles solares, calentadores solares de agua, biodigestores, sistemas de "
            "riego por goteo casero, la bicicleta como transporte cotidiano: estas "
            "herramientas reducen dependencias externas y aumentan la resiliencia del "
            "espacio. El principio clave es que sean comprensibles, reparables localmente "
            "y transferibles entre vecinos. Holmgren (2002) distingue entre la tecnología "
            "que refuerza la autonomía local y la que la debilita, independientemente de "
            "su complejidad o fuente energética."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("Schumacher, E.F. (1973)", "Small is Beautiful: Economics as if People Mattered", "https://www.schumachercollege.org.uk"),
            ("Practical Action", "Technology Challenging Poverty — recursos técnicos", "https://practicalaction.org"),
        ],
    },
    "Educación y Cultura": {
        "holmgren_name": "Culture & Education",
        "subtitulo": "Saberes locales · arte comunitario · redes de conocimiento",
        "resumen": (
            "Transmisión de saberes, valores y prácticas que sostienen culturas "
            "regenerativas. Para Holmgren (2002), sin transformación cultural "
            "los cambios técnicos no persisten: la permacultura es tanto un sistema "
            "de diseño como un movimiento de cambio cultural."
        ),
        "detalle": (
            "Este pétalo reconoce que compartir saberes — un taller de compostaje, "
            "un intercambio de semillas, una jornada de construcción colectiva — "
            "tiene un impacto transformador comparable a cualquier instalación técnica. "
            "Las redes de educación entre pares y los espacios de intercambio "
            "intercultural generan la base cultural sobre la que se sostienen todas "
            "las demás prácticas regenerativas. El arte, la música y las celebraciones "
            "comunitarias también son parte de este pétalo: son la expresión viva de "
            "una cultura que valora la vida y la naturaleza (Holmgren, 2002)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("Capra, F.", "Visión sistémica de la vida (video)", "https://youtu.be/O33uA_9kj4U"),
            ("Transition Network", "Manual de Transición — recursos para comunidades", "https://transitionnetwork.org"),
        ],
    },
    "Salud y Bienestar Espiritual": {
        "holmgren_name": "Health & Spiritual Wellbeing",
        "subtitulo": "Alimentación viva · plantas medicinales · bienestar integral",
        "resumen": (
            "Sistemas de salud preventivos basados en alimentación viva, movimiento, "
            "plantas medicinales y comunidad. Holmgren (2002) incluye el bienestar "
            "espiritual como dimensión esencial: la salud regenerativa integra cuerpo, "
            "mente, comunidad y ecosistema."
        ),
        "detalle": (
            "Cultivar plantas medicinales, cocinar con alimentos frescos de producción "
            "propia, crear espacios de contemplación en el jardín, participar en "
            "comunidades de cuidado mutuo: estas prácticas construyen salud de manera "
            "preventiva y reduce la dependencia de cadenas farmacéuticas y alimentarias "
            "industriales. La investigación en ecoterapia confirma que el contacto "
            "regular con entornos naturales reduce el estrés y mejora el bienestar "
            "integral. La jardinería terapéutica es reconocida en este pétalo como "
            "una práctica con doble beneficio: produce alimentos y nutre la salud "
            "mental (Holmgren, 2002)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("IPES-Food (2017)", "Too big to feed: Exploring the impacts of mega-mergers", "https://www.ipes-food.org"),
            ("Wahl, D.C.", "Diseñar para la regeneración y la salud planetaria (video)", "https://youtu.be/drY0L-wAop8"),
        ],
    },
    "Finanzas y Economía": {
        "holmgren_name": "Finances & Economics",
        "subtitulo": "Mercados locales · economías solidarias · soberanía alimentaria",
        "resumen": (
            "Sistemas económicos que mantienen la riqueza circulando localmente: "
            "mercados agroecológicos, cooperativas, trueque y finanzas éticas. "
            "Para Holmgren (2002), la soberanía económica es inseparable de "
            "la soberanía alimentaria y ecosistémica."
        ),
        "detalle": (
            "Las economías solidarias y locales crean circuitos cortos donde la "
            "riqueza generada permanece en la comunidad en lugar de extractarse hacia "
            "sistemas globales. Comprar directamente a productores locales, participar "
            "en cooperativas de consumo, crear bancos de tiempo o usar monedas "
            "comunitarias son prácticas que fortalecen la resiliencia económica del "
            "territorio. Este pétalo también incluye la 'contabilidad de la emergía' "
            "y las inversiones éticas que el propio diagrama de Holmgren menciona: "
            "herramientas para valorar el capital natural, no solo el financiero "
            "(Holmgren, 2002; Raworth, 2017)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("Raworth, K. (2017)", "Doughnut Economics: 7 Ways to Think Like a 21st-Century Economist", "https://doughnuteconomics.org"),
            ("P2P Foundation", "Commons Economy — recursos y casos", "https://p2pfoundation.net"),
        ],
    },
    "Tenencia de la Tierra y Gobernanza Comunitaria": {
        "holmgren_name": "Land Tenure & Community Governance",
        "subtitulo": "Uso colectivo del territorio · participación comunitaria",
        "resumen": (
            "Marcos legales y comunitarios para el acceso y cuidado colectivo de la "
            "tierra. Holmgren (2002) incluye este pétalo como condición estructural: "
            "sin acuerdos sobre el uso del territorio, las demás prácticas no tienen "
            "base estable donde arraigarse."
        ),
        "detalle": (
            "Los huertos comunitarios, las asambleas barriales, los fideicomisos de "
            "tierra comunitaria (Community Land Trusts) y la participación en "
            "planificación urbana son herramientas concretas para democratizar el "
            "acceso a la tierra en contextos urbanos. La resolución colaborativa de "
            "conflictos y los modelos de co-vivienda (co-housing) también forman parte "
            "de este pétalo. Ostrom (1990) demostró que las comunidades pueden "
            "gestionar recursos colectivos de manera efectiva y sostenible cuando "
            "tienen marcos institucionales adecuados — una evidencia fundamental "
            "para la gobernanza regenerativa (Holmgren, 2002; Ostrom, 1990)."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos", "https://permacultureprinciples.com/es/"),
            ("Ostrom, E. (1990)", "Governing the Commons. Cambridge University Press", "https://wtf.tw/ref/ostrom_1990.pdf"),
            ("Community Land Trust Network", "Fideicomisos de tierra comunitaria", "https://www.communitylandtrusts.org.uk"),
        ],
    },
}

IPR_SCALE = [
    ("Sin inicio",   "0",   "#9E9E9E",
     "Este pétalo aún no tiene prácticas activas. Gran potencial latente — todo camino comienza aquí."),
    ("🌱 Iniciando",   "1",   "#74C69D",
     "El primer paso ya está dado. En la permacultura, una primera práctica activa es el acto más importante."),
    ("🌿 Avanzando",   "2",   "#52B788",
     "Dos prácticas muestran intención sostenida. El sistema empieza a tomar forma y generar sus primeros resultados."),
    ("🌳 Consolidado", "3",   "#40916C",
     "Sistema estable con rendimientos constantes. La práctica regenerativa es parte del modo habitual del espacio."),
    ("🌸 Destacado",   "4–5", "#2D6A4F",
     "Alta integración entre prácticas. El espacio genera abundancia y puede compartir con la comunidad."),
    ("✨ Referente",   "6+",  "#1B4332",
     "Sistema autónomo y resiliente, capaz de compartir excedentes. Modelo de transformación regenerativa urbana."),
]

IPR_WHAT_IS = (
    "El Índice de Potencial Regenerativo (IPR) mide la diversidad de prácticas regenerativas "
    "activas en un espacio, organizadas según los 7 pétalos de la Flor de la Permacultura "
    "(Holmgren, 2002). El IPR no es un puntaje punitivo: celebra cada práctica existente "
    "como un logro real. La pregunta no es '¿cuánto falta?' sino '¿qué ya está floreciendo "
    "aquí y qué más podría despertar?'"
)

IPR_OBS_VS_POT = (
    "OBSERVADO: prácticas que ya existen y funcionan en el espacio hoy. "
    "POTENCIAL ADICIONAL: nuevas prácticas concretas y viables identificadas "
    "por el facilitador tras la visita diagnóstica. El potencial no requiere "
    "re-ingresar lo ya observado — solo suma lo nuevo, lo que puede activarse."
)

TAO_REFLEXION_SHORT = (
    "«La regeneración no surge del control absoluto sobre la naturaleza. Surge cuando "
    "aprendemos a cooperar con ella. No se trata de salvar la naturaleza como si fuera "
    "algo externo a nosotros — somos naturaleza. Cuando cuidamos nuestra propia vida, "
    "también cuidamos la red de vida de la cual formamos parte. Por eso el camino "
    "regenerativo también es un camino interior: mente abierta, corazón abierto, "
    "voluntad abierta. Como enseña el Tao, el agua transforma la roca no por violencia, "
    "sino por persistencia.»"
)

TAO_INVITACION = (
    "Este diagnóstico es un momento dentro de un proceso más amplio. Cada espacio tiene "
    "su propio ritmo de transformación — a veces comienza con algo pequeño: un huerto, "
    "un compostador, una conversación entre vecinos. Lo importante es seguir caminando. "
    "Cuando muchas personas comienzan a escuchar ese mismo pulso de vida, "
    "los territorios cambian. www.livlin.cl · Potencial para una vida regenerativa. 🌱"
)

GLOBAL_REFS = [
    ("Holmgren, D. (2002)", "Permacultura: Principios y senderos más allá de la sustentabilidad. Kaicron", "https://permacultureprinciples.com/es/"),
    ("Holmgren, D. (2002)", "Permaculture Principles and Pathways (English)", "https://permacultureprinciples.com/"),
    ("Mollison, B. (1988)", "Permaculture: A Designers' Manual. Tagari Publications", "https://www.permaculturenews.org"),
    ("Mang, P. & Reed, B. (2012)", "Designing from place: A regenerative framework. Building Research & Information", "https://doi.org/10.1080/09613218.2012.62134"),
    ("Ostrom, E. (1990)", "Governing the Commons. Cambridge University Press", "https://wtf.tw/ref/ostrom_1990.pdf"),
    ("Raworth, K. (2017)", "Doughnut Economics. Chelsea Green Publishing", "https://doughnuteconomics.org"),
    ("Schumacher, E.F. (1973)", "Small is Beautiful: Economics as if People Mattered", "https://www.schumachercollege.org.uk"),
    ("IPES-Food (2017)", "Too big to feed: Exploring the impacts of mega-mergers", "https://www.ipes-food.org"),
    ("Mason, F. (2025)", "Introducción al enfoque de la regeneración. LivLin", "https://doi.org/10.17605/OSF.IO/UCDEH"),
    ("Mason, F. (2025)", "Texto completo disponible en Google Drive", "https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing"),
    ("Lawton, G.", "Introducción a la Permacultura (video)", "https://youtu.be/-5N9Q8KtB5w"),
    ("Capra, F.", "Visión sistémica de la vida (video)", "https://youtu.be/O33uA_9kj4U"),
    ("Reed, B.", "Desarrollo y Diseño Regenerativo (video)", "https://youtu.be/pBuN9CtUVAw"),
    ("Wahl, D.C.", "Diseñar para la regeneración (video)", "https://youtu.be/drY0L-wAop8"),
    ("Recursos climáticos", "Clima y Permacultura — videos", "https://www.youtube.com/results?search_query=clima+permacultura"),
    ("LivLin", "Potencial para una vida regenerativa", "https://www.livlin.cl"),
]

LIVLIN_NARRATIVE_INTRO = (
    "¿Te abruma lo que está pasando en el mundo? "
    "Contaminación, pérdida de biodiversidad, cambio climático, conflictos. "
    "Si sientes angustia frente a esto, no estás exagerando — estás prestando atención. "
    "El problema no es sentir preocupación. El problema es quedarnos paralizados.\n\n"
    "La angustia crece cuando vemos el problema pero no vemos el siguiente paso. "
    "No podemos arreglar el mundo entero ahora. "
    "Pero sí podemos transformar el ecosistema que habitamos: nuestra casa, "
    "nuestra organización, nuestra comunidad.\n\n"
    "La acción regenerativa comienza con tres preguntas:\n"
    "¿Qué impacto estoy generando hoy?\n"
    "¿Cómo puedo reducir daño?\n"
    "¿Cómo puedo empezar a regenerar?\n\n"
    "En LivLin acompañamos ese proceso. "
    "Transformamos la angustia en diseño. La preocupación en estrategia. "
    "Y la intención en impacto medible.\n\n"
    "Sentir no es debilidad. Es conciencia. "
    "Lo importante es qué hacemos con ella. "
    "Empieza a regenerar donde estás. www.livlin.cl"
)
