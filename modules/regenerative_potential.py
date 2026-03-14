"""Módulo 7 — Flor de la Permacultura v2.1
Observado + Potencial ADICIONAL · Sin doble entrada · Radar dual · IPR.
"""
import json
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status

# ── Datos embebidos ───────────────────────────────────────────────────────────
_PETALOS_DATA = [{"nombre": "Manejo de la tierra y la naturaleza (urbano)", "categorias": {"produccion_alimentaria_urbana": ["Huertos en balcones y terrazas", "Huertos en macetas recicladas", "Huertos verticales en muros o cercos", "Jardines comestibles en patios pequeños", "Huertos en azoteas o techos planos", "Microhuertos en ventanas", "Cultivo hidropónico doméstico", "Cultivo acuapónico doméstico", "Cultivo en bolsas de cultivo o contenedores textiles", "Huertos en patios comunitarios", "Huertos escolares", "Huertos en centros culturales", "Huertos en espacios públicos recuperados", "Guerrilla gardening", "Cultivo de microgreens", "Germinados en casa", "Cultivo de hongos comestibles", "Cultivo de setas en café reciclado"], "suelo_vivo": ["Vermicompostaje doméstico", "Compostaje en baldes", "Compostaje bokashi", "Compostaje comunitario en el barrio", "Compostaje en departamentos usando lombrices", "Creación de suelo vivo en macetas", "Uso de microorganismos eficientes", "Uso de bioles y biofertilizantes", "Producción de biochar", "Fabricación de té de compost"], "biodiversidad_urbana": ["Plantación de árboles frutales urbanos", "Corredores de polinizadores", "Jardines para abejas nativas", "Jardines de mariposas", "Jardines medicinales urbanos", "Jardines aromáticos", "Refugios para insectos", "Casas para murciélagos", "Bebederos para aves", "Restauración de pequeños espacios degradados", "Plantación de especies nativas en jardines"], "agua": ["Captación de agua lluvia en casas", "Captación de agua lluvia en edificios", "Barriles recolectores de agua", "Sistemas de infiltración en patios", "Micro zanjas de infiltración", "Reutilización de aguas grises para riego", "Riego por goteo casero", "Jardines de lluvia urbanos", "Micro humedales artificiales"], "semillas": ["Guardar semillas en casa", "Intercambio de semillas entre vecinos", "Bibliotecas de semillas", "Bancos comunitarios de semillas", "Cultivo de variedades locales", "Multiplicación de plantas por esquejes", "Propagación de plantas nativas"]}}, {"nombre": "Ambiente construido", "categorias": {"vivienda_ecologica": ["Bioconstrucción en ampliaciones", "Uso de materiales naturales en remodelaciones", "Muros interiores de tierra o barro", "Pinturas naturales", "Aislación con materiales naturales"], "energia_pasiva": ["Diseño solar pasivo", "Ventilación cruzada en viviendas", "Uso de masas térmicas", "Sombreamiento natural con plantas", "Pérgolas verdes", "Enredaderas en fachadas"], "naturaleza_en_edificios": ["Techos verdes", "Muros verdes", "Jardines verticales comestibles", "Patios interiores con vegetación", "Balcones verdes"], "espacios_multifuncionales": ["Cocinas comunitarias", "Talleres compartidos", "Huertos en condominios", "Bodegas para alimentos comunitarios", "Espacios de compostaje en edificios"], "reutilizacion_materiales": ["Uso de pallets para jardinería", "Construcción con materiales reciclados", "Uso de ventanas recicladas para invernaderos", "Construcción de mini invernaderos", "Reutilización de contenedores"]}}, {"nombre": "Herramientas y tecnologías apropiadas", "categorias": {"energia": ["Paneles solares domésticos", "Calentadores solares de agua", "Cocinas solares", "Secadores solares de alimentos", "Sistemas solares portátiles"], "tecnologias_simples": ["Estufas rocket", "Hornos de barro urbanos", "Biodigestores domésticos pequeños", "Sistemas de riego automatizado de bajo consumo", "Sensores de humedad del suelo"], "agua": ["Filtros de agua domésticos", "Biofiltros de aguas grises", "Sistemas de captación de condensación", "Sistemas de almacenamiento de agua"], "movilidad": ["Uso de bicicleta", "Bicicletas de carga", "Carros para transportar cosechas", "Talleres comunitarios de reparación de bicicletas"], "alimentos": ["Fermentación de alimentos", "Deshidratación solar", "Conservas caseras", "Almacenamiento natural de alimentos", "Refrigeración pasiva"]}}, {"nombre": "Educación y cultura", "categorias": {"educacion_comunitaria": ["Talleres de agroecología urbana", "Talleres de compostaje", "Talleres de huertos urbanos", "Cursos de diseño regenerativo", "Intercambio de saberes tradicionales"], "educacion_practica": ["Aprendizaje basado en huertos", "Programas educativos en jardines escolares", "Programas de voluntariado ambiental", "Programas de mentoría en agroecología"], "cultura_regenerativa": ["Festivales de semillas", "Ferias de agricultura urbana", "Intercambio de plantas", "Cine ambiental comunitario", "Bibliotecas ecológicas"], "arte_y_comunidad": ["Murales ecológicos", "Música comunitaria", "Arte con materiales reciclados", "Teatro ambiental"], "redes": ["Redes de huertos urbanos", "Redes de semillas", "Redes de consumo local", "Redes de economía solidaria"]}}, {"nombre": "Salud y bienestar", "categorias": {"salud_fisica": ["Alimentación basada en plantas", "Consumo de alimentos locales", "Dietas agroecológicas", "Cocina saludable comunitaria"], "salud_mental": ["Jardinería terapéutica", "Baños de bosque urbanos", "Meditación en huertos", "Espacios de contemplación"], "medicina_natural": ["Cultivo de plantas medicinales", "Preparación de tinturas", "Preparación de pomadas", "Preparación de infusiones"], "comunidad": ["Grupos de apoyo comunitario", "Espacios de cuidado colectivo", "Redes de cuidado mutuo"], "movimiento": ["Yoga comunitario", "Tai chi en parques", "Caminatas ecológicas", "Bicicleteadas comunitarias"]}}, {"nombre": "Economía y finanzas", "categorias": {"economia_local": ["Mercados agroecológicos", "Ferias de intercambio", "Canastas comunitarias", "Agricultura apoyada por la comunidad (CSA)"], "economias_solidarias": ["Cooperativas de producción", "Cooperativas de consumo", "Cooperativas de vivienda", "Bancos de tiempo"], "sistemas_alternativos": ["Monedas locales", "Plataformas de trueque", "Redes de intercambio de servicios"], "emprendimientos_regenerativos": ["Producción de alimentos locales", "Viveros urbanos", "Diseño de huertos urbanos", "Educación ambiental", "Consultoría regenerativa"], "consumo_responsable": ["Compras a productores locales", "Reducción de consumo", "Reparación de objetos", "Reutilización de materiales", "Compras colectivas de alimentos", "Comprar a granel", "Evitar plásticos de un solo uso"]}}, {"nombre": "Tenencia de la tierra y gobernanza", "categorias": {"organizacion_comunitaria": ["Asambleas barriales", "Consejos comunitarios", "Mesas ambientales locales"], "gestion_espacios": ["Recuperación de sitios eriazos", "Creación de huertos comunitarios", "Parques comestibles urbanos", "Jardines comunitarios"], "participacion_ciudadana": ["Participación en planificación urbana", "Presupuestos participativos", "Defensa de áreas verdes"], "modelos_propiedad": ["Cooperativas de vivienda", "Comunidades intencionales urbanas", "Fideicomisos de tierra comunitaria"], "redes_territoriales": ["Redes de agroecología urbana", "Redes de transición urbana", "Redes de resiliencia comunitaria"]}}, {"nombre": "Prácticas cotidianas de sustentabilidad", "categorias": {"energia_domestica": ["Apagar luces cuando no se usan", "Usar ampolletas LED", "Usar electrodomésticos de bajo consumo", "Desconectar cargadores", "Usar regletas con interruptor"], "agua_domestica": ["Duchas cortas", "Cerrar la llave al lavar platos", "Reparar fugas de agua", "Reutilizar agua para riego"], "consumo_consciente": ["Comprar productos locales", "Comprar colectivamente", "Evitar envases innecesarios", "Reparar antes de comprar", "Compartir herramientas"], "vida_comunitaria": ["Conectar con vecinos", "Participar en organizaciones locales", "Participar en huertos comunitarios", "Organizar actividades de barrio"], "desarrollo_personal_regenerativo": ["Estudiar sobre regeneración", "Practicar agroecología", "Practicar meditación", "Practicar tai chi", "Practicar yoga", "Participar en talleres de regeneración"]}}]


