"""Módulo 7 — Flor de la Permacultura v3.3
7 pétalos Holmgren · Navegación por botones · Sin rerun en selección · IPR.
"""
import json
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status
from utils.petal_content import PETAL_DESC, IPR_SCALE, IPR_WHAT_IS, IPR_OBS_VS_POT

# ── Datos embebidos (7 pétalos Holmgren, 2002) ────────────────────────────────
_PETALOS_DATA = [{"nombre": "Administración de la Tierra y la Naturaleza", "categorias": {"produccion_alimentaria_urbana": ["Huertos en balcones y terrazas", "Huertos en macetas recicladas", "Huertos verticales en muros o cercos", "Jardines comestibles en patios pequeños", "Huertos en azoteas o techos planos", "Microhuertos en ventanas", "Cultivo hidropónico doméstico", "Cultivo acuapónico doméstico", "Cultivo en bolsas de cultivo o contenedores textiles", "Huertos en patios comunitarios", "Huertos escolares", "Huertos en centros culturales", "Huertos en espacios públicos recuperados", "Guerrilla gardening", "Cultivo de microgreens", "Germinados en casa", "Cultivo de hongos comestibles", "Cultivo de setas en café reciclado"], "suelo_vivo": ["Vermicompostaje doméstico", "Compostaje en baldes", "Compostaje bokashi", "Compostaje comunitario en el barrio", "Compostaje en departamentos usando lombrices", "Creación de suelo vivo en macetas", "Uso de microorganismos eficientes", "Uso de bioles y biofertilizantes", "Producción de biochar", "Fabricación de té de compost"], "biodiversidad_urbana": ["Plantación de árboles frutales urbanos", "Corredores de polinizadores", "Jardines para abejas nativas", "Jardines de mariposas", "Jardines medicinales urbanos", "Jardines aromáticos", "Refugios para insectos", "Casas para murciélagos", "Bebederos para aves", "Restauración de pequeños espacios degradados", "Plantación de especies nativas en jardines"], "agua": ["Captación de agua lluvia en casas", "Captación de agua lluvia en edificios", "Barriles recolectores de agua", "Sistemas de infiltración en patios", "Micro zanjas de infiltración", "Reutilización de aguas grises para riego", "Riego por goteo casero", "Jardines de lluvia urbanos", "Micro humedales artificiales"], "semillas": ["Guardar semillas en casa", "Intercambio de semillas entre vecinos", "Bibliotecas de semillas", "Bancos comunitarios de semillas", "Cultivo de variedades locales", "Multiplicación de plantas por esquejes", "Propagación de plantas nativas"], "agua_domestica": ["Duchas cortas", "Cerrar la llave al lavar platos", "Reparar fugas de agua", "Reutilizar agua para riego"]}, "subtitulo": "Agricultura urbana, suelo vivo, biodiversidad y agua"}, {"nombre": "Entorno Construido", "categorias": {"vivienda_ecologica": ["Bioconstrucción en ampliaciones", "Uso de materiales naturales en remodelaciones", "Muros interiores de tierra o barro", "Pinturas naturales", "Aislación con materiales naturales"], "energia_pasiva": ["Diseño solar pasivo", "Ventilación cruzada en viviendas", "Uso de masas térmicas", "Sombreamiento natural con plantas", "Pérgolas verdes", "Enredaderas en fachadas"], "naturaleza_en_edificios": ["Techos verdes", "Muros verdes", "Jardines verticales comestibles", "Patios interiores con vegetación", "Balcones verdes"], "espacios_multifuncionales": ["Cocinas comunitarias", "Talleres compartidos", "Huertos en condominios", "Bodegas para alimentos comunitarios", "Espacios de compostaje en edificios"], "reutilizacion_materiales": ["Uso de pallets para jardinería", "Construcción con materiales reciclados", "Uso de ventanas recicladas para invernaderos", "Construcción de mini invernaderos", "Reutilización de contenedores"]}, "subtitulo": "Bioconstrucción, diseño bioclimático y espacios regenerativos"}, {"nombre": "Herramientas y Tecnología", "categorias": {"energia": ["Paneles solares domésticos", "Calentadores solares de agua", "Cocinas solares", "Secadores solares de alimentos", "Sistemas solares portátiles"], "tecnologias_simples": ["Estufas rocket", "Hornos de barro urbanos", "Biodigestores domésticos pequeños", "Sistemas de riego automatizado de bajo consumo", "Sensores de humedad del suelo"], "agua": ["Filtros de agua domésticos", "Biofiltros de aguas grises", "Sistemas de captación de condensación", "Sistemas de almacenamiento de agua"], "movilidad": ["Uso de bicicleta", "Bicicletas de carga", "Carros para transportar cosechas", "Talleres comunitarios de reparación de bicicletas"], "alimentos": ["Fermentación de alimentos", "Deshidratación solar", "Conservas caseras", "Almacenamiento natural de alimentos", "Refrigeración pasiva"], "energia_domestica": ["Apagar luces cuando no se usan", "Usar ampolletas LED", "Usar electrodomésticos de bajo consumo", "Desconectar cargadores", "Usar regletas con interruptor"]}, "subtitulo": "Energía renovable, tecnología simple y movilidad sostenible"}, {"nombre": "Educación y Cultura", "categorias": {"educacion_comunitaria": ["Talleres de agroecología urbana", "Talleres de compostaje", "Talleres de huertos urbanos", "Cursos de diseño regenerativo", "Intercambio de saberes tradicionales"], "educacion_practica": ["Aprendizaje basado en huertos", "Programas educativos en jardines escolares", "Programas de voluntariado ambiental", "Programas de mentoría en agroecología"], "cultura_regenerativa": ["Festivales de semillas", "Ferias de agricultura urbana", "Intercambio de plantas", "Cine ambiental comunitario", "Bibliotecas ecológicas"], "arte_y_comunidad": ["Murales ecológicos", "Música comunitaria", "Arte con materiales reciclados", "Teatro ambiental"], "redes": ["Redes de huertos urbanos", "Redes de semillas", "Redes de consumo local", "Redes de economía solidaria"], "desarrollo_personal_regenerativo": ["Estudiar sobre regeneración", "Practicar agroecología", "Practicar meditación", "Practicar tai chi", "Practicar yoga", "Participar en talleres de regeneración"]}, "subtitulo": "Saberes locales, arte comunitario y redes de conocimiento"}, {"nombre": "Salud y Bienestar Espiritual", "categorias": {"salud_fisica": ["Alimentación basada en plantas", "Consumo de alimentos locales", "Dietas agroecológicas", "Cocina saludable comunitaria"], "salud_mental": ["Jardinería terapéutica", "Baños de bosque urbanos", "Meditación en huertos", "Espacios de contemplación"], "medicina_natural": ["Cultivo de plantas medicinales", "Preparación de tinturas", "Preparación de pomadas", "Preparación de infusiones"], "comunidad": ["Grupos de apoyo comunitario", "Espacios de cuidado colectivo", "Redes de cuidado mutuo"], "movimiento": ["Yoga comunitario", "Tai chi en parques", "Caminatas ecológicas", "Bicicleteadas comunitarias"]}, "subtitulo": "Alimentación viva, plantas medicinales y bienestar integral"}, {"nombre": "Finanzas y Economía", "categorias": {"economia_local": ["Mercados agroecológicos", "Ferias de intercambio", "Canastas comunitarias", "Agricultura apoyada por la comunidad (CSA)"], "economias_solidarias": ["Cooperativas de producción", "Cooperativas de consumo", "Cooperativas de vivienda", "Bancos de tiempo"], "sistemas_alternativos": ["Monedas locales", "Plataformas de trueque", "Redes de intercambio de servicios"], "emprendimientos_regenerativos": ["Producción de alimentos locales", "Viveros urbanos", "Diseño de huertos urbanos", "Educación ambiental", "Consultoría regenerativa"], "consumo_responsable": ["Compras a productores locales", "Reducción de consumo", "Reparación de objetos", "Reutilización de materiales", "Compras colectivas de alimentos", "Comprar a granel", "Evitar plásticos de un solo uso"], "consumo_consciente": ["Comprar productos locales", "Comprar colectivamente", "Evitar envases innecesarios", "Reparar antes de comprar", "Compartir herramientas"]}, "subtitulo": "Mercados locales, economías solidarias y soberanía alimentaria"}, {"nombre": "Tenencia de la Tierra y Gobernanza Comunitaria", "categorias": {"organizacion_comunitaria": ["Asambleas barriales", "Consejos comunitarios", "Mesas ambientales locales"], "gestion_espacios": ["Recuperación de sitios eriazos", "Creación de huertos comunitarios", "Parques comestibles urbanos", "Jardines comunitarios"], "participacion_ciudadana": ["Participación en planificación urbana", "Presupuestos participativos", "Defensa de áreas verdes"], "modelos_propiedad": ["Cooperativas de vivienda", "Comunidades intencionales urbanas", "Fideicomisos de tierra comunitaria"], "redes_territoriales": ["Redes de agroecología urbana", "Redes de transición urbana", "Redes de resiliencia comunitaria"], "vida_comunitaria": ["Conectar con vecinos", "Participar en organizaciones locales", "Participar en huertos comunitarios", "Organizar actividades de barrio"]}, "subtitulo": "Uso colectivo del territorio y participación comunitaria"}]

