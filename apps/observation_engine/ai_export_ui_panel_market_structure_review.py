# -------------------------------------------------------------------------------------------------
# AI Export Panel — Company Structure Review
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
    "market_structure_review"
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
    Renders the AI Export UI Panel for Company Structure Review.
    """

    st.markdown("### AI Export — Market Structure Review Snapshot")
    st.caption(
        "This export captures focus-asset market structure context, ownership and float "
        "characteristics, supply events, comparison context, and observation scaffolding. "
        "No AI scoring is applied."
    )

    snapshot_metadata = snapshot_results.get("snapshot_metadata", {})
    analysis_summary = snapshot_results.get("analysis_summary", {})

    export_bundle = {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": snapshot_metadata.get("theme", {}).get(
                    "code",
                    "market_structure_review",
                ),
                "title": snapshot_metadata.get("theme", {}).get(
                    "title",
                    "Market Structure Review",
                ),
            },
            "snapshot_timestamp": snapshot_metadata.get(
                "snapshot_timestamp"
            ) or datetime.now(UTC).isoformat(),
            "asset_type": asset_type_display,
            "dataset": snapshot_metadata.get("dataset", base_asset),
            "module_type": snapshot_metadata.get(
                "module_type",
                "market_structure_review",
            ),
        },
        "analysis_summary": {
            "focus_asset": analysis_summary.get(
                "focus_asset",
                {},
            ),
            "dataset_context": analysis_summary.get(
                "dataset_context",
                {},
            ),
            "structural_summary": analysis_summary.get(
                "structural_summary",
                "",
            ),
            "structure_profiles": analysis_summary.get(
                "structure_profiles",
                [],
            ),
            "supply_events": analysis_summary.get(
                "supply_events",
                [],
            ),
            "focus_supply_events": analysis_summary.get(
                "focus_supply_events",
                [],
            ),
            "observation_context": analysis_summary.get(
                "observation_context",
                {},
            ),
        },
        "metadata": snapshot_results.get("metadata", {}),
    }

    st.json(export_bundle, expanded=False)

    replace_existing = st.toggle(
        "🔁 Replace existing entry if it already exists",
        value=True,
    )

    if st.button("📌 Save Macro Insights"):
        os.makedirs(OBSERVATION_PATH, exist_ok=True)

        dataset_name = export_bundle.get("snapshot_metadata", {}).get(
            "dataset",
            base_asset,
        )
        filename = f"market_structure_review__{_safe_slug(dataset_name)}.json"
        save_path = os.path.join(OBSERVATION_PATH, filename)

        if os.path.exists(save_path) and not replace_existing:
            st.warning(
                "A saved snapshot already exists for this dataset. "
                "Enable replace to overwrite it."
            )
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(export_bundle, f, indent=4)

        st.success(f"📁 Snapshot saved to `{save_path}`")
