# -------------------------------------------------------------------------------------------------
# 🚀 Economic Exploration — 🔗 Thematic Correlation Explorer
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Universal correlation module with AI-ready scaffolding:
- Multi-theme, multi-indicator selection
- Full harmonisation (frequency, metadata)
- Z-score standardisation
- Correlation matrix + heatmap
- Dynamic multi-indicator overlay
- Timeline slicing with summary statistics
- Fully integrated Macro Interaction Tools (Observations, AI Export, Journal)
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup (Canonical)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------------------------------------------------------
# Core Utilities (Canonical)
# -------------------------------------------------------------------------------------------------
from core.helpers import ( # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# Resolve Named Paths
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_thematic_correlation_explore.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_thematic_correlation_explorer.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Load Registry & Engine Components
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))
sys.path.append(os.path.join(APPS_PATH, "registry"))
sys.path.append(os.path.join(APPS_PATH, "economic_exploration", "correlation_engine"))

from economic_series_map import ECONOMIC_SERIES_MAP
from correlation_data_loader import load_indicator_data
from harmonisation_engine import standardise_metadata_fields
from correlation_engine import build_correlation_matrix
from correlation_visualisation import render_correlation_heatmap, render_standardised_overlay

# Macro Interaction Tool Imports (Strict Canonical)
from observation_handler_thematic_correlation import (
    observation_input_form,
    display_observation_log,
    save_observation
)

from macro_insight_sidebar_panel_thematic_correlation import render_macro_sidebar_tools
from render_macro_interaction_tools_panel_thematic_correlation import render_macro_interaction_tools_panel

# -------------------------------------------------------------------------------------------------
# Page Setup (Canonical)
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Thematic Correlation Explorer", layout="wide")
st.title("🔗 Thematic Correlation Explorer")
st.caption("*Explore cross-theme macroeconomic relationships via fully harmonised multi-indicator correlation.*")

with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation (Canonical)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🌍 Economic Exploration')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Thematic Groupings (Canonical)
# -------------------------------------------------------------------------------------------------
theme_options = {
    "100_economic_growth_stability": "📈 Economic Growth Stability",
    "200_labour_market_dynamics": "💼 Labour Market Dynamics",
    "300_consumer_behaviour_confidence": "🛒 Consumer Behaviour Confidence",
    "400_inflation_price_dynamics": "📉 Inflation Price Dynamics",
    "500_monetary_indicators_policy_effects": "💵 Monetary Indicators Policy Effects",
    "600_financial_conditions_risk_analysis": "🔍 Financial Conditions Risk Analysis",
    "700_global_trade_economic_relations": "🌍 Global Trade Economic Relations",
    "800_supply_chains_logistics": "🚢 Supply Chains Logistics",
    "900_commodity_markets_pricing": "📦 Commodity Markets Pricing",
    "1000_currency_exchange_movements": "💱 Currency Exchange Movements",
    "1100_market_trends_financial_health": "📊 Market Trends Financial Health",
    "1200_industry_performance_production": "🏠 Industry Performance Production",
    "1300_sustainability_green_economy": "🌱 Sustainability Green Economy",
    "1400_digital_economy_ecommerce": "🔢 Digital Economy Ecommerce",
    "1500_innovation_rd_investment": "🚀 Innovation Rd Investment",
    "1600_urbanisation_and_smart_cities": "🌆 Urbanisation And Smart Cities",
    "1700_healthcare_economics": "🏥 Healthcare Economics",
    "1800_education_and_human_capital": "📚 Education And Human Capital",
    "1900_social_impact_and_inequality": "🤝 Social Impact And Inequality",
    "2000_geopolitical_risks_and_global_stability": "🌐 Geopolitical Risks And Global Stability",
    "2010_frontier_sectors": "🔮 Frontier Sectors"
}

