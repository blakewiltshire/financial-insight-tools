# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📚 Institutional Reference Directory

Structured directory of verified sources, regulatory bodies, statistical authorities,
and classification frameworks relevant to economic research, market analysis,
and institutional reporting.

Purpose
Offer a consistent and curated reference point for external data, standards,
and documentation across the Financial Insight Tools environment.

Key Sections
- Market Data & Financial Platforms
- Regulatory and Supervisory Bodies
- Industry Classifications and Identifiers
- Statistical and Government Agencies
- Global Research Portals and Benchmarks

Structure
- Displayed in logical groups via expanders
- Backed by YAML catalogue: docs/institutional_references.yaml
- All links open externally — no API or scraping logic

User Considerations
- Use to cross-reference data sources, validate identifiers, or find regulators
- Optimised for click-through efficiency (not in-app interaction)

Developer Notes
- Non-interactive: no data processing, uploads, or filters
- UI can be enhanced with images or doc-link icons if needed
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
import streamlit as st
import yaml

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_institutional_reference.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# YAML-backed reference catalogue
CATALOGUE_DIR = os.path.join(PROJECT_PATH, "docs", "catalogues")
DATA_YAML = os.path.join(CATALOGUE_DIR, "institutional_references.yaml")



# -------------------------------------------------------------------------------------------------
# Data Loading Helpers
# -------------------------------------------------------------------------------------------------
def load_reference_data(yaml_path: str):
    """
    Load the institutional references catalogue from YAML.

    Expected structure: list of entries, each with:
    - id
    - group_key
    - group_label
    - sort_order
    - name
    - url
    - description
    - is_core
    - tags
    """
    if not os.path.exists(yaml_path):
        return []

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
            if isinstance(data, list):
                return data
            return data.get("items", [])
    except Exception:  # pylint: disable=broad-except
        return []


def render_reference_group(data, group_key: str):
    """
    Render a bullet list for a given group_key from the reference catalogue.
    """
    if not data:
        st.markdown(
            "_No reference entries are currently loaded from the YAML catalogue. "
            "Check `docs/institutional_references.yaml` for configuration._"
        )
        return

    entries = [e for e in data if e.get("group_key") == group_key]
    if not entries:
        st.markdown(
            "_No entries found for this category in `institutional_references.yaml`._"
        )
        return

    entries = sorted(entries, key=lambda x: x.get("sort_order", 0))

    lines = []
    for entry in entries:
        name = entry.get("name", "").strip()
        url = entry.get("url", "").strip()
        description = entry.get("description", "").strip()

        if not name or not url:
            continue

        if description:
            lines.append(f"- [**{name}**]({url}) —  {description}")
        else:
            lines.append(f"- [**{name}**]({url})")

    if lines:
        st.markdown("\n\n".join(lines))
    else:
        st.markdown("_No valid reference entries available for this category._")


# Load catalogue once at module import
REFERENCE_DATA = load_reference_data(DATA_YAML)

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Institutional Reference Directory", layout="wide")
st.title("📚 Institutional Reference Directory")
st.caption(
    "*Central hub for accessing validated financial datasets, research links, and "
    "trusted sources supporting analysis and system workflows.*"
)

# Optional: top-level warning if YAML not found or empty
if not REFERENCE_DATA:
    st.warning(
        "No entries loaded from `docs/institutional_references.yaml`. "
        "Update the YAML file to populate this directory."
    )

# -------------------------------------------------------------------------------------------------
# Info Panels
# -------------------------------------------------------------------------------------------------
with st.expander("📘 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_institutional_reference.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📚 Reference Data & Trusted Sources')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.info(
    """
**📚 Reference Data & Trusted Sources**

This module provides curated access to global market data platforms, economic institutions,
and financial classification systems.

All links open externally — ideal for validation, sourcing identifiers, or augmenting research
with institutional-grade inputs.
"""
)

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

# -------------------------------------------------------------------------------------------------
# Main Content
# -------------------------------------------------------------------------------------------------

st.divider()

# --- Section: Market Data & Financial Information ---
with st.expander("📈 Market Data and Financial Information"):
    render_reference_group(REFERENCE_DATA, "market_data")

# --- Regulatory Bodies ---
with st.expander("⚖️ Regulatory Bodies and Classifications"):
    render_reference_group(REFERENCE_DATA, "regulators")

# --- Market Status & Credit Evaluation Authorities ---
with st.expander("🏛️ Market Status & Credit Evaluation Authorities"):
    render_reference_group(REFERENCE_DATA, "market_status")

# --- Educational Platforms ---
with st.expander("📚 Educational Platforms and Financial Tools"):
    render_reference_group(REFERENCE_DATA, "education")

# --- Industry Reports and Research Portals ---
with st.expander("🌎 Industry Reports and Research Portals"):
    render_reference_group(REFERENCE_DATA, "research")

# --- Statistical Agencies ---
with st.expander("📊 Government and Statistical Agencies"):
    render_reference_group(REFERENCE_DATA, "statistics")

# --- International Organizations ---
with st.expander("🌐 International Organisations"):
    render_reference_group(REFERENCE_DATA, "international")

# --- Standards and Identifiers ---
with st.expander("🆔 Standards, Identifiers & Classification Systems"):
    st.markdown("#### Financial Identifiers")
    render_reference_group(REFERENCE_DATA, "identifiers")

    st.markdown("#### Classification Systems & Industry Benchmarks")
    render_reference_group(REFERENCE_DATA, "classifications")

    st.markdown("#### Market Capitalisation Classification Frameworks")
    render_reference_group(REFERENCE_DATA, "market_caps")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, "
    "investment, or policy advice provided."
)
