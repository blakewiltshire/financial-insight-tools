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
# Local Visual Configuration — Monetary Indicators and Policy Effects
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument, unused-import

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
from universal_visual_config_500 import (
    display_chart_with_fallback,
    plot_money_supply_chart,
    plot_money_velocity_chart,
    plot_policy_rate_chart,
    plot_funding_conditions_chart,
    plot_lending_and_mortgage_chart,
    plot_curve_structure_chart,
    plot_real_policy_proxy_chart
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
        "Money Supply and Velocity Dynamics": "Money Supply and Velocity Dynamics",
        "Interest Rate Regime and Transmission": "Interest Rate Regime and Transmission",
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

    if selected_use_case == "Money Supply and Velocity Dynamics":
        for tab_index, (tab, period_label) in enumerate(tab_mapping.items()):
            with tab:
                df_monthly = _get_visual_df(df_map, "money_supply_monthly", period_label)
                df_quarterly = _get_visual_df(df_map, "money_velocity_quarterly", period_label)

                subtab1, subtab2, subtab3 = st.tabs([
                    "Money Supply",
                    "Velocity",
                    "Statistical Profile"
                ])

                with subtab1:
                    if df_monthly is None or df_monthly.empty:
                        st.warning("⚠️ Money supply chart not available — no monthly data loaded.")
                    else:
                        display_chart_with_fallback(
                            plot_money_supply_chart(df_monthly),
                            label="MoneySupply"
                        )

                with subtab2:
                    if df_quarterly is None or df_quarterly.empty:
                        st.warning("⚠️ Velocity chart not available — no quarterly data loaded.")
                    else:
                        display_chart_with_fallback(
                            plot_money_velocity_chart(df_quarterly),
                            label="MoneyVelocity"
                        )

                with subtab3:
                    series_lookup = {}

                    for col in ["M1 Money Supply", "M2 Money Supply"]:
                        if df_monthly is not None and not df_monthly.empty and col in df_monthly.columns:
                            series_lookup[col] = df_monthly

                    for col in ["M1 Money Velocity", "M2 Money Velocity"]:
                        if df_quarterly is not None and not df_quarterly.empty and col in df_quarterly.columns:
                            series_lookup[col] = df_quarterly

                    if not series_lookup:
                        st.warning("⚠️ Statistical profile not available — no money supply or velocity series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_500_money_tab_{tab_index}",
                            options=list(series_lookup.keys()),
                            default_index=0
                        )

                        selected_df = series_lookup[selected_series]
                        stats_df = calculate_statistical_profile(selected_df[selected_series])

                        col1, col2 = st.columns([2, 5])

                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "Interest Rate Regime and Transmission":
        for tab_index, (tab, period_label) in enumerate(tab_mapping.items()):
            with tab:
                df_policy = _get_visual_df(df_map, "policy_rates_monthly", period_label)
                df_funding = _get_visual_df(df_map, "funding_rates_daily", period_label)
                df_mortgage = _get_visual_df(df_map, "mortgage_rates_weekly", period_label)

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Policy",
                    "Funding",
                    "Lending & Mortgage",
                    "Curve & Proxy"
                ])

                with subtab1:
                    if df_policy is None or df_policy.empty:
                        st.warning("⚠️ PolicyRatePositioning not available — no monthly rate data loaded.")
                    else:
                        display_chart_with_fallback(
                            plot_policy_rate_chart(df_policy),
                            label="PolicyRatePositioning"
                        )

                with subtab2:
                    if df_funding is None or df_funding.empty:
                        st.warning("⚠️ FundingConditions not available — no daily rate data loaded.")
                    else:
                        display_chart_with_fallback(
                            plot_funding_conditions_chart(df_funding),
                            label="FundingConditions"
                        )

                with subtab3:
                    df_funding_full = _get_visual_df(df_map, "funding_rates_daily", "Full History")
                    df_mortgage_full = _get_visual_df(df_map, "mortgage_rates_weekly", "Full History")

                    if (df_funding_full is None or df_funding_full.empty) and (df_mortgage_full is None or df_mortgage_full.empty):
                        st.warning("⚠️ LendingMortgage not available — required data not loaded.")
                    else:
                        st.caption("📌 Lending & Mortgage visuals are shown on a full-history basis to preserve interpretability across mixed frequencies.")

                        display_chart_with_fallback(
                            plot_lending_and_mortgage_chart(df_funding_full, df_mortgage_full),
                            label="LendingMortgage"
                        )

                with subtab4:
                    inner_tab1, inner_tab2 = st.tabs([
                        "Curve Structure",
                        "Real Policy Proxy"
                    ])

                    with inner_tab1:
                        curve_fig = plot_curve_structure_chart(df_funding) if df_funding is not None and not df_funding.empty else None

                        if curve_fig is None or not curve_fig.data:
                            st.warning("⚠️ CurveStructure not available — no daily curve data loaded.")
                        else:
                            display_chart_with_fallback(
                                curve_fig,
                                label="CurveStructure"
                            )

                    with inner_tab2:
                        proxy_fig = plot_real_policy_proxy_chart(df_mortgage) if df_mortgage is not None and not df_mortgage.empty else None

                        if proxy_fig is None or not proxy_fig.data:
                            st.warning("⚠️ RealPolicyProxy not available — no weekly proxy data loaded.")
                        else:
                            display_chart_with_fallback(
                                proxy_fig,
                                label="RealPolicyProxy"
                            )

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
