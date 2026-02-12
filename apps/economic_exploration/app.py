# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order, no-name-in-module

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🌍 Economic Exploration — Insight Launcher

Modular geographic interface to explore country-specific economic dashboards
within the Financial Insight Tools system.

This module acts as the central dispatcher for launching individual
country dashboards, using a region → subregion → country selection structure
with an optional interactive map overlay.

Purpose
Enable country-level access to macroeconomic themes and dashboards via a structured,
regionally organised interface. Supports visual navigation, dynamic launching,
and reusable country app logic.

Key Features
- Interactive map and dropdowns for region → subregion → country selection
- Local app launching via subprocess (`launch_streamlit_app()`)
- Centralised access to modular economic themes by geography
- Dynamic loading of branding and support markdown assets

Structure
- Region and coordinates data: `/constants/regions.py`
- Path resolution: `core.helpers.get_named_paths(__file__)`
- Country launch logic: `run_country_app()` looks for `app.py` or `[country_name].py`
- About and support markdown: loaded from `/docs/`

User Considerations
- Each country app opens in a **new window**
- Keep this dashboard open to relaunch or navigate across countries

Developer Notes
- Scalable by default: just add new folders for countries under `/apps/`
- Works with any country-specific app that matches filename conventions
- Lightweight and non-analytical — this launcher is structural only
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys # Used for dynamic path handling before top-level imports

# -------------------------------------------------------------------------------------------------

# Path Setup — Adjust based on your module's location relative to the project root.
# Path to project root (level_up_2) — for markdown, branding, etc.
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import folium
from streamlit_folium import st_folium # Needed after sys.path is resolved

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    get_named_paths,
    launch_streamlit_app
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
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_economic_exploration.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
# IMAGE_PATH = os.path.join(ROOT_PATH, "images", "toolbox_app2.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------
from constants.regions import regions, country_coordinates  # pylint: disable=import-error

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup

# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Economic Exploration", layout="wide")
st.title("🌍 Economic Exploration")
st.caption("*Navigate country-level macro dashboards and thematic economic indicators \
through a structured lens.*")

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

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("🛠 Configuration & Setup")
st.sidebar.page_link("pages/01_economic_setup_and_registry_manager.py", label="Setup & Registry Manager")
st.sidebar.caption("📦 Add countries and themes using structured configuration and validation tools.")

st.sidebar.title("🔍 Exploratory Extensions")
st.sidebar.page_link("pages/02_thematic_correlation_explorer.py", label="Thematic Correlation Explorer")
st.sidebar.caption("📊 Explore cross-indicator relationships across countries and thematic groupings.")

st.sidebar.divider()


# --- Getting Started ---
st.sidebar.markdown("### 🧭 Getting Started")
st.sidebar.caption("*Modular, structured dashboards for navigating macro themes by country.*")

# if os.path.isfile(IMAGE_PATH):
#     st.sidebar.image(IMAGE_PATH, use_container_width=True)
# else:
#     st.warning("Placeholder image not found. Check /images/toolbox_app2.png.")

st.sidebar.info("""
**🌍 Economic Exploration Dashboard**

Use this launcher to explore macroeconomic themes by region and country.

- **Select a Region:** Begin by choosing a region to reveal available sub-regions and countries.
- **Pick a Country:** Select a country to load its tailored economic dashboard.
- **Launch the App:** Click **Explore** to open the country-specific app in a separate window.
- **Use the Map:** View the interactive map for geographic context and quick reference.

Each dashboard reflects a consistent structure and links to thematic micro apps across indicators.
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
# Region & Launch Utilities — App Initialisation, Country Mapping, Launch Handlers
# -------------------------------------------------------------------------------------------------
def generate_map():
    """
    Generate an interactive world map with markers for each country in the defined region
    structure.

    Each marker displays a popup with the region, sub-region, and country name.
    The map is cached to improve performance on repeated loads.

    Returns:
        folium.Map: A Folium map object with country-level markers.
    """
    map_object = folium.Map(location=[20, 0], zoom_start=2)
    for region, subregions in regions.items():
        for subregion, countries in subregions.items():
            for country, _ in countries.items():
                if country in country_coordinates:
                    coords = country_coordinates[country]
                    popup_message = (
                        f"Region: {region}<br>"
                        f"Sub-Region: {subregion}<br>"
                        f"Country: {country}"
                    )
                    folium.Marker(
                        location=coords,
                        popup=folium.Popup(popup_message, max_width=250),
                        icon=folium.Icon(color="red")
                    ).add_to(map_object)
    return map_object

# --- run app ----
@st.cache_data
def run_country_app(country_name):
    """
    Locate and launch the Streamlit app for a given country, if it exists.

    Args:
        country_name (str): Full name of the country (e.g., 'Canada', 'Japan').

    Side Effects:
        - Launches the country's app in a subprocess on a dynamic port.
        - Displays a success or error message in the Streamlit UI.
    """
    country_code = country_name.lower().replace(" ", "_")
    country_path = os.path.join(APP_PATH, country_code)
    # for filename in ["app.py", f"{country_code}.py"]:
    for filename in ["app.py", f"{country_code}.py"]:
        if os.path.isfile(os.path.join(country_path, filename)):
            launch_streamlit_app(country_path, filename)
            st.success(f"Launching {country_name} dashboard on a new port...")
            return
    st.error(f"No valid app file found for {country_name} in {country_path}.")

# -------------------------------------------------------------------------------------------------
# Main Content
# -------------------------------------------------------------------------------------------------

# --- Load About Markdown (auto-skips if not replaced) ---
with st.expander("📖 About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_economic_exploration.md")

# --- Choose Region, Sub-Region, and Country ---
st.header("🌍 Geographic Exploration")
with st.expander("View Map Guide"):
    st.write("Use the map as a visual guide to help with your selection.")
    m = generate_map()
    map_response = st_folium(m, width="100%")

selected_region = st.selectbox("Select a Region", list(regions.keys()))
if selected_region:
    sub_regions = list(regions[selected_region].keys())
    selected_sub_region = st.selectbox("Select a Sub-Region", sub_regions)
    if selected_sub_region:
        available_countries = list(regions[selected_region][selected_sub_region].keys())
        selected_country = st.selectbox("Select a Country", available_countries)
        if st.button(f"Explore {selected_country}"):
            run_country_app(selected_country)

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire \
— No trading, investment, or policy advice provided.")
