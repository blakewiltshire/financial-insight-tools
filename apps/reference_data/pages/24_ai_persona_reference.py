# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🧠 AI Persona Reference Guide

Centralised catalogue of role-based AI personas used in the Blake Wiltshire —
Navigating the World of Economics, Finance, and Markets Series.

Purpose
- Provide a reference list of personas with descriptions, focus areas, and exploration contexts.
- Support the 🔺 Triangular Navigation Program by giving users neutral, role-based scaffolds.
- Aligns with Appendix C (static snapshots) but continuously updated via this tool.

Key Features
- Search bar and A–Z filter for persona names.
- Displays definition, use case focus, and related domains.
- Optional YAML source (/docs/ai_personas.yaml) with inline fallback dataset.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys
import string
from typing import Dict, List, Any

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st  # type: ignore
try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # type: ignore
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_ai_personas_fit.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# YAML-backed reference catalogue
CATALOGUE_DIR = os.path.join(PROJECT_PATH, "docs", "catalogues")
DATA_YAML = os.path.join(CATALOGUE_DIR, "ai_personas.yaml")

# -------------------------------------------------------------------------------------------------
# Sample Dataset (fallback if YAML is not present) — includes perspective_frame
# -------------------------------------------------------------------------------------------------
SAMPLE_PERSONAS: Dict[str, Dict[str, List[str] | str]] = {
    "Behavioural Economist by Blake Wiltshire": {
        "definition": "Explores psychological and cognitive drivers of market behaviour, including biases, heuristics, and sentiment effects.",
        "focus": ["Market psychology", "Decision framing", "Behavioural finance"],
        "related": ["Investor Sentiment", "Market Cycles"],
        "perspective_frame": (
            "As a Behavioural Economist, interpret the insight bundle through the lens of cognitive bias, "
            "herding behaviour, and systemic feedback loops. Highlight framing effects and behavioural asymmetries."
        ),
    },
    "Quantitative Analyst by Blake Wiltshire": {
        "definition": "Applies statistical, mathematical, and model-based techniques to interpret markets and assess risk-return trade-offs.",
        "focus": ["Statistical modelling", "Algorithm design", "Risk metrics"],
        "related": ["Predictive Analytics", "Volatility Models"],
        "perspective_frame": (
            "As a Quantitative Analyst, analyse the bundle statistically. Identify distributions, volatility clusters, "
            "and correlation structures. Emphasise probability framing and model interpretation."
        ),
    },
    "Portfolio Manager by Blake Wiltshire": {
        "definition": "Focuses on asset allocation, diversification, and balancing risk-return objectives across multi-asset portfolios.",
        "focus": ["Diversification", "Rebalancing", "Strategic allocation"],
        "related": ["Asset Allocation", "Risk Management"],
        "perspective_frame": (
            "As a Portfolio Manager, assess the insight bundle in terms of diversification, risk allocation, "
            "and portfolio rebalancing. Identify rotation or regime-shift signals."
        ),
    },
    "Risk Analyst by Blake Wiltshire": {
        "definition": "Analyses exposures, scenarios, and stress tests to mitigate financial and systemic risks.",
        "focus": ["Scenario modelling", "Counterparty risk", "Stress testing"],
        "related": ["VaR", "Scenario Simulator"],
        "perspective_frame": (
            "As a Risk Analyst, evaluate the bundle for volatility sources, downside scenarios, and fragility indicators. "
            "Emphasise scenario testing and stress conditions."
        ),
    },
    "FinTech Innovator by Blake Wiltshire": {
        "definition": "Explores digital assets, blockchain, and AI applications in modern finance.",
        "focus": ["Blockchain", "AI", "Payments innovation"],
        "related": ["CBDCs", "Tokenisation"],
        "perspective_frame": (
            "As a FinTech Innovator, interpret the bundle from a digital-system perspective. Identify opportunities for "
            "automation, AI integration, or structural efficiency."
        ),
    },
    "Regulatory Advisor by Blake Wiltshire": {
        "definition": "Frames questions around compliance, oversight, and navigating evolving regulatory structures.",
        "focus": ["Policy frameworks", "Market conduct", "Compliance structures"],
        "related": ["Regulation", "Central Banks"],
        "perspective_frame": (
            "As a Regulatory Advisor, review the bundle for compliance, oversight, and governance implications. "
            "Highlight transparency gaps, jurisdictional constraints, and disclosure signals."
        ),
    },
    "Fundamental Analyst by Blake Wiltshire": {
        "definition": "Interprets company financials, sector dynamics, and valuation metrics to assess intrinsic value.",
        "focus": ["Balance sheets", "Cash flows", "Earnings drivers"],
        "related": ["Valuation", "Equity Research"],
        "perspective_frame": (
            "As a Fundamental Analyst, interpret the bundle using balance-sheet, earnings, and cash-flow perspectives. "
            "Highlight valuation drivers, quality metrics, and financial resilience factors."
        ),
    },
    "Value Investor by Blake Wiltshire": {
        "definition": "Frames margin of safety, durability of cash flows, and valuation anchors across cycles.",
        "focus": ["Unit economics", "Cash flow durability", "Valuation anchors"],
        "related": ["Quality factors", "Stewardship"],
        "perspective_frame": (
            "As a Value Investor, provide a structured analysis focused on intrinsic value, margin of safety, "
            "and fundamental signals within the insight bundle. Highlight long-term sustainability and valuation anchors."
        ),
    },
    "Economic Systems Architect by Blake Wiltshire": {
        "definition": "Designs structural framings of economic models, governance systems, and institutional scaffolds.",
        "focus": ["System design", "Macro frameworks", "Institutional structure"],
        "related": ["CFF", "Data contracts"],
        "perspective_frame": (
            "As an Economic Systems Architect, evaluate the insight bundle as part of a modular decision-support framework. "
            "Map data flows, integration layers, and systemic dependencies. Emphasise architecture, scalability, and "
            "interoperability within the DSS environment."
        ),
    },
}

