"""Excel export v2.2 — LivLin Indagación Regenerativa.
Auto-explicativo: cada sección incluye descripción, significado y referencias.
"""
import io, json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from utils.petal_content import (
    PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS,
    IPR_OBS_VS_POT, LIVLIN_DESC, LIVLIN_MODULES, GLOBAL_REFS
)

# ── Paleta ────────────────────────────────────────────────────────────────────
G_DARK="1B4332"; G_MED="2D6A4F"; G_MAIN="40916C"
G_PALE="D8F3DC"; G_ULTRA="F0FFF4"; WHITE="FFFFFF"
GOLD="FFF8DC"; AMBER="FFF3E0"; AMBER_D="E65100"; TEAL="E0F2F1"

def _f(h): return PatternFill("solid", fgColor=h)
def _s(s="thin"): return Side(style=s, color="AAAAAA")
THIN  = Border(left=_s(), right=_s(), top=_s(), bottom=_s())
BOT   = Border(bottom=Side(style="medium", color=G_MED))

def _cs(ws, r, c, val="", bg=WHITE, fg=G_DARK, bold=False, size=9,
        ha="left", wrap=True, mc=None, italic=False, border=None, url=None):
    if isinstance(val, (list, dict)): val = str(val)
    if val is None: val = ""
    cell = ws.cell(row=r, column=c, value=str(val)[:800])
    cell.fill = _f(bg)
    cell.font = Font(bold=bold, color=fg, size=size, italic=italic, name="Calibri",
                     underline="single" if url else None)
    cell.alignment = Alignment(horizontal=ha, vertical="top", wrap_text=wrap)
    if mc: ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+mc-1)
    if border: cell.border = border
    if url: cell.hyperlink = url
    return cell

def _head(ws, r, txt, bg=G_DARK, fg=WHITE, span=6, h=28, size=13):
    _cs(ws, r, 1, txt, bg=bg, fg=fg, bold=True, size=size, ha="center", mc=span)
    ws.row_dimensions[r].height = h; return r+1

def _subhead(ws, r, txt, bg=G_MED, fg=WHITE, span=6, h=22, size=10):
    _cs(ws, r, 1, txt, bg=bg, fg=fg, bold=True, size=size, mc=span)
    ws.row_dimensions[r].height = h; return r+1

