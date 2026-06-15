# -------------------------------------------------------------------------------------------------
# AI Export Snapshot Builder — Company Structure Review
# -------------------------------------------------------------------------------------------------

from datetime import datetime, UTC
import pandas as pd

def _safe_records(df):
    if df is None or df.empty:
        return []

    clean_df = df.copy()
    clean_df = clean_df.astype(object).where(pd.notna(clean_df), None)

    return clean_df.to_dict(orient="records")


def build_macro_insight_snapshot_company_structure_review(
    theme_code: str,
    theme_title: str,
    dataset_name: str,
    df,
    summary_payload: dict,
    contextual_insight: str,
) -> dict:
    """
    Build AI-ready snapshot for Company Structure Review.

    Exports module context, dataset context, headline observations,
    structural interpretation, peer context, and supporting comparison table.
    """

    comparison_table = _safe_records(df)

    peer_average_df = summary_payload.get("peer_average_df")
    ranking_df = summary_payload.get("ranking_df")
    peer_difference_df = summary_payload.get("peer_difference_df")

    return {
        "snapshot_metadata": {
            "theme": {
                "code": theme_code,
                "title": theme_title,
            },
            "snapshot_timestamp": datetime.now(UTC).isoformat(),
            "dataset": dataset_name,
            "module_type": "company_structure_review",
        },
        "analysis_summary": {
            "dataset_context": {
                "dataset_name": dataset_name,
                "companies_reviewed": int(len(df)) if df is not None else 0,
                "companies": (
                    df["Company"].dropna().astype(str).tolist()
                    if df is not None and "Company" in df.columns
                    else []
                ),
            },
            "headline_summary": {
                "highest_trailing_valuation": summary_payload.get("highest_trailing_pe_label"),
                "highest_revenue_growth": summary_payload.get("highest_growth_label"),
                "highest_operating_profitability": summary_payload.get("highest_margin_label"),
                "highest_short_interest": summary_payload.get("highest_short_interest_label"),
            },
            "structural_interpretation": contextual_insight,
            "company_structure_comparison": comparison_table,
            "peer_group_metrics": _safe_records(peer_average_df),
            "peer_rankings": _safe_records(ranking_df),
            "peer_difference_context": _safe_records(peer_difference_df),
            "observation_context": summary_payload.get("observation_context", {}),
        },
        "metadata": {
            "snapshot_notes": (
                "Generated from Company Structure Review. "
                "Outputs are observational and non-advisory."
            )
        },
    }
