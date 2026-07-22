# -------------------------------------------------------------------------------------------------
# AI Export Panel — Live Portfolio Monitor
# -------------------------------------------------------------------------------------------------

import json
import os
import sys
from datetime import datetime, UTC

import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup — Use canonical pathing structure
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.helpers import get_named_paths
from observation_engine.json_helpers import make_json_safe

# -------------------------------------------------------------------------------------------------
# Resolve Project and App Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
APP_PATH = PATHS["level_up_1"]

OBSERVATION_PATH = os.path.join(
    APP_PATH,
    "observation_engine",
    "storage",
    "ai_bundles",
    "live_portfolio_monitor",
)


def _safe_slug(value: str) -> str:
    """Create a stable file-safe slug."""
    if not value:
        return "portfolio_snapshot"

    slug = value.lower().strip()
    slug = slug.replace(" & ", " and ")
    slug = slug.replace("/", "_")
    slug = slug.replace("\\", "_")
    slug = slug.replace(" - ", "_")
    slug = slug.replace(" — ", "_")
    slug = slug.replace(" ", "_")
    slug = "".join(char for char in slug if char.isalnum() or char == "_")

    while "__" in slug:
        slug = slug.replace("__", "_")

    return slug.strip("_") or "portfolio_snapshot"


def render_ai_export_panel(snapshot_results: dict, base_asset: str, asset_type_display: str):
    """Render the optional AI export preview and save controls."""

    st.markdown("### AI Export — Live Portfolio Monitor Snapshot")
    st.caption(
        "This export captures the current position set, FIT exposure calculations, "
        "structural diagnostics, validation findings, and portfolio context. "
        "No AI scoring or broker-account calculation is applied."
    )

    snapshot_metadata = snapshot_results.get("snapshot_metadata", {})
    analysis_summary = snapshot_results.get("analysis_summary", {})

    export_bundle = {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": snapshot_metadata.get("theme", {}).get(
                    "code", "live_portfolio"
                ),
                "title": snapshot_metadata.get("theme", {}).get(
                    "title", "Live Portfolio Monitor"
                ),
            },
            "snapshot_timestamp": snapshot_metadata.get("snapshot_timestamp")
            or datetime.now(UTC).isoformat(),
            "asset_type": asset_type_display,
            "dataset": snapshot_metadata.get("dataset", base_asset),
            "module_type": snapshot_metadata.get(
                "module_type", "live_portfolio_monitor"
            ),
            "portfolio_scope": snapshot_metadata.get("portfolio_scope", {}),
        },
        "analysis_summary": {
            "account_configuration": analysis_summary.get(
                "account_configuration", {}
            ),
            "portfolio_summary": analysis_summary.get("portfolio_summary", {}),
            "position_records": analysis_summary.get("position_records", []),
            "exposure_summary": analysis_summary.get("exposure_summary", {}),
            "structural_diagnostics": analysis_summary.get(
                "structural_diagnostics", {}
            ),
            "validation": analysis_summary.get("validation", {}),
        },
        "metadata": snapshot_results.get("metadata", {}),
    }

    st.json(export_bundle, expanded=False)

    replace_existing = st.toggle(
        "🔁 Replace existing entry if it already exists",
        value=True,
        key="live_portfolio_replace_ai_export",
    )

    if st.button("📌 Save Macro Insights", key="save_live_portfolio_ai_export"):
        os.makedirs(OBSERVATION_PATH, exist_ok=True)

        filename = f"live_portfolio_monitor__{_safe_slug(base_asset)}.json"
        save_path = os.path.join(OBSERVATION_PATH, filename)

        if os.path.exists(save_path) and not replace_existing:
            st.warning(
                "A saved snapshot already exists for this portfolio source. "
                "Enable replace to overwrite it."
            )
            return

        with open(save_path, "w", encoding="utf-8") as file_handle:
            json.dump(make_json_safe(export_bundle), file_handle, indent=4)

        st.success(f"📁 Snapshot saved to `{save_path}`")
