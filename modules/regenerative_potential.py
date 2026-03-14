"""Módulo 7 — Flor de la Permacultura v2.0
Observado vs Potencial · IPR simplificado · Radar dual · Acciones + Otros.
"""
import json
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status

# ── Datos embebidos ───────────────────────────────────────────────────────────
_PETALOS_DATA = [{"nombre": "Manejo de la tierra y la naturaleza (urbano)", "categorias": {"produccion_alimentaria_urbana": ["Huertos en balcones y terrazas", "Huertos en macetas recicladas", "Huertos verticales en muros o cercos", "Jardines comestibles en patios pequeños", "Huertos en azoteas o techos planos", "Microhuertos en ventanas", "Cultivo hidropónico doméstico", "Cultivo acuapónico doméstico", "Cultivo en bolsas de cultivo o contenedores textiles", "Huertos en patios comunitarios", "Huertos escolares", "Huertos en centros culturales", "Huertos en espacios públicos recuperados", "Guerrilla gardening", "Cultivo de microgreens", "Germinados en casa", "Cultivo de hongos comestibles", "Cultivo de setas en café reciclado"], "suelo_vivo": ["Vermicompostaje doméstico", "Compostaje en baldes", "Compostaje bokashi", "Compostaje comunitario en el barrio", "Compostaje en departamentos usando lombrices", "Creación de suelo vivo en macetas", "Uso de microorganismos eficientes", "Uso de bioles y biofertilizantes", "Producción de biochar", "Fabricación de té de compost"], "biodiversidad_urbana": ["Plantación de árboles frutales urbanos", "Corredores de polinizadores", "Jardines para abejas nativas", "Jardines de mariposas", "Jardines medicinales urbanos", "Jardines aromáticos", "Refugios para insectos", "Casas para murciélagos", "Bebederos para aves", "Restauración de pequeños espacios degradados", "Plantación de especies nativas en jardines"], "agua": ["Captación de agua lluvia en casas", "Captación de agua lluvia en edificios", "Barriles recolectores de agua", "Sistemas de infiltración en patios", "Micro zanjas de infiltración", "Reutilización de aguas grises para riego", "Riego por goteo casero", "Jardines de lluvia urbanos", "Micro humedales artificiales"], "semillas": ["Guardar semillas en casa", "Intercambio de semillas entre vecinos", "Bibliotecas de semillas", "Bancos comunitarios de semillas", "Cultivo de variedades locales", "Multiplicación de plantas por esquejes", "Propagación de plantas nativas"]}}, {"nombre": "Ambiente construido", "categorias": {"vivienda_ecologica": ["Bioconstrucción en ampliaciones", "Uso de materiales naturales en remodelaciones", "Muros interiores de tierra o barro", "Pinturas naturales", "Aislación con materiales naturales"], "energia_pasiva": ["Diseño solar pasivo", "Ventilación cruzada en viviendas", "Uso de masas térmicas", "Sombreamiento natural con plantas", "Pérgolas verdes", "Enredaderas en fachadas"], "naturaleza_en_edificios": ["Techos verdes", "Muros verdes", "Jardines verticales comestibles", "Patios interiores con vegetación", "Balcones verdes"], "espacios_multifuncionales": ["Cocinas comunitarias", "Talleres compartidos", "Huertos en condominios", "Bodegas para alimentos comunitarios", "Espacios de compostaje en edificios"], "reutilizacion_materiales": ["Uso de pallets para jardinería", "Construcción con materiales reciclados", "Uso de ventanas recicladas para invernaderos", "Construcción de mini invernaderos", "Reutilización de contenedores"]}}, {"nombre": "Herramientas y tecnologías apropiadas", "categorias": {"energia": ["Paneles solares domésticos", "Calentadores solares de agua", "Cocinas solares", "Secadores solares de alimentos", "Sistemas solares portátiles"], "tecnologias_simples": ["Estufas rocket", "Hornos de barro urbanos", "Biodigestores domésticos pequeños", "Sistemas de riego automatizado de bajo consumo", "Sensores de humedad del suelo"], "agua": ["Filtros de agua domésticos", "Biofiltros de aguas grises", "Sistemas de captación de condensación", "Sistemas de almacenamiento de agua"], "movilidad": ["Uso de bicicleta", "Bicicletas de carga", "Carros para transportar cosechas", "Talleres comunitarios de reparación de bicicletas"], "alimentos": ["Fermentación de alimentos", "Deshidratación solar", "Conservas caseras", "Almacenamiento natural de alimentos", "Refrigeración pasiva"]}}, {"nombre": "Educación y cultura", "categorias": {"educacion_comunitaria": ["Talleres de agroecología urbana", "Talleres de compostaje", "Talleres de huertos urbanos", "Cursos de diseño regenerativo", "Intercambio de saberes tradicionales"], "educacion_practica": ["Aprendizaje basado en huertos", "Programas educativos en jardines escolares", "Programas de voluntariado ambiental", "Programas de mentoría en agroecología"], "cultura_regenerativa": ["Festivales de semillas", "Ferias de agricultura urbana", "Intercambio de plantas", "Cine ambiental comunitario", "Bibliotecas ecológicas"], "arte_y_comunidad": ["Murales ecológicos", "Música comunitaria", "Arte con materiales reciclados", "Teatro ambiental"], "redes": ["Redes de huertos urbanos", "Redes de semillas", "Redes de consumo local", "Redes de economía solidaria"]}}, {"nombre": "Salud y bienestar", "categorias": {"salud_fisica": ["Alimentación basada en plantas", "Consumo de alimentos locales", "Dietas agroecológicas", "Cocina saludable comunitaria"], "salud_mental": ["Jardinería terapéutica", "Baños de bosque urbanos", "Meditación en huertos", "Espacios de contemplación"], "medicina_natural": ["Cultivo de plantas medicinales", "Preparación de tinturas", "Preparación de pomadas", "Preparación de infusiones"], "comunidad": ["Grupos de apoyo comunitario", "Espacios de cuidado colectivo", "Redes de cuidado mutuo"], "movimiento": ["Yoga comunitario", "Tai chi en parques", "Caminatas ecológicas", "Bicicleteadas comunitarias"]}}, {"nombre": "Economía y finanzas", "categorias": {"economia_local": ["Mercados agroecológicos", "Ferias de intercambio", "Canastas comunitarias", "Agricultura apoyada por la comunidad (CSA)"], "economias_solidarias": ["Cooperativas de producción", "Cooperativas de consumo", "Cooperativas de vivienda", "Bancos de tiempo"], "sistemas_alternativos": ["Monedas locales", "Plataformas de trueque", "Redes de intercambio de servicios"], "emprendimientos_regenerativos": ["Producción de alimentos locales", "Viveros urbanos", "Diseño de huertos urbanos", "Educación ambiental", "Consultoría regenerativa"], "consumo_responsable": ["Compras a productores locales", "Reducción de consumo", "Reparación de objetos", "Reutilización de materiales", "Compras colectivas de alimentos", "Comprar a granel", "Evitar plásticos de un solo uso"]}}, {"nombre": "Tenencia de la tierra y gobernanza", "categorias": {"organizacion_comunitaria": ["Asambleas barriales", "Consejos comunitarios", "Mesas ambientales locales"], "gestion_espacios": ["Recuperación de sitios eriazos", "Creación de huertos comunitarios", "Parques comestibles urbanos", "Jardines comunitarios"], "participacion_ciudadana": ["Participación en planificación urbana", "Presupuestos participativos", "Defensa de áreas verdes"], "modelos_propiedad": ["Cooperativas de vivienda", "Comunidades intencionales urbanas", "Fideicomisos de tierra comunitaria"], "redes_territoriales": ["Redes de agroecología urbana", "Redes de transición urbana", "Redes de resiliencia comunitaria"]}}, {"nombre": "Prácticas cotidianas de sustentabilidad", "categorias": {"energia_domestica": ["Apagar luces cuando no se usan", "Usar ampolletas LED", "Usar electrodomésticos de bajo consumo", "Desconectar cargadores", "Usar regletas con interruptor"], "agua_domestica": ["Duchas cortas", "Cerrar la llave al lavar platos", "Reparar fugas de agua", "Reutilizar agua para riego"], "consumo_consciente": ["Comprar productos locales", "Comprar colectivamente", "Evitar envases innecesarios", "Reparar antes de comprar", "Compartir herramientas"], "vida_comunitaria": ["Conectar con vecinos", "Participar en organizaciones locales", "Participar en huertos comunitarios", "Organizar actividades de barrio"], "desarrollo_personal_regenerativo": ["Estudiar sobre regeneración", "Practicar agroecología", "Practicar meditación", "Practicar tai chi", "Practicar yoga", "Participar en talleres de regeneración"]}}]

