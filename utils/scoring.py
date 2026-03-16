"""scoring.py v6.0 — IPR dual (observado / potencial), escala 0-5, 5 niveles."""
import json
from pathlib import Path

def _load_petalos():
    jf = Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(jf, encoding="utf-8") as f:
            return json.load(f)["petalos"]
    except Exception:
        return []

FLOWER_DOMAINS = {
    "Administración de la Tierra y la Naturaleza": {"icon":"🌳","petal_num":1,"color":"#40916C","desc":"Sistemas regenerativos: bosques comestibles, semillas, agua y agroforestería","indicators":[]},
    "Entorno Construido":                           {"icon":"🏡","petal_num":2,"color":"#2D9596","desc":"Bioarquitectura, bioclimática, materiales naturales","indicators":[]},
    "Herramientas y Tecnología":                    {"icon":"🛠️","petal_num":3,"color":"#8B5E3C","desc":"Tecnología apropiada, eficiencia energética, reutilización","indicators":[]},
    "Educación y Cultura":                          {"icon":"📚","petal_num":4,"color":"#7B61FF","desc":"Educación viva, saberes locales, cultura regenerativa","indicators":[]},
    "Salud y Bienestar Espiritual":                 {"icon":"🧘","petal_num":5,"color":"#A67C00","desc":"Prevención, medicina holística, cuidado integral","indicators":[]},
    "Finanzas y Economía":                          {"icon":"💚","petal_num":6,"color":"#2D6A4F","desc":"Finanzas éticas, autosuficiencia, comercio justo","indicators":[]},
    "Tenencia de la Tierra y Gobernanza Comunitaria":{"icon":"🤝","petal_num":7,"color":"#1A6B6B","desc":"Gobernanza colectiva, cooperativas, resolución de conflictos","indicators":[]},
}
PETAL_ORDER = list(FLOWER_DOMAINS.keys())

# Escala 0-5: 5 niveles, máximo 5.
# Umbrales: 0=0, 1-2=1, 3-5=2, 6-9=3, 10-14=4, 15+=5
def _count_to_score(n: int) -> float:
    if n == 0:  return 0.0
    if n <= 2:  return 1.0
    if n <= 5:  return 2.0
    if n <= 9:  return 3.0
    if n <= 14: return 4.0
    return 5.0

def _score_to_level(score: float) -> tuple:
    if score == 0:    return "Sin inicio",    "#9E9E9E"
    if score <= 1:    return "Semilla",       "#74C69D"
    if score <= 2:    return "Brote",         "#52B788"
    if score <= 3:    return "Crecimiento",   "#40916C"
    if score <= 4:    return "Florecimiento", "#2D6A4F"
    return                "Abundancia",       "#1B4332"

def _ipr_obs_counts(data: dict) -> list:
    ipr_obs = data.get("ipr_obs", [])
    if ipr_obs and len(ipr_obs) >= 7:
        return [int(x) for x in ipr_obs[:7]]
    counts = []
    for i in range(7):
        obs   = data.get(f"petalo_{i}_obs", {})
        otros = data.get(f"petalo_{i}_otros_obs", [])
        n = sum(len(v) for v in obs.values() if isinstance(v, list)) + len(otros)
        counts.append(n)
    return counts

def _ipr_tot_counts(data: dict) -> list:
    ipr_tot = data.get("ipr_tot", [])
    if ipr_tot and len(ipr_tot) >= 7:
        return [int(x) for x in ipr_tot[:7]]
    counts = []
    for i in range(7):
        obs  = data.get(f"petalo_{i}_obs",      {})
        new_ = data.get(f"petalo_{i}_pot_new",  {})
        oo   = data.get(f"petalo_{i}_otros_obs", [])
        on   = data.get(f"petalo_{i}_otros_new", [])
        n = (sum(len(v) for v in obs.values()  if isinstance(v, list)) +
             sum(len(v) for v in new_.values() if isinstance(v, list)) +
             len(oo) + len(on))
        counts.append(n)
    return counts

def compute_domain_scores(data: dict) -> dict:
    counts = _ipr_obs_counts(data)
    return {PETAL_ORDER[i]: _count_to_score(counts[i]) for i in range(7)}

def compute_domain_scores_total(data: dict) -> dict:
    counts = _ipr_tot_counts(data)
    return {PETAL_ORDER[i]: _count_to_score(counts[i]) for i in range(7)}

def compute_wellbeing_score(data: dict) -> float:
    counts = _ipr_obs_counts(data)
    return _count_to_score(counts[4]) if len(counts) > 4 else 0.0

