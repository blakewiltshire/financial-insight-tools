# -------------------------------------------------------------------------------------------------
# AI Export Snapshot Builder — Market Structure Review
# -------------------------------------------------------------------------------------------------

from datetime import datetime, UTC
import pandas as pd


def _safe_records(df):
    if df is None or df.empty:
        return []

    clean_df = df.copy()
    clean_df = clean_df.astype(object).where(pd.notna(clean_df), None)

    return clean_df.to_dict(orient="records")


def build_macro_insight_snapshot_market_structure_review(
    theme_code: str,
    theme_title: str,
    dataset_name: str,
    profile_df,
    events_df,
    summary_payload: dict,
    contextual_insight: str,
) -> dict:
    """
    Build AI-ready snapshot for Market Structure Review.

    Exports focus-asset context, market structure profile, supply events,
    comparison context, observation scaffold, and perspective lenses.
    """

    observation_context = summary_payload.get("observation_context", {})
    focus_context = observation_context.get("focus_asset_context", {})
    comparison_context = observation_context.get("comparison_context", {})

    focus_supply_events = focus_context.get("supply_events", [])
    comparison_assets = comparison_context.get("comparison_assets", [])

    return {
        "snapshot_metadata": {
            "theme": {
                "code": theme_code,
                "title": theme_title,
            },
            "snapshot_timestamp": datetime.now(UTC).isoformat(),
            "dataset": dataset_name,
            "module_type": "market_structure_review",
        },
        "analysis_summary": {
            "focus_asset": {
                "company": summary_payload.get("focus_company"),
                "ticker": summary_payload.get("focus_ticker"),
                "structure_type": summary_payload.get("focus_structure_type"),
                "mapped_supply_events": summary_payload.get("focus_event_count"),
            },
            "dataset_context": {
                "dataset_name": dataset_name,
                "assets_reviewed": int(len(profile_df)) if profile_df is not None else 0,
                "comparison_assets": comparison_assets,
                "available_tickers": observation_context.get(
                    "dataset_context", {}
                ).get("available_tickers", []),
            },
            "structural_summary": summary_payload.get("structural_summary", ""),
            "structure_profiles": _safe_records(profile_df),
            "supply_events": _safe_records(events_df),
            "focus_supply_events": focus_supply_events,
            "observation_context": observation_context,
        },
        "metadata": {
            "snapshot_notes": (
                "Generated from Market Structure Review. Outputs are observational "
                "and non-advisory."
            )
        },
    }
