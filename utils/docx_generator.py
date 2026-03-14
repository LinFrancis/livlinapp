"""Generador Word v4.2 — LivLin Indagación Regenerativa.
Narrativa regenerativa alineada con Mason (2025). Logo embebido.
"""
import io, base64, json, tempfile
from datetime import datetime
from pathlib import Path
from utils.petal_content import (
    PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS, IPR_OBS_VS_POT,
    LIVLIN_URL, LIVLIN_TAGLINE, LIVLIN_DESC, LIVLIN_MODULES,
    LIVLIN_SERVICES_PITCH, LIVLIN_CLOSING, REGENERATION_FRAMEWORK, GLOBAL_REFS,
    TAO_REFLEXION_SHORT, TAO_INVITACION
)

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

C1 = RGBColor(0x00,0x59,0x54) if DOCX_OK else None  # #005954
C2 = RGBColor(0x33,0x8B,0x85) if DOCX_OK else None  # #338B85
C3 = RGBColor(0x5D,0xC1,0xB9) if DOCX_OK else None  # #5DC1B9
CA = RGBColor(0x2D,0x6A,0x4F) if DOCX_OK else None  # amber
CG = RGBColor(0x44,0x44,0x44) if DOCX_OK else None  # gray

MODULE_STATUS = {
    "respondido":  "✅ Respondido directamente por las personas del espacio",
    "inferido":    "🔍 Inferido por el facilitador tras la visita",
    "no_abordado": "⭕ Módulo no abordado en esta visita",
}

def _shd(cell, hex_color):
    tc=cell._tc; tcPr=tc.get_or_add_tcPr()
    shd=OxmlElement("w:shd"); shd.set(qn("w:val"),"clear")
    shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),hex_color); tcPr.append(shd)

def _H(doc,text,level=1,color=None,size=None):
    p=doc.add_heading(text,level=level)
    r=p.runs[0] if p.runs else p.add_run(text)
    if color: r.font.color.rgb=color
    if size: r.font.size=Pt(size)
    return p

def _p(doc,text,bold=False,color=None,size=10,italic=False,after=4):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(after)
    r=p.add_run(text); r.bold=bold; r.italic=italic; r.font.size=Pt(size)
    if color: r.font.color.rgb=color
    return p

def _box(doc,text,size=9,color=None):
    p=doc.add_paragraph()
    p.paragraph_format.space_before=Pt(3); p.paragraph_format.space_after=Pt(6)
    p.paragraph_format.left_indent=Cm(0.5)
    r=p.add_run(text); r.font.size=Pt(size); r.italic=True
    r.font.color.rgb=color or CA

def _kv(doc,rows):
    if not rows: return
    tbl=doc.add_table(rows=len(rows),cols=2); tbl.style="Table Grid"
    for i,(lbl,val) in enumerate(rows):
        cells=tbl.rows[i].cells
        _shd(cells[0],"D5FFFF"); _shd(cells[1],"FFFFFF")
        cells[0].paragraphs[0].paragraph_format.space_after=Pt(0)
        cells[1].paragraphs[0].paragraph_format.space_after=Pt(0)
        r0=cells[0].paragraphs[0].add_run(str(lbl))
        r0.bold=True; r0.font.size=Pt(9); r0.font.color.rgb=C1
        r1=cells[1].paragraphs[0].add_run(str(val)[:300] if val else "—")
        r1.font.size=Pt(9); r1.font.color.rgb=C2

def _ipr_table(doc):
    _p(doc,"Escala de niveles IPR — cómo interpretar los resultados:",bold=True,color=C1,size=10)
    tbl=doc.add_table(rows=len(IPR_SCALE)+1,cols=3); tbl.style="Table Grid"
    for i,h in enumerate(["Nivel","N° prácticas","¿Qué significa?"]):
        r=tbl.rows[0].cells[i].paragraphs[0].add_run(h)
        r.bold=True; r.font.size=Pt(8); r.font.color.rgb=C1
        _shd(tbl.rows[0].cells[i],"D5FFFF")
    for i,(lvl,n,_,meaning) in enumerate(IPR_SCALE,1):
        for j,val in enumerate([lvl,n,meaning]):
            r=tbl.rows[i].cells[j].paragraphs[0].add_run(val)
            r.font.size=Pt(8)
            _shd(tbl.rows[i].cells[j],"F0FFFE" if i%2==0 else "FFFFFF")

