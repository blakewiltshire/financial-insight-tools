# -------------------------------------------------------------------------------------------------
# 🧠 Render Macro Interaction Tools Panel — Intermarket Correlation Modules
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring, too-many-arguments
# -------------------------------------------------------------------------------------------------

import streamlit as st

def render_macro_interaction_tools_panel(
    show_observation: bool,
    show_log: bool,
    panel_title: str,
    selected_themes: list,
    selected_indicators: list,
    observation_input_callback,
    observation_log_callback
) -> None:
    """
    Renders observation form and log panel for Intermarket Correlation modules.

    Args:
        show_observation (bool): Toggle for showing the observation input form.
        show_log (bool): Toggle for showing the saved observation log.
        panel_title (str): Panel title describing the current view/context.
        selected_themes (List[str]): Thematic groupings included in analysis.
        selected_indicators (List[str]): Indicators or asset series involved.
        observation_input_callback (func): Form callback for logging observations.
        observation_log_callback (func): Viewer for historical log entries.
    """

    if show_observation:
        with st.expander("📝 Add New Observation", expanded=True):
            observation_input_callback(
                theme_title=panel_title,
                themes_selected=selected_themes,
                indicators_selected=selected_indicators
            )

    if show_log:
        with st.expander("📋 View/Edit/Delete Observations", expanded=True):
            observation_log_callback()
