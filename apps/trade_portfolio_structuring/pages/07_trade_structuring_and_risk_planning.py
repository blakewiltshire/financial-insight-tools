# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught


# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Trade Structuring & Risk Planning App

Streamlit-based module for designing structured trade setups using preloaded or user-uploaded data.
Supports single-asset (Shares, CFDs, Spread Betting) and dual-asset (Pairs, Spreads)
strategies with modular calculators for intuitive position sizing, risk-reward structuring,
and dashboard integration.

Key Features:
- Load asset data from preloaded lists or user CSV uploads
- Apply dedicated calculators for different trade types
- Generate structured trade setups including sizing, stops, and targets
- Support multi-leg strategies (pairs, sector spreads)
- Export and review trade journals alongside dashboard outputs

Part of the Financial Insight Tools suite. Path resolution and modular utilities align with
the central project architecture for consistent cross-app support.

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
import pandas as pd

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
ROOT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_trade_structuring.md")
HELP_APP_MD = os.path.join(ROOT_PATH, "docs", "help_trade_structuring.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
SAMPLE_FILE = os.path.join(
APPS_PATH, "observation_engine", "sample_inputs", "sample_trade_journal.csv"
)

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# 🧠 Observation Tools (User Observation Logging — Group A)
# -------------------------------------------------------------------------------------------------
from observation_handler_trade_structuring import (
    observation_input_form,
    display_observation_log
)

from render_macro_interaction_tools_panel_trade_structuring import (
render_macro_interaction_tools_panel
)
from macro_insight_sidebar_panel_trade_portfolio_structuring import render_macro_sidebar_tools

# -------------------------------------------------------------------------------------------------
# Clean and format Asset Files
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_default import (
    load_data_from_file, clean_data
)

# -------------------------------------------------------------------------------------------------
# Mapping Logic
# -------------------------------------------------------------------------------------------------
from apps.data_sources.financial_data.preloaded_assets import get_preloaded_assets
from apps.data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from apps.data_sources.financial_data.asset_map import get_asset_path
from apps.data_sources.financial_data.user_asset_map import get_user_asset_path


# -------------------------------------------------------------------------------------------------
# Trade Strategy Calculators
# -------------------------------------------------------------------------------------------------
from trade_structuring_modules.calculators import (
    shares_calculator_intuitive,
    cfd_calculator,
    pairs_spread_calculator
)

# -------------------------------------------------------------------------------------------------
# Trade Dashboard
# -------------------------------------------------------------------------------------------------
from trade_structuring_modules.trade_dashboard import (
    add_trade_to_dashboard,
    display_trade_dashboard
)
# -------------------------------------------------------------------------------------------------
# Reminder: __init__.py
# Ensure all relevant folders (e.g., /helpers, /use_cases, /data_sources etc)
# contain an empty __init__.py file.
# This marks them as Python packages and allows import resolution (especially important when
# running via Streamlit or exporting to other Python environments).
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Trade Structuring & Risk Planning", layout="wide")
st.title("🛠 Trade Structuring & Risk Planning")
st.caption(
    "*Design setups using stop loss, entry, reward ratio, and capital allocation.*"
)

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("docs/about_trade_structuring.md")

# -------------------------------------------------------------------------------------------------
# Start Sidebar Operations
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📈 Trade and Portfolio Structuring')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Load and Manage Trade Journal
# -------------------------------------------------------------------------------------------------
SAMPLE_FILE = os.path.join(
    APPS_PATH, "observation_engine", "sample_inputs", "sample_trade_journal.csv"
)


st.sidebar.title("📂 Upload Trade Journal (Optional Reference)")
with st.sidebar.expander("📂 Optional Journal Reference Upload", expanded=False):
    st.markdown("""
    Upload a CSV file containing an external trade journal, idea tracker, or watchlist.

    This file is **not required** — it simply acts as a **reference table** alongside this module's structured dashboard.
    You can use it to:

    - Cross-reference external trade ideas
    - Track trades from other platforms or strategies
    - Annotate with reflections using the Macro Interaction Tools panel below

    **Accepted Format:** CSV, max 200MB. Key columns may include `Asset`, `Entry Date`, `Strategy`, `Notes`, etc.
    """)

uploaded_journal = st.sidebar.file_uploader("Upload Trade Journal (CSV)", type="csv")

use_sample = False
if uploaded_journal:
    try:
        journal_df = pd.read_csv(uploaded_journal)
    except Exception:
        st.error("❌ Could not read file. Please ensure it's a valid CSV.")
        journal_df = None
else:
    journal_df = pd.read_csv(SAMPLE_FILE)
    use_sample = True

if journal_df is not None:
    caption_msg = (
        "📋 Sample journal loaded — modify as needed to reflect strategic intent."
        if use_sample else
        "📋 Review and edit your journal — row highlights guide you through focused assets."
    )
    st.caption(caption_msg)

    with st.expander("📋 Trade Journal Editor"):
        edited_journal_df = st.data_editor(
            journal_df,
            width='stretch',
            num_rows="dynamic",
        )

        csv_download = edited_journal_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Updated Journal (CSV)",
            data=csv_download,
            file_name="updated_trade_journal.csv",
            mime="text/csv",
        )