PETAL_ICONS = ["🌳","🏡","🛠️","📚","🧘","💚","🤝","🌿"]

# ── Descripciones oficiales (Holmgren, 2002) ─────────────────────────────────
PETAL_DESC = {
    "Manejo de la tierra y la naturaleza (urbano)":
        "Corazón de la permacultura: diseño con la naturaleza para producir alimentos, "
        "regenerar suelos y aumentar biodiversidad. En contexto urbano incluye huertos, "
        "compostaje, captación de agua y corredores de polinizadores. "
        "(Holmgren, *Permacultura: Principios y senderos más allá de la sustentabilidad*, 2002)",
    "Ambiente construido":
        "Diseño de edificaciones, infraestructuras y espacios construidos con criterios "
        "bioclimáticos y de bajo impacto. Incluye energía pasiva, materiales naturales, "
        "techos y muros verdes. Las decisiones en este pétalo tienen impacto por décadas. "
        "(Holmgren, 2002; Reed, *Regenerative Development*, 2007)",
    "Herramientas y tecnologías apropiadas":
        "Selección crítica de herramientas y tecnologías que sirven a las personas y al "
        "planeta. Prioriza tecnologías simples, reparables y de bajo consumo energético. "
        "Incluye energía solar, biodigestores y sistemas de riego eficiente. "
        "(Schumacher, *Small is Beautiful*, 1973; Holmgren, 2002)",
    "Educación y cultura":
        "Transmisión de saberes, valores y prácticas que sostienen culturas regenerativas. "
        "Abarca educación formal e informal, arte, intercambio de semillas y redes de "
        "conocimiento local. Sin cultura regenerativa, las técnicas no persisten. "
        "(Freire, *Pedagogía del oprimido*, 1968; Holmgren, 2002)",
    "Salud y bienestar":
        "Sistemas de salud preventivos basados en alimentación viva, movimiento, plantas "
        "medicinales y comunidad. La jardinería terapéutica, los baños de naturaleza y el "
        "bienestar colectivo son dimensiones centrales de este pétalo. "
        "(IPES-Food, 2017; Holmgren, 2002)",
    "Economía y finanzas":
        "Sistemas económicos que circulan la riqueza localmente: mercados agroecológicos, "
        "cooperativas, trueque, monedas locales y finanzas éticas. Reduce la dependencia "
        "del sistema extractivo y fortalece la soberanía alimentaria. "
        "(Gibson-Graham, *A Postcapitalist Politics*, 2006; Holmgren, 2002)",
    "Tenencia de la tierra y gobernanza":
        "Marcos legales y comunitarios para el acceso y cuidado colectivo de la tierra. "
        "Incluye cooperativas de vivienda, huertos comunitarios, asambleas barriales y "
        "participación ciudadana en el diseño urbano. "
        "(Ostrom, *Governing the Commons*, 1990; Holmgren, 2002)",
    "Prácticas cotidianas de sustentabilidad":
        "Las acciones diarias del hogar y la vida cotidiana que acumulan impacto sistémico: "
        "reducir, reutilizar, reparar, consumir local, conectar con vecinos. "
        "Este pétalo reconoce que los pequeños actos transforman la cultura. "
        "(Shove, *Comfort, Cleanliness and Convenience*, 2003; Holmgren, 2002)",
}

