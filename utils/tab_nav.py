"""Reusable session-state driven tab navigation — replaces st.tabs() with clickable prev/next."""
import streamlit as st


def get_active_tab(module_key: str, default: int = 0) -> int:
    key = f"active_tab_{module_key}"
    if key not in st.session_state:
        st.session_state[key] = default
    return int(st.session_state[key])


def tab_header(module_key: str, tabs: list):
    """Render clickable tab buttons at top of module."""
    active = get_active_tab(module_key)
    cols = st.columns(len(tabs))
    for i, (col, tab_name) in enumerate(zip(cols, tabs)):
        with col:
            btn_type = "primary" if i == active else "secondary"
            if st.button(tab_name, use_container_width=True, type=btn_type,
                         key=f"tabtop_{module_key}_{i}"):
                st.session_state[f"active_tab_{module_key}"] = i
                st.rerun()
    st.markdown("---")


def tab_nav_bottom(module_key: str, tabs: list, current_idx: int):
    """Render prev/next clickable buttons at bottom of a tab section."""
    st.markdown("---")
    c1, _, c2 = st.columns([1, 1, 1])
    with c1:
        if current_idx > 0:
            if st.button(f"⬅️ {tabs[current_idx - 1]}", use_container_width=True,
                         key=f"tabprev_{module_key}_{current_idx}"):
                st.session_state[f"active_tab_{module_key}"] = current_idx - 1
                st.rerun()
    with c2:
        if current_idx < len(tabs) - 1:
            if st.button(f"{tabs[current_idx + 1]} ➡️", use_container_width=True,
                         key=f"tabnext_{module_key}_{current_idx}"):
                st.session_state[f"active_tab_{module_key}"] = current_idx + 1
                st.rerun()