# --- Trade type selection ---
st.sidebar.title("🔎 Select Trade Type")

trade_type = st.sidebar.selectbox("Select Trade Type", [
    "Shares (No Leverage)",
    "CFDs (Leverage Applied)",
    "Spread Betting (Leverage Applied)",
    "Pairs Trading (Mean Reversion)",
    "Multi-Leg Spread (Sector / Intermarket / Relative Strength)"
])

TRADE_TYPE_MESSAGES = {
    "Shares (No Leverage)": (
        "⚖️ A straightforward long-only position. No leverage, no margin — "
        "direct equity exposure."
        "Ideal for sizing via capital allocation and managing clear stop-loss boundaries."
    ),
    "CFDs (Leverage Applied)": (
        "⚠️ Leverage amplifies gains and losses. This mode supports both "
        "long and short positions."
        "Structural trade planning should account for margin requirements and risk tiering."
    ),
    "Spread Betting (Leverage Applied)": (
        "⚠️ Similar to CFDs, but taxed differently in some jurisdictions. Reward-to-risk "
        "ratios and stop levels "
        "should be framed in stake-per-point terms. Often used in retail trading environments."
    ),
    "Pairs Trading (Mean Reversion)": (
        "🔁 Involves simultaneously long and short positions on correlated assets. "
        "Strategy relies on price convergence. "
        "Key metrics: spread ratio, z-score, divergence, and correlation."
    ),
    "Multi-Leg Spread (Sector / Intermarket / Relative Strength)": (
        "📊 Complex trade structure involving multiple legs. Typically constructed to "
        "express sector rotation, "
        "intermarket relationships, or structural themes. Requires deeper diagnostics "
        "and spread analysis."
    )
}

# Display message below selectbox
selected_message = TRADE_TYPE_MESSAGES.get(trade_type)
if selected_message:
    st.sidebar.markdown(selected_message)

st.sidebar.markdown("**Categories adjust dynamically based on trade type selection.**")

# --- Load Assets ---
def load_asset(asset_label):
    """
    Loads asset data from either preloaded (default/user) or user-uploaded CSV.

    Returns:
        tuple: (asset_name, asset_category_or_type, cleaned_df)
    """
    source = st.sidebar.selectbox(
        f"{asset_label} Asset Source",
        ["Preloaded Asset Types (Default)", "Preloaded Asset Types (User)", "Upload CSV"],
        key=f"{asset_label}_source"
    )

    if source == "Upload CSV":
        uploaded_file_inner = st.sidebar.file_uploader(
            f"Upload {asset_label} Asset CSV", type="csv", key=f"{asset_label}_file")
        asset_name_input = st.sidebar.text_input(
            f"{asset_label} Asset Name", key=f"{asset_label}_name_text")
        asset_type_input = st.sidebar.selectbox(
            f"{asset_label} Asset Type",
            ["Equities", "Currencies", "Commodities", "Indices", "ETFs", "Crypto"],
            key=f"{asset_label}_asset_type_select"
        )
        if uploaded_file_inner:
            df_uploaded = load_data_from_file(uploaded_file_inner)
            df_uploaded, _ = clean_data(df_uploaded)
            return asset_name_input, asset_type_input, df_uploaded

    elif source.startswith("Preloaded Asset Types"):
        assets_dict = (
            get_preloaded_assets() if "Default" in source else get_user_preloaded_assets()
        )
        selected_category = st.sidebar.selectbox(
            f"{asset_label} Asset Category",
            list(assets_dict.keys()),
            key=f"{asset_label}_category"
        )
        selected_asset = st.sidebar.selectbox(
            f"{asset_label} Asset",
            list(assets_dict[selected_category].keys())
            if "User" in source else assets_dict[selected_category],
            key=f"{asset_label}_select"
        )
        if selected_asset and selected_asset != "Select":
            selected_path = (
                get_asset_path(selected_category, selected_asset)
                if "Default" in source else get_user_asset_path(selected_category, selected_asset)
            )
            df_selected = load_data_from_file(selected_path)
            df_selected, _ = clean_data(df_selected)
            return selected_asset, selected_category, df_selected

    return None, None, None

