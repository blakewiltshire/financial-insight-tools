# -------------------------------------------------------------------------------------------------
# Generic Template — Visual Config (Local Extension)
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
import streamlit as st
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Path Setup
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
        "Employment Trends": "Employment Growth and Hiring Activity",
        "Unemployment Context": "Unemployment Rates and Volatility",
        "Labour Force Engagement": "Participation and Labour Supply Trends"
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


# -------------------------------------------------------------------------------------------------
# Universal Labour Tabs
# -------------------------------------------------------------------------------------------------
def render_universal_labour_tabs(
    selected_use_case: str,
    df: pd.DataFrame,
    tab_index: int,
    tab_key: str
) -> bool:
    """
    Universal UI (consistent across all countries) for:
    - Employment Trends
    - Unemployment Context
    - Labour Force Engagement

    Returns True if it handled the use case, else False.
    """
    # --- Employment Trends ---
    if selected_use_case == "Employment Trends":
        subtab1, subtab2, subtab3, subtab4 = st.tabs([
            "Hiring Momentum",
            "Volatility Context",
            "Inflection Points",
            "Statistical Profile"
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

        with subtab4:
            available_series = [
                col for col in [
                    "Number of People in Employment"
                ]
                if df is not None and not df.empty and col in df.columns and df[col].dropna().shape[0] > 0
            ]

            if not available_series:
                st.warning("⚠️ Statistical profile not available — no employment series loaded.")
            else:
                selected_series = _get_stable_series_selection(
                    widget_key=f"stats_profile_uk_200_employment_tab_{tab_index}",
                    options=available_series,
                    default_index=0
                )

                stats_df = calculate_statistical_profile(df[selected_series])

                if stats_df.empty:
                    st.warning("⚠️ Statistical profile not available — selected series contains insufficient data.")
                else:
                    col1, col2 = st.columns([2, 5])

                    with col1:
                        st.caption("Statistical profile reflects the currently selected period window.")
                        st.markdown(f"**Statistical Profile: {selected_series}**")
                        st.table(stats_df.set_index("Metric"))

        return True

    # --- Unemployment Context ---
    if selected_use_case == "Unemployment Context":
        subtab1, subtab2, subtab3, subtab4 = st.tabs([
            "Unemployment Direction",
            "Extremes & Reversion",
            "Volatility",
            "Statistical Profile"
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

        with subtab4:
            available_series = [
                col for col in [
                    "Unemployment Rate"
                ]
                if df is not None and not df.empty and col in df.columns and df[col].dropna().shape[0] > 0
            ]

            if not available_series:
                st.warning("⚠️ Statistical profile not available — no unemployment series loaded.")
            else:
                selected_series = _get_stable_series_selection(
                    widget_key=f"stats_profile_uk_200_unemployment_tab_{tab_index}",
                    options=available_series,
                    default_index=0
                )

                stats_df = calculate_statistical_profile(df[selected_series])

                if stats_df.empty:
                    st.warning("⚠️ Statistical profile not available — selected series contains insufficient data.")
                else:
                    col1, col2 = st.columns([2, 5])

                    with col1:
                        st.caption("Statistical profile reflects the currently selected period window.")
                        st.markdown(f"**Statistical Profile: {selected_series}**")
                        st.table(stats_df.set_index("Metric"))

        return True

    # --- Labour Force Engagement ---
    if selected_use_case == "Labour Force Engagement":
        subtab1, subtab2, subtab3, subtab4 = st.tabs([
            "Participation Direction",
            "Structural Variability",
            "Historical Extremes",
            "Statistical Profile"
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

        with subtab4:
            available_series = [
                col for col in [
                    "Labour Participation Rate"
                ]
                if df is not None and not df.empty and col in df.columns and df[col].dropna().shape[0] > 0
            ]

            if not available_series:
                st.warning("⚠️ Statistical profile not available — no participation series loaded.")
            else:
                selected_series = _get_stable_series_selection(
                    widget_key=f"stats_profile_uk_200_participation_tab_{tab_index}",
                    options=available_series,
                    default_index=0
                )

                stats_df = calculate_statistical_profile(df[selected_series])

                if stats_df.empty:
                    st.warning("⚠️ Statistical profile not available — selected series contains insufficient data.")
                else:
                    col1, col2 = st.columns([2, 5])

                    with col1:
                        st.caption("Statistical profile reflects the currently selected period window.")
                        st.markdown(f"**Statistical Profile: {selected_series}**")
                        st.table(stats_df.set_index("Metric"))

        return True

    return False


# -------------------------------------------------------------------------------------------------
# Chart Dispatcher — Universal Charts First, Local Extensions After
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    """
    Chart dispatcher for Labour Market Dynamics — with fallback messaging and AI compatibility.
    """
    for tab_index, (tab, data_slice) in enumerate(tab_mapping.items()):
        with tab:
            df = _get_visual_df(data_slice)

            handled = render_universal_labour_tabs(
                selected_use_case=selected_use_case,
                df=df,
                tab_index=tab_index,
                tab_key=str(tab)
            )

            if handled:
                continue
