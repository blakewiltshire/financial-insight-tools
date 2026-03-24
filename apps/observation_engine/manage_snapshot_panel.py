# -------------------------------------------------------------------------------------------------
# Manage Snapshots Panel (Platinum Implementation)
# -------------------------------------------------------------------------------------------------

import os
import sys
import json
import streamlit as st

# Add path to access emoji flags
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "constants")))
from emoji import FLAGS  # Flag emoji mapping

# Add path to access file utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from insight_loader import list_all_files

# -------------------------------------------------------------------------------------------------
# Canonical Module Group Labels
# -------------------------------------------------------------------------------------------------

MODULE_GROUP_LABELS = {
    "price_action": "Trade & Portfolio Structuring",
    "trade_timing": "Trade & Portfolio Structuring",
    "trade_structuring": "Trade & Portfolio Structuring",
    "trade_history": "Trade & Portfolio Structuring",
    "live_portfolio": "Trade & Portfolio Structuring",
    "market_scanner": "Trade & Portfolio Structuring",
    "economic_exploration": "Economic Exploration",
    "intermarket_correlation": "Intermarket Correlation",
    "reference_data": "Reference Data",
    "thematic_correlation": "Thematic Correlation",
}

# -------------------------------------------------------------------------------------------------
# Snapshot Display Label
# -------------------------------------------------------------------------------------------------

def build_snapshot_display_label(filepath: str) -> str:
    filename = os.path.basename(filepath).replace(".json", "")
    parts = filename.split("__")

    if filename.startswith("economic_exploration__") and len(parts) >= 5:
        _, country, theme, use_case, timeframe = parts
        country_name = country.replace("_", " ").title()
        theme_title = theme.replace("_", " ").title()
        emoji_flag = FLAGS.get(country_name, "🌐")
        return f"{emoji_flag} {country_name} — {theme_title} (Economic Exploration)"

    if filename.startswith("trade_and_portfolio_structuring__") and len(parts) >= 4:
        _, theme, use_case, asset = parts
        theme_title = theme.replace("_", " ").title()
        asset_name = asset.replace("_", " ").title()
        return f"🗂️ {theme_title} — {asset_name} (Trade & Portfolio Structuring)"

    return f"🗂️ {filename.replace('_', ' ').title()}"

# -------------------------------------------------------------------------------------------------
# Manage AI Snapshots Panel
# -------------------------------------------------------------------------------------------------

def render_manage_snapshots_panel():
    st.header("Manage Snapshots")
    st.caption("Review or delete AI-generated snapshot files across modules.")

    if st.button("Reload Snapshot List", key="reload_snapshot_list"):
        st.rerun()

    # Locate root path
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "ai_bundles"))

    # Walk recursively
    all_json_files = list_all_files(base_path, extension=".json")

    if not all_json_files:
        st.warning("No snapshot files found.")
        return

    # Label mapping
    label_map = {build_snapshot_display_label(f): f for f in all_json_files}
    selected_label = st.selectbox("Select Snapshot File", options=list(label_map.keys()))
    selected_file = label_map[selected_label]

    st.markdown(f"**File Path:** `{selected_file}`")

    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            raw_json = f.read()
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return

    with st.expander("View Snapshot JSON"):
        st.code(raw_json, language="json")

    if st.button("🗑️ Delete This Snapshot"):
        try:
            os.remove(selected_file)
            st.success(f"Deleted `{os.path.basename(selected_file)}`.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to delete file: {e}")
