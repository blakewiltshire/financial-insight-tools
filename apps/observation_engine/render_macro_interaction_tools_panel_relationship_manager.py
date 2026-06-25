# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools Panel — Relationship Manager
# -------------------------------------------------------------------------------------------------

"""
Renders observation and observation-log tools for the Relationship Manager module.

This mirrors the lightweight reference-data interaction pattern used across FIT reference modules.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st


def render_macro_interaction_tools_panel(
    show_observation,
    show_log,
    observation_input_callback,
    observation_log_callback,
):
    """
    Render observation capture and saved observation log panels.

    Args:
        show_observation (bool): Whether to display the observation input form.
        show_log (bool): Whether to display the saved observation log.
        observation_input_callback (Callable): Function rendering observation input form.
        observation_log_callback (Callable): Function rendering observation log.
    """
    if not show_observation and not show_log:
        return

    if show_observation and show_log:
        tab_observation, tab_log = st.tabs(["Record Observation", "Saved Observations"])
        with tab_observation:
            observation_input_callback()
        with tab_log:
            observation_log_callback()
        return

    if show_observation:
        observation_input_callback()

    if show_log:
        observation_log_callback()
