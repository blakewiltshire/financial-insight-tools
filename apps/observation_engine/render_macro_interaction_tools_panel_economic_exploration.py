# -------------------------------------------------------------------------------------------------
# 🧠 Macro Interaction Tools Panel — Platinum Canonical Build (Filename Aligned, Production Locked)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Main interaction panel rendering:

- Observation input form (custom notes)
- Observation journal log viewer
- AI export preview and AI bundle save operation (journal save removed)
"""

# -------------------------------------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Dynamic Absolute Path Setup
# -------------------------------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

# Append required submodules for imports
sys.path.append(os.path.join(PROJECT_ROOT, "observation_engine"))
sys.path.append(os.path.join(PROJECT_ROOT, "observation_engine", "storage"))
sys.path.append(os.path.join(PROJECT_ROOT, "economic_exploration"))

# -------------------------------------------------------------------------------------------------
# Internal Imports (Handlers and Export Logic)
# -------------------------------------------------------------------------------------------------
from observation_handler_economic_exploration import (
    observation_input_form,
    display_observation_log
)
from ai_export_builder_economic_exploration import save_ai_bundle_to_file

# -------------------------------------------------------------------------------------------------
# Core Interaction Panel Logic
# -------------------------------------------------------------------------------------------------
def render_macro_interaction_tools_panel(
    module_type: str,
    country: str,
    theme_code: str,
    theme_title: str,
    show_observation: bool,
    show_log: bool,
    show_ai_export: bool,
    theme_data: dict,
    selected_use_case: str,
    selected_timeframe: str,
    summary_df,
    label: str,
    explanation: str,
    ai_bundle: dict = None,
    observation_input_callback=None,
    observation_log_callback=None
):
    """
    Central UI for interacting with user observations and AI bundles.
    """
    st.markdown("---")
    st.subheader("🧠 Macro Interaction Tools")

    col1, col2 = st.columns([1, 1])

    # --- Observation Input Form ---
    if show_observation and observation_input_callback:
        with col1.expander("📌 Add Observation", expanded=False):
            observation_input_callback(
                module_type=module_type,
                country=country,
                theme_code=theme_code,
                theme_title=theme_title,
                indicator=selected_use_case,
                use_case=selected_use_case,
                timeframe=selected_timeframe,
                form_key="main_panel_obs_form"
            )

    # --- Journal Viewer ---
    if show_log and observation_log_callback:
        with col2.expander("📘 Observation Journal", expanded=False):
            observation_log_callback(
                module_type=module_type,
                country=country,
                theme_code=theme_code
            )

    # --- AI Export Panel ---
    if show_ai_export:
        st.markdown("### 🔎 Macro Insight Snapshots")

        if ai_bundle and ai_bundle.get("use_cases"):
            current = ai_bundle["use_cases"][0]

            st.json({
                "theme": ai_bundle.get("theme", {}),
                "scoring_methodology": ai_bundle.get("scoring_methodology", {}),
                "use_case": current.get("name"),
                "timeframe": current.get("timeframe"),
                "macro_score": current.get("macro_score"),
                "score_label": current.get("score_label"),
                "score_explanation": current.get("score_explanation"),
                "macro_signals": current.get("macro_signals", []),
                "metadata": current.get("metadata", []),
            }, expanded=False)

            replace_existing = st.toggle("🔁 Replace existing entry if it already exists", value=True)

            if st.button("📌 Save Macro Insights"):
                json_result = save_ai_bundle_to_file(
                    bundle=ai_bundle,
                    replace_existing=replace_existing
                )
                st.success(json_result)

        else:
            st.warning("⚠️ No AI bundle available for this theme + use case.")
