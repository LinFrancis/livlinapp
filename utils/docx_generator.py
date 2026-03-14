"""Generador de Informe Word v2.2 — LivLin Indagación Regenerativa.
Auto-explicativo: incluye descripción de cada pétalo, escala IPR y referencias.
"""
import io
from datetime import datetime
from utils.petal_content import (
    PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS,
    IPR_OBS_VS_POT, LIVLIN_DESC, LIVLIN_MODULES, GLOBAL_REFS
)

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    import json
    from pathlib import Path
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

C_DARK  = RGBColor(0x1B,0x43,0x32) if DOCX_OK else None
C_MED   = RGBColor(0x2D,0x6A,0x4F) if DOCX_OK else None
C_MAIN  = RGBColor(0x40,0x91,0x6C) if DOCX_OK else None
C_AMBER = RGBColor(0xE6,0x51,0x00) if DOCX_OK else None
C_GRAY  = RGBColor(0x55,0x55,0x55) if DOCX_OK else None

MODULE_STATUS = {
    "respondido":  "✅ Respondido directamente por las personas del espacio",
    "inferido":    "🔍 Inferido por el facilitador tras la visita",
    "no_abordado": "⭕ Módulo no abordado en esta visita",
}

def _shd(cell, hex_color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color); tcPr.append(shd)

def _heading(doc, text, level=1, color=None, size=None):
    p = doc.add_heading(text, level=level)
    r = p.runs[0] if p.runs else p.add_run(text)
    if color: r.font.color.rgb = color
    if size:  r.font.size = Pt(size)
    return p

