# -------------------------------------------------------------------------------------------------
# 🧠 Render Macro Interaction Tools Panel — Live Portfolio Monitor
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
    Renders input and log viewer for Live Portfolio Monitor notes.

    Args:
        show_observation (bool): Whether to show the live portfolio notes panel.
        show_log (bool): Whether to display journaled notes.
        observation_input_callback (func): Callback for capturing new portfolio notes.
        observation_log_callback (func): Callback for viewing or editing past entries.
    """

    if show_observation:
        with st.expander("📝 Add Live Portfolio Note", expanded=True):
            observation_input_callback()

    if show_log:
        with st.expander("📋 View/Edit/Delete Portfolio Notes", expanded=True):
            observation_log_callback()