# ── Scoring simplificado ─────────────────────────────────────────────────────
def _score_level(n: int) -> tuple[str, str, str]:
    """n = number of actions. Returns (level_name, emoji, color)"""
    if n == 0:   return "Sin inicio",    "○",  "#BDBDBD"
    if n == 1:   return "Iniciando",     "🌱", "#74C69D"
    if n == 2:   return "Avanzando",     "🌿", "#52B788"
    if n == 3:   return "Consolidado",   "🌳", "#40916C"
    if n <= 5:   return "Destacado",     "🌸", "#2D6A4F"
    return               "Referente",    "✨", "#1B4332"

def _petal_narrative(petal_name: str, n_obs: int, n_pot: int) -> str:
    lev_obs, em_obs, _ = _score_level(n_obs)
    lev_pot, em_pot, _ = _score_level(n_pot)
    gap = n_pot - n_obs
    parts = []
    if n_obs == 0:
        parts.append(f"Este espacio está en etapa inicial en **{petal_name}**.")
    else:
        parts.append(f"{em_obs} **{lev_obs}** — {n_obs} práctica(s) activa(s) en este pétalo.")
    if gap > 0:
        parts.append(f"El facilitador identifica **{gap} práctica(s) adicional(es)** con alto potencial para este espacio.")
    elif n_obs > 0:
        parts.append("El potencial reconocido está alineado con lo que ya se hace — ¡excellent sintonía!")
    return " ".join(parts)


