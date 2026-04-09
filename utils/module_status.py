"""Estado de módulo v11 — Indagación Regenerativa.

Cada módulo puede tener uno de tres estados:
  - "respondido"  : respuestas directas de las personas del espacio durante la visita
  - "inferido"    : respuestas interpretadas por el facilitador después de la visita
  - "no_abordado" : módulo no trabajado — no se registra ninguna respuesta

Uso en cada módulo:
    from utils.module_status import render_module_status, is_module_active

    status = render_module_status(data, "mod_sitio")
    if not is_module_active(status):
        return   # no renderizar ni guardar nada

    # Si status == "inferido", se puede mostrar un aviso visual
    if status == "inferido":
        st.info("🔍 Módulo en modo inferido — respuestas interpretadas por el facilitador.")
"""

import streamlit as st

# Clave de estado → (etiqueta, color, icono, descripción corta)
STATUS_OPTIONS = {
    "respondido":  ("✅ Respondido",  "#1B4332", "✅",
                    "Respuestas dadas directamente por las personas del espacio."),
    "inferido":    ("🔍 Inferido",    "#795548", "🔍",
                    "Respuestas interpretadas por el facilitador después de la visita."),
    "no_abordado": ("⭕ No abordado", "#9E9E9E", "⭕",
                    "Módulo no trabajado en esta visita."),
}

STATUS_LABELS  = [v[0] for v in STATUS_OPTIONS.values()]
STATUS_KEYS    = list(STATUS_OPTIONS.keys())


def render_module_status(data: dict, module_key: str, label: str = "") -> str:
    """Render the status selector at the top of a module.

    Args:
        data:       current visit data dict (will be mutated)
        module_key: e.g. "mod_sitio", "mod_sistemas"
        label:      optional module name for display

    Returns:
        current status string: "respondido" | "inferido" | "no_abordado"
    """
    current = data.get(module_key, "respondido")
    if current not in STATUS_KEYS:
        current = "respondido"

    current_idx = STATUS_KEYS.index(current)

    col1, col2 = st.columns([3, 7])
    with col1:
        chosen_label = st.radio(
            "Estado del módulo",
            STATUS_LABELS,
            index=current_idx,
            key=f"_status_radio_{module_key}",
            horizontal=False,
            label_visibility="collapsed",
        )
    chosen_key = STATUS_KEYS[STATUS_LABELS.index(chosen_label)]

    with col2:
        _, icon, desc = STATUS_OPTIONS[chosen_key][1], STATUS_OPTIONS[chosen_key][2], STATUS_OPTIONS[chosen_key][3]
        bg_map = {
            "respondido":  ("#D8F3DC", "#1B4332"),
            "inferido":    ("#FFF3E0", "#5D4037"),
            "no_abordado": ("#F5F5F5", "#757575"),
        }
        bg, fg = bg_map[chosen_key]
        st.markdown(
            f'<div style="background:{bg};border-radius:8px;padding:0.6rem 0.9rem;'
            f'color:{fg};font-size:0.85rem;margin-top:0.4rem;">'
            f'<strong>{icon} {STATUS_OPTIONS[chosen_key][0]}</strong><br>'
            f'<span style="font-size:0.8rem;">{desc}</span></div>',
            unsafe_allow_html=True,
        )

    # Persist status
    data[module_key] = chosen_key
    return chosen_key


def is_module_active(status: str) -> bool:
    """Returns True if the module should render its form fields."""
    return status != "no_abordado"


def module_status_badge(status: str) -> str:
    """Returns a short HTML badge for use in reports/summaries."""
    info = STATUS_OPTIONS.get(status, STATUS_OPTIONS["no_abordado"])
    bg_map = {
        "respondido":  ("#D8F3DC", "#1B4332"),
        "inferido":    ("#FFF3E0", "#5D4037"),
        "no_abordado": ("#F5F5F5", "#757575"),
    }
    bg, fg = bg_map.get(status, ("#F5F5F5", "#757575"))
    return (f'<span style="background:{bg};color:{fg};border-radius:4px;'
            f'padding:0.1rem 0.5rem;font-size:0.75rem;">{info[2]} {info[0]}</span>')


def get_module_status(data: dict, module_key: str) -> str:
    return data.get(module_key, "respondido")


def is_readonly() -> bool:
    """Returns True if the current user should see modules in read-only mode."""
    try:
        import streamlit as st
        user = st.session_state.get("current_user", {})
        return user.get("role", "user") != "admin"
    except Exception:
        return False


def render_readonly_notice():
    """Show a small read-only banner at the top of a module."""
    try:
        import streamlit as st
        st.markdown(
            '<div style="background:#E8F5E9;border:1px solid #A8D5B5;border-radius:6px;'
            'padding:0.4rem 0.8rem;margin-bottom:0.8rem;font-size:0.8rem;color:#2D6A4F;">'
            'Vista de resultados — esta sección muestra la información registrada en el diagnóstico.</div>',
            unsafe_allow_html=True)
    except Exception:
        pass


def render_not_addressed_notice(data: dict, module_key: str, readonly: bool):
    """Shows a message informing that the module is not addressed and allows reactivation."""
    st.markdown(
        f'<div style="background:#F5F5F5;border:1px solid #E0E0E0;border-radius:10px;'
        f'padding:1.5rem;margin:1rem 0;text-align:center;color:#757575;">'
        f'<div style="font-size:3rem;margin-bottom:0.5rem;">⭕</div>'
        f'<div style="font-size:1.1rem;font-weight:700;margin-bottom:0.4rem;">'
        f'Módulo marcado como "No abordado"</div>'
        f'<div style="font-size:0.9rem;line-height:1.6;">'
        f'Este módulo no forma parte del diagnóstico actual o no ha sido trabajado aún.<br>'
        f'Si deseas activarlo y comenzar el registro de datos, presiona el botón de abajo.'
        f'</div></div>', unsafe_allow_html=True)
    
    if not readonly:
        if st.button(f"🚀 Reactivar módulo", key=f"reactivate_{module_key}", use_container_width=True, type="primary"):
            data[module_key] = "respondido"
            from utils.data_manager import save_visit
            save_visit(data)
            st.success("Módulo reactivado.")
            from utils.tab_nav import show_drive_save_status
            show_drive_save_status()
            st.rerun()

