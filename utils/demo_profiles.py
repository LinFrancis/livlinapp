"""utils/demo_profiles.py -- Perfiles demo COMPLETOS para modo demostracion.
6 perfiles realistas en la Region Metropolitana (cuenca del Maipo).
Todos con niveles medios-bajos (realista para quienes recien comienzan).
Alto potencial de regeneracion. Cada perfil responde TODOS los modulos.
"""

# ── Base cuenca info for Santiago/Maipo ─────────────────────────────────────
_CUENCA_MAIPO = {
    "cuenca_cod": "057",
    "cuenca_nombre": "Rio Maipo",
    "cuenca_wiki_link": "https://es.wikipedia.org/wiki/Special:Search?search=Rio+Maipo&go=Go",
    "subcuenca_cod": "0571",
    "subcuenca_nombre": "Rio Maipo entre Rio Mapocho y Desembocadura",
    "subcuenca_wiki_link": "https://es.wikipedia.org/wiki/Special:Search?search=Rio+Maipo&go=Go",
    "subsubcuenca_cod": "05714",
    "subsubcuenca_nombre": "Rio Maipo entre Zanjón de la Aguada y Río Mapocho",
    "subsubcuenca_wiki_link": "https://es.wikipedia.org/wiki/Special:Search?search=Rio+Maipo&go=Go",
    "cuenca_wiki_summary": (
        "El rio Maipo es un curso fluvial que nace en la cordillera de los Andes, "
        "en el volcan Maipo, y desemboca en el oceano Pacifico. Es el principal rio "
        "de la Region Metropolitana de Santiago, Chile, con una cuenca de 15.380 km2. "
        "Abastece de agua potable a gran parte de Santiago y es fundamental para "
        "la agricultura del valle central."
    ),
    "cuenca_wiki_source": "Rio Maipo",
}


def _base_profile(pid, nombre, cliente, tipo, composicion, area, desc,
                  lat, lon, geo_display, geo_city,
                  tao_scores, tao_notas,
                  eco_data, salud_data,
                  suelo, sol, viento, veg, fauna, cultivo,
                  ctx, agua, energia, residuos,
                  ipr_obs, ipr_tot,
                  sintesis, plan):
    """Build a complete demo profile dict."""
    d = {
        "id": pid,
        "created_at": "2026-03-15T10:00:00",
        "updated_at": "2026-03-20T14:30:00",
        # ── M1: Proyecto ──
        "proyecto_nombre": nombre,
        "proyecto_cliente": cliente,
        "proyecto_tipo_espacio": tipo,
        "proyecto_composicion": composicion,
        "proyecto_area": area,
        "proyecto_descripcion": desc,
        "proyecto_direccion": geo_display,
        "proyecto_ciudad": geo_city,
        "proyecto_pais": "Chile",
        "geo_lat": lat, "geo_lon": lon,
        "geo_display": geo_display,
        "geo_city": geo_city, "geo_country": "Chile",
        # ── Module status ──
        "mod_cliente": "respondido",
        "mod_tao": "respondido",
        "mod_eco": "respondido",
        "mod_sitio": "respondido",
        "mod_sistemas": "respondido",
        "mod_potencial": "respondido",
        "mod_sintesis": "respondido",
        # ── Tao 5 dimensiones ──
        "tao_d1_wu_wei": tao_scores[0],
        "tao_d2_humildad": tao_scores[1],
        "tao_d3_compasion": tao_scores[2],
        "tao_d4_esencial": tao_scores[3],
        "tao_d5_retorno": tao_scores[4],
        "tao_notas": tao_notas,
        # ── IPR (7 petalos) ──
        "ipr_obs": ipr_obs,
        "ipr_tot": ipr_tot,
    }
    d.update(_CUENCA_MAIPO)
    d.update(eco_data)
    d.update(salud_data)
    d.update(suelo)
    d.update(sol)
    d.update(viento)
    d.update(veg)
    d.update(fauna)
    d.update(cultivo)
    d.update(ctx)
    d.update(agua)
    d.update(energia)
    d.update(residuos)
    d.update(sintesis)
    d.update(plan)
    return d


