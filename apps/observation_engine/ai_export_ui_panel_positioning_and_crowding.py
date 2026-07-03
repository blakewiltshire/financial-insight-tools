# -------------------------------------------------------------------------------------------------
# AI Export Panel — Positioning & Crowding
# -------------------------------------------------------------------------------------------------

import os
import sys
import json
from datetime import datetime, UTC
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup — Use canonical pathing structure
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.helpers import get_named_paths  # Canonical import
from observation_engine.json_helpers import make_json_safe

# -------------------------------------------------------------------------------------------------
# Resolve Project and App Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

OBSERVATION_PATH = os.path.join(
    APP_PATH,
    "observation_engine",
    "storage",
    "ai_bundles",
    "positioning_and_crowding"
)

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_slug(value: str) -> str:
    if not value:
        return "unnamed_snapshot"

    slug = value.lower().strip()
    slug = slug.replace(" & ", " and ")
    slug = slug.replace("/", "_")
    slug = slug.replace("\\", "_")
    slug = slug.replace(" - ", "_")
    slug = slug.replace(" — ", "_")
    slug = slug.replace(" ", "_")

    cleaned = []
    for char in slug:
        if char.isalnum() or char == "_":
            cleaned.append(char)

    slug = "".join(cleaned)

    while "__" in slug:
        slug = slug.replace("__", "_")

    return slug.strip("_") or "unnamed_snapshot"


# -------------------------------------------------------------------------------------------------
# Render Function — AI Export Panel
# -------------------------------------------------------------------------------------------------
def render_ai_export_panel(snapshot_results: dict, base_asset: str, asset_type_display: str):
    """
    Renders the AI Export UI Panel for Positioning & Crowding.

    Expects a page-native positioning snapshot structure.
    """

    st.markdown("### AI Export — Positioning & Crowding Snapshot")
    st.caption(
        "This export captures the selected positioning market, crowding context, "
        "percentile state, and flip behaviour. No AI scoring is applied."
    )

    snapshot_metadata = snapshot_results.get("snapshot_metadata", {})
    analysis_summary = snapshot_results.get("analysis_summary", {})
    positioning_context = analysis_summary.get("positioning_context", {})
    positioning_summary = analysis_summary.get("positioning_summary", {})

    export_bundle = {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": snapshot_metadata.get("theme", {}).get("code", "positioning_and_crowding"),
                "title": snapshot_metadata.get("theme", {}).get("title", "Positioning & Crowding")
            },
            "snapshot_timestamp": snapshot_metadata.get("snapshot_timestamp") or datetime.now(UTC).isoformat(),
            "asset_type": asset_type_display,
            "selected_market": snapshot_metadata.get("selected_market")
        },
        "analysis_summary": {
            "positioning_context": positioning_context,
            "positioning_summary": positioning_summary
        },
        "metadata": snapshot_results.get("metadata", {})
    }

    st.json(export_bundle, expanded=False)

    replace_existing = st.toggle("🔁 Replace existing entry if it already exists", value=True)

    if st.button("📌 Save Macro Insights"):
        os.makedirs(OBSERVATION_PATH, exist_ok=True)

        selected_market = export_bundle.get("snapshot_metadata", {}).get("selected_market", base_asset)
        filename = f"positioning_and_crowding__{_safe_slug(selected_market)}.json"
        save_path = os.path.join(OBSERVATION_PATH, filename)

        if os.path.exists(save_path) and not replace_existing:
            st.warning("A saved snapshot already exists for this market. Enable replace to overwrite it.")
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(make_json_safe(export_bundle), f, indent=4)

        st.success(f"📁 Snapshot saved to `{save_path}`")
