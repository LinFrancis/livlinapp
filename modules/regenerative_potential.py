"""Módulo 7 — Flor de la Permacultura v13.
Acciones por pétalo y subcategoría + IPR (Indicador de Potencial Regenerativo).
"""
import json
import streamlit as st
from pathlib import Path
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status
from utils.scoring import SCORE_SCALE

# ── Cargar base de acciones ───────────────────────────────────────────────────
# JSON embebido directamente como fallback garantizado
_PETALOS_EMBEDDED = '{"petalos": [{"nombre": "Manejo de la tierra y la naturaleza (urbano)", "categorias": {"produccion_alimentaria_urbana": ["Huertos en balcones y terrazas", "Huertos en macetas recicladas", "Huertos verticales en muros o cercos", "Jardines comestibles en patios pequeños", "Huertos en azoteas o techos planos", "Microhuertos en ventanas", "Cultivo hidropónico doméstico", "Cultivo acuapónico doméstico", "Cultivo en bolsas de cultivo o contenedores textiles", "Huertos en patios comunitarios", "Huertos escolares", "Huertos en centros culturales", "Huertos en espacios públicos recuperados", "Guerrilla gardening", "Cultivo de microgreens", "Germinados en casa", "Cultivo de hongos comestibles", "Cultivo de setas en café reciclado"], "suelo_vivo": ["Vermicompostaje doméstico", "Compostaje en baldes", "Compostaje bokashi", "Compostaje comunitario en el barrio", "Compostaje en departamentos usando lombrices", "Creación de suelo vivo en macetas", "Uso de microorganismos eficientes", "Uso de bioles y biofertilizantes", "Producción de biochar", "Fabricación de té de compost"], "biodiversidad_urbana": ["Plantación de árboles frutales urbanos", "Corredores de polinizadores", "Jardines para abejas nativas", "Jardines de mariposas", "Jardines medicinales urbanos", "Jardines aromáticos", "Refugios para insectos", "Casas para murciélagos", "Bebederos para aves", "Restauración de pequeños espacios degradados", "Plantación de especies nativas en jardines"], "agua": ["Captación de agua lluvia en casas", "Captación de agua lluvia en edificios", "Barriles recolectores de agua", "Sistemas de infiltración en patios", "Micro zanjas de infiltración", "Reutilización de aguas grises para riego", "Riego por goteo casero", "Jardines de lluvia urbanos", "Micro humedales artificiales"], "semillas": ["Guardar semillas en casa", "Intercambio de semillas entre vecinos", "Bibliotecas de semillas", "Bancos comunitarios de semillas", "Cultivo de variedades locales", "Multiplicación de plantas por esquejes", "Propagación de plantas nativas"]}}, {"nombre": "Ambiente construido", "categorias": {"vivienda_ecologica": ["Bioconstrucción en ampliaciones", "Uso de materiales naturales en remodelaciones", "Muros interiores de tierra o barro", "Pinturas naturales", "Aislación con materiales naturales"], "energia_pasiva": ["Diseño solar pasivo", "Ventilación cruzada en viviendas", "Uso de masas térmicas", "Sombreamiento natural con plantas", "Pérgolas verdes", "Enredaderas en fachadas"], "naturaleza_en_edificios": ["Techos verdes", "Muros verdes", "Jardines verticales comestibles", "Patios interiores con vegetación", "Balcones verdes"], "espacios_multifuncionales": ["Cocinas comunitarias", "Talleres compartidos", "Huertos en condominios", "Bodegas para alimentos comunitarios", "Espacios de compostaje en edificios"], "reutilizacion_materiales": ["Uso de pallets para jardinería", "Construcción con materiales reciclados", "Uso de ventanas recicladas para invernaderos", "Construcción de mini invernaderos", "Reutilización de contenedores"]}}, {"nombre": "Herramientas y tecnologías apropiadas", "categorias": {"energia": ["Paneles solares domésticos", "Calentadores solares de agua", "Cocinas solares", "Secadores solares de alimentos", "Sistemas solares portátiles"], "tecnologias_simples": ["Estufas rocket", "Hornos de barro urbanos", "Biodigestores domésticos pequeños", "Sistemas de riego automatizado de bajo consumo", "Sensores de humedad del suelo"], "agua": ["Filtros de agua domésticos", "Biofiltros de aguas grises", "Sistemas de captación de condensación", "Sistemas de almacenamiento de agua"], "movilidad": ["Uso de bicicleta", "Bicicletas de carga", "Carros para transportar cosechas", "Talleres comunitarios de reparación de bicicletas"], "alimentos": ["Fermentación de alimentos", "Deshidratación solar", "Conservas caseras", "Almacenamiento natural de alimentos", "Refrigeración pasiva"]}}, {"nombre": "Educación y cultura", "categorias": {"educacion_comunitaria": ["Talleres de agroecología urbana", "Talleres de compostaje", "Talleres de huertos urbanos", "Cursos de diseño regenerativo", "Intercambio de saberes tradicionales"], "educacion_practica": ["Aprendizaje basado en huertos", "Programas educativos en jardines escolares", "Programas de voluntariado ambiental", "Programas de mentoría en agroecología"], "cultura_regenerativa": ["Festivales de semillas", "Ferias de agricultura urbana", "Intercambio de plantas", "Cine ambiental comunitario", "Bibliotecas ecológicas"], "arte_y_comunidad": ["Murales ecológicos", "Música comunitaria", "Arte con materiales reciclados", "Teatro ambiental"], "redes": ["Redes de huertos urbanos", "Redes de semillas", "Redes de consumo local", "Redes de economía solidaria"]}}, {"nombre": "Salud y bienestar", "categorias": {"salud_fisica": ["Alimentación basada en plantas", "Consumo de alimentos locales", "Dietas agroecológicas", "Cocina saludable comunitaria"], "salud_mental": ["Jardinería terapéutica", "Baños de bosque urbanos", "Meditación en huertos", "Espacios de contemplación"], "medicina_natural": ["Cultivo de plantas medicinales", "Preparación de tinturas", "Preparación de pomadas", "Preparación de infusiones"], "comunidad": ["Grupos de apoyo comunitario", "Espacios de cuidado colectivo", "Redes de cuidado mutuo"], "movimiento": ["Yoga comunitario", "Tai chi en parques", "Caminatas ecológicas", "Bicicleteadas comunitarias"]}}, {"nombre": "Economía y finanzas", "categorias": {"economia_local": ["Mercados agroecológicos", "Ferias de intercambio", "Canastas comunitarias", "Agricultura apoyada por la comunidad (CSA)"], "economias_solidarias": ["Cooperativas de producción", "Cooperativas de consumo", "Cooperativas de vivienda", "Bancos de tiempo"], "sistemas_alternativos": ["Monedas locales", "Plataformas de trueque", "Redes de intercambio de servicios"], "emprendimientos_regenerativos": ["Producción de alimentos locales", "Viveros urbanos", "Diseño de huertos urbanos", "Educación ambiental", "Consultoría regenerativa"], "consumo_responsable": ["Compras a productores locales", "Reducción de consumo", "Reparación de objetos", "Reutilización de materiales", "Compras colectivas de alimentos", "Comprar a granel", "Evitar plásticos de un solo uso"]}}, {"nombre": "Tenencia de la tierra y gobernanza", "categorias": {"organizacion_comunitaria": ["Asambleas barriales", "Consejos comunitarios", "Mesas ambientales locales"], "gestion_espacios": ["Recuperación de sitios eriazos", "Creación de huertos comunitarios", "Parques comestibles urbanos", "Jardines comunitarios"], "participacion_ciudadana": ["Participación en planificación urbana", "Presupuestos participativos", "Defensa de áreas verdes"], "modelos_propiedad": ["Cooperativas de vivienda", "Comunidades intencionales urbanas", "Fideicomisos de tierra comunitaria"], "redes_territoriales": ["Redes de agroecología urbana", "Redes de transición urbana", "Redes de resiliencia comunitaria"]}}, {"nombre": "Prácticas cotidianas de sustentabilidad", "categorias": {"energia_domestica": ["Apagar luces cuando no se usan", "Usar ampolletas LED", "Usar electrodomésticos de bajo consumo", "Desconectar cargadores", "Usar regletas con interruptor"], "agua_domestica": ["Duchas cortas", "Cerrar la llave al lavar platos", "Reparar fugas de agua", "Reutilizar agua para riego"], "consumo_consciente": ["Comprar productos locales", "Comprar colectivamente", "Evitar envases innecesarios", "Reparar antes de comprar", "Compartir herramientas"], "vida_comunitaria": ["Conectar con vecinos", "Participar en organizaciones locales", "Participar en huertos comunitarios", "Organizar actividades de barrio"], "desarrollo_personal_regenerativo": ["Estudiar sobre regeneración", "Practicar agroecología", "Practicar meditación", "Practicar tai chi", "Practicar yoga", "Participar en talleres de regeneración"]}}]}'

