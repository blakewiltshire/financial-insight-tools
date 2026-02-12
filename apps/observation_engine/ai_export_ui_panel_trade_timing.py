# -------------------------------------------------------------------------------------------------
# 📤 Trade Timing — AI Export UI Panel (Platinum-Aligned)
# -------------------------------------------------------------------------------------------------
import os
import sys
import json
import pandas as pd
import streamlit as st
from datetime import datetime

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.helpers import get_named_paths
from ai_export_builder_trade_timing import build_macro_insight_snapshot_trade_timing

# -------------------------------------------------------------------------------------------------
# Paths & Registry
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]
STORAGE_FOLDER = os.path.join(APP_PATH, "observation_engine", "storage", "ai_bundles", "trade_timing")
os.makedirs(STORAGE_FOLDER, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 🔍 Render AI Export Panel — Trade Timing Snapshot
# -------------------------------------------------------------------------------------------------
def render_ai_export_panel(
    asset: str,
    summary_df: pd.DataFrame,
    timeframe_summary: dict,
    execution_readiness_label: str,
    score_explanation: str,
    predisposition: str,
    use_case_name: str,
    metadata_lookup: dict = None,
    indicator_weights: dict = None
):
    """
    Displays the export UI panel and handles bundle save for Trade Timing modules.
    """
    st.markdown("### 🔎 Macro Insight Snapshots")

    # Build the snapshot using the canonical builder
    success, snapshot = build_macro_insight_snapshot_trade_timing(
        asset=asset,
        summary_df=summary_df,
        timeframe_summary=timeframe_summary,
        execution_readiness_label=execution_readiness_label,
        score_explanation=score_explanation,
        predisposition=predisposition,
        use_case_name=use_case_name,
        metadata_lookup=metadata_lookup,
        indicator_weights=indicator_weights
    )

    if not success:
        st.error(f"❌ Failed to build AI export snapshot: {snapshot}")
        return

    # Preview snapshot inline
    st.markdown("#### 📦 Export Bundle Preview")
    st.caption("Snapshot of macro insight metadata and scoring structure")
    st.json(snapshot, expanded=False)

    # Save toggle
    replace_existing = st.toggle("🔁 Replace existing entry if it already exists", value=True)

    # Save trigger
    if st.button("📌 Save Macro Insights"):
        filename = f"trade_and_portfolio_structuring__trade_timing__{use_case_name.replace(' ', '_').lower()}__{asset.replace(' ', '_').lower()}.json"
        save_path = os.path.join(STORAGE_FOLDER, filename)

        if not replace_existing and os.path.exists(save_path):
            st.warning("⚠️ File already exists and 'Replace' is disabled.")
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)

        st.success(f"📁 Snapshot saved to: `{save_path}`")
