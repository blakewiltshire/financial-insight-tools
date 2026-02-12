# -------------------------------------------------------------------------------------------------
# 🧠 Macro Insight Sidebar Panel — Intermarket Correlation Modules (Platinum Canonical Build)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Reusable sidebar toggle interface for activating observation tools in Intermarket Correlation modules.

- Fully agnostic UI toggle interface
- No scoring logic (descriptive correlation summaries only)
- Compatible with observation logging and annotation (AI export removed)
"""
# -------------------------------------------------------------------------------------------------
# Third-party Imports
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Sidebar Interaction Panel Logic
# -------------------------------------------------------------------------------------------------

def render_macro_sidebar_tools(
    theme_readable: str,
    theme_code: str,
    selected_use_case: str,
):
    """
    Render sidebar toggles controlling observation panel visibility.

    Returns:
        Tuple of booleans: (show_observation, show_log)
    """
    st.sidebar.markdown("---")
    st.sidebar.title("🧠 Macro Interaction Tools")

    show_observation = st.sidebar.checkbox(
        "📝 Add Observation",
        key=f"{theme_code}_obs_toggle"
    )
    show_log = st.sidebar.checkbox(
        "📋 View Observation Log",
        key=f"{theme_code}_log_toggle"
    )

    return show_observation, show_log
