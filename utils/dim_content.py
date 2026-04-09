"""Dimension descriptions and interpretations — shared across modules."""


DIM_DESC = {
    "Producción alimentaria":  "Capacidad del espacio para producir alimentos frescos — cultivos, hierbas, frutales y hortalizas que contribuyen a la soberanía alimentaria del grupo.",
    "Biodiversidad urbana":    "Diversidad de especies vegetales y animales presentes — polinizadores, aves, plantas nativas, cobertura vegetal. Un espacio rico en biodiversidad es resiliente y saludable.",
    "Captación y gestión del agua":       "Gestión autónoma del agua: captación de lluvia, reutilización de aguas grises, eficiencia en el riego y reducción de la dependencia de la red pública.",
    "Regeneración del suelo":  "Salud biológica del suelo: materia orgánica, actividad microbiana, lombrices y hongos beneficiosos. El suelo vivo es la base de todo sistema regenerativo.",
    "Educación ambiental":     "Actividades de aprendizaje, transmisión de saberes y formación en ecología, permacultura y vida regenerativa que ocurren en el espacio o a partir de él.",
    "Bienestar comunitario":   "Calidad de los vínculos sociales: relaciones vecinales, participación comunitaria, redes de apoyo mutuo y capacidad de actuar colectivamente.",
    "Economía regenerativa":   "Prácticas de autosuficiencia, intercambio, comercio justo, trueque y economía circular que reducen la dependencia de mercados extractivos.",
    "Salud y bienestar":      "Conexión del grupo con la naturaleza, prácticas de bienestar espiritual y emocional, silencio, contemplación y el cuidado de la dimensión interior como raíz de toda acción regenerativa.",
    "Energía y eficiencia":    "Nivel de eficiencia energética y transición hacia renovables: uso de paneles solares, iluminación LED, reducción del consumo y adopción de tecnologías apropiadas.",
    "Entorno construido":      "Calidad regenerativa del espacio físico: bioarquitectura, diseño bioclimático, techos y muros verdes, uso de materiales naturales y espacios multifuncionales.",
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
    "Captación y gestión del agua": [
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
    "Salud y bienestar": [
        "El espacio tiene gran potencial para nutrir la dimensión interior. Un rincón de silencio o tiempo en contacto con la tierra puede ser el comienzo. Sanar nuestra relación con la naturaleza es el primer paso para regenerar.",
        "Hay primeras señales de conexión interior. Este vínculo puede profundizarse y convertirse en fuente de bienestar, calma y propósito.",
        "El espacio ya nutre el bienestar interior. Hay prácticas de conexión con la naturaleza que vale la pena cultivar.",
        "Buen nivel de bienestar interior. El espacio genera conexión, calma y sentido — base fundamental para una vida regenerativa.",
        "El espacio es fuente activa de bienestar interior y conexión profunda con la naturaleza.",
        "El espacio es un santuario interior — la conexión del grupo con la naturaleza es profunda y transformadora.",
    ],
    "Energía y eficiencia": [
        "El espacio todavía no ha incorporado tecnologías de eficiencia energética. Cambiar a LED o planificar paneles solares son primeros pasos concretos hacia la autonomía energética.",
        "Hay primeras intenciones o pequeñas mejoras en eficiencia. El camino hacia la autonomía energética está comenzando con señales concretas de acción.",
        "El espacio tiene algunas prácticas de eficiencia activas. La iluminación LED o el interés en solar son señales de avance real hacia la transición energética.",
        "Buen nivel de eficiencia energética. El espacio reduce su consumo y avanza hacia fuentes renovables — una contribución directa a la resiliencia climática.",
        "El espacio tiene energía solar u otras renovables activas. La eficiencia energética es parte central de su identidad regenerativa.",
        "El espacio es referente de eficiencia y autonomía energética — un modelo de transición renovable urbana que puede inspirar a su comunidad.",
    ],
    "Entorno construido": [
        "El entorno construido todavía no incorpora elementos regenerativos. Hay oportunidades concretas para comenzar: una pérgola vegetal, materiales naturales, o mejorar la ventilación.",
        "Hay primeras incorporaciones regenerativas en el entorno construido. El espacio empieza a integrar bioclimática o materiales naturales con intención.",
        "El entorno construido muestra prácticas regenerativas activas: bioarquitectura, energía pasiva o naturaleza integrada al diseño del espacio.",
        "El entorno construido es activamente regenerativo. El diseño trabaja a favor del bienestar, la eficiencia energética y la integración de la vida.",
        "El espacio construido es un ejemplo de diseño regenerativo — integra naturaleza, eficiencia y materiales naturales de manera consistente.",
        "El entorno construido es referente de bioarquitectura y diseño bioclimático regenerativo — un espacio que demuestra que construir y regenerar pueden ir de la mano.",
    ],
}

CLIMATE_REF = {
    "Producción alimentaria":  "🌡️ Cada kilo producido localmente evita emisiones de transporte y fortalece la soberanía alimentaria frente al cambio climático.",
    "Biodiversidad urbana":    "🦋 Cada planta nativa y polinizador apoyado es una acción directa contra la crisis global de pérdida de especies.",
    "Captación y gestión del agua":       "💧 Gestionar el agua de forma autónoma reduce la vulnerabilidad ante las sequías cada vez más frecuentes por el cambio climático.",
    "Regeneración del suelo":  "🌍 El suelo vivo es el mayor sumidero de carbono disponible — regenerar el suelo es combatir el cambio climático desde tu patio.",
    "Educación ambiental":     "📚 La educación ambiental construye la conciencia colectiva necesaria para enfrentar las tres crisis: clima, biodiversidad y contaminación.",
    "Bienestar comunitario":   "🤝 Las comunidades resilientes responden mejor colectivamente al cambio climático y sus consecuencias sociales.",
    "Economía regenerativa":   "🌾 Economías locales y circulares reducen emisiones, contaminación y dependencia de sistemas extractivos que agravan las crisis planetarias.",
    "Salud y bienestar":      "☯️ Sanar nuestra relación interior con la naturaleza es la raíz desde la que nace toda acción regenerativa sostenida en el tiempo.",
    "Energía y eficiencia":    "⚡ Cada kWh ahorrado y cada watt solar instalado reduce la dependencia de sistemas que agravan el cambio climático.",
    "Entorno construido":      "🏡 Un espacio construido de forma regenerativa reduce consumo energético, aumenta biodiversidad y mejora el bienestar.",
}