def _expl(ws, r, txt, span=6, h=None):
    """Explanation/context row — amber background."""
    _cs(ws, r, 1, txt, bg=AMBER, fg="3E2723", italic=True, size=8, mc=span, wrap=True)
    ws.row_dimensions[r].height = h or max(18, min(len(txt)//6, 60))
    return r+1

def _row(ws, r, label, value, span_v=4, h=20):
    _cs(ws, r, 1, label, bg=G_PALE, bold=True, size=9, mc=2, border=THIN)
    _cs(ws, r, 3, value, bg="FAFFFE", size=9, mc=span_v, wrap=True, border=BOT)
    ws.row_dimensions[r].height = h; return r+1

def _sp(ws, r, span=6):
    _cs(ws, r, 1, "", bg=G_ULTRA, mc=span)
    ws.row_dimensions[r].height = 5; return r+1

def _ref_row(ws, r, author, title, url, span=6):
    _cs(ws, r, 1, author, bg="F8F8F8", bold=True, size=8, mc=2, border=THIN)
    _cs(ws, r, 3, title,  bg="F8F8F8", size=8, mc=3, wrap=True, border=BOT)
    _cs(ws, r, 6, url, bg="F8F8F8", fg="1565C0", size=8, url=url, border=BOT)
    ws.row_dimensions[r].height = 18; return r+1

def _wcol(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def _load_petalos():
    jf = Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(jf, encoding="utf-8") as f:
            return json.load(f)["petalos"]
    except Exception:
        return []


def generate_excel(data: dict) -> bytes:
    wb = Workbook()
    petalos = _load_petalos()

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 0 — PRESENTACIÓN
    # ─────────────────────────────────────────────────────────────────────
    ws0 = wb.active; ws0.title = "🌿 Presentación"
    _wcol(ws0, [26, 16, 20, 18, 20, 16])

    r = _head(ws0, 1, "🌿 LivLin · Indagación Regenerativa v2.2", h=50, size=18)
    r = _head(ws0, r, "Diagnóstico de Permacultura Urbana  ·  www.livlin.com",
              bg=G_MED, h=26, size=11)
    r = _sp(ws0, r)

    # Datos del diagnóstico
    r = _subhead(ws0, r, "📋 Información del Diagnóstico")
    for lbl, key in [("Espacio","proyecto_nombre"),("Contacto","proyecto_cliente"),
                     ("Ciudad","proyecto_ciudad"),("Fecha","proyecto_fecha"),
                     ("Tipo de espacio","proyecto_tipo_espacio")]:
        r = _row(ws0, r, lbl, data.get(key,""))
    r = _sp(ws0, r)

    # About LivLin
    r = _subhead(ws0, r, "🌱 ¿Qué es LivLin?")
    r = _expl(ws0, r, LIVLIN_DESC, h=55)
    _cs(ws0, r, 1, "🔗 www.livlin.com", bg=G_ULTRA, fg="1565C0", size=9,
        url="https://www.livlin.com", mc=6)
    ws0.row_dimensions[r].height = 18; r += 1
    r = _sp(ws0, r)

    # IPR explanation
    r = _subhead(ws0, r, "📊 ¿Qué es el Índice de Potencial Regenerativo (IPR)?")
    r = _expl(ws0, r, IPR_WHAT_IS, h=55)
    r = _expl(ws0, r, IPR_OBS_VS_POT, h=45)
    r = _sp(ws0, r)

    # IPR scale
    r = _subhead(ws0, r, "🔢 Escala de niveles IPR — Cómo interpretar los resultados", bg=G_MAIN)
    _cs(ws0, r, 1, "Nivel", bg=G_PALE, bold=True, size=9, border=THIN)
    _cs(ws0, r, 2, "N° prácticas", bg=G_PALE, bold=True, size=9, ha="center", border=THIN)
    _cs(ws0, r, 3, "¿Qué significa?", bg=G_PALE, bold=True, size=9, mc=4, border=THIN)
    ws0.row_dimensions[r].height = 20; r += 1
    for lvl, n, color, meaning in IPR_SCALE:
        _cs(ws0, r, 1, lvl, bg=color+"22" if len(color)==6 else G_ULTRA,
            bold=True, size=9, border=THIN)
        _cs(ws0, r, 2, n,  bg=G_ULTRA, size=9, ha="center", border=THIN)
        _cs(ws0, r, 3, meaning, bg=G_ULTRA, size=9, mc=4, wrap=True, border=BOT)
        ws0.row_dimensions[r].height = 30; r += 1
    r = _sp(ws0, r)

    # Module index
    r = _subhead(ws0, r, "📑 Índice de módulos — Qué encontrarás en cada hoja")
    for mod_name, mod_desc in LIVLIN_MODULES:
        _cs(ws0, r, 1, mod_name, bg=G_PALE, bold=True, size=9, mc=2, border=THIN)
        _cs(ws0, r, 3, mod_desc, bg=G_ULTRA, size=9, mc=4, wrap=True, border=BOT)
        ws0.row_dimensions[r].height = 28; r += 1
    r = _sp(ws0, r)

    # Global references
    r = _subhead(ws0, r, "📚 Referencias bibliográficas y recursos en línea")
    r = _expl(ws0, r,
        "Las siguientes fuentes sustentan la metodología del diagnóstico. "
        "Haz clic en las URLs para acceder directamente a los recursos.", h=30)
    for author, title, url in GLOBAL_REFS:
        r = _ref_row(ws0, r, author, title, url)

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 1 — RESUMEN EJECUTIVO
    # ─────────────────────────────────────────────────────────────────────
    ws1 = wb.create_sheet("📊 Resumen Ejecutivo")
    _wcol(ws1, [26, 16, 16, 12, 14, 14])
    r = _head(ws1, 1, "📊 RESUMEN EJECUTIVO — Índice de Potencial Regenerativo (IPR)")
    r = _expl(ws1, r, f"{IPR_WHAT_IS}  {IPR_OBS_VS_POT}", h=60)
    r = _sp(ws1, r)
    for lbl, key in [("Espacio","proyecto_nombre"),("Contacto","proyecto_cliente"),
                     ("Fecha","proyecto_fecha"),("Ciudad","proyecto_ciudad")]:
        r = _row(ws1, r, lbl, data.get(key,""))
    r = _sp(ws1, r)

    r = _subhead(ws1, r, "🌸 IPR por pétalo — Observado vs Con potencial adicional")
    _cs(ws1, r, 1, "Pétalo", bg=G_PALE, bold=True, size=9, mc=2, border=THIN)
    _cs(ws1, r, 3, "✅ Observado hoy", bg="E8F5E9", bold=True, size=9, ha="center", border=THIN)
    _cs(ws1, r, 4, "🌟 + Potencial", bg=AMBER, bold=True, size=9, ha="center", border=THIN)
    _cs(ws1, r, 5, "Nivel observado", bg=G_PALE, bold=True, size=9, ha="center", border=THIN)
    _cs(ws1, r, 6, "Nivel total", bg=G_PALE, bold=True, size=9, ha="center", border=THIN)
    ws1.row_dimensions[r].height = 20; r += 1

    ipr_obs = data.get("ipr_obs", [])
    ipr_new = data.get("ipr_new", [])

    def _score_lv(n):
        if n==0: return "○ Sin inicio"
        if n==1: return "🌱 Iniciando"
        if n==2: return "🌿 Avanzando"
        if n==3: return "🌳 Consolidado"
        if n<=5: return "🌸 Destacado"
        return "✨ Referente"

    for i, p in enumerate(petalos):
        icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
        n_o  = ipr_obs[i] if i < len(ipr_obs) else 0
        n_n  = ipr_new[i] if i < len(ipr_new) else 0
        bg   = G_PALE if i % 2 == 0 else G_ULTRA
        _cs(ws1, r, 1, f"{icon} {p['nombre']}", bg=bg, bold=True, size=9, mc=2, border=THIN)
        _cs(ws1, r, 3, str(n_o), bg="F1F8F1", size=10, ha="center", border=THIN)
        _cs(ws1, r, 4, f"+{n_n}", bg="FFFDE7", fg=AMBER_D, size=10, ha="center", border=THIN)
        _cs(ws1, r, 5, _score_lv(n_o), bg=bg, size=8, ha="center", border=THIN)
        _cs(ws1, r, 6, _score_lv(n_o+n_n), bg=bg, size=8, ha="center", border=THIN)
        ws1.row_dimensions[r].height = 22; r += 1
    r = _sp(ws1, r)

    # IPR scale reminder
    r = _subhead(ws1, r, "🔢 Escala IPR — Referencia rápida", bg=G_MAIN)
    for lvl, n, _, meaning in IPR_SCALE:
        _cs(ws1, r, 1, f"{lvl} ({n})", bg=G_PALE, bold=True, size=8, mc=2, border=THIN)
        _cs(ws1, r, 3, meaning, bg=G_ULTRA, size=8, mc=4, wrap=True, border=BOT)
        ws1.row_dimensions[r].height = 22; r += 1
    r = _sp(ws1, r)

    dest = data.get("pot_practicas_destacadas","")
    if dest:
        r = _subhead(ws1, r, "✨ Prácticas más destacadas del espacio")
        _cs(ws1, r, 1, dest, bg=GOLD, fg="5C3D00", size=9, mc=6, wrap=True, italic=True)
        ws1.row_dimensions[r].height = 50; r += 1
    r = _sp(ws1, r)
    r = _expl(ws1, r,
        "📚 Metodología: Holmgren, D. (2002). Permacultura: Principios y senderos. "
        "Mollison, B. (1988). Permaculture: A Designers' Manual. · www.livlin.com", h=30)

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 2 — M1
    # ─────────────────────────────────────────────────────────────────────
    ws2 = wb.create_sheet("📋 M1 Información + Tao")
    _wcol(ws2, [24, 14, 24, 14, 12, 10])
    r = _head(ws2, 1, "📋 MÓDULO 1 — Información del Proyecto + Tao de la Regeneración")
    r = _expl(ws2, r,
        "Este módulo establece el contexto humano y motivacional del diagnóstico. "
        "Registra los datos del espacio, la intención regenerativa del grupo y su "
        "percepción de la triple crisis ambiental (cambio climático, pérdida de "
        "biodiversidad, contaminación). El 'sueño regenerativo' es la visión de futuro "
        "que guiará el proceso de transformación.", h=50)
    r = _sp(ws2, r)
    r = _subhead(ws2, r, "🏡 Datos del Espacio")
    for lbl, key in [
        ("Nombre del espacio","proyecto_nombre"),("Contacto / Grupo","proyecto_cliente"),
        ("Ciudad / País","proyecto_ciudad"),("Dirección / Barrio","proyecto_direccion"),
        ("Tipo de espacio","proyecto_tipo_espacio"),("Superficie (m²)","proyecto_superficie"),
        ("N° Habitantes","proyecto_habitantes"),("Descripción del barrio","proyecto_barrio_desc"),
        ("Intención del proyecto","proyecto_intencion"),
    ]:
        r = _row(ws2, r, lbl, str(data.get(key,"") or ""))
    r = _sp(ws2, r)
    r = _subhead(ws2, r, "🌀 Tao de la Regeneración")
    r = _expl(ws2, r,
        "El 'Tao de la Regeneración' explora la motivación profunda del espacio y sus "
        "habitantes. ¿Por qué quieren transformar este espacio? ¿Cuál es el sueño? "
        "¿Cómo perciben los grandes desafíos globales desde su contexto local?", h=40)
    for lbl, key in [
        ("Motivación principal","tao_motivacion"),("Sueño regenerativo","tao_sueno"),
        ("Relación con la naturaleza","tao_naturaleza"),("Desafíos percibidos","tao_desafios"),
        ("Cambio climático — percepción","tao_cc"),
        ("Pérdida de biodiversidad","tao_bio"),("Contaminación","tao_contam"),
    ]:
        v = data.get(key,"")
        if v: r = _row(ws2, r, lbl, str(v))

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 3 — M2-3
    # ─────────────────────────────────────────────────────────────────────
    ws3 = wb.create_sheet("🔬 M2-3 Ecología + Cultivo")
    _wcol(ws3, [24, 14, 24, 14, 12, 10])
    r = _head(ws3, 1, "🔬 MÓDULOS 2-3 — Observación Ecológica del Sitio")
    r = _expl(ws3, r,
        "La observación ecológica es la base del diseño en permacultura: 'observar e "
        "interactuar' es el primer principio de Holmgren. Este módulo registra las "
        "condiciones reales del suelo, vegetación, fauna, flujos naturales (sol, viento, agua) "
        "y potencial de producción de alimentos. Es la lectura del 'libro del sitio'.", h=50)
    r = _sp(ws3, r)
    for section, fields in [
        ("🪱 Suelo — Base de todo sistema vivo", [
            ("Tipo de suelo","suelo_tipo","El tipo de suelo determina qué se puede cultivar y cómo mejorarlo"),
            ("Compactación","suelo_compactacion","Alta compactación dificulta el crecimiento de raíces y la infiltración"),
            ("Materia orgánica","suelo_materia_organica","Indicador clave de salud del suelo"),
            ("Drenaje","suelo_drenaje","Drenaje deficiente puede causar encharcamiento y pudrición de raíces"),
            ("Color del suelo","suelo_color","El color revela el contenido de materia orgánica y minerales"),
            ("Olor al cavar","suelo_olor","Un olor a tierra húmeda indica actividad biológica saludable"),
            ("Notas del suelo","suelo_notas",""),
        ]),
        ("🌿 Vegetación", [
            ("Tipos presentes","veg_tipos",""),
            ("Especies identificadas","veg_especies",""),
            ("Invasoras / problemáticas","veg_invasoras","Las invasoras compiten con cultivos pero pueden indicar condiciones del suelo"),
        ]),
        ("☀️ Flujos Naturales", [
            ("Horas de sol / día","sol_horas","Mínimo 6h para la mayoría de los cultivos"),
            ("Orientación","sol_orientacion","Norte = más sol en el hemisferio sur"),
            ("Viento predominante","viento_direccion",""),
            ("Precipitación anual (mm)","agua_prec_anual",""),
            ("Mes más cálido","clima_mes_caluroso",""),("Mes más frío","clima_mes_frio",""),
            ("T° máxima registrada","clima_t_max_abs",""),("T° mínima registrada","clima_t_min_abs",""),
        ]),
        ("🥦 Potencial de Cultivo", [
            ("Área cultivable (m²)","cultivo_m2",""),
            ("Acceso al agua","cultivo_riego_acceso",""),
            ("Produce alimentos hoy","cultivo_produce_hoy",""),
            ("Espacio para frutales","cultivo_frutales",""),
        ]),
    ]:
        r = _subhead(ws3, r, section)
        for item in fields:
            lbl, key = item[0], item[1]
            nota = item[2] if len(item) > 2 else ""
            v = data.get(key, "")
            if v or nota:
                full_lbl = f"{lbl}\n({nota})" if nota else lbl
                r = _row(ws3, r, full_lbl, str(v) if v else "— no registrado —")
        r = _sp(ws3, r)

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 4 — M4-6
    # ─────────────────────────────────────────────────────────────────────
    ws4 = wb.create_sheet("🏙️ M4-6 Sistemas")
    _wcol(ws4, [24, 14, 24, 14, 12, 10])
    r = _head(ws4, 1, "🏙️ MÓDULOS 4-6 — Contexto Urbano, Agua, Energía y Materiales")
    r = _expl(ws4, r,
        "Este módulo analiza los sistemas que sostienen la vida cotidiana del espacio: "
        "¿de dónde viene y adónde va el agua? ¿Cómo se genera y consume la energía? "
        "¿Qué pasa con los residuos y materiales? Identificar estos flujos es clave para "
        "diseñar un sistema regenerativo que cierre ciclos y reduzca dependencias externas.", h=50)
    r = _sp(ws4, r)

    r = _subhead(ws4, r, "💧 Sistema de Agua")
    r = _expl(ws4, r,
        "El agua es el recurso más estratégico en un espacio urbano. Captarla, almacenarla, "
        "reutilizarla y devolverla limpia al ciclo son las metas del diseño hídrico regenerativo. "
        "Referencia: Lancaster, B. (2006). Rainwater Harvesting for Drylands. Rainsource Press.", h=40)
    for lbl, key, nota in [
        ("Consumo diario (L)","agua_consumo","Promedio global: 150-200L/persona/día. Meta regenerativa: <80L"),
        ("Precipitación anual (mm)","agua_prec_anual","Define el potencial de captación de lluvia"),
        ("Área de techo captación (m²)","agua_techo_m2","Potencial captación ≈ m² × mm lluvia × 0.8 eficiencia"),
        ("Tipo de riego","agua_riego_tipo","El riego por goteo ahorra hasta 70% vs riego por aspersión"),
        ("Gestión aguas grises","agua_grises","Las aguas grises tratadas pueden reutilizarse para riego"),
    ]:
        v = data.get(key,"")
        r = _row(ws4, r, f"{lbl}\n({nota})" if nota else lbl, str(v) if v else "")
    r = _sp(ws4, r)

    r = _subhead(ws4, r, "⚡ Sistema de Energía")
    r = _expl(ws4, r,
        "La energía solar es el recurso renovable más accesible en contextos urbanos. "
        "Entender el consumo actual permite dimensionar correctamente un sistema solar. "
        "Referencia: Renewable Energy World — www.renewableenergyworld.com", h=35)
    for lbl, key, nota in [
        ("Consumo mensual (kWh)","ene_kwh_mes","Consumo promedio hogar Chile: 150-250 kWh/mes"),
        ("Fuente principal","ene_fuente_principal",""),
        ("Interés en solar","ene_solar_interes",""),
    ]:
        v = data.get(key,"")
        r = _row(ws4, r, f"{lbl}\n({nota})" if nota else lbl, str(v) if v else "")
    r = _sp(ws4, r)

    r = _subhead(ws4, r, "♻️ Materiales y Residuos")
    r = _expl(ws4, r,
        "Cerrar el ciclo de materiales: lo que sale de un sistema como residuo puede ser "
        "el insumo de otro. El compostaje transforma residuos orgánicos en suelo vivo. "
        "Referencia: Ellen MacArthur Foundation — ellenmacarthurfoundation.org", h=35)
    for lbl, key in [
        ("Gestión residuos orgánicos","mat_residuos_organicos"),
        ("Compostaje","mat_compost"),("Reciclaje","mat_reciclaje"),
        ("Reducción plástico","mat_plastico_uso"),
    ]:
        v = data.get(key,"")
        if v: r = _row(ws4, r, lbl, str(v))

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 5 — M7 FLOR PERMACULTURA
    # ─────────────────────────────────────────────────────────────────────
    ws5 = wb.create_sheet("🌸 M7 Flor Permacultura")
    _wcol(ws5, [28, 20, 20, 6, 28])

    r = _head(ws5, 1, "🌸 FLOR DE LA PERMACULTURA — Índice de Potencial Regenerativo (IPR) · LivLin v2.2")
    r = _expl(ws5, r, IPR_WHAT_IS, h=50)
    r = _expl(ws5, r, IPR_OBS_VS_POT, h=40)
    r = _sp(ws5, r, span=5)

    # IPR scale in this sheet
    r = _subhead(ws5, r, "🔢 Escala IPR — Cómo leer los resultados por pétalo", bg=G_MAIN, span=5)
    for lvl, n, _, meaning in IPR_SCALE:
        _cs(ws5, r, 1, f"{lvl} ({n} prácticas)", bg=G_PALE, bold=True, size=8, mc=2, border=THIN)
        _cs(ws5, r, 3, meaning, bg=G_ULTRA, size=8, mc=3, wrap=True, border=BOT)
        ws5.row_dimensions[r].height = 22; r += 1
    r = _sp(ws5, r, span=5)

    for i, p in enumerate(petalos):
        icon   = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
        n_o    = ipr_obs[i] if i < len(ipr_obs) else 0
        n_n    = ipr_new[i] if i < len(ipr_new) else 0
        lv_o   = _score_lv(n_o); lv_t = _score_lv(n_o + n_n)
        desc   = PETAL_DESC.get(p["nombre"], {})
        resumen = desc.get("resumen","") if isinstance(desc, dict) else str(desc)
        detalle = desc.get("detalle","") if isinstance(desc, dict) else ""
        refs    = desc.get("referencias",[]) if isinstance(desc, dict) else []

        r = _subhead(ws5, r, f"{icon} {p['nombre']}  ·  {lv_o} observado  →  {lv_t} con potencial", span=5)

        # Petal description
        if resumen:
            r = _expl(ws5, r, resumen, span=5, h=40)
        if detalle:
            r = _expl(ws5, r, detalle, span=5, h=55)

        # Scores
        _cs(ws5, r, 1, f"✅ Observado: {n_o} práctica(s) — {lv_o}",
            bg="E8F5E9", bold=True, size=9, mc=2, border=THIN)
        _cs(ws5, r, 3, f"🌟 Pot. adicional: +{n_n} práctica(s) — Total: {lv_t}",
            bg=AMBER, fg=AMBER_D, bold=True, size=9, mc=3, border=THIN)
        ws5.row_dimensions[r].height = 22; r += 1

        # Action columns headers
        _cs(ws5, r, 1, "Subcategoría", bg=G_PALE, bold=True, size=8, border=THIN)
        _cs(ws5, r, 2, "✅ Prácticas observadas", bg="E8F5E9", bold=True, size=8, border=THIN)
        _cs(ws5, r, 3, "🌟 Potencial adicional", bg=AMBER, bold=True, fg=AMBER_D, size=8, border=THIN)
        _cs(ws5, r, 4, "N", bg=G_PALE, bold=True, size=8, ha="center", border=THIN)
        _cs(ws5, r, 5, "Notas del facilitador", bg=G_PALE, bold=True, size=8, border=THIN)
        ws5.row_dimensions[r].height = 18; r += 1

        obs_data  = data.get(f"petalo_{i}_obs",     {})
        new_data  = data.get(f"petalo_{i}_pot_new", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_new = data.get(f"petalo_{i}_otros_new", [])
        notas     = data.get(f"petalo_{i}_notas","")

        has_any = False
        for cat_key in p.get("categorias", {}):
            obs_sel = obs_data.get(cat_key, [])
            new_sel = new_data.get(cat_key, [])
            if not obs_sel and not new_sel: continue
            has_any = True
            cat_lbl = cat_key.replace("_"," ").title()
            _cs(ws5, r, 1, cat_lbl, bg=G_ULTRA, bold=True, size=8, border=THIN)
            _cs(ws5, r, 2, " · ".join(obs_sel), bg="F1F8F1", size=8, wrap=True, border=THIN)
            _cs(ws5, r, 3, " · ".join(new_sel), bg="FFFDE7", fg=AMBER_D, size=8, wrap=True, border=THIN)
            _cs(ws5, r, 4, str(len(obs_sel)+len(new_sel)), bg=G_ULTRA, size=9, ha="center", border=THIN)
            ws5.row_dimensions[r].height = max(18, min((len(obs_sel)+len(new_sel))*12, 60))
            r += 1

        if otros_obs or otros_new:
            _cs(ws5, r, 1, "Otros",          bg=G_ULTRA, bold=True, size=8, border=THIN)
            _cs(ws5, r, 2, " · ".join(otros_obs), bg="F1F8F1", size=8, wrap=True, border=THIN)
            _cs(ws5, r, 3, " · ".join(otros_new), bg="FFFDE7", fg=AMBER_D, size=8, wrap=True, border=THIN)
            _cs(ws5, r, 4, str(len(otros_obs)+len(otros_new)), bg=G_ULTRA, size=9, ha="center", border=THIN)
            ws5.row_dimensions[r].height = 20; r += 1
            has_any = True

        if not has_any:
            _cs(ws5, r, 1, "— Módulo no completado en este pétalo —",
                bg=G_ULTRA, italic=True, fg="888888", size=8, mc=4)
            ws5.row_dimensions[r].height = 18; r += 1

        if notas:
            _cs(ws5, r, 1, "📝 Notas:", bg=GOLD, bold=True, size=8)
            _cs(ws5, r, 2, notas, bg=GOLD, fg="5C3D00", size=8, mc=3, wrap=True, italic=True)
            ws5.row_dimensions[r].height = 30; r += 1

        # References for this petal
        if refs:
            for auth, tit, url in refs:
                _cs(ws5, r, 1, f"📚 {auth}", bg="F0F0F0", italic=True, size=7, mc=2)
                _cs(ws5, r, 3, tit, bg="F0F0F0", italic=True, size=7)
                _cs(ws5, r, 4, url, bg="F0F0F0", fg="1565C0", size=7, url=url, mc=2)
                ws5.row_dimensions[r].height = 16; r += 1

        r = _sp(ws5, r, span=5)

    dest = data.get("pot_practicas_destacadas","")
    if dest:
        r = _subhead(ws5, r, "✨ Prácticas más destacadas del espacio", span=5)
        _cs(ws5, r, 1, dest, bg=GOLD, fg="5C3D00", size=9, mc=5, wrap=True, italic=True)
        ws5.row_dimensions[r].height = 50; r += 1

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 6 — M9
    # ─────────────────────────────────────────────────────────────────────
    ws6 = wb.create_sheet("🗺️ M9 Síntesis + Plan")
    _wcol(ws6, [26, 14, 22, 14, 14, 10])
    r = _head(ws6, 1, "🗺️ MÓDULO 9 — Síntesis y Plan de Acción")
    r = _expl(ws6, r,
        "La síntesis integra todas las observaciones del diagnóstico en una visión coherente "
        "del espacio. El plan de acción organiza los próximos pasos en 3 horizontes temporales: "
        "acciones inmediatas (cambios rápidos, bajo costo), estacionales (requieren planificación) "
        "y estructurales (transformaciones de fondo a largo plazo).", h=45)
    r = _sp(ws6, r)
    r = _subhead(ws6, r, "📊 Síntesis del Diagnóstico")
    for key, lbl, expl in [
        ("sint_fortalezas","💚 Fortalezas","Lo que ya existe y funciona bien — base para construir"),
        ("sint_desafios","⚡ Desafíos","Obstáculos reales que requieren atención"),
        ("sint_oportunidades","🌱 Oportunidades","Potencial identificado pero aún no activado"),
        ("sint_narrativa","📖 Narrativa del proceso","Historia del espacio y su transformación"),
    ]:
        v = data.get(key,"")
        if v: r = _row(ws6, r, f"{lbl}\n({expl})", str(v), h=28)
    r = _sp(ws6, r)

    for plan_key, fase, desc_plan in [
        ("plan_inmediatas","⚡ Fase 1 — Acciones Inmediatas (0–3 meses)",
         "Cambios de bajo costo y alta visibilidad que generan motivación y muestran resultados rápidos"),
        ("plan_estacionales","🌱 Fase 2 — Acciones Estacionales (3–12 meses)",
         "Intervenciones que siguen los ritmos naturales y requieren mayor planificación"),
        ("plan_estructurales","🌳 Fase 3 — Transformaciones Estructurales (1–5 años)",
         "Cambios de fondo en infraestructura, gobernanza o sistemas que transforman el espacio a largo plazo"),
    ]:
        r = _subhead(ws6, r, fase)
        r = _expl(ws6, r, desc_plan, h=28)
        v = data.get(plan_key,"")
        if v:
            if isinstance(v, list):
                for item in v:
                    txt = item.get("titulo","") if isinstance(item,dict) else str(item)
                    r = _row(ws6, r, "→", txt)
            else:
                _cs(ws6, r, 1, str(v), bg=GOLD, fg="5C3D00", size=9, mc=6, wrap=True)
                ws6.row_dimensions[r].height = 40; r += 1
        else:
            _cs(ws6, r, 1, "— Sin acciones registradas —", bg=G_ULTRA, italic=True, fg="888888", size=8, mc=6)
            ws6.row_dimensions[r].height = 18; r += 1
        r = _sp(ws6, r)

    # ─────────────────────────────────────────────────────────────────────
    # HOJA 7 — DATOS BIOCLIMÁTICOS
    # ─────────────────────────────────────────────────────────────────────
    ws7 = wb.create_sheet("🌡️ Datos Bioclimáticos")
    _wcol(ws7, [26, 14, 24, 12, 14, 10])
    r = _head(ws7, 1, "🌡️ Datos Bioclimáticos del Sitio")
    r = _expl(ws7, r,
        "Los datos bioclimáticos son la base del diseño solar pasivo, el cálculo de captación "
        "de agua lluvia y la selección de cultivos apropiados. Fuente: Open-Meteo Historical API "
        "(datos históricos 5 años). Referencia: Hemenway, T. (2009). Gaia's Garden.", h=40)
    r = _sp(ws7, r)
    r = _subhead(ws7, r, "📍 Localización")
    for lbl, key, nota in [
        ("Latitud","lat",""),("Longitud","lon",""),
        ("Ciudad","proyecto_ciudad",""),("Elevación (m)","elevation",""),
    ]:
        v = data.get(key,"")
        if v is not None and v != "":
            r = _row(ws7, r, f"{lbl} {('('+nota+')') if nota else ''}", str(v))
    r = _sp(ws7, r)
    r = _subhead(ws7, r, "🌡️ Temperatura — Datos históricos")
    r = _expl(ws7, r,
        "Temperaturas basadas en promedio de los últimos 5 años disponibles. "
        "La T° mínima registrada es clave para seleccionar cultivos resistentes a heladas.", h=30)
    for lbl, key, nota in [
        ("Mes más cálido","clima_mes_caluroso","Mayor demanda de riego y refrigeración"),
        ("Temp. máx promedio (°C)","clima_t_max_abs","T° máxima del mes más cálido"),
        ("Mes más frío","clima_mes_frio","Riesgo de heladas, menor crecimiento vegetal"),
        ("Temp. mín promedio (°C)","clima_t_min_abs","T° mínima del mes más frío — crítica para cultivos"),
    ]:
        v = data.get(key,"")
        if v is not None and v != "":
            r = _row(ws7, r, f"{lbl}\n({nota})", str(v))
    r = _sp(ws7, r)
    r = _subhead(ws7, r, "💧 Agua y Solar")
    for lbl, key, nota in [
        ("Precipitación anual (mm)","agua_prec_anual",
         "Potencial captación techo (L) = mm × m² techo × 0.8"),
        ("Radiación solar prom (kWh/m²/día)","solar_annual_avg",
         "Referencia para dimensionar sistema solar fotovoltaico o térmico"),
        ("Mejor mes para solar","solar_best_month","Mes con mayor irradiancia disponible"),
    ]:
        v = data.get(key,"")
        if v is not None and v != "":
            r = _row(ws7, r, f"{lbl}\n({nota})", str(v))

    # Freeze + grid
    for ws in [ws0,ws1,ws2,ws3,ws4,ws5,ws6,ws7]:
        ws.freeze_panes = "A2"
        ws.sheet_view.showGridLines = True

    buf = io.BytesIO()
    wb.save(buf); buf.seek(0)
    return buf.read()
