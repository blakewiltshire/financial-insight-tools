# -------------------------------------------------------------------------------------------------
# AI Export Panel — Market & Volatility Scanner
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
from registry.stats_metadata_registry import STATISTICAL_METADATA
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
    "market_volatility",
)

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_slug(value: str) -> str:
    if not value:
        return "unknown"

    slug = str(value).lower().strip()
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

    return slug.strip("_") or "unknown"


# -------------------------------------------------------------------------------------------------
# Render Function — AI Export Panel
# -------------------------------------------------------------------------------------------------
def render_ai_export_panel(snapshot_results: dict, base_asset: str, asset_type_display: str):
    """
    Renders the AI Export UI Panel for the Market & Volatility Scanner.
    Builds a clean export structure using only metadata registry and snapshot fields.
    """

    st.markdown("### AI Export — Market & Volatility Scanner Snapshot")
    st.caption(
        "This export summarises key statistical insights using structured metadata. "
        "No AI scoring is applied."
    )

    # -------------------------------------------
    # Extract Sectioned Results from Snapshot
    # -------------------------------------------
    statistical_sections = snapshot_results.get("statistical_analysis", {})
    context_parameters = statistical_sections.get("context_parameters", {})
    metadata_summary = []

    for section_name, indicators in statistical_sections.items():
        if not isinstance(indicators, dict) or section_name == "context_parameters":
            continue

        for indicator, value in indicators.items():
            meta_block = STATISTICAL_METADATA.get(section_name, {}).get(indicator, {})

            if isinstance(meta_block, dict) and any(
                isinstance(v, dict) for v in meta_block.values()
            ):
                meta_values = list(meta_block.values())
                meta = {
                    "overview": meta_values[0].get("overview", ""),
                    "why_it_matters": meta_values[0].get("why_it_matters", ""),
                    "temporal_categorisation": meta_values[0].get(
                        "temporal_categorisation",
                        "",
                    ),
                    "investment_action_importance": meta_values[0].get(
                        "investment_action_importance",
                        "",
                    ),
                }
            else:
                meta = meta_block if isinstance(meta_block, dict) else {}

            metadata_summary.append(
                {
                    "section": section_name,
                    "indicator": indicator,
                    "value": value,
                    "overview": meta.get("overview", ""),
                    "why_it_matters": meta.get("why_it_matters", ""),
                    "temporal_categorisation": meta.get(
                        "temporal_categorisation",
                        "",
                    ),
                    "investment_action_importance": meta.get(
                        "investment_action_importance",
                        "",
                    ),
                }
            )

    # -------------------------------------------
    # Build Final Export Bundle
    # -------------------------------------------
    export_bundle = {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": "market_volatility",
                "title": "Market Volatility",
            },
            "snapshot_timestamp": snapshot_results.get("snapshot_metadata", {}).get(
                "snapshot_timestamp"
            )
            or datetime.now(UTC).isoformat(),
            "asset_type": asset_type_display,
            "module_group": "Trade & Portfolio Structuring",
            "use_case": "statistics",
        },
        "context_parameters": context_parameters,
        "macro_signals": metadata_summary,
        "metadata": snapshot_results.get("metadata", {}),
    }

    # -------------------------------------------
    # Display & Save
    # -------------------------------------------
    st.json(export_bundle, expanded=False)

    replace_existing = st.toggle(
        "🔁 Replace existing entry if it already exists",
        value=True,
    )

    if st.button("📌 Save Macro Insights"):
        os.makedirs(OBSERVATION_PATH, exist_ok=True)

        asset_slug = _safe_slug(base_asset)
        use_case_slug = "statistics"

        filename = (
            "trade_and_portfolio_structuring__"
            f"market_volatility__{use_case_slug}__{asset_slug}.json"
        )

        save_path = os.path.join(OBSERVATION_PATH, filename)

        if os.path.exists(save_path) and not replace_existing:
            st.warning(
                "A saved snapshot already exists for this asset. "
                "Enable replace to overwrite it."
            )
            return

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(make_json_safe(export_bundle), f, indent=4)

        st.success(f"📁 Snapshot saved to `{save_path}`")
