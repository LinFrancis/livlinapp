"""Auto-síntesis regenerativa: genera texto narrativo desde las respuestas del diagnóstico."""

from utils.scoring import compute_domain_scores, compute_synthesis_potentials


def _v(data, key, default=None):
    return data.get(key, default)


def _has(data, key, pos_vals=None):
    v = data.get(key)
    if v is None:
        return False
    if pos_vals:
        return v in pos_vals
    return bool(v)


def _score_val(data, key):
    v = data.get(key)
    return float(v) if isinstance(v, (int, float)) else 0


def generate_fortalezas(data: dict) -> str:
    """Genera texto de fortalezas basado en respuestas positivas."""
    items = []

    # Energías y flujos
    if _score_val(data, "sol_horas") >= 6:
        items.append(f"✅ Excelente exposición solar: {_v(data,'sol_horas',0)} horas de sol directo")
    elif _score_val(data, "sol_horas") >= 4:
        items.append(f"☀️ Buena exposición solar ({_v(data,'sol_horas',0)} h/día)")

    # Agua
    if _has(data, "agua_captacion_lluvia", ["Parcial", "Sí"]):
        items.append("💧 Ya existe captación de agua lluvia")
    if _has(data, "agua_grises", ["Parcialmente", "Sí"]):
        items.append("♻️ Reutilización de aguas grises activa")

    # Suelo y biodiversidad
    if _has(data, "suelo_materia_organica", ["Alto"]):
        items.append("🌍 Suelo con alta materia orgánica — excelente punto de partida")
    if _has(data, "fauna_polinizadores", ["Frecuentemente"]):
        items.append("🐝 Presencia frecuente de polinizadores — biodiversidad activa")
    if _has(data, "fauna_aves", ["Frecuentemente"]):
        items.append("🦅 Aves presentes frecuentemente — indicador de salud ecológica")
    if _has(data, "fauna_lombrices", ["Abundantes"]):
        items.append("🪱 Lombrices abundantes — suelo biológicamente activo")

    # Compostaje
    if _has(data, "res_compostan", ["Sí"]):
        items.append("🌱 Compostaje activo — cierre de ciclos orgánicos en marcha")

    # Reciclaje
    if _has(data, "res_separan", ["Siempre"]):
        items.append("♻️ Separación de reciclables sistemática")

    # Cultivo
    if _has(data, "cultivo_produce_hoy", ["Sí"]):
        items.append("🥦 Producción de alimentos ya en curso")
    if _score_val(data, "cultivo_m2") >= 5:
        items.append(f"🌿 {_v(data,'cultivo_m2',0)} m² disponibles para cultivo")

    # Energía
    if _has(data, "ene_led", ["Sí"]):
        items.append("💡 Iluminación 100% LED — eficiencia energética base asegurada")

    # Entorno
    if _score_val(data, "ctx_distancia_parques") > 0 and _score_val(data, "ctx_distancia_parques") < 300:
        items.append(f"🌳 Parque/área verde a menos de 300m del espacio")

    # Comunidad
    if _has(data, "ctx_vecinos", ["Buena", "Excelente"]):
        items.append("🤝 Buenas relaciones vecinales — red de apoyo disponible")

    # Flower scores
    domain_scores = compute_domain_scores(data)
    for domain, score in domain_scores.items():
        if score >= 4:
            items.append(f"🌸 Pétalo '{domain}': puntaje {score}/5 — muy desarrollado")

    # Tao
    if _has(data, "tao_conexion") and _score_val(data, "tao_conexion") >= 4:
        items.append("💚 Alta conexión emocional del grupo con el espacio")

    if not items:
        return "Completa más módulos del diagnóstico para generar fortalezas automáticas."
    return "\n".join(items)


def generate_oportunidades(data: dict) -> str:
    """Genera oportunidades donde hay potencial no aprovechado."""
    items = []

    if _has(data, "agua_pot_captacion", ["Medio", "Alto"]) and not _has(data, "agua_captacion_lluvia", ["Sí"]):
        items.append("💧 Alto potencial para instalar sistema de captación de lluvia")

    if _has(data, "cultivo_frutales", ["Posiblemente", "Sí"]) and not _has(data, "cultivo_produce_hoy", ["Sí"]):
        items.append("🍎 Espacio para árboles frutales — integrar estratos arbóreos")

    if _has(data, "cultivo_verticales", ["Posiblemente", "Sí"]):
        items.append("🧱 Potencial de cultivo vertical sin explotar — muros y rejas aprovechables")

    if not _has(data, "res_compostan", ["Sí"]) and _has(data, "res_espacio_compost", ["Poco", "Sí"]):
        items.append("🌱 Espacio disponible para compostaje — alta oportunidad de cierre de ciclos")

    if _has(data, "ene_solar_interes", ["Mediano plazo", "Sí, pronto"]):
        items.append("⚡ Interés en energía solar — analizar potencial fotovoltaico del lugar")

    if _has(data, "mat_pot_infra", ["Medio", "Alto"]):
        items.append("🌿 Potencial para infraestructura verde (muros, pérgolas, techos vivos)")

    if _has(data, "ctx_huertas_com", ["Sí"]):
        items.append("🤝 Huertas comunitarias cercanas — conectar y colaborar")

    if _score_val(data, "cultivo_m2") < 2 and _has(data, "proyecto_tipo_espacio", ["Casa", "Patio trasero"]):
        items.append("🏡 Casa con patio — potencial de cultivo subutilizado")

    # Flora/Fauna
    if not _has(data, "veg_tipos") or len(data.get("veg_tipos", [])) < 3:
        items.append("🌿 Baja diversidad vegetal — oportunidad de aumentar biodiversidad")

    if not _has(data, "fauna_polinizadores", ["Ocasionalmente", "Frecuentemente"]):
        items.append("🐝 Sin polinizadores visibles — instalar plantas nectaríferas")

    # Comunidad
    if _has(data, "ctx_vecinos", ["Ninguna", "Escasa"]):
        items.append("🏘️ Baja vinculación vecinal — construcción de red comunitaria es una gran oportunidad")

    if not items:
        return "Completa más módulos del diagnóstico para generar oportunidades automáticas."
    return "\n".join(items)


