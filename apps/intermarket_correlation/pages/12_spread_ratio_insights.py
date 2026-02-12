# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name
# pylint: disable=non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🔁 Spread & Ratio Insights Module

Part of the Financial Insight Tools DSS.

This module allows users to evaluate long-short relationships between two assets using
spread ratio dynamics, historical correlation, volatility, and mean reversion analysis.

Key Functions:
- Load paired asset data from default, user, or uploaded CSV sources.
- Calculate and chart spread ratio over Daily, Weekly, Monthly timeframes.
- Identify high/low spread extremes, support/resistance zones, and deviation from
historical mean.
- Support trade idea validation before formal structuring in the
Trade Structuring & Risk Planning module.

This module does not perform execution planning — it informs and supports decision context.
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import scipy.signal
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
# Resolve Named Paths
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_spread_and_pairs_analysis.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_spread_and_pairs_analysis.md")
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
from observation_handler_spread_ratio_insights import (
    observation_input_form,
    display_observation_log
)

# -------------------------------------------------------------------------------------------------
# Streamlit Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Spread & Ratio Insights", layout="wide")
st.title("⚖️ Spread & Ratio Insights")
st.caption("*Analyse pairwise asset relationships, spread dynamics, mean reversion signals, and historical ratio behaviour.*")

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
# Spread Ratio Calculation
# -------------------------------------------------------------------------------------------------
def compute_spread_ratio(long_df, short_df):
    spread_df = pd.merge(
        long_df[["date", "close"]].rename(columns={"close": "close_long"}),
        short_df[["date", "close"]].rename(columns={"close": "close_short"}),
        on="date"
    )
    spread_df['Spread Ratio'] = spread_df['close_long'] / spread_df['close_short']
    return spread_df

# -------------------------------------------------------------------------------------------------
# Sidebar Operations
# -------------------------------------------------------------------------------------------------
st.sidebar.title("🔎 Select Long and Short Assets")
data_source = st.sidebar.selectbox("Choose your data source", [
    "Preloaded Asset Types (Default)",
    "Preloaded Asset Types (User)",
    "Upload my own files"
])

df_long, df_short, df = None, None, None
long_asset, short_asset = None, None

# Upload Mode
if data_source == "Upload my own files":
    long_file = st.sidebar.file_uploader("Upload CSV for Long Asset", type="csv")
    short_file = st.sidebar.file_uploader("Upload CSV for Short Asset", type="csv")
    if long_file and short_file:
        df_long, _ = clean_data(load_data_from_file(long_file))
        df_short, _ = clean_data(load_data_from_file(short_file))
        long_asset = long_file.name
        short_asset = short_file.name
        df = compute_spread_ratio(df_long, df_short)
    else:
        st.info("Please upload both Long and Short asset CSV files.")
        st.stop()

# Preloaded Mode
elif data_source.startswith("Preloaded Asset Types"):
    is_user = "User" in data_source
    preloaded_assets = get_user_preloaded_assets() if is_user else get_preloaded_assets()

    long_category = st.sidebar.selectbox("Select Long Asset Category", list(preloaded_assets.keys()))
    long_asset = st.sidebar.selectbox(
        "Select Long Asset",
        list(preloaded_assets[long_category].keys()) if is_user else preloaded_assets[long_category]
    )

    short_category = st.sidebar.selectbox("Select Short Asset Category", list(preloaded_assets.keys()))
    short_asset = st.sidebar.selectbox(
        "Select Short Asset",
        list(preloaded_assets[short_category].keys()) if is_user else preloaded_assets[short_category]
    )

    if long_asset and short_asset:
        long_path = get_user_asset_path(long_category, long_asset) if is_user else get_asset_path(long_category, long_asset)
        short_path = get_user_asset_path(short_category, short_asset) if is_user else get_asset_path(short_category, short_asset)
        df_long, _ = clean_data(load_data_from_file(long_path))
        df_short, _ = clean_data(load_data_from_file(short_path))
        df = compute_spread_ratio(df_long, df_short)

