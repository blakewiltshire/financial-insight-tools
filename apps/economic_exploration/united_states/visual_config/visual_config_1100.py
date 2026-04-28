# -------------------------------------------------------------------------------------------------
# Visual Config (Local Extension)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument, unused-import

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Visual Configuration — Economic Exploration Suite
-----------------------------------------------------------------

Defines the country- or theme-specific visual rendering extensions for
Economic Exploration modules (Themes 100–2100+). This module extends the
universal charting engine, enabling more granular visualisation layers.

Role in the System:
- Adds localised chart overlays, sector breakdowns, and country-specific displays.
- Controls tab and subtab layouts per Use Case.
- Dynamically routes visual rendering based on the selected Use Case.

System Design Notes:
- Visual rendering is fully independent of indicator signal evaluation.
- **Use Case selection controls visual rendering**, with charts configured here.
- Chart data slices are passed via `df_map`, based on timeframe windows handled locally.
- Visual keys, tab names, subtab structures, and display logic are fully controlled here.
- This local module **does not reference indicator_map_XXX.py or insights** directly.

Architecture Summary:
- Each Use Case receives its own visualisation block inside `render_all_charts_local()`.
- Subtabs are always required (even for single-chart cases) to ensure consistent UI structure.
- Chart keys are managed via `display_chart_with_fallback()` to prevent Streamlit key conflicts.
- Local visuals may call universal chart functions (e.g., from `universal_visual_config_XXX.py`) for consistency.

Usage:
- Invoked automatically from the main theme module (`100_economic_growth_stability.py`, `200_labour_market_dynamics.py`, etc.)
- Required only when country- or theme-specific visuals are implemented.
- If no local visual config exists, universal visuals render by default.

AI Implementation Notes:
- Visual tab structure is critical for AI narrative consistency and export accuracy.
- Subtab names, chart labels, and layout stability directly influence AI macro narrative parsing.

"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys
import uuid

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))

if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Template Chart Imports
# -------------------------------------------------------------------------------------------------
from universal_visual_config_1100 import (
    display_chart_with_fallback,
    plot_signal_a_chart,
    plot_signal_b_chart,
    plot_signal_c_chart,
)

# -------------------------------------------------------------------------------------------------
# Shared Statistical Profile Import
# -------------------------------------------------------------------------------------------------
from universal_visual_shared import calculate_statistical_profile


# -------------------------------------------------------------------------------------------------
# Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    return {
        "Signal A": "Signal A — Time Series",
        "Signal B": "Signal B — Rolling Average",
        "Signal C": "Signal C — Band Highlight",
        "Aggregate Equity Allocation": "Aggregate Equity Allocation",
    }


# -------------------------------------------------------------------------------------------------
# Local Helpers
# -------------------------------------------------------------------------------------------------
def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = df.copy()

    if "date" not in df.columns:
        df = df.reset_index()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).sort_values("date")

    return df


def _slice_df_by_period_label(df: pd.DataFrame, period_label: str) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = _prepare_df(df)

    mapping = {
        "Last 3 Periods": 3,
        "Last 6 Periods": 6,
        "Last 12 Periods": 12,
        "Last 24 Periods": 24,
        "Last 60 Periods": 60,
        "Full History": None,
    }

    limit = mapping.get(period_label)

    if limit is None:
        return df.copy()

    return df.tail(limit).copy()


def _get_visual_df(df_map: dict, dataset_key: str, period_label: str) -> pd.DataFrame:
    df = df_map.get(dataset_key)
    return _slice_df_by_period_label(df, period_label)


def _get_stable_series_selection(widget_key: str, options: list[str], default_index: int = 0) -> str | None:
    if not options:
        return None

    if widget_key not in st.session_state or st.session_state[widget_key] not in options:
        st.session_state[widget_key] = options[default_index]

    selected = st.selectbox(
        "Select series for statistical profile",
        options=options,
        index=options.index(st.session_state[widget_key]),
        key=f"{widget_key}__selectbox",
    )

    st.session_state[widget_key] = selected
    return selected


