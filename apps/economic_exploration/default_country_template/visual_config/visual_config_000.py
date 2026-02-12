# -------------------------------------------------------------------------------------------------
# 📈 Generic Template — Visual Config (Local Extension)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument, unused-import

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📈 Local Visual Config — Thematic Extension Module
--------------------------------------------------

This module defines local chart logic for a specific thematic grouping.
It extends the universal visual configuration, enabling optional subtab
layouts, custom overlays, and fallback handling per insight use case.

🧭 Purpose:
- Support country-specific or theme-specific visual extensions
- Maintain consistent layout via **subtabs**, even if only one chart
- Ensure compatibility with fallback handling and AI summarisation

✅ Required Structure:
- Each use case must define charts within subtabs to ensure layout stability.
- Use `display_chart_with_fallback(...)` to prevent Streamlit key collisions.

🧠 AI Notes:
- Tab + subtab chart labels are required for unique Streamlit keys.
- This module is called automatically if present for the active theme module.

Usage:
- Invoked via `render_all_charts_local(...)` in the main theme module.
- Start from the universal chart dispatcher and add local extensions as needed.
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
from universal_visual_config_000 import (
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
