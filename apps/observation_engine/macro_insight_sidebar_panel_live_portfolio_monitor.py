# -------------------------------------------------------------------------------------------------
# Macro Insight Sidebar Panel — Live Portfolio Monitor
# -------------------------------------------------------------------------------------------------

import streamlit as st


def render_macro_sidebar_tools(theme_readable: str, theme_code: str):
    """Render the standard FIT1 module interaction toggles."""
    st.sidebar.markdown("---")
    st.sidebar.title("Macro Interaction Tools")

    show_observation = st.sidebar.checkbox(
        "Add Custom Observation",
        key=f"{theme_code}_obs_toggle",
    )
    show_ai_export = st.sidebar.checkbox(
        "Preview AI Export",
        key=f"{theme_code}_ai_toggle",
    )
    show_log = st.sidebar.checkbox(
        "View/Edit/Delete Observation Log",
        key=f"{theme_code}_log_toggle",
    )

    return show_observation, show_ai_export, show_log
