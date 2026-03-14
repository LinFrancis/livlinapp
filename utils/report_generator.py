"""Excel export completo v4 — Indagación Regenerativa."""
import pandas as pd
import io, json, textwrap
from openpyxl import Workbook
from openpyxl.styles import (PatternFill, Font, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from utils.scoring import (FLOWER_DOMAINS, ETHICAL_PRINCIPLES, SCORE_SCALE,
                            compute_domain_scores, compute_regenerative_score,
                            compute_synthesis_potentials, compute_wellbeing_score)

# ── Paleta ─────────────────────────────────────────────────────────────────
G_DARK  = "1B4332"; G_MED = "2D6A4F"; G_MAIN = "40916C"
G_LIGHT = "52B788"; G_PALE = "D8F3DC"; G_ULTRA = "F0FFF4"
WHITE   = "FFFFFF"; GRAY   = "F5F5F5"; GOLD   = "FFF8DC"

def _f(hex_): return PatternFill("solid", fgColor=hex_)
def _side(s="thin"): return Side(style=s, color=G_MED)
THIN_B  = Border(left=_side(), right=_side(), top=_side(), bottom=_side())
BOT_G   = Border(bottom=_side("medium"))

def _cs(ws, row, col, value, bg=WHITE, fg=G_DARK, bold=False, size=11,
        ha="left", wrap=False, mc=None, mr=None, border=None, italic=False):
    if isinstance(value, dict):
        value = str(value.get("label", value))
    if isinstance(value, (list,)):
        value = ", ".join(str(x) for x in value if x is not None)
    if value is None: value = ""
    c = ws.cell(row=row, column=col, value=value)
    c.fill      = _f(bg)
    c.font      = Font(bold=bold, color=fg, size=size, italic=italic, name="Calibri")
    c.alignment = Alignment(horizontal=ha, vertical="center", wrap_text=wrap)
    if border: c.border = border
    if mc: ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+mc-1)
    if mr: ws.merge_cells(start_row=row, start_column=col, end_row=row+mr-1, end_column=col)
    return c

def _sec(ws, r, title, bg=G_MED, fg=WHITE, span=6):
    _cs(ws, r, 1, title, bg=bg, fg=fg, bold=True, size=12, mc=span, ha="left"); ws.row_dimensions[r].height = 24; return r+1
def _sp(ws, r, col=None, span=6):
    _cs(ws, r, 1, "", bg=G_ULTRA, mc=span); ws.row_dimensions[r].height = 8; return r+1
def _row(ws, r, label, value, label_bg=G_PALE, val_bg=WHITE):
    _cs(ws, r, 1, label, bg=label_bg, fg=G_DARK, bold=True, size=10, mc=2, wrap=True, border=THIN_B)
    val = value
    if isinstance(val, dict): val = str(val)
    if isinstance(val, list): val = ", ".join(str(x) for x in val if x is not None)
    if val is None: val = ""
    _cs(ws, r, 3, str(val)[:500], bg=val_bg, fg=G_MED, size=10, mc=4, wrap=True, border=BOT_G)
    ws.row_dimensions[r].height = 20; return r+1
def _notes(ws, r, text, span=6, h=26):
    _cs(ws, r, 1, text, bg=GOLD, fg="5C3D00", size=9, mc=span, wrap=True, italic=True, border=BOT_G)
    ws.row_dimensions[r].height = h; return r+1

def _set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w

def _safe(v):
    if isinstance(v, dict): return str(v.get("label", v))
    if isinstance(v, list): return ", ".join(str(x) for x in v if x is not None)
    if v is None: return ""
    return str(v)[:500]