@st.cache_data
def _load_petalos() -> list:
    """Load from file if available, otherwise use embedded data."""
    for candidate in [
        Path(__file__).parent.parent / "data" / "petalos_regeneracion_urbana.json",
        Path(__file__).parent / ".." / "data" / "petalos_regeneracion_urbana.json",
    ]:
        try:
            if candidate.exists():
                with open(candidate, encoding="utf-8") as f:
                    return json.load(f)["petalos"]
        except Exception:
            pass
    # Fallback: use embedded data
    return json.loads(_PETALOS_EMBEDDED)["petalos"]

# Iconos por pétalo (orden del JSON)
PETAL_ICONS = ["🌳","🏡","🛠️","📚","🧘","💚","🤝","🌿"]

# Niveles de madurez IPR
def _ipr_level(pct: float) -> tuple[str, str]:
    if pct < 26:   return "🌱 Semilla",    "#74C69D"
    if pct < 51:   return "🌿 Brote",      "#52B788"
    if pct < 76:   return "🌳 Crecimiento","#40916C"
    return              "🌸 Floración",  "#1B4332"

def _narrative_for_petal(petal_name: str, pct: float, selected: list) -> str:
    level, _ = _ipr_level(pct)
    n = len(selected)
    if pct < 26:
        return (f"Con {n} práctica(s) activa(s), este pétalo está en etapa {level}. "
                f"Es el momento ideal para la observación activa y el diseño inicial. "
                f"Cada pequeña acción que sumes aquí construirá la base del sistema.")
    if pct < 51:
        return (f"{level} — {n} prácticas establecidas en {petal_name}. "
                f"Las estructuras básicas están tomando forma. "
                f"El sistema empieza a responder y producir sus primeros frutos.")
    if pct < 76:
        return (f"¡{level}! Con {n} prácticas integradas, {petal_name} muestra alta integración. "
                f"El sistema genera rendimientos constantes. Busca las conexiones entre prácticas "
                f"para multiplicar el efecto regenerativo.")
    return (f"🌸 {level} — {petal_name} es un referente de regeneración. "
            f"{n} prácticas activas muestran un sistema resiliente y autónomo, "
            f"capaz de compartir sus excedentes con la comunidad.")

