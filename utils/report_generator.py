"""Excel export v3.3 — LivLin Indagación Regenerativa.
Auto-explicativo, narrativa regenerativa alineada con Mason (2025).
Logo LivLin embebido en portada.
"""
import io, json, base64, tempfile, os
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from utils.petal_content import (
    PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS, IPR_OBS_VS_POT,
    LIVLIN_URL, LIVLIN_TAGLINE, LIVLIN_DESC, LIVLIN_MODULES,
    LIVLIN_SERVICES_PITCH, LIVLIN_CLOSING, REGENERATION_FRAMEWORK, GLOBAL_REFS,
    TAO_REFLEXION_SHORT, TAO_INVITACION
)

C1="1B4332"; C2="2D6A4F"; C3="40916C"; C4="52B788"; C5="D8F3DC"
WHITE="FFFFFF"; GRAY="F5F5F5"; GOLD="FFF8DC"; AMBER="FFF3E0"; AMBER_D="2D6A4F"

def _f(h): return PatternFill("solid", fgColor=h)
def _s(c=C2): return Side(style="thin", color=c)
THIN = Border(left=_s(), right=_s(), top=_s(), bottom=_s())
BOT  = Border(bottom=Side(style="medium", color=C1))

def _cs(ws, r, c, val="", bg=WHITE, fg=C1, bold=False, size=9,
        ha="left", wrap=True, mc=None, border=None, italic=False, url=None):
    if isinstance(val, (list,dict)): val=str(val)
    if val is None: val=""
    cell = ws.cell(row=r, column=c, value=str(val)[:800])
    cell.fill=_f(bg); cell.font=Font(bold=bold,color=fg,size=size,italic=italic,
                                      name="Calibri",underline="single" if url else None)
    cell.alignment=Alignment(horizontal=ha,vertical="top",wrap_text=wrap)
    if mc: ws.merge_cells(start_row=r,start_column=c,end_row=r,end_column=c+mc-1)
    if border: cell.border=border
    if url: cell.hyperlink=url
    return cell

def _H(ws,r,txt,bg=C1,fg=WHITE,span=6,h=30,sz=13):
    _cs(ws,r,1,txt,bg=bg,fg=fg,bold=True,size=sz,ha="center",mc=span)
    ws.row_dimensions[r].height=h; return r+1

def _h(ws,r,txt,bg=C2,fg=WHITE,span=6,h=22,sz=10):
    _cs(ws,r,1,txt,bg=bg,fg=WHITE,bold=True,size=sz,mc=span)
    ws.row_dimensions[r].height=h; return r+1

