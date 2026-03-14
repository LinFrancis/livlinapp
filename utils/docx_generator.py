"""Generador de Informe Word (.docx) — Indagación Regenerativa v8.
Usa python-docx para generar un documento completo con todos los resultados del diagnóstico.
"""
import io
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from utils.scoring import (FLOWER_DOMAINS, ETHICAL_PRINCIPLES, SCORE_SCALE,
                            compute_domain_scores, compute_regenerative_score,
                            score_label, compute_synthesis_potentials)

# ── Paleta LivLin ──────────────────────────────────────────────────────────
C_DARK   = RGBColor(0x1B, 0x43, 0x32)   # #1B4332
C_MED    = RGBColor(0x2D, 0x6A, 0x4F)   # #2D6A4F
C_MAIN   = RGBColor(0x40, 0x91, 0x6C)   # #40916C
C_LIGHT  = RGBColor(0x52, 0xB7, 0x88)   # #52B788
C_PALE   = RGBColor(0xD8, 0xF3, 0xDC)   # #D8F3DC
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
C_GRAY   = RGBColor(0x66, 0x66, 0x66)

MODULE_STATUS_LABELS = {
    "respondido":  "✅ Respondido directamente",
    "inferido":    "🔍 Inferido por facilitador",
    "no_abordado": "⭕ Módulo no abordado",
}

def _module_status_line(doc, status: str):
    """Add a small status line below a section heading."""
    label = MODULE_STATUS_LABELS.get(status, "")
    if not label:
        return
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"  {label}")
    r.font.size = Pt(8)
    r.italic = True
    color_map = {
        "respondido":  RGBColor(0x1B, 0x43, 0x32),
        "inferido":    RGBColor(0x79, 0x55, 0x48),
        "no_abordado": RGBColor(0x9E, 0x9E, 0x9E),
    }
    r.font.color.rgb = color_map.get(status, C_GRAY)


def _set_cell_bg(cell, hex_color: str):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _heading(doc, text: str, level: int = 1,
             color: RGBColor = None, size: int = None):
    p = doc.add_heading(text, level=level)
    run = p.runs[0] if p.runs else p.add_run(text)
    if color:
        run.font.color.rgb = color
    if size:
        run.font.size = Pt(size)
    return p


def _para(doc, text: str, bold: bool = False,
          color: RGBColor = None, size: int = 11,
          italic: bool = False, spacing_after: int = 6) -> object:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(spacing_after)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = color
    return p


def _kv_table(doc, rows: list, col_widths=(5, 11)):
    """Render a 2-col key/value table. rows = [(label, value), ...]"""
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, (label, value) in enumerate(rows):
        row = tbl.rows[i]
        row.height = Cm(0.7)
        # Label cell
        lc = row.cells[0]
        lc.width = Cm(col_widths[0])
        _set_cell_bg(lc, "D8F3DC")
        lp = lc.paragraphs[0]
        lp.paragraph_format.space_after = Pt(0)
        lr = lp.add_run(str(label))
        lr.bold = True
        lr.font.size = Pt(9)
        lr.font.color.rgb = C_DARK
        # Value cell
        vc = row.cells[1]
        vc.width = Cm(col_widths[1])
        vp = vc.paragraphs[0]
        vp.paragraph_format.space_after = Pt(0)
        vr = vp.add_run(str(value)[:300] if value else "—")
        vr.font.size = Pt(9)
        vr.font.color.rgb = C_MED
    return tbl


def _score_row(doc, label: str, score, max_score: int = 5):
    """Render a score with mini bar visualization using underscores."""
    if score is None:
        return
    val = int(score) if score else 0
    bar = "█" * val + "░" * (max_score - val)
    colors = {0:"9E9E9E",1:"74C69D",2:"52B788",3:"40916C",4:"2D6A4F",5:"1B4332"}
    sl = SCORE_SCALE.get(val, {}).get("label", "—")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(f"  {label}: ")
    r1.font.size = Pt(9)
    r1.font.color.rgb = C_DARK
    r2 = p.add_run(f"{bar} {val}/5")
    r2.font.size = Pt(9)
    r2.bold = True
    r2.font.color.rgb = RGBColor.from_string(colors.get(val, "9E9E9E"))
    r3 = p.add_run(f"  {sl}")
    r3.font.size = Pt(8)
    r3.italic = True
    r3.font.color.rgb = C_GRAY


