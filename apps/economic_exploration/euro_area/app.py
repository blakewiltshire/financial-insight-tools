# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order, no-name-in-module

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📍 Country-Level App Launcher — Insight Explorer
Modular access to macroeconomic themes by country and topic.
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
from PIL import Image

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    get_named_paths,
    build_sidebar_links,
    get_parent_path,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APP_PATH = PATHS["level_up_0"]
IMAGE_PARENT_PATH = get_parent_path(APP_PATH, levels_up=1)

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_economic_exploration_launcher.md")
HOWTO_APP_MD = os.path.join(PROJECT_PATH, "docs", "howto_economic_exploration_launcher.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------
from constants.emoji import FLAGS  # pylint: disable=import-error
from constants.page_icon import PAGE_ICONS  # pylint: disable=import-error

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------

# --- Config ---
COUNTRY_NAME = "Euro Area" # Add country name, e.g. United States
THEME = "insight_launcher" # Add the image name of the theme, remove file extension, e.g. .png
FLAG = FLAGS.get(COUNTRY_NAME, "🏳️")
PAGE_ICON = PAGE_ICONS.get(THEME, "❓")

# --- Streamlit Setup ---
st.set_page_config(
    page_title=f"{COUNTRY_NAME} — {THEME.replace('_', ' ').title()}",
    page_icon=PAGE_ICON,
    layout="wide"
)

# --- Header ---
st.header(f"{FLAG} {COUNTRY_NAME} – Insight Launcher: Economic Exploration")
st.caption("*Country-level macro insights organised by theme, signal type, and \
systemic relevance.*")


# --- Info Panel ---
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_economic_exploration_launcher.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Configuration
# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------

# --- Branding ---
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# --- Sidebar Title ---
st.sidebar.title(f"{FLAG} {COUNTRY_NAME} — Thematic Explorer")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()


# --- About & Support ---
with st.sidebar.expander("ℹ️ About & Support"):
    content = load_markdown_file(ABOUT_SUPPORT_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_and_support.md")

# -------------------------------------------------------------------------------------------------
# Main Content
# -------------------------------------------------------------------------------------------------
#  -- Load How-T0 --
content = load_markdown_file(HOWTO_APP_MD)
if content:
    st.markdown(content, unsafe_allow_html=True)
else:
    st.error("File not found: docs/howto_economic_exploration_launcher.md")

#  -- Admin Info --
st.info("""
**Admin Note:**
Add or update thematic analysis files by editing files in the /pages directory.
Use a numerical prefix for ordering and include a clear theme or indicator name.
""")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire \
— No trading, investment, or policy advice provided.")
