"""Excel export completo v2.1 — Indagación Regenerativa LivLin.
Hoja 0: Presentación + índice
Hoja 1: Resumen ejecutivo + IPR
Hoja 2: M1 Información + Tao
Hoja 3: M2-3 Ecología + Cultivo
Hoja 4: M4-6 Sistemas
Hoja 5: M7 Flor Permacultura (Observado + Potencial)
Hoja 6: M9 Síntesis + Plan
Hoja 7: Datos Bioclimáticos
"""
import pandas as pd
import io, json
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink
from utils.scoring import (FLOWER_DOMAINS, SCORE_SCALE,
                            compute_domain_scores, compute_regenerative_score,
                            compute_synthesis_potentials)

# ── Paleta ────────────────────────────────────────────────────────────────────
G_DARK="1B4332"; G_MED="2D6A4F"; G_MAIN="40916C"
G_LIGHT="52B788"; G_PALE="D8F3DC"; G_ULTRA="F0FFF4"
WHITE="FFFFFF"; GRAY="F5F5F5"; GOLD="FFF8DC"
AMBER="FFF3E0"; AMBER_D="E65100"; TEAL="E0F2F1"

def _f(h): return PatternFill("solid", fgColor=h)
def _s(s="thin"): return Side(style=s, color=G_MED)
THIN_B = Border(left=_s(), right=_s(), top=_s(), bottom=_s())
BOT_G  = Border(bottom=_s("medium"))
PETAL_ICONS = ["🌳","🏡","🛠️","📚","🧘","💚","🤝","🌿"]

def _cs(ws, row, col, value, bg=WHITE, fg=G_DARK, bold=False, size=10,
        ha="left", wrap=False, mc=None, mr=None, border=None, italic=False):
    if isinstance(value, dict): value = str(value.get("label", value))
    if isinstance(value, list): value = "; ".join(str(x) for x in value if x is not None)
    if value is None: value = ""
    c = ws.cell(row=row, column=col, value=str(value)[:500] if value else "")
    c.fill = _f(bg); c.font = Font(bold=bold, color=fg, size=size, italic=italic, name="Calibri")
    c.alignment = Alignment(horizontal=ha, vertical="center", wrap_text=wrap)
    if border: c.border = border
    if mc: ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+mc-1)
    if mr: ws.merge_cells(start_row=row, start_column=col, end_row=row+mr-1, end_column=col)
    return c

def _sec(ws, r, title, bg=G_MED, fg=WHITE, span=6):
    _cs(ws, r, 1, title, bg=bg, fg=fg, bold=True, size=11, mc=span)
    ws.row_dimensions[r].height = 22; return r+1

def _sp(ws, r, span=6):
    _cs(ws, r, 1, "", bg=G_ULTRA, mc=span); ws.row_dimensions[r].height = 6; return r+1

def _row(ws, r, label, value, lbg=G_PALE, vbg=WHITE):
    v = value
    if isinstance(v, (dict, list)): v = str(v)
    if v is None: v = ""
    _cs(ws, r, 1, label, bg=lbg, bold=True, size=9, mc=2, wrap=True, border=THIN_B)
    _cs(ws, r, 3, str(v)[:400], bg=vbg, fg=G_MED, size=9, mc=4, wrap=True, border=BOT_G)
    ws.row_dimensions[r].height = 20; return r+1

def _note(ws, r, text, span=6, h=26):
    _cs(ws, r, 1, text, bg=GOLD, fg="5C3D00", size=9, mc=span, wrap=True, italic=True, border=BOT_G)
    ws.row_dimensions[r].height = h; return r+1

def _wcol(ws, widths):
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w

def _safe(v):
    if isinstance(v, dict): return str(v.get("label", v))
    if isinstance(v, list): return "; ".join(str(x) for x in v if x is not None)
    return "" if v is None else str(v)

def _score_level(n):
    if n==0: return "○ Sin inicio"
    if n==1: return "🌱 Iniciando"
    if n==2: return "🌿 Avanzando"
    if n==3: return "🌳 Consolidado"
    if n<=5: return "🌸 Destacado"
    return "✨ Referente"