def _get_petalos():
    if isinstance(_PETALOS_DATA, list):
        return _PETALOS_DATA
    return json.loads(_PETALOS_DATA) if isinstance(_PETALOS_DATA, str) else []


def render():
    data = st.session_state.get("visit_data", {})
    if not data.get("id"):
        st.warning("⚠️ Primero crea o carga un diagnóstico.")
        return

    st.markdown("## 🌸 Flor de la Permacultura")
    st.markdown(
        '<p class="module-subtitle">Observado · Potencial · IPR por pétalo</p>',
        unsafe_allow_html=True)

    st.markdown("**Estado de este módulo:**")
    _mod_status = render_module_status(data, "mod_potencial")
    if not is_module_active(_mod_status):
        if st.button("💾 Guardar como No Abordado", key="save_na_mod_potencial",
                     use_container_width=True):
            st.session_state.visit_data = data
            save_visit(data)
            st.success("✅ Módulo marcado como No Abordado.")
            show_drive_save_status()
        return
    if _mod_status == "inferido":
        st.info("🔍 **Modo inferido** — Respuestas del facilitador.")
    st.markdown("---")

    petalos = _get_petalos()
    if not petalos:
        st.error("❌ No se pudieron cargar los datos de pétalos.")
        return

    # ── Tabs ─────────────────────────────────────────────────────────────
    tab_labels = [f"{PETAL_ICONS[i]} {p['nombre'][:20]}" for i, p in enumerate(petalos)]
    tab_labels.append("📊 Resumen")
    tabs = st.tabs(tab_labels)

    scores_obs = []
    scores_pot = []

    for i, (tab, petalo) in enumerate(zip(tabs[:-1], petalos)):
        with tab:
            icon = PETAL_ICONS[i]
            st.markdown(f"### {icon} {petalo['nombre']}")

            # ── Descripción oficial ───────────────────────────────────────
            with st.expander("📖 ¿Qué es este pétalo?", expanded=False):
                st.markdown(PETAL_DESC.get(petalo['nombre'], ""))

            kp = f"p{i}"
            saved_obs = data.get(f"petalo_{i}_obs", {})
            saved_pot = data.get(f"petalo_{i}_pot", {})
            saved_otros_obs = data.get(f"petalo_{i}_otros_obs", [])
            saved_otros_pot = data.get(f"petalo_{i}_otros_pot", [])

            # ── Two columns: Observado | Potencial ───────────────────────
            col_obs, col_pot = st.columns(2)

            new_obs  = {}
            new_pot  = {}
            sel_obs_all = []
            sel_pot_all = []

            with col_obs:
                st.markdown(
                    '<div style="background:#E8F5E9;border-radius:8px;padding:0.5rem 0.8rem;'                    'border-left:4px solid #40916C;margin-bottom:0.5rem;">'                    '<strong>✅ Observado</strong><br>'                    '<span style="font-size:0.78rem;color:#2D6A4F;">Lo que ya ocurre en el espacio</span></div>',
                    unsafe_allow_html=True)

                for cat_key, acciones in petalo["categorias"].items():
                    cat_label = cat_key.replace("_"," ").title()
                    opts = ["(Ninguno)"] + acciones
                    prev = [a for a in saved_obs.get(cat_key, []) if a in acciones]
                    sel = st.multiselect(
                        cat_label, options=opts,
                        default=prev,
                        key=f"{kp}_obs_{cat_key}",
                        placeholder="Selecciona…")
                    sel_clean = [s for s in sel if s != "(Ninguno)"]
                    new_obs[cat_key] = sel_clean
                    sel_obs_all.extend(sel_clean)

                # Otros observados
                st.markdown("**➕ Otros (observados)**")
                otros_obs = list(saved_otros_obs)
                for j, otro in enumerate(otros_obs):
                    cc1, cc2 = st.columns([4,1])
                    with cc1: st.caption(f"• {otro}")
                    with cc2:
                        if st.button("✕", key=f"{kp}_del_otro_obs_{j}"):
                            otros_obs.pop(j); st.rerun()
                nuevo_otro_obs = st.text_input("Agregar otro (observado)",
                    key=f"{kp}_new_otro_obs", placeholder="Describe la práctica…")
                if st.button("+ Agregar", key=f"{kp}_add_otro_obs"):
                    if nuevo_otro_obs.strip():
                        otros_obs.append(nuevo_otro_obs.strip()); st.rerun()
                data[f"petalo_{i}_otros_obs"] = otros_obs
                sel_obs_all.extend(otros_obs)

            with col_pot:
                st.markdown(
                    '<div style="background:#FFF8E1;border-radius:8px;padding:0.5rem 0.8rem;'                    'border-left:4px solid #F9A825;margin-bottom:0.5rem;">'                    '<strong>🌟 Potencial</strong><br>'                    '<span style="font-size:0.78rem;color:#E65100;">Lo que podría implementarse (criterio facilitador)</span></div>',
                    unsafe_allow_html=True)

                for cat_key, acciones in petalo["categorias"].items():
                    cat_label = cat_key.replace("_"," ").title()
                    opts = ["(Ninguno)"] + acciones
                    prev = [a for a in saved_pot.get(cat_key, []) if a in acciones]
                    sel = st.multiselect(
                        cat_label, options=opts,
                        default=prev,
                        key=f"{kp}_pot_{cat_key}",
                        placeholder="Selecciona…")
                    sel_clean = [s for s in sel if s != "(Ninguno)"]
                    new_pot[cat_key] = sel_clean
                    sel_pot_all.extend(sel_clean)

                # Otros potencial
                st.markdown("**➕ Otros (potencial)**")
                otros_pot = list(saved_otros_pot)
                for j, otro in enumerate(otros_pot):
                    cc1, cc2 = st.columns([4,1])
                    with cc1: st.caption(f"• {otro}")
                    with cc2:
                        if st.button("✕", key=f"{kp}_del_otro_pot_{j}"):
                            otros_pot.pop(j); st.rerun()
                nuevo_otro_pot = st.text_input("Agregar otro (potencial)",
                    key=f"{kp}_new_otro_pot", placeholder="Describe la práctica…")
                if st.button("+ Agregar", key=f"{kp}_add_otro_pot"):
                    if nuevo_otro_pot.strip():
                        otros_pot.append(nuevo_otro_pot.strip()); st.rerun()
                data[f"petalo_{i}_otros_pot"] = otros_pot
                sel_pot_all.extend(otros_pot)

            # Save selections
            data[f"petalo_{i}_obs"] = new_obs
            data[f"petalo_{i}_pot"] = new_pot

            # ── Score bar ─────────────────────────────────────────────────
            n_obs = len(sel_obs_all)
            n_pot = len(sel_pot_all)
            scores_obs.append(n_obs)
            scores_pot.append(n_pot)

            lev_obs, em_obs, c_obs = _score_level(n_obs)
            lev_pot, em_pot, c_pot = _score_level(n_pot)

            st.markdown("---")
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(
                    f'<div style="background:{c_obs};border-radius:8px;padding:0.5rem 1rem;'                    f'color:white;text-align:center;">'                    f'<div style="font-size:1.4rem;">{em_obs}</div>'                    f'<div style="font-weight:700;">{lev_obs}</div>'                    f'<div style="font-size:0.8rem;">{n_obs} práctica(s) observada(s)</div></div>',
                    unsafe_allow_html=True)
            with m2:
                st.markdown(
                    f'<div style="background:{c_pot};border-radius:8px;padding:0.5rem 1rem;'                    f'color:white;text-align:center;">'                    f'<div style="font-size:1.4rem;">{em_pot}</div>'                    f'<div style="font-weight:700;">{lev_pot}</div>'                    f'<div style="font-size:0.8rem;">{n_pot} práctica(s) con potencial</div></div>',
                    unsafe_allow_html=True)

            st.markdown(f"*{_petal_narrative(petalo['nombre'], n_obs, n_pot)}*")

            # Notes
            data[f"petalo_{i}_notas"] = st.text_area(
                "📝 Notas del facilitador para este pétalo",
                value=data.get(f"petalo_{i}_notas",""),
                height=70, key=f"{kp}_notas",
                placeholder="Observaciones, contexto, oportunidades específicas…")

    # ══════════════════════════════════════════════════════════════════════
    with tabs[-1]:
        st.markdown("### 📊 Resumen — Observado vs Potencial")

        data["ipr_obs"]     = scores_obs
        data["ipr_pot"]     = scores_pot
        data["ipr_petalos"] = [p["nombre"] for p in petalos]

        # ── Dual radar chart ──────────────────────────────────────────────
        try:
            import plotly.graph_objects as go
            labels = [f"{PETAL_ICONS[i]} {p['nombre'][:18]}"
                      for i, p in enumerate(petalos)]
            # Normalize to 0-10 scale for radar readability
            max_v = max(max(scores_obs + scores_pot, default=1), 1)
            norm_obs = [min(s / max_v * 10, 10) for s in scores_obs]
            norm_pot = [min(s / max_v * 10, 10) for s in scores_pot]

            lbls_c = labels + [labels[0]]
            obs_c  = norm_obs + [norm_obs[0]]
            pot_c  = norm_pot + [norm_pot[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=pot_c, theta=lbls_c, name="🌟 Potencial",
                fill="toself",
                fillcolor="rgba(249,168,37,0.15)",
                line=dict(color="#F9A825", width=2, dash="dash"),
            ))
            fig.add_trace(go.Scatterpolar(
                r=obs_c, theta=lbls_c, name="✅ Observado",
                fill="toself",
                fillcolor="rgba(64,145,108,0.3)",
                line=dict(color="#2D6A4F", width=2.5),
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,10],
                           tickfont=dict(size=8))),
                legend=dict(orientation="h", yanchor="bottom", y=1.05),
                height=450, margin=dict(l=60,r=60,t=50,b=30),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.caption(f"Gráfico no disponible: {e}")

        # ── Per-petal summary table ───────────────────────────────────────
        st.markdown("**Detalle por pétalo:**")
        for i, p in enumerate(petalos):
            n_o = scores_obs[i] if i < len(scores_obs) else 0
            n_p = scores_pot[i] if i < len(scores_pot) else 0
            lv_o, em_o, co = _score_level(n_o)
            lv_p, em_p, cp = _score_level(n_p)
            gap = n_p - n_o
            gap_txt = f"+{gap} potencial" if gap > 0 else ("= alineado" if n_o > 0 else "")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;'                f'padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'                f'<span style="width:26px;">{PETAL_ICONS[i]}</span>'                f'<span style="flex:1;font-size:0.8rem;color:#1B4332;">{p["nombre"][:32]}</span>'                f'<span style="background:{co};color:white;border-radius:5px;'                f'padding:0.1rem 0.5rem;font-size:0.75rem;min-width:90px;text-align:center;">'                f'{em_o} {lv_o} ({n_o})</span>'                f'<span style="font-size:0.7rem;color:#888;min-width:80px;">{gap_txt}</span>'                f'</div>', unsafe_allow_html=True)

        # ── Single open field ─────────────────────────────────────────────
        st.markdown("---")
        data["pot_practicas_destacadas"] = st.text_area(
            "✨ Prácticas más destacadas del espacio",
            value=data.get("pot_practicas_destacadas",""),
            height=100, key="pot_destacadas",
            placeholder="¿Qué es lo más valioso que ya está ocurriendo en este espacio?")

    # ── Guardar ───────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("💾 Guardar Flor de la Permacultura", use_container_width=True,
                 type="primary", key="save_potencial"):
        st.session_state.visit_data = data
        save_visit(data)
        st.success("✅ Flor de la Permacultura guardada.")
        show_drive_save_status()
