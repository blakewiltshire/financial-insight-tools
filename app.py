# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🚀 Financial Insight Tools — Start Launcher

Entry point for launching all core dashboards within the Financial Insight Tools suite.

🔹 Purpose
Acts as the central hub for launching modular decision-support dashboards covering \
macroeconomic analysis,
trading workflows, and portfolio tools. Designed for users managing multiple analytic \
workflows in parallel.

🔹 What This App Does
- Presents buttons to launch each module in a separate Streamlit subprocess
- Loads shared branding and markdown dynamically from `/brand/`, `/docs/`, and `/images/`
- Acts as the gateway for cross-module orchestration and UX continuity

🔹 Structure
- **Navigation:** Launches each app externally using `launch_streamlit_app()`
- **Assets:** Uses shared markdown and brand folders for UI consistency
- **Data Flow:** Each app handles its own logic independently — no shared data across subprocesses

🔹 User Considerations
- Each dashboard opens in a new window (multi-app workflows supported)
- Keep this launcher open for fast re-entry into other dashboards

🔹 Developer Notes
- Structured via a `MODULES` list with buttons and paths to `apps/*/app.py`
- Fail-safe error handling supports graceful exits for missing files or launch conflicts
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os

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
    render_module_dashboard,
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
ROOT_PATH = PATHS["level_up_0"]  # Previously PROJECT_BASE_PATH

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
IMAGE_PATH = os.path.join(ROOT_PATH, "images", "fit.png")
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_platform.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title=" Financial Insight Tools - Start Here", layout="wide")
st.title("Financial Insight Tools")
st.caption("*This unified launcher provides structured access to all core modules within the \
Financial Insight Tools system. It supports context-aware analysis across \
macroeconomic signals, asset structuring, intermarket relationships, and modular trade \
and portfolio workflows — grounded in disciplined, risk-aware decision flow.*")

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
# --- Branding ---
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member



if os.path.isfile(IMAGE_PATH):
    st.sidebar.image(IMAGE_PATH, width='stretch')

# --- Quick Overview ---
st.sidebar.markdown("### 🧭 Getting Started")
st.sidebar.caption("*Structure | Analyse | Decide – Trading, Investing, and Macroeconomics*")

# --- Introductory Note ---
st.sidebar.info(
    "Each module launches in a new window. Keep this launcher open for quick access to the full suite."
)

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
with st.expander("📖 About This Platform"):
    markdown_content = load_markdown_file(ABOUT_APP_MD)
    if markdown_content:
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_platform.md")
st.divider()

# --- Modules ---
MODULES = [
    {
        "title": "🌍 Economic Exploration",
        "description": "Country-level macro dashboards, thematic navigation",
        "path": os.path.join(ROOT_PATH, "apps", "economic_exploration"),
        "filename": "app.py",
        "button": "🌍 Launch Economic Exploration",
        "column": 1,
    },

    {
        "title": "📈 Trade & Portfolio Structuring",
        "description": "Full trade lifecycle from asset filtering to post-trade review",
        "path": os.path.join(ROOT_PATH, "apps", "trade_portfolio_structuring"),
        "filename": "app.py",
        "button": "📈 Launch Trading & Investing Suite",
        "column": 2,
    },
    {
        "title": "🔗 Intermarket & Correlation",
        "description": "Explore cross-asset, cross-theme, and macro–market relationships",
        "path": os.path.join(ROOT_PATH, "apps", "intermarket_correlation"),
        "filename": "app.py",
        "button": "🔗 Launch Intermarket and Correlation Dashboard",
        "column": 1,
    },
    {
        "title": "🛠 Toolbox & Calculators",
        "description": "Standalone utilities (position sizing, spread ratios, pip value, etc.)",
        "path": os.path.join(ROOT_PATH, "apps", "toolbox_calculators"),
        "filename": "app.py",
        "button": "🛠 Open Toolbox & Calculators",
        "column": 1,
    },
        {
        "title": "🧠 Observation & AI Export",
        "description": "Capture observations, tag context, and export AI-ready insight bundles.",
        "path": os.path.join(ROOT_PATH, "apps", "observation_ai_export"),
        "filename": "app.py",
        "button": "🧠 Launch Observation & AI Export",
        "column": 2,
    },

    {
        "title": "📚 Reference Data & Trusted Sources",
        "description": "Centralised hub for reliable data sources and guides.",
        "path": os.path.join(ROOT_PATH, "apps", "reference_data"),
        "filename": "app.py",
        "button": "📚 View Reference Data & Sources",
        "column": 2,
    },
]

# --- Render Module Dashboard ---
render_module_dashboard(MODULES, ROOT_PATH)

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
# st.markdown("---")
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
    investment, or policy advice provided."
)