# --- Interpretation Guidance ---
with st.expander("ℹ️ Interpretation Guidance"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_trade_structuring.md")


# --- Pairs or Multi-Leg Spread setup ---
if trade_type in ["Pairs Trading (Mean Reversion)",
"Multi-Leg Spread (Sector / Intermarket / Relative Strength)"]:
    st.sidebar.subheader("Long Leg Setup")
    long_asset_name, long_asset_type, long_df = load_asset("Long")

    st.sidebar.subheader("Short Leg Setup")
    short_asset_name, short_asset_type, short_df = load_asset("Short")

    if long_df is not None and short_df is not None:
        last_long_price = long_df.iloc[-1]['close']
        last_short_price = short_df.iloc[-1]['close']

        st.sidebar.success(f"Loaded Long Asset: {long_asset_name} ({long_asset_type})")
        st.sidebar.success(f"Loaded Short Asset: {short_asset_name} ({short_asset_type})")

        structured_trade = pairs_spread_calculator(
            asset_name_long=long_asset_name,
            asset_name_short=short_asset_name,
            long_price=last_long_price,
            short_price=last_short_price,
            long_asset_type=long_asset_type,
            short_asset_type=short_asset_type
        )
        if structured_trade and st.button(
        f"➕ Add {long_asset_name} / {short_asset_name} Spread to Dashboard"):
            add_trade_to_dashboard(structured_trade)
    else:
        st.info("Please load both long and short legs to structure spread trades.")


# --- Single asset setups ---
else:
    data_source = st.sidebar.selectbox(
        "Choose Data Source",
        ["Preloaded Asset Types (Default)", "Preloaded Asset Types (User)", "Upload CSV"]
    )

    df_main, asset_name_main, asset_type_main = None, None, None

    if data_source == "Upload CSV":
        uploaded_file_main = st.sidebar.file_uploader("Upload CSV File", type="csv")
        asset_name_main = st.sidebar.text_input("Asset Name")
        asset_type_main = st.sidebar.selectbox(
            "Asset Type", ["Equities", "Currencies", "Commodities", "Indices", "ETFs", "Crypto"]
        )
        if uploaded_file_main:
            df_main = load_data_from_file(uploaded_file_main)
            df_main, _ = clean_data(df_main)

    elif data_source.startswith("Preloaded Asset Types"):
        preloaded_assets = (
            get_preloaded_assets() if "Default" in data_source else get_user_preloaded_assets()
        )

        if trade_type == "Shares (No Leverage)":
            filtered = [cat for cat in preloaded_assets if "Equities" in cat]
        elif trade_type in ["CFDs (Leverage Applied)", "Spread Betting (Leverage Applied)"]:
            filtered = [cat for cat in preloaded_assets if any(x in cat for x in [
                "Equities", "Market Indices", "Commodities", "Currencies", "ETFs", "Crypto"])]
        else:
            filtered = list(preloaded_assets.keys())

        asset_category_main = st.sidebar.selectbox("Select Category", filtered)
        asset_name_main = st.sidebar.selectbox(
            "Select Asset",
            list(preloaded_assets[asset_category_main].keys())
            if "User" in data_source else preloaded_assets[asset_category_main]
        )

        if asset_name_main and asset_name_main != "Select":
            asset_path_main = (
                get_user_asset_path(asset_category_main, asset_name_main)
                if "User" in data_source else get_asset_path(asset_category_main, asset_name_main)
            )
            df_main = load_data_from_file(asset_path_main)
            df_main, _ = clean_data(df_main)
            asset_type_main = asset_category_main

    if df_main is not None:
        last_close_price = df_main.iloc[-1]['close']  # Fetch last close price for any asset
        last_close_date = df_main.iloc[-1]['date']
        st.sidebar.success(f"Loaded {asset_name_main} ({asset_type_main})")
        st.sidebar.markdown(
        f"Date range: {df_main['date'].min().date()} ➡️ {df_main['date'].max().date()}"
        )
        st.sidebar.markdown(f"Total records: {len(df_main)}")
        st.sidebar.markdown(f"Trade Type: {trade_type}")

        # Apply logic for Shares, CFDs, Spread Betting
        if trade_type in [
            "Shares (No Leverage)",
            "CFDs (Leverage Applied)",
            "Spread Betting (Leverage Applied)"
        ]:
            is_share = trade_type == "Shares (No Leverage)"
            calc = shares_calculator_intuitive if is_share else cfd_calculator
            structured_trade = calc(asset_name_main, last_close_price, last_close_date)

            if structured_trade and st.button(
                f"➕ Add {asset_name_main} to Dashboard"
            ):
                add_trade_to_dashboard(structured_trade)

# --- Trade Structuring Dashboard Display ---
display_trade_dashboard()

st.divider()

# -------------------------------------------------------------------------------------------------
# 🧠 Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
theme_code = "trade_structuring"
theme_title = "Trade Structuring & Risk Planning"
selected_use_case = "Trade Structuring & Risk Planning Snapshot"

# -------------------------------------------------------------------------------------------------
# 🧠 Activate Observation + Journal Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case
)

# -------------------------------------------------------------------------------------------------
# 🎯 Derive Assets In View (Used for Logging Context)
# -------------------------------------------------------------------------------------------------
try:
    asset_list_for_observation = [asset_name_main] if asset_name_main else []
except NameError:
    asset_list_for_observation = []


if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")
    st.caption("*Use this section to record reasoning behind planned trades — including macro"
     "setup, risk considerations, technical alignment, or personal conviction before execution.*")


render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_indicators=asset_list_for_observation,
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

    with open(os.path.join(ROOT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            width='stretch',
        )

    with open(os.path.join(ROOT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
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
