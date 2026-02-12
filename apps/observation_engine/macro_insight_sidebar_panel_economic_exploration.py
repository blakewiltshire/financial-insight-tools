# -------------------------------------------------------------------------------------------------
# 🧠 Macro Insight Sidebar Toggle Panel
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Reusable sidebar interaction toggle panel for activating observation tools.

- Fully agnostic toggle interface
- Does not require knowledge of form, observation, or AI processing logic
- Compatible across: Economic Exploration, Thematic Correlation Explorer, Trade Structuring, etc.
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
    selected_timeframe: str,
    summary_df,
    score_label: str,
    explanation: str
):
    """
    Sidebar UI toggles controlling activation of observation panels.

    Args:
        theme_readable (str): Display name of theme (for future extensions if required)
        theme_code (str): Theme identifier (used for unique toggle keys)
        selected_use_case (str): Current use case
        selected_timeframe (str): Current timeframe selected
        summary_df (DataFrame): Macro signal dataframe (for future extensions if needed)
        score_label (str): Current score label
        explanation (str): Current explanation label

    Returns:
        Tuple of booleans:
            - show_observation
            - show_ai_export
            - show_log
    """

    st.sidebar.markdown("---")
    st.sidebar.title("🧠 Macro Interaction Tools")

    show_observation = st.sidebar.checkbox(
        "📝 Add Custom Observation",
        key=f"{theme_code}_obs_toggle"
    )
    show_ai_export = st.sidebar.checkbox(
        "🧠 Preview AI Export",
        key=f"{theme_code}_ai_toggle"
    )
    show_log = st.sidebar.checkbox(
        "📋 View/Edit/Delete Observation Log",
        key=f"{theme_code}_log_toggle"
    )

    return show_observation, show_ai_export, show_log

# -------------------------------------------------------------------------------------------------
