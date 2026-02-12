# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name
# pylint: disable=unused-argument, unused-import

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📈 Local Visual Configuration — Economic Exploration Suite
-----------------------------------------------------------------

Defines the country- or theme-specific visual rendering extensions for
Economic Exploration modules (Themes 100–2100+). This module extends the
universal charting engine, enabling more granular visualisation layers.

✅ Role in the System:
- Adds localised chart overlays, sector breakdowns, and country-specific displays.
- Controls tab and subtab layouts per Use Case.
- Dynamically routes visual rendering based on the selected Use Case.

🧠 System Design Notes:
- Visual rendering is fully independent of indicator signal evaluation.
- **Use Case selection controls visual rendering**, with charts configured here.
- Chart data slices are passed via `df_map`, based on timeframe windows handled locally.
- Visual keys, tab names, subtab structures, and display logic are fully controlled here.
- This local module **does not reference indicator_map_XXX.py or insights** directly.

⚙️ Architecture Summary:
- Each Use Case receives its own visualisation block inside `render_all_charts_local()`.
- Subtabs are always required (even for single-chart cases) to ensure consistent UI structure.
- Chart keys are managed via `display_chart_with_fallback()` to prevent Streamlit key conflicts.
- Local visuals may call universal chart functions (e.g., from `universal_visual_config_XXX.py`) for consistency.

Usage:
- Invoked automatically from the main theme module (`100_📈_economic_growth_stability.py`, `200_💼_labour_market_dynamics.py`, etc.)
- Required only when country- or theme-specific visuals are implemented.
- If no local visual config exists, universal visuals render by default.

🧠 AI Implementation Notes:
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
    plot_gdp_component_growth_comparison
)

# -------------------------------------------------------------------------------------------------
# 📌 Visual Section Titles Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    """
    Returns a mapping of use case labels to visual section headers.
    Includes universal and local mappings (if applicable).
    """
    return {
        "Real GDP": "📉 Real GDP Trends & Visuals",
        "Nominal GDP": "📉 Nominal GDP Trends & Visuals",
        "GDP Components Breakdown": "📊 GDP Component Breakdown & Structure",
        "Macro Composite Signals": "🧠 Composite Indicators & Regime Signals"
    }

# -------------------------------------------------------------------------------------------------
# 🧭 Local Chart Configs (If applicable)
# -------------------------------------------------------------------------------------------------
def plot_cb_leading_index(df):
    """Line chart for the Conference Board Leading Index."""
    return plot_indicator_line_chart(
        df,
        y_column="US Leading Index (Conference Board)",
        title="📈 Conference Board Leading Index",
        yaxis_title="Index",
        marker=True
    )

def plot_wei_with_average(df):
    """Line chart with 4-week average for Weekly Economic Index (NY Fed)."""
    df = df.copy()
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
        line={"dash": 'dot'}
    ))

    fig.update_layout(
        title="📉 Weekly Economic Index (NY Fed)",
        xaxis_title="Date",
        yaxis_title="Index Level",
        height=480,
        template="plotly_white"
    )
    return fig

def plot_policy_uncertainty(df):
    """Line chart for the Economic Policy Uncertainty Index."""
    return plot_indicator_line_chart(
        df,
        y_column="Economic Policy Uncertainty Index",
        title="🌀 Economic Policy Uncertainty Index",
        yaxis_title="Index Level",
        marker=True
    )

def plot_cfnai_index(df):
    """Line chart for the Chicago Fed National Activity Index with baseline line."""
    fig = plot_indicator_line_chart(
        df,
        y_column="Chicago Fed National Activity Index",
        title="📊 National Activity Index (Chicago Fed)",
        yaxis_title="Index Level",
        marker=True
    )
    if fig:
        fig.add_hline(y=0, line_dash="dot", line_color="gray")
    return fig

# -------------------------------------------------------------------------------------------------
# 🚦 Chart Dispatcher — Universal Charts First, Local Extensions After
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for Economic Growth & Stability — with fallback
    messaging and AI compatibility.
    """
    for tab, data_slice in tab_mapping.items():
        with tab:
            df = data_slice.reset_index()

            if selected_use_case == "Real GDP":
                subtab1, subtab2 = st.tabs(["📈 Comparative Growth", "📊 GDP Levels"])
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

            elif selected_use_case == "Nominal GDP":
                subtab1, subtab2 = st.tabs(["📈 Nominal Growth", "📊 Nominal Level"])
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

            elif selected_use_case == "GDP Components Breakdown":
                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "📈 Domestic Drivers",
                    "🌐 Exports vs Imports",
                    "📐 Structural Share (%)",
                    "📊 Comparative Growth"
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

# -------------------------------------------------------------------------------------------------
# Optional Local Chart Dispatcher — Extend for Country-Specific Visuals
# -------------------------------------------------------------------------------------------------
    if selected_use_case == "Macro Composite Signals":
        period_options = [4, 8, 12, 20, 40, None]
        composite_tabs = list(tab_mapping.keys())[:6]

        for tab, periods in zip(composite_tabs, period_options):
            with tab:
                df_monthly = df_map["df_secondary"]
                df_monthly = df_monthly if periods is None else df_monthly.tail(periods)
                df_weekly = df_map["df_extended"]
                df_weekly = df_weekly if periods is None else df_weekly.tail(periods)

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "📈 Leading Index (CB)",
                    "📉 Weekly Economic Index",
                    "🌀 Policy Uncertainty",
                    "⚙️ National Activity Index"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_cb_leading_index(df_monthly.reset_index()),
                        label="Conference Board Leading Index"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_wei_with_average(df_weekly.reset_index()),
                        label="Weekly Economic Index"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_policy_uncertainty(df_monthly.reset_index()),
                        label="Economic Policy Uncertainty Index"
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_cfnai_index(df_monthly.reset_index()),
                        label="Chicago Fed National Activity Index"
                    )