def _logo(doc, width_inches=1.5):
    """Add logo to document. Uses /tmp/livlin_logo.png for cloud compatibility."""
    try:
        from utils.logo_b64 import LOGO_B64
        import os
        tmp_path = "/tmp/livlin_logo.png"
        if not os.path.exists(tmp_path):
            logo_bytes = base64.b64decode(LOGO_B64)
            with open(tmp_path, "wb") as f_tmp:
                f_tmp.write(logo_bytes)
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(); r.add_picture(tmp_path, width=Inches(width_inches))
        return True
    except Exception as e:
        print(f"[logo docx] {e}")
        # Fallback: text logo
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run("🌿 LivLin"); r.bold = True; r.font.size = Pt(18)
        if C1: r.font.color.rgb = C1
        return False

def _mod_status(doc,data,key):
    status=data.get(key,"respondido")
    lbl=MODULE_STATUS.get(status,"")
    if lbl: _p(doc,lbl,italic=True,color=CG,size=8,after=2)

def _load_petalos():
    jf=Path(__file__).parent.parent/"data"/"petalos_regeneracion_urbana.json"
    try:
        with open(jf,encoding="utf-8") as f: return json.load(f)["petalos"]
    except: return []

def _score_lv(n):
    for lvl,nr,_,_ in IPR_SCALE:
        try:
            lo,hi=(int(nr),int(nr)) if nr.isdigit() else (int(nr[0]),99)
            if lo<=n<=hi: return lvl
        except: pass
    return IPR_SCALE[-1][0]