# ════════════════════════════════════════════════════════════════════════════
# PERFIL 1: Pareja en departamento pequeno
# ════════════════════════════════════════════════════════════════════════════
P1 = _base_profile(
    pid="demo_pareja_depto",
    nombre="Departamento Barrio Italia",
    cliente="Camila y Matias",
    tipo="Departamento con terraza",
    composicion="Pareja sin hijos/as",
    area=65,
    desc=(
        "Departamento de 65m2 con terraza de 8m2 en Barrio Italia, Providencia. "
        "Camila es disenadora y Matias trabaja en ingenieria ambiental. Quieren "
        "transformar su terraza en un espacio productivo y reducir su huella "
        "ecologica urbana. Tienen interes en compostaje bokashi, cultivo en "
        "macetas y una vida mas consciente. Sus gatas Luna y Sol disfrutan "
        "del sol en la terraza."
    ),
    lat=-33.4422, lon=-70.6280,
    geo_display="Barrio Italia, Providencia, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[2, 3, 3, 2, 1],
    tao_notas="Recien comenzando a explorar la permacultura. Mucho interes pero poca experiencia practica. El trabajo absorbe mucho tiempo.",
    eco_data={
        "eco_cc_conciencia": "Lo sentimos como una amenaza real",
        "eco_cc_impacto": "Los veranos son cada vez mas calurosos. La terraza se vuelve insoportable en enero.",
        "eco_cc_respuesta": "Queremos poner sombra natural con trepadoras y reducir nuestro consumo energetico.",
        "eco_bio_conciencia": "Sabemos que existe pero parece distante",
        "eco_bio_local": "Antes se veian mas pajaros en el barrio. Ahora sobre todo palomas.",
        "eco_bio_accion": "Poner bebederos para aves y plantas que atraigan polinizadores en la terraza.",
        "eco_cont_conciencia": "La vivimos en el barrio",
        "eco_cont_tipos": ["Aire / smog", "Ruido"],
        "eco_cont_respuesta": "Usamos bicicleta para ir al trabajo. Reducimos plasticos.",
    },
    salud_data={
        "sal_alimentacion": "Regular -- mezcla de procesados y frescos",
        "sal_alim_local": "A veces",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio leve 1-2 veces/semana",
        "sal_contacto_naturaleza": "A veces",
        "sal_descanso": "Regular",
        "sal_practicas_text": "Matias hace yoga dos veces por semana. Camila cocina platos vegetarianos los fines de semana.",
    },
    suelo={
        "suelo_tipo": "No aplica (contenedores)",
        "suelo_compactacion": "No aplica",
        "suelo_materia_organica": "Medio",
        "suelo_drenaje": "Bueno",
        "suelo_color": "Oscuro (sustrato comercial)",
        "suelo_olor": "Neutro",
        "suelo_notas": "Usan sustrato comprado. Quieren aprender a preparar su propia mezcla con compost bokashi.",
    },
    sol={
        "sol_horas": 5,
        "sol_horas_invierno": 3,
        "sol_horas_verano": 7,
        "sol_orientacion": "Noroeste",
        "sol_zonas_max": "Terraza recibe sol directo de manana. Tarde tiene sombra del edificio vecino.",
        "sol_sombra_perm": "Rincon junto a la puerta corrediza queda siempre en sombra.",
    },
    viento={
        "viento_direccion": "Suroeste",
        "viento_protegidas": "La terraza esta parcialmente protegida por el muro lateral.",
        "viento_expuestas": "Las macetas del borde reciben viento fuerte en tardes de verano.",
    },
    veg={
        "veg_tipos": ["Aromáticas", "Ornamentales"],
        "veg_especies": "Romero, lavanda, albahaca en macetas. Un limonero enano que no da frutos aun.",
        "veg_invasoras": "Ninguna identificada.",
    },
    fauna={
        "fauna_lombrices": "No aplica (contenedores)",
        "fauna_plagas": "Pulgones en la albahaca en verano.",
        "fauna_aves_especies": "Palomas, zorzales ocasionales, chincoles.",
    },
    cultivo={
        "cultivo_m2": 3,
        "cultivo_m2_futuro": 6,
        "cultivo_produce_hoy": "En proceso",
        "cultivo_frutales": "Posiblemente",
        "cultivo_verticales": "Si",
        "cultivo_plantas_actuales": "Romero, albahaca, cilantro, tomates cherry (2 plantas).",
        "cultivo_interes": "Queremos instalar un muro verde comestible y ampliar a lechugas y kale.",
        "cultivo_notas": "Espacio limitado pero con mucho potencial vertical.",
    },
    ctx={
        "ctx_cuenca": "Rio Maipo",
        "ctx_vecinos": "Escasa",
        "ctx_actores": "Feria del barrio los sabados; una tienda de plantas a 3 cuadras.",
        "ctx_participacion": "Baja",
        "ctx_distancia_parques": "Parque Bustamante a 5 minutos caminando.",
    },
    agua={
        "agua_fuente": "Red pública",
        "agua_consumo": 180,
        "agua_riego_sistema": "Manual con regadera",
        "agua_captacion_lluvia": "No",
        "agua_fugas": "No",
        "agua_grises": "No",
    },
    energia={
        "ene_fuente": "Red eléctrica",
        "ene_kwh_dia_calc": 6.5,
        "ene_led": "Parcialmente",
        "ene_solar_interes": "Mediano plazo",
    },
    residuos={
        "res_compostan": "En proceso",
        "res_compost_tipo": "Bokashi",
        "res_organico_kg": 3,
        "res_tipos_generados": ["Orgánicos", "Plásticos", "Cartón"],
    },
    ipr_obs=[2, 1, 1, 1, 2, 2, 0],
    ipr_tot=[5, 3, 3, 3, 4, 4, 2],
    sintesis={
        "sint_fortalezas": "Alta motivacion de la pareja. Conocimiento ambiental profesional de Matias. Terraza con buen sol matutino. Barrio con acceso a feria y tiendas de plantas.",
        "sint_oportunidades": "Cultivo vertical en muros de terraza. Compostaje bokashi ya iniciado. Captacion de agua lluvia en canaleta. Conexion con vecinos del edificio para huerto colectivo en azotea.",
        "sint_limitaciones": "Espacio muy reducido (8m2 terraza). Poco tiempo libre entre semana. Sin contacto con vecinos del edificio. Sombra parcial en invierno.",
        "sint_quick_wins": "Instalar jardineras verticales en el muro soleado. Completar sistema bokashi. Poner bebedero para aves. Germinar microgreens en la cocina.",
        "sint_observaciones": "Perfil tipico de pareja urbana joven con alta conciencia ecologica pero limitaciones de espacio y tiempo. El potencial principal esta en maximizar el uso vertical y en iniciar compostaje.",
    },
    plan={
        "plan_inmediatas": "1. Instalar 4 jardineras verticales en muro noroeste (capacidad +12 plantas)\n2. Completar primer ciclo de compost bokashi\n3. Sembrar microgreens y germinados en cocina\n4. Instalar bebedero y comedero para aves",
        "plan_estacionales": "1. Sembrar tomates y hierbas de verano (septiembre)\n2. Instalar trepadora comestible (maracuya o kiwi enano) en primavera\n3. Iniciar banco de semillas con intercambio vecinal\n4. Preparar sustrato propio con bokashi maduro",
        "plan_estructurales": "1. Proponer huerto comunitario en azotea del edificio\n2. Evaluar sistema de captacion de agua lluvia en balcon\n3. Transicion a iluminacion LED completa\n4. Conectar con red de huertos urbanos del barrio",
    },
)

