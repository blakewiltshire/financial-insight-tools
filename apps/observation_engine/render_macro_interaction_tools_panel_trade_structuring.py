
# -------------------------------------------------------------------------------------------------
# 🧠 Render Macro Interaction Tools Panel — Trade Structuring & Risk Planning
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring, too-many-arguments
# -------------------------------------------------------------------------------------------------

import streamlit as st

def render_macro_interaction_tools_panel(
    show_observation: bool,
    show_log: bool,
    panel_title: str,
    selected_indicators: list,
    observation_input_callback,
    observation_log_callback
) -> None:
    """
    Renders observation form and log panel for Trade Structuring module.

    Args:
        show_observation (bool): Toggle for showing the observation input form.
        show_log (bool): Toggle for showing the saved observation log.
        panel_title (str): Panel title describing the current view/context.
        selected_indicators (List[str]): Indicator or base asset being structured.
        observation_input_callback (func): Form callback for logging observations.
        observation_log_callback (func): Viewer for historical log entries.
    """

    if show_observation:
        with st.expander("📝 Add New Note", expanded=True):
            observation_input_callback()

    if show_log:
        with st.expander("📋 View/Edit/Delete Notes", expanded=True):
            observation_log_callback()
