# -------------------------------------------------------------------------------------------------
# Visual Config (Local Extension) — Theme 200 Labour Market Dynamics (Platinum+)
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
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Chart Imports
# -------------------------------------------------------------------------------------------------
from universal_visual_config_700 import (
    display_chart_with_fallback,
    plot_trade_flows_chart,
    plot_trade_balance_chart,
    plot_reserve_layer_chart,
    plot_current_account_anchor_chart,
    plot_net_international_position_chart,
    plot_investment_income_pressure_chart
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
        "Country External Balance": "Country External Balance",
        "External Constraint Capital Flow": "External Constraint Capital Flow",
    }


# -------------------------------------------------------------------------------------------------
# Local Helpers
# -------------------------------------------------------------------------------------------------
def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = df.copy()

    if hasattr(df, "reset_index"):
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


def _get_stable_series_selection(widget_key: str, options: list[str], default_index: int = 0) -> str:
    if not options:
        return None

    if widget_key not in st.session_state or st.session_state[widget_key] not in options:
        st.session_state[widget_key] = options[default_index]

    selected = st.selectbox(
        "Select series for statistical profile",
        options=options,
        index=options.index(st.session_state[widget_key]),
        key=f"{widget_key}__selectbox"
    )

    st.session_state[widget_key] = selected
    return selected


# -------------------------------------------------------------------------------------------------
# Chart Dispatcher
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    if selected_use_case == "Country External Balance":
        for tab_index, (tab, period_label) in enumerate(tab_mapping.items()):
            with tab:
                df_monthly = _get_visual_df(df_map, "trade_flows_monthly", period_label)
                df_quarterly = _get_visual_df(df_map, "capital_flow_quarterly", period_label)

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Trade Flows",
                    "Trade Balance",
                    "Reserve Layer",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_trade_flows_chart(df_monthly),
                        label="TradeFlows"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_trade_balance_chart(df_monthly),
                        label="TradeBalance"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_reserve_layer_chart(df_monthly),
                        label="ReserveLayer"
                    )

                with subtab4:
                    available_series = [
                        col for col in [
                            "Exports of Goods and Services",
                            "Imports of Goods and Services",
                            "Trade Balance Goods and Services",
                            "Trade Balance Goods",
                            "Trade Balance Services",
                            "Official Reserves Excluding Gold"
                        ] if df_monthly is not None and not df_monthly.empty and col in df_monthly.columns
                    ]

                    if (
                        df_quarterly is not None
                        and not df_quarterly.empty
                        and "Current Account Balance" in df_quarterly.columns
                    ):
                        available_series.append("Current Account Balance")

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no external balance series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_700_country_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        if selected_series in df_monthly.columns:
                            stats_df = calculate_statistical_profile(df_monthly[selected_series])
                        else:
                            stats_df = calculate_statistical_profile(df_quarterly[selected_series])

                        col1, col2 = st.columns([2, 5])

                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "External Constraint Capital Flow":
        for tab_index, (tab, period_label) in enumerate(tab_mapping.items()):
            with tab:
                df_monthly = _get_visual_df(df_map, "trade_flows_monthly", period_label)
                df_quarterly = _get_visual_df(df_map, "capital_flow_quarterly", period_label)

                subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
                    "Current Account Anchor",
                    "Net International Position",
                    "Investment Income Pressure",
                    "Reserve Support",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_current_account_anchor_chart(df_quarterly),
                        label="CurrentAccountAnchor"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_net_international_position_chart(df_quarterly),
                        label="NetInternationalPosition"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_investment_income_pressure_chart(df_quarterly),
                        label="InvestmentIncomePressure"
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_reserve_layer_chart(df_monthly),
                        label="ReserveSupport"
                    )

                with subtab5:
                    available_series = []

                    if df_quarterly is not None and not df_quarterly.empty:
                        available_series.extend([
                            col for col in [
                                "Current Account Balance",
                                "Net International Investment Position Quarterly",
                                "Primary Investment Income payments",
                            ] if col in df_quarterly.columns
                        ])

                    if (
                        df_monthly is not None
                        and not df_monthly.empty
                        and "Official Reserves Excluding Gold" in df_monthly.columns
                    ):
                        available_series.append("Official Reserves Excluding Gold")

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no external constraint series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_700_constraint_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        if df_quarterly is not None and selected_series in df_quarterly.columns:
                            stats_df = calculate_statistical_profile(df_quarterly[selected_series])
                        else:
                            stats_df = calculate_statistical_profile(df_monthly[selected_series])

                        col1, col2 = st.columns([2, 5])

                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
