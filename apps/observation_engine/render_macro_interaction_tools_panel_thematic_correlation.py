# -------------------------------------------------------------------------------------------------
# 🧠 Macro Interaction Panel — Thematic Correlation Explorer (Platinum Canonical Build)
# -------------------------------------------------------------------------------------------------
# Handles rendering of Observation Input and Journal Log Viewer for correlation themes
# -------------------------------------------------------------------------------------------------

import streamlit as st


def render_macro_interaction_tools_panel(
    show_observation: bool,
    show_log: bool,
    theme_code: str,
    theme_title: str,
    selected_use_case: str,
    themes_selected,
    indicators_selected,
    observation_input_callback,
    observation_log_callback
) -> None:
    """
    Renders observation input and journal log panels for Thematic Correlation Explorer.

    Args:
        show_observation (bool): Toggle for observation form
        show_log (bool): Toggle for journal log
        theme_code (str): Theme identifier
        theme_title (str): Theme readable title
        selected_use_case (str): Use case or snapshot context
        themes_selected (list): List of theme codes selected
        indicators_selected (list): List of indicator labels selected
        observation_input_callback (func): Observation form renderer
        observation_log_callback (func): Journal viewer renderer
    """

    # 📝 Observation Input Form
    if show_observation:
            observation_input_callback(
                theme_title=theme_title,
                themes_selected=themes_selected,
                indicators_selected=indicators_selected
            )

    if show_log:
        with st.expander("📋 View/Edit/Delete Observations", expanded=True):
            observation_log_callback()
