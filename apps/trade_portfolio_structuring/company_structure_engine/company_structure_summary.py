# -------------------------------------------------------------------------------------------------
# Company Structure Summary
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring

"""
Company Structure Summary
-------------------------

Builds peer-group summary outputs for the Company Structure Review module.

Responsibilities:
- Calculate PE spread
- Build peer averages
- Build ranking table
- Build difference-from-peer-average table
- Generate headline summary labels
- Build observation context scaffold for AI export
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------------------------
METRIC_COLUMNS = [
    "Trailing_PE",
    "Forward_PE",
    "PE_Spread",
    "Revenue_Growth_Pct",
    "Operating_Margin_Pct",
    "Short_Interest_Pct",
]

DISPLAY_LABELS = {
    "Trailing_PE": "Trailing P/E",
    "Forward_PE": "Forward P/E",
    "PE_Spread": "P/E Spread",
    "Revenue_Growth_Pct": "Revenue Growth %",
    "Operating_Margin_Pct": "Operating Margin %",
    "Short_Interest_Pct": "Short Interest %",
}


# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_metric_label(df: pd.DataFrame, metric: str, ascending: bool = False) -> str:
    if metric not in df.columns:
        return "N/A"

    valid_df = df.dropna(subset=[metric])

    if valid_df.empty:
        return "N/A"

    sorted_df = valid_df.sort_values(metric, ascending=ascending)
    row = sorted_df.iloc[0]

    value = row[metric]
    company = row["Company"]

    if pd.isna(value):
        return "N/A"

    if metric.endswith("_Pct"):
        return f"{company} ({value:.2f}%)"

    return f"{company} ({value:.2f})"


def _build_peer_average_df(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for metric in METRIC_COLUMNS:
        if metric not in df.columns:
            continue

        metric_avg = df[metric].mean(skipna=True)
        metric_median = df[metric].median(skipna=True)

        rows.append({
            "Metric": DISPLAY_LABELS.get(metric, metric),
            "Peer_Average": metric_avg,
            "Peer_Median": metric_median,
            "Available_Observations": int(df[metric].notna().sum()),
            "Missing_Observations": int(df[metric].isna().sum()),
        })

    return pd.DataFrame(rows)


def _build_ranking_df(df: pd.DataFrame) -> pd.DataFrame:
    ranking_df = df[["Company", "Ticker"]].copy()

    for metric in METRIC_COLUMNS:
        if metric not in df.columns:
            continue

        ranking_df[f"{metric}_Rank"] = df[metric].rank(
            ascending=False,
            method="min",
        )

    return ranking_df


def _build_peer_difference_df(df: pd.DataFrame) -> pd.DataFrame:
    diff_df = df[["Company", "Ticker"]].copy()

    for metric in METRIC_COLUMNS:
        if metric not in df.columns:
            continue

        metric_avg = df[metric].mean(skipna=True)

        diff_df[f"{metric}_Peer_Avg"] = metric_avg
        diff_df[f"{metric}_Diff"] = df[metric] - metric_avg

        diff_df[f"{metric}_Diff_Pct"] = np.where(
            metric_avg != 0,
            ((df[metric] - metric_avg) / abs(metric_avg)) * 100,
            np.nan,
        )

    return diff_df


# -------------------------------------------------------------------------------------------------
# Main Summary Builder
# -------------------------------------------------------------------------------------------------
def build_company_structure_summary(df: pd.DataFrame) -> dict:
    df_summary = df.copy()

    if "PE_Spread" not in df_summary.columns:
        df_summary["PE_Spread"] = (
            df_summary["Trailing_PE"] - df_summary["Forward_PE"]
        )

    peer_average_df = _build_peer_average_df(df_summary)
    ranking_df = _build_ranking_df(df_summary)
    peer_difference_df = _build_peer_difference_df(df_summary)

    observation_context = {
        "companies_reviewed": int(len(df_summary)),
        "available_metrics": [
            metric for metric in METRIC_COLUMNS
            if metric in df_summary.columns
        ],
        "missing_values": {
            metric: int(df_summary[metric].isna().sum())
            for metric in METRIC_COLUMNS
            if metric in df_summary.columns
        },
        "peer_averages": peer_average_df.to_dict(orient="records"),
    }

    return {
        "highest_trailing_pe_label": _safe_metric_label(
            df_summary,
            "Trailing_PE",
            ascending=False,
        ),
        "lowest_trailing_pe_label": _safe_metric_label(
            df_summary,
            "Trailing_PE",
            ascending=True,
        ),
        "highest_forward_pe_label": _safe_metric_label(
            df_summary,
            "Forward_PE",
            ascending=False,
        ),
        "lowest_forward_pe_label": _safe_metric_label(
            df_summary,
            "Forward_PE",
            ascending=True,
        ),
        "highest_growth_label": _safe_metric_label(
            df_summary,
            "Revenue_Growth_Pct",
            ascending=False,
        ),
        "highest_margin_label": _safe_metric_label(
            df_summary,
            "Operating_Margin_Pct",
            ascending=False,
        ),
        "highest_short_interest_label": _safe_metric_label(
            df_summary,
            "Short_Interest_Pct",
            ascending=False,
        ),
        "peer_average_df": peer_average_df,
        "ranking_df": ranking_df,
        "peer_difference_df": peer_difference_df,
        "observation_context": observation_context,
    }
