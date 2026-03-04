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
import pandas as pd

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
    plot_labour_with_extremes,
    plot_labour_volatility,
    plot_labour_momentum
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
# Universal Labour Tabs
# -------------------------------------------------------------------------------------------------
def render_universal_labour_tabs(selected_use_case: str, df: pd.DataFrame, tab_key: str) -> bool:
    """
    Universal UI (consistent across all countries) for:
    - Employment Trends
    - Unemployment Context
    - Labour Force Engagement

    Returns True if it handled the use case, else False.
    """
    # --- Employment Trends ---
    if selected_use_case == "Employment Trends":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Hiring Momentum",
            "📉 Volatility Context",
            "🔁 Inflection Points"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Number of People in Employment",
                    "Employment Trends",
                    "Employment Level"
                ),
                label=f"{tab_key}_HiringMomentum"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Number of People in Employment",
                    "Hiring Volatility",
                    "Employment Level"
                ),
                label=f"{tab_key}_HiringVolatility"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_momentum(
                    df,
                    "Number of People in Employment",
                    "Turning Points in Employment",
                    "Employment Level"
                ),
                label=f"{tab_key}_EmploymentInflection"
            )
        return True

    # --- Unemployment Context ---
    if selected_use_case == "Unemployment Context":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Unemployment Direction",
            "📈 Extremes & Reversion",
            "🌪️ Volatility"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Unemployment Rate",
                    "Unemployment Direction",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentDirection"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_with_extremes(
                    df,
                    "Unemployment Rate",
                    "Reversion from Extremes",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentReversion"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Unemployment Rate",
                    "Volatility in Unemployment",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentVolatility"
            )
        return True

    # --- Labour Force Engagement ---
    if selected_use_case == "Labour Force Engagement":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Participation Direction",
            "🔄 Structural Variability",
            "📉 Historical Extremes"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Labour Participation Rate",
                    "Participation Trend",
                    "Participation Rate (%)"
                ),
                label=f"{tab_key}_ParticipationTrend"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Labour Participation Rate",
                    "Variability in Participation",
                    "Volatility (percentage points)",
                    window=6
                ),
                label=f"{tab_key}_ParticipationVariability"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_with_extremes(
                    df,
                    "Labour Participation Rate",
                    "Reversion from Historical Extremes",
                    "Participation Rate (%)"
                ),
                label=f"{tab_key}_ParticipationExtremes"
            )
        return True

    return False

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

            # --- Universal (consistent across countries) ---
            handled = render_universal_labour_tabs(selected_use_case, df, tab)
            if handled:
                continue
