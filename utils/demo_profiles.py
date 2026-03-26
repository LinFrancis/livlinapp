"""utils/demo_profiles.py -- Perfiles demo para modo demostracion.
6 perfiles realistas en la Region Metropolitana (cuenca del Maipo).
Todos con niveles medios-bajos (realista para quienes recien comienzan).
Alto potencial de regeneracion en todos los casos.
"""

DEMO_PROFILES = [
    {
        "id": "demo_pareja_depto",
        "proyecto_nombre": "Departamento Barrio Italia",
        "proyecto_cliente": "Camila y Matias",
        "proyecto_tipo_espacio": "Departamento con terraza",
        "proyecto_composicion": "Pareja sin hijos/as",
        "proyecto_area": 65,
        "proyecto_descripcion": (
            "Departamento de 65m2 con terraza de 8m2 en Barrio Italia, Providencia. "
            "Camila es disenadora y Matias es ingeniero ambiental. Quieren transformar "
            "su terraza en un espacio productivo y reducir su huella ecologica urbana. "
            "Tienen interes en compostaje, cultivo en macetas y vida mas consciente."
        ),
        "geo_lat": -33.4422,
        "geo_lon": -70.6280,
        # Tao dimensions (medios-bajos, realistas)
        "tao_d1_wu_wei": 2,
        "tao_d2_humildad": 3,
        "tao_d3_compasion": 3,
        "tao_d4_esencial": 2,
        "tao_d5_retorno": 1,
        "tao_notas": "Recien comenzando a explorar la permacultura. Mucho interes pero poca experiencia practica.",
        # Salud (moved from old Tao T.7)
        "sal_alimentacion": "Regular -- mezcla de procesados y frescos",
        "sal_alim_local": "A veces",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio leve 1-2 veces/semana",
        "sal_contacto_naturaleza": "A veces",
        "sal_descanso": "Regular",
        # Conciencia ecologica
        "eco_cc_conciencia": "Lo sentimos como una amenaza real",
        "eco_bio_conciencia": "Sabemos que existe pero parece distante",
        "eco_cont_conciencia": "La vivimos en el barrio",
        # Basic module status
        "mod_tao": "respondido",
    },
    {
        "id": "demo_familia_grande",
        "proyecto_nombre": "Casa Familiar La Florida",
        "proyecto_cliente": "Familia Gonzalez-Muoz",
        "proyecto_tipo_espacio": "Casa con patio/jardin",
        "proyecto_composicion": "Familia con hijos/as menores",
        "proyecto_area": 220,
        "proyecto_descripcion": (
            "Casa de 220m2 con patio delantero de 40m2 y patio trasero de 60m2 en La Florida. "
            "Familia de 5 personas: padres y tres hijos (4, 8 y 12 anos). "
            "El patio trasero tiene cesped y algunos arboles frutales viejos. "
            "Quieren crear un huerto familiar, compostera y espacio de juego natural para los ninos. "
            "La abuela, que vive cerca, tiene conocimientos de plantas medicinales."
        ),
        "geo_lat": -33.5170,
        "geo_lon": -70.5980,
        "tao_d1_wu_wei": 2,
        "tao_d2_humildad": 2,
        "tao_d3_compasion": 3,
        "tao_d4_esencial": 3,
        "tao_d5_retorno": 2,
        "tao_notas": "La familia tiene mucho entusiasmo. Los ninos son un motor de cambio. La abuela aporta saberes tradicionales.",
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "A veces",
        "sal_alim_plantas": "A veces",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "Frecuentemente",
        "sal_descanso": "Bien",
        "eco_cc_conciencia": "Lo conocemos pero parece lejano",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_cont_conciencia": "La vivimos en el barrio",
        "mod_tao": "respondido",
    },
    {
        "id": "demo_senora_condominio",
        "proyecto_nombre": "Condominio Los Jardines de Nunoa",
        "proyecto_cliente": "Maria Elena Torres",
        "proyecto_tipo_espacio": "Comunidad / copropiedad",
        "proyecto_composicion": "Persona viviendo sola",
        "proyecto_area": 85,
        "proyecto_descripcion": (
            "Maria Elena (63 anos) vive sola en un departamento de 85m2 en un condominio "
            "de 48 departamentos en Nunoa. Hay areas verdes comunes con cesped y palmeras. "
            "Ella quiere proponer a la comunidad un huerto comunitario, compostera colectiva "
            "y actividades de jardineria para los vecinos. Ya tiene contacto con 6 vecinos interesados. "
            "El desafio principal es convencer a la administracion del condominio."
        ),
        "geo_lat": -33.4560,
        "geo_lon": -70.5970,
        "tao_d1_wu_wei": 3,
        "tao_d2_humildad": 3,
        "tao_d3_compasion": 2,
        "tao_d4_esencial": 2,
        "tao_d5_retorno": 2,
        "tao_notas": "Maria Elena tiene mucha energia y conexion con la tierra, pero enfrenta resistencia institucional del condominio.",
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "A veces",
        "sal_descanso": "Regular",
        "eco_cc_conciencia": "Es parte de nuestra motivacion de accion",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "mod_tao": "respondido",
    },
    {
        "id": "demo_restaurante",
        "proyecto_nombre": "Restaurante Raices del Maipo",
        "proyecto_cliente": "Francisco Araya",
        "proyecto_tipo_espacio": "Otro",
        "proyecto_composicion": "Organizacion o institucion",
        "proyecto_area": 180,
        "proyecto_descripcion": (
            "Restaurante de cocina chilena contemporanea en Providencia con terraza de 45m2 "
            "y patio trasero de 30m2. Francisco quiere transformar la terraza en un jardin "
            "comestible con hierbas aromaticas y verduras de hoja, instalar compostera para "
            "residuos organicos de la cocina, y crear una conexion visible entre la comida "
            "y su origen. El restaurante genera 15kg de residuos organicos diarios."
        ),
        "geo_lat": -33.4325,
        "geo_lon": -70.6150,
        "tao_d1_wu_wei": 1,
        "tao_d2_humildad": 2,
        "tao_d3_compasion": 2,
        "tao_d4_esencial": 2,
        "tao_d5_retorno": 3,
        "tao_notas": "El ritmo del restaurante es intenso. El desafio es integrar practicas regenerativas en una operacion comercial exigente.",
        "sal_alimentacion": "Muy buena -- dieta basada en plantas y local",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio leve 1-2 veces/semana",
        "sal_contacto_naturaleza": "Raramente",
        "sal_descanso": "Poco -- dormimos mal o poco",
        "eco_cc_conciencia": "Lo sentimos como una amenaza real",
        "eco_bio_conciencia": "Sabemos que existe pero parece distante",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "mod_tao": "respondido",
    },
    {
        "id": "demo_escuela",
        "proyecto_nombre": "Escuela Republica de Colombia",
        "proyecto_cliente": "Equipo docente y apoderados",
        "proyecto_tipo_espacio": "Escuela / jardin infantil",
        "proyecto_composicion": "Grupo comunitario / vecinos",
        "proyecto_area": 800,
        "proyecto_descripcion": (
            "Escuela basica municipal en Macul con 420 estudiantes. Tienen un patio de 500m2 "
            "mayoritariamente de cemento y tierra compactada. Un grupo de 12 apoderados y 4 profesores "
            "quiere crear un jardin educativo, huerto escolar y zona de juego natural. "
            "El municipio ha dado autorizacion inicial. Necesitan un plan de diseno participativo."
        ),
        "geo_lat": -33.4890,
        "geo_lon": -70.6020,
        "tao_d1_wu_wei": 2,
        "tao_d2_humildad": 2,
        "tao_d3_compasion": 3,
        "tao_d4_esencial": 2,
        "tao_d5_retorno": 1,
        "tao_notas": "Mucha energia comunitaria. Los ninos son el centro del proyecto. Falta experiencia tecnica en permacultura.",
        "sal_alimentacion": "Regular -- mezcla de procesados y frescos",
        "sal_alim_local": "No",
        "sal_alim_plantas": "A veces",
        "sal_ejercicio": "Caminatas ocasionales",
        "sal_contacto_naturaleza": "Raramente",
        "sal_descanso": "Regular",
        "eco_cc_conciencia": "Lo conocemos pero parece lejano",
        "eco_bio_conciencia": "No la conociamos",
        "eco_cont_conciencia": "La vivimos en el barrio",
        "mod_tao": "respondido",
    },
    {
        "id": "demo_huerto_comunitario",
        "proyecto_nombre": "Huerto Comunitario Cerro Blanco",
        "proyecto_cliente": "Colectivo Verde Recoleta",
        "proyecto_tipo_espacio": "Huerto comunitario",
        "proyecto_composicion": "Comunidad intencional",
        "proyecto_area": 350,
        "proyecto_descripcion": (
            "Terreno municipal recuperado de 350m2 al pie del Cerro Blanco en Recoleta. "
            "Un colectivo de 18 personas de distintas edades y origenes lleva 8 meses "
            "trabajando el espacio. Ya tienen camas de cultivo, compostera y sistema de "
            "riego por goteo basico. Quieren profundizar en diseno permacultural, "
            "agroforesteria urbana y gobernanza comunitaria del espacio."
        ),
        "geo_lat": -33.4180,
        "geo_lon": -70.6480,
        "tao_d1_wu_wei": 3,
        "tao_d2_humildad": 3,
        "tao_d3_compasion": 3,
        "tao_d4_esencial": 3,
        "tao_d5_retorno": 2,
        "tao_notas": "El colectivo tiene buena cohesion grupal y experiencia basica. Necesitan profundizar en diseno de ecosistemas.",
        "sal_alimentacion": "Buena -- mayoritariamente alimentos frescos",
        "sal_alim_local": "Frecuentemente",
        "sal_alim_plantas": "Frecuentemente",
        "sal_ejercicio": "Ejercicio moderado 3+ veces/semana",
        "sal_contacto_naturaleza": "Es parte de nuestra rutina",
        "sal_descanso": "Bien",
        "eco_cc_conciencia": "Es parte de nuestra motivacion de accion",
        "eco_bio_conciencia": "La vemos en nuestro barrio",
        "eco_cont_conciencia": "Es una preocupacion activa",
        "mod_tao": "respondido",
    },
]


def get_demo_profile(profile_id):
    """Return a demo profile dict by ID."""
    for p in DEMO_PROFILES:
        if p["id"] == profile_id:
            return dict(p)  # return copy
    return None


def list_demo_profiles():
    """Return list of (id, display_name) tuples."""
    return [(p["id"], f"{p['proyecto_nombre']} -- {p['proyecto_cliente']}") for p in DEMO_PROFILES]