def _para(doc, text, bold=False, color=None, size=10, italic=False, after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return p

def _expl_box(doc, text, size=9):
    """Amber explanation box."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Cm(0.5)
    r = p.add_run(text)
    r.font.size = Pt(size); r.italic = True
    r.font.color.rgb = RGBColor(0xE6,0x51,0x00)

def _kv(doc, rows, col_w=(5,11)):
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = "Table Grid"
    for i, (lbl, val) in enumerate(rows):
        cells = tbl.rows[i].cells
        _shd(cells[0], "D8F3DC"); _shd(cells[1], "FFFFFF")
        cells[0].paragraphs[0].paragraph_format.space_after = Pt(0)
        cells[1].paragraphs[0].paragraph_format.space_after = Pt(0)
        r0 = cells[0].paragraphs[0].add_run(str(lbl))
        r0.bold = True; r0.font.size = Pt(9); r0.font.color.rgb = C_DARK
        r1 = cells[1].paragraphs[0].add_run(str(val)[:300] if val else "—")
        r1.font.size = Pt(9); r1.font.color.rgb = C_MED

def _mod_status(doc, data, key):
    status = data.get(key,"respondido")
    lbl = MODULE_STATUS.get(status,"")
    if lbl:
        _para(doc, lbl, italic=True, color=C_GRAY, size=8, after=2)

def _ipr_table(doc):
    """Render IPR scale as a table."""
    _para(doc, "Escala IPR — Cómo interpretar los resultados:", bold=True, color=C_DARK, size=10)
    tbl = doc.add_table(rows=len(IPR_SCALE)+1, cols=3)
    tbl.style = "Table Grid"
    hdrs = ["Nivel","N° prácticas","¿Qué significa?"]
    for i, h in enumerate(hdrs):
        r = tbl.rows[0].cells[i].paragraphs[0].add_run(h)
        r.bold = True; r.font.size = Pt(8); r.font.color.rgb = C_DARK
        _shd(tbl.rows[0].cells[i], "D8F3DC")
    for i, (lvl, n, color, meaning) in enumerate(IPR_SCALE, 1):
        row = tbl.rows[i]
        for j, val in enumerate([lvl, n, meaning]):
            r = row.cells[j].paragraphs[0].add_run(val)
            r.font.size = Pt(8)
            _shd(row.cells[j], "F0FFF4" if i%2==0 else "FFFFFF")

def _load_petalos():
    jf = Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json"
    try:
        with open(jf, encoding="utf-8") as f:
            return json.load(f)["petalos"]
    except Exception:
        return []

def generate_docx(data: dict) -> bytes:
    if not DOCX_OK:
        raise ImportError("python-docx no instalado")

    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Cm(2.5); sec.bottom_margin = Cm(2.5)
        sec.left_margin = Cm(3.0); sec.right_margin = Cm(2.5)

    # ── PORTADA ───────────────────────────────────────────────────────────
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = p.add_run("🌿 INDAGACIÓN REGENERATIVA")
    rt.bold = True; rt.font.size = Pt(26); rt.font.color.rgb = C_DARK

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = p2.add_run("Diagnóstico de Permacultura Urbana — LivLin v2.2  ·  www.livlin.com")
    rs.font.size = Pt(12); rs.font.color.rgb = C_MED; rs.italic = True

    doc.add_paragraph()
    nombre = data.get("proyecto_nombre","Sin nombre")
    _kv(doc, [
        ("🏡 Espacio", nombre),
        ("👤 Contacto", data.get("proyecto_cliente","")),
        ("📍 Ciudad", data.get("proyecto_ciudad","")),
        ("📅 Fecha", data.get("proyecto_fecha","") or str(datetime.now())[:10]),
        ("Estado del diagnóstico", MODULE_STATUS.get(data.get("mod_cliente","respondido"),"")),
    ])
    doc.add_paragraph()
    doc.add_page_break()

    # ── QUÉ ES LIVLIN ─────────────────────────────────────────────────────
    _heading(doc, "Acerca de LivLin", 1, C_DARK, 14)
    _expl_box(doc, LIVLIN_DESC, size=10)
    _para(doc, "🔗 www.livlin.com", color=C_MAIN, size=10)
    doc.add_paragraph()

    _heading(doc, "Módulos del Diagnóstico", 2, C_MED, 11)
    for mod_name, mod_desc in LIVLIN_MODULES:
        _para(doc, mod_name, bold=True, color=C_DARK, size=10, after=2)
        _para(doc, mod_desc, italic=True, color=C_GRAY, size=9, after=6)
    doc.add_paragraph()
    doc.add_page_break()

    # ── ÍNDICE DE POTENCIAL REGENERATIVO ─────────────────────────────────
    _heading(doc, "Índice de Potencial Regenerativo (IPR)", 1, C_DARK, 14)
    _expl_box(doc, IPR_WHAT_IS, size=10)
    _expl_box(doc, IPR_OBS_VS_POT, size=9)
    doc.add_paragraph()
    _ipr_table(doc)
    doc.add_paragraph()

    # IPR summary per petal
    ipr_obs  = data.get("ipr_obs", [])
    ipr_new  = data.get("ipr_new", [])
    petalos  = _load_petalos()

    def _lv(n):
        for lvl, nr, _, _ in IPR_SCALE:
            lo, hi = (int(nr), int(nr)) if nr.isdigit() else (int(nr[0]), 99)
            if lo <= n <= hi: return lvl
        return IPR_SCALE[-1][0]

    if ipr_obs or ipr_new:
        _para(doc, "Resumen IPR por pétalo:", bold=True, color=C_DARK, size=10)
        rows = []
        for i, p in enumerate(petalos):
            n_o = ipr_obs[i] if i < len(ipr_obs) else 0
            n_n = ipr_new[i] if i < len(ipr_new) else 0
            icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
            rows.append((f"{icon} {p['nombre'][:35]}",
                         f"Observado: {n_o} → {_lv(n_o)}  |  +{n_n} potencial → {_lv(n_o+n_n)}"))
        _kv(doc, rows)
    doc.add_page_break()

    # ── M1 ────────────────────────────────────────────────────────────────
    _heading(doc, "1. Información del Proyecto y Tao", 1, C_DARK, 14)
    _mod_status(doc, data, "mod_cliente")
    _expl_box(doc, "El Tao de la Regeneración explora la motivación profunda del espacio y sus "
              "habitantes: el sueño regenerativo que guía el proceso de transformación.")
    rows = []
    for lbl, key in [
        ("Tipo de espacio","proyecto_tipo_espacio"),("Superficie (m²)","proyecto_superficie"),
        ("N° Habitantes","proyecto_habitantes"),("Barrio","proyecto_barrio_desc"),
    ]:
        v = data.get(key)
        if v: rows.append((lbl, str(v)))
    if rows: _kv(doc, rows)
    doc.add_paragraph()
    for k, lbl in [("proyecto_intencion","Intención del proyecto"),
                   ("tao_motivacion","Motivación"), ("tao_sueno","Sueño regenerativo")]:
        v = data.get(k,"")
        if v:
            _para(doc, f"{lbl}:", bold=True, color=C_DARK, size=10)
            _para(doc, v, italic=True, color=C_GRAY, size=10)
    doc.add_page_break()

    # ── M2-3 ──────────────────────────────────────────────────────────────
    _heading(doc, "2. Observación Ecológica del Sitio", 1, C_DARK, 14)
    _mod_status(doc, data, "mod_sitio")
    _expl_box(doc, "'Observar e interactuar' es el primer principio de Holmgren. "
              "La observación cuidadosa del sitio es la base de todo diseño en permacultura.")
    doc.add_paragraph()

    for section, fields in [
        ("Suelo", [("suelo_tipo","Tipo"),("suelo_compactacion","Compactación"),
                   ("suelo_materia_organica","Materia orgánica"),("suelo_drenaje","Drenaje"),
                   ("suelo_color","Color"),("suelo_olor","Olor"),("suelo_notas","Notas")]),
        ("Vegetación", [("veg_especies","Especies"),("veg_invasoras","Invasoras")]),
        ("Flujos Naturales", [("sol_horas","Horas sol/día"),("sol_orientacion","Orientación"),
                               ("clima_mes_caluroso","Mes más cálido"),("clima_mes_frio","Mes más frío"),
                               ("clima_t_max_abs","T° máx registrada"),("clima_t_min_abs","T° mín registrada"),
                               ("agua_prec_anual","Precipitación anual (mm)")]),
    ]:
        _heading(doc, section, 2, C_MED, 11)
        rows = [(lbl, str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc, rows)
        else: _para(doc, "— No registrado —", italic=True, color=C_GRAY, size=9)
    doc.add_page_break()

    # ── M4-6 ─────────────────────────────────────────────────────────────
    _heading(doc, "3. Sistemas — Agua, Energía y Materiales", 1, C_DARK, 14)
    _mod_status(doc, data, "mod_sistemas")
    _expl_box(doc, "Entender los flujos de agua, energía y materiales permite identificar "
              "dónde cerrar ciclos y reducir dependencias externas.")
    for section, fields in [
        ("💧 Agua", [("agua_consumo","Consumo diario (L)"),("agua_prec_anual","Precip. anual (mm)"),
                     ("agua_techo_m2","Techo captación (m²)"),("agua_riego_tipo","Tipo riego"),
                     ("agua_grises","Aguas grises")]),
        ("⚡ Energía", [("ene_kwh_mes","Consumo mensual (kWh)"),("ene_fuente_principal","Fuente principal"),
                        ("ene_solar_interes","Interés solar")]),
        ("♻️ Materiales", [("mat_compost","Compostaje"),("mat_reciclaje","Reciclaje"),
                            ("mat_plastico_uso","Reducción plástico")]),
    ]:
        _heading(doc, section, 2, C_MED, 11)
        rows = [(lbl, str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc, rows)
    doc.add_page_break()

    # ── M7 FLOR ───────────────────────────────────────────────────────────
    _heading(doc, "4. Flor de la Permacultura — IPR", 1, C_DARK, 14)
    _mod_status(doc, data, "mod_potencial")
    _expl_box(doc, IPR_WHAT_IS)
    _expl_box(doc, IPR_OBS_VS_POT)
    doc.add_paragraph()

    for i, petalo in enumerate(petalos):
        n_o  = ipr_obs[i] if i < len(ipr_obs) else 0
        n_n  = ipr_new[i] if i < len(ipr_new) else 0
        icon = PETAL_ICONS[i] if i < len(PETAL_ICONS) else "🌱"
        _heading(doc, f"{icon} {petalo['nombre']}", 2, C_MED, 11)

        # IPR scores
        p_score = doc.add_paragraph()
        p_score.paragraph_format.space_after = Pt(4)
        r1 = p_score.add_run(f"✅ Observado: {n_o} → {_lv(n_o)}  |  ")
        r1.font.size = Pt(9); r1.bold = True; r1.font.color.rgb = C_MAIN
        r2 = p_score.add_run(f"🌟 +{n_n} potencial → Total: {_lv(n_o+n_n)}")
        r2.font.size = Pt(9); r2.bold = True; r2.font.color.rgb = C_AMBER

        # Petal description
        desc = PETAL_DESC.get(petalo["nombre"], {})
        if isinstance(desc, dict):
            resumen = desc.get("resumen","")
            detalle = desc.get("detalle","")
            refs    = desc.get("referencias",[])
            if resumen: _expl_box(doc, resumen, size=9)
            if detalle: _para(doc, detalle, italic=True, color=C_GRAY, size=8, after=4)
            if refs:
                _para(doc, "📚 Referencias:", bold=True, color=C_DARK, size=8, after=1)
                for auth, tit, url in refs:
                    _para(doc, f"  {auth} — {tit} · {url}", italic=True, color=C_GRAY, size=8, after=1)

        # Actions
        obs_data  = data.get(f"petalo_{i}_obs",     {})
        new_data  = data.get(f"petalo_{i}_pot_new", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_new = data.get(f"petalo_{i}_otros_new", [])
        notas     = data.get(f"petalo_{i}_notas","")

        obs_rows = [(k.replace("_"," ").title(), " · ".join(v))
                    for k,v in obs_data.items() if v]
        if otros_obs: obs_rows.append(("Otros observados", " · ".join(otros_obs)))
        if obs_rows:
            _para(doc, "✅ Prácticas observadas:", bold=True, color=C_MAIN, size=9, after=2)
            _kv(doc, obs_rows)

        new_rows = [(k.replace("_"," ").title(), " · ".join(v))
                    for k,v in new_data.items() if v]
        if otros_new: new_rows.append(("Otros potencial", " · ".join(otros_new)))
        if new_rows:
            doc.add_paragraph()
            _para(doc, "🌟 Potencial adicional:", bold=True, color=C_AMBER, size=9, after=2)
            _kv(doc, new_rows)

        if notas:
            _para(doc, f"📝 Notas: {notas}", italic=True, color=C_GRAY, size=9)
        doc.add_paragraph()

    dest = data.get("pot_practicas_destacadas","")
    if dest:
        _heading(doc, "✨ Prácticas más destacadas del espacio", 2, C_MED, 11)
        _para(doc, dest, italic=True, color=C_GRAY, size=10)
    doc.add_page_break()

    # ── M9 ────────────────────────────────────────────────────────────────
    _heading(doc, "5. Síntesis y Plan de Acción", 1, C_DARK, 14)
    _mod_status(doc, data, "mod_plan")
    _expl_box(doc, "El plan de acción organiza los próximos pasos en 3 horizontes temporales: "
              "inmediato (0-3 meses), estacional (3-12 meses) y estructural (1-5 años). "
              "Cada horizonte tiene una lógica diferente: velocidad, escala y tipo de recursos.")
    for k, lbl in [("sint_fortalezas","💚 Fortalezas"),("sint_desafios","⚡ Desafíos"),
                   ("sint_oportunidades","🌱 Oportunidades"),("sint_narrativa","📖 Narrativa")]:
        v = data.get(k,"")
        if v:
            _para(doc, lbl, bold=True, color=C_DARK, size=10)
            _para(doc, v, italic=True, color=C_GRAY, size=10)
    doc.add_paragraph()
    for pk, fase in [
        ("plan_inmediatas","⚡ Acciones Inmediatas (0–3 meses)"),
        ("plan_estacionales","🌿 Acciones Estacionales (3–12 meses)"),
        ("plan_estructurales","🌳 Transformaciones Estructurales (1–5 años)"),
    ]:
        v = data.get(pk)
        if v:
            _para(doc, fase, bold=True, color=C_MED, size=10)
            if isinstance(v, list):
                for item in v:
                    txt = item.get("titulo","") if isinstance(item,dict) else str(item)
                    if txt:
                        p = doc.add_paragraph(style="List Bullet")
                        p.paragraph_format.space_after = Pt(2)
                        p.add_run(txt).font.size = Pt(9)
            else:
                _para(doc, str(v), italic=True, color=C_GRAY, size=9)
    doc.add_page_break()

    # ── REFERENCIAS ───────────────────────────────────────────────────────
    _heading(doc, "Referencias y Recursos", 1, C_DARK, 14)
    _para(doc, "Las siguientes fuentes sustentan la metodología del diagnóstico:", size=10)
    doc.add_paragraph()
    for auth, tit, url in GLOBAL_REFS:
        _para(doc, f"• {auth} — {tit}", bold=False, color=C_DARK, size=9, after=2)
        _para(doc, f"  🔗 {url}", italic=True, color=C_MAIN, size=8, after=4)

    # ── PIE ───────────────────────────────────────────────────────────────
    doc.add_page_break()
    p_pie = doc.add_paragraph()
    p_pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pie = p_pie.add_run(
        f"Diagnóstico generado con LivLin — Indagación Regenerativa v2.2  ·  "
        f"{str(datetime.now())[:10]}")
    r_pie.font.size = Pt(8); r_pie.font.color.rgb = C_GRAY; r_pie.italic = True
    p_w = doc.add_paragraph()
    p_w.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rw = p_w.add_run("🌿 LivLin · Permacultura Urbana · www.livlin.com")
    rw.font.size = Pt(10); rw.font.color.rgb = C_MAIN; rw.bold = True

    buf = io.BytesIO()
    doc.save(buf); buf.seek(0)
    return buf.read()