def compute_cross_module_score(data: dict) -> dict:
    """Sub-indicadores de módulos 2-6 que aportan al IPR global. Escala 0-5."""
    scores = {}
    # Suelo (M2)
    suelo_mo = data.get("suelo_materia_organica","")
    suelo_cp = data.get("suelo_compactacion","")
    suelo_dr = data.get("suelo_drenaje","")
    if any([suelo_mo, suelo_cp, suelo_dr]):
        pts = 0
        if suelo_mo == "Alto": pts += 4
        elif suelo_mo == "Medio": pts += 2
        if suelo_cp == "Baja": pts += 3
        elif suelo_cp == "Media": pts += 1
        if suelo_dr == "Bueno": pts += 3
        elif suelo_dr == "Moderado": pts += 1
        scores["Calidad del suelo"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Materia orgánica, compactación y drenaje observados.", "fuente":"M2 · Ecología"}
    # Agua (M5)
    if any([data.get("agua_captacion_lluvia"), data.get("agua_grises"), data.get("agua_riego_sistema")]):
        pts = 0
        if data.get("agua_captacion_lluvia") == "Sí": pts += 4
        elif data.get("agua_captacion_lluvia") == "Parcial": pts += 2
        if data.get("agua_grises") == "Sí": pts += 3
        elif data.get("agua_grises") == "Parcialmente": pts += 1
        if data.get("agua_riego_sistema") == "Por goteo": pts += 2
        elif data.get("agua_riego_sistema") == "Automático": pts += 1
        if data.get("agua_fugas") == "No": pts += 1
        if data.get("agua_fuente") in ["Agua reciclada","Mixta"]: pts += 2
        scores["Gestión del agua"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Captación lluvia, grises y eficiencia de riego.", "fuente":"M5 · Agua"}
    # Energía (M6)
    if any([data.get("ene_fuente"), data.get("ene_led")]):
        pts = 0
        if data.get("ene_fuente") == "Panel solar": pts += 5
        elif data.get("ene_fuente") == "Mixta": pts += 3
        if data.get("ene_led") == "Sí": pts += 3
        elif data.get("ene_led") == "Parcialmente": pts += 1
        if data.get("ene_solar_interes") == "Sí, pronto": pts += 2
        try:
            kwh = float(data.get("ene_kwh_dia_calc",0) or 0)
            if 0 < kwh < 5: pts += 2
            elif kwh < 10: pts += 1
        except Exception: pass
        scores["Eficiencia energética"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Fuente energética, LED y consumo estimado.", "fuente":"M6 · Energía"}
    # Biodiversidad (M2)
    veg_tipos = data.get("veg_tipos", [])
    if isinstance(veg_tipos, list) and veg_tipos or data.get("fauna_lombrices"):
        pts = min(len(veg_tipos) * 2, 6) if isinstance(veg_tipos, list) else 0
        if data.get("fauna_lombrices") == "Frecuentemente": pts += 2
        elif data.get("fauna_lombrices") == "Ocasionalmente": pts += 1
        if data.get("fauna_aves_especies"): pts += 2
        scores["Biodiversidad observada"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Tipos de vegetación, fauna del suelo y aves.", "fuente":"M2 · Ecología"}
    # Cultivo (M3)
    if any([data.get("cultivo_m2"), data.get("cultivo_produce_hoy")]):
        pts = 0
        try:
            area_tot  = float(data.get("proyecto_area",0) or data.get("proyecto_superficie",0) or 0)
            area_cult = float(data.get("cultivo_m2",0) or 0)
            if area_tot > 0 and area_cult > 0:
                pct = area_cult / area_tot * 100
                if pct >= 50: pts += 5
                elif pct >= 25: pts += 3
                elif pct > 0: pts += 1
        except Exception: pass
        if data.get("cultivo_produce_hoy") == "Sí": pts += 3
        elif data.get("cultivo_produce_hoy") == "Algo": pts += 1
        if data.get("cultivo_frutales") == "Sí": pts += 2
        if data.get("cultivo_verticales") == "Sí": pts += 2
        scores["Potencial productivo"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Área cultivable, producción actual y aprovechamiento.", "fuente":"M3 · Cultivo"}
    # Contexto comunitario (M4)
    ctx_vecinos = data.get("ctx_vecinos","")
    if ctx_vecinos or data.get("ctx_participacion"):
        pts = 0
        if ctx_vecinos in ["Buena","Muy buena","Excelente"]: pts += 4
        elif ctx_vecinos in ["Regular","Algo tensa"]: pts += 1
        if data.get("ctx_participacion") == "Sí, activamente": pts += 4
        elif data.get("ctx_participacion") == "A veces": pts += 2
        actores = data.get("ctx_actores",[])
        if isinstance(actores, list) and len(actores) > 0: pts += 2
        scores["Contexto comunitario"] = {"score": min(round(pts/2.0, 1), 5), "desc":"Relaciones vecinales, participación barrial y redes.", "fuente":"M4 · Contexto"}
    return scores

def compute_regenerative_score(data: dict) -> float:
    """IPR Global observado: 70% MFP + 30% módulos cruzados. Escala 0-5."""
    ds = compute_domain_scores(data)
    mfp_avg = sum(ds.values()) / 7
    cross = compute_cross_module_score(data)
    cross_vals = [v["score"] for v in cross.values()] if cross else []
    cross_avg = sum(cross_vals) / len(cross_vals) if cross_vals else 0.0
    if cross_vals:
        return min(5.0, round(mfp_avg * 0.70 + cross_avg * 0.30, 1))
    return min(5.0, round(mfp_avg, 1))

def compute_regenerative_score_potential(data: dict) -> float:
    """IPR Potencial: observado+potencial en MFP + módulos cruzados."""
    ds_tot = compute_domain_scores_total(data)
    mfp_avg = sum(ds_tot.values()) / 7
    cross = compute_cross_module_score(data)
    cross_vals = [v["score"] for v in cross.values()] if cross else []
    cross_avg = sum(cross_vals) / len(cross_vals) if cross_vals else 0.0
    if cross_vals:
        return min(5.0, round(mfp_avg * 0.70 + cross_avg * 0.30, 1))
    return min(5.0, round(mfp_avg, 1))

def score_label(score: float) -> tuple:
    if score == 0:    return "Sin inicio — potencial enorme por revelar", "#9E9E9E"
    if score <= 1:    return "Semilla — el terreno está listo para regenerar", "#74C69D"
    if score <= 2:    return "Brote — primeros pasos regenerativos en marcha", "#52B788"
    if score <= 3:    return "Crecimiento — el espacio florece hacia la regeneración", "#40916C"
    if score <= 4:    return "Florecimiento — espacio regenerativo sólido y activo", "#2D6A4F"
    return "Abundancia — referente vivo de regeneración", "#1B4332"

def compute_synthesis_potentials(data: dict) -> dict:
    """
    10 dimensiones de potencial regenerativo — perspectiva potencial (obs+pot). 0-5.
    Integra MFP (pétalos) + datos observados de módulos 2-6.
    """
    counts_tot = _ipr_tot_counts(data)
    counts_obs = _ipr_obs_counts(data)

    def _p(mk, pi):
        v = data.get(mk)
        if v is not None:
            try: return min(5.0, float(v))
            except: pass
        return _count_to_score(counts_tot[pi]) if pi < len(counts_tot) else 0.0

    def _cross(key_si, key_no, key_pa=None, pts_si=5, pts_no=0, pts_pa=2):
        """Score from a Yes/No/Partial field."""
        v = data.get(key_si, "")
        if v == "Sí": return min(5.0, pts_si / 10 * 5)
        if key_pa and v == key_pa: return min(5.0, pts_pa / 10 * 5)
        return 0.0

    # 1. Producción alimentaria — P0 (Tierra) + cultivo M3
    prod = _p("sint_pot_alimentaria", 0)
    if data.get("cultivo_produce_hoy") == "Sí": prod = min(5.0, prod + 0.5)
    result = {"Producción alimentaria": round(min(5.0, prod), 1)}

    # 2. Biodiversidad urbana — P0 (Tierra) + veg/fauna M2
    bio = _p("sint_pot_biodiversidad", 0)
    veg_tipos = data.get("veg_tipos", [])
    if isinstance(veg_tipos, list) and len(veg_tipos) >= 3: bio = min(5.0, bio + 0.5)
    result["Biodiversidad urbana"] = round(min(5.0, bio), 1)

    # 3. Regeneración del suelo — P0 (Tierra) + suelo M2
    suelo = _p("sint_pot_suelo", 0)
    if data.get("suelo_materia_organica") == "Alto": suelo = min(5.0, suelo + 1.0)
    elif data.get("suelo_materia_organica") == "Medio": suelo = min(5.0, suelo + 0.5)
    result["Regeneración del suelo"] = round(min(5.0, suelo), 1)

    # 4. Captación y gestión del agua — P2 (Herramientas) + agua M5
    agua = _p("sint_pot_agua", 2)
    if data.get("agua_captacion_lluvia") == "Sí": agua = min(5.0, agua + 1.0)
    elif data.get("agua_captacion_lluvia") == "Parcial": agua = min(5.0, agua + 0.5)
    if data.get("agua_grises") == "Sí": agua = min(5.0, agua + 0.5)
    result["Captación y gestión del agua"] = round(min(5.0, agua), 1)

    # 5. Energía y eficiencia — P2 (Herramientas) + energía M6
    ene_pts = 0
    if data.get("ene_fuente") == "Panel solar": ene_pts += 5
    elif data.get("ene_fuente") == "Mixta": ene_pts += 3
    if data.get("ene_led") == "Sí": ene_pts += 3
    elif data.get("ene_led") == "Parcialmente": ene_pts += 1
    if data.get("ene_solar_interes") == "Sí, pronto": ene_pts += 2
    p2_score = _count_to_score(counts_tot[2]) if len(counts_tot) > 2 else 0.0
    ene_cross = min(5.0, round(ene_pts / 10 * 5, 1))
    ene = max(p2_score, ene_cross) if (data.get("ene_fuente") or data.get("ene_led")) else p2_score
    result["Energía y eficiencia"] = round(min(5.0, ene), 1)

    # 6. Educación ambiental — P3 (Educación)
    result["Educación ambiental"] = round(_p("sint_pot_educacion", 3), 1)

    # 7. Bienestar comunitario — P6 (Gobernanza) + contexto M4
    com = _p("sint_pot_bienestar", 6)
    ctx_vecinos = data.get("ctx_vecinos", "")
    if ctx_vecinos in ["Buena", "Muy buena", "Excelente"]: com = min(5.0, com + 0.5)
    if data.get("ctx_participacion") == "Sí, activamente": com = min(5.0, com + 0.5)
    result["Bienestar comunitario"] = round(min(5.0, com), 1)

    # 8. Economía regenerativa — P5 (Finanzas)
    result["Economía regenerativa"] = round(_p("sint_pot_economia", 5), 1)

    # 9. Salud y bienestar — P4 (Salud)
    result["Salud y bienestar"] = round(_p("sint_pot_interior", 4), 1)

    # 10. Entorno construido — P1 (Entorno)
    result["Entorno construido"] = round(_p("sint_pot_entorno", 1), 1)

    return result


def compute_synthesis_potentials_obs(data: dict) -> dict:
    """10 dimensiones — perspectiva observada. 0-5."""
    counts_obs = _ipr_obs_counts(data)
    def _o(pi): return _count_to_score(counts_obs[pi]) if pi < len(counts_obs) else 0.0

    ene_pts = 0
    if data.get("ene_fuente") == "Panel solar": ene_pts += 5
    elif data.get("ene_fuente") == "Mixta": ene_pts += 3
    if data.get("ene_led") == "Sí": ene_pts += 3
    elif data.get("ene_led") == "Parcialmente": ene_pts += 1
    p2_obs = _o(2)
    ene_cross = min(5.0, round(ene_pts / 10 * 5, 1))
    ene_obs = max(p2_obs, ene_cross) if (data.get("ene_fuente") or data.get("ene_led")) else p2_obs

    return {
        "Producción alimentaria":       round(_o(0), 1),
        "Biodiversidad urbana":         round(_o(0), 1),
        "Regeneración del suelo":       round(_o(0), 1),
        "Captación y gestión del agua": round(_o(2), 1),
        "Energía y eficiencia":         round(min(5.0, ene_obs), 1),
        "Educación ambiental":          round(_o(3), 1),
        "Bienestar comunitario":        round(_o(6), 1),
        "Economía regenerativa":        round(_o(5), 1),
        "Salud y bienestar":            round(_o(4), 1),
        "Entorno construido":           round(_o(1), 1),
    }


# ── Descripción de qué mide cada dimensión ───────────────────────────────────
DIM_WHAT_MEASURES = {
    "Producción alimentaria": {
        "que_mide": "La capacidad del espacio de producir alimentos frescos: hortalizas, hierbas, frutales, hongos y germinados.",
        "fuentes":  "Módulo 7 · Pétalo 1 (Tierra) + Módulo 3 · Cultivo",
        "icono":    "🥦",
    },
    "Biodiversidad urbana": {
        "que_mide": "La diversidad de vida presente: plantas nativas, polinizadores, aves, lombrices y cobertura vegetal.",
        "fuentes":  "Módulo 7 · Pétalo 1 (Tierra) + Módulo 2 · Ecología",
        "icono":    "🦋",
    },
    "Regeneración del suelo": {
        "que_mide": "La salud biológica del suelo: materia orgánica, compostaje, cobertura y actividad microbiana.",
        "fuentes":  "Módulo 7 · Pétalo 1 (Tierra) + Módulo 2 · Suelo",
        "icono":    "🌍",
    },
    "Captación y gestión del agua": {
        "que_mide": "La autonomía hídrica del espacio: captación de lluvia, reutilización de grises, eficiencia de riego.",
        "fuentes":  "Módulo 7 · Pétalo 3 (Herramientas) + Módulo 5 · Agua",
        "icono":    "💧",
    },
    "Energía y eficiencia": {
        "que_mide": "El nivel de eficiencia energética y transición hacia renovables: paneles solares, LED, bajo consumo.",
        "fuentes":  "Módulo 7 · Pétalo 3 (Herramientas) + Módulo 6 · Energía",
        "icono":    "⚡",
    },
    "Educación ambiental": {
        "que_mide": "Las prácticas de aprendizaje, transmisión de saberes y formación en ecología y vida regenerativa.",
        "fuentes":  "Módulo 7 · Pétalo 4 (Educación y Cultura)",
        "icono":    "📚",
    },
    "Bienestar comunitario": {
        "que_mide": "La calidad de los vínculos sociales: relaciones vecinales, participación comunitaria y redes de apoyo.",
        "fuentes":  "Módulo 7 · Pétalo 7 (Gobernanza) + Módulo 4 · Contexto",
        "icono":    "🤝",
    },
    "Economía regenerativa": {
        "que_mide": "Las prácticas de economía circular: autosuficiencia, trueque, mercados locales y consumo consciente.",
        "fuentes":  "Módulo 7 · Pétalo 6 (Finanzas y Economía)",
        "icono":    "💚",
    },
    "Salud y bienestar": {
        "que_mide": "El cuidado de la salud integral: alimentación viva, plantas medicinales, movimiento y bienestar espiritual.",
        "fuentes":  "Módulo 7 · Pétalo 5 (Salud y Bienestar Espiritual)",
        "icono":    "🧘",
    },
    "Entorno construido": {
        "que_mide": "La calidad del espacio físico: bioarquitectura, diseño bioclimático, techos/muros verdes y materiales naturales.",
        "fuentes":  "Módulo 7 · Pétalo 2 (Entorno Construido)",
        "icono":    "🏡",
    },
}

# ── Textos duales (Español Chileno, tono LivLin) ─────────────────────────────
DIM_INTERP_DUAL = {
    "Producción alimentaria":{
        "actual":["Este espacio todavía no produce alimentos, pero el potencial está ahí esperando. Una maceta o un germinado es el inicio del camino.","Hay una primera chispa de producción. Todavía es pequeña, pero ya está pasando algo importante en este espacio.","El espacio ya produce algunos alimentos. Es un comienzo real, con raíces que van tomando fuerza.","Hay producción alimentaria activa y variada. Este espacio contribuye con alimentos frescos a quienes lo habitan.","El espacio es una fuente relevante de alimentos. Un ejemplo concreto de soberanía alimentaria urbana.","Abundancia alimentaria real. Este espacio produce, comparte y demuestra que la ciudad puede alimentarse desde adentro."],
        "potencial":["Con una primera maceta o bancal, este espacio puede comenzar a producir alimentos frescos. El camino está completamente abierto.","Las prácticas identificadas abren la posibilidad de escalar la producción. Hay espacio y condiciones para crecer.","Sumando las prácticas potenciales, este espacio puede convertirse en una fuente real de alimentos para el grupo.","El potencial identificado puede fortalecer significativamente la producción. Este espacio tiene todo para avanzar.","Con lo que se puede incorporar, este espacio podría convertirse en un referente de producción urbana regenerativa.","Este espacio tiene el potencial de ser un modelo vivo de abundancia alimentaria. El camino ya está trazado."],
    },
    "Biodiversidad urbana":{
        "actual":["La biodiversidad está por despertar. No se observan prácticas activas, pero el espacio tiene todo para acoger vida.","Hay primeras señales de vida. La biodiversidad está dando sus primeros pasos en este espacio.","Se observan prácticas que apoyan la vida en el espacio. La biodiversidad comienza a tener presencia real.","El espacio alberga biodiversidad activa. Hay plantas, polinizadores o fauna que ya se benefician del cuidado.","Alta biodiversidad funcional. El espacio es un refugio vivo que contribuye a la resiliencia del entorno.","El espacio es un santuario de biodiversidad urbana — modelo de cómo las ciudades pueden volver a ser hogar de vida."],
        "potencial":["Incorporar nativas, crear refugios o plantar flores sería un cambio enorme para la vida en este espacio.","Las prácticas identificadas pueden convertir este espacio en corredor de polinizadores y aves del barrio.","Con lo que se puede sumar, este espacio tiene el potencial de ser un nodo real de biodiversidad.","El potencial identificado puede transformar este espacio en un refugio reconocido de biodiversidad urbana.","Este espacio podría convertirse en referente vivo de cómo recuperar la biodiversidad en la ciudad.","El potencial de este espacio es extraordinario — puede ser un santuario de vida en medio de la ciudad."],
    },
    "Captación de agua":{
        "actual":["El espacio depende completamente del agua de red. Cada gota que se capture o reutilice es un paso hacia la autonomía hídrica.","Hay conciencia sobre el agua y primeras intenciones. El camino hacia la soberanía hídrica está por empezar.","Existen algunos sistemas de gestión hídrica. El espacio empieza a tomar control de un recurso cada vez más escaso.","Buen manejo del agua. El espacio capta o reutiliza — modelo de eficiencia frente al estrés hídrico.","Sistema hídrico robusto. El espacio gestiona el agua como el recurso precioso que es.","Soberanía hídrica completa. Este espacio es referente de gestión regenerativa del agua."],
        "potencial":["Un barril bajo la canaleta o reutilizar el agua de la ducha son primeros pasos concretos hacia la autonomía hídrica.","Las prácticas identificadas permiten capturar y reutilizar agua. El potencial hídrico de este espacio es real.","Sumando lo identificado, este espacio puede alcanzar una gestión hídrica significativamente más autónoma.","El potencial hídrico es alto. Con las mejoras identificadas, puede convertirse en modelo de eficiencia.","Este espacio podría lograr soberanía hídrica importante. Las condiciones están dadas para avanzar.","El potencial hídrico es extraordinario — puede ser referente de autonomía hídrica en contexto urbano."],
    },
    "Regeneración del suelo":{
        "actual":["El suelo está esperando ser despertado. Sin prácticas activas aún, tiene todo el potencial para transformarse en suelo vivo.","El suelo está comenzando a regenerarse. Cada acción de compost o cobertura es un paso irreversible hacia la vida.","El suelo está mejorando. Se observan señales de vida biológica transformando la tierra desde adentro.","Buen suelo biológicamente activo. La materia orgánica y los organismos vivos trabajan para el espacio.","Suelo saludable y regenerado. Alta actividad biológica — ejemplo de cómo recuperar la tierra urbana.","Suelo vivo y abundante. Este espacio demuestra que la regeneración del suelo urbano es posible y poderosa."],
        "potencial":["Con compost, cobertura vegetal y materia orgánica, este espacio puede transformar su suelo completamente.","Las prácticas identificadas pueden despertar el suelo y convertirlo en aliado productivo del espacio.","Sumando lo identificado, este espacio puede alcanzar un suelo con actividad biológica real y productiva.","El potencial de mejora del suelo es alto. Las prácticas identificadas pueden hacer una diferencia enorme.","Este espacio puede lograr un suelo saludable y regenerado. Las condiciones están dadas para avanzar.","El potencial de este suelo es extraordinario — puede convertirse en referente de regeneración del suelo urbano."],
    },
    "Educación ambiental":{
        "actual":["El espacio tiene potencial educativo enorme todavía no activado. La educación regenerativa puede empezar con una sola conversación.","Hay interés y apertura al aprendizaje. Con pequeñas actividades, el espacio puede volverse escuela a cielo abierto.","El espacio ya genera aprendizaje activo. Hay conocimiento que se practica y comparte en el grupo.","El espacio es fuente activa de educación ambiental. La cultura del cuidado se consolida y se transmite.","El espacio educa e inspira a la comunidad. Su efecto multiplicador va más allá de quienes lo habitan.","El espacio es una escuela viva de permacultura. Su influencia educativa trasciende sus límites físicos."],
        "potencial":["Un taller, un intercambio de semillas o una biblioteca de saberes pueden activar el potencial educativo de este espacio.","Las prácticas identificadas pueden convertir este espacio en un lugar de aprendizaje vivo y cultural.","Con lo identificado, el espacio puede consolidarse como fuente de educación ambiental para el grupo y el barrio.","El potencial educativo es alto. Con las prácticas identificadas, puede inspirar a mucha gente.","Este espacio podría convertirse en referente educativo de permacultura para su comunidad.","El potencial educativo es extraordinario — puede ser escuela viva que inspire a toda la ciudad."],
    },
    "Bienestar comunitario":{
        "actual":["Los lazos comunitarios están por tejerse. El espacio tiene todo para ser nodo de encuentro y cuidado colectivo.","Hay algunos vínculos comunitarios emergiendo. Con más actividades, el espacio puede fortalecer su comunidad.","El espacio muestra una red comunitaria en desarrollo. Los vínculos son la base de la resiliencia.","Buena red comunitaria activa. El espacio genera encuentros y colaboraciones reales.","Excelente bienestar comunitario. El espacio genera confianza, colaboración y apoyo mutuo de manera consistente.","El espacio es un corazón comunitario — modelo de cómo los espacios urbanos pueden ser bienestar colectivo."],
        "potencial":["Con iniciativas compartidas, aunque sean pequeñas, este espacio puede empezar a tejer comunidad de verdad.","Las prácticas identificadas pueden fortalecer los vínculos comunitarios de este espacio significativamente.","Sumando lo identificado, este espacio puede convertirse en punto de encuentro real para su comunidad.","El potencial comunitario es alto. Con lo identificado, puede consolidarse como nodo de resiliencia barrial.","Este espacio podría convertirse en referente de bienestar comunitario para su barrio.","El potencial comunitario es extraordinario — puede ser un corazón vivo de la comunidad."],
    },
    "Economía regenerativa":{
        "actual":["El espacio está al inicio de su transición económica. El potencial para avanzar hacia la autosuficiencia y el intercambio justo es enorme.","Hay primeras prácticas de economía alternativa emergiendo. El espacio puede convertirse en nodo de intercambio local.","El espacio practica formas de economía regenerativa — autoproducción, intercambio o consumo más consciente.","Buenas prácticas de economía regenerativa. El espacio produce excedentes y contribuye a economías más justas.","El espacio es modelo de economía regenerativa — autosuficiencia, intercambio y finanzas éticas en conjunto.","El espacio es referente de economía circular y regenerativa en su comunidad."],
        "potencial":["Compartir semillas, producir alimentos o reducir compras son primeros pasos hacia una economía regenerativa.","Las prácticas identificadas pueden convertir este espacio en nodo activo de economía local y circular.","Con lo identificado, el espacio puede avanzar significativamente hacia la autosuficiencia y el intercambio justo.","El potencial económico regenerativo es alto. Con lo identificado, puede ser modelo real de economía alternativa.","Este espacio puede convertirse en referente de economía regenerativa para su barrio y comunidad.","El potencial es extraordinario — puede demostrar en la práctica que otra economía es posible."],
    },
    "Bienestar interior":{
        "actual":["El espacio tiene potencial enorme para nutrir la dimensión interior. No se observan prácticas activas de bienestar y conexión.","Hay primeras señales de conexión interior. Este vínculo puede profundizarse y ser fuente de bienestar y propósito.","El espacio ya nutre el bienestar interior. Hay prácticas de conexión con la naturaleza que vale cultivar.","Buen nivel de bienestar interior. El espacio genera conexión, calma y sentido — base de una vida regenerativa.","El espacio es fuente activa de bienestar interior y conexión profunda con la naturaleza.","El espacio es un santuario interior — la conexión del grupo con la naturaleza es profunda y transformadora."],
        "potencial":["Un rincón de silencio, tiempo en contacto con la tierra o prácticas contemplativas pueden transformar la dimensión interior.","Las prácticas identificadas pueden profundizar la conexión interior del grupo con el espacio de manera real.","Sumando lo identificado, este espacio puede convertirse en fuente real de bienestar interior y calma.","El potencial de bienestar interior es alto. Con lo identificado, puede nutrir profundamente al grupo.","Este espacio podría convertirse en un santuario de bienestar interior. Las condiciones están dadas.","El potencial interior es extraordinario — puede ser fuente profunda de conexión y transformación."],
    },
    "Captación y gestión del agua":{
        "actual":["El espacio depende completamente del agua de red. Cada gota que se capture o reutilice es un paso hacia la autonomía hídrica.","Hay conciencia sobre el agua y primeras intenciones. El camino hacia la soberanía hídrica está por empezar.","Existen algunos sistemas de gestión hídrica. El espacio empieza a tomar control de un recurso cada vez más escaso.","Buen manejo del agua. El espacio capta o reutiliza — modelo de eficiencia frente al estrés hídrico.","Sistema hídrico robusto. El espacio gestiona el agua como el recurso precioso que es.","Soberanía hídrica completa. Este espacio es referente de gestión regenerativa del agua."],
        "potencial":["Un barril bajo la canaleta o reutilizar el agua de la ducha son primeros pasos concretos hacia la autonomía hídrica.","Las prácticas identificadas permiten capturar y reutilizar agua. El potencial hídrico de este espacio es real.","Sumando lo identificado, este espacio puede alcanzar una gestión hídrica significativamente más autónoma.","El potencial hídrico es alto. Con las mejoras identificadas, puede convertirse en modelo de eficiencia.","Este espacio podría lograr soberanía hídrica importante. Las condiciones están dadas para avanzar.","El potencial hídrico es extraordinario — puede ser referente de autonomía hídrica en contexto urbano."],
    },
    "Energía y eficiencia":{
        "actual":["El espacio no ha incorporado tecnologías de eficiencia energética. Hay un gran potencial para mejorar el consumo y avanzar hacia las renovables.","Hay primeras intenciones o pequeñas mejoras en eficiencia. El camino hacia la autonomía energética está comenzando.","El espacio tiene algunas prácticas de eficiencia activas. La LED o el interés en solar son señales de avance concreto.","Buen nivel de eficiencia energética. El espacio reduce su consumo y avanza hacia fuentes renovables.","El espacio tiene energía solar u otras renovables activas. La eficiencia energética es parte de su identidad.","El espacio es referente de eficiencia y autonomía energética — un modelo de transición renovable urbana."],
        "potencial":["Cambiar a LED, desconectar cargadores o planificar paneles solares son pasos concretos hacia la autonomía energética.","Las prácticas identificadas pueden reducir el consumo y avanzar hacia la independencia energética.","Con lo identificado, este espacio puede alcanzar una eficiencia energética real y comenzar la transición solar.","El potencial energético es alto. Con lo identificado, puede lograr autonomía energética significativa.","Este espacio podría convertirse en modelo de transición energética renovable para su comunidad.","El potencial es extraordinario — puede ser referente de eficiencia y energía renovable en contexto urbano."],
    },
    "Salud y bienestar":{
        "actual":["El espacio todavía no ha activado su dimensión de salud y bienestar. Hay potencial enorme para nutrir el cuerpo, la mente y el espíritu.","Hay primeras prácticas de salud y bienestar activas. El cuidado integral empieza a tener presencia en el espacio.","El espacio ya cuida la salud y el bienestar del grupo. Hay prácticas de alimentación, movimiento o contemplación integradas.","El espacio es fuente real de salud y bienestar. Las prácticas integradas nutren el cuerpo, la mente y el espíritu.","El espacio es referente de salud y bienestar integral — alimentación viva, plantas medicinales y cuidado colectivo.","Este espacio es santuario de salud y bienestar integral — transforma profundamente la calidad de vida del grupo."],
        "potencial":["Cultivar plantas medicinales, mejorar la alimentación o crear espacios de contemplación pueden transformar el bienestar.","Las prácticas identificadas pueden incorporar elementos de salud y bienestar que nutran al grupo de manera real.","Con lo identificado, el espacio puede convertirse en fuente activa de salud y bienestar integral.","El potencial de salud y bienestar es alto. Con lo identificado, puede transformar profundamente al grupo.","Este espacio puede convertirse en referente de salud y bienestar integral para su comunidad.","El potencial es extraordinario — puede ser santuario de salud y bienestar que inspire a muchos."],
    },
    "Entorno construido":{
        "actual":["El entorno construido todavía no incorpora elementos regenerativos. Hay oportunidades concretas para empezar a transformar el espacio físico.","Hay primeras incorporaciones regenerativas en el entorno construido. El espacio empieza a integrar bioclimática o materiales naturales.","El entorno construido muestra prácticas regenerativas activas — bioarquitectura, energía pasiva o naturaleza integrada.","El entorno construido es activamente regenerativo. El diseño trabaja a favor del bienestar, la eficiencia y la vida.","El espacio construido es ejemplo de diseño regenerativo — integra naturaleza, eficiencia y materiales naturales.","El entorno construido es referente de bioarquitectura y diseño bioclimático regenerativo."],
        "potencial":["Una pérgola verde, materiales naturales o ventilación cruzada pueden transformar el entorno construido.","Las prácticas identificadas pueden incorporar elementos regenerativos al entorno construido de manera real.","Con lo identificado, el espacio puede avanzar hacia un entorno construido que trabaja en armonía con la naturaleza.","El potencial de transformación del entorno construido es alto. Puede ser modelo de diseño regenerativo.","Este espacio puede convertirse en ejemplo de entorno construido regenerativo para su barrio.","El potencial es extraordinario — puede ser referente de bioarquitectura urbana."],
    },
}

PETAL_INTERP_DUAL = {
    "Administración de la Tierra y la Naturaleza":{
        "actual":["Este espacio todavía no ha activado su relación con la tierra. Cualquier primera práctica — un huerto, una compostera, una planta nativa — es el inicio de un camino transformador.","Hay primeras prácticas activas en la gestión de la tierra. La semilla está plantada y el camino hacia la regeneración ha comenzado.","El espacio ya cuida su relación con la tierra. Hay prácticas concretas de producción, suelo o biodiversidad generando cambio real.","El espacio tiene una relación activa y madura con la tierra. Las prácticas regenerativas están consolidadas y generan resultados visibles.","El espacio es un ejemplo de administración regenerativa de la tierra. Las prácticas integradas generan abundancia y ciclos cerrados.","Este espacio es un modelo vivo de administración regenerativa. Inspirador, replicable y en constante evolución."],
        "potencial":["Con un huerto, una compostera o algunas plantas nativas, este espacio puede comenzar a administrar su tierra de manera regenerativa.","Las prácticas identificadas pueden transformar significativamente la relación de este espacio con su tierra.","Sumando las prácticas potenciales, este espacio puede alcanzar una gestión de la tierra integrada y productiva.","El potencial en administración de la tierra es alto. Con lo identificado, puede consolidarse como referente.","Este espacio puede convertirse en modelo de administración regenerativa de la tierra para su comunidad.","El potencial es extraordinario — puede ser un modelo vivo de relación regenerativa con la tierra."],
    },
    "Entorno Construido":{
        "actual":["El entorno construido todavía no incorpora elementos regenerativos. Hay oportunidades concretas para empezar a transformar el espacio físico.","Hay primeras incorporaciones regenerativas en el entorno construido. El espacio empieza a integrar bioclimática o materiales naturales.","El entorno construido muestra prácticas regenerativas activas — bioarquitectura, energía pasiva o naturaleza integrada.","El entorno construido es activamente regenerativo. El diseño trabaja a favor del bienestar, la eficiencia y la vida.","El espacio construido es ejemplo de diseño regenerativo — integra naturaleza, eficiencia y materiales naturales.","El entorno construido es referente de bioarquitectura y diseño bioclimático regenerativo."],
        "potencial":["Una pérgola verde, materiales naturales o ventilación cruzada pueden transformar el entorno construido.","Las prácticas identificadas pueden incorporar elementos regenerativos al entorno construido de manera real.","Con lo identificado, el espacio puede avanzar hacia un entorno construido que trabaja en armonía con la naturaleza.","El potencial de transformación del entorno construido es alto. Puede ser modelo de diseño regenerativo.","Este espacio puede convertirse en ejemplo de entorno construido regenerativo para su barrio.","El potencial es extraordinario — puede ser referente de bioarquitectura urbana."],
    },
    "Herramientas y Tecnología":{
        "actual":["El espacio todavía no ha incorporado tecnologías apropiadas. Hay potencial enorme para mejorar la eficiencia y la autonomía.","Hay primeras herramientas o tecnologías apropiadas en uso. El espacio empieza a tomar control de sus recursos.","El espacio usa varias tecnologías apropiadas. La eficiencia energética y la autonomía tecnológica van creciendo.","Buen uso de herramientas y tecnologías regenerativas. El espacio tiene autonomía real y eficiencia demostrada.","El espacio es modelo de tecnología apropiada — renovables, eficiencia y herramientas simples en conjunto.","Este espacio es referente de tecnología apropiada y regenerativa en contexto urbano."],
        "potencial":["Panel solar, estufa rocket, fermentación de alimentos — hay tecnologías simples que pueden transformar este espacio.","Las prácticas identificadas pueden mejorar la autonomía tecnológica y eficiencia del espacio significativamente.","Con lo identificado, el espacio puede incorporar herramientas que cierren ciclos de recursos de manera real.","El potencial tecnológico es alto. Con lo identificado, puede lograr autonomía energética e hídrica real.","Este espacio puede convertirse en modelo de tecnología apropiada para su comunidad.","El potencial tecnológico es extraordinario — puede ser referente de autonomía regenerativa."],
    },
    "Educación y Cultura":{
        "actual":["El espacio tiene gran potencial educativo todavía no activado. La educación regenerativa puede empezar con una sola conversación.","Hay primeras prácticas educativas y culturales activas. El espacio empieza a construir cultura regenerativa.","El espacio genera aprendizaje y cultura regenerativa. Los saberes se practican y comparten activamente.","El espacio es fuente activa de educación y cultura regenerativa — inspira y forma a quienes lo habitan.","El espacio es referente educativo y cultural regenerativo. Su influencia se extiende al barrio.","Este espacio es escuela viva y centro cultural regenerativo — modelo transformador para la ciudad."],
        "potencial":["Un taller, un intercambio de semillas o una biblioteca de saberes pueden activar el potencial educativo.","Las prácticas identificadas pueden convertir este espacio en lugar de aprendizaje vivo y cultural.","Con lo identificado, el espacio puede consolidarse como fuente activa de educación y cultura regenerativa.","El potencial educativo y cultural es alto. Con lo identificado, puede inspirar a mucha gente.","Este espacio podría convertirse en referente educativo regenerativo para su comunidad.","El potencial es extraordinario — puede ser motor de cultura regenerativa para toda la ciudad."],
    },
    "Salud y Bienestar Espiritual":{
        "actual":["El espacio todavía no ha activado su dimensión de salud y bienestar. Hay potencial enorme para nutrir el cuerpo, la mente y el espíritu.","Hay primeras prácticas de salud y bienestar activas. El cuidado integral empieza a tener presencia en el espacio.","El espacio ya cuida la salud y el bienestar del grupo. Hay prácticas de alimentación, movimiento o contemplación integradas.","El espacio es fuente real de salud y bienestar. Las prácticas integradas nutren el cuerpo, la mente y el espíritu.","El espacio es referente de salud y bienestar integral — alimentación viva, plantas medicinales y cuidado colectivo.","Este espacio es santuario de salud y bienestar integral — transforma profundamente la calidad de vida del grupo."],
        "potencial":["Cultivar plantas medicinales, mejorar la alimentación o crear espacios de contemplación pueden transformar el bienestar.","Las prácticas identificadas pueden incorporar elementos de salud y bienestar que nutran al grupo de manera real.","Con lo identificado, el espacio puede convertirse en fuente activa de salud y bienestar integral.","El potencial de salud y bienestar es alto. Con lo identificado, puede transformar profundamente al grupo.","Este espacio puede convertirse en referente de salud y bienestar integral para su comunidad.","El potencial es extraordinario — puede ser santuario de salud y bienestar que inspire a muchos."],
    },
    "Finanzas y Economía":{
        "actual":["El espacio todavía no ha activado prácticas de economía regenerativa. El potencial para avanzar hacia la autosuficiencia es enorme.","Hay primeras prácticas de economía regenerativa activas. El espacio empieza a reducir su dependencia extractiva.","El espacio practica varias formas de economía regenerativa — autoproducción, intercambio o consumo consciente.","El espacio tiene prácticas económicas regenerativas consolidadas. Genera valor, lo comparte y contribuye.","El espacio es modelo de economía regenerativa — autosuficiencia, intercambio y finanzas éticas funcionando.","Este espacio es referente de economía circular y regenerativa — demostrando que otra economía es posible."],
        "potencial":["Intercambiar semillas, producir alimentos para compartir o reducir compras son primeros pasos concretos.","Las prácticas identificadas pueden convertir este espacio en nodo activo de economía local y circular.","Con lo identificado, el espacio puede avanzar significativamente hacia la autosuficiencia y el intercambio justo.","El potencial económico regenerativo es alto. Con lo identificado, puede ser modelo real de economía alternativa.","Este espacio puede convertirse en referente de economía regenerativa para su barrio y comunidad.","El potencial es extraordinario — puede demostrar en la práctica que otra economía es posible."],
    },
    "Tenencia de la Tierra y Gobernanza Comunitaria":{
        "actual":["El espacio todavía no ha activado prácticas de gobernanza comunitaria. El potencial para construir comunidad es enorme.","Hay primeras prácticas de gobernanza y participación comunitaria activas. Los lazos con la comunidad empiezan.","El espacio ya practica gobernanza comunitaria. Hay participación, organización y cuidado colectivo del territorio.","El espacio tiene gobernanza comunitaria consolidada — participación, redes territoriales y cuidado colectivo.","El espacio es modelo de gobernanza comunitaria regenerativa — organización, participación y cuidado del territorio.","Este espacio es referente de gobernanza comunitaria y tenencia colectiva de la tierra."],
        "potencial":["Conectar con vecinos, participar en iniciativas del barrio o recuperar un sitio eriazo son primeros pasos concretos.","Las prácticas identificadas pueden fortalecer los vínculos comunitarios y la gobernanza del espacio.","Con lo identificado, el espacio puede avanzar hacia una gobernanza comunitaria activa y mayor cuidado del territorio.","El potencial de gobernanza comunitaria es alto. Con lo identificado, puede ser modelo de organización territorial.","Este espacio puede convertirse en referente de gobernanza comunitaria y cuidado colectivo del territorio.","El potencial es extraordinario — puede ser modelo vivo de gobernanza regenerativa y tenencia comunitaria."],
    },
}

def get_interp_text(dim: str, score: float, perspective: str = "actual") -> str:
    idx = min(5, round(score))
    texts = DIM_INTERP_DUAL.get(dim, {}).get(perspective, [])
    if not texts: return ""
    return texts[min(idx, len(texts)-1)]

def get_petal_interp(petal_name: str, score: float, perspective: str = "actual") -> str:
    idx = min(5, round(score))
    texts = PETAL_INTERP_DUAL.get(petal_name, {}).get(perspective, [])
    if not texts: return ""
    return texts[min(idx, len(texts)-1)]

IPR_METODOLOGIA = """
El Indice de Potencial Regenerativo (IPR) v6.0 mide el nivel de actividad regenerativa del espacio en dos perspectivas complementarias:

ESTADO ACTUAL: Lo que ya está ocurriendo en el espacio hoy. Refleja las prácticas activas observadas. Un puntaje bajo no indica carencia — indica el enorme potencial de transformación disponible.

POTENCIAL PROYECTADO: Lo que el espacio podría llegar a ser incorporando las prácticas adicionales identificadas por el facilitador. Describe el horizonte posible si se avanza en el camino regenerativo.

COMPOSICIÓN DEL IPR GLOBAL (escala 0-5):
  70% — Modelo Flor de la Permacultura (MFP): promedio de los 7 pétalos de Holmgren (2002).
  30% — Sub-indicadores de módulos 2-6: calidad del suelo, gestión del agua, eficiencia energética, biodiversidad observada, potencial productivo y contexto comunitario.

ESCALA DE NIVELES:
  0   = Sin inicio    — El camino regenerativo está por comenzar
  2   = Semilla       — Primeras prácticas activas
  4   = Brote         — Prácticas en marcha, el espacio está creciendo
  6   = Crecimiento   — Prácticas consolidadas, regenera con fuerza
  8   = Florecimiento — Alta densidad de prácticas, referente local
  10  = Abundancia    — Modelo vivo de regeneración

PUNTUACIÓN POR PRÁCTICAS (MFP):
  0=0 | 1-2=2 | 3-5=4 | 6-9=6 | 10-14=8 | 15+=10
"""