# -------------------------------------------------------------------------------------------------
# User Selection — Multi Theme, Multi Indicator
# -------------------------------------------------------------------------------------------------
primary_theme_label = st.sidebar.selectbox("Select Primary Thematic Grouping:", list(theme_options.values()))
primary_theme_code = [code for code, label in theme_options.items() if label == primary_theme_label][0]
remaining_theme_options = {k: v for k, v in theme_options.items() if k != primary_theme_code}

secondary_theme_labels = st.sidebar.multiselect("Select Additional Thematic Groupings (optional):",
                                        list(remaining_theme_options.values()))
secondary_theme_codes = [code for code, label in remaining_theme_options.items() if label in secondary_theme_labels]
selected_theme_codes = [primary_theme_code] + secondary_theme_codes

# -------------------------------------------------------------------------------------------------
# Build Full Indicator Pool (Canonical)
# -------------------------------------------------------------------------------------------------
eligible_indicators = []
for country, themes in ECONOMIC_SERIES_MAP.items():
    for theme_code, templates in themes.items():
        if theme_code in selected_theme_codes:
            for template_key, indicators in templates.items():
                for indicator_name, metadata in indicators.items():
                    if metadata.get("allow_correlation"):
                        seasonal, value_type, unit_type = standardise_metadata_fields(metadata)
                        eligible_indicators.append({
                            "label": f"{country} — {indicator_name}",
                            "country": country,
                            "theme_code": theme_code,
                            "indicator_id": metadata.get("indicator_id"),
                            "indicator_name": indicator_name,
                            "seasonal": seasonal,
                            "value_type": value_type,
                            "unit_type": unit_type
                        })

