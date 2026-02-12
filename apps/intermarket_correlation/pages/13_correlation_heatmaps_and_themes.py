# -------------------------------------------------------------------------------------------------
# 🔀 Correlation Heatmaps & Themes (Platinum Canonical Build with Full Fixes)
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import altair as alt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
# -------------------------------------------------------------------------------------------------
# Resolve Named Paths
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_correlation_heatmaps_and_themes.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_correlation_heatmaps.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Data Sources
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

from data_sources.financial_data.processing_correlation import (
    load_asset_data, load_data_from_file, clean_data
)
from data_sources.financial_data.shared_utils import convert_date_to_us_format
from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path

from use_cases.correlation_charting import (
    generate_correlation_heatmap,
    plot_pairwise_scatter,
    plot_rolling_correlation
)

# -------------------------------------------------------------------------------------------------
# 🔗 Macro Interaction Tools — Sidebar + Observation Panel Integration
# -------------------------------------------------------------------------------------------------
from macro_insight_sidebar_panel_intermarket_correlation import render_macro_sidebar_tools
from render_macro_interaction_tools_panel_intermarket_correlation import render_macro_interaction_tools_panel
from observation_handler_correlation_heatmaps import (
    observation_input_form,
    display_observation_log
)

# -------------------------------------------------------------------------------------------------
# Streamlit Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Correlation Heatmaps & Themes", layout="wide")
st.title("🔀 Correlation Heatmaps & Themes")
st.caption("*Explore asset class interrelationships, cross-market correlations, and thematic co-movement structures.*")

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
# Data Ingestion and Source Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.title("🔎 Select Correlation Data Group")
data_source = st.sidebar.selectbox("Choose data source", [
    "Preloaded Asset Types (Default)",
    "Preloaded Asset Types (User)",
    "Upload my own files"
])

preloaded_assets_default = get_preloaded_assets()
preloaded_assets_user = get_user_preloaded_assets()
correlation_df = None

def load_group_assets(asset_category, source_type):
    all_data = []
    if source_type == 'Preloaded Asset Types (Default)':
        assets = preloaded_assets_default[asset_category]
        for asset in assets:
            path = get_asset_path(asset_category, asset)
            df = load_data_from_file(path, "Interday", None)
            df.rename(columns={'close': asset}, inplace=True)
            all_data.append(df[['date', asset]])
    elif source_type == 'Preloaded Asset Types (User)':
        assets = list(preloaded_assets_user[asset_category].keys())
        for asset in assets:
            path = get_user_asset_path(asset_category, asset)
            df = load_data_from_file(path, "Interday", None)
            df.rename(columns={'close': asset}, inplace=True)
            all_data.append(df[['date', asset]])
    if not all_data:
        return None
    merged = all_data[0]
    for df in all_data[1:]:
        merged = pd.merge(merged, df, on='date', how='inner')
    return merged

if data_source == 'Preloaded Asset Types (Default)':
    asset_category = st.sidebar.selectbox("Select Asset Category", list(preloaded_assets_default.keys()))
    correlation_df = load_group_assets(asset_category, data_source)

elif data_source == 'Preloaded Asset Types (User)':
    asset_category = st.sidebar.selectbox("Select Asset Category", list(preloaded_assets_user.keys()))
    correlation_df = load_group_assets(asset_category, data_source)

elif data_source == 'Upload my own files':
    uploaded_files = st.sidebar.file_uploader("Upload multiple CSV files", type="csv", accept_multiple_files=True)
    all_data = []
    for file in uploaded_files:
        try:
            df = pd.read_csv(file, converters={1: lambda x: float(str(x).replace(',', ''))})
            df.rename(columns={df.columns[1]: file.name}, inplace=True)
            df = df[['Date', file.name]].rename(columns={'Date': 'date'})
            df['date'] = pd.to_datetime(df['date'])
            all_data.append(df)
        except Exception as e:
            st.warning(f"File '{file.name}' could not be processed: {e}")
    if all_data:
        merged = all_data[0]
        for df in all_data[1:]:
            merged = pd.merge(merged, df, on='date', how='inner')
        correlation_df = merged