# -------------------------------------------------------------------------------------------------
# Main Analysis Block
# -------------------------------------------------------------------------------------------------
if df is not None:

    st.sidebar.title("Performance Analysis")
    periods_slider = st.sidebar.slider("Compare over past X periods", min_value=1, max_value=30, value=7)

    view_tabs = st.tabs(["Views (Daily / Weekly / Monthly)", "📉 Short-Term (50 Days)", "📊 Medium-Term (200 Days)", "ℹ️ Help: How to"])

    with view_tabs[0]:
        st.markdown(f"**Data range:** {df['date'].min().date()} to {df['date'].max().date()}")
        st.markdown(f"**Long Asset:** {long_asset}")
        st.markdown(f"**Short Asset:** {short_asset}")
        st.markdown(f"**Periods under analysis:** {periods_slider} periods")

    def generate_combined_spread_summary(spread_df):
        stats = {
            "Average Spread Ratio": round(spread_df['Spread Ratio'].mean(), 4),
            "Max Spread Ratio": round(spread_df['Spread Ratio'].max(), 4),
            "Min Spread Ratio": round(spread_df['Spread Ratio'].min(), 4),
            "Volatility (Std Dev)": round(spread_df['Spread Ratio'].std(), 4),
            "Correlation (Long vs Short)": round(spread_df['close_long'].corr(spread_df['close_short']), 4)
        }
        spread_mean = spread_df['Spread Ratio'].mean()
        spread_std = spread_df['Spread Ratio'].std()
        deviation = (spread_df.iloc[-1]['Spread Ratio'] - spread_mean) / spread_std
        readiness = {
            "Deviation from Mean (Z-Score)": f"{deviation:.2f}",
            "Support Levels": [round(val, 4) for val in spread_df['Spread Ratio'].nsmallest(2).tolist()],
            "Resistance Levels": [round(val, 4) for val in spread_df['Spread Ratio'].nlargest(2).tolist()]
        }
        return {**stats, **readiness}

    def performance_message(observed):
        if observed > 0:
            return "green", "Spread expanded over the selected period."
        if observed < 0:
            return "red", "Spread contracted over the selected period."
        return "orange", "Spread remained stable with no significant movement."

    with view_tabs[0]:
        tabs = st.tabs(["Daily View", "Weekly View", "Monthly View"])

        for timeframe, tab in zip(["Daily", "Weekly", "Monthly"], tabs):
            with tab:
                col1, col2, _ = st.columns([2, 2, 0.5])
                slice_data = resample_spread_data(df.copy(), timeframe)
                combined_summary = generate_combined_spread_summary(slice_data)

                with col1:
                    st.write(f"### Summary Statistics & Readiness ({timeframe})")
                    for key, val in combined_summary.items():
                        st.write(f"**{key}:** {val}")

                with col2:
                    entry_spread = slice_data.iloc[-(periods_slider + 1)]['Spread Ratio']
                    current_spread = slice_data.iloc[-1]['Spread Ratio']
                    returns = slice_data['Spread Ratio'].pct_change().tail(periods_slider).multiply(100).tolist()
                    compounded_product = np.prod([(1 + r/100) for r in returns])
                    observed_movement = (current_spread / entry_spread - 1) * 100
                    expected_movement = (compounded_product - 1) * 100
                    drift = observed_movement - expected_movement

                    st.write(f"### Spread Performance ({timeframe})")
                    st.write(f"**Entry Spread:** {entry_spread:.6f}")
                    st.write(f"**Current Spread:** {current_spread:.6f}")
                    st.write(f"**Observed Movement:** {observed_movement:.2f}%")
                    st.write(f"**Expected Change (compounded):** {expected_movement:.2f}%")
                    st.write(f"**Drift (unexpected deviation):** {drift:.2f}%")

                    color, message = performance_message(observed_movement)
                    st.markdown(f"<span style='color:{color}'><b>{message}</b></span>", unsafe_allow_html=True)

                    slice_data["Direction"] = slice_data["Spread Ratio"].diff().apply(lambda x: "↑" if x > 0 else "↓")
                    slice_data['date'] = pd.to_datetime(slice_data['date']).dt.date
                    st.dataframe(slice_data[['date', 'close_long', 'close_short', 'Spread Ratio', 'Direction']].tail(periods_slider).reset_index(drop=True))

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=slice_data["date"], y=slice_data["Spread Ratio"], mode='lines', name="Spread Ratio"))
                fig.update_layout(title=f"{timeframe} Spread Ratio Chart", xaxis_title="Date", yaxis_title="Spread Ratio")
                st.plotly_chart(fig, use_container_width=True, key=f"spread_{timeframe}")

    # Help Tab
    with view_tabs[3]:
        st.subheader("How to Read These Summaries and Charts")
        content = load_markdown_file(HELP_APP_MD)
        if content:
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.warning("Help file not found.")

    # Final support/resistance analysis
    def create_high_low_markers_ratio(spread_df):
        if "Spread Ratio" not in spread_df.columns or spread_df["Spread Ratio"].dropna().empty:
            return None
        df_valid = spread_df.dropna(subset=["Spread Ratio"])
        if df_valid.empty:
            return None
        try:
            max_idx = df_valid['Spread Ratio'].idxmax()
            min_idx = df_valid['Spread Ratio'].idxmin()
            return (
                go.Scatter(x=[df_valid.loc[max_idx, 'date']], y=[df_valid.loc[max_idx, 'Spread Ratio']],
                           mode="markers", marker={"color": "purple", "size": 10}, name="Highest"),
                go.Scatter(x=[df_valid.loc[min_idx, 'date']], y=[df_valid.loc[min_idx, 'Spread Ratio']],
                           mode="markers", marker={"color": "orange", "size": 10}, name="Lowest")
            )
        except (KeyError, IndexError, ValueError):
            return None

    def detect_ratio_support_resistance(spread_df):
        df_temp = spread_df.copy().reset_index()
        peaks, _ = scipy.signal.find_peaks(df_temp['Spread Ratio'], distance=5)
        troughs, _ = scipy.signal.find_peaks(-df_temp['Spread Ratio'], distance=5)
        support_levels = df_temp.loc[troughs, 'Spread Ratio'].sort_values().head(2).tolist()
        resistance_levels = df_temp.loc[peaks, 'Spread Ratio'].sort_values(ascending=False).head(2).tolist()
        return support_levels, resistance_levels

    short_term, medium_term = df.tail(50), df.tail(200)
    for tab, timeframe, data_slice, key_suffix in zip(
        view_tabs[1:], ["Short-Term", "Medium-Term"], [short_term, medium_term], ["short", "medium"]
    ):
        with tab:
            st.subheader(f"Spread Ratio Over Time - {timeframe}")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_slice["date"], y=data_slice["Spread Ratio"], mode='lines', name="Spread Ratio"))
            markers = create_high_low_markers_ratio(data_slice)
            if markers:
                fig.add_trace(markers[0])
                fig.add_trace(markers[1])
            fig.update_layout(xaxis_title="Date", yaxis_title="Spread Ratio")
            st.plotly_chart(fig, use_container_width=True, key=f"main_chart_{key_suffix}")
            supports, resistances = detect_ratio_support_resistance(data_slice)
            st.info(f"📌 Detected Support Levels: {supports} | Resistance Levels: {resistances}")
            st.caption("High/Low markers use purple (high) and orange (low) for neutrality.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Macro Interaction Setup
# -------------------------------------------------------------------------------------------------
theme_code = "spread_ratio_insights"
theme_title = "Spread & Ratio Insights"
selected_use_case = "Spread & Ratio Structure Snapshot"

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