def generate_excel(data: dict) -> bytes:
    wb = Workbook()

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 1 — RESUMEN EJECUTIVO
    # ════════════════════════════════════════════════════════════════════════
    ws1 = wb.active; ws1.title = "📊 Resumen Ejecutivo"
    _set_col_widths(ws1, [20,18,18,18,18,18])

    # Header
    ws1.merge_cells("A1:F1")
    ws1["A1"] = "INDAGACIÓN REGENERATIVA · LivLin v2.0  ·  www.livlin.com"
    ws1["A1"].fill = _f(G_DARK); ws1["A1"].font = Font(color=WHITE, bold=True, size=18, name="Calibri")
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 42

    r = 2
    r = _sp(ws1, r)
    r = _row(ws1, r, "Nombre del diagnóstico", data.get("proyecto_nombre",""))
    r = _row(ws1, r, "Grupo / familia", data.get("proyecto_cliente",""))
    r = _row(ws1, r, "Fecha", data.get("proyecto_fecha",""))
    r = _row(ws1, r, "Ciudad / País", f"{data.get('proyecto_ciudad','')} · {data.get('proyecto_pais','')}")
    r = _row(ws1, r, "Tipo de espacio", data.get("proyecto_tipo_espacio",""))
    r = _row(ws1, r, "Área total", f"{data.get('proyecto_area',0)} m²")
    r = _row(ws1, r, "Composición del grupo", data.get("proyecto_composicion",""))
    r = _row(ws1, r, "Adultos / Niños", f"{data.get('proyecto_n_adultos',0)} / {data.get('proyecto_n_ninos',0)}")
    r = _sp(ws1, r)

    # Scores
    domain_scores = compute_domain_scores(data)
    global_score  = compute_regenerative_score(data)
    potenciales   = compute_synthesis_potentials(data)

    r = _sec(ws1, r, "🌸 REGENERATIVE SCORE — PÉTALOS DE LA PERMACULTURA")
    for domain, score in domain_scores.items():
        meta = FLOWER_DOMAINS[domain]
        bar = "█" * int(score) + "░" * (5 - int(score))
        _cs(ws1, r, 1, f"{meta['icon']} P{meta['petal_num']} {domain}", bg=G_ULTRA, bold=True, size=10, mc=4)
        _cs(ws1, r, 5, f"{score:.1f}/5  {bar}", bg=G_PALE, fg=G_DARK, bold=True, size=10, mc=2, ha="center")
        ws1.row_dimensions[r].height = 22; r += 1

    r = _sp(ws1, r)
    _cs(ws1, r, 1, "⭐ POTENCIAL REGENERATIVO GLOBAL", bg=G_MAIN, fg=WHITE, bold=True, size=14, mc=4)
    _cs(ws1, r, 5, f"{global_score:.2f}/5.0", bg=G_MAIN, fg=WHITE, bold=True, size=16, mc=2, ha="center")
    ws1.row_dimensions[r].height = 32; r += 1
    r = _sp(ws1, r)

    r = _sec(ws1, r, "📊 POTENCIALES DEL SITIO (auto-calculados)")
    for dim, val in potenciales.items():
        _cs(ws1, r, 1, dim, bg=G_ULTRA, bold=True, size=10, mc=4)
        _cs(ws1, r, 5, f"{val:.1f}/5", bg=G_PALE, fg=G_MED, bold=True, mc=2, ha="center")
        ws1.row_dimensions[r].height = 20; r += 1
    r = _sp(ws1, r)

    # Síntesis
    r = _sec(ws1, r, "📝 SÍNTESIS NARRATIVA AUTO-GENERADA")
    for key, label in [
        ("sint_fortalezas","💪 Fortalezas"),
        ("sint_oportunidades","🚀 Oportunidades"),
        ("sint_limitaciones","⚠️ Limitaciones"),
        ("sint_quick_wins","⚡ Quick Wins"),
        ("sint_observaciones","🌿 Observaciones finales"),
    ]:
        r = _row(ws1, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 2 — MÓDULO 1 + TAO
    # ════════════════════════════════════════════════════════════════════════
    ws2 = wb.create_sheet("📋 M1 Información + Tao")
    _set_col_widths(ws2, [24,16,16,16,16,16])
    r = 1
    r = _sec(ws2, r, "MÓDULO 1 — INFORMACIÓN DEL PROYECTO")
    for key, label in [
        ("proyecto_nombre","Nombre del proyecto"),("proyecto_cliente","Grupo / familia"),
        ("proyecto_direccion","Dirección"),("proyecto_ciudad","Ciudad"),
        ("proyecto_pais","País"),("proyecto_fecha","Fecha"),
        ("proyecto_area","Área total (m²)"),("proyecto_tipo_espacio","Tipo de espacio"),
        ("proyecto_composicion","Composición del grupo"),
        ("proyecto_n_adultos","Adultos"),("proyecto_n_ninos","Niños/as"),
        ("proyecto_habitantes","Descripción del grupo"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))
    r = _sp(ws2, r)

    r = _sec(ws2, r, "🗺️ GEOLOCALIZACIÓN")
    for key, label in [
        ("geo_display","Dirección geolocalizada"),("geo_lat","Latitud"),
        ("geo_lon","Longitud"),("geo_city","Ciudad"),("geo_country","País"),
        ("agua_prec_anual","Precipitación anual (mm/año)"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))

    # Solar data
    if data.get("geo_solar"):
        try:
            import ast
            solar = ast.literal_eval(data["geo_solar"]) if isinstance(data["geo_solar"],str) else data["geo_solar"]
            r = _row(ws2, r, "Radiación solar promedio anual (kWh/m²/día)", str(solar.get("annual_avg_kwh_m2","")))
            months = solar.get("months",[])
            rad    = solar.get("monthly_kwh_m2",[])
            if months and rad:
                r = _row(ws2, r, "Radiación solar por mes", ", ".join(f"{m}:{v}" for m,v in zip(months,rad)))
        except Exception: pass

    r = _sp(ws2, r)
    r = _sec(ws2, r, "💭 INTENCIÓN DEL GRUPO")
    for key, label in [
        ("intencion_motivo","Motivación"),("intencion_cambios","Cambios deseados"),
        ("intencion_vision5","Visión a 5 años"),("intencion_intentado","Lo intentado antes"),
        ("intencion_mejor","Lo que funciona mejor"),("intencion_frustracion","Fuente de frustración"),
        ("intencion_recursos","Recursos disponibles"),("intencion_suenos","Sueños"),
        ("intencion_notas","Notas"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))
    r = _sp(ws2, r)

    r = _sec(ws2, r, "☯️ TAO DE LA REGENERACIÓN")
    for key, label in [
        ("tao_tiempo_aire","Tiempo al aire libre/día"),("tao_silencio","Práctica de silencio"),
        ("tao_conexion","Conexión con el espacio (0-5)"),("tao_contemplacion","Rincón de contemplación"),
        ("tao_sensacion","Sensación al estar aquí"),("tao_deseado","Lo deseado"),
        ("tao_no_deseado","Lo no deseado"),("tao_llama","La llama que no se apaga"),
        ("tao_ritmo","Ritmo de vida"),("tao_tiempo_libre","Tiempo libre disponible"),
        ("tao_sencillez","Tendencia a la sencillez"),("tao_consumo","Relación con el consumo"),
        ("tao_naturaleza_ext","Relación con la naturaleza"),("tao_cuerpo_tierra","Contacto con la tierra"),
        ("tao_cc_conciencia","Conciencia cambio climático"),("tao_cc_impacto","Impacto CC en el lugar"),
        ("tao_bio_conciencia","Conciencia biodiversidad"),("tao_bio_local","Cambios biodiversidad local"),
        ("tao_cont_conciencia","Conciencia contaminación"),("tao_cont_tipos","Tipos contaminación"),
        ("tao_bienestar","Bienestar interior deseado"),("tao_palabra_esencial","Palabras esenciales"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 3 — MÓDULOS 2-3
    # ════════════════════════════════════════════════════════════════════════
    ws3 = wb.create_sheet("🔬 M2-3 Ecología + Cultivo")
    _set_col_widths(ws3, [24,16,16,16,16,16])
    r = 1
    r = _sec(ws3, r, "MÓDULOS 2–3 — ECOLOGÍA + FLUJOS + CULTIVO")

    r = _sec(ws3, r, "🌍 SUELO / ESPACIO", bg=G_MED)
    for key, label in [
        ("proyecto_tipo_espacio","Tipo de espacio"),("suelo_tipo","Tipo de suelo"),
        ("suelo_compactacion","Compactación"),("suelo_materia_organica","Materia orgánica"),
        ("suelo_drenaje","Drenaje"),("suelo_color","Color del suelo"),("suelo_olor","Olor"),
        ("esp_exposicion","Orientación (si aplica)"),("esp_sol_horas","Horas de sol"),
        ("esp_viento","Exposición al viento"),("suelo_notas","Notas del suelo"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))

    r = _sec(ws3, r, "🌿 VEGETACIÓN Y FAUNA", bg=G_MED)
    for key, label in [
        ("veg_tipos","Tipos de vegetación"),("veg_especies","Especies identificadas"),
        ("veg_invasoras","Plantas invasoras"),("fauna_polinizadores","Polinizadores"),
        ("fauna_aves","Aves"),("fauna_lombrices","Lombrices"),
        ("fauna_plagas","Plagas"),("fauna_aves_especies","Especies aves"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))

    r = _sec(ws3, r, "☀️ FLUJOS NATURALES", bg=G_MED)
    for key, label in [
        ("sol_horas","Horas de sol (promedio)"),("sol_horas_invierno","Horas sol invierno"),
        ("sol_horas_verano","Horas sol verano"),("sol_orientacion","Orientación principal"),
        ("sol_zonas_max","Zonas más soleadas"),("sol_sombra_perm","Sombras permanentes"),
        ("sol_obstaculos","Obstáculos de sombra"),("viento_direccion","Dirección viento"),
        ("agua_flujo_lluvia","Flujo de lluvia"),("agua_acumulacion","Acumulación de agua"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))

    r = _sec(ws3, r, "🥦 POTENCIAL DE CULTIVO", bg=G_MED)
    for key, label in [
        ("cultivo_areas_tipo","Áreas de cultivo"),("cultivo_m2","Área cultivable total (m²)"),
        ("cultivo_produce_hoy","¿Produce hoy?"),("cultivo_sustrato_calidad","Calidad del sustrato"),
        ("cultivo_riego_acceso","Acceso al agua"),("cultivo_frutales","Potencial frutales"),
        ("cultivo_verticales","Cultivos verticales"),("cultivo_plantas_actuales","Plantas actuales"),
        ("cultivo_interes","Interés de producción"),("cultivo_notas","Notas"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))

    # Bancales
    if data.get("bancales"):
        r = _sec(ws3, r, "📐 BANCALES / ZONAS DE CULTIVO", bg=G_MED)
        _cs(ws3, r, 1, "Nombre", bg=G_PALE, bold=True); _cs(ws3, r, 2, "Área m²", bg=G_PALE, bold=True)
        _cs(ws3, r, 3, "Volumen m³", bg=G_PALE, bold=True); _cs(ws3, r, 4, "Litros", bg=G_PALE, bold=True)
        r += 1
        total_a = total_v = total_l = 0
        for b in data["bancales"]:
            _cs(ws3, r, 1, b.get("nombre","")); _cs(ws3, r, 2, b.get("area",0))
            _cs(ws3, r, 3, b.get("vol",0)); _cs(ws3, r, 4, b.get("litros",0))
            ws3.row_dimensions[r].height = 20; r += 1
            total_a += b.get("area",0); total_v += b.get("vol",0); total_l += b.get("litros",0)
        _cs(ws3, r, 1, "TOTAL", bg=G_PALE, bold=True); _cs(ws3, r, 2, round(total_a,2), bg=G_PALE, bold=True)
        _cs(ws3, r, 3, round(total_v,3), bg=G_PALE, bold=True); _cs(ws3, r, 4, total_l, bg=G_PALE, bold=True)
        r += 1

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 4 — MÓDULOS 4-6
    # ════════════════════════════════════════════════════════════════════════
    ws4 = wb.create_sheet("🏙️ M4-6 Contexto+Agua+Ene")
    _set_col_widths(ws4, [24,16,16,16,16,16])
    r = 1
    r = _sec(ws4, r, "MÓDULO 4 — CONTEXTO URBANO")
    for key, label in [
        ("ctx_distancia_parques","Parque más cercano (m)"),("ctx_cuenca","Cuenca hidrográfica"),
        ("ctx_corredores","Corredores biológicos"),("ctx_arboles_calle","Árboles en calle"),
        ("ctx_vecinos","Relación vecinal"),("ctx_participacion","Participación comunitaria"),
        ("ctx_huertas_com","Huertas comunitarias"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))

    # Parques lista
    if data.get("ctx_parques_lista"):
        r = _sec(ws4, r, "🌳 PARQUES REGISTRADOS", bg=G_MED)
        for p in data["ctx_parques_lista"]:
            r = _row(ws4, r, p.get("nombre",""), f"{p.get('dist','')} m · {p.get('uso','')}")

    # Actores
    if data.get("ctx_actores"):
        r = _sec(ws4, r, "🤝 MAPEO DE ACTORES COMUNITARIOS", bg=G_MED)
        for a in data["ctx_actores"]:
            r = _row(ws4, r, f"{a.get('tipo','')} · {a.get('nombre','')}", a.get("relacion",""))

    r = _sp(ws4, r)
    r = _sec(ws4, r, "MÓDULO 5 — AGUA")
    for key, label in [
        ("agua_fuente","Fuente de agua"),("agua_riego_sistema","Sistema de riego"),
        ("agua_captacion_lluvia","Captación lluvia"),("agua_pot_captacion","Potencial captación"),
        ("agua_grises","Reutilización aguas grises"),("agua_fugas","Fugas"),
        ("agua_consumo","Consumo estimado (m³/mes)"),
        ("agua_consumo_estimado_ldia","Consumo estimado (L/día)"),
        ("agua_techo_m2","Techo captación (m²)"),
        ("agua_prec_anual","Precipitación anual (mm)"),
        ("agua_litros_captacion_anual","Litros captación potencial/año"),
        ("agua_sequias","Vulnerabilidad a sequías"),("agua_sequias_impacto","Impacto sequías"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))

    # Fuentes de agua
    if data.get("fuentes_agua"):
        r = _sec(ws4, r, "🚿 FUENTES DE AGUA ESTIMADAS", bg=G_MED)
        for f in data["fuentes_agua"]:
            r = _row(ws4, r, f.get("nombre",""), f"{f.get('lit_dia',0)} L/día")

    r = _sp(ws4, r)
    r = _sec(ws4, r, "MÓDULO 5 — ENERGÍA")
    for key, label in [
        ("ene_fuente","Fuente energética"),("ene_consumo","Consumo declarado"),
        ("ene_kwh_dia_calc","Consumo calculado (kWh/día)"),("ene_led","Iluminación LED"),
        ("ene_solar_interes","Interés solar"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))

    if data.get("equipos_electricos"):
        r = _sec(ws4, r, "🔌 EQUIPOS ELÉCTRICOS", bg=G_MED)
        for e in data["equipos_electricos"]:
            r = _row(ws4, r, e.get("nombre",""),
                f"{e.get('watts',0)}W × {e.get('horas',0)}h × {e.get('cant',1)}u = {e.get('kwh_dia',0)} kWh/día")

    r = _sp(ws4, r)
    r = _sec(ws4, r, "MÓDULO 6 — MATERIALES Y RESIDUOS")
    for key, label in [
        ("res_compost_tipo","Sistema compostaje"),("res_compostan","¿Compostan?"),
        ("res_intentos_fallidos","Intentos fallidos de compostaje"),
        ("res_fraccion_organica","Fracción orgánica"),("res_espacio_compost","Espacio compost"),
        ("res_separan","¿Separan reciclables?"),("res_reutilizan","¿Reutilizan materiales?"),
        ("res_segunda_mano","¿Segunda mano?"),("res_materiales_huerto","Materiales reutilizables"),
        ("mat_pot_infra","Potencial infraestructura verde"),
        ("mat_infraestructura_verde","Infra verde existente"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 5 — FLOR DE LA PERMACULTURA
    # ════════════════════════════════════════════════════════════════════════
    ws5 = wb.create_sheet("🌸 M7 Flor Permacultura")
    _set_col_widths(ws5, [32, 14, 14, 8, 32])
    ws5.merge_cells("A1:E1")
    ws5["A1"] = "🌸 FLOR DE LA PERMACULTURA — OBSERVADO vs POTENCIAL  ·  LivLin v2.0"
    ws5["A1"].fill = _f(G_DARK); ws5["A1"].font = Font(color=WHITE, bold=True, size=14, name="Calibri")
    ws5["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws5.row_dimensions[1].height = 32
    r = 2

    # Legend
    _cs(ws5, r, 1, "✅ OBSERVADO = prácticas activas en el espacio", bg="E8F5E9", fg=G_DARK, bold=True, size=10, mc=2)
    _cs(ws5, r, 3, "🌟 POTENCIAL = identificado por el facilitador", bg="FFF8E1", fg="E65100", bold=True, size=10, mc=3)
    ws5.row_dimensions[r].height = 22; r += 1
    r = _sp(ws5, r, span=5)

    # Per-petal sheets
    import json as _json
    from pathlib import Path as _Path
    _jf = _Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(_jf, encoding="utf-8") as _f2:
            _petalos = _json.load(_f2)["petalos"]
    except Exception:
        _petalos = []

    icons = ["🌳","🏡","🛠️","📚","🧘","💚","🤝","🌿"]
    ipr_obs = data.get("ipr_obs", [])
    ipr_pot = data.get("ipr_pot", [])

    for i, p in enumerate(_petalos):
        icon = icons[i] if i < len(icons) else "🌱"
        n_obs = ipr_obs[i] if i < len(ipr_obs) else 0
        n_pot = ipr_pot[i] if i < len(ipr_pot) else 0
        r = _sec(ws5, r, f"{icon} {p['nombre']}", bg=G_MED, span=5)
        # Score row
        _cs(ws5, r, 1, f"✅ Observado: {n_obs} práctica(s)", bg="E8F5E9", fg=G_DARK, bold=True, mc=2)
        _cs(ws5, r, 3, f"🌟 Potencial: {n_pot} práctica(s)", bg="FFF8E1", fg="E65100", bold=True, mc=2)
        ws5.row_dimensions[r].height = 20; r += 1

        # Acciones observadas
        obs_data = data.get(f"petalo_{i}_obs", {})
        pot_data = data.get(f"petalo_{i}_pot", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_pot = data.get(f"petalo_{i}_otros_pot", [])

        for cat_key in p.get("categorias", {}):
            cat_label = cat_key.replace("_"," ").title()
            obs_sel = obs_data.get(cat_key, [])
            pot_sel = pot_data.get(cat_key, [])
            if obs_sel or pot_sel:
                _cs(ws5, r, 1, cat_label, bg=G_PALE, bold=True, size=9, mc=2)
                _cs(ws5, r, 3, "", bg=G_PALE, mc=3)
                ws5.row_dimensions[r].height = 18; r += 1
                max_len = max(len(obs_sel), len(pot_sel), 1)
                for j in range(max_len):
                    obs_v = obs_sel[j] if j < len(obs_sel) else ""
                    pot_v = pot_sel[j] if j < len(pot_sel) else ""
                    _cs(ws5, r, 1, f"  ✅ {obs_v}" if obs_v else "", bg="F1F8F1", size=9, mc=2, wrap=True)
                    _cs(ws5, r, 3, f"  🌟 {pot_v}" if pot_v else "", bg="FFFDE7", size=9, mc=3, wrap=True)
                    ws5.row_dimensions[r].height = 18; r += 1

        if otros_obs or otros_pot:
            _cs(ws5, r, 1, "Otros (observados)", bg=G_PALE, bold=True, size=9, mc=2)
            _cs(ws5, r, 3, "Otros (potencial)", bg=G_PALE, bold=True, size=9, mc=3)
            ws5.row_dimensions[r].height = 18; r += 1
            for txt in otros_obs:
                _cs(ws5, r, 1, f"  ✅ {txt}", bg="F1F8F1", size=9, mc=2, wrap=True)
                ws5.row_dimensions[r].height = 18; r += 1
            for txt in otros_pot:
                _cs(ws5, r, 3, f"  🌟 {txt}", bg="FFFDE7", size=9, mc=3, wrap=True)
                ws5.row_dimensions[r].height = 18; r += 1

        notas = data.get(f"petalo_{i}_notas","")
        if notas:
            r = _notes(ws5, r, f"📝 Notas: {notas}", span=5)

        r = _sp(ws5, r, span=5)

    # Prácticas destacadas
    dest = data.get("pot_practicas_destacadas","")
    if dest:
        r = _sec(ws5, r, "✨ Prácticas más destacadas", span=5)
        r = _notes(ws5, r, dest, span=5, h=50)

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 6 — SÍNTESIS Y PLAN
    # ════════════════════════════════════════════════════════════════════════
    ws6 = wb.create_sheet("🗺️ M9 Síntesis + Plan")
    _set_col_widths(ws6, [28, 20, 18, 14, 18])
    r = 1
    r = _sec(ws6, r, "📊 POTENCIALES DEL SITIO", span=5)
    pots = compute_synthesis_potentials(data)
    for dim, val in pots.items():
        _cs(ws6, r, 1, dim, bg=G_ULTRA, bold=True, size=10, mc=3, border=THIN_B)
        _cs(ws6, r, 4, f"{val:.1f}/5", bg=G_PALE, bold=True, ha="center", border=THIN_B)
        ws6.row_dimensions[r].height = 22; r += 1
    r = _sp(ws6, r, span=5)

    r = _sec(ws6, r, "📝 SÍNTESIS NARRATIVA", span=5)
    for key, label in [
        ("sint_fortalezas","💪 Fortalezas"),("sint_oportunidades","🚀 Oportunidades"),
        ("sint_limitaciones","⚠️ Limitaciones"),("sint_quick_wins","⚡ Quick Wins"),
        ("sint_observaciones","🌿 Observaciones finales"),
    ]:
        r = _row(ws6, r, label, _safe(data.get(key,"")))
    r = _sp(ws6, r, span=5)

    r = _sec(ws6, r, "🗓️ PLAN DE ACCIÓN", span=5)
    for plan_key, fase in [
        ("plan_inmediatas","⚡ Fase 1 — Inmediatas (0–3 meses)"),
        ("plan_estacionales","🌱 Fase 2 — Estacionales (3–12 meses)"),
        ("plan_estructurales","🌳 Fase 3 — Estructurales (1–5 años)"),
    ]:
        r = _sec(ws6, r, fase, bg=G_MED, span=5)
        if data.get(plan_key):
            _cs(ws6, r, 1, "Acción", bg=G_PALE, bold=True)
            _cs(ws6, r, 2, "Responsable", bg=G_PALE, bold=True)
            _cs(ws6, r, 3, "Costo", bg=G_PALE, bold=True)
            _cs(ws6, r, 4, "Estado", bg=G_PALE, bold=True)
            r += 1
            for acc in data[plan_key]:
                _cs(ws6, r, 1, acc.get("titulo",""), size=10, wrap=True)
                _cs(ws6, r, 2, acc.get("resp",""), size=10)
                _cs(ws6, r, 3, acc.get("costo",""), size=10)
                _cs(ws6, r, 4, acc.get("estado",""), size=10)
                ws6.row_dimensions[r].height = 22; r += 1
        else:
            r = _row(ws6, r, "Sin acciones registradas", "")
        r = _sp(ws6, r, span=5)

    # ════════════════════════════════════════════════════════════════════════
    # HOJA 7 — DATOS BIOCLIMÁTICOS
    # ════════════════════════════════════════════════════════════════════════
    ws7 = wb.create_sheet("🌡️ Datos Bioclimáticos")
    _set_col_widths(ws7, [18]*14)
    r = 1
    r = _sec(ws7, r, "🌡️ DATOS BIOCLIMÁTICOS DEL LUGAR", span=13)

    if data.get("geo_clima_anual"):
        try:
            import ast
            clima = ast.literal_eval(data["geo_clima_anual"]) if isinstance(data["geo_clima_anual"],str) else data["geo_clima_anual"]
            months = clima.get("months",[])
            # Header row
            _cs(ws7, r, 1, "Mes", bg=G_PALE, bold=True)
            for j, m in enumerate(months, 2):
                _cs(ws7, r, j, m, bg=G_PALE, bold=True, ha="center")
            ws7.row_dimensions[r].height = 20; r += 1
            for key, label in [("t_max","T° Máx (°C)"),("t_min","T° Mín (°C)"),("prec","Precipitación (mm)"),("wind","Viento (km/h)")]:
                _cs(ws7, r, 1, label, bg=G_ULTRA, bold=True, size=10)
                for j, val in enumerate(clima.get(key,[]), 2):
                    _cs(ws7, r, j, val, ha="center", size=10)
                ws7.row_dimensions[r].height = 22; r += 1
        except Exception as e:
            r = _row(ws7, r, "Error leyendo datos climáticos", str(e))

    if data.get("geo_solar"):
        r = _sp(ws7, r, span=13)
        r = _sec(ws7, r, "☀️ ENERGÍA SOLAR", span=13)
        try:
            import ast
            solar = ast.literal_eval(data["geo_solar"]) if isinstance(data["geo_solar"],str) else data["geo_solar"]
            months = solar.get("months",[])
            _cs(ws7, r, 1, "Mes", bg=G_PALE, bold=True)
            for j, m in enumerate(months, 2): _cs(ws7, r, j, m, bg=G_PALE, bold=True, ha="center")
            ws7.row_dimensions[r].height = 20; r += 1
            _cs(ws7, r, 1, "Rad. (kWh/m²/día)", bg=G_ULTRA, bold=True, size=10)
            for j, val in enumerate(solar.get("monthly_kwh_m2",[]), 2):
                _cs(ws7, r, j, val, ha="center", size=10)
            ws7.row_dimensions[r].height = 22; r += 1
            _cs(ws7, r, 1, "Panel 100W kWh/día", bg=G_ULTRA, bold=True, size=10)
            for j, val in enumerate(solar.get("panel_100w_kwh_day",[]), 2):
                _cs(ws7, r, j, val, ha="center", size=10)
            ws7.row_dimensions[r].height = 22; r += 1
            r = _row(ws7, r, "Promedio anual kWh/m²/día", str(solar.get("annual_avg_kwh_m2","")))
        except Exception as e:
            r = _row(ws7, r, "Error leyendo datos solares", str(e))

    # ════════════════════════════════════════════════════════════════════════
    # Freeze panes and final formatting
    for ws in [ws1, ws2, ws3, ws4, ws5, ws6, ws7]:
        ws.freeze_panes = "A2"
        ws.sheet_view.showGridLines = True

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()
