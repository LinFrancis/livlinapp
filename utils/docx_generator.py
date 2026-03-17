"""Generador Word v7.0 — LivLin · ERP/HRP, escala 0-10."""
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

C1 = RGBColor(0x00,0x59,0x54) if DOCX_OK else None
C2 = RGBColor(0x33,0x8B,0x85) if DOCX_OK else None
C3 = RGBColor(0x5D,0xC1,0xB9) if DOCX_OK else None
CA = RGBColor(0x2D,0x6A,0x4F) if DOCX_OK else None
CG = RGBColor(0x44,0x44,0x44) if DOCX_OK else None

MODULE_STATUS = {
    "respondido":  "✅ Respondido directamente",
    "inferido":    "🔍 Inferido por el facilitador",
    "no_abordado": "⭕ No abordado",
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

def _logo(doc, width_inches=1.5):
    try:
        from utils.logo_b64 import LOGO_B64
        import os
        tmp_path = "/tmp/livlin_logo.png"
        if not os.path.exists(tmp_path):
            logo_bytes = base64.b64decode(LOGO_B64)
            with open(tmp_path, "wb") as f_tmp: f_tmp.write(logo_bytes)
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(); r.add_picture(tmp_path, width=Inches(width_inches))
        return True
    except Exception:
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

def generate_docx(data:dict)->bytes:
    if not DOCX_OK:
        raise ImportError("python-docx no instalado.")

    doc=Document()
    for sec in doc.sections:
        sec.top_margin=Cm(2.5); sec.bottom_margin=Cm(2.5)
        sec.left_margin=Cm(3.0); sec.right_margin=Cm(2.5)

    petalos=_load_petalos()
    facilitador=data.get("proyecto_facilitador","")
    ipr_obs=data.get("ipr_obs",[])
    ipr_new=data.get("ipr_new",[])

    # Compute ERP/HRP
    from utils.scoring import (compute_erp, compute_hrp, compute_domain_scores,
        compute_domain_scores_total, compute_cross_module_score, CROSS_MODULE_DETAIL,
        score_label, brecha_valor, brecha_texto, _score_to_level, get_petal_interp,
        compute_synthesis_potentials, compute_synthesis_potentials_obs, get_interp_text)
    erp = compute_erp(data)
    hrp = compute_hrp(data)
    brecha = brecha_valor(erp, hrp)
    brecha_txt = brecha_texto(erp, hrp)
    label_erp, _ = score_label(erp)
    label_hrp, _ = score_label(hrp)
    domain_obs = compute_domain_scores(data)
    domain_tot = compute_domain_scores_total(data)
    cross = compute_cross_module_score(data)

    # ── PORTADA ──
    doc.add_paragraph()
    _logo(doc)
    doc.add_paragraph()
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rt=p.add_run("INDAGACIÓN REGENERATIVA"); rt.bold=True; rt.font.size=Pt(24); rt.font.color.rgb=C1
    p2=doc.add_paragraph(); p2.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rs=p2.add_run("Diagnóstico de Permacultura Urbana"); rs.font.size=Pt(12); rs.font.color.rgb=C2
    p3=doc.add_paragraph(); p3.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rt2=p3.add_run(f"LivLin v7.0 · {LIVLIN_TAGLINE} · www.livlin.cl")
    rt2.font.size=Pt(10); rt2.font.color.rgb=C3; rt2.italic=True
    doc.add_paragraph()

    rows=[("🏡 Espacio",data.get("proyecto_nombre","")),
          ("👤 Contacto",data.get("proyecto_cliente","")),
          ("📍 Ciudad",data.get("proyecto_ciudad","")),
          ("📅 Fecha",data.get("proyecto_fecha","") or str(datetime.now())[:10])]
    if data.get("proyecto_mascotas"):
        rows.append(("🐾 Mascotas", data["proyecto_mascotas"]))
    if facilitador: rows.append(("🌿 Facilitador/a",facilitador))
    _kv(doc,rows)
    doc.add_paragraph()

    # ERP / HRP Summary
    _H(doc,"Estado Regenerativo Presente (ERP) y Horizonte Regenerativo Potencial (HRP)",2,C1,12)
    _kv(doc,[
        ("🌍 ERP", f"{erp}/10 — {label_erp}"),
        ("🌱 HRP", f"{hrp}/10 — {label_hrp}"),
        ("🌀 Brecha", f"{brecha} pts — {brecha_txt}"),
    ])
    doc.add_paragraph()
    _box(doc,IPR_WHAT_IS,color=C2)
    _box(doc,IPR_OBS_VS_POT,color=CG)
    doc.add_page_break()

    # ── MARCO CONCEPTUAL ──
    _H(doc,"Marco conceptual: el enfoque de la regeneración",1,C1,14)
    _box(doc,REGENERATION_FRAMEWORK,color=C2)
    _box(doc,LIVLIN_DESC,color=CG)
    doc.add_page_break()

    # ── M1 ──
    _H(doc,"1. Información del Proyecto e Intención",1,C1,14)
    _mod_status(doc,data,"mod_cliente")
    rows=[]
    for lbl,key in [("Tipo","proyecto_tipo_espacio"),("Superficie (m²)","proyecto_superficie"),
                    ("Habitantes","proyecto_habitantes"),("Mascotas","proyecto_mascotas")]:
        v=data.get(key)
        if v: rows.append((lbl,str(v)))
    if rows: _kv(doc,rows)
    doc.add_paragraph()
    for k,lbl in [("intencion_motivo","Motivo"),("intencion_vision5","Visión 5 años"),
                  ("intencion_suenos","Sueños regenerativos")]:
        v=data.get(k,"")
        if v:
            _p(doc,f"{lbl}:",bold=True,color=C1,size=10)
            _p(doc,v,italic=True,color=CG,size=10)
    doc.add_page_break()

    # ── M2-3 ──
    _H(doc,"2. Observación Ecológica del Sitio",1,C1,14)
    _mod_status(doc,data,"mod_sitio")
    for section,fields in [
        ("Suelo",[("suelo_tipo","Tipo"),("suelo_compactacion","Compactación"),
                  ("suelo_materia_organica","Materia org."),("suelo_drenaje","Drenaje")]),
        ("Flujos",[("sol_horas","Horas sol"),("sol_orientacion","Orientación"),
                   ("agua_prec_anual","Precipitación mm")]),
    ]:
        _H(doc,section,2,C2,11)
        rows=[(lbl,str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc,rows)
    doc.add_page_break()

    # ── M4-6 ──
    _H(doc,"3. Sistemas — Agua, Energía y Contexto",1,C1,14)
    _mod_status(doc,data,"mod_sistemas")
    for section,fields in [
        ("💧 Agua",[("agua_consumo","Consumo L/día"),("agua_captacion_lluvia","Captación"),("agua_grises","Grises")]),
        ("⚡ Energía",[("ene_fuente","Fuente"),("ene_led","LED"),("ene_kwh_dia_calc","kWh/día")]),
    ]:
        _H(doc,section,2,C2,11)
        rows=[(lbl,str(data.get(k,""))) for k,lbl in fields if data.get(k)]
        if rows: _kv(doc,rows)
    doc.add_page_break()

    # ── M7 FLOR ──
    _H(doc,"4. Flor de la Permacultura — ERP / HRP",1,C1,14)
    _mod_status(doc,data,"mod_potencial")
    _box(doc,IPR_WHAT_IS,color=C2)
    doc.add_paragraph()

    from utils.scoring import PETAL_ORDER
    for i,petalo in enumerate(petalos):
        n_o=ipr_obs[i] if i<len(ipr_obs) else 0
        n_n=ipr_new[i] if i<len(ipr_new) else 0
        icon=PETAL_ICONS[i] if i<len(PETAL_ICONS) else "🌱"
        p_name = petalo["nombre"]
        e_score = domain_obs.get(p_name,0)
        h_score = domain_tot.get(p_name,0)
        lv_e,_=_score_to_level(e_score)
        lv_h,_=_score_to_level(h_score)

        _H(doc,f"{icon} {p_name}",2,C2,11)
        p_sc=doc.add_paragraph(); p_sc.paragraph_format.space_after=Pt(4)
        r1=p_sc.add_run(f"🌍 ERP: {e_score:.0f}/10 ({lv_e})   |   ")
        r1.font.size=Pt(9); r1.bold=True; r1.font.color.rgb=C1
        r2=p_sc.add_run(f"🌱 HRP: {h_score:.0f}/10 ({lv_h})")
        r2.font.size=Pt(9); r2.bold=True; r2.font.color.rgb=CA

        # Interpretations
        interp_e = get_petal_interp(p_name, e_score, "erp")
        interp_h = get_petal_interp(p_name, h_score, "hrp")
        if interp_e: _box(doc,f"ERP: {interp_e}",size=9,color=C1)
        if interp_h: _box(doc,f"HRP: {interp_h}",size=9,color=CA)

        obs_data=data.get(f"petalo_{i}_obs",{})
        new_data=data.get(f"petalo_{i}_pot_new",{})
        otros_obs=data.get(f"petalo_{i}_otros_obs",[])
        otros_new=data.get(f"petalo_{i}_otros_new",[])
        obs_rows=[(k.replace("_"," ").title()," · ".join(v)) for k,v in obs_data.items() if v]
        if otros_obs: obs_rows.append(("Otras"," · ".join(otros_obs)))
        if obs_rows:
            _p(doc,"Prácticas observadas (ERP):",bold=True,color=C1,size=9,after=2)
            _kv(doc,obs_rows)
        new_rows=[(k.replace("_"," ").title()," · ".join(v)) for k,v in new_data.items() if v]
        if otros_new: new_rows.append(("Otras"," · ".join(otros_new)))
        if new_rows:
            doc.add_paragraph()
            _p(doc,"Prácticas potenciales (→ HRP):",bold=True,color=CA,size=9,after=2)
            _kv(doc,new_rows)
        doc.add_paragraph()

    # Sub-indicadores transparency
    if cross:
        _H(doc,"Sub-indicadores M2-6 (aportan 20% al ERP)",2,C2,11)
        rows = [(name, f"{info['score']}/10 — {info['fuente']}") for name,info in cross.items()]
        _kv(doc,rows)
        doc.add_paragraph()
        _p(doc,"Transparencia: variables y escalas de puntuación",bold=True,color=C1,size=10)
        for name, detail in CROSS_MODULE_DETAIL.items():
            actual = cross.get(name,{}).get("score","—")
            _p(doc,f"{detail.get('icono','')} {name}: {actual}/10 · {detail['formula']}",bold=True,color=C2,size=9)
            for vn,vs in detail["variables"]:
                _p(doc,f"  • {vn}: {vs}",color=CG,size=8,after=1)
    doc.add_page_break()

    # ── M9 ──
    _H(doc,"5. Síntesis y Plan de Acción",1,C1,14)
    for k,lbl in [("sint_fortalezas","💚 Fortalezas"),("sint_oportunidades","🌱 Oportunidades"),
                   ("sint_limitaciones","⚡ Desafíos"),("sint_quick_wins","🎯 Primeros pasos")]:
        v=data.get(k,"")
        if v: _p(doc,f"{lbl}: {v}",color=CG,size=10)
    doc.add_paragraph()
    for pk,fase in [("plan_inmediatas","⚡ Inmediatas (0–3 meses)"),
                    ("plan_estacionales","🌿 Estacionales (3–12 meses)"),
                    ("plan_estructurales","🌳 Estructurales (1–5 años)")]:
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

    # ── CIERRE ──
    _H(doc,"LivLin — Tu aliado en la regeneración",1,C1,14)
    _logo(doc)
    _box(doc,LIVLIN_SERVICES_PITCH,size=11,color=C1)
    doc.add_paragraph()
    _box(doc,"Hoy, el espacio muestra un Estado Regenerativo Presente (ERP) que refleja su vitalidad actual. "
         "Al mismo tiempo, identificamos un Horizonte Regenerativo Potencial (HRP) que abre posibilidades. "
         "La diferencia entre ambos nos señala el camino.",size=10,color=C2)
    doc.add_paragraph()
    p_w=doc.add_paragraph(); p_w.alignment=WD_ALIGN_PARAGRAPH.CENTER
    rw=p_w.add_run(f"🌿 {LIVLIN_TAGLINE} · www.livlin.cl")
    rw.font.size=Pt(11); rw.font.color.rgb=C1; rw.bold=True
    doc.add_page_break()

    # ── REFERENCIAS ──
    _H(doc,"Referencias y Recursos",1,C1,14)
    for auth,tit,url in GLOBAL_REFS:
        _p(doc,f"• {auth} — {tit}",bold=False,color=C1,size=9,after=2)
        _p(doc,f"  🔗 {url}",italic=True,color=C3,size=8,after=4)

    p_pie=doc.add_paragraph(); p_pie.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r_pie=p_pie.add_run(f"LivLin Indagación Regenerativa v7.0 · {str(datetime.now())[:10]}")
    r_pie.font.size=Pt(8); r_pie.font.color.rgb=CG; r_pie.italic=True

    buf=io.BytesIO(); doc.save(buf); buf.seek(0)
    return buf.read()
