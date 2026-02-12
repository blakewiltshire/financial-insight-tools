# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
⚠️ Value at Risk (VaR) Calculator

Estimates potential asset loss at defined confidence levels over selected periods.
Designed for integration with Trade Structuring & Risk Planning.

Key Features:
- Load asset price data from default, user, or uploaded CSV sources.
- Compute historical Value at Risk using configurable confidence levels.
- Visualise return distributions and tail risk exposure.
- Support trade planning through observed drawdown expectations.

Note: This is a simplified single-asset VaR tool. For full contextual diagnostics,
use with Market & Volatility Scanner or integrated DSS modules.
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
import numpy as np
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_var_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_var_calculator.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Loaders and Mapping Logic
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_default import (
    load_data_from_file, clean_data
)
from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Value at Risk (VaR) Calculator", layout="wide")
st.title("⚠️ Value at Risk (VaR) Calculator")
st.caption("*Simulate expected portfolio loss at a chosen confidence level.*")

with st.expander("📘 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_var_calculator.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠️ Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
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
    asset_path = get_user_asset_path(category, asset) if is_user else get_asset_path(
    category, asset)
    df, _ = clean_data(load_data_from_file(asset_path))
    asset_name = asset

# -------------------------------------------------------------------------------------------------
# Analysis Settings
# -------------------------------------------------------------------------------------------------
st.sidebar.title("VaR Settings")
confidence_level = st.sidebar.select_slider("Confidence Level", options=[90, 95, 99], value=95)
holding_period = st.sidebar.slider("Holding Period (Days)", min_value=1, max_value=30, value=1)

with st.expander("ℹ️ Help: How to interpret VaR analysis"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_var_calculator.md")

# -------------------------------------------------------------------------------------------------
# Main View – VaR Computation and Chart
# -------------------------------------------------------------------------------------------------
st.subheader("📉 Historical Value at Risk Analysis")

# Calculate daily returns
df = df.copy()
df["returns"] = df["close"].pct_change().dropna()
df = df.dropna(subset=["returns"])

# Calculate percentile-based VaR and CVaR
confidence_pct = confidence_level / 100
var_value = np.percentile(df["returns"], 100 - confidence_level)
cvar_value = df[df["returns"] <= var_value]["returns"].mean()

# Scale for holding period
var_scaled = var_value * np.sqrt(holding_period)
cvar_scaled = cvar_value * np.sqrt(holding_period)

# Display summary
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Summary")
    st.markdown(f"- **Asset:** {asset_name}")
    st.markdown(f"- **Confidence Level:** {confidence_level}%")
    st.markdown(f"- **Holding Period:** {holding_period} day(s)")
    st.markdown(f"- **Value at Risk (VaR):** {var_scaled:.2%}")
    st.markdown(f"- **Expected Shortfall (CVaR):** {cvar_scaled:.2%}")

with col2:
    st.markdown("### Interpretation")
    st.caption(f"With {confidence_level}% confidence, losses are not expected to exceed "
               f"**{abs(var_scaled):.2%}** over a {holding_period}-day horizon.")
    st.caption(f"If this threshold is breached, the **expected shortfall** is approximately "
               f"**{abs(cvar_scaled):.2%}** — representing average loss beyond VaR.")

# Histogram and overlays
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=df["returns"] * 100,
    nbinsx=100,
    marker={"color": "lightblue"},
    name="Daily Returns",
    opacity=0.75
))

fig.add_vline(x=var_value * 100, line_width=2, line_color="red", line_dash="dash")
fig.add_vline(x=cvar_value * 100, line_width=2, line_color="orange", line_dash="dot")

fig.add_annotation(
    x=var_value * 100, y=0, yshift=20, showarrow=False,
    text=f"VaR: {var_value*100:.2f}%",
    font={"color": "red"}
)

fig.add_annotation(
    x=cvar_value * 100, y=0, yshift=40, showarrow=False,
    text=f"CVaR: {cvar_value*100:.2f}%",
    font={"color": "orange"}
)


fig.update_layout(
    title="Return Distribution with VaR & CVaR Overlays",
    xaxis_title="Return (%)",
    yaxis_title="Frequency",
    bargap=0.05
)

st.plotly_chart(fig, width='stretch')

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

st.markdown("---")
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
           "No trading, investment, or policy advice provided.")
