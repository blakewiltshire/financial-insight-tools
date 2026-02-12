# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📚 Reference Data & Trusted Sources — Insight Launcher

Central hub for accessing institutional-grade sources, classification systems,
and indicator metadata that support system-wide validation and contextual insight.

Purpose
Provide fast navigation to non-interactive data directories and structural inspection tools.

Key Modules
- Institutional Reference Directory
- Thematic Registry Explorer
- Classification Schema Viewer

Structure
- Button-driven layout using `st.switch_page()`
- Markdown support via `/docs/about_reference.md`
- Sidebar includes logo, support, and onboarding notes

User Considerations
- Designed for internal validation and research cross-referencing
- Optimised for reliability, not interactivity

Developer Notes
- Each submodule operates independently and loads via `/pages/`
"""
# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup — Adjust based on your module's location relative to the project root.
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
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_0"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_reference.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Reference Data & Trusted Sources", layout="wide")
st.title("📚 Reference Data & Trusted Sources")
st.caption("*Central hub for reliable data sources, theme mapping, and classification schemas.*")

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------

# --- Branding ---
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# --- Getting Started ---
st.sidebar.markdown("### 🧭 Getting Started")
st.sidebar.caption("*Institutional-grade reference support for validation, sourcing, \
and system architecture.*")

st.sidebar.info("""
**📚 Reference Data & Trusted Sources**

This launcher provides structured access to validated links, classification viewers,
and the internal thematic registry system used across the Financial Insight Tools suite.

Use this module to validate metadata, inspect mappings, and cross-reference official data sources.
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

with st.expander("📖 About This App"):
    markdown_content = load_markdown_file(ABOUT_APP_MD)
    if markdown_content:
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_reference.md")

st.divider()
st.header("📂 Launch Reference Modules")
col1, col2 = st.columns(2)

# --- Module 1 ---
with col1:
    st.markdown("### 📚 Institutional Reference Directory")
    st.write("Directory of market data platforms, regulators, and statistical portals.")
    if st.button("📚 Launch Institutional Directory"):
        st.switch_page("pages/22_institutional_reference_directory.py")

# --- Module 2 ---
with col2:
    st.markdown("### 📚 Classification Schema Viewer")
    st.write("Visualise economic/industry classification hierarchies.")
    if st.button("📚 Launch Classification Viewer"):
        st.switch_page("pages/23_classification_schema_viewer.py")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🧠 AI Persona Reference")
    st.write("Centralised repository of role definitions and exploration frameworks.")
    if st.button("🧠 AI Persona Reference"):
        st.switch_page("pages/24_ai_persona_reference.py")

with col2:
    st.markdown("### 🗂️ Index & Glossary Viewer")
    st.write("Alphabetical cross-reference of key concepts, terms, and chapter references.")
    if st.button("🗂️ Index & Glossary Viewer"):
        st.switch_page("pages/25_index_glossary_viewer.py")

st.divider()

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
investment, or policy advice provided."
)
