# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🔗 Intermarket & Correlation — Insight Launcher

Modular dashboard for analysing cross-asset relationships, macro linkages, and volatility dynamics
within the Financial Insight Tools suite.

Purpose
To facilitate exploration of how financial assets, economic signals, and thematic spreads interact
across timeframes — enabling structured diagnostics, comparative overlays, and volatility-based
filtering.

Key Features
- Structured navigation to submodules covering macro–asset overlays, cross-asset pairings,
spreads, and correlation matrices
- Statistical diagnostics including Pearson/Spearman correlations, z-scores, lag analysis,
and volatility comparisons
- Visual workflows for thematic heatmaps, inter-asset grids, and macro consistency checks

Structure
- Modules accessed via the main window using `st.switch_page()` (no sidebar navigation)
- Markdown and branding loaded from shared directories (`/docs`, `/brand`)
- Page resolution based on `NN_🔠_Descriptive_Name.py` format for consistency

User Considerations
- All tools run inside the same Streamlit instance for unified correlation analysis
- Supports pre-configured use cases and custom comparisons
- For simultaneous cross-module workflows, launch via the 🚀 Financial Insight Tools entry point

Developer Notes
- Pages are fully self-contained and interoperable via shared helper utilities
- Future enhancements may include AI tagging, signal logging, or dynamic indicator templates
- Ideal for analysts exploring inter-market dynamics without committing to full trade
structuring flows
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
from core.helpers import (  # pylint: disable=import-error
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
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_intermarket_correlation.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below (Optional)
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Intermarket & Correlation Dashboard", layout="wide")
st.title("🔗 Intermarket & Correlation Dashboard")
st.caption("*This launcher supports structured comparison of asset behaviour across macro "
"signals, themes, and markets. Modules focus on intermarket flow, cross-asset correlation, and "
"relationship diagnostics to enhance systemic awareness and strategy alignment.*")

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------

# --- Branding ---
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------

# --- Getting Started, Branding Image and Caption ---
st.sidebar.markdown("### 🧭 Getting Started")
st.sidebar.caption("*Cross-market relationships, regime shifts, and volatility interplay.*")

st.sidebar.info("""
**🔗 Intermarket & Correlation**

Analyse relationships between assets, indicators, and macro variables.

Modules include cross-asset correlation, macro-to-market overlays,
spread and ratio analysis, and correlation heatmaps.

Use the main dashboard to explore each section interactively.
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
# Main Content
# -------------------------------------------------------------------------------------------------

# --- Load About Markdown (auto-skips if not replaced) ---
with st.expander("📖 About This App"):
    markdown_content = load_markdown_file(ABOUT_APP_MD)
    if markdown_content:
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_intermarket_correlation.md")
st.divider()

# --- Modules ---
st.header("📂 Module Sections")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔀 Cross-Asset Correlation")
    st.write("Explore correlation strength between asset classes.")
    if st.button("🔄 Explore Cross-Asset Correlations"):
        st.switch_page("pages/11_cross_asset_correlation.py")
    st.divider()

    st.markdown("### 🗺️ Correlation Heatmaps & Themes")
    st.write("Visualise multi-asset correlation matrices by theme.")
    if st.button("🌐 View Heatmaps & Macro Themes"):
        st.switch_page("pages/12_correlation_heatmaps_and_themes.py")
    st.divider()

with col2:
    st.markdown("### ⚖️ Spread & Ratio Insights")
    st.write("Analyse relative pricing across instruments and themes.")
    if st.button("🧮 Launch Spread & Ratio Analysis"):
        st.switch_page("pages/13_spread_ratio_insights.py")
    st.divider()

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
    investment, or policy advice provided."
)
