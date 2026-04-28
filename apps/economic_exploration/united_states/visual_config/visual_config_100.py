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

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Add universal visual_config path
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Chart Imports
# -------------------------------------------------------------------------------------------------
from universal_visual_config_100 import (
    display_chart_with_fallback,
    plot_indicator_line_chart,
    plot_gdp_growth_comparison,
    plot_gdp_real_level_with_extremes,
    plot_gdp_nominal_level,
    plot_gdp_nominal_yoy_growth,
    plot_gdp_domestic_components_lines,
    plot_gdp_external_sector_trade_lines,
    plot_gdp_component_structure_area_share,
    plot_gdp_component_growth_comparison,
)

# -------------------------------------------------------------------------------------------------
# Shared Statistical Profile Import
# -------------------------------------------------------------------------------------------------
from universal_visual_shared import calculate_statistical_profile

# -------------------------------------------------------------------------------------------------
# Visual Section Titles Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    """
    Returns a mapping of use case labels to visual section headers.
    Includes universal and local mappings where applicable.
    """
    return {
        "Real GDP": "Real GDP Trends & Visuals",
        "Nominal GDP": "Nominal GDP Trends & Visuals",
        "GDP Components Breakdown": "GDP Component Breakdown & Structure",
        "Macro Composite Signals": "Composite Indicators & Regime Signals",
    }


# -------------------------------------------------------------------------------------------------
# Local Chart Configs
# -------------------------------------------------------------------------------------------------
def plot_cb_leading_index(df: pd.DataFrame) -> go.Figure:
    """Line chart for the Conference Board Leading Index."""
    return plot_indicator_line_chart(
        df,
        y_column="Leading Economic Index (Conference Board)",
        title="Leading Economic Index (Conference Board)",
        yaxis_title="Index",
        marker=True
    )


def plot_wei_with_average(df: pd.DataFrame) -> go.Figure:
    """Line chart with 4-week average for Weekly Economic Index (NY Fed)."""
    df = df.copy()

    required_cols = ["date", "Weekly Economic Index (Lewis-Mertens-Stock)"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    if df["Weekly Economic Index (Lewis-Mertens-Stock)"].dropna().empty:
        return go.Figure()

    df["4W Avg"] = df["Weekly Economic Index (Lewis-Mertens-Stock)"].rolling(4).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Weekly Economic Index (Lewis-Mertens-Stock)"],
        name="Weekly",
        mode="lines+markers"
    ))
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["4W Avg"],
        name="4-Week Avg",
        mode="lines",
        line={"dash": "dot"}
    ))

    fig.update_layout(
        title="Weekly Economic Index (NY Fed)",
        xaxis_title="Date",
        yaxis_title="Index Level",
        height=480,
        template="plotly_white"
    )
    return fig


def plot_policy_uncertainty(df: pd.DataFrame) -> go.Figure:
    """Line chart for the Economic Policy Uncertainty Index."""
    return plot_indicator_line_chart(
        df,
        y_column="Economic Policy Uncertainty Index",
        title="Economic Policy Uncertainty Index",
        yaxis_title="Index Level",
        marker=True
    )


def plot_cfnai_index(df: pd.DataFrame) -> go.Figure:
    """Line chart for the Chicago Fed National Activity Index with baseline line."""
    fig = plot_indicator_line_chart(
        df,
        y_column="Chicago Fed National Activity Index",
        title="National Activity Index (Chicago Fed)",
        yaxis_title="Index Level",
        marker=True
    )

    if fig:
        fig.add_hline(y=0, line_dash="dot", line_color="gray")

    return fig


# -------------------------------------------------------------------------------------------------
# Local Helpers
# -------------------------------------------------------------------------------------------------
def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resets index where needed, normalises the date column, and sorts values.
    """
    if df is None or df.empty:
        return df

    df = df.copy()

    if hasattr(df, "reset_index"):
        df = df.reset_index()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).sort_values("date")

    return df