def generate_docx(data: dict) -> bytes:
    """Generate a complete Word document from visit data. Returns bytes."""
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx no está instalado. Agrega 'python-docx>=1.1.0' a requirements.txt")

    doc = Document()

    # ── Page margins ───────────────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(2.5)

    # ── Styles ─────────────────────────────────────────────────────────────
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)

    # ════════════════════════════════════════════════════════════════════════
    # PORTADA
    # ════════════════════════════════════════════════════════════════════════
    doc.add_paragraph()
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = p_title.add_run("🌿 INDAGACIÓN REGENERATIVA")
    rt.bold = True; rt.font.size = Pt(26); rt.font.color.rgb = C_DARK

    p_subtitle = doc.add_paragraph()
    p_subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = p_subtitle.add_run("Diagnóstico de Permacultura Urbana — LivLin v2.0  ·  www.livlin.com")
    rs.font.size = Pt(13); rs.font.color.rgb = C_MED; rs.italic = True

    doc.add_paragraph()

    nombre  = data.get("proyecto_nombre", "Sin nombre")
    cliente = data.get("proyecto_cliente", "")
    ciudad  = data.get("proyecto_ciudad", "")
    fecha   = data.get("proyecto_fecha") or str(datetime.now())[:10]
    facilitador = data.get("proyecto_facilitador", "")

    cover_rows = [
        ("🏡 Espacio", nombre),
        ("👤 Contacto", cliente),
        ("📍 Ciudad / Barrio", ciudad),
        ("📅 Fecha de visita", fecha),
    ]
    if facilitador:
        cover_rows.append(("🌱 Facilitador/a", facilitador))

    doc.add_paragraph()
    _kv_table(doc, cover_rows, col_widths=(5, 11))
    doc.add_paragraph()

    # Regenerative Score en portada
    global_score = compute_regenerative_score(data)
    label_g, _ = score_label(global_score)
    p_score = doc.add_paragraph()
    p_score.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_score.paragraph_format.space_before = Pt(12)
    r_sc = p_score.add_run(f"Regenerative Score Global: {global_score} / 5.0")
    r_sc.bold = True; r_sc.font.size = Pt(16); r_sc.font.color.rgb = C_DARK
    p_lbl = doc.add_paragraph()
    p_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_lbl = p_lbl.add_run(label_g)
    r_lbl.font.size = Pt(12); r_lbl.font.color.rgb = C_MAIN; r_lbl.italic = True

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════════
    # 1. INTENCIÓN Y CONTEXTO
    # ════════════════════════════════════════════════════════════════════════
    _heading(doc, "1. Intención y Contexto", 1, C_DARK, 14)
    _module_status_line(doc, data.get("mod_cliente", "respondido"))

    intenc = data.get("proyecto_intencion", "")
    tipo   = data.get("proyecto_tipo_espacio", "")
    sup    = data.get("proyecto_superficie", "")
    habit  = data.get("proyecto_habitantes", "")
    barrio = data.get("proyecto_barrio_desc", "")

    rows_ctx = []
    if tipo:    rows_ctx.append(("Tipo de espacio", tipo))
    if sup:     rows_ctx.append(("Superficie (m²)", str(sup)))
    if habit:   rows_ctx.append(("N° habitantes / personas", str(habit)))
    if ciudad:  rows_ctx.append(("Ciudad / Barrio", ciudad))
    if barrio:  rows_ctx.append(("Descripción del barrio", barrio))
    if rows_ctx:
        _kv_table(doc, rows_ctx)
        doc.add_paragraph()

    if intenc:
        _para(doc, "Intención del proyecto:", bold=True, color=C_DARK, size=10)
        _para(doc, intenc, color=C_GRAY, size=10, italic=True)

    # Motivación (Tao)
    motivacion = data.get("tao_motivacion", "")
    sueno      = data.get("tao_sueno", "")
    if motivacion or sueno:
        _para(doc, "Motivación y sueño regenerativo:", bold=True, color=C_MED, size=10)
        if motivacion: _para(doc, motivacion, italic=True, color=C_GRAY)
        if sueno:      _para(doc, sueno, italic=True, color=C_GRAY)

    doc.add_paragraph()

    # ════════════════════════════════════════════════════════════════════════
    # 2. OBSERVACIÓN ECOLÓGICA
    # ════════════════════════════════════════════════════════════════════════
    _heading(doc, "2. Observación Ecológica del Sitio", 1, C_DARK, 14)
    _module_status_line(doc, data.get("mod_sitio", "respondido"))

    suelo_rows = []
    for k, label in [
        ("suelo_tipo","Tipo de suelo"), ("suelo_compactacion","Compactación"),
        ("suelo_materia_organica","Materia orgánica"), ("suelo_drenaje","Drenaje"),
        ("suelo_color","Color del suelo"), ("suelo_olor","Olor"),
    ]:
        v = data.get(k)
        if v: suelo_rows.append((label, v))
    if suelo_rows:
        _heading(doc, "Suelo", 2, C_MED, 11)
        _kv_table(doc, suelo_rows)
        doc.add_paragraph()

    veg_tipos = data.get("veg_tipos", [])
    veg_esp   = data.get("veg_especies", "")
    if veg_tipos or veg_esp:
        _heading(doc, "Vegetación", 2, C_MED, 11)
        veg_rows = []
        if veg_tipos: veg_rows.append(("Tipos presentes", ", ".join(veg_tipos)))
        if veg_esp:   veg_rows.append(("Especies identificadas", veg_esp))
        inv = data.get("veg_invasoras","")
        if inv: veg_rows.append(("Invasoras / problemáticas", inv))
        _kv_table(doc, veg_rows)
        doc.add_paragraph()

    sol_h = data.get("sol_horas")
    if sol_h is not None:
        _heading(doc, "Flujos Naturales", 2, C_MED, 11)
        flujo_rows = [("Horas de sol/día (anual)", f"{sol_h} h")]
        for k, label in [
            ("sol_horas_invierno","Sol en invierno"), ("sol_horas_verano","Sol en verano"),
            ("sol_orientacion","Orientación"), ("viento_direccion","Viento predominante"),
        ]:
            v = data.get(k)
            if v is not None: flujo_rows.append((label, str(v)))
        _kv_table(doc, flujo_rows)
        doc.add_paragraph()

    # Cultivo
    cult_m2 = data.get("cultivo_m2")
    if cult_m2:
        _heading(doc, "Potencial de Cultivo", 2, C_MED, 11)
        cult_rows = [("Área cultivable (m²)", str(cult_m2))]
        for k, label in [
            ("cultivo_riego_acceso","Acceso al agua"), ("cultivo_produce_hoy","Produce alimentos hoy"),
            ("cultivo_frutales","Espacio para frutales"), ("cultivo_verticales","Cultivos verticales"),
        ]:
            v = data.get(k)
            if v: cult_rows.append((label, str(v)))
        _kv_table(doc, cult_rows)
        if data.get("bancales"):
            doc.add_paragraph()
            _para(doc, "Bancales / zonas de cultivo:", bold=True, color=C_DARK, size=9)
            for b in data["bancales"]:
                _para(doc, f"  • {b.get('nombre','')} — {b.get('area',0)} m² · {b.get('vol',0)} m³ · {b.get('litros',0)} L",
                      size=9, color=C_GRAY)
        doc.add_paragraph()

    # ════════════════════════════════════════════════════════════════════════
    # 3. SISTEMAS — AGUA, ENERGÍA, MATERIALES
    # ════════════════════════════════════════════════════════════════════════
    _heading(doc, "3. Sistemas — Agua, Energía y Materiales", 1, C_DARK, 14)
    _module_status_line(doc, data.get("mod_sistemas", "respondido"))

    # Agua
    _heading(doc, "3.1 · Sistema de Agua", 2, C_MED, 11)
    agua_rows = []
    for k, label in [
        ("agua_consumo","Consumo diario (L)"), ("agua_prec_anual","Precipitación anual (mm)"),
        ("agua_techo_m2","Área de techo captación (m²)"), ("agua_efic_captacion","Eficiencia captación (%)"),
        ("agua_riego_tipo","Tipo de riego"), ("agua_grises","Gestión aguas grises"),
    ]:
        v = data.get(k)
        if v is not None and v != "" and v != 0: agua_rows.append((label, str(v)))
    fuentes = data.get("fuentes_agua", [])
    if fuentes:
        agua_rows.append(("Fuentes de agua", ", ".join(f.get("tipo","") for f in fuentes)))
    if agua_rows: _kv_table(doc, agua_rows)
    doc.add_paragraph()

    # Energía
    _heading(doc, "3.2 · Sistema de Energía", 2, C_MED, 11)
    ene_rows = []
    for k, label in [
        ("ene_kwh_mes","Consumo mensual (kWh)"), ("ene_kwh_dia_calc","Consumo diario estimado (kWh)"),
        ("ene_fuente_principal","Fuente principal"), ("ene_solar_interes","Interés en solar"),
    ]:
        v = data.get(k)
        if v is not None and v != "": ene_rows.append((label, str(v)))
    equipos = data.get("equipos_electricos", [])
    if equipos:
        ene_rows.append(("Equipos principales", "; ".join(
            f"{e.get('nombre','')} {e.get('watts','')}W" for e in equipos[:5])))
    if ene_rows: _kv_table(doc, ene_rows)
    doc.add_paragraph()

    # Materiales
    _heading(doc, "3.3 · Materiales y Residuos", 2, C_MED, 11)
    mat_rows = []
    for k, label in [
        ("mat_residuos_organicos","Gestión residuos orgánicos"), ("mat_compost","Compostaje"),
        ("mat_reciclaje","Reciclaje"), ("mat_plastico_uso","Reducción plástico"),
    ]:
        v = data.get(k)
        if v: mat_rows.append((label, str(v)))
    if mat_rows: _kv_table(doc, mat_rows)
    doc.add_paragraph()

    # ════════════════════════════════════════════════════════════════════════
    # 4. FLOR DE LA PERMACULTURA — 7 PÉTALOS
    # ════════════════════════════════════════════════════════════════════════
    _heading(doc, "4. Flor de la Permacultura — 7 Pétalos", 1, C_DARK, 14)
    _module_status_line(doc, data.get("mod_potencial", "respondido"))
    _para(doc, f"Regenerative Score Global: {global_score} / 5.0 — {score_label(global_score)[0]}",
          bold=True, color=C_MAIN, size=12)
    doc.add_paragraph()

    # IPR scores
    ipr_obs = data.get("ipr_obs", [])
    ipr_pot = data.get("ipr_pot", [])
    _para(doc, "Observado vs Potencial por pétalo:", bold=True, color=C_MAIN, size=12)
    doc.add_paragraph()

    import json as _json2
    from pathlib import Path as _Path2
    _jf2 = _Path2(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(_jf2, encoding="utf-8") as _ff:
            _petalos2 = _json2.load(_ff)["petalos"]
    except Exception:
        _petalos2 = []

    icons2 = ["🌳","🏡","🛠️","📚","🧘","💚","🤝","🌿"]
    for i, p in enumerate(_petalos2):
        n_o = ipr_obs[i] if i < len(ipr_obs) else 0
        n_p = ipr_pot[i] if i < len(ipr_pot) else 0
        icon = icons2[i] if i < len(icons2) else "🌱"
        _heading(doc, f"{icon} {p['nombre']}", 2, C_MED, 11)
        _module_status_line(doc, "respondido")

        # Score summary
        score_txt = f"✅ Observado: {n_o} práctica(s)   |   🌟 Potencial: {n_p} práctica(s)"
        _para(doc, score_txt, bold=True, color=C_MAIN, size=10)

        obs_data = data.get(f"petalo_{i}_obs", {})
        pot_data = data.get(f"petalo_{i}_pot", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_pot = data.get(f"petalo_{i}_otros_pot", [])

        obs_rows = [(cat_key.replace("_"," ").title(), ", ".join(v))
                    for cat_key, v in obs_data.items() if v]
        if otros_obs: obs_rows.append(("Otros observados", ", ".join(otros_obs)))
        pot_rows = [(cat_key.replace("_"," ").title(), ", ".join(v))
                    for cat_key, v in pot_data.items() if v]
        if otros_pot: pot_rows.append(("Otros potencial", ", ".join(otros_pot)))

        if obs_rows:
            _para(doc, "✅ Prácticas observadas:", bold=True, color=RGBColor(0x1B,0x43,0x32), size=9)
            _kv_table(doc, obs_rows)
        if pot_rows:
            doc.add_paragraph()
            _para(doc, "🌟 Potencial identificado:", bold=True, color=RGBColor(0xE6,0x51,0x00), size=9)
            _kv_table(doc, pot_rows)

        notas = data.get(f"petalo_{i}_notas","")
        if notas:
            _para(doc, f"📝 {notas}", italic=True, color=C_GRAY, size=9)
        doc.add_paragraph()

    # Prácticas destacadas
    dest = data.get("pot_practicas_destacadas","")
    if dest:
        _para(doc, "✨ Prácticas más destacadas", bold=True, color=C_DARK, size=11)
        _para(doc, dest, italic=True, color=C_GRAY, size=10)

    # Principios éticos
    _heading(doc, "Principios Éticos", 2, C_MED, 11)
    for principle in ETHICAL_PRINCIPLES:
        eth_score = data.get(f"eth_score_{principle['key']}")
        title_line = principle["title"]
        if eth_score is not None:
            title_line += f"  [{eth_score}/5]"
        _para(doc, title_line, bold=True, color=C_DARK, size=10)
        for key, label, _ in principle["questions"]:
            v = data.get(key, "")
            if v:
                p = doc.add_paragraph()
                rb = p.add_run(f"{label}: ")
                rb.bold = True; rb.font.size = Pt(9); rb.font.color.rgb = C_MED
                rv = p.add_run(str(v))
                rv.font.size = Pt(9); rv.italic = True; rv.font.color.rgb = C_GRAY
    doc.add_paragraph()

    # ════════════════════════════════════════════════════════════════════════
    # 5. SÍNTESIS Y PLAN DE ACCIÓN
    # ════════════════════════════════════════════════════════════════════════
    _heading(doc, "5. Síntesis y Plan de Acción", 1, C_DARK, 14)
    _module_status_line(doc, data.get("mod_plan", "respondido"))

    for k, label in [
        ("sint_fortalezas",      "💚 Fortalezas del espacio"),
        ("sint_desafios",        "⚡ Desafíos principales"),
        ("sint_oportunidades",   "🌱 Oportunidades regenerativas"),
        ("sint_narrativa",       "📖 Narrativa del proceso"),
    ]:
        v = data.get(k, "")
        if v:
            _para(doc, label, bold=True, color=C_DARK, size=11)
            _para(doc, v, color=C_GRAY, size=10, italic=True)

    doc.add_paragraph()
    _heading(doc, "Plan de Acción", 2, C_MED, 11)

    for k, label, color in [
        ("plan_inmediatas",    "⚡ Acciones Inmediatas (0–3 meses)",   C_MAIN),
        ("plan_estacionales",  "🌿 Acciones Estacionales (3–12 meses)", C_MED),
        ("plan_estructurales", "🌳 Transformaciones Estructurales (1–3 años)", C_DARK),
    ]:
        v = data.get(k)
        if v:
            _para(doc, label, bold=True, color=color, size=10)
            if isinstance(v, list):
                for item in v:
                    p = doc.add_paragraph(style="List Bullet")
                    p.paragraph_format.space_after = Pt(3)
                    r = p.add_run(str(item))
                    r.font.size = Pt(9); r.font.color.rgb = C_GRAY
            else:
                for line in str(v).splitlines():
                    if line.strip():
                        p = doc.add_paragraph(style="List Bullet")
                        p.paragraph_format.space_after = Pt(3)
                        r = p.add_run(line.strip())
                        r.font.size = Pt(9); r.font.color.rgb = C_GRAY
            doc.add_paragraph()

    # ════════════════════════════════════════════════════════════════════════
    # PIE
    # ════════════════════════════════════════════════════════════════════════
    doc.add_page_break()
    p_pie = doc.add_paragraph()
    p_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pie = p_pie.add_run(f"Diagnóstico generado con LivLin — Indagación Regenerativa  ·  {str(datetime.now())[:10]}")
    r_pie.font.size = Pt(8); r_pie.font.color.rgb = C_GRAY; r_pie.italic = True

    # LivLin website line
    p_web = doc.add_paragraph()
    p_web.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_web = p_web.add_run("🌿 LivLin · Permacultura Urbana · www.livlin.com")
    r_web.font.size = Pt(9); r_web.font.color.rgb = C_MAIN; r_web.bold = True

    # ── Serialize to bytes ─────────────────────────────────────────────────
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()
