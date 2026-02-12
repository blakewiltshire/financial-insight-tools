# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🗂️ Index & Glossary Viewer

Alphabetical cross-reference of key concepts, terms, and chapter references across the
Blake Wiltshire — *Navigating the World of Economics, Finance, and Markets* series.

Purpose
- Provide a navigable, continuously updatable index/glossary module aligned to the guides.
- Support quick look-ups, cross-refs to chapters/sections, and related-term exploration.

Key Features
- Search (prefix/substring), A–Z quick filter, and term chips for related concepts.
- Chapter references rendered as compact chips (e.g., “Ch2 — Monetary Policy”).
- Inline dataset fallback + optional YAML source: /docs/index_glossary.yaml

Structure
- Non-interactive directory-style app; all outbound links open externally.
- Uses shared helpers (load_markdown_file, build_sidebar_links, get_named_paths).
- UI consistent with the Institutional Reference Directory (sidebar, branding, expanders).

Developer Notes
- Data model kept simple: { term: { "definition": str, "chapters": [..], "related": [..] } }
- To switch to a fully external source, populate /docs/index_glossary.yaml with the same schema.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys
import string
from typing import Dict, List

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

# Shared docs (optional)
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_index_glossary.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# YAML-backed reference catalogue
CATALOGUE_DIR = os.path.join(PROJECT_PATH, "docs", "catalogues")
DATA_YAML = os.path.join(CATALOGUE_DIR, "index_glossary.yaml")

# -------------------------------------------------------------------------------------------------
# Sample Dataset (fallback if YAML is not present)
# -------------------------------------------------------------------------------------------------
SAMPLE_TERMS: Dict[str, Dict[str, List[str]]] = {
    "Artificial Intelligence (AI)": {
        "definition": "Algorithmic methods used for pattern detection, forecasting, and workflow automation across research, execution, and risk functions.",
        "chapters": ["Ch2 — Central Banks & Monetary Policy", "Ch4 — Investment Services & Platforms", "Ch5 — Trading Mechanics"],
        "related": ["Algorithmic Trading", "Predictive Analytics", "Quant Research"],
    },
    "Asset Allocation": {
        "definition": "Framework for distributing capital across asset classes to balance risk, return, and liquidity constraints.",
        "chapters": ["Ch3 — Market Facilitation (context: asset services)", "Ch1 — Introduction (Risk & Diversification)"],
        "related": ["Diversification", "Risk Budget", "Rebalancing"],
    },
    "Central Banks": {
        "definition": "Monetary authorities responsible for price stability, liquidity, and financial system resilience via policy tools and market operations.",
        "chapters": ["Ch1 — Introduction (Foundations)", "Ch2 — Central Banks & Monetary Policy"],
        "related": ["Monetary Policy", "QE/QT", "Inflation Targeting"],
    },
    "Diversification": {
        "definition": "Risk management principle of spreading exposure across instruments, sectors, and geographies to reduce concentration risk.",
        "chapters": ["Ch1 — Introduction (Risk Management)", "Ch4 — Investment Services (portfolio tooling)"],
        "related": ["Asset Allocation", "Correlation", "Risk Parity"],
    },
    "Inflation": {
        "definition": "Generalised increase in the price level, influencing real returns, discount rates, and relative asset performance.",
        "chapters": ["Ch2 — Central Banks & Monetary Policy", "Ch5 — Trading Mechanics (market impact)"],
        "related": ["Interest Rates", "Real Yield", "Inflation Targeting"],
    },
    "Market Makers": {
        "definition": "Liquidity providers quoting two-way prices to support orderly markets and efficient price discovery.",
        "chapters": ["Ch5 — Trading Mechanics and Market Operations"],
        "related": ["Order Book", "Bid-Ask Spread", "Clearinghouses"],
    },
    "Order Types": {
        "definition": "Instructions governing how trades execute (e.g., market, limit, stop) under specified price and time conditions.",
        "chapters": ["Ch5 — Trading Mechanics and Market Operations"],
        "related": ["Execution", "Liquidity", "Slippage"],
    },
}

