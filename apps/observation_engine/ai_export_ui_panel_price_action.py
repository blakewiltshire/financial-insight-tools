# -------------------------------------------------------------------------------------------------
# 🧠 AI Export UI Panel — Price Action (Platinum Canonical)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

import os
import sys
import json
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.helpers import get_named_paths
from ai_export_builder_price_action import build_macro_insight_snapshot_price_action

# -------------------------------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
APP_PATH = PATHS["level_up_1"]
STORAGE_FOLDER = os.path.join(APP_PATH, "observation_engine", "storage", "ai_bundles", "price_action")
os.makedirs(STORAGE_FOLDER, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 🔍 Render AI Export Panel — Price Action Snapshot
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
    Displays the export UI panel for Price Action snapshot. Delegates save to user via button.
    """
    st.markdown("### 🔎 Macro Insight Snapshots")

    # Build snapshot — no saving here
    success, snapshot = build_macro_insight_snapshot_price_action(
        asset=asset,
        summary_df=summary_df,
        timeframe_summary=timeframe_summary,
        execution_readiness_label=execution_readiness_label,
        score_explanation=score_explanation,
        predisposition=predisposition,
        use_case_name=use_case_name,
        indicator_weights=indicator_weights,
        metadata_lookup=metadata_lookup
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
        filename = f"trade_and_portfolio_structuring__price_action__{use_case_name.replace(' ', '_').lower()}__{asset.replace(' ', '_').lower()}.json"
        save_path = os.path.join(STORAGE_FOLDER, filename)

        if not replace_existing and os.path.exists(save_path):
            st.warning("⚠️ File already exists and 'Replace' is disabled.")
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)

        st.success(f"📁 Snapshot saved to: `{save_path}`")
