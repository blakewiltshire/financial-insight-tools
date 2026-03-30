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
    plot_services_consumption_real_chart,
)

# -------------------------------------------------------------------------------------------------
# Section Header Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    return {
        "Forward Production Conditions": "Forward Production Conditions",
        "Services Activity Conditions": "Services Activity Conditions",
    }

# -------------------------------------------------------------------------------------------------
# Chart Dispatcher for Template Theme
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    if selected_use_case == "Forward Production Conditions":
        for tab, data_slice in tab_mapping.items():
            with tab:
                df = data_slice.reset_index()

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Forward Production Conditions",
                    "Business Conditions Diffusion Index",
                    "Industrial Production Index",
                    "Manufacturing Durable Goods Orders"
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

    elif selected_use_case == "Services Activity Conditions":
        for tab, data_slice in tab_mapping.items():
            with tab:
                df = data_slice.reset_index()

                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Services Activity Conditions",
                    "Business Conditions Diffusion Index",
                    "Services Consumption (Nominal)",
                    "Services Consumption (Real)"
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

    else:
        for tab, _ in tab_mapping.items():
            with tab:
                st.info("ℹ️ No charts available for the selected use case.")