# ════════════════════════════════════════════════════════════════════════════
# PERFIL 2: Familia grande con casa y patio
# ════════════════════════════════════════════════════════════════════════════
P2 = _base_profile(
    pid="demo_familia_casa",
    nombre="Casa Familiar La Florida",
    cliente="Familia Gonzalez-Munoz",
    tipo="Casa con patio/jardín",
    composicion="Familia con hijos/as menores",
    area=220,
    desc=(
        "Casa de 220m2 con patio delantero de 40m2 y patio trasero de 60m2 "
        "en La Florida. Familia de 5: padres (Carolina profesora, Pedro "
        "carpintero) y tres hijos (Sofia 4, Tomas 8, Valentina 12). "
        "El patio trasero tiene cesped, un limonero viejo y un naranjo. "
        "La abuela Eliana vive a dos cuadras y conoce plantas medicinales. "
        "Tienen un perro (Canelo) y dos gallinas (Pepa y Lola)."
    ),
    lat=-33.5170, lon=-70.5980,
    geo_display="La Florida, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[2, 2, 3, 3, 2],
    tao_notas="Familia con mucho entusiasmo. Los ninos son un motor de cambio. La abuela Eliana aporta saberes tradicionales de plantas medicinales. El desafio es el tiempo: ambos padres trabajan.",
    eco_data={
        "eco_cc_conciencia": "Lo conocemos pero parece lejano",
        "eco_cc_impacto": "El patio se seca mucho en verano. Las gallinas sufren con el calor.",
        "eco_cc_respuesta": "Plantamos un arbol de sombra el ano pasado. Queremos captar agua lluvia.",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_bio_local": "Antes habia muchas mas mariposas. Los ninos notan que hay menos abejas.",
        "eco_bio_accion": "Plantar flores nativas para abejas. Dejar un rincon silvestre en el patio.",
        "eco_cont_conciencia": "La vivimos en el barrio",
        "eco_cont_tipos": ["Aire / smog", "Plásticos y residuos"],
        "eco_cont_respuesta": "Separamos residuos. Usamos bolsas reutilizables. Los ninos recogen basura del pasaje.",
    },
    salud_data={
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "A veces",
        "sal_alim_plantas": "A veces",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "Frecuentemente",
        "sal_descanso": "Bien",
        "sal_practicas_text": "Los ninos juegan mucho al aire libre. La abuela prepara aguas de hierbas. Carolina hace caminatas con el perro.",
    },
    suelo={
        "suelo_tipo": "Arcilloso-limoso",
        "suelo_compactacion": "Media",
        "suelo_materia_organica": "Bajo",
        "suelo_drenaje": "Regular",
        "suelo_color": "Cafe claro",
        "suelo_olor": "Neutro",
        "suelo_notas": "Suelo tipico del valle de Santiago. Necesita incorporacion de materia organica. Las raices del limonero compactan la zona cercana.",
    },
    sol={
        "sol_horas": 7,
        "sol_horas_invierno": 4,
        "sol_horas_verano": 10,
        "sol_orientacion": "Norte",
        "sol_zonas_max": "Centro del patio trasero recibe sol todo el dia. Patio delantero tiene sol de manana.",
        "sol_sombra_perm": "Bajo el naranjo y junto al muro sur.",
    },
    viento={
        "viento_direccion": "Suroeste",
        "viento_protegidas": "El patio trasero esta protegido por muros en tres lados.",
        "viento_expuestas": "Patio delantero expuesto a viento de la calle.",
    },
    veg={
        "veg_tipos": ["Frutales", "Césped", "Ornamentales"],
        "veg_especies": "Limonero (viejo, produce bien), naranjo, pasto bermuda, rosales, lavanda.",
        "veg_invasoras": "Bermuda invade las camas de cultivo.",
    },
    fauna={
        "fauna_lombrices": "Pocas",
        "fauna_plagas": "Babosas en invierno. Pulgones en primavera.",
        "fauna_aves_especies": "Zorzales, chincoles, tordos. Las gallinas Pepa y Lola.",
    },
    cultivo={
        "cultivo_m2": 8,
        "cultivo_m2_futuro": 30,
        "cultivo_produce_hoy": "Si",
        "cultivo_frutales": "Si",
        "cultivo_verticales": "Posiblemente",
        "cultivo_plantas_actuales": "Tomates, lechugas, zanahorias, cilantro, perejil. Limon y naranja.",
        "cultivo_interes": "Ampliar huerto, incorporar camas elevadas, guilds de frutales, plantas medicinales de la abuela.",
        "cultivo_notas": "Mucho potencial en el patio trasero. 60m2 disponibles, solo 8m2 cultivados actualmente.",
    },
    ctx={
        "ctx_cuenca": "Rio Maipo",
        "ctx_vecinos": "Regular",
        "ctx_actores": "Feria libre los miercoles a 3 cuadras. Escuela de los ninos tiene huerto.",
        "ctx_participacion": "Media",
        "ctx_distancia_parques": "Plaza del barrio a 2 cuadras. Parque La Florida a 15 min.",
    },
    agua={
        "agua_fuente": "Red pública",
        "agua_consumo": 450,
        "agua_riego_sistema": "Manguera manual",
        "agua_captacion_lluvia": "No",
        "agua_fugas": "No",
        "agua_grises": "No",
    },
    energia={
        "ene_fuente": "Red eléctrica",
        "ene_kwh_dia_calc": 12,
        "ene_led": "Parcialmente",
        "ene_solar_interes": "Sí, pronto",
    },
    residuos={
        "res_compostan": "No",
        "res_compost_tipo": "Ninguno",
        "res_organico_kg": 8,
        "res_tipos_generados": ["Orgánicos", "Plásticos", "Cartón", "Vidrio"],
    },
    ipr_obs=[4, 1, 2, 2, 2, 3, 1],
    ipr_tot=[9, 4, 4, 5, 5, 6, 4],
    sintesis={
        "sint_fortalezas": "Gran superficie de patio (100m2 total). Frutales ya establecidos. Familia motivada con ninos como motor. Saberes de la abuela en plantas medicinales. Gallinas ya integradas. Buen sol.",
        "sint_oportunidades": "Ampliar huerto de 8 a 30m2 con camas elevadas. Instalar compostera de tres camaras. Captacion de agua lluvia desde techo (gran superficie). Jardin medicinal con la abuela. Conectar con huerto de la escuela.",
        "sint_limitaciones": "Suelo compactado y bajo en materia organica. Bermuda invasora. Riego solo manual. Ambos padres trabajan, tiempo limitado entre semana. Sin compostaje activo.",
        "sint_quick_wins": "1. Construir compostera con pallets (Pedro es carpintero). 2. Incorporar mulch al suelo. 3. Sembrar abono verde en areas no cultivadas. 4. Instalar 2 camas elevadas.",
        "sint_observaciones": "Caso con alto potencial: gran espacio, familia completa comprometida, saberes intergeneracionales. El cuello de botella es el suelo y el tiempo. Priorizamos compostaje y camas elevadas.",
    },
    plan={
        "plan_inmediatas": "1. Construir compostera de 3 camaras con pallets reciclados\n2. Aplicar 10cm de mulch en todo el patio trasero\n3. Instalar 2 camas elevadas de 1.2x2.4m\n4. Iniciar semillero en invernadero casero",
        "plan_estacionales": "1. Sembrar abono verde (vicia/avena) en areas no cultivadas (otono)\n2. Plantar 3 frutales nuevos (guild: manzano + frambuesas + frutilla) en primavera\n3. Instalar riego por goteo casero desde barril\n4. Crear rincon de plantas medicinales con la abuela",
        "plan_estructurales": "1. Instalar sistema de captacion de agua lluvia (2000L)\n2. Disenar food forest en mitad del patio trasero\n3. Paneles solares en techo norte (presupuesto familiar)\n4. Vincular con programa de huertos comunitarios municipal",
    },
)

