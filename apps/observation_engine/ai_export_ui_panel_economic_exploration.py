# -------------------------------------------------------------------------------------------------
# 🧠 AI Export UI Panel — Platinum Production Build (Standalone Snapshot System)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

import streamlit as st
import os
import json
import datetime

# -------------------------------------------------------------------------------------------------
# Base Save Folder
# -------------------------------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
AI_BUNDLE_FOLDER = os.path.join(STORAGE_FOLDER, "ai_bundles", "economic_exploration")

# -------------------------------------------------------------------------------------------------
# Render Export Panel
# -------------------------------------------------------------------------------------------------
def render_ai_export_ui_panel(
    module_type: str,
    theme: str,
    indicator: str,
    use_case: str,
    timeframe: str,
    macro_signals: list,
    score_label: str,
    explanation: str,
    metadata: list = None
):
    st.subheader("🔎 Macro Insight Snapshot")
    st.markdown("This exports the AI-ready metadata snapshot for the current view.")

    export_object = {
        "theme": theme,
        "indicator": indicator,
        "use_case": use_case,
        "timeframe": timeframe,
        "macro_score_label": score_label,
        "macro_score_explanation": explanation,
        "macro_signals": macro_signals,
        "metadata": metadata or []
    }

    with st.expander("📦 Preview Export Bundle", expanded=False):
        st.json(export_object)

    replace_existing = st.toggle("🔁 Replace file if exists", value=True)

    if st.button("📌 Save Snapshot"):
        filepath = save_snapshot(module_type, theme, use_case, timeframe, export_object, replace_existing)
        st.success(f"✅ Saved to: {filepath}")

# -------------------------------------------------------------------------------------------------
# Save Snapshot Function
# -------------------------------------------------------------------------------------------------
def save_snapshot(module_type, theme, use_case, timeframe, bundle_obj, replace_existing):
    folder = os.path.join(AI_BUNDLE_FOLDER, module_type)
    module_type="economic_exploration"
    os.makedirs(folder, exist_ok=True)

    filename = f"economic_exploration__{theme.lower()}__{use_case.lower().replace(' ', '_')}__{timeframe.lower()}.json"
    full_path = os.path.join(folder, filename)

    if not replace_existing and os.path.exists(full_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"economic_exploration__{theme.lower()}__{use_case.lower().replace(' ', '_')}__{timeframe.lower()}__{timestamp}.json"
        full_path = os.path.join(folder, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(bundle_obj, f, indent=2)
    return full_path
