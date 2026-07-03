# -------------------------------------------------------------------------------------------------
# AI Export Panel — Relative Macro Transmission
# -------------------------------------------------------------------------------------------------

import os
import sys
import json
import datetime as dt
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
    "relative_macro_transmission"
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
    Renders the AI Export UI Panel for Relative Macro Transmission.

    Expects a page-native RMT snapshot structure.
    """

    st.markdown("### AI Export — Relative Macro Transmission Snapshot")
    st.caption(
        "This export captures the selected comparison context and transmission state. "
        "No AI scoring is applied."
    )

    snapshot_metadata = snapshot_results.get("snapshot_metadata", {})
    analysis_summary = snapshot_results.get("analysis_summary", {})
    comparison_context = analysis_summary.get("comparison_context", {})
    transmission_summary = analysis_summary.get("transmission_summary", {})

    export_bundle = {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": snapshot_metadata.get("theme", {}).get("code", "relative_macro_transmission"),
                "title": snapshot_metadata.get("theme", {}).get("title", "Relative Macro Transmission")
            },
            "snapshot_timestamp": snapshot_metadata.get("snapshot_timestamp") or datetime.now(UTC).isoformat(),
            "asset_type": asset_type_display,
            "use_case": snapshot_metadata.get("use_case")
        },
        "analysis_summary": {
            "comparison_context": comparison_context,
            "transmission_summary": transmission_summary
        },
        "metadata": snapshot_results.get("metadata", {})
    }

    st.json(export_bundle, expanded=False)

    replace_existing = st.toggle("🔁 Replace existing entry if it already exists", value=True)

    if st.button("📌 Save Macro Insights"):
        os.makedirs(OBSERVATION_PATH, exist_ok=True)

        use_case = export_bundle.get("snapshot_metadata", {}).get("use_case", base_asset)
        filename = f"relative_macro_transmission__{_safe_slug(use_case)}.json"
        save_path = os.path.join(OBSERVATION_PATH, filename)

        if os.path.exists(save_path) and not replace_existing:
            st.warning("A saved snapshot already exists for this use case. Enable replace to overwrite it.")
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(make_json_safe(export_bundle), f, indent=4)

        st.success(f"📁 Snapshot saved to `{save_path}`")
