"""Modulo Conciencia Ecologica -- Cambio climatico, biodiversidad, contaminacion.
Separado del Tao de la Regeneracion. Modulo opcional e independiente.
"""
import streamlit as st
from utils.data_manager import save_visit
from utils.module_status import render_module_status, is_module_active
from utils.tab_nav import show_drive_save_status, tab_header, tab_nav_bottom, get_active_tab


ECO_INTRO = (
    "La triple crisis planetaria -- cambio climatico, perdida de biodiversidad "
    "y contaminacion -- es el contexto en el que toda accion regenerativa se "
    "situa. Este modulo explora como estas realidades se manifiestan en el "
    "espacio que habitamos y como nos relacionamos con ellas."
)


def render():
    from utils.module_status import is_readonly as _is_ro, render_readonly_notice
    _readonly = _is_ro()
    if _readonly:
        render_readonly_notice()

    st.markdown("## Conciencia Ecologica")
    st.markdown(
        '<p class="module-subtitle">Cambio climatico, biodiversidad y contaminacion '
        '-- como se manifiestan en nuestro espacio.</p>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="info-box">{ECO_INTRO}</div>',
        unsafe_allow_html=True)

    data = st.session_state.visit_data

    st.markdown("**Estado de este modulo:**")
    _mod_status = render_module_status(data, "mod_eco")
    if not is_module_active(_mod_status):
        from utils.module_status import render_not_addressed_notice
        render_not_addressed_notice(data, "mod_eco", _readonly)
        return


    st.markdown("---")

    # -- Tabs for 3 crisis areas --
    CRISIS_TABS = ["Cambio Climatico", "Perdida de Biodiversidad", "Contaminacion"]
    tab_header("eco_crisis", CRISIS_TABS)
    crisis_active = get_active_tab("eco_crisis")

    if crisis_active == 0:
        st.markdown("### Cambio Climatico")
        data["eco_cc_conciencia"] = st.radio(
            "Que tan presente esta el cambio climatico en su vida cotidiana?",
            ["No lo pensamos mucho", "Lo conocemos pero parece lejano",
             "Lo sentimos como una amenaza real", "Es parte de nuestra motivacion de accion"],
            index=["No lo pensamos mucho", "Lo conocemos pero parece lejano",
                   "Lo sentimos como una amenaza real", "Es parte de nuestra motivacion de accion"
                   ].index(data.get("eco_cc_conciencia", "Lo conocemos pero parece lejano")),
            disabled=_readonly)
        data["eco_cc_impacto"] = st.text_area(
            "Han sentido el cambio climatico en este lugar? (sequias, lluvias intensas, calor inusual...)",
            value=data.get("eco_cc_impacto", ""), height=80,
            placeholder="Ej: Los ultimos veranos han sido mas secos...",
            disabled=_readonly)
        data["eco_cc_respuesta"] = st.text_area(
            "Que acciones han tomado o piensan tomar frente al cambio climatico?",
            value=data.get("eco_cc_respuesta", ""), height=80,
            placeholder="Ej: Guardar mas agua, plantar arboles de sombra...",
            disabled=_readonly)

    elif crisis_active == 1:
        st.markdown("### Perdida de Biodiversidad")
        data["eco_bio_conciencia"] = st.radio(
            "Tienen conciencia de la crisis de biodiversidad?",
            ["No la conociamos", "Sabemos que existe pero parece distante",
             "La vemos en nuestro barrio", "Es algo que sentimos profundamente"],
            index=["No la conociamos", "Sabemos que existe pero parece distante",
                   "La vemos en nuestro barrio", "Es algo que sentimos profundamente"
                   ].index(data.get("eco_bio_conciencia", "Sabemos que existe pero parece distante")),
            disabled=_readonly)
        data["eco_bio_local"] = st.text_area(
            "Han notado cambios en la biodiversidad local? (menos aves, insectos, desaparicion de especies...)",
            value=data.get("eco_bio_local", ""), height=80,
            placeholder="Ej: Antes habia muchas mas mariposas en el barrio...",
            disabled=_readonly)
        data["eco_bio_accion"] = st.text_area(
            "Que podrian hacer en este espacio para contribuir a la biodiversidad local?",
            value=data.get("eco_bio_accion", ""), height=80,
            placeholder="Ej: Plantar nativas, dejar un rincon sin intervenir...",
            disabled=_readonly)

    elif crisis_active == 2:
        st.markdown("### Contaminacion")
        data["eco_cont_conciencia"] = st.radio(
            "Que tan presente esta la contaminacion en su vida cotidiana?",
            ["No lo pensamos", "Es algo lejano", "La vivimos en el barrio", "Es una preocupacion activa"],
            index=["No lo pensamos", "Es algo lejano", "La vivimos en el barrio", "Es una preocupacion activa"
                   ].index(data.get("eco_cont_conciencia", "Es algo lejano")),
            disabled=_readonly)
        data["eco_cont_tipos"] = st.multiselect(
            "Que tipos de contaminacion identifican cerca o en este espacio?",
            ["Aire / smog", "Suelo contaminado", "Ruido", "Luz artificial excesiva",
             "Plasticos y residuos", "Agua contaminada", "Ninguna visible"],
            default=data.get("eco_cont_tipos", []),
            disabled=_readonly)
        data["eco_cont_respuesta"] = st.text_area(
            "Que hacen o podrian hacer para reducir la contaminacion desde este espacio?",
            value=data.get("eco_cont_respuesta", ""), height=80,
            placeholder="Ej: Reducir plasticos, usar productos naturales de limpieza...",
            disabled=_readonly)

    tab_nav_bottom("eco_crisis", CRISIS_TABS, crisis_active)

    st.markdown("---")
    _, col_b, _ = st.columns([2, 1, 2])
    with col_b:
        if not _readonly:
            if st.button("Guardar Conciencia Ecologica", use_container_width=True, type="primary"):
                vid = save_visit(data)
                data["id"] = vid
                st.session_state.visit_data = data
                st.success("Guardado.")