# ── Contenido compartido (misma fuente que Excel y Word) ────────────────────
from utils.petal_content import PETAL_DESC, PETAL_ICONS, IPR_SCALE, IPR_WHAT_IS, IPR_OBS_VS_POT
# ── Scoring ───────────────────────────────────────────────────────────────────
def _score_level(n: int) -> tuple:
    if n == 0: return "Sin inicio",  "○",  "#BDBDBD"
    if n == 1: return "Iniciando",   "🌱", "#74C69D"
    if n == 2: return "Avanzando",   "🌿", "#52B788"
    if n == 3: return "Consolidado", "🌳", "#40916C"
    if n <= 5: return "Destacado",   "🌸", "#2D6A4F"
    return           "Referente",   "✨", "#1B4332"

def _petal_narrative(petal_name: str, n_obs: int, n_new: int) -> str:
    lev_obs, em_obs, _ = _score_level(n_obs)
    total_pot = n_obs + n_new
    lev_tot,  em_tot,  _ = _score_level(total_pot)
    parts = []
    if n_obs == 0:
        parts.append(f"Este espacio está en etapa inicial en **{petal_name}**. Cada primera acción es el paso más importante.")
    else:
        parts.append(f"{em_obs} **{lev_obs}** — {n_obs} práctica(s) activa(s) registradas.")
    if n_new > 0:
        parts.append(f"El facilitador identifica **{n_new} práctica(s) adicional(es)** con potencial concreto para este espacio.")
        parts.append(f"Con esas incorporaciones, el pétalo alcanzaría nivel {em_tot} **{lev_tot}** ({total_pot} prácticas).")
    elif n_obs > 0:
        parts.append("El facilitador no identifica nuevas incorporaciones inmediatas — el nivel actual está bien consolidado.")
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
        '<p class="module-subtitle">Índice de Potencial Regenerativo (IPR) · Observado + Potencial adicional</p>',
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
        st.error("❌ No se pudieron cargar los datos.")
        return

    # ── Info IPR ──────────────────────────────────────────────────────────
    with st.expander("ℹ️ ¿Qué es el Índice de Potencial Regenerativo (IPR)?", expanded=False):
        st.markdown(f"**¿Qué es el IPR?** {IPR_WHAT_IS}")
        st.markdown(f"**Observado vs Potencial:** {IPR_OBS_VS_POT}")
        st.markdown("**Escala de niveles:**")
        rows = []
        for lvl, n, color, meaning in IPR_SCALE:
            rows.append(f"| {lvl} | {n} | {meaning} |")
        table_md = "| Nivel | N° prácticas | Significado |\n|-------|-------------|-------------|\n" + "\n".join(rows)
        st.markdown(table_md)
        st.markdown("📚 *Holmgren, D. (2002). Permacultura: Principios y senderos. · www.livlin.com*")

    # ── Tabs ─────────────────────────────────────────────────────────────
    tab_labels = [f"{PETAL_ICONS[i]} {p['nombre'][:20]}" for i, p in enumerate(petalos)]
    tab_labels.append("📊 Resumen IPR")
    tabs = st.tabs(tab_labels)

    scores_obs = []
    scores_new = []

    for i, (tab, petalo) in enumerate(zip(tabs[:-1], petalos)):
        with tab:
            icon = PETAL_ICONS[i]
            st.markdown(f"### {icon} {petalo['nombre']}")

            with st.expander("📖 ¿Qué es este pétalo? · Referencias", expanded=False):
                desc = PETAL_DESC.get(petalo["nombre"], {})
                if isinstance(desc, dict):
                    st.markdown(f"**{desc.get('resumen','')}**")
                    st.markdown(desc.get("detalle",""))
                    refs = desc.get("referencias", [])
                    if refs:
                        st.markdown("📚 **Referencias:**")
                        for author, title, url in refs:
                            st.markdown(f"- {author} — *{title}* · [{url}]({url})")
                else:
                    st.markdown(str(desc))

            kp = f"p{i}"
            saved_obs  = data.get(f"petalo_{i}_obs",      {})
            saved_new  = data.get(f"petalo_{i}_pot_new",  {})
            saved_otros_obs = data.get(f"petalo_{i}_otros_obs", [])
            saved_otros_new = data.get(f"petalo_{i}_otros_new", [])

            new_obs = {}
            new_new = {}
            sel_obs_all = []
            sel_new_all = []

            # ── OBSERVADO ────────────────────────────────────────────────
            st.markdown(
                '<div style="background:#E8F5E9;border-radius:8px;padding:0.5rem 0.8rem;'
                'border-left:4px solid #40916C;margin:0.5rem 0;">'
                '<strong>✅ Observado</strong> — '
                '<span style="font-size:0.8rem;color:#2D6A4F;">'
                'Lo que ya ocurre en el espacio hoy</span></div>',
                unsafe_allow_html=True)

            for cat_key, acciones in petalo["categorias"].items():
                cat_label = cat_key.replace("_"," ").title()
                opts  = ["(Ninguno)"] + acciones
                prev  = [a for a in saved_obs.get(cat_key, []) if a in acciones]
                sel   = st.multiselect(cat_label, options=opts, default=prev,
                                       key=f"{kp}_obs_{cat_key}", placeholder="Selecciona…")
                clean = [s for s in sel if s != "(Ninguno)"]
                new_obs[cat_key] = clean
                sel_obs_all.extend(clean)

            # Otros observados
            otros_obs = list(saved_otros_obs)
            if otros_obs:
                for j, txt in enumerate(otros_obs):
                    c1, c2 = st.columns([5,1])
                    with c1: st.caption(f"✅ {txt}")
                    with c2:
                        if st.button("✕", key=f"{kp}_del_obs_{j}"):
                            otros_obs.pop(j); st.rerun()
            with st.container():
                nc1, nc2 = st.columns([4,1])
                with nc1:
                    nuevo_obs = st.text_input("Otra práctica observada",
                        key=f"{kp}_new_otro_obs", placeholder="Describe la práctica…",
                        label_visibility="collapsed")
                with nc2:
                    if st.button("+ Añadir", key=f"{kp}_add_obs", use_container_width=True):
                        if nuevo_obs.strip():
                            otros_obs.append(nuevo_obs.strip()); st.rerun()
            data[f"petalo_{i}_otros_obs"] = otros_obs
            sel_obs_all.extend(otros_obs)
            data[f"petalo_{i}_obs"] = new_obs

            n_obs = len(sel_obs_all)
            lv_o, em_o, co = _score_level(n_obs)
            st.markdown(
                f'<div style="background:{co};border-radius:6px;padding:0.3rem 0.8rem;'
                f'color:white;display:inline-block;margin:0.3rem 0;">'
                f'{em_o} <strong>{lv_o}</strong> — {n_obs} práctica(s) observada(s)</div>',
                unsafe_allow_html=True)

            st.markdown("---")

            # ── POTENCIAL ADICIONAL ───────────────────────────────────────
            st.markdown(
                '<div style="background:#FFF8E1;border-radius:8px;padding:0.5rem 0.8rem;'
                'border-left:4px solid #F9A825;margin:0.5rem 0;">'
                '<strong>🌟 Potencial adicional</strong> — '
                '<span style="font-size:0.8rem;color:#E65100;">'
                'Nuevas prácticas viables para este espacio (criterio facilitador). '
                'Las ya observadas no se repiten aquí.</span></div>',
                unsafe_allow_html=True)

            for cat_key, acciones in petalo["categorias"].items():
                cat_label = cat_key.replace("_"," ").title()
                # Exclude already observed to avoid double entry
                ya_obs  = new_obs.get(cat_key, [])
                opts_pot = ["(Ninguno)"] + [a for a in acciones if a not in ya_obs]
                if len(opts_pot) == 1:
                    continue  # all actions already observed in this category
                prev = [a for a in saved_new.get(cat_key, [])
                        if a in acciones and a not in ya_obs]
                sel  = st.multiselect(cat_label, options=opts_pot, default=prev,
                                      key=f"{kp}_pot_{cat_key}",
                                      placeholder="Nuevas acciones a sumar…")
                clean = [s for s in sel if s != "(Ninguno)"]
                new_new[cat_key] = clean
                sel_new_all.extend(clean)

            # Otros potencial
            otros_new = list(saved_otros_new)
            if otros_new:
                for j, txt in enumerate(otros_new):
                    c1, c2 = st.columns([5,1])
                    with c1: st.caption(f"🌟 {txt}")
                    with c2:
                        if st.button("✕", key=f"{kp}_del_new_{j}"):
                            otros_new.pop(j); st.rerun()
            with st.container():
                nc1, nc2 = st.columns([4,1])
                with nc1:
                    nuevo_new = st.text_input("Otra práctica potencial",
                        key=f"{kp}_new_otro_new", placeholder="Nueva acción concreta…",
                        label_visibility="collapsed")
                with nc2:
                    if st.button("+ Añadir", key=f"{kp}_add_new", use_container_width=True):
                        if nuevo_new.strip():
                            otros_new.append(nuevo_new.strip()); st.rerun()
            data[f"petalo_{i}_otros_new"] = otros_new
            sel_new_all.extend(otros_new)
            data[f"petalo_{i}_pot_new"] = new_new

            scores_obs.append(n_obs)
            scores_new.append(len(sel_new_all))

            # Score summary
            n_new = len(sel_new_all)
            n_tot = n_obs + n_new
            lv_t, em_t, ct = _score_level(n_tot)
            lv_n, em_n, cn = _score_level(n_new)

            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(
                    f'<div style="background:{co};border-radius:8px;padding:0.4rem 0.7rem;'
                    f'color:white;text-align:center;">'
                    f'<div style="font-size:1.1rem;">{em_o}</div>'
                    f'<div style="font-size:0.8rem;font-weight:700;">{lv_o}</div>'
                    f'<div style="font-size:0.72rem;">Observado: {n_obs}</div></div>',
                    unsafe_allow_html=True)
            with m2:
                st.markdown(
                    f'<div style="background:#F9A825;border-radius:8px;padding:0.4rem 0.7rem;'
                    f'color:white;text-align:center;">'
                    f'<div style="font-size:1.1rem;">+{n_new}</div>'
                    f'<div style="font-size:0.8rem;font-weight:700;">Potencial adicional</div>'
                    f'<div style="font-size:0.72rem;">nuevas prácticas</div></div>',
                    unsafe_allow_html=True)
            with m3:
                st.markdown(
                    f'<div style="background:{ct};border-radius:8px;padding:0.4rem 0.7rem;'
                    f'color:white;text-align:center;">'
                    f'<div style="font-size:1.1rem;">{em_t}</div>'
                    f'<div style="font-size:0.8rem;font-weight:700;">{lv_t}</div>'
                    f'<div style="font-size:0.72rem;">Total con potencial: {n_tot}</div></div>',
                    unsafe_allow_html=True)

            st.markdown(f"*{_petal_narrative(petalo['nombre'], n_obs, n_new)}*")

            data[f"petalo_{i}_notas"] = st.text_area(
                "📝 Notas del facilitador",
                value=data.get(f"petalo_{i}_notas",""), height=70,
                key=f"{kp}_notas",
                placeholder="Contexto, condiciones específicas, oportunidades concretas…")

    # ══════════════════════════════════════════════════════════════════════
    with tabs[-1]:
        st.markdown("### 📊 Resumen — Índice de Potencial Regenerativo (IPR)")

        data["ipr_obs"] = scores_obs
        data["ipr_new"] = scores_new
        data["ipr_tot"] = [o + n for o, n in zip(scores_obs, scores_new)]
        data["ipr_petalos"] = [p["nombre"] for p in petalos]

        # Dual radar
        try:
            import plotly.graph_objects as go
            labels = [f"{PETAL_ICONS[i]} {p['nombre'][:18]}"
                      for i, p in enumerate(petalos)]
            scores_tot = data["ipr_tot"]
            max_v = max(max(scores_obs + scores_tot, default=1), 1)

            norm_obs = [min(s/max_v*10, 10) for s in scores_obs]
            norm_tot = [min(s/max_v*10, 10) for s in scores_tot]
            lbls_c = labels + [labels[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=norm_tot + [norm_tot[0]], theta=lbls_c,
                name="🌟 Con potencial adicional",
                fill="toself", fillcolor="rgba(249,168,37,0.12)",
                line=dict(color="#F9A825", width=2, dash="dash")))
            fig.add_trace(go.Scatterpolar(
                r=norm_obs + [norm_obs[0]], theta=lbls_c,
                name="✅ Observado hoy",
                fill="toself", fillcolor="rgba(64,145,108,0.28)",
                line=dict(color="#2D6A4F", width=2.5)))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,10],
                           tickfont=dict(size=8))),
                legend=dict(orientation="h", yanchor="bottom", y=1.05),
                height=450, margin=dict(l=60,r=60,t=50,b=30),
                paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.caption(f"Gráfico no disponible: {e}")

        st.markdown("**Detalle por pétalo:**")
        for i, p in enumerate(petalos):
            n_o = scores_obs[i] if i < len(scores_obs) else 0
            n_n = scores_new[i] if i < len(scores_new) else 0
            n_t = n_o + n_n
            lv_o, em_o, co = _score_level(n_o)
            lv_t, em_t, ct = _score_level(n_t)
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;'
                f'padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
                f'<span style="width:26px;">{PETAL_ICONS[i]}</span>'
                f'<span style="flex:1;font-size:0.8rem;color:#1B4332;">{p["nombre"][:34]}</span>'
                f'<span style="background:{co};color:white;border-radius:5px;'
                f'padding:0.1rem 0.4rem;font-size:0.72rem;min-width:95px;text-align:center;">'
                f'{em_o} {lv_o} ({n_o})</span>'
                f'<span style="color:#F9A825;font-size:0.75rem;min-width:60px;">+{n_n} pot.</span>'
                f'<span style="background:{ct};color:white;border-radius:5px;'
                f'padding:0.1rem 0.4rem;font-size:0.72rem;min-width:75px;text-align:center;">'
                f'{em_t} {lv_t}</span>'
                f'</div>', unsafe_allow_html=True)

        st.markdown("---")
        data["pot_practicas_destacadas"] = st.text_area(
            "✨ Prácticas más destacadas del espacio",
            value=data.get("pot_practicas_destacadas",""), height=100,
            key="pot_destacadas",
            placeholder="¿Qué es lo más valioso que ya está ocurriendo en este espacio?")

    st.markdown("---")
    if st.button("💾 Guardar Flor de la Permacultura", use_container_width=True,
                 type="primary", key="save_potencial"):
        st.session_state.visit_data = data
        save_visit(data)
        st.success("✅ Flor de la Permacultura guardada.")
        show_drive_save_status()