# ════════════════════════════════════════════════════════════════════════════
# PERFIL 3: Senora sola en condominio
# ════════════════════════════════════════════════════════════════════════════
P3 = _base_profile(
    pid="demo_senora_condominio",
    nombre="Condominio Los Jardines de Nunoa",
    cliente="Maria Elena Torres",
    tipo="Comunidad / copropiedad",
    composicion="Persona viviendo sola",
    area=85,
    desc=(
        "Maria Elena (63) vive sola en un departamento de 85m2 en un condominio "
        "de 48 unidades en Nunoa. Areas verdes comunes: 200m2 de cesped con palmeras "
        "y arbustos ornamentales. Quiere proponer huerto comunitario, compostera "
        "colectiva y actividades de jardineria para vecinos. Ya tiene 6 vecinos "
        "interesados. El desafio: convencer a la administracion."
    ),
    lat=-33.4560, lon=-70.5970,
    geo_display="Nunoa, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[3, 3, 2, 2, 2],
    tao_notas="Maria Elena tiene mucha energia y conexion con la tierra. Enfrenta resistencia institucional del condominio. Su fortaleza es la paciencia y su red de 6 vecinos aliados.",
    eco_data={
        "eco_cc_conciencia": "Es parte de nuestra motivacion de accion",
        "eco_cc_impacto": "El condominio gasta mucha agua regando cesped que se seca en verano.",
        "eco_cc_respuesta": "Proponer reemplazo de cesped por jardin mediterraneo y huerto.",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_bio_local": "Las palmeras del condominio no aportan alimento a ningun animal.",
        "eco_bio_accion": "Plantar nativas y arbustos con frutos para aves.",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "eco_cont_tipos": ["Aire / smog", "Plásticos y residuos", "Ruido"],
        "eco_cont_respuesta": "Proponer punto limpio en el condominio. Compostera comunitaria.",
    },
    salud_data={
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "A veces",
        "sal_descanso": "Regular",
        "sal_practicas_text": "Hace caminatas diarias. Cocina con productos de la feria. Practica jardineria como terapia.",
    },
    suelo={
        "suelo_tipo": "Franco-arcilloso",
        "suelo_compactacion": "Alta",
        "suelo_materia_organica": "Bajo",
        "suelo_drenaje": "Regular",
        "suelo_color": "Cafe claro",
        "suelo_notas": "El cesped del condominio tiene suelo muy compactado por anos sin trabajo. Necesita rehabilitacion.",
    },
    sol={"sol_horas": 6, "sol_horas_invierno": 3, "sol_horas_verano": 9, "sol_orientacion": "Norte-Poniente", "sol_zonas_max": "Area central del jardin comun tiene sol directo.", "sol_sombra_perm": "Bajo las palmeras y junto al estacionamiento."},
    viento={"viento_direccion": "Suroeste", "viento_protegidas": "El edificio protege del viento dominante.", "viento_expuestas": "Sector poniente del jardin."},
    veg={"veg_tipos": ["Césped", "Ornamentales", "Árboles"], "veg_especies": "Palmeras, arbustos podados, cesped bermuda.", "veg_invasoras": "Cesped bermuda invade todo."},
    fauna={"fauna_lombrices": "Muy pocas", "fauna_plagas": "Ninguna visible.", "fauna_aves_especies": "Palomas, gorriones."},
    cultivo={"cultivo_m2": 0, "cultivo_m2_futuro": 25, "cultivo_produce_hoy": "No", "cultivo_frutales": "Posiblemente", "cultivo_verticales": "Posiblemente", "cultivo_interes": "Huerto comunitario en area comun, hierbas aromaticas, verduras de hoja.", "cultivo_notas": "Todo el potencial esta en convencer a la administracion y al comite de vecinos."},
    ctx={"ctx_cuenca": "Rio Maipo", "ctx_vecinos": "Regular", "ctx_actores": "Junta de vecinos, feria del barrio, ONG ambiental comunal.", "ctx_participacion": "Media"},
    agua={"agua_fuente": "Red pública", "agua_consumo": 120, "agua_riego_sistema": "Aspersores (comunes)", "agua_captacion_lluvia": "No", "agua_fugas": "No", "agua_grises": "No"},
    energia={"ene_fuente": "Red eléctrica", "ene_kwh_dia_calc": 5, "ene_led": "Si", "ene_solar_interes": "Mediano plazo"},
    residuos={"res_compostan": "No", "res_compost_tipo": "Ninguno", "res_organico_kg": 2, "res_tipos_generados": ["Orgánicos", "Plásticos", "Cartón"]},
    ipr_obs=[0, 0, 0, 1, 2, 1, 1],
    ipr_tot=[4, 2, 1, 4, 4, 3, 5],
    sintesis={
        "sint_fortalezas": "Liderazgo de Maria Elena. 6 vecinos aliados. 200m2 de espacio comun disponible. Condominio con infraestructura de riego existente. Ubicacion con buena feria local.",
        "sint_oportunidades": "Huerto comunitario en 25m2 de cesped subutilizado. Compostera comunitaria (48 departamentos generan mucho organico). Talleres de jardineria para vecinos. Jardin de lluvia en area de drenaje.",
        "sint_limitaciones": "Resistencia de la administracion del condominio. Suelo muy compactado. Sin infraestructura de cultivo. Vecinos aun no convencidos en mayoria.",
        "sint_quick_wins": "1. Taller abierto de jardineria en area comun. 2. Macetas demostrativas con hierbas. 3. Presentar propuesta a comite de administracion. 4. Crear grupo de WhatsApp de vecinos verdes.",
        "sint_observaciones": "El mayor potencial aqui es comunitario. Si Maria Elena logra mover al condominio, el impacto se multiplica por 48 familias. La estrategia debe ser gradual, sin imponer.",
    },
    plan={
        "plan_inmediatas": "1. Presentar propuesta de piloto (4m2 de huerto + compostera) a la administracion\n2. Organizar taller abierto de hierbas aromaticas en macetas\n3. Crear red de vecinos interesados (WhatsApp + reuniones mensuales)\n4. Instalar 6 macetas demostrativas de hierbas en areas comunes",
        "plan_estacionales": "1. Si se aprueba piloto: construir 3 camas elevadas en primavera\n2. Instalar compostera comunitaria de 3 etapas\n3. Plantar arbusto nativo con frutos (calafate, maqui) en otono\n4. Organizar feria de intercambio de plantas entre vecinos",
        "plan_estructurales": "1. Reemplazar 50% del cesped por jardin mediterraneo bajo en agua\n2. Crear espacio de encuentro comunitario junto al huerto\n3. Incorporar modelo en reglamento de copropiedad\n4. Conectar con red municipal de huertos comunitarios",
    },
)

