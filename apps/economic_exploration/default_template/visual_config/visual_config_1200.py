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
from universal_visual_config_1200 import (
    display_chart_with_fallback,
    plot_signal_a_chart,
    plot_signal_b_chart,
    plot_signal_c_chart
)

# -------------------------------------------------------------------------------------------------
# 📌 Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    """
    Returns a mapping of use case labels to section headers in the UI.

    Returns:
        dict: Mapping of use case name → section display title.
    """
    return {
        "Signal A": "📊 Signal A — Time Series",
        "Signal B": "📊 Signal B — Rolling Average",
        "Signal C": "📊 Signal C — Band Highlight"
    }

# -------------------------------------------------------------------------------------------------
# 🧭 Local Chart Configs (If applicable)
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# 🚦 Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for the Generic Template theme.

    Parameters:
        selected_use_case (str): Selected insight use case (Signal A, B, or C).
        tab_mapping (dict): Dictionary of tab label → dataframe subset.
        df_map (dict): Original dataset registry dictionary.

    Renders:
        Streamlit visual tabs with fallback messaging.
    """
    for tab, data_slice in tab_mapping.items():
        with tab:
            df = data_slice.reset_index()

            # --- Signal A ---
            if selected_use_case == "Signal A":
                subtab1, = st.tabs(["📈 Signal A Chart"])
                with subtab1:
                    display_chart_with_fallback(
                        plot_signal_a_chart(df),
                        label=f"{tab}_SignalA"
                    )

            # --- Signal B ---
            elif selected_use_case == "Signal B":
                subtab1, = st.tabs(["📉 Signal B Chart"])
                with subtab1:
                    display_chart_with_fallback(
                        plot_signal_b_chart(df),
                        label=f"{tab}_SignalB"
                    )

            # --- Signal C ---
            elif selected_use_case == "Signal C":
                subtab1, = st.tabs(["📊 Signal C Chart"])
                with subtab1:
                    display_chart_with_fallback(
                        plot_signal_c_chart(df),
                        label=f"{tab}_SignalC"
                    )

            else:
                st.info("ℹ️ No charts available for the selected use case.")

            # 🔧 Optional extension block (add local visuals if needed)
            # elif selected_use_case == "Local Macro Indicator":
            #     display_chart_with_fallback(
            #         plot_indicator_line_chart(...),
            #         label="Local Chart Title"
            #     )
