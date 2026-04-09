"""scoring.py v7.0 — ERP / HRP dual, escala 0-10, 5 niveles narrativos.

ERP (Estado Regenerativo Presente):
    80% MFP observado (7 pétalos, solo prácticas activas hoy)
    20% Sub-indicadores M2-6
HRP (Horizonte Regenerativo Potencial):
    100% MFP proyectado (obs+pot). Sin sub-indicadores M2-6.
"""
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
    "Administración de la Tierra y la Naturaleza": {"icon":"🌳","petal_num":1,"color":"#40916C","desc":"Sistemas regenerativos: bosques comestibles, semillas, agua y agroforestería"},
    "Entorno Construido":                           {"icon":"🏡","petal_num":2,"color":"#2D9596","desc":"Bioarquitectura, bioclimática, materiales naturales"},
    "Herramientas y Tecnología":                    {"icon":"🛠️","petal_num":3,"color":"#8B5E3C","desc":"Tecnología apropiada, eficiencia energética, reutilización"},
    "Educación y Cultura":                          {"icon":"📚","petal_num":4,"color":"#7B61FF","desc":"Educación viva, saberes locales, cultura regenerativa"},
    "Salud y Bienestar Espiritual":                 {"icon":"🧘","petal_num":5,"color":"#A67C00","desc":"Prevención, medicina holística, cuidado integral"},
    "Finanzas y Economía":                          {"icon":"💚","petal_num":6,"color":"#2D6A4F","desc":"Finanzas éticas, autosuficiencia, comercio justo"},
    "Tenencia de la Tierra y Gobernanza Comunitaria":{"icon":"🤝","petal_num":7,"color":"#1A6B6B","desc":"Gobernanza colectiva, cooperativas, resolución de conflictos"},
}
PETAL_ORDER = list(FLOWER_DOMAINS.keys())

# Escala 0-10: mapeo prácticas -> puntaje
def _count_to_score(n: int) -> float:
    if n == 0:  return 0.0
    if n <= 2:  return 2.0
    if n <= 5:  return 4.0
    if n <= 9:  return 6.0
    if n <= 14: return 8.0
    return 10.0

def _score_to_level(score: float) -> tuple:
    if score < 2:   return "Sin inicio",    "#9E9E9E"
    if score < 4:   return "Semilla",       "#74C69D"
    if score < 6:   return "Brote",         "#52B788"
    if score < 8:   return "Crecimiento",   "#40916C"
    return              "Abundancia",       "#1B4332"