PETAL_ICONS = ["🌳","🏡","🛠️","📚","🧘","💚","🤝"]


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


def _petal_done(data, i):
    obs = data.get(f"petalo_{i}_obs", {})
    new = data.get(f"petalo_{i}_pot_new", {})
    otros_obs = data.get(f"petalo_{i}_otros_obs", [])
    otros_new = data.get(f"petalo_{i}_otros_new", [])
    return (any(v for v in obs.values()) or
            any(v for v in new.values()) or
            bool(otros_obs) or bool(otros_new))


def render():
    data = st.session_state.get("visit_data", {})
    if not data.get("id"):
        st.warning("⚠️ Primero crea o carga un diagnóstico.")
        return

    st.markdown("## 🌸 Flor de la Permacultura")
    st.markdown(
        '<p class="module-subtitle">7 pétalos · Holmgren (2002) · Observado + Potencial · IPR</p>',
        unsafe_allow_html=True)

    # ── Estado del módulo ─────────────────────────────────────────────────
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

    # ── Source + IPR info ─────────────────────────────────────────────────
    with st.expander("ℹ️ ¿De dónde vienen los 7 pétalos? · ¿Qué es el IPR?", expanded=False):
        st.markdown("""
**Los 7 pétalos de la Flor de la Permacultura** fueron definidos por David Holmgren en
*Permacultura: Principios y senderos más allá de la sustentabilidad* (2002) como los
**7 ámbitos que deben transformarse** para transitar hacia una cultura sostenible.
No son arbitrarios: representan las dimensiones interconectadas de la vida humana que
la permacultura identifica como esenciales para el descenso creativo y la regeneración.

Esta herramienta incluye además un catálogo de prácticas urbanas y periurbanas para
cada pétalo — característica especial de LivLin que amplía la aplicabilidad del marco
en contextos de alta densidad poblacional.

📚 *Holmgren, D. (2002). Permacultura: Principios y senderos. Holmgren Design Services.*
https://permacultureprinciples.com/es/
        """)
        st.markdown("---")
        st.markdown(f"**{IPR_WHAT_IS}**")
        st.markdown(f"*{IPR_OBS_VS_POT}*")
        st.markdown("""
**Las prácticas identificadas son para implementar en corto y mediano plazo**,
acordes a las condiciones reales del espacio. La propuesta es avanzar progresivamente
en todos los pétalos — no es necesario comenzar por todos a la vez. Cada pétalo donde
exista al menos una práctica activa ya es un avance significativo.
        """)
        st.markdown("**Escala IPR:**")
        for lvl, n, _, meaning in IPR_SCALE:
            st.markdown(f"- **{lvl} ({n} prácticas):** {meaning}")

    # ── Navigation: button grid ──────────────────────────────────────────
    if "petal_active" not in st.session_state:
        st.session_state.petal_active = -1  # -1 = show summary

    st.markdown("**Navegar por pétalo:**")
    # Summary button
    is_summary = st.session_state.petal_active == -1
    sum_style = "primary" if is_summary else "secondary"
    c_cols = st.columns([2] + [1]*7)
    with c_cols[0]:
        if st.button("📊 Resumen IPR", type=sum_style, use_container_width=True,
                     key="btn_summary"):
            st.session_state.petal_active = -1
            st.rerun()
    for i, p in enumerate(petalos):
        done = _petal_done(data, i)
        badge = "✅" if done else "○"
        with c_cols[i+1]:
            is_active = st.session_state.petal_active == i
            btn_type = "primary" if is_active else "secondary"
            short = p['nombre'][:8] + "…" if len(p['nombre']) > 8 else p['nombre']
            if st.button(f"{badge} {PETAL_ICONS[i]}\n{short}",
                         type=btn_type, use_container_width=True,
                         key=f"btn_petal_{i}"):
                st.session_state.petal_active = i
                st.rerun()

    st.markdown("---")

    # ── Score accumulators ───────────────────────────────────────────────
    scores_obs = []
    scores_new = []
    for i in range(len(petalos)):
        obs_data  = data.get(f"petalo_{i}_obs", {})
        new_data  = data.get(f"petalo_{i}_pot_new", {})
        otros_obs = data.get(f"petalo_{i}_otros_obs", [])
        otros_new = data.get(f"petalo_{i}_otros_new", [])
        n_o = sum(len(v) for v in obs_data.values()) + len(otros_obs)
        n_n = sum(len(v) for v in new_data.values()) + len(otros_new)
        scores_obs.append(n_o)
        scores_new.append(n_n)

    # ══════════════════════════════════════════════════════════════════════
    active = st.session_state.petal_active

    if active == -1:
        # ── RESUMEN ───────────────────────────────────────────────────────
        st.markdown("### 📊 Resumen — Índice de Potencial Regenerativo (IPR)")

        data["ipr_obs"] = scores_obs
        data["ipr_new"] = scores_new
        data["ipr_tot"] = [o+n for o,n in zip(scores_obs,scores_new)]
        data["ipr_petalos"] = [p["nombre"] for p in petalos]

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
                fill="toself", fillcolor="rgba(82,183,136,0.12)",
                line=dict(color="#52B788", width=2, dash="dash")))
            fig.add_trace(go.Scatterpolar(
                r=norm_obs + [norm_obs[0]], theta=lbls_c,
                name="✅ Observado hoy",
                fill="toself", fillcolor="rgba(27,67,50,0.28)",
                line=dict(color="#1B4332", width=2.5)))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0,10],
                           tickfont=dict(size=8))),
                legend=dict(orientation="h", yanchor="bottom", y=1.05),
                height=420, margin=dict(l=60,r=60,t=50,b=30),
                paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True, key="radar_chart")

            # Store chart as image for reports
            try:
                img_bytes = fig.to_image(format="png", width=700, height=420)
                import base64
                data["ipr_radar_b64"] = base64.b64encode(img_bytes).decode()
            except Exception:
                pass
        except Exception as e:
            st.caption(f"Gráfico no disponible: {e}")

        st.markdown("**Detalle por pétalo:**")
        for i, p in enumerate(petalos):
            n_o = scores_obs[i]; n_n = scores_new[i]; n_t = n_o + n_n
            lv_o, em_o, co = _score_level(n_o)
            lv_t, em_t, ct = _score_level(n_t)
            done = "✅" if n_o > 0 else "○"
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;'                f'padding:0.3rem 0;border-bottom:1px solid #D8F3DC;">'                f'<span style="width:26px;">{PETAL_ICONS[i]}</span>'                f'<span style="flex:1;font-size:0.82rem;color:#1B4332;">{done} {p["nombre"][:36]}</span>'                f'<span style="background:{co};color:white;border-radius:5px;'                f'padding:0.1rem 0.4rem;font-size:0.72rem;min-width:90px;text-align:center;">'                f'{em_o} {lv_o} ({n_o})</span>'                f'<span style="color:#52B788;font-size:0.75rem;min-width:65px;">+{n_n} pot.</span>'                f'<span style="background:{ct};color:white;border-radius:5px;'                f'padding:0.1rem 0.4rem;font-size:0.72rem;min-width:75px;text-align:center;">'                f'{em_t} {lv_t}</span>'                f'</div>', unsafe_allow_html=True)

        st.markdown("---")
        data["pot_practicas_destacadas"] = st.text_area(
            "✨ Prácticas más destacadas del espacio",
            value=data.get("pot_practicas_destacadas",""), height=100,
            key="pot_destacadas",
            placeholder="¿Qué es lo más valioso que ya está ocurriendo en este espacio?")

    else:
        # ── PÉTALO INDIVIDUAL ─────────────────────────────────────────────
        petalo = petalos[active]
        icon   = PETAL_ICONS[active]
        st.markdown(f"### {icon} {petalo['nombre']}")

        with st.expander("📖 ¿Qué es este pétalo? · Holmgren (2002)", expanded=False):
            desc = PETAL_DESC.get(petalo["nombre"], {})
            if isinstance(desc, dict):
                st.markdown(f"**{desc.get('resumen','')}**")
                st.markdown(desc.get("detalle",""))
                for auth, tit, url in desc.get("referencias",[]):
                    st.markdown(f"- {auth} — *{tit}* · [{url}]({url})")

        kp = f"p{active}"
        saved_obs  = data.get(f"petalo_{active}_obs",      {})
        saved_new  = data.get(f"petalo_{active}_pot_new",  {})
        saved_otros_obs = data.get(f"petalo_{active}_otros_obs", [])
        saved_otros_new = data.get(f"petalo_{active}_otros_new", [])

        # ── OBSERVADO ────────────────────────────────────────────────────
        st.markdown(
            '<div style="background:#F0FFF4;border-radius:8px;padding:0.5rem 0.8rem;'            'border-left:4px solid #40916C;margin:0.5rem 0;">'            '<strong>✅ Observado</strong> — '            '<span style="font-size:0.8rem;color:#2D6A4F;">'            'Lo que ya ocurre en el espacio hoy. Selecciona todo lo que aplica.</span></div>',
            unsafe_allow_html=True)

        new_obs = {}
        for cat_key, acciones in petalo["categorias"].items():
            cat_label = cat_key.replace("_"," ").title()
            opts  = ["(Ninguno)"] + acciones
            prev  = [a for a in saved_obs.get(cat_key, []) if a in acciones]
            # NO rerun on change - collect all at once
            sel = st.multiselect(cat_label, options=opts, default=prev,
                                 key=f"{kp}_obs_{cat_key}",
                                 placeholder="Selecciona las que aplican…")
            new_obs[cat_key] = [s for s in sel if s != "(Ninguno)"]
        data[f"petalo_{active}_obs"] = new_obs

        # Otros observados
        otros_obs = list(saved_otros_obs)
        if otros_obs:
            for j, txt in enumerate(otros_obs):
                cc1, cc2 = st.columns([5,1])
                with cc1: st.caption(f"✅ {txt}")
                with cc2:
                    if st.button("✕", key=f"{kp}_del_obs_{j}"):
                        otros_obs.pop(j)
                        data[f"petalo_{active}_otros_obs"] = otros_obs
                        st.session_state.visit_data = data
                        st.rerun()
        nc1, nc2 = st.columns([4,1])
        with nc1:
            nuevo_obs = st.text_input("Otra práctica observada",
                key=f"{kp}_new_otro_obs", placeholder="Describe la práctica…",
                label_visibility="collapsed")
        with nc2:
            if st.button("+ Añadir", key=f"{kp}_add_obs", use_container_width=True):
                if nuevo_obs.strip():
                    otros_obs.append(nuevo_obs.strip())
                    data[f"petalo_{active}_otros_obs"] = otros_obs
                    st.session_state.visit_data = data
                    st.rerun()
        data[f"petalo_{active}_otros_obs"] = otros_obs

        st.markdown("---")

        # ── POTENCIAL ADICIONAL ──────────────────────────────────────────
        st.markdown(
            '<div style="background:#FFFBEB;border-radius:8px;padding:0.5rem 0.8rem;'            'border-left:4px solid #52B788;margin:0.5rem 0;">'            '<strong>🌟 Potencial adicional</strong> — '            '<span style="font-size:0.8rem;color:#2D6A4F;">'            'Nuevas prácticas viables (criterio facilitador). Las ya observadas no se repiten.</span></div>',
            unsafe_allow_html=True)

        new_new = {}
        for cat_key, acciones in petalo["categorias"].items():
            cat_label = cat_key.replace("_"," ").title()
            ya_obs    = new_obs.get(cat_key, [])
            opts_pot  = ["(Ninguno)"] + [a for a in acciones if a not in ya_obs]
            if len(opts_pot) == 1: continue
            prev = [a for a in saved_new.get(cat_key, [])
                    if a in acciones and a not in ya_obs]
            sel = st.multiselect(cat_label, options=opts_pot, default=prev,
                                 key=f"{kp}_pot_{cat_key}",
                                 placeholder="Nuevas acciones a sumar…")
            new_new[cat_key] = [s for s in sel if s != "(Ninguno)"]
        data[f"petalo_{active}_pot_new"] = new_new

        otros_new = list(saved_otros_new)
        if otros_new:
            for j, txt in enumerate(otros_new):
                cc1, cc2 = st.columns([5,1])
                with cc1: st.caption(f"🌟 {txt}")
                with cc2:
                    if st.button("✕", key=f"{kp}_del_new_{j}"):
                        otros_new.pop(j)
                        data[f"petalo_{active}_otros_new"] = otros_new
                        st.session_state.visit_data = data
                        st.rerun()
        nc1, nc2 = st.columns([4,1])
        with nc1:
            nuevo_new = st.text_input("Otra práctica potencial",
                key=f"{kp}_new_otro_new", placeholder="Nueva acción concreta…",
                label_visibility="collapsed")
        with nc2:
            if st.button("+ Añadir", key=f"{kp}_add_new", use_container_width=True):
                if nuevo_new.strip():
                    otros_new.append(nuevo_new.strip())
                    data[f"petalo_{active}_otros_new"] = otros_new
                    st.session_state.visit_data = data
                    st.rerun()
        data[f"petalo_{active}_otros_new"] = otros_new

        # Score display
        n_obs = sum(len(v) for v in new_obs.values()) + len(otros_obs)
        n_new = sum(len(v) for v in new_new.values()) + len(otros_new)
        lv_o, em_o, co = _score_level(n_obs)
        lv_t, em_t, ct = _score_level(n_obs + n_new)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f'<div style="background:{co};border-radius:8px;padding:0.4rem 0.7rem;'                f'color:white;text-align:center;">'                f'<div style="font-size:1.1rem;">{em_o}</div>'                f'<div style="font-size:0.8rem;font-weight:700;">{lv_o}</div>'                f'<div style="font-size:0.72rem;">Observado: {n_obs}</div></div>',
                unsafe_allow_html=True)
        with m2:
            st.markdown(
                f'<div style="background:#52B788;border-radius:8px;padding:0.4rem 0.7rem;'                f'color:white;text-align:center;">'                f'<div style="font-size:1.1rem;">+{n_new}</div>'                f'<div style="font-size:0.8rem;font-weight:700;">Potencial adicional</div>'                f'<div style="font-size:0.72rem;">nuevas prácticas</div></div>',
                unsafe_allow_html=True)
        with m3:
            st.markdown(
                f'<div style="background:{ct};border-radius:8px;padding:0.4rem 0.7rem;'                f'color:white;text-align:center;">'                f'<div style="font-size:1.1rem;">{em_t}</div>'                f'<div style="font-size:0.8rem;font-weight:700;">{lv_t}</div>'                f'<div style="font-size:0.72rem;">Total: {n_obs+n_new}</div></div>',
                unsafe_allow_html=True)

        st.markdown(f"*{_petal_narrative(petalo['nombre'], n_obs, n_new)}*")

        data[f"petalo_{active}_notas"] = st.text_area(
            "📝 Notas del facilitador para este pétalo",
            value=data.get(f"petalo_{active}_notas",""), height=70,
            key=f"{kp}_notas",
            placeholder="Contexto, condiciones específicas, oportunidades…")

    # ── Guardar ───────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("💾 Guardar Flor de la Permacultura", use_container_width=True,
                 type="primary", key="save_potencial"):
        st.session_state.visit_data = data
        save_visit(data)
        st.success("✅ Flor de la Permacultura guardada.")
        show_drive_save_status()
