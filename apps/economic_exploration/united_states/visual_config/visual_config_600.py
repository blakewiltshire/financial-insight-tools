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
# 📥 Universal Chart Imports
# -------------------------------------------------------------------------------------------------
from universal_visual_config_600 import (
    display_chart_with_fallback,
    plot_housing_pipeline_chart,
    plot_mortgage_financing_chart,
    plot_yield_curve_structure_chart,
)

# -------------------------------------------------------------------------------------------------
# 📌 Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    return {
        "Housing Construction Cycle": "Housing Construction Pipeline",
        "Mortgage Financing Conditions": "Mortgage Financing Conditions",
        "Yield Curve Structure": "Yield Curve Structure",
    }

# -------------------------------------------------------------------------------------------------
# 🚦 Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    if selected_use_case == "Housing Construction Cycle":
        for tab, data_slice in tab_mapping.items():
            with tab:
                df = data_slice.reset_index()

                subtab1, = st.tabs(["Housing Construction Pipeline"])

                with subtab1:
                    display_chart_with_fallback(
                        plot_housing_pipeline_chart(df),
                        label="HousingPipeline"
                    )

    elif selected_use_case == "Mortgage Financing Conditions":
        period_options = [3, 6, 12, 24, 60, None]
        mortgage_tabs = list(tab_mapping.keys())[:6]

        for tab, periods in zip(mortgage_tabs, period_options):
            with tab:
                df_weekly = df_map.get("df_secondary")

                if df_weekly is None or df_weekly.empty:
                    st.warning("⚠️ Mortgage financing chart not available — no weekly data loaded.")
                    continue

                df_weekly = df_weekly if periods is None else df_weekly.tail(periods)

                subtab1, = st.tabs(["Mortgage Financing Conditions"])

                with subtab1:
                    display_chart_with_fallback(
                        plot_mortgage_financing_chart(df_weekly.reset_index()),
                        label="MortgageFinancing"
                    )

    elif selected_use_case == "Yield Curve Structure":
        period_options = [3, 6, 12, 24, 60, None]
        yield_curve_tabs = list(tab_mapping.keys())[:6]

        for tab, periods in zip(yield_curve_tabs, period_options):
            with tab:
                df_daily = df_map.get("df_extended")

                if df_daily is None or df_daily.empty:
                    st.warning("⚠️ Yield curve chart not available — no daily data loaded.")
                    continue

                df_daily = df_daily if periods is None else df_daily.tail(periods)

                subtab1, = st.tabs(["Yield Curve Structure"])

                with subtab1:
                    display_chart_with_fallback(
                        plot_yield_curve_structure_chart(df_daily.reset_index()),
                        label="YieldCurveStructure"
                    )

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