def generate_limitaciones(data: dict) -> str:
    """Genera limitaciones o desafíos a partir de respuestas de bajo nivel."""
    items = []

    if _has(data, "suelo_compactacion", ["Alta"]):
        items.append("⚠️ Suelo muy compactado — requiere descompactación antes de cultivar")

    if _has(data, "suelo_materia_organica", ["Bajo"]):
        items.append("⚠️ Baja materia orgánica en el suelo — necesita incorporación urgente")

    if _has(data, "agua_fugas", ["Sí"]):
        items.append("🔧 Fugas de agua visibles — pérdida de recurso hídrico a corregir")

    if _score_val(data, "sol_horas") < 3 and _score_val(data, "sol_horas") > 0:
        items.append(f"🌥️ Baja exposición solar ({_v(data,'sol_horas',0)} h/día) — limitante para cultivos")

    if _has(data, "agua_riego_sistema", ["No existe"]) and _has(data, "cultivo_produce_hoy", ["Sí", "En proceso"]):
        items.append("💧 Sin sistema de riego en espacio productivo — riesgo para los cultivos")

    if _has(data, "res_compost_tipo", ["Ninguno"]) and _has(data, "proyecto_area") and _score_val(data, "proyecto_area") > 10:
        items.append("🗑️ Sin compostaje en espacio grande — ciclos de materia orgánica abiertos")

    if _has(data, "ctx_densidad", ["Alto"]):
        items.append("🏙️ Alta densidad urbana — limitaciones de espacio, luz y suelo")

    if _has(data, "ene_fuente", ["Red eléctrica"]) and not _has(data, "ene_solar_interes", ["Sí, pronto"]):
        items.append("⚡ Dependencia total de red eléctrica sin planes de transición energética")

    if _has(data, "tao_ritmo", ["Muy acelerado", "Acelerado"]):
        items.append("⏱️ Ritmo de vida acelerado del grupo — puede dificultar el cuidado continuo del espacio")

    if _has(data, "tao_tiempo_libre", ["Muy poco"]):
        items.append("⏳ Poco tiempo libre disponible — requiere diseño de bajo mantenimiento")

    if not items:
        return "Completa más módulos del diagnóstico para identificar limitaciones automáticamente."
    return "\n".join(items)


def generate_quick_wins(data: dict) -> str:
    """Genera intervenciones de alto impacto y bajo costo basadas en el contexto."""
    items = []

    if not _has(data, "res_compostan", ["Sí", "Parcialmente"]):
        items.append("⚡ Instalar un compostero básico — bajo costo, alto impacto en suelo y residuos")

    if not _has(data, "ene_led", ["Sí"]):
        items.append("💡 Cambiar toda la iluminación a LED — amortización en menos de 6 meses")

    if _has(data, "agua_pot_captacion", ["Medio", "Alto"]):
        items.append("💧 Instalar primera cisterna o barril para captar agua de lluvia")

    if not _has(data, "res_separan", ["Siempre"]):
        items.append("♻️ Implementar sistema de separación de residuos en el hogar")

    if _score_val(data, "cultivo_m2") < 2:
        items.append("🌱 Crear primer bancal elevado o maceta productiva en zona más soleada")

    if not _has(data, "fauna_polinizadores", ["Frecuentemente"]):
        items.append("🌸 Plantar 3–5 especies nectaríferas nativas para atraer polinizadores")

    if _has(data, "suelo_compactacion", ["Alta"]):
        items.append("⛏️ Airear el suelo con horqueta y aplicar compost maduro — primer paso de regeneración")

    if _has(data, "mat_pot_infra", ["Alto"]) and not _has(data, "mat_infraestructura_verde", ["Sí"]):
        items.append("🌿 Instalar primer muro verde o estructura trepadora — impacto visual inmediato")

    if _has(data, "ctx_huertas_com", ["Sí"]) and not _has(data, "ctx_participacion", ["Regularmente"]):
        items.append("🤝 Visitar la huerta comunitaria más cercana y conectar con la red local")

    if not items:
        items.append("🌱 Comenzar con observación sistemática del espacio durante 4 semanas antes de intervenir")
        items.append("📓 Llevar un diario del espacio: sol, viento, agua, biodiversidad observada")

    return "\n".join(items[:6])  # máx 6 quick wins


def generate_all(data: dict) -> dict:
    return {
        "sint_fortalezas":    generate_fortalezas(data),
        "sint_oportunidades": generate_oportunidades(data),
        "sint_limitaciones":  generate_limitaciones(data),
        "sint_quick_wins":    generate_quick_wins(data),
    }