# ════════════════════════════════════════════════════════════════════════════
# PERFIL 4: Restaurante con terraza
# ════════════════════════════════════════════════════════════════════════════
P4 = _base_profile(
    pid="demo_restaurante",
    nombre="Restaurante Raices del Maipo",
    cliente="Francisco Araya",
    tipo="Otro",
    composicion="Organización o institución",
    area=180,
    desc=(
        "Restaurante de cocina chilena contemporanea en Providencia. Terraza "
        "de 45m2 y patio trasero de 30m2. Francisco (chef y dueno) quiere "
        "transformar la terraza en jardin comestible, instalar compostera "
        "para residuos de cocina y crear conexion entre la comida y su origen. "
        "El restaurante genera 15kg de residuos organicos diarios. "
        "Equipo de 8 personas en cocina y sala."
    ),
    lat=-33.4325, lon=-70.6150,
    geo_display="Providencia, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[1, 2, 2, 2, 3],
    tao_notas="El ritmo del restaurante es intenso. Francisco tiene vision clara pero el dia a dia absorbe. El equipo esta abierto al cambio. La conexion con productores locales ya existe parcialmente.",
    eco_data={
        "eco_cc_conciencia": "Lo sentimos como una amenaza real",
        "eco_cc_impacto": "El calor extremo en verano afecta la terraza y el consumo energetico de refrigeracion.",
        "eco_cc_respuesta": "Queremos sombra natural en terraza y reducir la cadena de frio.",
        "eco_bio_conciencia": "Sabemos que existe pero parece distante",
        "eco_bio_local": "No hemos prestado atencion a la biodiversidad del entorno.",
        "eco_bio_accion": "Plantar aromaticas que atraigan polinizadores en la terraza.",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "eco_cont_tipos": ["Plásticos y residuos", "Agua contaminada"],
        "eco_cont_respuesta": "Eliminar plasticos de un solo uso. Instalar trampa de grasas. Compostar organicos.",
    },
    salud_data={
        "sal_alimentacion": "Muy buena -- dieta basada en plantas y local",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio leve 1-2 veces/semana",
        "sal_contacto_naturaleza": "Raramente",
        "sal_descanso": "Poco -- dormimos mal o poco",
    },
    suelo={"suelo_tipo": "No aplica (contenedores y camas elevadas)", "suelo_notas": "Patio trasero tiene tierra compactada. Terraza es baldosas."},
    sol={"sol_horas": 6, "sol_horas_verano": 9, "sol_orientacion": "Poniente", "sol_zonas_max": "Terraza tiene sol intenso de tarde.", "sol_sombra_perm": "Patio trasero tiene sombra del edificio vecino."},
    viento={"viento_direccion": "Suroeste", "viento_protegidas": "El patio trasero."},
    veg={"veg_tipos": ["Ornamentales"], "veg_especies": "Solo plantas decorativas en la terraza.", "veg_invasoras": "Ninguna."},
    fauna={"fauna_aves_especies": "Palomas y gorriones."},
    cultivo={"cultivo_m2": 0, "cultivo_m2_futuro": 20, "cultivo_produce_hoy": "No", "cultivo_frutales": "No", "cultivo_verticales": "Si", "cultivo_interes": "Hierbas aromaticas frescas, microgreens, flores comestibles.", "cultivo_notas": "El valor comercial de hierbas frescas en plato es altisimo. Retorno de inversion inmediato."},
    ctx={"ctx_cuenca": "Rio Maipo", "ctx_vecinos": "Escasa", "ctx_actores": "Proveedores de ingredientes locales. Red de restaurantes sustentables.", "ctx_participacion": "Baja"},
    agua={"agua_fuente": "Red pública", "agua_consumo": 800, "agua_riego_sistema": "No existe", "agua_captacion_lluvia": "No", "agua_fugas": "No"},
    energia={"ene_fuente": "Red eléctrica", "ene_kwh_dia_calc": 45, "ene_led": "Si", "ene_solar_interes": "Mediano plazo"},
    residuos={"res_compostan": "No", "res_compost_tipo": "Ninguno", "res_organico_kg": 15, "res_tipos_generados": ["Orgánicos", "Plásticos", "Cartón", "Vidrio", "Aceite usado"]},
    ipr_obs=[1, 0, 1, 0, 1, 2, 0],
    ipr_tot=[5, 2, 3, 3, 3, 5, 1],
    sintesis={
        "sint_fortalezas": "15kg diarios de organico = recurso enorme para compost. Chef comprometido. Terraza con buen sol. Red de proveedores locales. Visibilidad publica del restaurante.",
        "sint_oportunidades": "Compostera comercial para 15kg/dia. Huerto de hierbas aromaticas en terraza (ahorro en compras). Muro verde comestible visible a clientes. Eliminar plasticos. Narrativa gastronomica regenerativa.",
        "sint_limitaciones": "Ritmo de trabajo intenso. Alto consumo de agua y energia. Sin experiencia en cultivo. Espacio de patio limitado. Equipo necesita capacitacion.",
        "sint_quick_wins": "1. Instalar 10 macetas de aromaticas en terraza (uso inmediato en cocina). 2. Contratar servicio de retiro de organicos para compostaje. 3. Eliminar envases plasticos descartables. 4. Germinar microgreens en cocina.",
    },
    plan={
        "plan_inmediatas": "1. Instalar 10 macetas de hierbas aromaticas en terraza\n2. Iniciar programa de microgreens en cocina\n3. Contratar retiro de organicos (15kg/dia)\n4. Eliminar plasticos descartables del servicio",
        "plan_estacionales": "1. Disenar e instalar muro verde comestible en terraza\n2. Capacitar equipo en separacion de residuos\n3. Iniciar compostera en patio trasero\n4. Incorporar narrativa regenerativa en carta del restaurante",
        "plan_estructurales": "1. Instalar compostera comercial de ciclo rapido\n2. Sistema de riego automatizado para hierbas\n3. Paneles solares en techo\n4. Certificacion de restaurante sustentable",
    },
)

