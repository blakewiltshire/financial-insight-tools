# -------------------------------------------------------------------------------------------------
# 📈 Economic Growth Stability — Visual Config (Local Extension)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument, unused-import

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
# 📦 Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st

# -------------------------------------------------------------------------------------------------
# 🧭 Add Universal Visual Path
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 📊 Universal Chart Functions
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
# 🧾 Visual Section Title Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles() -> dict:
    """
    Returns display headers for each use case within this theme.

    Supports both universal and optional local labelling.
    """
    return {
        "Real GDP": "📉 Real GDP Trends & Visuals",
        "Nominal GDP": "📉 Nominal GDP Trends & Visuals",
        "GDP Components Breakdown": "📊 GDP Component Breakdown & Structure",
        "US Macro Composite Signals": "🧠 Composite Indicators & Regime Signals"
    }


# -------------------------------------------------------------------------------------------------
# 🧭 Local Chart Configs (If applicable)
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# 📈 Chart Dispatcher — Universal Charts First, Local Additions Follow
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case: str, tab_mapping: dict, df_map: dict):
    """
    Dispatches use-case-specific visuals for Economic Growth & Stability theme.

    Args:
        selected_use_case (str): Active use case selected by user.
        tab_mapping (dict): Mapping of timeframe tabs to time-sliced DataFrames.
        df_map (dict): Dataset mapping used for visualisation (e.g., df_generic).
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

            # 🔧 Optional extension block (add local visuals if needed)
            # elif selected_use_case == "Local Macro Indicator":
            #     display_chart_with_fallback(
            #         plot_indicator_line_chart(...),
            #         label="Local Chart Title"
            #     )