def _expl(ws,r,txt,span=6,h=None):
    _cs(ws,r,1,txt,bg=AMBER,fg=AMBER_D,italic=True,size=8,mc=span,wrap=True)
    ws.row_dimensions[r].height=h or max(18,min(len(txt)//5,55))
    return r+1

def _row(ws,r,lbl,val,h=20):
    _cs(ws,r,1,lbl,bg=C5,bold=True,size=9,mc=2,border=THIN)
    _cs(ws,r,3,str(val) if val else "",bg=WHITE,fg=C2,size=9,mc=4,wrap=True,border=BOT)
    ws.row_dimensions[r].height=h; return r+1

def _sp(ws,r,span=6):
    _cs(ws,r,1,"",bg=C5,mc=span); ws.row_dimensions[r].height=5; return r+1

def _ref(ws,r,auth,title,url,span=6):
    _cs(ws,r,1,auth,bg=GRAY,bold=True,size=8,mc=2,border=THIN)
    _cs(ws,r,3,title,bg=GRAY,size=8,mc=3,wrap=True,border=BOT)
    _cs(ws,r,6,url,bg=GRAY,fg="1565C0",size=8,url=url,border=BOT)
    ws.row_dimensions[r].height=18; return r+1

def _wcol(ws,widths):
    for i,w in enumerate(widths,1):
        ws.column_dimensions[get_column_letter(i)].width=w

def _score_lv(n):
    if n==0: return "○ Sin inicio"
    if n==1: return "🌱 Iniciando"
    if n==2: return "🌿 Avanzando"
    if n==3: return "🌳 Consolidado"
    if n<=5: return "🌸 Destacado"
    return "✨ Referente"

def _load_petalos():
    jf = Path(__file__).parent.parent/"data"/"petalos_regeneracion_urbana.json"
    try:
        with open(jf,encoding="utf-8") as f: return json.load(f)["petalos"]
    except: return []

_LOGO_TMP = None

def _add_logo(ws, row=1, col=1, size_cm=2.5):
    """Add LivLin logo to worksheet. Uses /tmp/livlin_logo.png for cloud compatibility."""
    global _LOGO_TMP
    try:
        from utils.logo_b64 import LOGO_B64
        import os
        tmp_path = "/tmp/livlin_logo.png"
        if not os.path.exists(tmp_path):
            logo_bytes = base64.b64decode(LOGO_B64)
            with open(tmp_path, "wb") as _fh2:
                _fh2.write(logo_bytes)
        _LOGO_TMP = tmp_path
        img = XLImage(tmp_path)
        px = int(size_cm * 37.8)
        img.width = px; img.height = px
        ws.add_image(img, ws.cell(row=row, column=col).coordinate)
        return True
    except Exception as e:
        print(f"[logo] {e}")
        return False


def generate_excel(data: dict) -> bytes:
    wb = Workbook()
    petalos  = _load_petalos()
    ipr_obs  = data.get("ipr_obs", [])
    ipr_new  = data.get("ipr_new", [])
    facilitador = data.get("proyecto_facilitador","")
    fecha_emision = data.get("informe_fecha_emision","")

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 0 — PRESENTACIÓN
    # ═══════════════════════════════════════════════════════════════════
    ws0=wb.active; ws0.title="🌿 Presentación"
    _wcol(ws0,[26,16,20,18,20,16])

    # Logo en esquina superior izquierda
    _add_logo(ws0, row=1, col=1, size_cm=2.2)

    # Título principal (col 2 en adelante para dar espacio al logo)
    ws0.merge_cells("B1:F1")
    ws0["B1"]="🌿 LivLin · Indagación Regenerativa v3.3"
    ws0["B1"].fill=_f(C1); ws0["B1"].font=Font(color=WHITE,bold=True,size=18,name="Calibri")
    ws0["B1"].alignment=Alignment(horizontal="center",vertical="center")
    ws0.row_dimensions[1].height=55

    ws0.merge_cells("A2:F2")
    ws0["A2"]=f"Potencial para una vida regenerativa  ·  www.livlin.cl"
    ws0["A2"].fill=_f(C2); ws0["A2"].font=Font(color=WHITE,size=11,italic=True,name="Calibri")
    ws0["A2"].alignment=Alignment(horizontal="center",vertical="center")
    ws0.row_dimensions[2].height=26

    r=3; r=_sp(ws0,r)

    # Datos del diagnóstico
    r=_h(ws0,r,"📋 Información del Diagnóstico")
    for lbl,key in [("Espacio","proyecto_nombre"),("Contacto","proyecto_cliente"),
                    ("Ciudad","proyecto_ciudad"),("Fecha de visita","proyecto_fecha"),
                    ("Tipo de espacio","proyecto_tipo_espacio")]:
        r=_row(ws0,r,lbl,data.get(key,""))
    if facilitador: r=_row(ws0,r,"Facilitador/a",facilitador)
    if fecha_emision: r=_row(ws0,r,"Fecha emisión informe",fecha_emision)
    r=_sp(ws0,r)

    # Marco regenerativo
    r=_h(ws0,r,"🌱 Marco conceptual: el enfoque de la regeneración")
    r=_expl(ws0,r,REGENERATION_FRAMEWORK,h=50)
    r=_expl(ws0,r,LIVLIN_DESC,h=65)
    _cs(ws0,r,1,"🔗 www.livlin.cl",bg=C5,fg="1565C0",size=9,url=LIVLIN_URL,mc=6)
    ws0.row_dimensions[r].height=18; r+=1
    r=_sp(ws0,r)

    # IPR
    r=_h(ws0,r,"📊 Índice de Potencial Regenerativo (IPR) — Qué es y cómo interpretar")
    r=_expl(ws0,r,IPR_WHAT_IS,h=50)
    r=_expl(ws0,r,IPR_OBS_VS_POT,h=45)
    r=_sp(ws0,r)

    r=_h(ws0,r,"🔢 Escala de niveles IPR",bg=C2,span=6)
    _cs(ws0,r,1,"Nivel",bg=C4,bold=True,size=9,border=THIN)
    _cs(ws0,r,2,"N° prácticas",bg=C4,bold=True,size=9,ha="center",border=THIN)
    _cs(ws0,r,3,"Significado regenerativo",bg=C4,bold=True,size=9,mc=4,border=THIN)
    ws0.row_dimensions[r].height=20; r+=1
    for lvl,n,_,meaning in IPR_SCALE:
        bg=C5 if r%2==0 else WHITE
        _cs(ws0,r,1,lvl,bg=bg,bold=True,size=9,border=THIN)
        _cs(ws0,r,2,n,bg=bg,size=9,ha="center",border=THIN)
        _cs(ws0,r,3,meaning,bg=bg,size=9,mc=4,wrap=True,border=BOT)
        ws0.row_dimensions[r].height=28; r+=1
    r=_sp(ws0,r)

    # Módulos
    r=_h(ws0,r,"📑 Índice de módulos — qué encontrarás en cada hoja")
    for mod,desc in LIVLIN_MODULES:
        _cs(ws0,r,1,mod,bg=C4,bold=True,size=9,mc=2,border=THIN)
        _cs(ws0,r,3,desc,bg=C5,size=9,mc=4,wrap=True,border=BOT)
        ws0.row_dimensions[r].height=28; r+=1
    r=_sp(ws0,r)

    # Referencias
    r=_h(ws0,r,"📚 Referencias y recursos — materiales de profundización")
    r=_expl(ws0,r,"Todos los materiales listados aquí amplían el marco conceptual de este diagnóstico. "
            "Haz clic en las URLs para acceder directamente.",h=25)
    for auth,title,url in GLOBAL_REFS:
        r=_ref(ws0,r,auth,title,url)

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 1 — RESUMEN EJECUTIVO
    # ═══════════════════════════════════════════════════════════════════
    ws1=wb.create_sheet("📊 Resumen IPR")
    _wcol(ws1,[26,14,14,12,14,14])
    _add_logo(ws1,1,1,1.8)
    ws1.merge_cells("B1:F1")
    ws1["B1"]="📊 RESUMEN — ÍNDICE DE POTENCIAL REGENERATIVO"
    ws1["B1"].fill=_f(C1); ws1["B1"].font=Font(color=WHITE,bold=True,size=13,name="Calibri")
    ws1["B1"].alignment=Alignment(horizontal="center",vertical="center")
    ws1.row_dimensions[1].height=45
    r=2; r=_expl(ws1,r,f"{IPR_WHAT_IS} {IPR_OBS_VS_POT}",h=60)
    r=_sp(ws1,r)
    for lbl,key in [("Espacio","proyecto_nombre"),("Fecha","proyecto_fecha")]:
        r=_row(ws1,r,lbl,data.get(key,""))
    if facilitador: r=_row(ws1,r,"Facilitador/a",facilitador)
    r=_sp(ws1,r)

    r=_h(ws1,r,"🌸 IPR por pétalo — Observado hoy vs Con potencial adicional")
    _cs(ws1,r,1,"Pétalo",bg=C4,bold=True,size=9,mc=2,border=THIN)
    _cs(ws1,r,3,"✅ Observado",bg=C5,bold=True,size=9,ha="center",border=THIN)
    _cs(ws1,r,4,"🌟 + Potencial",bg=AMBER,bold=True,size=9,ha="center",border=THIN)
    _cs(ws1,r,5,"Nivel observado",bg=C4,bold=True,size=9,ha="center",border=THIN)
    _cs(ws1,r,6,"Nivel con potencial",bg=C4,bold=True,size=9,ha="center",border=THIN)
    ws1.row_dimensions[r].height=20; r+=1
    for i,p in enumerate(petalos):
        icon=PETAL_ICONS[i] if i<len(PETAL_ICONS) else "🌱"
        n_o=ipr_obs[i] if i<len(ipr_obs) else 0
        n_n=ipr_new[i] if i<len(ipr_new) else 0
        bg=C5 if i%2==0 else WHITE
        _cs(ws1,r,1,f"{icon} {p['nombre']}",bg=bg,bold=True,size=9,mc=2,border=THIN)
        _cs(ws1,r,3,str(n_o),bg=C5,size=10,ha="center",border=THIN)
        _cs(ws1,r,4,f"+{n_n}",bg=AMBER,fg=AMBER_D,size=10,ha="center",border=THIN)
        _cs(ws1,r,5,_score_lv(n_o),bg=bg,size=8,ha="center",border=THIN)
        _cs(ws1,r,6,_score_lv(n_o+n_n),bg=bg,size=8,ha="center",border=THIN)
        ws1.row_dimensions[r].height=22; r+=1
    r=_sp(ws1,r)

    dest=data.get("pot_practicas_destacadas","")
    if dest:
        r=_h(ws1,r,"✨ Prácticas más destacadas del espacio")
        _cs(ws1,r,1,dest,bg=GOLD,fg="5C3D00",size=9,mc=6,wrap=True,italic=True)
        ws1.row_dimensions[r].height=55; r+=1
    r=_sp(ws1,r)

    # LivLin services pitch
    r=_h(ws1,r,"🌿 Próximos pasos con LivLin",bg=C2)
    r=_expl(ws1,r,LIVLIN_SERVICES_PITCH,h=55)
    _cs(ws1,r,1,"🔗 www.livlin.cl · Potencial para una vida regenerativa",
        bg=C5,fg="1565C0",size=9,url=LIVLIN_URL,mc=6)
    ws1.row_dimensions[r].height=18; r+=1

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 2 — M1
    # ═══════════════════════════════════════════════════════════════════
    ws2=wb.create_sheet("📋 M1 Intención + Tao")
    _wcol(ws2,[24,14,24,14,12,10])
    r=_H(ws2,1,"📋 MÓDULO 1 — Intención y Contexto + Tao de la Regeneración")
    r=_expl(ws2,r,"Este módulo establece el horizonte de sentido del diagnóstico. Explora la motivación "
            "regenerativa del espacio, el sueño que mueve a quienes lo habitan y su percepción de la "
            "triple crisis planetaria. Siguiendo a Mason (2025): 'cada día tenemos una oportunidad de "
            "vivir el tránsito hacia una mejor forma de vivir'.",h=50)
    r=_sp(ws2,r)
    r=_h(ws2,r,"🏡 Datos del Espacio")
    for lbl,key in [("Nombre","proyecto_nombre"),("Contacto","proyecto_cliente"),
                    ("Ciudad","proyecto_ciudad"),("Dirección","proyecto_direccion"),
                    ("Tipo de espacio","proyecto_tipo_espacio"),("Superficie (m²)","proyecto_superficie"),
                    ("Habitantes","proyecto_habitantes"),("Barrio","proyecto_barrio_desc"),
                    ("Intención","proyecto_intencion")]:
        v=data.get(key,""); 
        if v: r=_row(ws2,r,lbl,str(v))
    if facilitador: r=_row(ws2,r,"Facilitador/a",facilitador)
    r=_sp(ws2,r)
    r=_h(ws2,r,"🌀 Tao de la Regeneración — Motivación y sueño")
    r=_expl(ws2,r,"El 'Tao de la regeneración' explora qué mueve a las personas a transformar su espacio. "
            "Es el motor interno del proceso: sin motivación clara, las técnicas no persisten (Mason, 2025).",h=35)
    for lbl,key in [("Motivación","tao_motivacion"),("Sueño regenerativo","tao_sueno"),
                    ("Relación con la naturaleza","tao_naturaleza"),
                    ("Cambio climático","tao_cc"),("Biodiversidad","tao_bio"),("Contaminación","tao_contam")]:
        v=data.get(key,"")
        if v: r=_row(ws2,r,lbl,str(v))

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 3 — M2-3
    # ═══════════════════════════════════════════════════════════════════
    ws3=wb.create_sheet("🔬 M2-3 Ecología del Sitio")
    _wcol(ws3,[24,14,24,14,12,10])
    r=_H(ws3,1,"🔬 MÓDULOS 2-3 — Observación Ecológica del Sitio")
    r=_expl(ws3,r,"'Observar e interactuar' es el primer principio de Holmgren. Antes de diseñar cualquier "
            "intervención, el facilitador lee el lugar: su suelo, agua, sol, viento, biodiversidad. "
            "Esta observación es la base de todo proceso regenerativo bien fundamentado.",h=45)
    r=_sp(ws3,r)
    for section, fields, nota in [
        ("🪱 Suelo — Base de todo sistema vivo",
         [("suelo_tipo","Tipo"),("suelo_compactacion","Compactación"),("suelo_materia_organica","Materia orgánica"),
          ("suelo_drenaje","Drenaje"),("suelo_color","Color"),("suelo_olor","Olor"),("suelo_notas","Notas")],
         "El suelo vivo es el capital más valioso de un espacio regenerativo. Su salud determina todo lo demás."),
        ("🌿 Vegetación",
         [("veg_tipos","Tipos presentes"),("veg_especies","Especies identificadas"),("veg_invasoras","Invasoras")],
         "La vegetación existente revela la historia y el potencial ecológico del lugar."),
        ("☀️ Flujos Naturales — Sol, Viento, Agua, Clima",
         [("sol_horas","Horas sol/día"),("sol_orientacion","Orientación"),("viento_direccion","Viento"),
          ("agua_prec_anual","Precipitación anual (mm)"),("clima_mes_caluroso","Mes más cálido"),
          ("clima_mes_frio","Mes más frío"),("clima_t_max_abs","T° máxima"),("clima_t_min_abs","T° mínima")],
         "Entender los flujos energéticos del sitio permite diseñar con ellos, no contra ellos."),
        ("🥦 Potencial de Cultivo",
         [("cultivo_m2","Área cultivable (m²)"),("cultivo_riego_acceso","Acceso al agua"),
          ("cultivo_produce_hoy","Produce alimentos hoy"),("cultivo_frutales","Espacio para frutales")],
         "Todo espacio urbano tiene potencial de producción alimentaria. Aquí se cuantifica el de este lugar."),
    ]:
        r=_h(ws3,r,section)
        r=_expl(ws3,r,nota,h=25)
        for k,lbl in fields:
            v=data.get(k,"")
            if v: r=_row(ws3,r,lbl,str(v))
        r=_sp(ws3,r)

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 4 — M4-6
    # ═══════════════════════════════════════════════════════════════════
    ws4=wb.create_sheet("🏙️ M4-6 Sistemas")
    _wcol(ws4,[24,14,24,14,12,10])
    r=_H(ws4,1,"🏙️ MÓDULOS 4-6 — Contexto, Agua, Energía y Materiales")
    r=_expl(ws4,r,"Mapear los flujos vitales del espacio revela oportunidades de autonomía: donde el agua "
            "se desperdicia, puede captarse; donde la energía se derrocha, puede ahorrarse; donde los "
            "residuos se botan, pueden convertirse en recursos. Cerrar ciclos es regenerar (Mason, 2025).",h=45)
    r=_sp(ws4,r)
    r=_h(ws4,r,"💧 Sistema de Agua")
    r=_expl(ws4,r,"Captación, almacenamiento, uso eficiente y reutilización de aguas grises: las 4 palancas "
            "de la soberanía hídrica urbana. Cada litro de lluvia captada es un litro que no depende de la red.",h=30)
    for lbl,key in [("Consumo diario (L)","agua_consumo"),("Precipitación anual (mm)","agua_prec_anual"),
                    ("Área de techo captación (m²)","agua_techo_m2"),("Tipo de riego","agua_riego_tipo"),
                    ("Aguas grises","agua_grises")]:
        v=data.get(key,"")
        if v: r=_row(ws4,r,lbl,str(v))
    r=_sp(ws4,r)
    r=_h(ws4,r,"⚡ Sistema de Energía")
    r=_expl(ws4,r,"La transición energética comienza en casa: conocer el consumo actual es el primer paso "
            "para dimensionar un sistema solar y reducir la dependencia de la red eléctrica.",h=30)
    for lbl,key in [("Consumo mensual (kWh)","ene_kwh_mes"),("Fuente principal","ene_fuente_principal"),
                    ("Interés en solar","ene_solar_interes")]:
        v=data.get(key,"")
        if v: r=_row(ws4,r,lbl,str(v))
    r=_sp(ws4,r)
    r=_h(ws4,r,"♻️ Materiales y Residuos")
    r=_expl(ws4,r,"Los residuos no existen en la naturaleza: todo cicla. Compostar, reutilizar y reducir "
            "son los primeros pasos para cerrar el ciclo de materiales en el espacio.",h=28)
    for lbl,key in [("Compostaje","mat_compost"),("Reciclaje","mat_reciclaje"),
                    ("Reducción plástico","mat_plastico_uso")]:
        v=data.get(key,"")
        if v: r=_row(ws4,r,lbl,str(v))

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 5 — M7 FLOR
    # ═══════════════════════════════════════════════════════════════════
    ws5=wb.create_sheet("🌸 M7 Flor Permacultura")
    _wcol(ws5,[28,18,18,6,28])
    _add_logo(ws5,1,1,1.8)
    ws5.merge_cells("B1:E1")
    ws5["B1"]="🌸 FLOR DE LA PERMACULTURA — Índice de Potencial Regenerativo (IPR)"
    ws5["B1"].fill=_f(C1); ws5["B1"].font=Font(color=WHITE,bold=True,size=13,name="Calibri")
    ws5["B1"].alignment=Alignment(horizontal="center",vertical="center")
    ws5.row_dimensions[1].height=45
    r=2; r=_expl(ws5,r,IPR_WHAT_IS,span=5,h=45)
    r=_expl(ws5,r,IPR_OBS_VS_POT,span=5,h=40)
    r=_sp(ws5,r,span=5)

    r=_h(ws5,r,"🔢 Escala IPR",bg=C2,span=5)
    for lvl,n,_,meaning in IPR_SCALE:
        _cs(ws5,r,1,f"{lvl} ({n})",bg=C5,bold=True,size=8,mc=2,border=THIN)
        _cs(ws5,r,3,meaning,bg=WHITE,size=8,mc=3,wrap=True,border=BOT)
        ws5.row_dimensions[r].height=22; r+=1
    r=_sp(ws5,r,span=5)

    for i,p in enumerate(petalos):
        icon=PETAL_ICONS[i] if i<len(PETAL_ICONS) else "🌱"
        n_o=ipr_obs[i] if i<len(ipr_obs) else 0
        n_n=ipr_new[i] if i<len(ipr_new) else 0
        lv_o=_score_lv(n_o); lv_t=_score_lv(n_o+n_n)
        desc=PETAL_DESC.get(p["nombre"],{})
        resumen=desc.get("resumen","") if isinstance(desc,dict) else ""
        detalle=desc.get("detalle","") if isinstance(desc,dict) else ""
        refs=desc.get("referencias",[]) if isinstance(desc,dict) else []

        r=_h(ws5,r,f"{icon} {p['nombre']}  ·  {lv_o} → con potencial: {lv_t}",span=5)
        if resumen: r=_expl(ws5,r,resumen,span=5,h=40)
        if detalle: r=_expl(ws5,r,detalle,span=5,h=55)

        _cs(ws5,r,1,f"✅ Observado: {n_o} práctica(s) — {lv_o}",bg=C5,bold=True,size=9,mc=2,border=THIN)
        _cs(ws5,r,3,f"🌟 Potencial adicional: +{n_n} → Total: {lv_t}",bg=AMBER,fg=AMBER_D,bold=True,size=9,mc=3,border=THIN)
        ws5.row_dimensions[r].height=22; r+=1

        _cs(ws5,r,1,"Subcategoría",bg=C4,bold=True,size=8,border=THIN)
        _cs(ws5,r,2,"✅ Prácticas observadas",bg=C5,bold=True,size=8,border=THIN)
        _cs(ws5,r,3,"🌟 Potencial adicional",bg=AMBER,bold=True,fg=AMBER_D,size=8,border=THIN)
        _cs(ws5,r,4,"N",bg=C4,bold=True,size=8,ha="center",border=THIN)
        _cs(ws5,r,5,"Notas",bg=C4,bold=True,size=8,border=THIN)
        ws5.row_dimensions[r].height=18; r+=1

        obs_data=data.get(f"petalo_{i}_obs",{})
        new_data=data.get(f"petalo_{i}_pot_new",{})
        otros_obs=data.get(f"petalo_{i}_otros_obs",[])
        otros_new=data.get(f"petalo_{i}_otros_new",[])
        notas=data.get(f"petalo_{i}_notas","")
        has_any=False

        for cat_key in p.get("categorias",{}):
            obs_s=obs_data.get(cat_key,[]); new_s=new_data.get(cat_key,[])
            if not obs_s and not new_s: continue
            has_any=True
            _cs(ws5,r,1,cat_key.replace("_"," ").title(),bg=WHITE,bold=True,size=8,border=THIN)
            _cs(ws5,r,2," · ".join(obs_s),bg=C5,size=8,wrap=True,border=THIN)
            _cs(ws5,r,3," · ".join(new_s),bg=AMBER,fg=AMBER_D,size=8,wrap=True,border=THIN)
            _cs(ws5,r,4,str(len(obs_s)+len(new_s)),bg=WHITE,size=9,ha="center",border=THIN)
            ws5.row_dimensions[r].height=max(18,min((len(obs_s)+len(new_s))*12,55)); r+=1

        if otros_obs or otros_new:
            _cs(ws5,r,1,"Otras prácticas",bg=WHITE,bold=True,size=8,border=THIN)
            _cs(ws5,r,2," · ".join(otros_obs),bg=C5,size=8,wrap=True,border=THIN)
            _cs(ws5,r,3," · ".join(otros_new),bg=AMBER,fg=AMBER_D,size=8,wrap=True,border=THIN)
            _cs(ws5,r,4,str(len(otros_obs)+len(otros_new)),bg=WHITE,size=9,ha="center",border=THIN)
            ws5.row_dimensions[r].height=20; r+=1; has_any=True

        if not has_any:
            _cs(ws5,r,1,"— Sin prácticas registradas para este pétalo —",
                bg=WHITE,italic=True,fg="888888",size=8,mc=4)
            ws5.row_dimensions[r].height=18; r+=1

        if notas:
            _cs(ws5,r,1,"📝 Notas del facilitador:",bg=GOLD,bold=True,size=8)
            _cs(ws5,r,2,notas,bg=GOLD,fg="5C3D00",size=8,mc=3,wrap=True,italic=True)
            ws5.row_dimensions[r].height=30; r+=1

        if refs:
            for auth,tit,url in refs:
                _cs(ws5,r,1,f"📚 {auth}",bg=GRAY,italic=True,size=7,mc=2)
                _cs(ws5,r,3,tit,bg=GRAY,italic=True,size=7)
                _cs(ws5,r,4,url,bg=GRAY,fg="1565C0",size=7,url=url,mc=2)
                ws5.row_dimensions[r].height=16; r+=1
        r=_sp(ws5,r,span=5)

    # Radar chart image
    radar_b64 = data.get("ipr_radar_b64","")
    if radar_b64:
        try:
            import base64, io as _io
            from openpyxl.drawing.image import Image as _XLImg
            img_bytes = base64.b64decode(radar_b64)
            tmp_radar = "/tmp/livlin_radar.png"
            with open(tmp_radar,"wb") as _fh: _fh.write(img_bytes)
            xl_img = _XLImg(tmp_radar)
            xl_img.width = 520; xl_img.height = 320
            ws5.add_image(xl_img, ws5.cell(row=r, column=1).coordinate)
            r += 20  # space for image
            r=_expl(ws5,r,"Gráfico radar: verde sólido = Observado hoy · verde punteado = Con potencial adicional. "
                    "Escala 0–10 normalizada al máximo de prácticas del diagnóstico.",span=5,h=28)
        except Exception as e:
            r=_expl(ws5,r,f"[Gráfico radar no disponible: {e}]",span=5,h=18)

    dest=data.get("pot_practicas_destacadas","")
    if dest:
        r=_h(ws5,r,"✨ Prácticas más destacadas del espacio",span=5)
        _cs(ws5,r,1,dest,bg=GOLD,fg="5C3D00",size=9,mc=5,wrap=True,italic=True)
        ws5.row_dimensions[r].height=55; r+=1
    r=_sp(ws5,r,span=5)
    r=_h(ws5,r,"🌿 LivLin puede acompañarte en implementar este potencial",bg=C2,span=5)
    r=_expl(ws5,r,LIVLIN_SERVICES_PITCH,span=5,h=50)

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 6 — M9
    # ═══════════════════════════════════════════════════════════════════
    ws6=wb.create_sheet("🗺️ M9 Síntesis + Plan")
    _wcol(ws6,[26,14,22,14,14,10])
    r=_H(ws6,1,"🗺️ MÓDULO 9 — Síntesis y Plan de Acción")
    r=_expl(ws6,r,"La hoja de ruta regenerativa organiza los próximos pasos en 3 horizontes temporales, "
            "siguiendo la lógica del descenso creativo: acciones cotidianas inmediatas que generan "
            "motivación + transformaciones de fondo que se sostienen en generaciones (Mason, 2025).",h=45)
    r=_sp(ws6,r)
    r=_h(ws6,r,"📊 Síntesis del Diagnóstico")
    # Source explanation
    r=_expl(ws6,r,
        "Las dimensiones regenerativas son un instrumento de síntesis desarrollado por LivLin "
        "para visualizar el potencial del espacio en 8 áreas clave interconectadas, "
        "fundamentadas en los principios de la permacultura (Holmgren, 2002), "
        "el diseño regenerativo (Mang & Reed, 2012) y el enfoque ecosocial (Mason, 2025).",h=40)

    # Dimensional scores with interpretations
    try:
        from utils.scoring import compute_synthesis_potentials
        from modules.action_plan import DIM_INTERP, DIM_DESC
        pots = compute_synthesis_potentials(data)
        if pots:
            r=_h(ws6,r,"Dimensiones Regenerativas — Puntaje e Interpretación",bg=C2,span=6)
            for dim, val in pots.items():
                level_idx = min(int(round(val)), 5)
                interp = DIM_INTERP.get(dim, [""]*(level_idx+1))[level_idx] if dim in DIM_INTERP else ""
                dim_desc = DIM_DESC.get(dim, "")
                _cs(ws6,r,1,dim,bg=C4,bold=True,size=9,mc=2,border=THIN)
                _cs(ws6,r,3,f"{val:.1f}/5",bg=C5,bold=True,size=10,ha="center",border=THIN)
                _cs(ws6,r,5,dim_desc[:200],bg=WHITE,size=8,mc=2,wrap=True,border=BOT)
                ws6.row_dimensions[r].height=20; r+=1
                if interp:
                    r=_expl(ws6,r,f"📊 {interp}",h=35)
            r=_sp(ws6,r)
    except Exception as e:
        print(f"[report] dimensions: {e}")

    for key,lbl in [("sint_fortalezas","💚 Fortalezas — lo que ya florece"),
                    ("sint_desafios","⚡ Desafíos — obstáculos reales"),
                    ("sint_oportunidades","🌱 Oportunidades — potencial por activar"),
                    ("sint_narrativa","📖 Narrativa del proceso")]:
        v=data.get(key,"")
        if v: r=_row(ws6,r,lbl,str(v),h=28)
    r=_sp(ws6,r)
    for pk,fase,desc in [
        ("plan_inmediatas","⚡ Fase 1 — Acciones Inmediatas (0–3 meses)",
         "Cambios de bajo costo y alta visibilidad. Generan motivación, muestran resultados y "
         "rompen los primeros patrones degenerativos cotidianos."),
        ("plan_estacionales","🌱 Fase 2 — Acciones Estacionales (3–12 meses)",
         "Intervenciones que siguen los ritmos naturales y requieren planificación. Estructuran "
         "los ciclos del espacio y consolidan las prácticas iniciales."),
        ("plan_estructurales","🌳 Fase 3 — Transformaciones Estructurales (1–5 años)",
         "Cambios de fondo en infraestructura, gobernanza o sistemas. Son las inversiones que "
         "construyen resiliencia para las futuras generaciones."),
    ]:
        r=_h(ws6,r,fase); r=_expl(ws6,r,desc,h=28)
        v=data.get(pk,"")
        if v:
            if isinstance(v,list):
                for item in v:
                    txt=item.get("titulo","") if isinstance(item,dict) else str(item)
                    if txt: r=_row(ws6,r,"→",txt)
            else:
                _cs(ws6,r,1,str(v),bg=GOLD,fg="5C3D00",size=9,mc=6,wrap=True)
                ws6.row_dimensions[r].height=40; r+=1
        else:
            _cs(ws6,r,1,"— Sin acciones registradas —",bg=WHITE,italic=True,fg="888888",size=8,mc=6)
            ws6.row_dimensions[r].height=18; r+=1
        r=_sp(ws6,r)
    r=_h(ws6,r,"🌿 LivLin — Tu aliado en la implementación",bg=C2)
    r=_expl(ws6,r,LIVLIN_CLOSING,h=65)

    # Tao closing in M9 sheet
    r=_sp(ws6,r)
    r=_h(ws6,r,"🌿 Un camino interior — Tao de la Regeneración",bg=C1)
    r=_expl(ws6,r,TAO_REFLEXION_SHORT,h=60)
    r=_expl(ws6,r,TAO_INVITACION,h=45)

    # ═══════════════════════════════════════════════════════════════════
    # HOJA 7 — DATOS BIOCLIMÁTICOS
    # ═══════════════════════════════════════════════════════════════════
    ws7=wb.create_sheet("🌡️ Datos Bioclimáticos")
    _wcol(ws7,[26,14,24,12,14,10])
    r=_H(ws7,1,"🌡️ Datos Bioclimáticos del Sitio")
    r=_expl(ws7,r,
        "Los datos climáticos de este informe son generados automáticamente mediante dos APIs externas:\n"
        "1) NOMINATIM / OpenStreetMap (https://nominatim.openstreetmap.org): geocodificación — "
        "convierte la dirección del espacio en coordenadas geográficas precisas.\n"
        "2) OPEN-METEO Historical Weather API (https://open-meteo.com): proporciona estadísticas "
        "climáticas históricas (promedio de los últimos 5 años disponibles) incluyendo temperatura "
        "máxima y mínima mensual, precipitación acumulada y velocidad del viento.\n"
        "Ambas son APIs abiertas y gratuitas sin términos comerciales. "
        "Los datos son referenciales y deben complementarse con observación directa del sitio.",h=65)
    r=_sp(ws7,r)
    for lbl,key in [("Latitud","lat"),("Longitud","lon"),("Ciudad","proyecto_ciudad"),("Elevación","elevation")]:
        v=data.get(key,"")
        if v is not None and v!="": r=_row(ws7,r,lbl,str(v))
    r=_sp(ws7,r)
    r=_h(ws7,r,"🌡️ Temperatura")
    for lbl,key,expl in [
        ("Mes más cálido","clima_mes_caluroso","Mayor demanda de riego y sombra"),
        ("T° máx promedio (°C)","clima_t_max_abs","Base para diseño de ventilación y sombra"),
        ("Mes más frío","clima_mes_frio","Riesgo de heladas — clave para selección de cultivos"),
        ("T° mín promedio (°C)","clima_t_min_abs","Determina qué cultivos sobreviven el invierno"),
    ]:
        v=data.get(key,"")
        if v: r=_row(ws7,r,f"{lbl} ({expl})",str(v))
    r=_sp(ws7,r)
    r=_h(ws7,r,"💧 Agua y Solar")
    for lbl,key,expl in [
        ("Precipitación anual (mm)","agua_prec_anual","Potencial captación = mm × m² techo × 0.8"),
        ("Radiación solar (kWh/m²/día)","solar_annual_avg","Base para dimensionar instalación solar"),
        ("Mejor mes solar","solar_best_month","Mes de máxima generación solar disponible"),
    ]:
        v=data.get(key,"")
        if v: r=_row(ws7,r,f"{lbl} ({expl})",str(v))
    r=_sp(ws7,r)
    r=_expl(ws7,r,"📚 Referencias: La diferencia entre clima y el tiempo: https://www.youtube.com/watch?v=emPKer_pV14 · "
            "Elementos climáticos: https://www.youtube.com/watch?v=fQmHwUqX91E · "
            "Clima y Permacultura: https://www.youtube.com/results?search_query=clima+permacultura",h=35)

    for ws in [ws0,ws1,ws2,ws3,ws4,ws5,ws6,ws7]:
        ws.freeze_panes="A2"; ws.sheet_view.showGridLines=True

    buf=io.BytesIO(); wb.save(buf); buf.seek(0)
    return buf.read()
