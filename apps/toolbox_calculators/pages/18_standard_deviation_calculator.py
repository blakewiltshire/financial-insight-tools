# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Standard Deviation Calculator

Supports volatility benchmarking and trade expectation planning based on
historic asset variability.
Designed for use before Trade Structuring & Risk Planning.

Key Features:
- Load single-asset data from default, user, or uploaded CSV sources.
- Calculate standard deviation over Daily, Weekly, Monthly, 50-day, and 200-day views.
- Interpret observed volatility and contextualise trade risk alignment.
- Visualise mean and band distribution across timeframes.

Note: This is a simplified diagnostic tool and should be used alongside
Market & Volatility Scanner for full statistical context.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup — Adjust based on your module's location relative to the project root.
# Path to project root (level_up_3) — for markdown, branding, etc.
# Path to apps directory (level_up_2) — for `use_cases`, `helpers`, etc.
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders, sidebar links etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_standard_deviation_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_standard_deviation.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")


# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Clean and format Single Asset Files
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_default import (
    load_data_from_file, clean_data, resample_to_frequency
)


# -------------------------------------------------------------------------------------------------
# Mapping Logic
# -------------------------------------------------------------------------------------------------
from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Standard Deviation Calculator", layout="wide")
st.title("📊 Standard Deviation Calculator")
st.caption("*Assess return dispersion to support risk control logic.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_standard_deviation_calculator.md")

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠 Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Asset Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.title("🔎 Select Asset")
data_source = st.sidebar.selectbox("Choose your data source", [
    "Preloaded Asset Types (Default)",
    "Preloaded Asset Types (User)",
    "Upload my own file"
])

df, asset_name = None, None
if data_source == "Upload my own file":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df, _ = clean_data(load_data_from_file(uploaded_file))
        asset_name = uploaded_file.name
    else:
        st.info("Please upload a CSV file.")
        st.stop()
elif data_source.startswith("Preloaded"):
    is_user = "User" in data_source
    assets = get_user_preloaded_assets() if is_user else get_preloaded_assets()
    category = st.sidebar.selectbox("Asset Category", list(assets.keys()))
    asset = st.sidebar.selectbox("Select Asset",
    list(assets[category].keys()) if is_user else assets[category])
    asset_path = get_user_asset_path(
    category, asset) if is_user else get_asset_path(category, asset
    )
    df, _ = clean_data(load_data_from_file(asset_path))
    asset_name = asset

# -------------------------------------------------------------------------------------------------
# Analysis Timeframes
# -------------------------------------------------------------------------------------------------
st.sidebar.title("Time Horizon")
timeframe = "Timeframe Label"  # Label Output
period_slider = st.sidebar.slider("Compare over past X periods", min_value=30,
max_value=300, value=100)

# -------------------------------------------------------------------------------------------------
# Help
# -------------------------------------------------------------------------------------------------
with st.expander("ℹ️ Help: How to interpret standard deviation analysis"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_standard_deviation.md")

# -------------------------------------------------------------------------------------------------
# Main View Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs(["📈 Variability Overview", "📉 Short-Term (50 Days)", "📊 Medium-Term (200 Days)"])

def analyse_volatility(subset_df, title_suffix):
    """
    Displays summary statistics and chart with standard deviation bands for a given asset view.
    """
    std = subset_df['close'].std()
    mean = subset_df['close'].mean()
    latest_price = subset_df['close'].iloc[-1]

    upper_band = mean + std
    lower_band = mean - std
    band_width_pct = (std / mean) * 100

    z_score = (latest_price - mean) / std if std > 0 else 0
    summary = {
        "Mean Price": f"{mean:.2f}",
        "Standard Deviation": f"{std:.2f}",
        "Band Width %": f"{band_width_pct:.2f}%",
        "Z-Score (Current Price)": f"{z_score:.2f}"
    }

    col1, col2 = st.columns([2, 3])

    with col1:
        st.write(f"**Summary ({title_suffix})**")
        for k, v in summary.items():
            st.markdown(f"- **{k}:** {v}")

        if abs(z_score) > 2:
            st.warning("Asset is significantly away from its mean — monitor \
            risk-reward alignment.")
        elif abs(z_score) > 1:
            st.info("Moderate deviation from mean — consider range edges for planning.")
        else:
            st.success("Price near historical mean — volatility may be compressing.")

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=subset_df['date'], y=subset_df['close'], name="Price"))
        fig.add_trace(go.Scatter(x=subset_df['date'], y=[mean]*len(subset_df),
        name="Mean", line={"dash": "dash"}))
        fig.add_trace(go.Scatter(x=subset_df['date'], y=[upper_band]*len(subset_df),
        name="+1 Std Dev", line={"dash": "dot"}))
        fig.add_trace(go.Scatter(x=subset_df['date'], y=[lower_band]*len(subset_df),
        name="-1 Std Dev", line={"dash": "dot"}))

        fig.update_layout(title=f"Price and Volatility Bands — {title_suffix}",
                          xaxis_title="Date", yaxis_title="Price")

        # Add explanatory caption before displaying the chart
        st.caption("Volatility bands represent ±1 standard deviation around the historical mean. \
        Used for contextual planning.")

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------------------------------------
# Daily/Weekly/Monthly View
# -------------------------------------------------------------------------------------------------
with tabs[0]:
    view_df = resample_to_frequency(df, column="close", timeframe=timeframe)
    view_df = view_df.tail(period_slider)
    st.markdown(f"**Asset:** {asset_name}  |  **Periods Used:** {len(view_df)}")
    analyse_volatility(view_df, f"{timeframe} View")

# -------------------------------------------------------------------------------------------------
# 50-Day and 200-Day Views
# -------------------------------------------------------------------------------------------------
for i, (label, window) in enumerate(zip(["Short-Term", "Medium-Term"], [50, 200]), start=1):
    with tabs[i]:
        slice_df = df.tail(window)
        analyse_volatility(slice_df, f"{label} — {window} Days")

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
            use_container_width=True,
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.sidebar.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
           "No trading, investment, or policy advice provided.")
