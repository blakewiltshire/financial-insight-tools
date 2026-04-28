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
from universal_visual_config_600 import (
    display_chart_with_fallback,
    plot_housing_pipeline_chart,
    plot_mortgage_financing_chart,
    plot_yield_curve_structure_chart,
    plot_sovereign_debt_sustainability_chart,
    plot_sovereign_liquidity_refinancing_chart,
    plot_balance_sheet_expansion_constraint_chart,
    plot_credit_conditions_financing_pressure_chart,
    plot_bank_balance_sheet_liquidity_chart
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
        "Housing Construction Cycle": "Housing Construction Pipeline",
        "Mortgage Financing Conditions": "Mortgage Financing Conditions",
        "Yield Curve Structure": "Yield Curve Structure",
        "Sovereign Debt Sustainability": "Sovereign Debt Sustainability",
        "Sovereign Liquidity and Refinancing Pressure": "Sovereign Liquidity and Refinancing Pressure",
        "Balance Sheet Expansion and System Constraint": "Balance Sheet Expansion and System Constraint",
        "Credit Conditions and Financing Pressure": "Credit Conditions and Financing Pressure",
        "Bank Balance Sheet Liquidity and Credit Capacity": "Bank Balance Sheet Liquidity and Credit Capacity",
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


def _slice_df_by_period_count(df: pd.DataFrame, period_count) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    df = _prepare_df(df)

    if period_count is None:
        return df.copy()

    return df.tail(period_count).copy()


def _get_visual_df(df_map: dict, dataset_key: str, period_count) -> pd.DataFrame:
    df = df_map.get(dataset_key)
    return _slice_df_by_period_count(df, period_count)


def _get_full_visual_df(df_map: dict, dataset_key: str) -> pd.DataFrame:
    df = df_map.get(dataset_key)
    return _prepare_df(df)


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


def _render_stats_tab(df: pd.DataFrame, available_series: list[str], widget_key: str, full_history: bool = False):
    if df is None or df.empty:
        st.warning("⚠️ Statistical profile not available — no data loaded.")
        return

    available_series = [col for col in available_series if col in df.columns]

    if not available_series:
        st.warning("⚠️ Statistical profile not available — no compatible series loaded.")
        return

    selected_series = _get_stable_series_selection(
        widget_key=widget_key,
        options=available_series,
        default_index=0
    )

    stats_df = calculate_statistical_profile(df[selected_series])

    col1, col2 = st.columns([2, 5])

    with col1:
        if full_history:
            st.caption("Statistical profile reflects full-history structural data.")
        else:
            st.caption("Statistical profile reflects the currently selected period window.")
        st.markdown(f"**Statistical Profile: {selected_series}**")
        st.table(stats_df.set_index("Metric"))


# -------------------------------------------------------------------------------------------------
# Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    period_options = [3, 6, 12, 24, 60, None]

    for tab_index, ((tab, primary_data_slice), period_count) in enumerate(zip(tab_mapping.items(), period_options)):
        with tab:

            if selected_use_case == "Housing Construction Cycle":
                df = _prepare_df(primary_data_slice)

                subtab1, subtab2 = st.tabs([
                    "Housing Construction Pipeline",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_housing_pipeline_chart(df),
                        label="HousingPipeline"
                    )

                with subtab2:
                    _render_stats_tab(
                        df=df,
                        available_series=[
                            "Housing Units Authorized",
                            "Housing Units Started",
                            "Housing Units Completed",
                        ],
                        widget_key=f"stats_profile_600_housing_{tab_index}"
                    )

            elif selected_use_case == "Mortgage Financing Conditions":
                df = _get_visual_df(df_map, "df_secondary", period_count)

                subtab1, subtab2 = st.tabs([
                    "Mortgage Financing Conditions",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_mortgage_financing_chart(df),
                        label="MortgageFinancing"
                    )

                with subtab2:
                    _render_stats_tab(
                        df=df,
                        available_series=["Long-Term Mortgage Rate"],
                        widget_key=f"stats_profile_600_mortgage_{tab_index}"
                    )

            elif selected_use_case == "Yield Curve Structure":
                df = _get_visual_df(df_map, "df_extended", period_count)

                subtab1, subtab2 = st.tabs([
                    "Yield Curve Structure",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_yield_curve_structure_chart(df),
                        label="YieldCurveStructure"
                    )

                with subtab2:
                    _render_stats_tab(
                        df=df,
                        available_series=["Yield Curve Spread"],
                        widget_key=f"stats_profile_600_curve_{tab_index}"
                    )

            elif selected_use_case == "Sovereign Debt Sustainability":
                df_quarterly = _get_full_visual_df(df_map, "df_quarterly_sovereign")
                df_annual = _get_full_visual_df(df_map, "df_annual_sovereign")

                subtab1, subtab2 = st.tabs([
                    "Sovereign Debt Sustainability",
                    "Statistical Profile"
                ])

                with subtab1:
                    st.caption("📌 Structural sovereign visuals are shown on a full-history basis to preserve interpretability across mixed frequencies.")
                    display_chart_with_fallback(
                        plot_sovereign_debt_sustainability_chart(df_quarterly, df_annual),
                        label="SovereignDebtSustainability"
                    )

                with subtab2:
                    stats_df = df_quarterly if df_quarterly is not None and not df_quarterly.empty else df_annual
                    _render_stats_tab(
                        df=stats_df,
                        available_series=[
                            "Sovereign Debt Percentage of GDP",
                            "Sovereign Debt",
                            "Real GDP (Level)",
                            "Government Fiscal Balance",
                            "Government Interest Outlays",
                            "Government Net Outlays",
                            "Government Receipts",
                        ],
                        widget_key=f"stats_profile_600_sovereign_debt_{tab_index}",
                        full_history=True
                    )

            elif selected_use_case == "Sovereign Liquidity and Refinancing Pressure":
                df_weekly = _get_full_visual_df(df_map, "df_weekly_sovereign")
                df_annual = _get_full_visual_df(df_map, "df_annual_sovereign")

                subtab1, subtab2 = st.tabs([
                    "Sovereign Liquidity and Refinancing Pressure",
                    "Statistical Profile"
                ])

                with subtab1:
                    st.caption("📌 Structural sovereign visuals are shown on a full-history basis to preserve interpretability across mixed frequencies.")
                    display_chart_with_fallback(
                        plot_sovereign_liquidity_refinancing_chart(df_weekly, df_annual),
                        label="SovereignLiquidityRefinancing"
                    )

                with subtab2:
                    stats_df = df_weekly if df_weekly is not None and not df_weekly.empty else df_annual
                    _render_stats_tab(
                        df=stats_df,
                        available_series=[
                            "10-Year Sovereign Yield",
                            "Central Bank Total Assets",
                            "Government Interest Outlays",
                            "Government Receipts",
                        ],
                        widget_key=f"stats_profile_600_sovereign_liquidity_{tab_index}",
                        full_history=True
                    )

            elif selected_use_case == "Balance Sheet Expansion and System Constraint":
                df_weekly = _get_full_visual_df(df_map, "df_weekly_sovereign")
                df_quarterly = _get_full_visual_df(df_map, "df_quarterly_sovereign")

                subtab1, subtab2 = st.tabs([
                    "Balance Sheet Expansion and System Constraint",
                    "Statistical Profile"
                ])

                with subtab1:
                    st.caption("📌 Structural sovereign visuals are shown on a full-history basis to preserve interpretability across mixed frequencies.")
                    display_chart_with_fallback(
                        plot_balance_sheet_expansion_constraint_chart(df_weekly, df_quarterly),
                        label="BalanceSheetExpansionConstraint"
                    )

                with subtab2:
                    stats_df = df_weekly if df_weekly is not None and not df_weekly.empty else df_quarterly
                    _render_stats_tab(
                        df=stats_df,
                        available_series=[
                            "10-Year Sovereign Yield",
                            "Central Bank Total Assets",
                            "Sovereign Debt Percentage of GDP",
                            "Sovereign Debt",
                            "Real GDP (Level)",
                        ],
                        widget_key=f"stats_profile_600_balance_sheet_{tab_index}",
                        full_history=True
                    )

            elif selected_use_case == "Credit Conditions and Financing Pressure":
                df = _get_visual_df(df_map, "df_daily_credit", period_count)

                subtab1, subtab2 = st.tabs([
                    "Credit Conditions and Financing Pressure",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_credit_conditions_financing_pressure_chart(df),
                        label="CreditConditionsFinancingPressure"
                    )

                with subtab2:
                    _render_stats_tab(
                        df=df,
                        available_series=[
                            "Corporate Credit Spread",
                            "High Yield Credit Spread",
                            "CCC and Lower Credit Spread",
                        ],
                        widget_key=f"stats_profile_600_credit_{tab_index}"
                    )

            elif selected_use_case == "Bank Balance Sheet Liquidity and Credit Capacity":
                df = _get_visual_df(df_map, "df_weekly_credit", period_count)

                subtab1, subtab2 = st.tabs([
                    "Bank Balance Sheet Liquidity and Credit Capacity",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_bank_balance_sheet_liquidity_chart(df),
                        label="BankBalanceSheetLiquidity"
                    )

                with subtab2:
                    _render_stats_tab(
                        df=df,
                        available_series=[
                            "Bank Cash Assets",
                            "Treasury and Agency Securities Holdings",
                            "Bank Total Assets",
                        ],
                        widget_key=f"stats_profile_600_bank_{tab_index}"
                    )

            else:
                st.info("ℹ️ No charts available for the selected use case.")
