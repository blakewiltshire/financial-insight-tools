# -------------------------------------------------------------------------------------------------
# Observation & AI Export — Central Intelligence Hub
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Observation & AI Export — Central Intelligence Hub

This Streamlit application serves as the consolidated intelligence and workflow hub
for reviewing, bundling, and exporting structured macroeconomic observations and insights.

It integrates the following key components:

- Snapshot Browser: Explore saved macro snapshots with full metadata.
- Observation Browser: Review user-generated notes, matched to indicators.
- Manage Snapshots & Observations: Edit or delete previously saved insights.
- Build Export Bundle: Combine selected insights into an AI-ready JSON bundle.
- AI Prompt & Response: Compose structured AI prompts and save persona-aligned responses.
- Load / Restore: Upload, preview, and manage saved JSON/Markdown files.

Session state tracks active snapshot and observation bundles for export.

The module is part of the broader Financial Insight Tools framework — focused on
supporting decision-making through structured, modular, and context-aware workflows.
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
    get_named_paths
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
APPS_PATH = PATHS["level_up_1"]
APP_PATH = PATHS["level_up_0"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_observation_ai_export.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Observation Engine Module Path Setup
# Required for importing from apps/observation_engine inside app.py (located in observation_ai_export)
# -------------------------------------------------------------------------------------------------
OBS_ENGINE_PATH = os.path.join(APPS_PATH, "observation_engine")
if OBS_ENGINE_PATH not in sys.path:
    sys.path.append(OBS_ENGINE_PATH)

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below (Optional)
# These should be structured clearly by function:

from snapshot_browser_panel import render_snapshot_browser_panel
from observation_browser_panel import render_observation_browser_panel
from manage_observation_panel import render_manage_observations_panel
from manage_snapshot_panel import render_manage_snapshots_panel
from build_export_bundle_panel import render_build_export_bundle_panel
from ai_prompt_response_panel import render_ai_prompt_response_panel
from ai_file_manager_panel import render_load_restore_panel

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Observation & AI Export",
    page_icon="",
    layout="wide"
)
st.title("🧠 Observation & AI Export")
st.caption("")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_observation_ai_export.md")

# -------------------------------------------------------------------------------------------------
#  Sidebar — Global Settings or Filters
# -------------------------------------------------------------------------------------------------

 # --- Branding ---
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# --- Getting Started, Branding Image and Caption ---
st.sidebar.caption("*Consolidate your insights. Review, bundle, and export AI-ready snapshots "
"and observations.*")

# -------------------------------------------------------------------------------------------------
# Sidebar — Info
# -------------------------------------------------------------------------------------------------
st.sidebar.info("""
**Observation & AI Export Dashboard**

- **Snapshot Browser:** View saved macro snapshots with metadata.
- **Observation Browser:** Review notes and insights across modules.
- **Manage Snapshots / Observations:** Organise or remove saved entries.
- **Build Export Bundle:** Package insights into structured AI-ready files.
- **AI Prompt & Response:** Load personas and generate AI interactions.
- **Load / Restore:** Upload, preview, and manage saved files.

Designed as a modular workspace for structured insight and analysis.
""")

# -------------------------------------------------------------------------------------------------
# Initialise Session State for Bundling
# -------------------------------------------------------------------------------------------------
if "bundle_snapshots" not in st.session_state:
    st.session_state["bundle_snapshots"] = []

if "bundle_observations" not in st.session_state:
    st.session_state["bundle_observations"] = []

if "ai_bundle_current" not in st.session_state:
    st.session_state["ai_bundle_current"] = {}

# -------------------------------------------------------------------------------------------------
# Main Tab Navigation
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Snapshot Browser",          # 0 — Insight Browsing
    "Observation Browser",       # 1
    "Manage Snapshots",          # 2 — Insight Management
    "Manage Observations",       # 3
    "Build Export Bundle",       # 4 — Insight Operations
    "AI Prompt & Response",      # 5
    "Load / Restore"             # 6
])

# -------------------------------------------------------------------------------------------------
# Tab 0 — Snapshot Browser
# -------------------------------------------------------------------------------------------------
with tabs[0]:
    render_snapshot_browser_panel()

# -------------------------------------------------------------------------------------------------
# Tab 1 — User Observations
# -------------------------------------------------------------------------------------------------
with tabs[1]:
    render_observation_browser_panel()

# -------------------------------------------------------------------------------------------------
# Tab 2 — Manage Snapshots
# -------------------------------------------------------------------------------------------------
with tabs[2]:
    render_manage_snapshots_panel()

# -------------------------------------------------------------------------------------------------
# Tab 3 — Manage Observations
# -------------------------------------------------------------------------------------------------
with tabs[3]:
    render_manage_observations_panel()

# -------------------------------------------------------------------------------------------------
# Tab 4 — Build Export Bundle
# -------------------------------------------------------------------------------------------------
with tabs[4]:
    render_build_export_bundle_panel()

# -------------------------------------------------------------------------------------------------
# Tab 5 — AI Prompt & Response Interface
# -------------------------------------------------------------------------------------------------
with tabs[5]:
    render_ai_prompt_response_panel()

# -------------------------------------------------------------------------------------------------
# Tab 6 — Load / Restore Insight Bundles
# -------------------------------------------------------------------------------------------------
with tabs[6]:
    render_load_restore_panel()

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