def _score_to_level_idx(score: float) -> int:
    if score < 2: return 0
    if score < 4: return 1
    if score < 6: return 2
    if score < 8: return 3
    return 4

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
        obs  = data.get(f"petalo_{i}_obs", {})
        new_ = data.get(f"petalo_{i}_pot_new", {})
        oo   = data.get(f"petalo_{i}_otros_obs", [])
        on   = data.get(f"petalo_{i}_otros_new", [])
        n = (sum(len(v) for v in obs.values() if isinstance(v, list)) +
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

# ── Sub-indicadores M2-6 transparencia ────────────────────────────────
CROSS_MODULE_DETAIL = {
    "Calidad del suelo": {
        "variables": [("Materia orgánica","Alto=8 · Medio=4 · Bajo=0"),("Compactación","Baja=6 · Media=2 · Alta=0"),("Drenaje","Bueno=6 · Moderado=2 · Malo=0")],
        "formula": "Suma / 2, máx 10", "fuente": "M2 · Ecología", "icono": "🪱",
    },
    "Gestión del agua": {
        "variables": [("Captación lluvia","Sí=8 · Parcial=4"),("Aguas grises","Sí=6 · Parcial=2"),("Riego","Goteo=4 · Auto=2"),("Fugas","No=2"),("Fuente","Reciclada/Mixta=4")],
        "formula": "Suma / 2.4, máx 10", "fuente": "M5 · Agua", "icono": "💧",
    },
    "Eficiencia energética": {
        "variables": [("Fuente","Solar=10 · Mixta=6"),("LED","Sí=6 · Parcial=2"),("Interés solar","Pronto=4"),("Consumo","<5kWh=4 · <10=2")],
        "formula": "Suma / 2.4, máx 10", "fuente": "M6 · Energía", "icono": "⚡",
    },
    "Biodiversidad observada": {
        "variables": [("Tipos vegetación","2 pts c/u, máx 12"),("Lombrices","Frec=4 · Ocas=2"),("Aves","Spp obs=4")],
        "formula": "Suma / 2, máx 10", "fuente": "M2 · Ecología", "icono": "🦋",
    },
    "Potencial productivo": {
        "variables": [("% cultivable","≥50%=10 · ≥25%=6 · >0=2"),("Producción","Sí=6 · Algo=2"),("Frutales","Sí=4"),("Vertical","Sí=4")],
        "formula": "Suma / 2.4, máx 10", "fuente": "M3 · Cultivo", "icono": "🥦",
    },
    "Contexto comunitario": {
        "variables": [("Rel. vecinal","Buena+=8 · Regular=2"),("Participación","Activa=8 · A veces=4"),("Actores","Ident.=4")],
        "formula": "Suma / 2, máx 10", "fuente": "M4 · Contexto", "icono": "🤝",
    },
}

def compute_cross_module_score(data: dict) -> dict:
    scores = {}
    suelo_mo = data.get("suelo_materia_organica","")
    suelo_cp = data.get("suelo_compactacion","")
    suelo_dr = data.get("suelo_drenaje","")
    if any([suelo_mo, suelo_cp, suelo_dr]):
        pts = 0
        if suelo_mo == "Alto": pts += 8
        elif suelo_mo == "Medio": pts += 4
        if suelo_cp == "Baja": pts += 6
        elif suelo_cp == "Media": pts += 2
        if suelo_dr == "Bueno": pts += 6
        elif suelo_dr == "Moderado": pts += 2
        scores["Calidad del suelo"] = {"score": min(round(pts/2.0,1),10), "desc":"Materia orgánica, compactación y drenaje.", "fuente":"M2 · Ecología"}
    if any([data.get("agua_captacion_lluvia"), data.get("agua_grises"), data.get("agua_riego_sistema")]):
        pts = 0
        if data.get("agua_captacion_lluvia") == "Sí": pts += 8
        elif data.get("agua_captacion_lluvia") == "Parcial": pts += 4
        if data.get("agua_grises") == "Sí": pts += 6
        elif data.get("agua_grises") == "Parcialmente": pts += 2
        if data.get("agua_riego_sistema") == "Por goteo": pts += 4
        elif data.get("agua_riego_sistema") == "Automático": pts += 2
        if data.get("agua_fugas") == "No": pts += 2
        if data.get("agua_fuente") in ["Agua reciclada","Mixta"]: pts += 4
        scores["Gestión del agua"] = {"score": min(round(pts/2.4,1),10), "desc":"Captación lluvia, grises y eficiencia de riego.", "fuente":"M5 · Agua"}
    if any([data.get("ene_fuente"), data.get("ene_led")]):
        pts = 0
        if data.get("ene_fuente") == "Panel solar": pts += 10
        elif data.get("ene_fuente") == "Mixta": pts += 6
        if data.get("ene_led") == "Sí": pts += 6
        elif data.get("ene_led") == "Parcialmente": pts += 2
        if data.get("ene_solar_interes") == "Sí, pronto": pts += 4
        try:
            kwh = float(data.get("ene_kwh_dia_calc",0) or 0)
            if 0 < kwh < 5: pts += 4
            elif kwh < 10: pts += 2
        except: pass
        scores["Eficiencia energética"] = {"score": min(round(pts/2.4,1),10), "desc":"Fuente energética, LED y consumo.", "fuente":"M6 · Energía"}
    veg_tipos = data.get("veg_tipos", [])
    if isinstance(veg_tipos, list) and veg_tipos or data.get("fauna_lombrices"):
        pts = min(len(veg_tipos)*2, 12) if isinstance(veg_tipos, list) else 0
        if data.get("fauna_lombrices") == "Frecuentemente": pts += 4
        elif data.get("fauna_lombrices") == "Ocasionalmente": pts += 2
        if data.get("fauna_aves_especies"): pts += 4
        scores["Biodiversidad observada"] = {"score": min(round(pts/2.0,1),10), "desc":"Vegetación, fauna del suelo y aves.", "fuente":"M2 · Ecología"}
    if any([data.get("cultivo_m2"), data.get("cultivo_produce_hoy")]):
        pts = 0
        try:
            area_tot = float(data.get("proyecto_area",0) or data.get("proyecto_superficie",0) or 0)
            area_cult = float(data.get("cultivo_m2",0) or 0)
            if area_tot > 0 and area_cult > 0:
                pct = area_cult / area_tot * 100
                if pct >= 50: pts += 10
                elif pct >= 25: pts += 6
                elif pct > 0: pts += 2
        except: pass
        if data.get("cultivo_produce_hoy") == "Sí": pts += 6
        elif data.get("cultivo_produce_hoy") == "Algo": pts += 2
        if data.get("cultivo_frutales") == "Sí": pts += 4
        if data.get("cultivo_verticales") == "Sí": pts += 4
        scores["Potencial productivo"] = {"score": min(round(pts/2.4,1),10), "desc":"Área cultivable, producción y aprovechamiento.", "fuente":"M3 · Cultivo"}
    ctx_v = data.get("ctx_vecinos","")
    if ctx_v or data.get("ctx_participacion"):
        pts = 0
        if ctx_v in ["Buena","Muy buena","Excelente"]: pts += 8
        elif ctx_v in ["Regular","Algo tensa"]: pts += 2
        if data.get("ctx_participacion") == "Sí, activamente": pts += 8
        elif data.get("ctx_participacion") == "A veces": pts += 4
        actores = data.get("ctx_actores",[])
        if isinstance(actores, list) and len(actores) > 0: pts += 4
        scores["Contexto comunitario"] = {"score": min(round(pts/2.0,1),10), "desc":"Relaciones vecinales, participación y redes.", "fuente":"M4 · Contexto"}
    return scores

def compute_erp(data: dict) -> float:
    ds = compute_domain_scores(data)
    mfp_avg = sum(ds.values()) / 7
    cross = compute_cross_module_score(data)
    cross_vals = [v["score"] for v in cross.values()] if cross else []
    cross_avg = sum(cross_vals) / len(cross_vals) if cross_vals else 0.0
    if cross_vals:
        return min(10.0, round(mfp_avg * 0.80 + cross_avg * 0.20, 1))
    return min(10.0, round(mfp_avg, 1))

def compute_hrp(data: dict) -> float:
    ds_tot = compute_domain_scores_total(data)
    mfp_avg = sum(ds_tot.values()) / 7
    return min(10.0, round(mfp_avg, 1))

# Aliases
compute_regenerative_score = compute_erp
compute_regenerative_score_potential = compute_hrp

def score_label(score: float) -> tuple:
    if score < 2: return "Sin inicio — el camino regenerativo está por comenzar", "#9E9E9E"
    if score < 4: return "Semilla — primeras prácticas activas", "#74C69D"
    if score < 6: return "Brote — prácticas en marcha, el espacio crece", "#52B788"
    if score < 8: return "Crecimiento — prácticas consolidadas, regenera con fuerza", "#40916C"
    return "Abundancia — referente vivo de regeneración", "#1B4332"

def brecha_texto(erp: float, hrp: float) -> str:
    diff = round(hrp - erp, 1)
    if diff <= 0: return "El espacio ya ha activado todo el potencial identificado."
    pct = round(diff / max(hrp, 0.1) * 100)
    if diff < 1: return f"+{diff} pts de potencial por activar. Muy cerca de su horizonte."
    if diff < 2.5: return f"+{diff} pts por activar ({pct}%). Oportunidades concretas de avance."
    if diff < 5: return f"+{diff} pts por activar ({pct}%). Campo de acción amplio y prometedor."
    return f"+{diff} pts por activar ({pct}%). Enorme horizonte de transformación disponible."

def brecha_valor(erp: float, hrp: float) -> float:
    return round(max(0, hrp - erp), 1)

# ── Síntesis 10 dimensiones ──────────────────────────────────────────
def compute_synthesis_potentials(data: dict) -> dict:
    counts_tot = _ipr_tot_counts(data)
    def _p(mk, pi):
        v = data.get(mk)
        if v is not None:
            try: return min(10.0, float(v) * 2)
            except: pass
        return _count_to_score(counts_tot[pi]) if pi < len(counts_tot) else 0.0
    prod = _p("sint_pot_alimentaria", 0)
    if data.get("cultivo_produce_hoy") == "Sí": prod = min(10.0, prod + 1.0)
    result = {"Producción alimentaria": round(min(10.0, prod), 1)}
    bio = _p("sint_pot_biodiversidad", 0)
    veg_tipos = data.get("veg_tipos", [])
    if isinstance(veg_tipos, list) and len(veg_tipos) >= 3: bio = min(10.0, bio + 1.0)
    result["Biodiversidad urbana"] = round(min(10.0, bio), 1)
    suelo = _p("sint_pot_suelo", 0)
    if data.get("suelo_materia_organica") == "Alto": suelo = min(10.0, suelo + 2.0)
    elif data.get("suelo_materia_organica") == "Medio": suelo = min(10.0, suelo + 1.0)
    result["Regeneración del suelo"] = round(min(10.0, suelo), 1)
    agua = _p("sint_pot_agua", 2)
    if data.get("agua_captacion_lluvia") == "Sí": agua = min(10.0, agua + 2.0)
    elif data.get("agua_captacion_lluvia") == "Parcial": agua = min(10.0, agua + 1.0)
    if data.get("agua_grises") == "Sí": agua = min(10.0, agua + 1.0)
    result["Captación y gestión del agua"] = round(min(10.0, agua), 1)
    ene_pts = 0
    if data.get("ene_fuente") == "Panel solar": ene_pts += 10
    elif data.get("ene_fuente") == "Mixta": ene_pts += 6
    if data.get("ene_led") == "Sí": ene_pts += 6
    elif data.get("ene_led") == "Parcialmente": ene_pts += 2
    if data.get("ene_solar_interes") == "Sí, pronto": ene_pts += 4
    p2_score = _count_to_score(counts_tot[2]) if len(counts_tot) > 2 else 0.0
    ene_cross = min(10.0, round(ene_pts / 2.4, 1))
    ene = max(p2_score, ene_cross) if (data.get("ene_fuente") or data.get("ene_led")) else p2_score
    result["Energía y eficiencia"] = round(min(10.0, ene), 1)
    result["Educación ambiental"] = round(_p("sint_pot_educacion", 3), 1)
    com = _p("sint_pot_bienestar", 6)
    if data.get("ctx_vecinos","") in ["Buena","Muy buena","Excelente"]: com = min(10.0, com + 1.0)
    if data.get("ctx_participacion") == "Sí, activamente": com = min(10.0, com + 1.0)
    result["Bienestar comunitario"] = round(min(10.0, com), 1)
    result["Economía regenerativa"] = round(_p("sint_pot_economia", 5), 1)
    sal = _p("sint_pot_interior", 4)
    if data.get("sal_alimentacion") in ["Muy buena — dieta basada en plantas y local","Excelente — producimos parte de lo que comemos"]: sal = min(10.0, sal + 1.0)
    if data.get("sal_ejercicio") in ["Ejercicio moderado 3+ veces/semana","Actividad física diaria integrada a la vida"]: sal = min(10.0, sal + 1.0)
    result["Salud y bienestar"] = round(min(10.0, sal), 1)
    result["Entorno construido"] = round(_p("sint_pot_entorno", 1), 1)
    return result

def compute_synthesis_potentials_obs(data: dict) -> dict:
    counts_obs = _ipr_obs_counts(data)
    def _o(pi): return _count_to_score(counts_obs[pi]) if pi < len(counts_obs) else 0.0
    ene_pts = 0
    if data.get("ene_fuente") == "Panel solar": ene_pts += 10
    elif data.get("ene_fuente") == "Mixta": ene_pts += 6
    if data.get("ene_led") == "Sí": ene_pts += 6
    elif data.get("ene_led") == "Parcialmente": ene_pts += 2
    p2_obs = _o(2)
    ene_cross = min(10.0, round(ene_pts / 2.4, 1))
    ene_obs = max(p2_obs, ene_cross) if (data.get("ene_fuente") or data.get("ene_led")) else p2_obs
    sal_base = _o(4)
    sal_boost = 0.0
    if data.get("sal_alimentacion") in ["Buena — mayoritariamente alimentos frescos","Muy buena — dieta basada en plantas y local","Excelente — producimos parte de lo que comemos"]: sal_boost += 2.0
    if data.get("sal_ejercicio") in ["Ejercicio moderado 3+ veces/semana","Actividad física diaria integrada a la vida"]: sal_boost += 2.0
    if data.get("sal_alim_local") in ["Frecuentemente","Sí, priorizamos lo local"]: sal_boost += 1.0
    if data.get("sal_alim_plantas") in ["Frecuentemente","Mayoritariamente basada en plantas"]: sal_boost += 1.0
    return {
        "Producción alimentaria": round(_o(0),1), "Biodiversidad urbana": round(_o(0),1),
        "Regeneración del suelo": round(_o(0),1), "Captación y gestión del agua": round(_o(2),1),
        "Energía y eficiencia": round(min(10.0, ene_obs),1), "Educación ambiental": round(_o(3),1),
        "Bienestar comunitario": round(_o(6),1), "Economía regenerativa": round(_o(5),1),
        "Salud y bienestar": round(min(10.0, sal_base + sal_boost),1), "Entorno construido": round(_o(1),1),
    }

DIM_WHAT_MEASURES = {
    "Producción alimentaria": {"que_mide":"Capacidad de producir alimentos frescos: hortalizas, hierbas, frutales, hongos y germinados.","fuentes":"M7·P1 + M3·Cultivo","icono":"🥦"},
    "Biodiversidad urbana": {"que_mide":"Diversidad de vida: plantas nativas, polinizadores, aves, lombrices y cobertura vegetal.","fuentes":"M7·P1 + M2·Ecología","icono":"🦋"},
    "Regeneración del suelo": {"que_mide":"Salud biológica del suelo: materia orgánica, compostaje, cobertura y actividad microbiana.","fuentes":"M7·P1 + M2·Suelo","icono":"🌍"},
    "Captación y gestión del agua": {"que_mide":"Autonomía hídrica: captación de lluvia, reutilización de grises, eficiencia de riego.","fuentes":"M7·P3 + M5·Agua","icono":"💧"},
    "Energía y eficiencia": {"que_mide":"Eficiencia energética y transición renovable: paneles solares, LED, bajo consumo.","fuentes":"M7·P3 + M6·Energía","icono":"⚡"},
    "Educación ambiental": {"que_mide":"Prácticas de aprendizaje, saberes y formación en ecología y vida regenerativa.","fuentes":"M7·P4 (Educación)","icono":"📚"},
    "Bienestar comunitario": {"que_mide":"Vínculos sociales: relaciones vecinales, participación comunitaria y redes de apoyo.","fuentes":"M7·P7 + M4·Contexto","icono":"🤝"},
    "Economía regenerativa": {"que_mide":"Economía circular: autosuficiencia, trueque, mercados locales y consumo consciente.","fuentes":"M7·P6 (Finanzas)","icono":"💚"},
    "Salud y bienestar": {"que_mide":"Alimentación saludable, actividad física, plantas medicinales, contacto con naturaleza.","fuentes":"M7·P5 + Tao T.7","icono":"🧘"},
    "Entorno construido": {"que_mide":"Bioarquitectura, diseño bioclimático, techos/muros verdes y materiales naturales.","fuentes":"M7·P2 (Entorno)","icono":"🏡"},
}

# Textos interpretativos 5 niveles (idx 0-4) para escala 0-10
DIM_INTERP_DUAL = {
    "Producción alimentaria":{"erp":["Sin producción activa. El potencial está esperando.","Primera chispa de producción activa.","Ya produce algunos alimentos. Comienzo real.","Producción activa y variada.","Abundancia alimentaria real."],"hrp":["Puede comenzar con una maceta o bancal.","Las prácticas identificadas abren posibilidades.","Puede convertirse en fuente real de alimentos.","Potencial para fortalecer la producción.","Puede ser modelo de abundancia alimentaria."]},
    "Biodiversidad urbana":{"erp":["La biodiversidad está por despertar.","Primeras señales de vida.","Prácticas que apoyan la vida.","Biodiversidad activa.","Santuario de biodiversidad urbana."],"hrp":["Incorporar nativas, crear refugios.","Puede ser corredor de polinizadores.","Potencial de nodo de biodiversidad.","Refugio reconocido de biodiversidad.","Potencial extraordinario de biodiversidad."]},
    "Regeneración del suelo":{"erp":["Suelo esperando ser despertado.","Comenzando a regenerarse.","Señales de vida biológica.","Suelo biológicamente activo.","Suelo vivo y abundante."],"hrp":["Compost y cobertura pueden transformar.","Puede despertar el suelo.","Puede alcanzar actividad biológica real.","Potencial de mejora alto.","Potencial extraordinario de regeneración."]},
    "Captación y gestión del agua":{"erp":["Depende del agua de red.","Conciencia sobre el agua.","Primeros sistemas hídricos.","Buen manejo del agua.","Soberanía hídrica."],"hrp":["Un barril o reutilizar grises.","Puede capturar y reutilizar agua.","Gestión hídrica más autónoma.","Potencial hídrico alto.","Potencial hídrico extraordinario."]},
    "Energía y eficiencia":{"erp":["Sin tecnologías de eficiencia.","Primeras mejoras.","Algunas prácticas de eficiencia.","Buen nivel de eficiencia.","Referente de autonomía energética."],"hrp":["LED, desconectar, planificar solar.","Puede reducir consumo.","Eficiencia real y transición solar.","Potencial energético alto.","Referente de energía renovable."]},
    "Educación ambiental":{"erp":["Potencial educativo no activado.","Interés y apertura.","Aprendizaje activo.","Fuente de educación ambiental.","Escuela viva de permacultura."],"hrp":["Un taller o biblioteca de saberes.","Lugar de aprendizaje vivo.","Fuente de educación para el barrio.","Potencial educativo alto.","Escuela viva para la ciudad."]},
    "Bienestar comunitario":{"erp":["Lazos por tejerse.","Vínculos emergiendo.","Red comunitaria en desarrollo.","Red comunitaria activa.","Corazón comunitario."],"hrp":["Iniciativas compartidas pequeñas.","Puede fortalecer vínculos.","Punto de encuentro real.","Nodo de resiliencia barrial.","Corazón vivo de la comunidad."]},
    "Economía regenerativa":{"erp":["Inicio de transición económica.","Primeras prácticas económicas.","Economía regenerativa activa.","Prácticas consolidadas.","Referente de economía circular."],"hrp":["Compartir, producir, reducir.","Nodo de economía local.","Autosuficiencia e intercambio.","Modelo de economía alternativa.","Otra economía es posible."]},
    "Salud y bienestar":{"erp":["Dimensión de salud no activada.","Primeras prácticas activas.","Cuidado de salud integrado.","Fuente de salud y bienestar.","Santuario de bienestar integral."],"hrp":["Plantas medicinales, alimentación.","Elementos de salud reales.","Fuente de bienestar integral.","Potencial de bienestar alto.","Santuario que inspire."]},
    "Entorno construido":{"erp":["Sin elementos regenerativos.","Primeras incorporaciones.","Prácticas regenerativas activas.","Entorno activamente regenerativo.","Referente de bioarquitectura."],"hrp":["Pérgola verde, materiales naturales.","Incorporar elementos regenerativos.","Entorno en armonía con naturaleza.","Potencial de transformación alto.","Referente de bioarquitectura."]},
    "Captación de agua":{"erp":["Depende del agua de red.","Conciencia sobre el agua.","Primeros sistemas hídricos.","Buen manejo del agua.","Soberanía hídrica."],"hrp":["Barril o reutilizar grises.","Capturar y reutilizar agua.","Gestión más autónoma.","Potencial hídrico alto.","Referente hídrico."]},
    "Bienestar interior":{"erp":["Potencial interior enorme.","Primeras señales de conexión.","Bienestar interior activo.","Conexión, calma y sentido.","Santuario interior."],"hrp":["Rincón de silencio, tierra.","Profundizar conexión.","Fuente de bienestar interior.","Potencial interior alto.","Fuente profunda de conexión."]},
}

PETAL_INTERP_DUAL = {
    "Administración de la Tierra y la Naturaleza":{"erp":["No ha activado su relación con la tierra.","Primeras prácticas activas.","Cuida su relación con la tierra.","Relación activa y madura.","Modelo vivo de administración regenerativa."],"hrp":["Huerto, compostera o nativas.","Puede transformar la relación con la tierra.","Gestión integrada y productiva.","Puede consolidarse como referente.","Modelo vivo de relación regenerativa."]},
    "Entorno Construido":{"erp":["Sin elementos regenerativos.","Primeras incorporaciones.","Prácticas activas.","Activamente regenerativo.","Referente de bioarquitectura."],"hrp":["Pérgola verde o materiales naturales.","Incorporar elementos regenerativos.","Armonía con la naturaleza.","Modelo de diseño regenerativo.","Referente de bioarquitectura."]},
    "Herramientas y Tecnología":{"erp":["Sin tecnologías apropiadas.","Primeras herramientas.","Varias tecnologías apropiadas.","Autonomía real y eficiencia.","Referente de tecnología regenerativa."],"hrp":["Solar, rocket, fermentación.","Autonomía tecnológica.","Herramientas que cierran ciclos.","Autonomía energética e hídrica.","Referente de autonomía."]},
    "Educación y Cultura":{"erp":["Potencial educativo no activado.","Primeras prácticas educativas.","Aprendizaje y cultura activa.","Fuente de educación regenerativa.","Escuela viva y centro cultural."],"hrp":["Taller, semillas, saberes.","Lugar de aprendizaje vivo.","Fuente de educación y cultura.","Puede inspirar a mucha gente.","Motor cultural para la ciudad."]},
    "Salud y Bienestar Espiritual":{"erp":["Sin prácticas de salud activas.","Primeras prácticas.","Cuidado integral activo.","Fuente real de salud.","Santuario de bienestar integral."],"hrp":["Medicinales, alimentación, contemplación.","Elementos de salud reales.","Fuente de bienestar integral.","Puede transformar al grupo.","Santuario que inspire."]},
    "Finanzas y Economía":{"erp":["Sin economía regenerativa.","Primeras prácticas económicas.","Formas de economía regenerativa.","Prácticas consolidadas.","Referente de economía circular."],"hrp":["Semillas, producir, reducir.","Nodo de economía local.","Autosuficiencia e intercambio.","Modelo de economía alternativa.","Otra economía es posible."]},
    "Tenencia de la Tierra y Gobernanza Comunitaria":{"erp":["Sin gobernanza comunitaria.","Primeras prácticas.","Gobernanza activa.","Gobernanza consolidada.","Referente de gobernanza comunitaria."],"hrp":["Conectar con vecinos.","Fortalecer vínculos.","Gobernanza activa y cuidado.","Modelo de organización territorial.","Modelo de gobernanza regenerativa."]},
}

def get_interp_text(dim, score, perspective="erp"):
    if perspective == "actual": perspective = "erp"
    if perspective == "potencial": perspective = "hrp"
    idx = _score_to_level_idx(score)
    texts = DIM_INTERP_DUAL.get(dim, {}).get(perspective, [])
    if not texts: return ""
    return texts[min(idx, len(texts)-1)]

def get_petal_interp(petal_name, score, perspective="erp"):
    if perspective == "actual": perspective = "erp"
    if perspective == "potencial": perspective = "hrp"
    idx = _score_to_level_idx(score)
    texts = PETAL_INTERP_DUAL.get(petal_name, {}).get(perspective, [])
    if not texts: return ""
    return texts[min(idx, len(texts)-1)]

ERP_HRP_METODOLOGIA = """🌍 Estado Regenerativo Presente (ERP): 80% MFP observado + 20% Sub-indicadores M2-6. Fotografía del momento actual.
🌱 Horizonte Regenerativo Potencial (HRP): 100% MFP proyectado (obs+pot). Visión de lo que el espacio puede llegar a ser.
🌀 Brecha (HRP − ERP): Campo de acción donde se definen estrategias y prioridades.

Escala 0-10 · 5 niveles: 0-2 Sin inicio | 2-4 Semilla | 4-6 Brote | 6-8 Crecimiento | 8-10 Abundancia
Puntuación MFP: 0=0 | 1-2=2 | 3-5=4 | 6-9=6 | 10-14=8 | 15+=10"""
IPR_METODOLOGIA = ERP_HRP_METODOLOGIA
