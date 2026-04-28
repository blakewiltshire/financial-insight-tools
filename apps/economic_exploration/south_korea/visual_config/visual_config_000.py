# -------------------------------------------------------------------------------------------------
#  Generic Template — Visual Config (Local Extension)
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
- Invoked automatically from the main theme module (`100_economic_growth_stability.py`, `200_💼_labour_market_dynamics.py`, etc.)
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
from universal_visual_config_000 import (
    display_chart_with_fallback,
    plot_signal_a_chart,
    plot_signal_b_chart,
    plot_signal_c_chart
)

# -------------------------------------------------------------------------------------------------
# Shared Statistical Profile Import
# -------------------------------------------------------------------------------------------------
from universal_visual_shared import calculate_statistical_profile

# -------------------------------------------------------------------------------------------------
# Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    """
    Returns a mapping of use case labels to section headers in the UI.
    """
    return {
        "Signal A": "Signal A — Time Series",
        "Signal B": "Signal B — Rolling Average",
        "Signal C": "Signal C — Band Highlight"
    }

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


def _render_statistical_profile(
    df: pd.DataFrame,
    candidate_columns: list[str],
    widget_key: str,
    warning_message: str
) -> None:
    """
    Renders a generic statistical profile block below the chart.
    """
    available_series = [
        col for col in candidate_columns
        if df is not None and not df.empty and col in df.columns and df[col].dropna().shape[0] > 0
    ]

    if not available_series:
        st.warning(warning_message)
        return

    selected_series = _get_stable_series_selection(
        widget_key=widget_key,
        options=available_series,
        default_index=0
    )

    stats_df = calculate_statistical_profile(df[selected_series])

    if stats_df.empty:
        st.warning("⚠️ Statistical profile not available — selected series contains insufficient data.")
        return

    st.caption("Statistical profile reflects the currently selected period window.")
    st.markdown(f"**Statistical Profile: {selected_series}**")
    st.table(stats_df.set_index("Metric"))


# -------------------------------------------------------------------------------------------------
# Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for the Generic Template theme.

    Parameters:
        selected_use_case (str): Selected insight use case (Signal A, B, or C).
        tab_mapping (dict): Dictionary of tab label → dataframe subset.
        df_map (dict): Original dataset registry dictionary.
    """
    for tab_index, (tab, data_slice) in enumerate(tab_mapping.items()):
        with tab:
            df = _get_visual_df(data_slice)

            # --- Signal A ---
            if selected_use_case == "Signal A":
                display_chart_with_fallback(
                    plot_signal_a_chart(df),
                    label=f"{tab}_SignalA"
                )

                st.markdown("---")

                _render_statistical_profile(
                    df=df,
                    candidate_columns=["Signal A"],
                    widget_key=f"stats_profile_000_signal_a_tab_{tab_index}",
                    warning_message="⚠️ Statistical profile not available — no Signal A series loaded."
                )

            # --- Signal B ---
            elif selected_use_case == "Signal B":
                display_chart_with_fallback(
                    plot_signal_b_chart(df),
                    label=f"{tab}_SignalB"
                )

                st.markdown("---")

                _render_statistical_profile(
                    df=df,
                    candidate_columns=["Signal B"],
                    widget_key=f"stats_profile_000_signal_b_tab_{tab_index}",
                    warning_message="⚠️ Statistical profile not available — no Signal B series loaded."
                )

            # --- Signal C ---
            elif selected_use_case == "Signal C":
                display_chart_with_fallback(
                    plot_signal_c_chart(df),
                    label=f"{tab}_SignalC"
                )

                st.markdown("---")

                _render_statistical_profile(
                    df=df,
                    candidate_columns=["Signal C"],
                    widget_key=f"stats_profile_000_signal_c_tab_{tab_index}",
                    warning_message="⚠️ Statistical profile not available — no Signal C series loaded."
                )

            else:
                st.info("ℹ️ No charts available for the selected use case.")