# ════════════════════════════════════════════════════════════════════════════
# PERFIL 5: Escuela con jardin
# ════════════════════════════════════════════════════════════════════════════
P5 = _base_profile(
    pid="demo_escuela",
    nombre="Escuela Republica de Colombia",
    cliente="Equipo docente y apoderados",
    tipo="Escuela / jardín infantil",
    composicion="Grupo comunitario / vecinos",
    area=800,
    desc=(
        "Escuela basica municipal en Macul con 420 estudiantes. Patio de 500m2 "
        "mayoritariamente cemento y tierra compactada. Un grupo de 12 apoderados "
        "y 4 profesores quiere crear jardin educativo, huerto escolar y zona de "
        "juego natural. El municipio dio autorizacion inicial. Director apoya."
    ),
    lat=-33.4890, lon=-70.6020,
    geo_display="Macul, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[2, 2, 3, 2, 1],
    tao_notas="Mucha energia comunitaria. Los ninos son el centro del proyecto. Falta experiencia tecnica en permacultura. El grupo de apoderados es diverso y motivado.",
    eco_data={
        "eco_cc_conciencia": "Lo conocemos pero parece lejano",
        "eco_cc_impacto": "El patio de cemento se calienta demasiado en verano. Los ninos no pueden jugar.",
        "eco_cc_respuesta": "Plantar arboles de sombra. Reemplazar cemento por areas verdes.",
        "eco_bio_conciencia": "No la conociamos",
        "eco_bio_local": "No hemos observado biodiversidad en el patio.",
        "eco_bio_accion": "Crear jardin de mariposas, hotel de insectos, bebederos para aves.",
        "eco_cont_conciencia": "La vivimos en el barrio",
        "eco_cont_tipos": ["Aire / smog", "Plásticos y residuos"],
        "eco_cont_respuesta": "Programa de reciclaje escolar. Reduccion de envases en colaciones.",
    },
    salud_data={
        "sal_alimentacion": "Regular -- mezcla de procesados y frescos",
        "sal_alim_local": "No",
        "sal_alim_plantas": "A veces",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "Raramente",
        "sal_descanso": "Regular",
    },
    suelo={"suelo_tipo": "Tierra compactada/ripio", "suelo_compactacion": "Alta", "suelo_materia_organica": "Muy bajo", "suelo_drenaje": "Malo", "suelo_color": "Gris palido", "suelo_notas": "Suelo degradado por decadas de uso como patio de recreo. Necesita rehabilitacion completa."},
    sol={"sol_horas": 8, "sol_horas_verano": 12, "sol_orientacion": "Norte", "sol_zonas_max": "Centro del patio sin sombra.", "sol_sombra_perm": "Solo junto al edificio escolar."},
    viento={"viento_direccion": "Suroeste", "viento_protegidas": "Junto al edificio."},
    veg={"veg_tipos": ["Árboles"], "veg_especies": "3 pimientos (Schinus molle) viejos en una esquina.", "veg_invasoras": "Malezas en grietas del cemento."},
    fauna={"fauna_lombrices": "Ninguna visible", "fauna_aves_especies": "Palomas, gorriones."},
    cultivo={"cultivo_m2": 0, "cultivo_m2_futuro": 80, "cultivo_produce_hoy": "No", "cultivo_frutales": "Si", "cultivo_verticales": "Posiblemente", "cultivo_interes": "Huerto pedagogico, jardin de mariposas, zona de juego natural, mini bosque comestible.", "cultivo_notas": "800m2 de patio: enorme potencial de transformacion. 420 estudiantes como fuerza de trabajo y aprendizaje."},
    ctx={"ctx_cuenca": "Rio Maipo", "ctx_vecinos": "Regular", "ctx_actores": "Municipalidad de Macul, JUNJI, universidad cercana, junta de vecinos.", "ctx_participacion": "Alta"},
    agua={"agua_fuente": "Red pública", "agua_consumo": 2000, "agua_riego_sistema": "No existe", "agua_captacion_lluvia": "No", "agua_fugas": "No"},
    energia={"ene_fuente": "Red eléctrica", "ene_kwh_dia_calc": 30, "ene_led": "Parcialmente", "ene_solar_interes": "Mediano plazo"},
    residuos={"res_compostan": "No", "res_compost_tipo": "Ninguno", "res_organico_kg": 20, "res_tipos_generados": ["Orgánicos", "Plásticos", "Cartón", "Tetrapak"]},
    ipr_obs=[0, 0, 0, 1, 0, 0, 1],
    ipr_tot=[6, 3, 2, 6, 3, 2, 5],
    sintesis={
        "sint_fortalezas": "Gran superficie disponible (500m2 patio). 420 estudiantes como aprendices y agentes de cambio. 16 adultos comprometidos. Apoyo del director y municipio. Pimientos nativos ya existentes.",
        "sint_oportunidades": "Huerto pedagogico integrado al curriculum. Mini bosque comestible (Miyawaki). Captacion de agua lluvia del techo (gran superficie). Compostera escolar con residuos de 420 almuerzos. Laboratorio vivo de biodiversidad.",
        "sint_limitaciones": "Suelo extremadamente degradado. Sin presupuesto asignado. Sin infraestructura de riego. Patio usado para recreo (conflicto de uso). Vacaciones escolares interrumpen cuidado.",
        "sint_quick_wins": "1. Instalar 6 camas elevadas con sustrato importado. 2. Compostera de 3 etapas con residuos del casino. 3. Hotel de insectos con materiales reciclados (proyecto escolar). 4. 5 arboles frutales en maceteros grandes.",
    },
    plan={
        "plan_inmediatas": "1. Construir 6 camas elevadas (1.2x3m) con donacion de maderas\n2. Instalar compostera escolar con residuos del casino\n3. Plantar 5 arboles frutales en maceteros grandes\n4. Crear hotel de insectos como proyecto de ciencias",
        "plan_estacionales": "1. Programa curricular: cada curso adopta una cama de cultivo\n2. Plantar mini bosque Miyawaki en esquina del patio (primavera)\n3. Instalar sistema de riego por goteo desde estanque\n4. Taller de compostaje para apoderados",
        "plan_estructurales": "1. Reemplazar 100m2 de cemento por areas verdes permeables\n2. Instalar sistema de captacion de agua lluvia (5000L)\n3. Crear sala de clases al aire libre junto al huerto\n4. Postular a fondo municipal de areas verdes",
    },
)