# -------------------------------------------------------------------------------------------------
# Date Range Filtering
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📅 Select Date Range")
if correlation_df is not None:
    correlation_df['date'] = pd.to_datetime(correlation_df['date'])
    min_date, max_date = correlation_df['date'].min().date(), correlation_df['date'].max().date()
    start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
    filtered_df = correlation_df[(correlation_df['date'] >= pd.to_datetime(start_date)) &
                                  (correlation_df['date'] <= pd.to_datetime(end_date))].copy()
else:
    filtered_df = None

# -------------------------------------------------------------------------------------------------
# Main Correlation Analysis
# -------------------------------------------------------------------------------------------------
if filtered_df is not None and len(filtered_df.columns) > 2:

    st.subheader("📑 Correlation Summary Insights")
    corr_matrix = filtered_df.drop(columns=["date"]).corr()

    avg_corr = round(((corr_matrix.values.sum() - len(corr_matrix)) / (len(corr_matrix)**2 - len(corr_matrix))), 3)

    if avg_corr >= 0.75:
        label, msg = "🚩 High Co-Movement", "High internal clustering — synchronized asset movement."
    elif avg_corr >= 0.5:
        label, msg = "⚠️ Moderate Co-Movement", "Noticeable systemic overlap — partial synchronization."
    elif avg_corr >= 0.25:
        label, msg = "🟠 Some Dispersal", "Partial differentiation present — some asset coupling remains."
    else:
        label, msg = "✅ Strong Dispersion", "Broad cross-asset variation — systemic sensitivity is low."

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Average Correlation:**", avg_corr)
        st.write("**Systemic Co-Movement:**", label)
        st.caption(f"**Interpretation:** {msg}")

    corr_pairs = corr_matrix.unstack().reset_index()
    corr_pairs.columns = ['Asset X', 'Asset Y', 'Correlation']
    corr_pairs = corr_pairs[corr_pairs['Asset X'] != corr_pairs['Asset Y']]
    corr_pairs.drop_duplicates(subset=['Correlation'], inplace=True)

    top_pairs = corr_pairs.sort_values('Correlation', ascending=False).head(5)
    bottom_pairs = corr_pairs.sort_values('Correlation', ascending=True).head(5)

    with col2:
        st.write("**Top Positive Correlations:**")
        st.table(top_pairs[['Asset X', 'Asset Y', 'Correlation']])
        st.write("**Top Inverse Correlations:**")
        st.table(bottom_pairs[['Asset X', 'Asset Y', 'Correlation']])

    tab1, tab2, tab3, tab4 = st.tabs(["📉 Pairwise Scatter", "📈 Rolling Correlation", "🔲 Full Heatmap", "ℹ️ Help: How to"])

    with tab1:
        asset_columns = list(filtered_df.columns)
        asset_columns.remove("date")
        col_x, col_y = st.columns(2)
        asset_x = col_x.selectbox("Select Asset X", asset_columns)
        asset_y = col_y.selectbox("Select Asset Y", asset_columns, index=1 if len(asset_columns) > 1 else 0)
        scatter = plot_pairwise_scatter(filtered_df, asset_x, asset_y)
        st.plotly_chart(scatter, use_container_width=True, key="scatter")

    with tab2:
        window = st.slider("Rolling Window", min_value=10, max_value=100, value=30, step=5)
        rolling_chart = plot_rolling_correlation(filtered_df.set_index('date')[asset_x],
                                                  filtered_df.set_index('date')[asset_y], window)
        st.altair_chart(rolling_chart, use_container_width=True)

    with tab3:
        heatmap = generate_correlation_heatmap(corr_matrix)
        st.altair_chart(heatmap, use_container_width=True)

    with tab4:
        st.subheader("ℹ️ How to read these summaries and charts")
        help_content = load_markdown_file(HELP_APP_MD)
        if help_content:
            st.markdown(help_content, unsafe_allow_html=True)
        else:
            st.info("Help documentation not yet populated.")

else:
    st.warning("Please load valid data with at least two assets to compute correlation.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Define Theme Metadata Before Use
# -------------------------------------------------------------------------------------------------
theme_code = "correlation_heatmaps"
theme_title = "Correlation Heatmaps & Themes"
selected_use_case = "Correlation Heatmap Snapshot"

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

# Derive final asset list for observation logging
if filtered_df is not None:
    asset_list_for_observation = [col for col in filtered_df.columns if col != "date"]
else:
    asset_list_for_observation = []

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_themes=[theme_code],
    selected_indicators=asset_list_for_observation,
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