# -------------------------------------------------------------------------------------------------
# Local AEA Chart Functions
# -------------------------------------------------------------------------------------------------
def plot_equity_market_value_chart(df: pd.DataFrame) -> go.Figure:
    required_cols = [
        "date",
        "Domestic Financial Sector Equities",
        "Nonfinancial Corporate Equities",
    ]

    if df is None or df.empty or not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Domestic Financial Sector Equities"],
        mode="lines",
        name="Domestic Financial Sector Equities",
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Nonfinancial Corporate Equities"],
        mode="lines",
        name="Nonfinancial Corporate Equities",
    ))

    fig.update_layout(
        title="Equity Market Value",
        xaxis_title="Date",
        yaxis_title="Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def plot_liability_structure_chart(df: pd.DataFrame) -> go.Figure:
    required_cols = [
        "date",
        "Central Government Debt Liabilities",
        "State Local Government Debt Liabilities",
        "Nonfinancial Corporate Debt Liabilities",
        "Household Nonprofit Debt Liabilities",
        "Rest Of World Debt Liabilities",
    ]

    if df is None or df.empty or not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    for col in required_cols:
        if col == "date":
            continue

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df[col],
            mode="lines",
            name=col,
        ))

    fig.update_layout(
        title="Liability Structure",
        xaxis_title="Date",
        yaxis_title="Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def _build_aear_series(df: pd.DataFrame) -> pd.Series:
    required_cols = [
        "Domestic Financial Sector Equities",
        "Nonfinancial Corporate Equities",
        "Central Government Debt Liabilities",
        "State Local Government Debt Liabilities",
        "Nonfinancial Corporate Debt Liabilities",
        "Household Nonprofit Debt Liabilities",
        "Rest Of World Debt Liabilities",
    ]

    if df is None or df.empty or not all(col in df.columns for col in required_cols):
        return pd.Series(dtype=float)

    total_equity_market_value = (
        df["Domestic Financial Sector Equities"].fillna(0)
        + df["Nonfinancial Corporate Equities"].fillna(0)
    )

    total_real_economy_liabilities = (
        df["Central Government Debt Liabilities"].fillna(0)
        + df["State Local Government Debt Liabilities"].fillna(0)
        + df["Nonfinancial Corporate Debt Liabilities"].fillna(0)
        + df["Household Nonprofit Debt Liabilities"].fillna(0)
        + df["Rest Of World Debt Liabilities"].fillna(0)
    )

    aear = total_equity_market_value / (
        total_equity_market_value + total_real_economy_liabilities
    ).replace(0, pd.NA)

    aear.name = "Aggregate Equity Allocation Ratio"
    return aear


def plot_aggregate_equity_allocation_ratio_chart(df: pd.DataFrame) -> go.Figure:
    if df is None or df.empty or "date" not in df.columns:
        return go.Figure()

    aear = _build_aear_series(df)

    if aear.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=aear,
        mode="lines",
        name="Aggregate Equity Allocation Ratio",
    ))

    fig.update_layout(
        title="Aggregate Equity Allocation Ratio",
        xaxis_title="Date",
        yaxis_title="Ratio",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def _build_standardised_overlay(
    aear_df: pd.DataFrame,
    comparator_df: pd.DataFrame,
    comparator_col: str,
) -> pd.DataFrame:
    if aear_df is None or aear_df.empty or comparator_df is None or comparator_df.empty:
        return pd.DataFrame()

    if "date" not in aear_df.columns or "date" not in comparator_df.columns:
        return pd.DataFrame()

    if comparator_col not in comparator_df.columns:
        return pd.DataFrame()

    aear_df = _prepare_df(aear_df)
    comparator_df = _prepare_df(comparator_df)

    aear_series = _build_aear_series(aear_df)

    if aear_series.empty:
        return pd.DataFrame()

    aear_overlay = pd.DataFrame({
        "date": aear_df["date"],
        "Aggregate Equity Allocation Ratio": aear_series,
    }).dropna()

    aear_overlay["quarter"] = aear_overlay["date"].dt.to_period("Q")
    comparator_df["quarter"] = comparator_df["date"].dt.to_period("Q")

    comparator_q = comparator_df.groupby("quarter", as_index=False)[comparator_col].mean()

    merged = pd.merge(
        aear_overlay,
        comparator_q,
        on="quarter",
        how="inner",
    ).dropna()

    if merged.empty:
        return pd.DataFrame()

    merged = merged[["date", "Aggregate Equity Allocation Ratio", comparator_col]].copy()

    for col in ["Aggregate Equity Allocation Ratio", comparator_col]:
        std = merged[col].std()

        if pd.isna(std) or std == 0:
            return pd.DataFrame()

        merged[col] = (merged[col] - merged[col].mean()) / std

    return merged


def plot_aear_vs_country_equity_proxy_chart(
    df_quarterly: pd.DataFrame,
    df_monthly: pd.DataFrame,
) -> go.Figure:
    overlay = _build_standardised_overlay(
        aear_df=df_quarterly,
        comparator_df=df_monthly,
        comparator_col="EUSA",
    )

    if overlay.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["Aggregate Equity Allocation Ratio"],
        mode="lines",
        name="Aggregate Equity Allocation Ratio",
    ))

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["EUSA"],
        mode="lines",
        name="Country Equity Proxy",
    ))

    fig.update_layout(
        title="AEAR vs Country Equity Proxy",
        xaxis_title="Date",
        yaxis_title="Standardised Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def plot_aear_vs_10y_yield_chart(
    df_quarterly: pd.DataFrame,
    df_monthly: pd.DataFrame,
) -> go.Figure:
    overlay = _build_standardised_overlay(
        aear_df=df_quarterly,
        comparator_df=df_monthly,
        comparator_col="US10YT",
    )

    if overlay.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["Aggregate Equity Allocation Ratio"],
        mode="lines",
        name="Aggregate Equity Allocation Ratio",
    ))

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["US10YT"],
        mode="lines",
        name="Long-Term Sovereign Yield (10Y)",
    ))

    fig.update_layout(
        title="AEAR vs Long-Term Sovereign Yield (10Y)",
        xaxis_title="Date",
        yaxis_title="Standardised Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def plot_aear_vs_central_bank_funds_rate_chart(
    df_quarterly: pd.DataFrame,
    df_monthly: pd.DataFrame,
) -> go.Figure:
    overlay = _build_standardised_overlay(
        aear_df=df_quarterly,
        comparator_df=df_monthly,
        comparator_col="Central Bank Funds Rate",
    )

    if overlay.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["Aggregate Equity Allocation Ratio"],
        mode="lines",
        name="Aggregate Equity Allocation Ratio",
    ))

    fig.add_trace(go.Scatter(
        x=overlay["date"],
        y=overlay["Central Bank Funds Rate"],
        mode="lines",
        name="Central Bank Funds Rate",
    ))

    fig.update_layout(
        title="AEAR vs Central Bank Funds Rate",
        xaxis_title="Date",
        yaxis_title="Standardised Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig


def build_aear_statistical_series_map(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {}

    required_equity_cols = [
        "Domestic Financial Sector Equities",
        "Nonfinancial Corporate Equities",
    ]

    required_liability_cols = [
        "Central Government Debt Liabilities",
        "State Local Government Debt Liabilities",
        "Nonfinancial Corporate Debt Liabilities",
        "Household Nonprofit Debt Liabilities",
        "Rest Of World Debt Liabilities",
    ]

    available_series_map = {}

    if all(col in df.columns for col in required_equity_cols):
        available_series_map["Total Equity Market Value"] = (
            df["Domestic Financial Sector Equities"].fillna(0)
            + df["Nonfinancial Corporate Equities"].fillna(0)
        )

    if all(col in df.columns for col in required_liability_cols):
        available_series_map["Total Real Economy Liabilities"] = (
            df["Central Government Debt Liabilities"].fillna(0)
            + df["State Local Government Debt Liabilities"].fillna(0)
            + df["Nonfinancial Corporate Debt Liabilities"].fillna(0)
            + df["Household Nonprofit Debt Liabilities"].fillna(0)
            + df["Rest Of World Debt Liabilities"].fillna(0)
        )

    if (
        "Total Equity Market Value" in available_series_map
        and "Total Real Economy Liabilities" in available_series_map
    ):
        available_series_map["Aggregate Equity Allocation Ratio"] = (
            available_series_map["Total Equity Market Value"]
            / (
                available_series_map["Total Equity Market Value"]
                + available_series_map["Total Real Economy Liabilities"]
            ).replace(0, pd.NA)
        )

    return available_series_map


# -------------------------------------------------------------------------------------------------
# Chart Dispatcher
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tabs_dict, tab_mapping, df_map):
    label_lookup = {
        "3": "Last 3 Periods",
        "6": "Last 6 Periods",
        "12": "Last 12 Periods",
        "24": "Last 24 Periods",
        "60": "Last 60 Periods",
        "full": "Full History",
    }

    if selected_use_case == "Aggregate Equity Allocation":
        for tab_key, tab in tabs_dict.items():
            period_label = label_lookup.get(tab_key, tab_key)

            with tab:
                df_quarterly = _get_visual_df(
                    df_map,
                    "df_aggregate_equity_allocation",
                    period_label,
                )

                df_quarterly_full = _get_visual_df(
                    df_map,
                    "df_aggregate_equity_allocation",
                    "Full History",
                )

                df_monthly_full = _get_visual_df(
                    df_map,
                    "df_market_context",
                    "Full History",
                )

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Equity Market Value",
                    "Liability Structure",
                    "Aggregate Equity Allocation Ratio",
                    "Statistical Profile",
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_equity_market_value_chart(df_quarterly),
                        label=f"{period_label}_EquityMarketValue",
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_liability_structure_chart(df_quarterly),
                        label=f"{period_label}_LiabilityStructure",
                    )

                with subtab3:
                    inner1, inner2, inner3, inner4 = st.tabs([
                        "AEAR",
                        "AEAR vs Country Equity Proxy",
                        "AEAR vs Long-Term Sovereign Yield (10Y)",
                        "AEAR vs Central Bank Funds Rate",
                    ])

                    with inner1:
                        display_chart_with_fallback(
                            plot_aggregate_equity_allocation_ratio_chart(df_quarterly),
                            label=f"{period_label}_AEAR",
                        )

                    with inner2:
                        st.caption(
                            "📌 Standardised comparison of full-history AEAR and quarterly-aligned Country Equity Proxy."
                        )
                        display_chart_with_fallback(
                            plot_aear_vs_country_equity_proxy_chart(
                                df_quarterly_full,
                                df_monthly_full,
                            ),
                            label=f"{period_label}_AEARvsCountryEquityProxy",
                        )

                    with inner3:
                        st.caption(
                            "📌 Standardised comparison of full-history AEAR and quarterly-aligned Long-Term Sovereign Yield (10Y)."
                        )
                        display_chart_with_fallback(
                            plot_aear_vs_10y_yield_chart(
                                df_quarterly_full,
                                df_monthly_full,
                            ),
                            label=f"{period_label}_AEARvs10YYield",
                        )

                    with inner4:
                        st.caption(
                            "📌 Standardised comparison of full-history AEAR and quarterly-aligned Central Bank Funds Rate."
                        )
                        display_chart_with_fallback(
                            plot_aear_vs_central_bank_funds_rate_chart(
                                df_quarterly_full,
                                df_monthly_full,
                            ),
                            label=f"{period_label}_AEARvsCentralBankFundsRate",
                        )

                with subtab4:
                    available_series_map = build_aear_statistical_series_map(df_quarterly)
                    available_series = list(available_series_map.keys())

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no structural series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_1100_{period_label}",
                            options=available_series,
                            default_index=0,
                        )

                        stats_df = calculate_statistical_profile(
                            available_series_map[selected_series]
                        )

                        st.caption("Statistical profile reflects the currently selected period window.")
                        st.markdown(f"**Statistical Profile: {selected_series}**")
                        st.table(stats_df.set_index("Metric"))

        return

        for tab, data_slice in tab_mapping.items():
            with tab:
                df = data_slice.reset_index()

                if selected_use_case == "Signal A":
                    subtab1, = st.tabs(["Signal A Chart"])
                    with subtab1:
                        display_chart_with_fallback(
                            plot_signal_a_chart(df),
                            label=f"{period_label}_SignalA",
                        )

                elif selected_use_case == "Signal B":
                    subtab1, = st.tabs(["Signal B Chart"])
                    with subtab1:
                        display_chart_with_fallback(
                            plot_signal_b_chart(df),
                            label=f"{period_label}_SignalB",
                        )

                elif selected_use_case == "Signal C":
                    subtab1, = st.tabs(["Signal C Chart"])
                    with subtab1:
                        display_chart_with_fallback(
                            plot_signal_c_chart(df),
                            label=f"{period_label}_SignalC",
                        )

                else:
                    st.info("ℹ️ No charts available for the selected use case.")
