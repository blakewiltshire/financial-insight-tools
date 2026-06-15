# -------------------------------------------------------------------------------------------------
# Company Structure Visualisation
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring

"""
Company Structure Visualisation
-------------------------------

Chart rendering helpers for the Company Structure Review module.

These visuals are comparative and observational. They do not provide
investment recommendations, valuation opinions, or trade signals.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st


# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _metric_available(df: pd.DataFrame, metric: str) -> bool:
    return metric in df.columns and df[metric].notna().any()


def _sorted_metric_df(
    df: pd.DataFrame,
    metric: str,
    ascending: bool = False,
) -> pd.DataFrame:
    if not _metric_available(df, metric):
        return pd.DataFrame()

    return (
        df[["Company", "Ticker", metric]]
        .dropna(subset=[metric])
        .sort_values(metric, ascending=ascending)
        .reset_index(drop=True)
    )


def _render_bar_chart(
    df: pd.DataFrame,
    metric: str,
    title: str,
    y_axis_title: str,
    ascending: bool = False,
):
    chart_df = _sorted_metric_df(df, metric, ascending=ascending)

    if chart_df.empty:
        st.info(f"No available data for {title}.")
        return

    fig = px.bar(
        chart_df,
        x=metric,
        y="Company",
        orientation="h",
        title=title,
        hover_data=["Ticker"],
        template="plotly_white",
    )

    fig.update_layout(
        xaxis_title=y_axis_title,
        yaxis_title="Company",
        height=max(420, 36 * len(chart_df)),
        margin={"l": 20, "r": 20, "t": 55, "b": 35},
    )

    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, width="stretch")


def _render_peer_average_table(
    df: pd.DataFrame,
    metric: str,
    metric_label: str,
):
    if not _metric_available(df, metric):
        st.info(f"No available data for {metric_label}.")
        return

    metric_avg = df[metric].mean(skipna=True)

    table_df = df[["Company", "Ticker", metric]].copy()
    table_df = table_df.dropna(subset=[metric])
    table_df["Peer_Average"] = metric_avg
    table_df["Difference"] = table_df[metric] - metric_avg
    table_df["Difference_Pct"] = (
        (table_df["Difference"] / abs(metric_avg)) * 100
        if metric_avg != 0
        else pd.NA
    )

    table_df = table_df.sort_values(metric, ascending=False)

    st.dataframe(
        table_df,
        width="stretch",
        hide_index=True,
    )


# -------------------------------------------------------------------------------------------------
# Market Expectations
# -------------------------------------------------------------------------------------------------
def render_valuation_comparison(df: pd.DataFrame):
    st.markdown("### Market Expectations")
    st.caption(
        "Compare trailing and forward valuation multiples across the selected peer group. "
        "P/E spread is calculated as trailing P/E minus forward P/E."
    )

    col1, col2 = st.columns(2)

    with col1:
        _render_bar_chart(
            df,
            "Trailing_PE",
            "Trailing P/E Comparison",
            "Trailing P/E",
            ascending=False,
        )

    with col2:
        _render_bar_chart(
            df,
            "Forward_PE",
            "Forward P/E Comparison",
            "Forward P/E",
            ascending=False,
        )

    st.markdown("### P/E Spread")
    _render_bar_chart(
        df,
        "PE_Spread",
        "P/E Spread Comparison",
        "Trailing P/E - Forward P/E",
        ascending=False,
    )

    with st.expander("Peer Average Context — Valuation"):
        st.markdown("#### Trailing P/E")
        _render_peer_average_table(df, "Trailing_PE", "Trailing P/E")

        st.markdown("#### Forward P/E")
        _render_peer_average_table(df, "Forward_PE", "Forward P/E")

        st.markdown("#### P/E Spread")
        _render_peer_average_table(df, "PE_Spread", "P/E Spread")


# -------------------------------------------------------------------------------------------------
# Growth & Quality
# -------------------------------------------------------------------------------------------------
def render_growth_quality_panel(df: pd.DataFrame):
    st.markdown("### Growth & Quality")
    st.caption(
        "Review revenue growth and operating margin across the selected company group. "
        "These measures provide context around growth profile and operating profitability."
    )

    col1, col2 = st.columns(2)

    with col1:
        _render_bar_chart(
            df,
            "Revenue_Growth_Pct",
            "Revenue Growth Comparison",
            "Revenue Growth (%)",
            ascending=False,
        )

    with col2:
        _render_bar_chart(
            df,
            "Operating_Margin_Pct",
            "Operating Margin Comparison",
            "Operating Margin (%)",
            ascending=False,
        )

    with st.expander("Peer Average Context — Growth & Quality"):
        st.markdown("#### Revenue Growth")
        _render_peer_average_table(df, "Revenue_Growth_Pct", "Revenue Growth")

        st.markdown("#### Operating Margin")
        _render_peer_average_table(df, "Operating_Margin_Pct", "Operating Margin")


# -------------------------------------------------------------------------------------------------
# Market Skepticism
# -------------------------------------------------------------------------------------------------
def render_market_skepticism_panel(df: pd.DataFrame):
    st.markdown("### Market Skepticism")
    st.caption(
        "Compare short interest across the selected peer group. "
        "Short interest may indicate areas of market disagreement or scepticism."
    )

    _render_bar_chart(
        df,
        "Short_Interest_Pct",
        "Short Interest Comparison",
        "Short Interest (%)",
        ascending=False,
    )

    with st.expander("Peer Average Context — Short Interest"):
        _render_peer_average_table(df, "Short_Interest_Pct", "Short Interest")
