# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🛑 ATR-Based Stop Calculator

Supports stop-loss zone estimation using Average True Range (ATR) volatility logic.
Designed for pre-trade planning, particularly within Trade Structuring & Risk Planning.

Key Features:
- Load single-asset data from default, user, or uploaded CSV sources.
- Compute ATR across Daily, Weekly, Monthly views with short- and medium-term windows.
- Determine suggested stop-loss distances based on historical volatility buffers.
- Visualise price and ATR-based stop range overlays.

Note: This is a volatility tool — it does not generate trading signals or strategies.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import load_markdown_file, build_sidebar_links, get_named_paths

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_atr_stop_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_atr_stop_calculator.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Data + Mapping
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_default import (
    load_data_from_file, clean_data, resample_data
)
from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="ATR-Based Stop Calculator", layout="wide")
st.title("🛑 ATR-Based Stop Calculator")
st.caption("*Use asset volatility to plan structured exit zones.*")

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_atr_stop_calculator.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Setup
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
        st.stop()
elif data_source.startswith("Preloaded"):
    is_user = "User" in data_source
    assets = get_user_preloaded_assets() if is_user else get_preloaded_assets()
    category = st.sidebar.selectbox("Asset Category", list(assets.keys()))
    asset = st.sidebar.selectbox("Select Asset",
                                 list(assets[category].keys()) if is_user else assets[category])
    path = get_user_asset_path(category, asset) if is_user else get_asset_path(category, asset)
    df, _ = clean_data(load_data_from_file(path))
    asset_name = asset

# -------------------------------------------------------------------------------------------------
# Sidebar Controls
# -------------------------------------------------------------------------------------------------
st.sidebar.title("Time Horizon")
period_slider = st.sidebar.slider("Compare over past X periods", 30, 300, 100)

with st.expander("ℹ️ Help: How to interpret ATR-based analysis"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_atr_stop_calculator.md")

# -------------------------------------------------------------------------------------------------
# ATR Calculation
# -------------------------------------------------------------------------------------------------
# pylint: disable=redefined-outer-name
def calculate_atr(df_slice, window=14):
    """
    Calculate the Average True Range (ATR) for a given DataFrame slice.

    Parameters:
        df_slice (pd.DataFrame): DataFrame with columns ['high', 'low', 'close'].
        window (int): Number of periods to use for ATR calculation.

    Returns:
        pd.DataFrame: Original DataFrame with added columns for True Range and ATR.
    """
    df_slice = df_slice.copy()
    df_slice["Previous Close"] = df_slice["close"].shift(1)
    df_slice["High-Low"] = df_slice["high"] - df_slice["low"]
    df_slice["High-PC"] = (df_slice["high"] - df_slice["Previous Close"]).abs()
    df_slice["Low-PC"] = (df_slice["low"] - df_slice["Previous Close"]).abs()
    df_slice["True Range"] = df_slice[["High-Low", "High-PC", "Low-PC"]].max(axis=1)
    df_slice["ATR"] = df_slice["True Range"].rolling(window=window).mean()
    return df_slice

# -------------------------------------------------------------------------------------------------
# Volatility Summary & Chart
# -------------------------------------------------------------------------------------------------
# pylint: disable=redefined-outer-name
def render_atr_analysis(df_slice, label, window=14):
    """
    Render ATR analysis, including summary statistics and a dual-axis chart.

    Parameters:
        df_slice (pd.DataFrame): Time-series data including ['high', 'low', 'close', 'date'].
        label (str): Label for the asset or series being analysed.
        window (int): Number of periods to use for ATR calculation.

    Returns:
        None. Renders visual output in the Streamlit app.
    """
    df_atr = calculate_atr(df_slice, window)
    df_atr = df_atr.dropna().copy()
    latest = df_atr.iloc[-1]
    current_price = latest["close"]
    atr = latest["ATR"]
    upper = current_price + atr
    lower = current_price - atr

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown(f"<h5 style='margin-bottom: 0.5rem;'>ATR Summary "
                    f"<small>({window}-period window from \
                    last {len(df_slice)} periods)</small></h5>",
                    unsafe_allow_html=True)
        st.markdown(f"- **Current ATR ({window}):** {atr:.2f}")
        st.markdown(f"- **Upper Band (Stop Buffer):** {upper:.2f}")
        st.markdown(f"- **Lower Band (Stop Buffer):** {lower:.2f}")

        st.caption(
        f"This view uses a {window}-period window to measure recent \
        price variability.\n\n"
        "ATR (Average True Range) reflects typical daily price movement. \
        It does not predict direction — "
        "it quantifies how far the asset *might* move in either direction under \
        recent conditions.\n\n"
        "The bands shown here represent one ATR above and below the current price. \
        These are **volatility buffers**, "
        "not targets. Use them to estimate whether a proposed stop-loss or Desired \
        Profit Target (DPT) lies "
        "within typical range movement."
    )

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_atr['date'], y=df_atr['close'], name="Price"))
        fig.add_trace(go.Scatter(x=df_atr['date'], y=df_atr['ATR'], name=f"ATR ({window})",
                                 yaxis="y2", line={"dash": "dot"}))
        fig.add_trace(go.Scatter(x=df_atr['date'], y=[upper]*len(df_atr),
                                 name="Upper ATR Band", line={"dash": "dot"}))
        fig.add_trace(go.Scatter(x=df_atr['date'], y=[lower]*len(df_atr),
                                 name="Lower ATR Band", line={"dash": "dot"}))

        fig.update_layout(
            title=f"ATR Overlay — {label}",
            xaxis_title="Date",
            yaxis_title="Price",
            yaxis2={"title": "ATR", "overlaying": "y", "side": "right", "showgrid": False},
            legend={"x": 0.01, "y": 0.99}

        )
        st.plotly_chart(fig, width='stretch')

# -------------------------------------------------------------------------------------------------
# Main View Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs(["📈 Volatility View", "📉 Short-Term (50 Days)", "📊 Medium-Term (200 Days)"])

# Daily — user slice
with tabs[0]:
    full_df = resample_data(df.copy(), "Daily")
    view_df = full_df.tail(period_slider)
    st.markdown(f"**Asset:** {asset_name}  |  **Periods Used:** {len(view_df)}")
    render_atr_analysis(view_df, "Volatility View")

# 50d and 200d
for i, (label, window) in enumerate(zip(["Short-Term", "Medium-Term"], [50, 200]), start=1):
    with tabs[i]:
        df_short = resample_data(df.copy(), "Daily").tail(window)
        render_atr_analysis(df_short, f"{label} — {window} Days")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.sidebar.divider()

# --- About & Support ---
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
st.markdown("---")
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
           "No trading, investment, or policy advice provided.")