# -------------------------------------------------------------------------------------------------
# Data Loading
# -------------------------------------------------------------------------------------------------
def load_terms() -> Dict[str, Dict[str, List[str]]]:
    """Load terms from YAML if available, else fall back to SAMPLE_TERMS."""
    if yaml and os.path.exists(DATA_YAML):
        try:
            with open(DATA_YAML, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            # Basic schema guard
            if isinstance(data, dict):
                return data
        except Exception:  # pragma: no cover
            pass
    return SAMPLE_TERMS

TERMS = load_terms()
TERMS_NORMALISED = {k.strip(): v for k, v in TERMS.items()}

# -------------------------------------------------------------------------------------------------
# UI Helpers
# -------------------------------------------------------------------------------------------------
def render_term(term: str, payload: Dict[str, List[str]]):
    """Render a single term card."""
    definition = payload.get("definition", "").strip()
    chapters = payload.get("chapters", [])
    related = payload.get("related", [])

    st.markdown(f"#### **{term}**")
    if definition:
        st.write(definition)

    if chapters:
        st.markdown(
            " ".join([f"`{c}`" for c in chapters])
        )

    if related:
        st.caption("Related:")
        st.markdown(
            " ".join([f"[{r}](#)" for r in related])
        )

    st.divider()

def filter_terms(query: str, initial: str) -> List[str]:
    """Return sorted term list filtered by search and initial letter."""
    keys = list(TERMS_NORMALISED.keys())

    if initial and initial in string.ascii_uppercase:
        keys = [k for k in keys if k.upper().startswith(initial.upper())]

    if query:
        q = query.strip().lower()
        keys = [k for k in keys if q in k.lower() or q in TERMS_NORMALISED[k].get("definition","").lower()]

    return sorted(keys, key=str.lower)

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Index & Glossary Viewer", layout="wide")
st.title("🗂️ Index & Glossary Viewer")
st.caption("*Alphabetical cross-reference of key concepts, terms, and chapter references.*")

# Intro / About (optional markdown file; fall back to inline)
with st.expander("📖 About This Module", expanded=True):
    about = load_markdown_file(ABOUT_APP_MD)
    if about:
        st.markdown(about, unsafe_allow_html=True)
    else:
        st.markdown(
            "This viewer consolidates terms used across the series and companion tools. "
            "Entries link to chapters and adjacent concepts, supporting quick look-ups and deeper navigation."
        )

# Sidebar: nav + brand (mirrors your pattern)
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📚 Reference Data & Trusted Sources')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.info(
    """
**🗂️ Index & Glossary Viewer**

A consolidated reference for terms and structural concepts used across the
Financial Insight Tools (FIT) ecosystem and the *Navigating the World of
Economics, Finance, and Markets* series.

Provides alphabetical navigation, chapter links, and related concepts to support
contextual interpretation across guides and companion modules. Designed for
quick look-ups and structural framing — not advisory outcomes.
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

st.divider()

# -------------------------------------------------------------------------------------------------
# Controls (Search + A–Z filter)
# -------------------------------------------------------------------------------------------------
col1, col2 = st.columns([3, 2])
with col1:
    query = st.text_input("🔎 Search terms or definitions", placeholder="e.g., ‘inflation’, ‘order types’, ‘AI’")

with col2:
    letters = ["All"] + list(string.ascii_uppercase)
    initial = st.selectbox("Filter by letter", letters, index=0, key="filter_letter_select")
    initial = "" if initial == "All" else initial

# A–Z row of buttons (quick jump) — ensure unique keys
az_cols = st.columns(13)
for i, L in enumerate(string.ascii_uppercase):
    with az_cols[i // 2]:
        if st.button(L, key=f"az_{L}", use_container_width=True):
            initial = L

st.markdown("---")

# -------------------------------------------------------------------------------------------------
# Results
# -------------------------------------------------------------------------------------------------
results = filter_terms(query, initial)

if not results:
    st.info("No matching entries. Try a different letter or refine your search.")
else:
    st.caption(f"Showing **{len(results)}** entr{'y' if len(results)==1 else 'ies'}")
    for term in results:
        render_term(term, TERMS_NORMALISED[term])

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, "
    "investment, or policy advice provided."
)