# ════════════════════════════════════════════════════════════════════════════
# PERFIL 6: Huerto comunitario
# ════════════════════════════════════════════════════════════════════════════
P6 = _base_profile(
    pid="demo_huerto_comunitario",
    nombre="Huerto Comunitario Cerro Blanco",
    cliente="Colectivo Verde Recoleta",
    tipo="Huerto comunitario",
    composicion="Comunidad intencional",
    area=350,
    desc=(
        "Terreno municipal recuperado de 350m2 al pie del Cerro Blanco, Recoleta. "
        "Colectivo de 18 personas de distintas edades y origenes. 8 meses "
        "trabajando el espacio. Ya tienen camas de cultivo, compostera basica "
        "y riego por goteo artesanal. Quieren profundizar en diseno permacultural, "
        "agroforesteria urbana y gobernanza comunitaria."
    ),
    lat=-33.4180, lon=-70.6480,
    geo_display="Recoleta, Santiago, Chile",
    geo_city="Santiago",
    tao_scores=[3, 3, 3, 3, 2],
    tao_notas="El colectivo tiene buena cohesion grupal y experiencia basica. Han aprendido a organizarse en asamblea. Necesitan profundizar en diseno de ecosistemas y en la dimension interior del trabajo regenerativo.",
    eco_data={
        "eco_cc_conciencia": "Es parte de nuestra motivacion de accion",
        "eco_cc_impacto": "El cerro se esta secando. Los incendios forestales llegan cada vez mas cerca.",
        "eco_cc_respuesta": "Plantamos nativas para restaurar el pie del cerro. Captamos agua lluvia.",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_bio_local": "El cerro tiene flora nativa degradada. Hemos visto menos lagartijas y mas perros callejeros.",
        "eco_bio_accion": "Crear corredor de polinizadores entre el huerto y el cerro. Plantar nativas.",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "eco_cont_tipos": ["Plásticos y residuos", "Suelo contaminado"],
        "eco_cont_respuesta": "Limpieza regular del entorno. Biorremediacion con girasoles en zona contaminada.",
    },
    salud_data={
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio moderado 3+ veces/semana",
        "sal_contacto_naturaleza": "Es parte de nuestra rutina",
        "sal_descanso": "Bien",
        "sal_practicas_text": "El trabajo en el huerto es nuestra actividad fisica principal. Cocinamos juntos con lo cosechado.",
    },
    suelo={"suelo_tipo": "Franco-arenoso", "suelo_compactacion": "Media", "suelo_materia_organica": "Medio", "suelo_drenaje": "Bueno", "suelo_color": "Cafe oscuro (mejorado)", "suelo_notas": "Suelo rehabilitado parcialmente con compost durante 8 meses. Zona norte aun degradada."},
    sol={"sol_horas": 8, "sol_horas_invierno": 5, "sol_horas_verano": 11, "sol_orientacion": "Norte (ladera del cerro)", "sol_zonas_max": "Todo el terreno tiene excelente exposicion solar.", "sol_sombra_perm": "Solo bajo el algarrobo existente."},
    viento={"viento_direccion": "Suroeste", "viento_protegidas": "El cerro protege del viento norte.", "viento_expuestas": "Borde sur del terreno."},
    veg={"veg_tipos": ["Hortalizas", "Aromáticas", "Frutales", "Nativas"], "veg_especies": "Tomates, lechugas, zanahorias, acelgas, albahaca, romero. Un algarrobo y dos espinos. Maqui silvestre.", "veg_invasoras": "Galega y zarzamora en el borde del cerro."},
    fauna={"fauna_lombrices": "Abundantes (en compost)", "fauna_plagas": "Babosas, pulgones estacionales.", "fauna_aves_especies": "Zorzales, chincoles, loicas, picaflores en verano. Lagartijas."},
    cultivo={"cultivo_m2": 80, "cultivo_m2_futuro": 200, "cultivo_produce_hoy": "Si", "cultivo_frutales": "Si", "cultivo_verticales": "No", "cultivo_plantas_actuales": "12 camas de hortalizas. 5 frutales jovenes. 2 espirales de aromaticas. Compostera de 3 camaras.", "cultivo_interes": "Ampliar a 200m2. Disenar food forest. Guild de frutales. Vivero comunitario de nativas.", "cultivo_notas": "El huerto ya es productivo. El proximo paso es el diseno integral del sistema agroforestal."},
    ctx={"ctx_cuenca": "Rio Maipo", "ctx_vecinos": "Buena", "ctx_actores": "Municipalidad de Recoleta, ONG local, universidad, feria del barrio, otros huertos comunitarios.", "ctx_participacion": "Alta"},
    agua={"agua_fuente": "Red pública (llave municipal)", "agua_consumo": 300, "agua_riego_sistema": "Goteo artesanal", "agua_captacion_lluvia": "Sí", "agua_fugas": "No", "agua_grises": "No"},
    energia={"ene_fuente": "Red eléctrica (conexión básica)", "ene_kwh_dia_calc": 2, "ene_led": "No aplica", "ene_solar_interes": "Mediano plazo"},
    residuos={"res_compostan": "Si", "res_compost_tipo": "Compostaje aeróbico + vermicompostaje", "res_organico_kg": 25, "res_tipos_generados": ["Orgánicos", "Cartón"]},
    ipr_obs=[7, 2, 2, 4, 3, 3, 4],
    ipr_tot=[12, 4, 4, 7, 5, 5, 7],
    sintesis={
        "sint_fortalezas": "350m2 con excelente sol. Colectivo de 18 personas organizado. 8 meses de experiencia. Compostaje activo y productivo. Captacion de agua lluvia ya instalada. Biodiversidad emergente. Conexion con redes locales.",
        "sint_oportunidades": "Diseno agroforestal del terreno completo. Vivero de nativas para restauracion del cerro. Talleres abiertos para el barrio. Mercado comunitario semanal. Programa de voluntariado. Conexion con circuito de huertos de Recoleta.",
        "sint_limitaciones": "Terreno municipal (precariedad legal). Suelo aun parcialmente degradado. Sin estructura permanente (bodega, bano). Acceso a agua depende de llave municipal. Zarzamora invasora en borde.",
        "sint_quick_wins": "1. Ampliar compostaje para recibir residuos de vecinos. 2. Instalar 6 camas nuevas en zona norte. 3. Plantar cortaviento nativo en borde sur. 4. Iniciar banco de semillas con intercambio mensual.",
    },
    plan={
        "plan_inmediatas": "1. Disenar plano maestro agroforestal del terreno completo\n2. Ampliar camas de cultivo de 80 a 120m2\n3. Instalar cortaviento nativo (quillay, peumo, boldo) en borde sur\n4. Organizar primer taller abierto de compostaje para el barrio",
        "plan_estacionales": "1. Plantar guild de frutales (ciruelo + grosella + frutilla + trébol) en primavera\n2. Iniciar vivero comunitario de nativas (semillas del cerro)\n3. Instalar segundo estanque de captacion de agua lluvia (1000L)\n4. Mercado comunitario mensual con lo cosechado",
        "plan_estructurales": "1. Gestionar comodato municipal por 10 anos\n2. Construir bodega comunitaria con materiales reciclados\n3. Disenar e implementar food forest en 150m2\n4. Postular a programa de restauracion ecologica del cerro con CONAF",
    },
)


DEMO_PROFILES = [P1, P2, P3, P4, P5, P6]


def get_demo_profile(profile_id):
    """Return a demo profile dict by ID."""
    for p in DEMO_PROFILES:
        if p["id"] == profile_id:
            return dict(p)
    return None


def list_demo_profiles():
    """Return list of (id, nombre, cliente, tipo, desc_corta) tuples."""
    result = []
    for p in DEMO_PROFILES:
        desc = p.get("proyecto_descripcion", "")
        if len(desc) > 100:
            desc = desc[:100] + "..."
        result.append((
            p["id"],
            p["proyecto_nombre"],
            p["proyecto_cliente"],
            p.get("proyecto_tipo_espacio", ""),
            desc,
        ))
    return result