def generate_docx(data:dict)->bytes:
    if not DOCX_OK:
        raise ImportError("python-docx no instalado. Agrega 'python-docx>=1.1.0' a requirements.txt")

    doc=Document()
    for sec in doc.sections:
        sec.top_margin=Cm(2.5); sec.bottom_margin=Cm(2.5)
        sec.left_margin=Cm(3.0); sec.right_margin=Cm(2.5)

    petalos=_load_petalos()
    facilitador=data.get("proyecto_facilitador","")
    ipr_obs=data.get("ipr_obs",[])
    ipr_new=data.get("ipr_new",[])

    # ── PORTADA ───────────────────────────────────────────────────────────
    doc.add_paragraph()
    _logo(doc)
    doc.add_paragraph()

    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rt=p.add_run("INDAGACIÓN REGENERATIVA")
    rt.bold=True; rt.font.size=Pt(24); rt.font.color.rgb=C1

    p2=doc.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rs=p2.add_run("Diagnóstico de Permacultura Urbana"); rs.font.size=Pt(12); rs.font.color.rgb=C2

    p3=doc.add_paragraph(); p3.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rt2=p3.add_run(f"LivLin v4.2  ·  {LIVLIN_TAGLINE}  ·  www.livlin.cl")
    rt2.font.size=Pt(10); rt2.font.color.rgb=C3; rt2.italic=True

    doc.add_paragraph()
    rows=[
        ("🏡 Espacio",data.get("proyecto_nombre","")),
        ("👤 Contacto",data.get("proyecto_cliente","")),
        ("📍 Ciudad",data.get("proyecto_ciudad","")),
        ("📅 Fecha visita",data.get("proyecto_fecha","") or str(datetime.now())[:10]),
    ]
    if facilitador: rows.append(("🌿 Facilitador/a",facilitador))
    if data.get("informe_fecha_emision"):
        rows.append(("📋 Fecha emisión",data["informe_fecha_emision"]))
    _kv(doc,rows)
    doc.add_paragraph()
    doc.add_page_break()

    # ── MARCO CONCEPTUAL ─────────────────────────────────────────────────
    _H(doc,"Marco conceptual: el enfoque de la regeneración",1,C1,14)
    _box(doc,REGENERATION_FRAMEWORK,size=10,color=C2)
    doc.add_paragraph()
    _H(doc,"¿Qué es LivLin?",2,C2,11)
    _box(doc,LIVLIN_DESC,size=10,color=CG)
    _p(doc,"🔗 www.livlin.cl · Potencial para una vida regenerativa",color=C3,size=9)
    doc.add_paragraph()
    _H(doc,"Módulos del Diagnóstico",2,C2,11)
    for mod,desc in LIVLIN_MODULES:
        _p(doc,mod,bold=True,color=C1,size=10,after=2)
        _p(doc,desc,italic=True,color=CG,size=9,after=6)
    doc.add_page_break()

    # ── IPR ───────────────────────────────────────────────────────────────
    _H(doc,"Índice de Potencial Regenerativo (IPR)",1,C1,14)
    _box(doc,IPR_WHAT_IS,size=10,color=C2)
    _box(doc,IPR_OBS_VS_POT,size=9,color=CG)
    doc.add_paragraph()
    _ipr_table(doc)
    doc.add_paragraph()

    # Add radar chart if available
    radar_b64 = data.get("ipr_radar_b64","")
    if radar_b64:
        try:
            import base64 as _b64
            img_bytes = _b64.b64decode(radar_b64)
            tmp_radar = "/tmp/livlin_radar.png"
            with open(tmp_radar,"wb") as _fh: _fh.write(img_bytes)
            p_r = doc.add_paragraph(); p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_r.add_run().add_picture(tmp_radar, width=Inches(5.5))
            _p(doc,"Verde sólido = Observado hoy · Verde punteado = Con potencial adicional. "
               "Escala normalizada al máximo de prácticas registradas.",
               italic=True, color=CG, size=8)
        except Exception as e:
            _p(doc,f"[Gráfico no disponible: {e}]",italic=True,color=CG,size=8)

    if ipr_obs or ipr_new:
        _p(doc,"Resumen IPR por pétalo:",bold=True,color=C1,size=10)
        rows=[]
        for i,p in enumerate(petalos):
            n_o=ipr_obs[i] if i<len(ipr_obs) else 0
            n_n=ipr_new[i] if i<len(ipr_new) else 0
            icon=PETAL_ICONS[i] if i<len(PETAL_ICONS) else "🌱"
            rows.append((f"{icon} {p['nombre'][:35]}",
                         f"✅ {n_o} — {_score_lv(n_o)}  |  🌟 +{n_n} → {_score_lv(n_o+n_n)}"))
        _kv(doc,rows)
    doc.add_page_break()

    # ── M1 ────────────────────────────────────────────────────────────────
    _H(doc,"1. Intención y Contexto",1,C1,14)
    _mod_status(doc,data,"mod_cliente")
    _box(doc,"'Cada día tenemos una oportunidad de vivir el tránsito hacia una mejor forma de vivir.' "
         "— Mason (2025). Este módulo registra el horizonte de sentido que guiará el proceso.",color=C2)
    rows=[]
    for lbl,key in [("Tipo de espacio","proyecto_tipo_espacio"),("Superficie (m²)","proyecto_superficie"),
                    ("Habitantes","proyecto_habitantes"),("Barrio","proyecto_barrio_desc")]:
        v=data.get(key)
        if v: rows.append((lbl,str(v)))
    if rows: _kv(doc,rows)
    doc.add_paragraph()
    for k,lbl in [("proyecto_intencion","Intención"),("tao_motivacion","Motivación"),
                  ("tao_sueno","Sueño regenerativo")]:
        v=data.get(k,"")
        if v:
            _p(doc,f"{lbl}:",bold=True,color=C1,size=10)
            _p(doc,v,italic=True,color=CG,size=10)
    doc.add_page_break()

    # ── M2-3 ─────────────────────────────────────────────────────────────
    _H(doc,"2. Observación Ecológica del Sitio",1,C1,14)
    _mod_status(doc,data,"mod_sitio")
    _box(doc,"'Observar e interactuar' — primer principio de Holmgren (2002). Antes de diseñar, se lee el lugar: "
         "su suelo, agua, sol, viento y biodiversidad son el texto del que emerge el diseño regenerativo.",color=C2)
    for section,fields in [
        ("Suelo",[("suelo_tipo","Tipo"),("suelo_compactacion","Compactación"),
                  ("suelo_materia_organica","Materia org."),("suelo_drenaje","Drenaje"),
                  ("suelo_color","Color"),("suelo_notas","Notas")]),
        ("Flujos Naturales",[("sol_horas","Horas sol (estimado/medido)"),("sol_orientacion","Orientación"),
                              ("clima_mes_caluroso","Mes cálido [Open-Meteo API]"),
                              ("clima_mes_frio","Mes frío [Open-Meteo API]"),
                              ("clima_t_max_abs","T° máx [Open-Meteo API]"),
                              ("clima_t_min_abs","T° mín [Open-Meteo API]"),
                              ("agua_prec_anual","Precipitación anual mm [Open-Meteo API]")]),
        ("Vegetación",[("veg_especies","Especies"),("veg_invasoras","Invasoras")]),
    ]:
        _H(doc,section,2,C2,11)
        rows=[(lbl,str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc,rows)
        else: _p(doc,"— No registrado —",italic=True,color=CG,size=9)
    doc.add_page_break()

    # ── M4-6 ─────────────────────────────────────────────────────────────
    _H(doc,"3. Sistemas — Agua, Energía y Materiales",1,C1,14)
    _mod_status(doc,data,"mod_sistemas")
    _box(doc,"Cerrar ciclos es regenerar: agua que se capta, energía que se genera, residuos que se "
         "convierten en recursos. Cada flujo mapeado es una oportunidad de autonomía.",color=C2)
    for section,fields in [
        ("💧 Agua",[("agua_consumo","Consumo (L/día)"),("agua_prec_anual","Precip. anual (mm)"),
                    ("agua_techo_m2","Techo captación (m²)"),("agua_riego_tipo","Riego"),("agua_grises","Aguas grises")]),
        ("⚡ Energía",[("ene_kwh_mes","Consumo (kWh/mes)"),("ene_fuente_principal","Fuente"),
                       ("ene_solar_interes","Interés solar")]),
        ("♻️ Materiales",[("mat_compost","Compostaje"),("mat_reciclaje","Reciclaje"),
                          ("mat_plastico_uso","Reducción plástico")]),
    ]:
        _H(doc,section,2,C2,11)
        rows=[(lbl,str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc,rows)
    doc.add_page_break()

    # ── M7 FLOR ───────────────────────────────────────────────────────────
    _H(doc,"4. Flor de la Permacultura — Índice de Potencial Regenerativo (IPR)",1,C1,14)
    _mod_status(doc,data,"mod_potencial")
    _box(doc,IPR_WHAT_IS,color=C2)
    _box(doc,IPR_OBS_VS_POT,color=CG)
    doc.add_paragraph()

    for i,petalo in enumerate(petalos):
        n_o=ipr_obs[i] if i<len(ipr_obs) else 0
        n_n=ipr_new[i] if i<len(ipr_new) else 0
        icon=PETAL_ICONS[i] if i<len(PETAL_ICONS) else "🌱"
        _H(doc,f"{icon} {petalo['nombre']}",2,C2,11)

        p_sc=doc.add_paragraph(); p_sc.paragraph_format.space_after=Pt(4)
        r1=p_sc.add_run(f"✅ Observado: {n_o} → {_score_lv(n_o)}   |   ")
        r1.font.size=Pt(9); r1.bold=True; r1.font.color.rgb=C1
        r2=p_sc.add_run(f"🌟 +{n_n} potencial → Total: {_score_lv(n_o+n_n)}")
        r2.font.size=Pt(9); r2.bold=True; r2.font.color.rgb=CA

        desc=PETAL_DESC.get(petalo["nombre"],{})
        if isinstance(desc,dict):
            if desc.get("resumen"): _box(doc,desc["resumen"],size=9,color=C2)
            if desc.get("detalle"): _p(doc,desc["detalle"],italic=True,color=CG,size=8,after=4)
            for auth,tit,url in desc.get("referencias",[]):
                _p(doc,f"📚 {auth} — {tit} · {url}",italic=True,color=CG,size=7,after=1)

        obs_data=data.get(f"petalo_{i}_obs",{})
        new_data=data.get(f"petalo_{i}_pot_new",{})
        otros_obs=data.get(f"petalo_{i}_otros_obs",[])
        otros_new=data.get(f"petalo_{i}_otros_new",[])
        notas=data.get(f"petalo_{i}_notas","")

        obs_rows=[(k.replace("_"," ").title()," · ".join(v))
                   for k,v in obs_data.items() if v]
        if otros_obs: obs_rows.append(("Otras prácticas observadas"," · ".join(otros_obs)))
        if obs_rows:
            _p(doc,"✅ Prácticas observadas hoy:",bold=True,color=C1,size=9,after=2)
            _kv(doc,obs_rows)

        new_rows=[(k.replace("_"," ").title()," · ".join(v))
                   for k,v in new_data.items() if v]
        if otros_new: new_rows.append(("Otras prácticas (potencial)"," · ".join(otros_new)))
        if new_rows:
            doc.add_paragraph()
            _p(doc,"🌟 Potencial adicional identificado por el facilitador:",bold=True,color=CA,size=9,after=2)
            _kv(doc,new_rows)

        if notas: _p(doc,f"📝 Notas: {notas}",italic=True,color=CG,size=9)
        doc.add_paragraph()

    dest=data.get("pot_practicas_destacadas","")
    if dest:
        _H(doc,"✨ Prácticas más destacadas del espacio",2,C2,11)
        _p(doc,dest,italic=True,color=CG,size=10)
    doc.add_page_break()

    # ── M9 ────────────────────────────────────────────────────────────────
    _H(doc,"5. Síntesis y Plan de Acción",1,C1,14)
    _mod_status(doc,data,"mod_plan")
    _box(doc,"La hoja de ruta del descenso creativo organiza los próximos pasos en 3 horizontes: "
         "acciones cotidianas inmediatas, cambios estacionales y transformaciones estructurales "
         "que construyen resiliencia para las generaciones futuras. — Mason (2025)",color=C2)
    for k,lbl in [("sint_fortalezas","💚 Fortalezas — lo que ya florece"),
                   ("sint_desafios","⚡ Desafíos — obstáculos reales"),
                   ("sint_oportunidades","🌱 Oportunidades — potencial por activar")]:
        v=data.get(k,"")
        if v: _p(doc,f"{lbl}: {v}",color=CG,size=10)
    doc.add_paragraph()
    for pk,fase in [("plan_inmediatas","⚡ Acciones Inmediatas (0–3 meses)"),
                    ("plan_estacionales","🌿 Acciones Estacionales (3–12 meses)"),
                    ("plan_estructurales","🌳 Transformaciones Estructurales (1–5 años)")]:
        v=data.get(pk)
        if v:
            _p(doc,fase,bold=True,color=C2,size=10)
            if isinstance(v,list):
                for item in v:
                    txt=item.get("titulo","") if isinstance(item,dict) else str(item)
                    if txt:
                        p=doc.add_paragraph(style="List Bullet")
                        p.paragraph_format.space_after=Pt(2)
                        p.add_run(txt).font.size=Pt(9)
            else:
                _p(doc,str(v),italic=True,color=CG,size=9)
    doc.add_page_break()

    # ── LIVLIN SERVICES ───────────────────────────────────────────────────
    _H(doc,"LivLin — Acompañamiento para hacer realidad este potencial",1,C1,14)
    _logo(doc)
    doc.add_paragraph()
    _box(doc,LIVLIN_SERVICES_PITCH,size=11,color=C1)
    doc.add_paragraph()
    _box(doc,LIVLIN_CLOSING,size=10,color=C2)
    doc.add_paragraph()
    p_w=doc.add_paragraph(); p_w.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rw=p_w.add_run(f"🌿 {LIVLIN_TAGLINE}  ·  www.livlin.cl")
    rw.font.size=Pt(11); rw.font.color.rgb=C1; rw.bold=True
    doc.add_page_break()

    # ── REFERENCIAS ───────────────────────────────────────────────────────
    _H(doc,"Referencias y Recursos de Profundización",1,C1,14)
    _p(doc,"Los siguientes materiales amplían el marco conceptual de este diagnóstico:",size=10)
    doc.add_paragraph()
    for auth,tit,url in GLOBAL_REFS:
        _p(doc,f"• {auth} — {tit}",bold=False,color=C1,size=9,after=2)
        _p(doc,f"  🔗 {url}",italic=True,color=C3,size=8,after=4)

    # ── PIE ───────────────────────────────────────────────────────────────
    p_pie=doc.add_paragraph(); p_pie.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r_pie=p_pie.add_run(f"LivLin Indagación Regenerativa v4.2  ·  {str(datetime.now())[:10]}")
    r_pie.font.size=Pt(8); r_pie.font.color.rgb=CG; r_pie.italic=True

    buf=io.BytesIO(); doc.save(buf); buf.seek(0)
    return buf.read()
