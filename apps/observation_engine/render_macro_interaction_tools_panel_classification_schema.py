# -------------------------------------------------------------------------------------------------
# 🧠 Render Macro Interaction Tools Panel — Classification Schema Viewer
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
    Renders input and log viewer for Classification Schema Viewer notes.

    Args:
        show_observation (bool): Whether to show the Classification Schema Viewer notes panel.
        show_log (bool): Whether to display journaled notes.
        observation_input_callback (func): Callback for capturing new Classification Schema Viewer notes.
        observation_log_callback (func): Callback for viewing or editing past entries.
    """

    if show_observation:
        with st.expander("📝 Add Classification Schema Viewer Note", expanded=True):
            observation_input_callback()

    if show_log:
        with st.expander("📋 View/Edit/Delete Classification Schema Viewer Notes", expanded=True):
            observation_log_callback()
