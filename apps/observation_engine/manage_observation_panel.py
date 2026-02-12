# -------------------------------------------------------------------------------------------------
# 📋 Manage Observations Panel
# -------------------------------------------------------------------------------------------------

import os
import sys
import pandas as pd
import streamlit as st

# 📦 Add path to access emoji.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "constants")))
from emoji import FLAGS  # Reusable flag dictionary

from insight_loader import list_all_files

# -------------------------------------------------------------------------------------------------
# 🏷️ File Display Label Builder
# -------------------------------------------------------------------------------------------------

def build_file_display_label(filepath: str) -> str:
    """
    Builds a clean and user-friendly display label for an observation file.
    Applies emoji flag and resolves canonical module group names.
    """
    # Parse path
    path_parts = filepath.split(os.sep)

    try:
        raw_group = path_parts[-2]
    except IndexError:
        raw_group = "unknown"

    # Canonical module group overrides
    MODULE_GROUP_LABELS = {
        "price_action": "Trade & Portfolio Structuring",
        "trade_timing": "Trade & Portfolio Structuring",
        "trade_structuring": "Trade & Portfolio Structuring",
        "trade_history": "Trade & Portfolio Structuring",
        "live_portfolio": "Trade & Portfolio Structuring",
        "market_scanner": "Trade & Portfolio Structuring",
    }

    # Final group label
    group_label = MODULE_GROUP_LABELS.get(raw_group.lower(), raw_group.replace("_", " ").title())

    # Filename parts
    filename = os.path.basename(filepath)
    parts = filename.replace("__user_observations.csv", "").split("__")

    if len(parts) < 2:
        return f"📄 {filename}"

    country_or_scope = parts[0].replace("_", " ").title()
    theme_title = parts[1].replace("_", " ").title()

    # Flag
    emoji_flag = FLAGS.get(country_or_scope, "🗂️")

    # Label builder
    if country_or_scope.lower() in ["default", "global"]:
        country_label = f"{emoji_flag} "
    else:
        country_label = f"{emoji_flag} {country_or_scope} — "

    return f"{country_label}{theme_title} ({group_label})"

# -------------------------------------------------------------------------------------------------
# 📋 Main Panel Renderer
# -------------------------------------------------------------------------------------------------

def render_manage_observations_panel():
    st.header("📋 Manage Observations")
    st.caption("Edit or delete saved observations by selecting a file. Changes are written directly to the original CSV.")

    # 🔄 Reload button
    if st.button("🔄 Reload Observation Files"):
        st.rerun()

    # 📂 Load observation file paths
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
    all_files = list_all_files(base_path, extension=".csv")

    if not all_files:
        st.warning("No observation files found.")
        return

    # 🏷️ Build display labels
    file_options = {
        build_file_display_label(path): path
        for path in all_files
    }

    selected_label = st.selectbox("📁 Select Observation File", options=list(file_options.keys()))
    selected_file = file_options[selected_label]

    try:
        df = pd.read_csv(selected_file)
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
        return

    if df.empty:
        st.info("This file contains no observations.")
        return

    # ✍️ Inline Editor
    st.markdown("### 📝 Edit or Delete Observations")
    st.caption("Double-click to edit fields or use the row selector to delete entries. All changes are saved on confirmation.")

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        width='stretch',
        key="editor_observations"
    )

    # 💾 Save button
    if st.button("💾 Save Changes"):
        try:
            edited_df.to_csv(selected_file, index=False)
            st.success(f"✅ Changes saved to `{os.path.basename(selected_file)}`.")
        except Exception as e:
            st.error(f"❌ Failed to save file: {e}")