def _get_visual_df(tab_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the already-sliced dataframe provided by tab_mapping.
    """
    return _prepare_df(tab_df)


def _get_stable_series_selection(widget_key: str, options: list[str], default_index: int = 0) -> str:
    """
    Preserves statistical profile series selection across Streamlit reruns.
    """
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
# Chart Dispatcher — Universal Charts First, Local Extensions After
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for Economic Growth & Stability.
    Uses the page's existing tab_mapping pattern: tab -> sliced dataframe.
    """

    if selected_use_case == "Real GDP":
        for tab_index, (tab, tab_df) in enumerate(tab_mapping.items()):
            with tab:
                df = _get_visual_df(tab_df)

                subtab1, subtab2, subtab3 = st.tabs([
                    "Comparative Growth",
                    "GDP Levels",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_gdp_growth_comparison(df),
                        label="Real GDP Growth Comparison",
                        partial_warning=True
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_gdp_real_level_with_extremes(
                            df,
                            value_column="Real GDP (Level)",
                            title="Real GDP Level",
                            yaxis_title="Billions (Chained)"
                        ),
                        label="Real GDP Level"
                    )

                with subtab3:
                    available_series = [
                        col for col in [
                            "Real GDP (Level)",
                            "Real GDP QoQ % Change",
                            "Real GDP YoY % Change",
                            "Real GDP QoQ Annualized"
                        ]
                        if df is not None and not df.empty and col in df.columns
                    ]

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no real GDP series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_100_real_gdp_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(df[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "Nominal GDP":
        for tab_index, (tab, tab_df) in enumerate(tab_mapping.items()):
            with tab:
                df = _get_visual_df(tab_df)

                subtab1, subtab2, subtab3 = st.tabs([
                    "Nominal Growth",
                    "Nominal Level",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_gdp_nominal_yoy_growth(df),
                        label="Nominal GDP YoY Growth"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_gdp_nominal_level(df),
                        label="Nominal GDP Level"
                    )

                with subtab3:
                    temp_df = df.copy() if df is not None else pd.DataFrame()

                    if (
                        temp_df is not None
                        and not temp_df.empty
                        and "Nominal GDP" in temp_df.columns
                        and "YoY Nominal % Change" not in temp_df.columns
                    ):
                        temp_df["YoY Nominal % Change"] = temp_df["Nominal GDP"].pct_change(periods=4) * 100

                    available_series = [
                        col for col in [
                            "Nominal GDP",
                            "YoY Nominal % Change"
                        ]
                        if temp_df is not None and not temp_df.empty and col in temp_df.columns
                    ]

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no nominal GDP series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_100_nominal_gdp_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(temp_df[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "GDP Components Breakdown":
        for tab_index, (tab, tab_df) in enumerate(tab_mapping.items()):
            with tab:
                df = _get_visual_df(tab_df)

                subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
                    "Domestic Drivers",
                    "Exports vs Imports",
                    "Structural Share (%)",
                    "Comparative Growth",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_gdp_domestic_components_lines(df),
                        label="Domestic GDP Components",
                        partial_warning=True
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_gdp_external_sector_trade_lines(df),
                        label="Exports vs Imports",
                        partial_warning=True
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_gdp_component_structure_area_share(df),
                        label="Component Share Breakdown",
                        partial_warning=True
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_gdp_component_growth_comparison(df),
                        label="GDP Component Growth Comparison",
                        partial_warning=True
                    )

                with subtab5:
                    available_series = [
                        col for col in [
                            "Real Personal Consumption Expenditures",
                            "Real Gross Private Domestic Investment",
                            "Government Consumption Expenditures and Gross Investment",
                            "Real Exports of Goods and Services",
                            "Real Imports of Goods and Services"
                        ]
                        if df is not None and not df.empty and col in df.columns
                    ]

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no GDP component series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_100_gdp_components_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(df[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "Macro Composite Signals":
        period_options = [4, 8, 12, 20, 40, None]
        composite_tabs = list(tab_mapping.keys())[:6]

        for tab_index, (tab, periods) in enumerate(zip(composite_tabs, period_options)):
            with tab:
                df_monthly = df_map["df_secondary"]
                df_monthly = df_monthly if periods is None else df_monthly.tail(periods)
                df_monthly = _prepare_df(df_monthly)

                df_weekly = df_map["df_extended"]
                df_weekly = df_weekly if periods is None else df_weekly.tail(periods)
                df_weekly = _prepare_df(df_weekly)

                subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
                    "Leading Economic Index (Conference Board)",
                    "Weekly Economic Index",
                    "Policy Uncertainty",
                    "National Activity Index",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_cb_leading_index(df_monthly),
                        label="Leading Economic Index (Conference Board)"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_wei_with_average(df_weekly),
                        label="Weekly Economic Index"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_policy_uncertainty(df_monthly),
                        label="Economic Policy Uncertainty Index"
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_cfnai_index(df_monthly),
                        label="Chicago Fed National Activity Index"
                    )

                with subtab5:
                    available_series_map = {}

                    if df_monthly is not None and not df_monthly.empty:
                        for col in [
                            "Leading Economic Index (Conference Board)",
                            "Economic Policy Uncertainty Index",
                            "Chicago Fed National Activity Index"
                        ]:
                            if col in df_monthly.columns:
                                available_series_map[col] = df_monthly[col]

                    if df_weekly is not None and not df_weekly.empty:
                        if "Weekly Economic Index (Lewis-Mertens-Stock)" in df_weekly.columns:
                            available_series_map["Weekly Economic Index (Lewis-Mertens-Stock)"] = (
                                df_weekly["Weekly Economic Index (Lewis-Mertens-Stock)"]
                            )

                    available_series = list(available_series_map.keys())

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no macro composite series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_100_macro_composite_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(available_series_map[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
