# -------------------------------------------------------------------------------------------------
# 📈 Generic Template — Visual Config (Local Extension)
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
# 🧱 Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st

# -------------------------------------------------------------------------------------------------
# 🛠 Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Chart Imports (Theme 200)
# -------------------------------------------------------------------------------------------------
from universal_visual_config_200 import (
    display_chart_with_fallback,
    plot_labour_line_chart,
    plot_labour_with_extremes
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
        "Employment Trends": "📈 Employment Growth and Hiring Activity",
        "Unemployment Context": "📉 Unemployment Rates and Volatility",
        "Labour Force Engagement": "🧠 Participation and Labour Supply Trends"
    }

# -------------------------------------------------------------------------------------------------
# 🧭 Local Chart Configs (If applicable)
# -------------------------------------------------------------------------------------------------




# -------------------------------------------------------------------------------------------------
# 🚦 Chart Dispatcher — Universal Charts First, Local Extensions After
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for Labour Market Dynamics — with fallback messaging and AI compatibility.
    """
    for tab, data_slice in tab_mapping.items():
        with tab:
            df = data_slice.reset_index()

            # --- Employment Trends ---
            if selected_use_case == "Employment Trends":
                subtab1, subtab2, subtab3 = st.tabs([
                    "📈 Hiring Momentum",
                    "📉 Volatility Context",
                    "🔁 Inflection Points"
                ])
                with subtab1:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Employment ex Agriculture",
                        "Employment Trends", "Employment Level"),
                        label=f"{tab}_Hiring Momentum"
                    )
                with subtab2:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Employment ex Agriculture",
                        "Hiring Volatility", "Employment Level"),
                        label=f"{tab}_Hiring Volatility"
                    )
                with subtab3:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Employment ex Agriculture",
                        "Turning Points in Employment", "Employment Level"),
                        label=f"{tab}_Employment Inflection"
                    )

            # --- Unemployment Context ---
            elif selected_use_case == "Unemployment Context":
                subtab1, subtab2, subtab3 = st.tabs([
                    "📈 Unemployment Direction",
                    "📈 Extremes & Reversion",
                    "🌪️ Volatility"
                ])
                with subtab1:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Unemployment Rate", "Unemployment Direction",
                        "Unemployment Rate (%)"),
                        label=f"{tab}_Unemployment Direction"
                    )
                with subtab2:
                    display_chart_with_fallback(
                        plot_labour_with_extremes(df, "Unemployment Rate",
                        "Reversion from Extremes", "Unemployment Rate (%)"),
                        label=f"{tab}_Unemployment Reversion"
                    )
                with subtab3:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Unemployment Rate",
                        "Volatility in Unemployment", "Unemployment Rate (%)"),
                        label=f"{tab}_Unemployment Volatility"
                    )

            # --- Labour Force Engagement ---
            elif selected_use_case == "Labour Force Engagement":
                subtab1, subtab2, subtab3 = st.tabs([
                    "📈 Participation Direction",
                    "🔄 Structural Variability",
                    "📉 Historical Extremes"
                ])
                with subtab1:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Labour Participation Rate",
                        "Participation Trend", "Participation Rate (%)"),
                        label=f"{tab}_Participation Trend"
                    )
                with subtab2:
                    display_chart_with_fallback(
                        plot_labour_line_chart(df, "Labour Participation Rate",
                        "Variability in Participation", "Participation Rate (%)"),
                        label=f"{tab}_Participation Variability"
                    )
                with subtab3:
                    display_chart_with_fallback(
                        plot_labour_with_extremes(df, "Labour Participation Rate",
                        "Reversion from Historical Extremes", "Participation Rate (%)"),
                        label=f"{tab}_Participation Extremes"
                    )
