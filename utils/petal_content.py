"""Contenido compartido de los pétalos — v2.2.
Usado por el módulo de permacultura, el Excel y el Word.
Una sola fuente de verdad para descripciones, referencias y escala IPR.
"""

PETAL_ICONS = ["🌳", "🏡", "🛠️", "📚", "🧘", "💚", "🤝", "🌿"]

# ── Descripciones completas (mismas que se muestran en la app) ────────────────
PETAL_DESC = {
    "Manejo de la tierra y la naturaleza (urbano)": {
        "resumen": (
            "Corazón de la permacultura urbana: diseñar con la naturaleza para producir "
            "alimentos, regenerar suelos y restaurar biodiversidad. Incluye huertos, "
            "compostaje, captación de agua lluvia y corredores de polinizadores."
        ),
        "detalle": (
            "Este pétalo reconoce que incluso en contextos urbanos densificados es posible "
            "crear sistemas alimentarios locales resilientes. Las prácticas van desde el "
            "huerto en maceta hasta bosques comestibles en patios comunitarios, pasando por "
            "el compostaje doméstico, el vermicompostaje, la captación de agua lluvia y la "
            "creación de refugios para fauna benéfica. Cada práctica contribuye a regenerar "
            "los ciclos naturales dentro del tejido urbano."
        ),
        "referencias": [
            ("Holmgren, D. (2002)", "Permacultura: Principios y senderos más allá de la sustentabilidad", "https://holmgren.com.au"),
            ("Mollison, B. (1988)", "Permaculture: A Designers' Manual. Tagari Publications", "https://www.permaculturenews.org"),
            ("Hemenway, T. (2009)", "Gaia's Garden: A Guide to Home-Scale Permaculture", "https://www.chelseagreen.com"),
        ],
    },
    "Ambiente construido": {
        "resumen": (
            "Diseño de edificaciones e infraestructuras con criterios bioclimáticos y bajo "
            "impacto. Incluye energía pasiva, materiales naturales, techos y muros verdes. "
            "Las decisiones en este pétalo tienen impacto durante décadas."
        ),
        "detalle": (
            "El ambiente construido representa la mayor huella material de nuestras vidas. "
            "La bioconstrucción, el diseño solar pasivo, el uso de materiales locales y "
            "naturales, y la integración de naturaleza en los edificios (techos verdes, muros "
            "verdes, jardines interiores) transforman los edificios de consumidores de energía "
            "en sistemas que colaboran con los ciclos naturales. Hasta las remodelaciones "
            "pequeñas con materiales naturales suman en este pétalo."
        ),
        "referencias": [
            ("Minke, G. (2006)", "Building with Earth: Design and Technology of a Sustainable Architecture", "https://birkhauser.com"),
            ("Reed, B. & Moff, S. (2007)", "Regenerative Development and Design. Wiley", "https://www.regenesisgroup.com"),
            ("Living Future Institute", "Living Building Challenge Standard", "https://living-future.org"),
        ],
    },
    "Herramientas y tecnologías apropiadas": {
        "resumen": (
            "Selección crítica de tecnologías que sirven a las personas y al planeta. "
            "Prioriza herramientas simples, reparables y de bajo consumo: energía solar, "
            "biodigestores, sistemas de riego eficiente."
        ),
        "detalle": (
            "La tecnología apropiada no es necesariamente la más sofisticada, sino la más "
            "adecuada al contexto: accesible, reparable localmente, de bajo impacto ambiental "
            "y que fortalece la autonomía del usuario. Paneles solares, calentadores solares, "
            "cocinas rocket, biodigestores pequeños, filtros de agua artesanales y sistemas "
            "de riego por goteo casero son ejemplos de tecnología apropiada para contextos "
            "urbanos y periurbanos."
        ),
        "referencias": [
            ("Schumacher, E.F. (1973)", "Small is Beautiful: Economics as if People Mattered. Harper & Row", "https://www.schumachercollege.org.uk"),
            ("Practical Action", "Technology Challenging Poverty — recursos técnicos gratuitos", "https://practicalaction.org"),
            ("ITDG (2016)", "Appropriate Technology Library", "https://www.villageearth.org/appropriate-technology"),
        ],
    },
    "Educación y cultura": {
        "resumen": (
            "Transmisión de saberes, valores y prácticas que sostienen culturas regenerativas. "
            "Abarca educación formal e informal, arte, intercambio de semillas y redes de "
            "conocimiento local. Sin cultura regenerativa, las técnicas no persisten."
        ),
        "detalle": (
            "La cultura es el sistema operativo de cualquier cambio social duradero. Este pétalo "
            "reconoce que compartir saberes, crear arte con materiales reciclados, organizar "
            "festivales de semillas o mentorear a vecinos en agroecología son actos tan "
            "transformadores como instalar un panel solar. Las redes de educación entre pares "
            "(peer-to-peer) y los espacios de intercambio intercultural son fundamentales para "
            "escalar la transición regenerativa."
        ),
        "referencias": [
            ("Freire, P. (1968)", "Pedagogía del oprimido. Siglo XXI Editores", "https://www.sigloxxieditores.com"),
            ("Illich, I. (1971)", "Deschooling Society. Harper & Row", "https://www.preservenet.com/theory/Illich"),
            ("Transition Network", "Manual de Transición — recursos para comunidades", "https://transitionnetwork.org"),
        ],
    },
    "Salud y bienestar": {
        "resumen": (
            "Sistemas de salud preventivos basados en alimentación viva, movimiento, plantas "
            "medicinales y comunidad. La jardinería terapéutica, los baños de naturaleza "
            "y el bienestar colectivo son dimensiones centrales."
        ),
        "detalle": (
            "La salud regenerativa va más allá de la ausencia de enfermedad: incluye el "
            "bienestar físico, mental, emocional y comunitario. Cultivar plantas medicinales, "
            "cocinar alimentos frescos de producción propia, practicar jardinería terapéutica "
            "o crear espacios de contemplación son prácticas que nutren la salud integral. "
            "La investigación reciente confirma que el contacto regular con naturaleza reduce "
            "el estrés, la ansiedad y mejora la salud cardiovascular."
        ),
        "referencias": [
            ("IPES-Food (2017)", "Too big to feed: Exploring the impacts of mega-mergers", "https://www.ipes-food.org"),
            ("Pretty, J. et al. (2017)", "Nature contact and human health. Int. Journal of Environmental Research and Public Health", "https://www.mdpi.com/journal/ijerph"),
            ("Kaplan, R. & Kaplan, S. (1989)", "The Experience of Nature: A Psychological Perspective", "https://www.cambridge.org"),
        ],
    },
    "Economía y finanzas": {
        "resumen": (
            "Sistemas económicos que circulan la riqueza localmente: mercados agroecológicos, "
            "cooperativas, trueque, monedas locales y finanzas éticas. Reduce la dependencia "
            "del sistema extractivo y fortalece la soberanía alimentaria."
        ),
        "detalle": (
            "Este pétalo invita a repensar el dinero, el intercambio y el valor. Las economías "
            "solidarias y locales crean circuitos cortos donde la riqueza generada permanece "
            "en la comunidad. Desde comprar directamente a productores locales hasta participar "
            "en cooperativas de consumo, crear bancos de tiempo o usar monedas comunitarias, "
            "cada práctica fortalece la resiliencia económica del territorio."
        ),
        "referencias": [
            ("Gibson-Graham, J.K. (2006)", "A Postcapitalist Politics. University of Minnesota Press", "https://www.upress.umn.edu"),
            ("Raworth, K. (2017)", "Doughnut Economics: Seven Ways to Think Like a 21st-Century Economist", "https://doughnuteconomics.org"),
            ("P2P Foundation", "Peer-to-Peer Commons Economy — recursos y casos", "https://p2pfoundation.net"),
        ],
    },
    "Tenencia de la tierra y gobernanza": {
        "resumen": (
            "Marcos legales y comunitarios para el acceso y cuidado colectivo de la tierra. "
            "Incluye cooperativas de vivienda, huertos comunitarios, asambleas barriales "
            "y participación ciudadana en el diseño urbano."
        ),
        "detalle": (
            "La tierra es el recurso más estratégico de cualquier proyecto regenerativo. Este "
            "pétalo aborda cómo las comunidades pueden acceder, usar y cuidar colectivamente "
            "los espacios, más allá de la propiedad individual. Los fideicomisos de tierra "
            "comunitaria (CLT), las cooperativas de vivienda, los huertos comunitarios formales "
            "y los acuerdos de uso compartido son herramientas concretas para democratizar "
            "el acceso a la tierra en contextos urbanos."
        ),
        "referencias": [
            ("Ostrom, E. (1990)", "Governing the Commons: The Evolution of Institutions for Collective Action", "https://wtf.tw/ref/ostrom_1990.pdf"),
            ("De Angelis, M. (2017)", "Omnia Sunt Communia: On the Commons and the Transformation to Postcapitalism", "https://www.zedbooks.net"),
            ("Community Land Trust Network", "Guías y casos de fideicomisos de tierra comunitaria", "https://www.communitylandtrusts.org.uk"),
        ],
    },
    "Prácticas cotidianas de sustentabilidad": {
        "resumen": (
            "Las acciones diarias del hogar y la vida cotidiana que acumulan impacto sistémico: "
            "reducir, reutilizar, reparar, consumir local, conectar con vecinos. "
            "Los pequeños actos transforman la cultura cuando se vuelven hábito colectivo."
        ),
        "detalle": (
            "Este pétalo honra las prácticas cotidianas que, aunque parezcan pequeñas, "
            "son la base de la transición cultural. Apagar luces, reparar antes de comprar, "
            "ducharse menos tiempo, compartir herramientas con vecinos o participar en "
            "organizaciones locales: cada acto individual, multiplicado por miles de personas, "
            "genera un impacto sistémico. La coherencia entre valores y prácticas cotidianas "
            "es el fundamento de cualquier cambio social profundo."
        ),
        "referencias": [
            ("Shove, E. (2003)", "Comfort, Cleanliness and Convenience: The Social Organization of Normality", "https://www.bergpublishers.com"),
            ("Jackson, T. (2009)", "Prosperity Without Growth: Economics for a Finite Planet. Earthscan", "https://www.prosperitywithoutgrowth.com"),
            ("Ellen MacArthur Foundation", "Economía circular — recursos y casos de estudio", "https://ellenmacarthurfoundation.org"),
        ],
    },
}