if not eligible_indicators:
    st.warning("No eligible indicators found for selected themes.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Multi-Indicator Selection
# -------------------------------------------------------------------------------------------------
all_labels = [x['label'] for x in eligible_indicators]
selected_labels = st.sidebar.multiselect("Select Indicators for Correlation Analysis:", all_labels)
selected_objects = [x for x in eligible_indicators if x['label'] in selected_labels]

if not selected_objects:
    st.warning("Please select at least one indicator to proceed.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Metadata Diagnostics Summary (Canonical)
# -------------------------------------------------------------------------------------------------
for category, label in [("seasonal", "Seasonal Adjustment"),
                        ("value_type", "Value Type"),
                        ("unit_type", "Unit Scale")]:
    unique_vals = set([obj[category] for obj in selected_objects])
    if len(unique_vals) > 1:
        st.sidebar.warning(f"⚠ Mixed {label}: {', '.join(unique_vals)}")

with st.sidebar.expander("ℹ️ Harmonisation Signals"):
    st.markdown("""
**Seasonal Adjustment**
Differences may introduce distortion between adjusted and raw data.

**Value Type**
Mixing levels, growth rates, and indexes may affect comparability.

**Unit Scale**
Standardisation helps but scaling disparities still warrant caution.
""")

# -------------------------------------------------------------------------------------------------
# Load & Harmonise Data
# -------------------------------------------------------------------------------------------------
harmonised_series = []
for obj in selected_objects:
    loader_obj = {
        "country": obj["country"],
        "theme_code": obj["theme_code"],
        "indicator_id": obj["indicator_id"],
        "indicator_name": obj["indicator_name"]
    }
    series, metadata, status = load_indicator_data(loader_obj, PROJECT_PATH)
    if status:
        st.warning(f"{obj['label']}: {status}")
    else:
        harmonised_series.append(series)

if not harmonised_series:
    st.warning("No data successfully loaded.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# DataFrame Build
# -------------------------------------------------------------------------------------------------
full_df = pd.concat(harmonised_series, axis=1, join="inner")
standardised_df = (full_df - full_df.mean()) / full_df.std()

# -------------------------------------------------------------------------------------------------
# Structural Correlation Summary
# -------------------------------------------------------------------------------------------------
full_corr = standardised_df.corr()
off_diag = full_corr.where(~np.eye(full_corr.shape[0], dtype=bool)).stack().values
if len(off_diag) > 0:
    direct_count = sum(off_diag > 0.3)
    inverse_count = sum(off_diag < -0.3)
    max_corr = np.nanmax(off_diag)
    min_corr = np.nanmin(off_diag)
else:
    direct_count = inverse_count = 0
    max_corr = min_corr = np.nan

# -------------------------------------------------------------------------------------------------
# Generate Summary Table (for AI Bundle Compatibility)
# -------------------------------------------------------------------------------------------------
summary_data = {
    "Statistic": [
        "Indicators Selected",
        "Countries Represented",
        "Date Range",
        "Direct Relationships (r > 0.3)",
        "Inverse Relationships (r < -0.3)",
        "Max Correlation",
        "Min Correlation"
    ],
    "Value": [
        len(selected_objects),
        len(set([x['country'] for x in selected_objects])),
        f"{full_df.index.min().date()} ➔ {full_df.index.max().date()}",
        direct_count,
        inverse_count,
        round(max_corr, 3) if not np.isnan(max_corr) else 'N/A',
        round(min_corr, 3) if not np.isnan(min_corr) else 'N/A'
    ]
}
summary_df = pd.DataFrame(summary_data)



# -------------------------------------------------------------------------------------------------
# Main Correlation Analysis Tabs (Canonical)
# -------------------------------------------------------------------------------------------------
tabs = st.tabs(["Overview Summary", "📉 Short-Term (50 Days)", "📊 Medium-Term (200 Days)", "🕰 Full History", "ℹ️ Help"])

# Overview Tab
with tabs[0]:
    st.write(f"**Indicators Selected:** {len(selected_objects)}")
    st.write(f"**Countries Represented:** {len(set([x['country'] for x in selected_objects]))}")
    st.write(f"**Date Range:** {full_df.index.min().date()} ➔ {full_df.index.max().date()}")
    st.write("**Structural Correlation Summary:**")
    st.write(f"- Direct Relationships (r > +0.3): {direct_count}")
    st.write(f"- Inverse Relationships (r < -0.3): {inverse_count}")
    st.write(f"- Max Correlation: {round(max_corr, 3) if not np.isnan(max_corr) else 'N/A'}")
    st.write(f"- Min Correlation: {round(min_corr, 3) if not np.isnan(min_corr) else 'N/A'}")


# Rolling Windows
for i, (tab, label, window) in enumerate(zip(tabs[1:4], ["Short-Term", "Medium-Term", "Full History"], [50, 200, None])):
    with tab:
        sliced = standardised_df.tail(window) if window else standardised_df
        corr_matrix = sliced.corr()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**Summary Statistics ({label}):**")
            values = corr_matrix.values.flatten()
            st.write(f"- Mean Correlation: {round(np.nanmean(values), 3)}")
            st.write(f"- Std Dev Correlation: {round(np.nanstd(values), 3)}")
            st.write(f"- Max: {round(np.nanmax(values), 3)}")
            st.write(f"- Min: {round(np.nanmin(values), 3)}")
        with col2:
            render_correlation_heatmap(corr_matrix, key_suffix=f"{i}")

        st.divider()
        render_standardised_overlay(sliced, key_suffix=f"{i}")

# Help Tab
with tabs[4]:
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.warning("Help file not found.")

st.divider()


# -------------------------------------------------------------------------------------------------
# Macro Interaction Panel — Observation
# -------------------------------------------------------------------------------------------------
theme_code = primary_theme_code
theme_title = primary_theme_label
selected_use_case = "Thematic Correlation Snapshot"

# Sidebar — Macro Interaction Tools Activation Panel
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case,
    selected_timeframe=None,
    summary_df=summary_df
)

# -------------------------------------------------------------------------------------------------
# 🧠 Macro Interaction Tools (Visible Title + Panels)
# -------------------------------------------------------------------------------------------------
if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    theme_code=theme_code,
    theme_title=theme_title,
    selected_use_case=selected_use_case,
    themes_selected=selected_theme_codes,
    indicators_selected=selected_labels,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    with open(os.path.join(PROJECT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            width='stretch',
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width='stretch',
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()

st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
    No trading, investment, or policy advice provided."
)
