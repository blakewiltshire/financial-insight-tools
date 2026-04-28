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
from universal_visual_config_1200 import (
    display_chart_with_fallback,
    plot_forward_production_conditions_chart,
    plot_business_conditions_chart,
    plot_industrial_production_chart,
    plot_manufacturing_orders_chart,
    plot_services_activity_conditions_chart,
    plot_services_consumption_nominal_chart,
    plot_services_consumption_real_chart
)

# -------------------------------------------------------------------------------------------------
# Shared Statistical Profile Import
# -------------------------------------------------------------------------------------------------
from universal_visual_shared import calculate_statistical_profile

# -------------------------------------------------------------------------------------------------
# Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    return {
        "Forward Production Conditions": "Forward Production Conditions",
        "Services Activity Conditions": "Services Activity Conditions",
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
# Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    if selected_use_case == "Forward Production Conditions":
        for tab_index, (tab, data_slice) in enumerate(tab_mapping.items()):
            with tab:
                df = _get_visual_df(data_slice)

                subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
                    "Forward Production Conditions",
                    "Business Conditions Diffusion Index",
                    "Industrial Production Index",
                    "Manufacturing Durable Goods Orders",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_forward_production_conditions_chart(df),
                        label="ForwardProductionConditions"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_business_conditions_chart(df),
                        label="BusinessConditionsDiffusionIndex"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_industrial_production_chart(df),
                        label="IndustrialProductionIndex"
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_manufacturing_orders_chart(df),
                        label="ManufacturingDurableGoodsOrders"
                    )

                with subtab5:
                    available_series = [
                        col for col in [
                            "Business Conditions Diffusion Index",
                            "Industrial Production Index",
                            "Manufacturing Durable Goods Orders"
                        ]
                        if df is not None and not df.empty and col in df.columns
                    ]

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no forward production series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_1200_forward_production_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(df[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    elif selected_use_case == "Services Activity Conditions":
        for tab_index, (tab, data_slice) in enumerate(tab_mapping.items()):
            with tab:
                df = _get_visual_df(data_slice)

                subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs([
                    "Services Activity Conditions",
                    "Business Conditions Diffusion Index",
                    "Services Consumption (Nominal)",
                    "Services Consumption (Real)",
                    "Statistical Profile"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_services_activity_conditions_chart(df),
                        label="ServicesActivityConditions"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_business_conditions_chart(df),
                        label="BusinessConditionsDiffusionIndex"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_services_consumption_nominal_chart(df),
                        label="ServicesConsumptionNominal"
                    )

                with subtab4:
                    display_chart_with_fallback(
                        plot_services_consumption_real_chart(df),
                        label="ServicesConsumptionReal"
                    )

                with subtab5:
                    available_series = [
                        col for col in [
                            "Business Conditions Diffusion Index",
                            "Services Consumption (Nominal)",
                            "Services Consumption (Real)"
                        ]
                        if df is not None and not df.empty and col in df.columns
                    ]

                    if not available_series:
                        st.warning("⚠️ Statistical profile not available — no services activity series loaded.")
                    else:
                        selected_series = _get_stable_series_selection(
                            widget_key=f"stats_profile_1200_services_activity_tab_{tab_index}",
                            options=available_series,
                            default_index=0
                        )

                        stats_df = calculate_statistical_profile(df[selected_series])

                        col1, col2 = st.columns([2, 5])
                        with col1:
                            st.caption("Statistical profile reflects the currently selected period window.")
                            st.markdown(f"**Statistical Profile: {selected_series}**")
                            st.table(stats_df.set_index("Metric"))

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