# ── Escala IPR — misma que se muestra en la app ───────────────────────────────
IPR_SCALE = [
    ("○ Sin inicio",   "0",   "#BDBDBD",
     "Área por explorar — este pétalo aún no tiene prácticas activas. "
     "Gran potencial latente esperando ser activado."),
    ("🌱 Iniciando",   "1",   "#74C69D",
     "El primer paso ya está dado — ¡este es el paso más importante! "
     "Una práctica activa demuestra intención y capacidad de acción."),
    ("🌿 Avanzando",   "2",   "#52B788",
     "Dos prácticas muestran intención sostenida. El sistema empieza "
     "a tomar forma y genera sus primeros frutos concretos."),
    ("🌳 Consolidado", "3",   "#40916C",
     "Sistema estable que genera rendimientos constantes. La práctica "
     "es parte del modo habitual de vida del espacio."),
    ("🌸 Destacado",   "4–5", "#2D6A4F",
     "Alta integración entre prácticas. El espacio genera abundancia "
     "e inspira a otros en la comunidad. Referente local."),
    ("✨ Referente",   "6+",  "#1B4332",
     "Sistema autónomo, resiliente y capaz de compartir excedentes "
     "con la comunidad. Modelo de transformación regenerativa urbana."),
]

IPR_WHAT_IS = (
    "El Índice de Potencial Regenerativo (IPR) mide la diversidad y profundidad de prácticas "
    "regenerativas activas en un espacio, organizadas según los 8 pétalos de la Flor de la "
    "Permacultura de David Holmgren (2002). A diferencia de un puntaje punitivo, el IPR "
    "celebra cada práctica existente como un logro real. El objetivo no es llegar a un número "
    "perfecto, sino reconocer dónde hay vitalidad y dónde hay oportunidad de crecimiento."
)