def generate_excel(data: dict) -> bytes:
    wb = Workbook()

    # ════════════════════════════════════════════════════════════════════
    # HOJA 0 — PRESENTACIÓN / PORTADA
    # ════════════════════════════════════════════════════════════════════
    ws0 = wb.active; ws0.title = "🌿 Presentación"
    _wcol(ws0, [28, 20, 20, 18, 18, 14])

    # Header
    ws0.merge_cells("A1:F1")
    ws0["A1"] = "🌿 LivLin · Indagación Regenerativa v2.1"
    ws0["A1"].fill = _f(G_DARK); ws0["A1"].font = Font(color=WHITE, bold=True, size=20, name="Calibri")
    ws0["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws0.row_dimensions[1].height = 50

    ws0.merge_cells("A2:F2")
    ws0["A2"] = "Diagnóstico de Permacultura Urbana · www.livlin.com"
    ws0["A2"].fill = _f(G_MED); ws0["A2"].font = Font(color=WHITE, size=12, italic=True, name="Calibri")
    ws0["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws0.row_dimensions[2].height = 28

    r = 3
    r = _sp(ws0, r, span=6)

    # Project info
    r = _sec(ws0, r, "📋 Información del Diagnóstico", span=6)
    for label, key in [
        ("Espacio", "proyecto_nombre"), ("Contacto", "proyecto_cliente"),
        ("Ciudad", "proyecto_ciudad"), ("Fecha de visita", "proyecto_fecha"),
        ("Tipo de espacio", "proyecto_tipo_espacio"),
    ]:
        r = _row(ws0, r, label, data.get(key,""))
    r = _sp(ws0, r, span=6)

    # About LivLin
    r = _sec(ws0, r, "🌱 ¿Qué es LivLin?", span=6)
    livlin_text = (
        "LivLin es una plataforma de diagnóstico y acompañamiento para la transformación regenerativa "
        "de espacios urbanos. Usamos la metodología de la Flor de la Permacultura (Holmgren, 2002) "
        "y el diseño sistémico para identificar el potencial regenerativo de cada espacio y comunidad. "
        "Trabajamos con facilitadores capacitados que realizan visitas diagnósticas y generan "
        "informes personalizados con planes de acción concretos."
    )
    _cs(ws0, r, 1, livlin_text, bg=G_ULTRA, fg=G_DARK, size=10, mc=6, wrap=True, italic=True)
    ws0.row_dimensions[r].height = 65; r += 1
    r = _sp(ws0, r, span=6)

    # IPR explanation
    r = _sec(ws0, r, "📊 ¿Qué es el Índice de Potencial Regenerativo (IPR)?", span=6)
    ipr_text = (
        "El IPR mide la diversidad y profundidad de prácticas regenerativas en un espacio, "
        "organizadas en los 8 pétalos de la Flor de la Permacultura. "
        "No es un puntaje punitivo: cualquier práctica activa es un logro. "
        "El IPR distingue entre lo OBSERVADO (prácticas que ya existen) y el POTENCIAL ADICIONAL "
        "(nuevas prácticas viables identificadas por el facilitador tras la visita)."
    )
    _cs(ws0, r, 1, ipr_text, bg=AMBER, fg="3E2723", size=10, mc=6, wrap=True)
    ws0.row_dimensions[r].height = 60; r += 1
    r += 1

    # IPR scale table
    _cs(ws0, r, 1, "Nivel IPR", bg=G_MED, fg=WHITE, bold=True, size=10, border=THIN_B)
    _cs(ws0, r, 2, "N° prácticas", bg=G_MED, fg=WHITE, bold=True, size=10, ha="center", border=THIN_B)
    _cs(ws0, r, 3, "Significado", bg=G_MED, fg=WHITE, bold=True, size=10, mc=4, border=THIN_B)
    ws0.row_dimensions[r].height = 20; r += 1
    for level, n_range, meaning in [
        ("○ Sin inicio",   "0",   "Área por explorar — gran potencial latente"),
        ("🌱 Iniciando",   "1",   "El primer paso ya está dado — ¡fundamental!"),
        ("🌿 Avanzando",   "2",   "Dos prácticas muestran intención sostenida"),
        ("🌳 Consolidado", "3",   "Sistema estable, genera rendimientos constantes"),
        ("🌸 Destacado",   "4–5", "Alta integración, inspira a otros en la comunidad"),
        ("✨ Referente",   "6+",  "Sistema autónomo, comparte excedentes con la comunidad"),
    ]:
        bg = G_PALE if r % 2 == 0 else G_ULTRA
        _cs(ws0, r, 1, level, bg=bg, bold=True, size=9, border=THIN_B)
        _cs(ws0, r, 2, n_range, bg=bg, size=9, ha="center", border=THIN_B)
        _cs(ws0, r, 3, meaning, bg=bg, size=9, mc=4, wrap=True, border=THIN_B)
        ws0.row_dimensions[r].height = 18; r += 1
    r = _sp(ws0, r, span=6)

    # Module index
    r = _sec(ws0, r, "📑 Índice de módulos en este documento", span=6)
    for sheet_name, desc in [
        ("📊 Resumen Ejecutivo",        "Síntesis del IPR global, puntajes por pétalo y datos del espacio"),
        ("📋 M1 Información + Tao",     "Datos del proyecto, intención, sueño regenerativo y contexto comunitario"),
        ("🔬 M2-3 Ecología + Cultivo",  "Observación ecológica del sitio: suelo, vegetación, fauna, flujos naturales y cultivo"),
        ("🏙️ M4-6 Sistemas",            "Contexto urbano, sistema de agua, energía y materiales/residuos"),
        ("🌸 M7 Flor Permacultura",     "Prácticas observadas y potencial adicional por los 8 pétalos de la permacultura (IPR)"),
        ("🗺️ M9 Síntesis + Plan",        "Fortalezas, oportunidades, limitaciones y plan de acción en 3 horizontes temporales"),
        ("🌡️ Datos Bioclimáticos",       "Clima anual, temperatura, precipitación, radiación solar y patrones estacionales"),
    ]:
        _cs(ws0, r, 1, sheet_name, bg=G_PALE, bold=True, size=9, mc=2, border=THIN_B)
        _cs(ws0, r, 3, desc, bg=G_ULTRA, size=9, mc=4, wrap=True, border=BOT_G)
        ws0.row_dimensions[r].height = 20; r += 1
    r = _sp(ws0, r, span=6)

    # References
    r = _sec(ws0, r, "📚 Referencias y recursos clave", span=6)
    refs = [
        ("Holmgren, D. (2002)", "Permacultura: Principios y senderos. Holmgren Design Services", "https://holmgren.com.au"),
        ("Mollison, B. (1988)", "Permaculture: A Designers' Manual. Tagari Publications", "https://www.permaculturenews.org"),
        ("Ostrom, E. (1990)",   "Governing the Commons. Cambridge University Press", "https://wtf.tw/ref/ostrom_1990.pdf"),
        ("Raworth, K. (2017)",  "Doughnut Economics. Chelsea Green Publishing", "https://doughnuteconomics.org"),
        ("IPES-Food (2017)",    "Too big to feed: Exploring the impacts of mega-mergers", "https://www.ipes-food.org"),
        ("LivLin",              "Plataforma de diagnóstico regenerativo urbano", "https://www.livlin.com"),
    ]
    for author, title, url in refs:
        _cs(ws0, r, 1, author, bg=G_PALE, bold=True, size=8, border=THIN_B)
        _cs(ws0, r, 2, title,  bg=G_ULTRA, size=8, mc=3, wrap=True, border=BOT_G)
        c_url = ws0.cell(row=r, column=5, value=url)
        c_url.fill = _f(G_ULTRA); c_url.font = Font(color="1565C0", size=8, underline="single", name="Calibri")
        c_url.hyperlink = url
        ws0.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
        ws0.row_dimensions[r].height = 18; r += 1

    # ════════════════════════════════════════════════════════════════════
    # HOJA 1 — RESUMEN EJECUTIVO
    # ════════════════════════════════════════════════════════════════════
    ws1 = wb.create_sheet("📊 Resumen Ejecutivo")
    _wcol(ws1, [22, 16, 16, 14, 14, 16])

    ws1.merge_cells("A1:F1")
    ws1["A1"] = "📊 RESUMEN EJECUTIVO — INDAGACIÓN REGENERATIVA  ·  LivLin v2.1  ·  www.livlin.com"
    ws1["A1"].fill = _f(G_DARK); ws1["A1"].font = Font(color=WHITE, bold=True, size=14, name="Calibri")
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 38

    r = 2
    r = _sp(ws1, r)
    for label, key in [
        ("Espacio / Proyecto", "proyecto_nombre"), ("Contacto", "proyecto_cliente"),
        ("Fecha", "proyecto_fecha"), ("Ciudad", "proyecto_ciudad"),
    ]:
        r = _row(ws1, r, label, data.get(key,""))
    r = _sp(ws1, r)

    # IPR summary
    r = _sec(ws1, r, "🌸 ÍNDICE DE POTENCIAL REGENERATIVO (IPR) — POR PÉTALO")
    _cs(ws1, r, 1, "Pétalo", bg=G_PALE, bold=True, size=9, mc=3, border=THIN_B)
    _cs(ws1, r, 4, "✅ Observado", bg="E8F5E9", bold=True, size=9, ha="center", border=THIN_B)
    _cs(ws1, r, 5, "🌟 + Potencial", bg=AMBER, bold=True, size=9, ha="center", border=THIN_B)
    _cs(ws1, r, 6, "Nivel", bg=G_PALE, bold=True, size=9, ha="center", border=THIN_B)
    ws1.row_dimensions[r].height = 20; r += 1

    ipr_obs = data.get("ipr_obs", [])
    ipr_new = data.get("ipr_new", [])
    ipr_names = data.get("ipr_petalos", [])

    _jf = Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(_jf, encoding="utf-8") as _ff:
            _petalos_list = json.load(_ff)["petalos"]
    except Exception:
        _petalos_list = []

    for i, p in enumerate(_petalos_list):
        icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
        n_o  = ipr_obs[i] if i < len(ipr_obs) else 0
        n_n  = ipr_new[i] if i < len(ipr_new) else 0
        n_t  = n_o + n_n
        lev  = _score_level(n_t)
        bg   = G_PALE if i % 2 == 0 else G_ULTRA
        _cs(ws1, r, 1, f"{icon} {p['nombre']}", bg=bg, bold=True, size=9, mc=3, border=THIN_B)
        _cs(ws1, r, 4, str(n_o), bg="F1F8F1", size=10, ha="center", border=THIN_B)
        _cs(ws1, r, 5, f"+{n_n}", bg="FFFDE7", fg=AMBER_D, size=10, ha="center", border=THIN_B)
        _cs(ws1, r, 6, lev, bg=bg, size=9, ha="center", border=THIN_B)
        ws1.row_dimensions[r].height = 22; r += 1

    r = _sp(ws1, r)
    dest = data.get("pot_practicas_destacadas","")
    if dest:
        r = _sec(ws1, r, "✨ PRÁCTICAS MÁS DESTACADAS")
        r = _note(ws1, r, dest, h=50)
    r = _sp(ws1, r)
    r = _note(ws1, r,
        "📚 IPR basado en: Holmgren, D. (2002). Permacultura: Principios y senderos. "
        "Holmgren Design Services. · Mollison, B. (1988). Permaculture: A Designers' Manual. · "
        "Más info: www.livlin.com", h=35)

    # ════════════════════════════════════════════════════════════════════
    # HOJA 2 — M1 INFORMACIÓN + TAO
    # ════════════════════════════════════════════════════════════════════
    ws2 = wb.create_sheet("📋 M1 Información + Tao")
    _wcol(ws2, [24, 16, 22, 16, 12, 12])
    r = 1
    r = _sec(ws2, r, "📋 MÓDULO 1 — INFORMACIÓN DEL PROYECTO + TAO DE LA REGENERACIÓN")
    r = _sp(ws2, r)
    r = _sec(ws2, r, "🏡 Datos del Espacio", bg=G_LIGHT)
    for label, key in [
        ("Nombre del espacio", "proyecto_nombre"), ("Contacto / Grupo", "proyecto_cliente"),
        ("Ciudad / País", "proyecto_ciudad"), ("Dirección / Barrio", "proyecto_direccion"),
        ("Tipo de espacio", "proyecto_tipo_espacio"), ("Superficie (m²)", "proyecto_superficie"),
        ("N° Habitantes", "proyecto_habitantes"), ("Descripción del barrio", "proyecto_barrio_desc"),
        ("Intención del proyecto", "proyecto_intencion"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))
    r = _sp(ws2, r)
    r = _sec(ws2, r, "🌀 Tao de la Regeneración — Motivación", bg=G_LIGHT)
    for label, key in [
        ("Motivación principal", "tao_motivacion"), ("Sueño regenerativo", "tao_sueno"),
        ("Relación con la naturaleza", "tao_naturaleza"), ("Desafíos percibidos", "tao_desafios"),
        ("Cambio climático — percepción", "tao_cc"), ("Biodiversidad — percepción", "tao_bio"),
        ("Contaminación — percepción", "tao_contam"),
    ]:
        r = _row(ws2, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════
    # HOJA 3 — M2-3 ECOLOGÍA
    # ════════════════════════════════════════════════════════════════════
    ws3 = wb.create_sheet("🔬 M2-3 Ecología + Cultivo")
    _wcol(ws3, [24, 16, 22, 14, 14, 12])
    r = 1
    r = _sec(ws3, r, "🌍 MÓDULO 2-3 — OBSERVACIÓN ECOLÓGICA DEL SITIO")
    r = _sp(ws3, r)
    r = _sec(ws3, r, "🪱 Suelo", bg=G_LIGHT)
    for label, key in [
        ("Tipo de suelo","suelo_tipo"),("Compactación","suelo_compactacion"),
        ("Materia orgánica","suelo_materia_organica"),("Drenaje","suelo_drenaje"),
        ("Color","suelo_color"),("Olor","suelo_olor"),("Notas","suelo_notas"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))
    r = _sp(ws3, r)
    r = _sec(ws3, r, "🌿 Vegetación", bg=G_LIGHT)
    r = _row(ws3, r, "Tipos presentes", _safe(data.get("veg_tipos",[])))
    r = _row(ws3, r, "Especies identificadas", _safe(data.get("veg_especies","")))
    r = _row(ws3, r, "Invasoras / problemáticas", _safe(data.get("veg_invasoras","")))
    r = _sp(ws3, r)
    r = _sec(ws3, r, "☀️ Flujos Naturales — Sol, Viento, Agua", bg=G_LIGHT)
    for label, key in [
        ("Horas de sol / día","sol_horas"),("Orientación","sol_orientacion"),
        ("Viento dirección","viento_direccion"),("Agua lluvia (mm/año)","agua_prec_anual"),
        ("Temp. más cálida","clima_mes_caluroso"),("Temp. más fría","clima_mes_frio"),
        ("T° máx registrada","clima_t_max_abs"),("T° mín registrada","clima_t_min_abs"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))
    r = _sp(ws3, r)
    r = _sec(ws3, r, "🥦 Potencial de Cultivo", bg=G_LIGHT)
    for label, key in [
        ("Área cultivable (m²)","cultivo_m2"),("Acceso al agua","cultivo_riego_acceso"),
        ("Produce alimentos hoy","cultivo_produce_hoy"),("Espacio para frutales","cultivo_frutales"),
    ]:
        r = _row(ws3, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════
    # HOJA 4 — M4-6 SISTEMAS
    # ════════════════════════════════════════════════════════════════════
    ws4 = wb.create_sheet("🏙️ M4-6 Sistemas")
    _wcol(ws4, [24, 16, 22, 14, 14, 12])
    r = 1
    r = _sec(ws4, r, "🏙️ MÓDULO 4-6 — SISTEMAS: AGUA, ENERGÍA Y MATERIALES")
    r = _sp(ws4, r)
    r = _sec(ws4, r, "💧 Sistema de Agua", bg=G_LIGHT)
    for label, key in [
        ("Consumo diario (L)","agua_consumo"),("Precipitación anual (mm)","agua_prec_anual"),
        ("Área de techo captación (m²)","agua_techo_m2"),("Tipo de riego","agua_riego_tipo"),
        ("Gestión aguas grises","agua_grises"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))
    r = _sp(ws4, r)
    r = _sec(ws4, r, "⚡ Sistema de Energía", bg=G_LIGHT)
    for label, key in [
        ("Consumo mensual (kWh)","ene_kwh_mes"),("Fuente principal","ene_fuente_principal"),
        ("Interés en solar","ene_solar_interes"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))
    r = _sp(ws4, r)
    r = _sec(ws4, r, "♻️ Materiales y Residuos", bg=G_LIGHT)
    for label, key in [
        ("Gestión residuos orgánicos","mat_residuos_organicos"),("Compostaje","mat_compost"),
        ("Reciclaje","mat_reciclaje"),("Reducción plástico","mat_plastico_uso"),
    ]:
        r = _row(ws4, r, label, _safe(data.get(key,"")))

    # ════════════════════════════════════════════════════════════════════
    # HOJA 5 — M7 FLOR PERMACULTURA
    # ════════════════════════════════════════════════════════════════════
    ws5 = wb.create_sheet("🌸 M7 Flor Permacultura")
    _wcol(ws5, [30, 18, 18, 8, 28])

    ws5.merge_cells("A1:E1")
    ws5["A1"] = "🌸 FLOR DE LA PERMACULTURA — ÍNDICE DE POTENCIAL REGENERATIVO (IPR)  ·  LivLin v2.1"
    ws5["A1"].fill = _f(G_DARK); ws5["A1"].font = Font(color=WHITE, bold=True, size=13, name="Calibri")
    ws5["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws5.row_dimensions[1].height = 32

    r = 2
    # IPR explanation in sheet
    _cs(ws5, r, 1,
        "El IPR mide la diversidad de prácticas regenerativas activas. "
        "OBSERVADO = ya existe hoy. POTENCIAL = nuevas prácticas viables identificadas por el facilitador "
        "(no requiere re-ingresar lo observado). Scoring: 0=Sin inicio · 1=🌱Iniciando · 2=🌿Avanzando · "
        "3=🌳Consolidado · 4-5=🌸Destacado · 6+=✨Referente. "
        "Referencia: Holmgren, D. (2002). Permacultura: Principios y senderos. www.livlin.com",
        bg=AMBER, fg="3E2723", size=9, mc=5, wrap=True, italic=True)
    ws5.row_dimensions[r].height = 55; r += 1
    r = _sp(ws5, r, span=5)

    for i, p in enumerate(_petalos_list):
        icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
        n_o  = ipr_obs[i] if i < len(ipr_obs) else 0
        n_n  = ipr_new[i] if i < len(ipr_new) else 0
        n_t  = n_o + n_n
        r = _sec(ws5, r, f"{icon} {p['nombre']}  ·  IPR: {_score_level(n_o)} observado  →  {_score_level(n_t)} con potencial", bg=G_MED, span=5)

        # Headers
        _cs(ws5, r, 1, "Subcategoría",     bg=G_PALE, bold=True, size=9, border=THIN_B)
        _cs(ws5, r, 2, "✅ Observado",     bg="E8F5E9", bold=True, size=9, border=THIN_B)
        _cs(ws5, r, 3, "🌟 Pot. adicional",bg=AMBER, bold=True, size=9, border=THIN_B)
        _cs(ws5, r, 4, "N",               bg=G_PALE, bold=True, size=9, ha="center", border=THIN_B)
        _cs(ws5, r, 5, "Notas",            bg=G_PALE, bold=True, size=9, border=THIN_B)
        ws5.row_dimensions[r].height = 20; r += 1

        obs_data = data.get(f"petalo_{i}_obs", {})
        new_data = data.get(f"petalo_{i}_pot_new", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_new = data.get(f"petalo_{i}_otros_new", [])

        for cat_key in p.get("categorias", {}):
            cat_label = cat_key.replace("_"," ").title()
            obs_sel  = obs_data.get(cat_key, [])
            new_sel  = new_data.get(cat_key, [])
            if not obs_sel and not new_sel:
                continue
            _cs(ws5, r, 1, cat_label, bg=G_ULTRA, bold=True, size=9, border=THIN_B)
            _cs(ws5, r, 2, "; ".join(obs_sel), bg="F1F8F1", size=8, wrap=True, border=THIN_B)
            _cs(ws5, r, 3, "; ".join(new_sel), bg="FFFDE7", fg=AMBER_D, size=8, wrap=True, border=THIN_B)
            _cs(ws5, r, 4, str(len(obs_sel)+len(new_sel)), bg=G_ULTRA, size=9, ha="center", border=THIN_B)
            ws5.row_dimensions[r].height = max(20, min(len(obs_sel)*14, 60)); r += 1

        if otros_obs or otros_new:
            _cs(ws5, r, 1, "Otros",          bg=G_ULTRA, bold=True, size=9, border=THIN_B)
            _cs(ws5, r, 2, "; ".join(otros_obs), bg="F1F8F1", size=8, wrap=True, border=THIN_B)
            _cs(ws5, r, 3, "; ".join(otros_new), bg="FFFDE7", fg=AMBER_D, size=8, wrap=True, border=THIN_B)
            _cs(ws5, r, 4, str(len(otros_obs)+len(otros_new)), bg=G_ULTRA, size=9, ha="center", border=THIN_B)
            ws5.row_dimensions[r].height = 20; r += 1

        notas = data.get(f"petalo_{i}_notas","")
        if notas:
            _cs(ws5, r, 1, "📝 Notas:", bg=GOLD, bold=True, size=9)
            _cs(ws5, r, 2, notas, bg=GOLD, size=9, mc=4, wrap=True, italic=True)
            ws5.row_dimensions[r].height = 28; r += 1
        r = _sp(ws5, r, span=5)

    dest = data.get("pot_practicas_destacadas","")
    if dest:
        r = _sec(ws5, r, "✨ Prácticas más destacadas del espacio", span=5)
        r = _note(ws5, r, dest, span=5, h=50)

    # ════════════════════════════════════════════════════════════════════
    # HOJA 6 — M9 SÍNTESIS + PLAN
    # ════════════════════════════════════════════════════════════════════
    ws6 = wb.create_sheet("🗺️ M9 Síntesis + Plan")
    _wcol(ws6, [26, 18, 18, 14, 14, 12])
    r = 1
    r = _sec(ws6, r, "🗺️ MÓDULO 9 — SÍNTESIS Y PLAN DE ACCIÓN")
    r = _sp(ws6, r)
    r = _sec(ws6, r, "📊 Síntesis del Diagnóstico", bg=G_LIGHT)
    for key, label in [
        ("sint_fortalezas","💚 Fortalezas"), ("sint_desafios","⚡ Desafíos"),
        ("sint_oportunidades","🌱 Oportunidades"), ("sint_narrativa","📖 Narrativa"),
    ]:
        v = data.get(key,"")
        if v: r = _row(ws6, r, label, v)
    r = _sp(ws6, r)
    r = _sec(ws6, r, "🗓️ Plan de Acción — 3 Horizontes Temporales", bg=G_LIGHT)
    for plan_key, fase in [
        ("plan_inmediatas",    "⚡ Fase 1 — Inmediatas (0–3 meses)"),
        ("plan_estacionales",  "🌱 Fase 2 — Estacionales (3–12 meses)"),
        ("plan_estructurales", "🌳 Fase 3 — Estructurales (1–5 años)"),
    ]:
        r = _sec(ws6, r, fase, bg=G_MED, span=6)
        v = data.get(plan_key,"")
        if v:
            if isinstance(v, list):
                for acc in v:
                    if isinstance(acc, dict):
                        r = _row(ws6, r, acc.get("titulo",""), acc.get("resp",""))
                    else:
                        r = _row(ws6, r, str(acc), "")
            else:
                r = _note(ws6, r, str(v), h=40)
        r = _sp(ws6, r)

    # ════════════════════════════════════════════════════════════════════
    # HOJA 7 — DATOS BIOCLIMÁTICOS
    # ════════════════════════════════════════════════════════════════════
    ws7 = wb.create_sheet("🌡️ Datos Bioclimáticos")
    _wcol(ws7, [20, 14, 14, 14, 14, 14])
    r = 1
    r = _sec(ws7, r, "🌡️ DATOS BIOCLIMÁTICOS DEL SITIO")
    r = _sp(ws7, r)
    r = _sec(ws7, r, "📍 Localización", bg=G_LIGHT)
    for label, key in [
        ("Latitud","lat"),("Longitud","lon"),("Ciudad","proyecto_ciudad"),
        ("Elevación (m)","elevation"),
    ]:
        v = data.get(key)
        if v: r = _row(ws7, r, label, str(v))
    r = _sp(ws7, r)
    r = _sec(ws7, r, "🌡️ Temperatura", bg=G_LIGHT)
    for label, key in [
        ("Mes más cálido","clima_mes_caluroso"),("Temp. máx promedio (°C)","clima_t_max_abs"),
        ("Mes más frío","clima_mes_frio"),("Temp. mín promedio (°C)","clima_t_min_abs"),
    ]:
        v = data.get(key)
        if v is not None: r = _row(ws7, r, label, str(v))
    r = _sp(ws7, r)
    r = _sec(ws7, r, "💧 Precipitación y Radiación Solar", bg=G_LIGHT)
    r = _row(ws7, r, "Precipitación anual (mm)", str(data.get("agua_prec_anual","")))
    r = _row(ws7, r, "Radiación solar prom (kWh/m²/día)", str(data.get("solar_annual_avg","")))
    r = _row(ws7, r, "Mejor mes para solar", str(data.get("solar_best_month","")))
    r = _sp(ws7, r)

    # Freeze + gridlines
    for ws in [ws0, ws1, ws2, ws3, ws4, ws5, ws6, ws7]:
        ws.freeze_panes = "A2"
        ws.sheet_view.showGridLines = True

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()
