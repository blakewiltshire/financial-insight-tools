# -------------------------------------------------------------------------------------------------
# Company Structure Interpretation
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring

"""
Company Structure Interpretation
--------------------------------

Builds lightweight structural interpretation text for the Company Structure Review module.

The output is observational and non-advisory. It does not produce valuation opinions,
investment recommendations, fair value estimates, or trading signals.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_value(value, suffix: str = "") -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}{suffix}"


def _get_metric_leader(df: pd.DataFrame, metric: str, ascending: bool = False):
    if metric not in df.columns:
        return None

    valid_df = df.dropna(subset=[metric])

    if valid_df.empty:
        return None

    row = valid_df.sort_values(metric, ascending=ascending).iloc[0]

    return {
        "company": row.get("Company", "N/A"),
        "ticker": row.get("Ticker", "N/A"),
        "value": row.get(metric),
    }


def _metric_available(df: pd.DataFrame, metric: str) -> bool:
    return metric in df.columns and df[metric].notna().any()


def _peer_average(df: pd.DataFrame, metric: str):
    if not _metric_available(df, metric):
        return None
    return df[metric].mean(skipna=True)

def _peer_median(df: pd.DataFrame, metric: str):
    if not _metric_available(df, metric):
        return None
    return df[metric].median(skipna=True)


# -------------------------------------------------------------------------------------------------
# Interpretation Builder
# -------------------------------------------------------------------------------------------------
def build_company_structure_interpretation(
    dataset_name: str,
    df: pd.DataFrame,
    summary_payload: dict,
) -> str:
    """
    Build a short non-advisory structural interpretation for the selected company group.
    """

    if df is None or df.empty:
        return "No company structure data is available for interpretation."

    company_count = len(df)

    highest_pe = _get_metric_leader(df, "Trailing_PE", ascending=False)
    lowest_pe = _get_metric_leader(df, "Trailing_PE", ascending=True)
    highest_growth = _get_metric_leader(df, "Revenue_Growth_Pct", ascending=False)
    highest_margin = _get_metric_leader(df, "Operating_Margin_Pct", ascending=False)
    highest_short_interest = _get_metric_leader(df, "Short_Interest_Pct", ascending=False)

    trailing_avg = _peer_average(df, "Trailing_PE")
    forward_avg = _peer_average(df, "Forward_PE")
    spread_avg = _peer_average(df, "PE_Spread")
    growth_avg = _peer_average(df, "Revenue_Growth_Pct")
    margin_avg = _peer_average(df, "Operating_Margin_Pct")
    short_avg = _peer_average(df, "Short_Interest_Pct")

    trailing_median = _peer_median(df, "Trailing_PE")
    forward_median = _peer_median(df, "Forward_PE")
    spread_median = _peer_median(df, "PE_Spread")

    paragraphs = []

    paragraphs.append(
        f"The selected dataset contains {company_count} companies within the "
        f"**{dataset_name}** review group. The module compares valuation, growth, "
        "operating profitability, and market scepticism metrics to surface structural "
        "differences across the peer group."
    )

    if (
        highest_pe
        and lowest_pe
        and trailing_avg is not None
        and trailing_median is not None
    ):
        paragraphs.append(
            "Trailing valuation multiples (P/E) range from "
            f"**{lowest_pe['company']}** at **{_safe_value(lowest_pe['value'])}** "
            f"to **{highest_pe['company']}** at **{_safe_value(highest_pe['value'])}**. "
            f"The peer average trailing P/E is **{_safe_value(trailing_avg)}**, "
            f"while the peer median is **{_safe_value(trailing_median)}**. "
            "Differences between average and median values may indicate that one or more "
            "high-multiple companies are materially influencing the peer-group valuation profile."
        )

    if (
        forward_avg is not None
        and forward_median is not None
        and spread_avg is not None
        and spread_median is not None
    ):
        paragraphs.append(
            f"The peer average forward P/E is **{_safe_value(forward_avg)}**, "
            f"while the peer median is **{_safe_value(forward_median)}**. "
            f"The average P/E spread is **{_safe_value(spread_avg)}**, "
            f"with a median spread of **{_safe_value(spread_median)}**. "
            "Positive spreads indicate forward valuation is below trailing valuation, "
            "while negative spreads indicate forward valuation exceeds trailing valuation. "
            "This provides an expectations lens rather than a valuation judgement."
        )

    growth_quality_components = []

    if highest_growth and growth_avg is not None:
        growth_quality_components.append(
            f"Revenue growth is led by **{highest_growth['company']}** at "
            f"**{_safe_value(highest_growth['value'], '%')}**, compared with a peer "
            f"average of **{_safe_value(growth_avg, '%')}**"
        )

    if highest_margin and margin_avg is not None:
        growth_quality_components.append(
            f"operating profitability is led by **{highest_margin['company']}** at "
            f"**{_safe_value(highest_margin['value'], '%')}**, compared with a peer "
            f"average of **{_safe_value(margin_avg, '%')}**"
        )

    if growth_quality_components:
        paragraphs.append(
            ", while ".join(growth_quality_components)
            + ". These metrics provide context around growth profile, operating efficiency, "
              "and the characteristics the market may appear prepared to reward."
        )

    if highest_short_interest and short_avg is not None:
        paragraphs.append(
            f"Short interest is highest for **{highest_short_interest['company']}** at "
            f"**{_safe_value(highest_short_interest['value'], '%')}**, compared with a peer "
            f"average of **{_safe_value(short_avg, '%')}**. Short interest may indicate areas "
            "of market disagreement or scepticism, but it does not by itself determine direction."
        )

    paragraphs.append(
        "These observations support structured review. They do not determine whether a company "
        "is attractive, unattractive, undervalued, or overvalued. The purpose is to clarify "
        "what the market may appear prepared to pay, how that compares with peers, and which "
        "structural questions may merit further interpretation."
    )

    return "\n\n".join(paragraphs)