# -------------------------------------------------------------------------------------------------
# Data Loading & Normalisation
# -------------------------------------------------------------------------------------------------
def _chip_html(text: str) -> str:
    """Return inert 'chip' HTML (neutral, non-clickable)."""
    safe = str(text).replace("|", "¦")
    return (
        "<span style='display:inline-block;padding:4px 8px;margin:2px;"
        "border:1px solid #e5e7eb;border-radius:9999px;font-size:12px;"
        "color:#374151;background:#ffffff;'>"
        f"{safe}</span>"
    )

def load_personas_yaml(path: str) -> Dict[str, Any]:
    """Load YAML file if available and valid, else return empty dict."""
    if not yaml:
        return {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            if isinstance(data, dict):
                return data
        except Exception:  # pragma: no cover
            return {}
    return {}

def build_registry() -> List[Dict[str, Any]]:
    """
    Produce a unified list of persona dicts with a superset schema:
    - name, icon, short_description, definition, focus, related
    - behaviour, avoid, starters, gpt, prompt_template_key, perspective_frame (optional)
    """
    data = load_personas_yaml(DATA_YAML)
    if "personas" in data and isinstance(data["personas"], list):
        return data["personas"]

    # Fallback to SAMPLE_PERSONAS → normalise to the superset schema
    registry: List[Dict[str, Any]] = []
    for name, payload in SAMPLE_PERSONAS.items():
        registry.append({
            "name": name,
            "icon": payload.get("icon", ""),
            "short_description": payload.get("short_description", ""),
            "definition": payload.get("definition", ""),
            "focus": payload.get("focus", []),
            "related": payload.get("related", []),
            "behaviour": payload.get("behaviour", ""),
            "avoid": payload.get("avoid", []),
            "starters": payload.get("starters", []),
            "gpt": payload.get("gpt", {}),
            "prompt_template_key": payload.get("prompt_template_key", name),
            "perspective_frame": payload.get("perspective_frame", ""),
        })
    return registry

REGISTRY: List[Dict[str, Any]] = build_registry()

# -------------------------------------------------------------------------------------------------
# UI Helpers
# -------------------------------------------------------------------------------------------------
def render_persona(card: Dict[str, Any]) -> None:
    """Render a single persona card with neutral, non-leading presentation."""
    name = card.get("name", "Unnamed Persona")
    icon = card.get("icon", "")
    short_desc = card.get("short_description", "")
    definition = card.get("definition", "")
    focus = card.get("focus", []) or []
    related = card.get("related", []) or []
    behaviour = (card.get("behaviour") or "").strip()
    avoid = card.get("avoid", []) or []
    starters = card.get("starters", []) or []
    gpt_meta = card.get("gpt", {}) or {}

    st.markdown(f"#### {icon} **{name}**" if icon else f"#### **{name}**")
    if short_desc:
        st.write(short_desc)
    if definition:
        st.caption(definition)

    if focus:
        st.markdown("**Focus Areas:**")
        st.markdown(" ".join(_chip_html(x) for x in focus), unsafe_allow_html=True)

    if related:
        st.markdown("**Related:**")
        st.markdown(" ".join(_chip_html(x) for x in related), unsafe_allow_html=True)

    if behaviour:
        st.markdown("**How this perspective behaves**")
        st.write(behaviour)

    if avoid:
        st.markdown("**Avoid**")
        st.markdown("- " + "\n- ".join(str(a) for a in avoid))

    if starters:
        with st.expander("Conversation starters"):
            for s in starters:
                st.markdown(f"- {s}")

    # Optional: show perspective frame if present (read-only)
    op_prompt = (card.get("perspective_frame") or "").strip()
    if op_prompt:
        with st.expander("Perspective frame (optional)"):
            st.code(op_prompt, language="text")

    if gpt_meta:
        with st.expander("GPT metadata"):
            st.json(gpt_meta)

    st.divider()

def filter_registry(query: str, initial: str) -> List[Dict[str, Any]]:
    """Return filtered & sorted persona list by search and initial."""
    def matches(p: Dict[str, Any]) -> bool:
        if not query:
            return True
        hay = " ".join([
            p.get("name", ""),
            p.get("short_description", ""),
            p.get("definition", ""),
            " ".join(p.get("focus", []) or []),
            " ".join(p.get("related", []) or []),
        ]).lower()
        return query.lower().strip() in hay

    items = REGISTRY[:]
    if initial and initial in string.ascii_uppercase:
        items = [p for p in items if p.get("name", "").upper().startswith(initial.upper())]
    items = [p for p in items if matches(p)]
    return sorted(items, key=lambda x: x.get("name", "").lower())

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="AI Persona Reference Guide", layout="wide")
st.title("🧠 AI Persona Reference Guide")
st.caption("*Role definitions and contextual exploration scaffolds.*")

