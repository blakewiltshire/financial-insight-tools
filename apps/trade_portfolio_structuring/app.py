# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------

"""
📈 Trade & Portfolio Structuring — Insight Launcher

Modular dashboard for managing trade workflows and post-trade portfolio diagnostics
within the Financial Insight Tools suite.

Unlike other launchers (e.g., 🌍 Economic Exploration), this app uses
**inline page transitions** via `st.switch_page()` — enabling seamless movement
between modules without launching subprocesses.

Purpose
Provide a cohesive launchpad for key trading and investment tools — from pre-trade
filters and risk structuring to post-trade review and analytics.

Key Features
- Inline module transitions (no subprocesses)
- Buttons for direct access to Trade Structuring, Timing, Review, and Scanner tools
- Structured layout and captions aligned with suite-wide UX
- Asset Snapshot Scanner included for quick performance reviews

Structure
- Main window navigation: buttons linked to `NN_🔠_Descriptive_Name.py`
- Markdown integration: About files from `/docs/about_<module>.md`
- Shared helpers: All modules share loaders, filters, and constants

User Considerations
- Single Streamlit session: fast transitions without window switching
- Ideal for end-to-end trade workflows in one tab
- For multi-window work, use 🚀 Financial Insight Tools launcher

Developer Notes
- All tools are self-contained and aligned with shared interface logic
- No sidebar navigation — all routing happens via main dashboard layout
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup — Adjust based on your module's location relative to the project root.
# Path to project root (level_up_2) — for markdown, branding, etc.
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    get_named_paths,
)
from core.theme import inject_global_styles
inject_global_styles()
# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_0"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_trade_structuring_portfolio.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below (Optional)
# These should be structured clearly by function:

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Trade & Portfolio Structuring", layout="wide")
st.title("📈 Trade & Portfolio Structuring")
st.caption(
    "*This launcher provides structured access to all modules within the "
    "Trade & Portfolio Structuring suite. "
    "From exploratory market tools and timing signals to structured trade planning and portfolio "
    "review, each component aligns with risk-aware, modular decision-making principles.*"
)

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------

# --- Branding ---
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member
# -------------------------------------------------------------------------------------------------
#
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------

# --- Getting Started, Branding Image and Caption ---
st.sidebar.markdown("### 🧭 Getting Started")
st.sidebar.caption("*Modular workflows for trade setup, risk planning, and performance review.*")

st.sidebar.info("""
**📈 Trade & Portfolio Structuring**

Navigate the full trade lifecycle — from pre-trade scans and timing confirmation
to structured execution and outcome review.

Launch each module directly using the main dashboard.
""")

# --- About & Support ---
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
            use_container_width=True,
        )

    with open(os.path.join(ROOT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# -------------------------------------------------------------------------------------------------
# Main Content
# -------------------------------------------------------------------------------------------------

# --- Load About Markdown (auto-skips if not replaced) ---
with st.expander("📖 About This App"):
    markdown_content = load_markdown_file(ABOUT_APP_MD)
    if markdown_content:
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_trade_structuring_portfolio.md'.")
st.divider()


# --- Section: Exploration & Market Scanning ---
st.header("📊 Exploration & Market Scanning")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔎 Market & Volatility Scanner")
    st.write("Scan markets for volatility, key moves, and pre-trade potential.")
    if st.button("🔎 Market & Volatility Scanner"):
        st.switch_page("pages/03_market_and_volatility_scanner.py")
    st.divider()

    st.markdown("### 📋 Asset Snapshot Scanner")
    st.write("Summarise metrics across asset categories.")
    if st.button("📋 Asset Snapshot Scanner"):
        st.switch_page("pages/04_asset_snapshot_generator.py")
    st.divider()

with col2:
    st.markdown("### ⏳ Trade Timing & Confirmation")
    st.write("Confirm timing signals and technical strength.")
    if st.button("⏳ Trade Timing & Confirmation"):
        st.switch_page("pages/05_trade_timing_and_confirmation.py")
    st.divider()

    st.markdown("### 📊 Price Action & Trend Confirmation")
    st.write("Reinforce trend logic through structure analysis.")
    if st.button("📊 Price Action & Trend Confirmation"):
        st.switch_page("pages/06_price_action_and_trend_confirmation.py")
    st.divider()

# --- Section: Trade Structuring & Planning ---
st.header("🛠 Trade Structuring & Planning")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🛠 Trade Structuring & Risk Planning")
    st.write("Build trades with sizing and margin logic.")
    if st.button("🛠 Trade Structuring & Risk Planning"):
        st.switch_page("pages/07_trade_structuring_and_risk_planning.py")
    st.divider()

with col2:
    st.markdown("### 📁 User Asset Manager")
    st.write("Inspect and snapshot your own datasets.")
    if st.button("📁 User Asset Manager"):
        st.switch_page("pages/08_user_asset_manager.py")
    st.divider()

# --- Section: Portfolio Review & Monitoring ---
st.header("📈 Portfolio & Trade Performance Review")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📘 Trade History & Strategy")
    st.write("Review, validate, and learn from past trades.")
    if st.button("📘 Trade History & Strategy"):
        st.switch_page("pages/09_trade_history_and_strategy.py")

with col2:
    st.markdown("### 🧭 Live Portfolio Monitor")
    st.write("Track current positioning and risk exposure.")
    if st.button("🧭 Live Portfolio Monitor"):
        st.switch_page("pages/10_live_portfolio_monitor.py")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
    investment, or policy advice provided."
)
