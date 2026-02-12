# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🛠 Toolbox & Calculators — Insight Launcher

Modular dashboard for launching standalone utilities that support strategy calibration,
position sizing, and risk framing.

Purpose
Provide fast access to targeted tools used throughout the system — for planning,
calibration, back-of-envelope checks, or supporting deeper workflows.

Key Features
- Ratio and spread analysis tools
- Position sizing (Kelly), VaR estimators, compounding simulations
- Data Cleaner and format inspection utility

Structure
- Button-driven layout using `st.switch_page()`
- Markdown loaded from `/docs/about_toolbox_calculators.md`
- Shared structure with other Insight Launchers (branding, footer)

User Considerations
- No external links or subprocesses — runs fully in one session
- Use when standalone calculations are required without launching other dashboards

Developer Notes
- Modular but non-navigational: no need for sidebar tree
- Works well as a utility companion to deeper workflow modules
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
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_toolbox_calculators.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below (Optional)
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Toolbox & Calculators", layout="wide")
st.title("🛠 Toolbox & Calculators")
st.caption(
"*Quick-access utilities for precision trade planning, risk evaluation, \
and structural financial analysis.*")

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
st.sidebar.caption(
"*Standalone tools for structuring, calibrating, and stress-testing financial decisions.*")

st.sidebar.info("""
**🛠 Toolbox & Calculators**

Access precision utilities for position sizing, compounding, VaR, and trade evaluation.

Each module operates independently, supporting structured inputs and exportable outputs.

Launch any calculator or utility from the main dashboard.
""")

# --- About & Support ---
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
        st.error("File not found: docs/about_toolbox_calculators.md")
st.divider()

# --- Modules ---

st.header("🔢 Position Sizing & Return Optimisation")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧠 Kelly Criterion Calculator")
    st.write("Estimate optimal bet sizing for expected value.")
    if st.button("🧠 Kelly Criterion Calculator"):
        st.switch_page("pages/14_kelly_criterion.py")

    st.markdown("### 📏 Break-Even Distance Calculator")
    st.write("Calculate the move needed to reach profitability.")
    if st.button("📏 Break-Even Distance Calculator"):
        st.switch_page("pages/15_break-even_distance_calculator.py")

with col2:
    st.markdown("### 💸 Compounding Calculator")
    st.write("Visualise the impact of recurring investment growth.")
    if st.button("💸 Compounding Calculator"):
        st.switch_page("pages/16_💸_compounding_calculator.py")

st.divider()

st.header("⚖️ Risk & Volatility Tools")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚠️ Value at Risk (VaR) Calculator")
    st.write("Quantify potential downside under normal conditions.")
    if st.button("⚠️ Value at Risk (VaR) Calculator"):
        st.switch_page("pages/17_var_calculator.py")

    st.markdown("### 📉 Standard Deviation Calculator")
    st.write("Evaluate variability for target or buffer setting.")
    if st.button("📉 Standard Deviation Calculator"):
        st.switch_page("pages/18_standard_deviation_calculator.py")

with col2:
    st.markdown("### 🛑 ATR-Based Stop Calculator")
    st.write("Calculate volatility-based stop-loss buffers.")
    if st.button("🛑 ATR-Based Stop Calculator"):
        st.switch_page("pages/19_atr_based_stop_calculator.py")

st.divider()

st.header("🔧 System Utilities & Data Tools")
col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🧼 Data Cleaner & Inspector")
    st.write("Upload and review financial data for errors.")
    if st.button("🧼 Data Cleaner & Inspector"):
        st.switch_page("pages/20_data_cleaner_and_inspector.py")

with col2:
    st.markdown("### 💱 Historical Data Currency Converter")
    st.write("Convert OHLC pricing to a consistent currency.")
    if st.button("💱 Launch Currency Converter"):
        st.switch_page("pages/21_historical_data_currency_converter.py")


# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
    investment, or policy advice provided."
)
