# -------------------------------------------------------------------------------------------------
# 🧠 Render Macro Interaction Tools Panel — Trade History & Strategy
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring, too-many-arguments
# -------------------------------------------------------------------------------------------------

import streamlit as st

def render_macro_interaction_tools_panel(
    show_observation: bool,
    show_log: bool,
    observation_input_callback,
    observation_log_callback
) -> None:
    """
    Renders reflection input and log viewer for Trade History & Strategy.

    Args:
        show_observation (bool): Whether to show the form panel.
        show_log (bool): Whether to show saved journal entries.
        observation_input_callback (func): Callback that renders the input form.
        observation_log_callback (func): Callback that renders the historical log view.
    """

    if show_observation:
        with st.expander("📝 Add Historical Reflection", expanded=True):
            observation_input_callback()

    if show_log:
        with st.expander("📋 View/Edit/Delete Historical Reflections", expanded=True):
            observation_log_callback()