def _global_narrative(scores: list[float], petalos: list) -> str:
    avg = sum(scores) / len(scores) if scores else 0
    top = [(petalos[i]["nombre"], s) for i, s in enumerate(scores)]
    top.sort(key=lambda x: x[1], reverse=True)
    strongest = top[0][0] if top else "—"
    weakest   = top[-1][0] if top else "—"
    level, _  = _ipr_level(avg)
    return (f"**{level} — IPR Global: {avg:.0f}%**\n\n"
            f"Tu espacio muestra su mayor vitalidad en **{strongest}**, donde las prácticas "
            f"están más consolidadas. El área con mayor potencial de crecimiento es "
            f"**{weakest}** — una oportunidad para nuevas semillas regenerativas.\n\n"
            f"Recuerda: cada práctica que integras no solo transforma tu espacio, "
            f"también inspira a quienes te rodean. Eres agente de cambio en tu comunidad. 🌱")

def render():
    data = st.session_state.get("visit_data", {})
    if not data.get("id"):
        st.warning("⚠️ Primero crea o carga un diagnóstico desde el panel de administración.")
        return

    st.markdown("## 🌸 Flor de la Permacultura")
    st.markdown('<p class="module-subtitle">Acciones regenerativas activas en tu espacio · IPR por pétalo</p>',
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
        st.info("🔍 **Modo inferido** — Las respuestas son interpretaciones del facilitador.")
    st.markdown("---")

    petalos = _load_petalos()

    # ── Tabs: una por pétalo + resumen ────────────────────────────────────
    tab_labels = [f"{PETAL_ICONS[i]} {p['nombre'][:22]}" for i, p in enumerate(petalos)]
    tab_labels.append("📊 Resumen IPR")
    tabs = st.tabs(tab_labels)

    ipr_scores = []

    for i, (tab, petalo) in enumerate(zip(tabs[:-1], petalos)):
        with tab:
            icon = PETAL_ICONS[i]
            st.markdown(f"### {icon} {petalo['nombre']}")

            # Calculate totals for this petal
            total_acciones = sum(len(v) for v in petalo["categorias"].values())
            key_prefix     = f"p{i}"

            # Load previously saved selections
            saved = data.get(f"petalo_{i}_acciones", {})

            selected_all = []
            new_saved    = {}

            # ── Notes field at top ────────────────────────────────────────
            notas_key = f"petalo_{i}_notas"
            data[notas_key] = st.text_area(
                "📝 Notas / observaciones de este pétalo",
                value=data.get(notas_key, ""),
                height=70,
                key=f"{key_prefix}_notas",
                placeholder="Contexto, intenciones, dificultades…"
            )

            st.markdown("**Selecciona las prácticas activas en este espacio:**")

            # ── Categorías con multiselect ────────────────────────────────
            for cat_key, acciones in petalo["categorias"].items():
                cat_label = cat_key.replace("_", " ").title()
                saved_cat = saved.get(cat_key, [])

                selected = st.multiselect(
                    f"**{cat_label}**",
                    options=acciones,
                    default=[a for a in saved_cat if a in acciones],
                    key=f"{key_prefix}_{cat_key}",
                    placeholder="Selecciona las que aplican…",
                )
                new_saved[cat_key] = selected
                selected_all.extend(selected)

            data[f"petalo_{i}_acciones"] = new_saved

            # ── IPR for this petal ────────────────────────────────────────
            pct = round(len(selected_all) / total_acciones * 100, 1) if total_acciones else 0
            ipr_scores.append(pct)
            level, color = _ipr_level(pct)

            st.markdown("---")
            col_ipr, col_bar = st.columns([1, 3])
            with col_ipr:
                st.markdown(
                    f'<div style="background:{color};border-radius:10px;padding:0.6rem 1rem;'
                    f'text-align:center;color:white;">'
                    f'<div style="font-size:1.5rem;font-weight:700;">{pct:.0f}%</div>'
                    f'<div style="font-size:0.8rem;">{level}</div>'
                    f'<div style="font-size:0.75rem;opacity:0.85;">{len(selected_all)}/{total_acciones} prácticas</div>'
                    f'</div>', unsafe_allow_html=True)
            with col_bar:
                st.markdown(f"_{_narrative_for_petal(petalo['nombre'], pct, selected_all)}_")

    # ── Resumen IPR global ────────────────────────────────────────────────
    with tabs[-1]:
        st.markdown("### 📊 Resumen — Indicador de Potencial Regenerativo (IPR)")

        if not any(ipr_scores):
            st.info("Selecciona prácticas en los pétalos para ver el resumen.")
        else:
            avg_ipr = sum(ipr_scores) / len(ipr_scores)
            data["ipr_global"]  = round(avg_ipr, 1)
            data["ipr_por_petalo"] = {petalos[i]["nombre"]: ipr_scores[i]
                                      for i in range(len(petalos))}

            # Global metric
            g_level, g_color = _ipr_level(avg_ipr)
            st.markdown(
                f'<div style="background:{g_color};border-radius:12px;padding:1rem 1.5rem;'
                f'text-align:center;color:white;margin-bottom:1rem;">'
                f'<div style="font-size:2rem;font-weight:800;">{avg_ipr:.0f}%</div>'
                f'<div style="font-size:1rem;">{g_level} — IPR Global</div></div>',
                unsafe_allow_html=True)

            # Radar chart
            try:
                import plotly.graph_objects as go
                labels = [f"{PETAL_ICONS[i]} {p['nombre'][:20]}" for i, p in enumerate(petalos)]
                vals   = ipr_scores + [ipr_scores[0]]
                lbls   = labels    + [labels[0]]
                fig = go.Figure(go.Scatterpolar(
                    r=vals, theta=lbls,
                    fill="toself",
                    fillcolor="rgba(64,145,108,0.25)",
                    line=dict(color="#2D6A4F", width=2),
                    marker=dict(color="#1B4332", size=6),
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                               tickfont=dict(size=9))),
                    showlegend=False,
                    height=420,
                    margin=dict(l=60, r=60, t=30, b=30),
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.caption(f"Gráfico no disponible: {e}")

            # Per-petal bars
            st.markdown("**Detalle por pétalo:**")
            for i, (p, pct) in enumerate(zip(petalos, ipr_scores)):
                level, color = _ipr_level(pct)
                n_sel = sum(len(v) for v in data.get(f"petalo_{i}_acciones", {}).values())
                n_tot = sum(len(v) for v in p["categorias"].values())
                filled = int(pct / 10)
                bar    = "█" * filled + "░" * (10 - filled)
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.3rem;">'
                    f'<span style="width:28px;font-size:1.1rem;">{PETAL_ICONS[i]}</span>'
                    f'<span style="width:220px;font-size:0.82rem;color:#1B4332;">{p["nombre"][:30]}</span>'
                    f'<span style="font-family:monospace;color:{color};font-size:0.85rem;">{bar}</span>'
                    f'<span style="font-size:0.8rem;color:{color};font-weight:700;">{pct:.0f}%</span>'
                    f'<span style="font-size:0.75rem;color:#888;">{n_sel}/{n_tot}</span>'
                    f'</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(_global_narrative(ipr_scores, petalos))

            # Free-text fields
            st.markdown("---")
            st.markdown("**💬 Reflexiones adicionales**")
            c1, c2 = st.columns(2)
            with c1:
                data["pot_practicas_destacadas"] = st.text_area(
                    "✨ Prácticas más destacadas del espacio",
                    value=data.get("pot_practicas_destacadas", ""),
                    height=100, key="pot_destacadas")
                data["pot_integraciones"] = st.text_area(
                    "🔗 Integraciones entre prácticas (sinergias)",
                    value=data.get("pot_integraciones", ""),
                    height=100, key="pot_integ",
                    placeholder="Ej: captación de agua lluvia + huerto vertical…")
            with c2:
                data["pot_proximos_pasos"] = st.text_area(
                    "🚀 Próximos pasos prioritarios",
                    value=data.get("pot_proximos_pasos", ""),
                    height=100, key="pot_pasos")
                data["pot_vision"] = st.text_area(
                    "🌟 Visión de futuro del espacio",
                    value=data.get("pot_vision", ""),
                    height=100, key="pot_vision_txt",
                    placeholder="¿Cómo imaginas este espacio en 3 años?…")

    # ── Guardar ───────────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("💾 Guardar Flor de la Permacultura", use_container_width=True,
                 type="primary", key="save_potencial"):
        st.session_state.visit_data = data
        save_visit(data)
        st.success("✅ Flor de la Permacultura guardada.")
        show_drive_save_status()
