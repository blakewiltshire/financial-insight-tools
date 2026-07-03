# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Reference & Investigation Resources — Insight Launcher

Central hub for accessing institutional-grade sources, classification systems, reference manager
and indicator metadata that support system-wide validation and contextual insight.

Purpose
Provide fast navigation to non-interactive data directories and structural inspection tools.

Key Modules
- - Reference Manager
- Classification Schema Viewer
- Institutional Reference Directory
- AI Persona Reference
- Index & Glossary Viewer

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
st.set_page_config(page_title="Reference & Investigation Resources", layout="wide")
st.title("📚 Reference & Investigation Resources")
st.caption("*Supporting resources for expanding observations, organising candidate assets, \
validating information, and maintaining analytical consistency.*")

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------

# --- Branding ---
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# --- Getting Started ---
st.sidebar.caption("*Supporting resources for structured investigation and analytical consistency.*")

st.sidebar.info("""
**Reference & Investigation Resources**

This launcher provides the supporting resources used throughout Financial Insight Tools.

Use these modules to:

- expand observations into candidate assets
- organise investigations through structured classifications
- validate information using institutional sources
- maintain consistent terminology and analytical perspectives

These resources support investigation before market examination and AI-assisted reflection.
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

with st.expander("ℹ️ About This App"):
    markdown_content = load_markdown_file(ABOUT_APP_MD)
    if markdown_content:
        st.markdown(markdown_content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_reference.md")

st.space()

# --- Modules ---
col1, col2 = st.columns(2, gap="small")

with col1:
    with st.container(border=True):
        st.markdown("### Relationship Manager")
        st.write(
            "Expand observations into relationship themes and candidate assets for further investigation."
        )
        if st.button("Launch Relationship Manager"):
            st.switch_page("pages/25_relationship_manager.py")

with col2:
    with st.container(border=True):
        st.markdown("### Classification Schema Viewer")
        st.write(
            "Organise candidate assets using market, sector, industry, and company classification frameworks."
        )
        if st.button("Launch Classification Schema Viewer"):
            st.switch_page("pages/26_classification_schema_viewer.py")

col1, col2 = st.columns(2, gap="small")

with col1:
    with st.container(border=True):
        st.markdown("### Institutional Reference Directory")
        st.write(
            "Validate investigations using institutional market data, regulators, and official statistical sources."
        )
        if st.button("Launch Institutional Directory"):
            st.switch_page("pages/27_institutional_reference_directory.py")

with col2:
    with st.container(border=True):
        st.markdown("### AI Persona Reference")
        st.write(
            "Explore structured analytical perspectives for reviewing investigations through different professional lenses."
        )
        if st.button("AI Persona Reference"):
            st.switch_page("pages/28_ai_persona_reference.py")

col1, col2 = st.columns(2, gap="small")

with col1:
    with st.container(border=True):
        st.markdown("### Index & Glossary")
        st.write(
            "Shared terminology, concepts, and cross-references used throughout Financial Insight Tools."
        )
        if st.button("Index & Glossary"):
            st.switch_page("pages/29_index_glossary.py")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.space()
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
investment, or policy advice provided."
)
