# -------------------------------------------------------------------------------------------------
# Render Macro Interaction Tools Panel — Live Portfolio Monitor
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring, too-many-arguments

import streamlit as st


def render_macro_interaction_tools_panel(
    show_observation: bool,
    show_log: bool,
    panel_title: str,
    selected_themes: list,
    selected_indicators: list,
    observation_input_callback,
    observation_log_callback,
) -> None:
    """Render the observation form and saved observation log."""

    if show_observation:
        with st.expander("Add New Observation", expanded=True):
            observation_input_callback(
                theme_title=panel_title,
                themes_selected=selected_themes,
                indicators_selected=selected_indicators,
            )

    if show_log:
        with st.expander("View/Edit/Delete Observations", expanded=True):
            observation_log_callback()
