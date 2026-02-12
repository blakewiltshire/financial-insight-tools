# -------------------------------------------------------------------------------------------------
# 🔀 Cross-Asset Correlation Module (Platinum Canonical Build with Full History)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# -------------------------------------------------------------------------------------------------
"""
Cross-Asset Correlation Module:
- Full multi-period comparative correlation
- Spread ratio dynamics
- Rolling correlation insights
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
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import numpy as np

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
# Use get_named_paths(__file__) to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
# Resolve Named Paths
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_cross_asset_correlation.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_cross_asset_correlation.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Data Sources
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))


from data_sources.financial_data.processing_default import (
    load_data_from_file, clean_data, resample_spread_data
)

from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# 🔗 Macro Interaction Tools — Sidebar + Observation Panel Integration
# -------------------------------------------------------------------------------------------------
from macro_insight_sidebar_panel_intermarket_correlation import render_macro_sidebar_tools
from render_macro_interaction_tools_panel_intermarket_correlation import render_macro_interaction_tools_panel
from observation_handler_cross_asset_correlation import (
    observation_input_form,
    display_observation_log
)

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Cross-Asset Correlation", layout="wide")
st.title("🔀 Cross-Asset Correlation")
st.caption("*Examine relationships between asset classes to support hedging logic, intermarket "
"strategy construction, or systemic signal validation.*")

with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🔗 Intermarket & Correlation')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()


st.logo(BRAND_LOGO_PATH)

# -------------------------------------------------------------------------------------------------
# Asset Ingestion Block (Canonical)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("🔎 Select Cross-Asset Pair")
data_source = st.sidebar.selectbox("Choose your data source", [
    "Preloaded Asset Types (Default)",
    "Preloaded Asset Types (User)",
    "Upload my own files"
])

df_long, df_short, long_asset, short_asset = None, None, None, None

if data_source == "Upload my own files":
    long_file = st.sidebar.file_uploader("Upload CSV for Asset 1", type="csv")
    short_file = st.sidebar.file_uploader("Upload CSV for Asset 2", type="csv")
    if long_file and short_file:
        raw_long = load_data_from_file(long_file)
        df_long, _ = clean_data(raw_long)
        raw_short = load_data_from_file(short_file)
        df_short, _ = clean_data(raw_short)
        long_asset = long_file.name
        short_asset = short_file.name
    else:
        st.stop()

elif data_source.startswith("Preloaded Asset Types"):
    is_user = "User" in data_source
    preloaded_assets = get_user_preloaded_assets() if is_user else get_preloaded_assets()

    long_category = st.sidebar.selectbox("Select Asset 1 Category", list(preloaded_assets.keys()))
    long_asset = st.sidebar.selectbox(
        "Select Asset 1",
        list(preloaded_assets[long_category].keys()) if is_user else preloaded_assets[long_category]
    )

    short_category = st.sidebar.selectbox("Select Asset 2 Category", list(preloaded_assets.keys()))
    short_asset = st.sidebar.selectbox(
        "Select Asset 2",
        list(preloaded_assets[short_category].keys()) if is_user else preloaded_assets[short_category]
    )

    if long_asset and short_asset:
        long_path = get_user_asset_path(
            long_category, long_asset) if is_user else get_asset_path(long_category, long_asset)
        short_path = get_user_asset_path(
            short_category, short_asset) if is_user else get_asset_path(short_category, short_asset)
        raw_long = load_data_from_file(long_path)
        df_long, _ = clean_data(raw_long)
        raw_short = load_data_from_file(short_path)
        df_short, _ = clean_data(raw_short)

# -------------------------------------------------------------------------------------------------
# Analysis Tabs
# -------------------------------------------------------------------------------------------------
if df_long is not None and df_short is not None:

    merged = pd.merge(
        df_long[["date", "close"]].rename(columns={"close": "close_long"}),
        df_short[["date", "close"]].rename(columns={"close": "close_short"}),
        on="date"
    )
    merged['Spread Ratio'] = merged['close_long'] / merged['close_short']
    merged['Correlation'] = merged['close_long'].rolling(30).corr(merged['close_short'])

    view_tabs = st.tabs([
        "Overview Summary",
        "📉 Short-Term (50 Days)",
        "📊 Medium-Term (200 Days)",
        "🕰 Full History",
        "ℹ️ Help: How to"
    ])

    with view_tabs[0]:
        st.markdown(f"**Data Range:** {merged['date'].min().date()} to {merged['date'].max().date()}")
        st.markdown(f"**Asset 1:** {long_asset}")
        st.markdown(f"**Asset 2:** {short_asset}")

    def compute_summary(slice_df):
        stats = {
            "Average Correlation (Full)": round(slice_df['close_long'].corr(slice_df['close_short']), 3),
            "Spread Ratio Mean": round(slice_df['Spread Ratio'].mean(), 4),
            "Spread Ratio Volatility": round(slice_df['Spread Ratio'].std(), 4),
            "Max Spread Ratio": round(slice_df['Spread Ratio'].max(), 4),
            "Min Spread Ratio": round(slice_df['Spread Ratio'].min(), 4),
        }
        spread_mean = slice_df['Spread Ratio'].mean()
        spread_std = slice_df['Spread Ratio'].std()
        deviation = (slice_df.iloc[-1]['Spread Ratio'] - spread_mean) / spread_std
        stats["Deviation from Mean (Z-Score)"] = round(deviation, 2)
        return stats

    for tab, label, data_slice, key_suffix in zip(
        view_tabs[1:],
        ["Short-Term", "Medium-Term", "Full History"],
        [merged.tail(50), merged.tail(200), merged],
        ["short", "medium", "full"]
    ):
        with tab:
            summary = compute_summary(data_slice)
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"### Summary Statistics ({label})")
                for key, val in summary.items():
                    st.write(f"**{key}:** {val}")
            with col2:
                st.write(f"### Rolling Correlation ({label})")
                fig_corr = go.Figure()
                fig_corr.add_trace(go.Scatter(
                    x=data_slice['date'],
                    y=data_slice['Correlation'],
                    mode="lines",
                    name="Rolling Correlation"
                ))
                fig_corr.update_layout(
                    xaxis_title="Date", yaxis_title="Correlation",
                    yaxis=dict(range=[-1, 1]), template="plotly_white"
                )
                st.plotly_chart(fig_corr, use_container_width=True, key=f"plot_corr_{key_suffix}")

            st.write(f"### Spread Ratio Over Time ({label})")
            fig_spread = go.Figure()
            fig_spread.add_trace(go.Scatter(
                x=data_slice['date'],
                y=data_slice['Spread Ratio'],
                mode="lines",
                name="Spread Ratio"
            ))
            fig_spread.update_layout(
                xaxis_title="Date", yaxis_title="Spread Ratio", template="plotly_white"
            )
            st.plotly_chart(fig_spread, use_container_width=True, key=f"plot_spread_{key_suffix}")

    with view_tabs[4]:
        content = load_markdown_file(HELP_APP_MD)
        if content:
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.warning("Help file not found.")

else:
    st.warning("Please select or upload valid assets for analysis.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Macro Interaction Setup
# -------------------------------------------------------------------------------------------------
theme_code = "cross_asset_correlation"
theme_title = "Cross-Asset Correlation"
selected_use_case = "Cross-Asset Correlation Snapshot"

# -------------------------------------------------------------------------------------------------
# 🔍 Sidebar Activation Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case
)

# -------------------------------------------------------------------------------------------------
# 🧠 Macro Interaction Tools
# -------------------------------------------------------------------------------------------------
if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")

# Prepare selected indicators from user input
selected_indicators = [long_asset, short_asset] if long_asset and short_asset else []

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_themes=[theme_title],
    selected_indicators=selected_indicators,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

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



st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools — No trading, investment, or policy advice provided.")