IPR_OBS_VS_POT = (
    "OBSERVADO: prácticas que ya existen y funcionan en el espacio hoy. "
    "POTENCIAL ADICIONAL: nuevas prácticas concretas y viables identificadas por el "
    "facilitador tras la visita diagnóstica, basándose en las condiciones reales del espacio. "
    "El potencial adicional no requiere re-ingresar lo ya observado — solo suma lo nuevo."
)

# ── Información LivLin ────────────────────────────────────────────────────────
LIVLIN_DESC = (
    "LivLin es una plataforma de diagnóstico y acompañamiento para la transformación "
    "regenerativa de espacios urbanos. Usamos la metodología de la Flor de la Permacultura "
    "(Holmgren, 2002) y el diseño sistémico para identificar el potencial regenerativo de "
    "cada espacio y comunidad. Trabajamos con facilitadores capacitados que realizan visitas "
    "diagnósticas y generan informes personalizados con planes de acción concretos. "
    "Nuestra misión es acelerar la transición hacia ciudades más vivas, resilientes y justas."
)

LIVLIN_MODULES = [
    ("📋 M1 · Información + Tao",
     "Datos del proyecto, intención regenerativa, sueño del espacio y percepción de la "
     "triple crisis (cambio climático, pérdida de biodiversidad, contaminación). "
     "Establece el contexto humano y motivacional del diagnóstico."),
    ("🌍 M2-3 · Observación Ecológica",
     "Lectura del sitio: tipo de suelo, compactación, materia orgánica, vegetación, fauna, "
     "flujos naturales (sol, viento, agua), datos climáticos históricos y potencial de cultivo. "
     "Base ecológica del diagnóstico."),
    ("🏙️ M4-6 · Sistemas",
     "Análisis del contexto urbano, sistema de agua (consumo, captación, reutilización), "
     "sistema de energía (consumo, fuentes, potencial solar) y gestión de materiales y residuos. "
     "Dimensión técnica e infraestructural del espacio."),
    ("🌸 M7 · Flor de la Permacultura",
     "Corazón del diagnóstico: registro de prácticas activas (Observado) y potencial adicional "
     "identificado por el facilitador, organizados en los 8 pétalos de Holmgren. "
     "Genera el Índice de Potencial Regenerativo (IPR) con radar visual."),
    ("🗺️ M9 · Síntesis y Plan de Acción",
     "Fortalezas, desafíos y oportunidades del espacio. Plan de acción en 3 horizontes: "
     "inmediato (0-3 meses), estacional (3-12 meses) y estructural (1-5 años). "
     "Hoja de ruta concreta y priorizada para la transformación regenerativa."),
    ("📷 Registro Fotográfico",
     "Documentación visual del espacio por categorías (suelo, vegetación, agua, energía, etc.). "
     "Las fotos se almacenan permanentemente en la base de datos del diagnóstico."),
]

GLOBAL_REFS = [
    ("Holmgren, D. (2002)", "Permacultura: Principios y senderos más allá de la sustentabilidad", "https://holmgren.com.au"),
    ("Mollison, B. (1988)", "Permaculture: A Designers' Manual. Tagari Publications", "https://www.permaculturenews.org"),
    ("Ostrom, E. (1990)",   "Governing the Commons. Cambridge University Press", "https://wtf.tw/ref/ostrom_1990.pdf"),
    ("Raworth, K. (2017)",  "Doughnut Economics: 7 Ways to Think Like a 21st-Century Economist", "https://doughnuteconomics.org"),
    ("IPES-Food (2017)",    "Too big to feed: Exploring the impacts of mega-mergers", "https://www.ipes-food.org"),
    ("Transition Network",  "Manual de Transición — Recursos para comunidades", "https://transitionnetwork.org"),
    ("Practical Action",    "Technology Challenging Poverty — recursos técnicos gratuitos", "https://practicalaction.org"),
    ("LivLin",              "Plataforma de diagnóstico regenerativo urbano", "https://www.livlin.com"),
]
