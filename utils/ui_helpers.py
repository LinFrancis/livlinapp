"""utils/ui_helpers.py -- Shared UI helper functions.
Extracted from report.py to avoid duplication and respect SRP.
"""
import streamlit as st


def safe_float(v, default=0.0):
    """Safely convert value to float."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def val(data, key, default="No registrado"):
    """Get value from data dict, returning default for empty values."""
    v = data.get(key)
    if v in [None, "", [], 0, 0.0]:
        return default
    return v


def show_field(label, value, empty_msg="No registrado"):
    """Display a labeled field if value is not empty."""
    if value in [None, "", [], 0, 0.0]:
        return
    st.markdown(
        f'<div style="padding:0.3rem 0;border-bottom:1px solid #E8F5E9;">'
        f'<span style="font-size:0.75rem;color:#52B788;text-transform:uppercase;">{label}</span><br>'
        f'<span style="font-size:0.88rem;color:#1B4332;">{value}</span></div>',
        unsafe_allow_html=True)


def card(label, value, bg="#F0FFF4", fg="#1B4332", border="#52B788"):
    """Display a styled card with label and value."""
    if not value or value == "No registrado":
        return
    st.markdown(
        f'<div style="background:{bg};border-radius:8px;padding:0.6rem 0.8rem;'
        f'margin-bottom:0.5rem;border-left:3px solid {border};">'
        f'<div style="font-size:0.72rem;color:{border};text-transform:uppercase;margin-bottom:0.2rem;">{label}</div>'
        f'<div style="font-size:0.88rem;color:{fg};line-height:1.5;">{value}</div></div>',
        unsafe_allow_html=True)


def ref_box(refs):
    """Render a reference box at the bottom of a section."""
    if not refs:
        return
    lines = "".join(
        f'<div style="font-size:0.78rem;color:#555;padding:2px 0;">'
        f'📖 {auth} — <em>{title}</em> '
        f'<a href="{url}" target="_blank" style="color:#1565C0;font-size:0.75rem;">↗</a></div>'
        for auth, title, url in refs
    )
    st.markdown(
        f'<div style="background:#FAFAFA;border-radius:8px;padding:0.6rem 0.8rem;margin-top:0.8rem;'
        f'border-top:2px solid #D8F3DC;">'
        f'<div style="font-size:0.7rem;color:#40916C;font-weight:700;margin-bottom:0.3rem;">📚 Referencias de esta seccion</div>'
        f'{lines}</div>', unsafe_allow_html=True)


def status_badge(data, mod_key):
    """Generate a small status badge HTML for module status."""
    s = data.get(mod_key, "")
    if s == "respondido":
        return '<span style="background:#D8F3DC;color:#1B4332;padding:2px 6px;border-radius:4px;font-size:0.65rem;">Respondido</span>'
    if s == "inferido":
        return '<span style="background:#FFF3E0;color:#E65100;padding:2px 6px;border-radius:4px;font-size:0.65rem;">Inferido</span>'
    if s == "no_abordado":
        return '<span style="background:#FAFAFA;color:#999;padding:2px 6px;border-radius:4px;font-size:0.65rem;">No abordado</span>'
    return '<span style="background:#FAFAFA;color:#BBB;padding:2px 6px;border-radius:4px;font-size:0.65rem;">Pendiente</span>'