# Intro / About
with st.expander("📖 About This Module", expanded=True):
    about = load_markdown_file(ABOUT_APP_MD)
    if about:
        st.markdown(about, unsafe_allow_html=True)
    else:
        st.markdown(
            "This module catalogues AI Personas — structured role-based framings used "
            "across guides and the 🔺 Triangular Navigation Program. "
            "They support neutral, non-advisory exploration by offering perspectives, "
            "not prescriptions."
        )

# Sidebar (mirrors your pattern)
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📚 Reference Data & Trusted Sources')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.info(
    """
**🧠 AI Persona Reference (FIT)**

This module provides neutral, role-based analytical framings used across the
Financial Insight Tools and the *Navigating the World of Economics, Finance,
and Markets* guide series.

Personas support structured exploration — not predictions or investment advice.
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
            width='stretch',
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width='stretch',
        )

st.markdown("---")

# -------------------------------------------------------------------------------------------------
# Controls
# -------------------------------------------------------------------------------------------------
col1, col2 = st.columns([3, 2])
with col1:
    query = st.text_input("🔎 Search personas or definitions", placeholder="e.g., ‘Risk Analyst’, ‘FinTech’")
with col2:
    letters = ["All"] + list(string.ascii_uppercase)
    initial = st.selectbox("Filter by letter", letters, index=0, key="persona_filter_letter_select")
    initial = "" if initial == "All" else initial

# A–Z row (non-leading quick filter) — unique keys per button
az_cols = st.columns(13)
for i, L in enumerate(string.ascii_uppercase):
    with az_cols[i // 2]:
        if st.button(L, key=f"persona_az_{L}", width='stretch'):
            initial = L

st.markdown("---")

# -------------------------------------------------------------------------------------------------
# Results
# -------------------------------------------------------------------------------------------------
results = filter_registry(query, initial)
if not results:
    st.info("No matching personas. Try a different letter or refine your search.")
else:
    st.caption(f"Showing **{len(results)} persona{'s' if len(results)!=1 else ''}**")
    for card in results:
        render_persona(card)

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
    "Neutral scaffolds for exploration — not advice."
)
