# -------------------------------------------------------------------------------------------------
# Positioning & Crowding
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Positioning & Crowding
----------------------

Weekly positioning and crowding monitor for core futures markets.

Purpose:
- Review leveraged positioning across core FX, rates, equity, and volatility markets
- Detect crowding, percentile extremes, and flip behaviour
- Support timing and gatekeeping before execution-oriented workflows

Outputs:
- Positioning Conditions Summary
- Positioning vs Market Overlay
- Positioning Structure Table
- Observation + AI Export Capture

This module is observational and gatekeeping-focused.
It does not provide trading, investment, or policy advice.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup (Canonical)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities (Canonical)
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Named Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_positioning_and_crowding.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_positioning_and_crowding.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Engine / Loader Imports
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

from data_sources.positioning.processing_positioning import (  # pylint: disable=import-error
    get_available_positioning_markets,
    load_positioning_market_bundle,
    build_positioning_summary_table,
)

from render_positioning_visualisation import (  # pylint: disable=import-error
    render_positioning_overlay,
    render_positioning_extremes_panel,
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools — Sidebar + Observation Panel Integration
# -------------------------------------------------------------------------------------------------
from render_macro_interaction_tools_panel_intermarket_correlation import (
    render_macro_interaction_tools_panel,
)
from macro_insight_sidebar_panel_positioning_and_crowding import (
    render_macro_sidebar_tools,
)

from observation_handler_positioning_and_crowding import (
    observation_input_form,
    display_observation_log,
)

# -------------------------------------------------------------------------------------------------
# AI Export Tools — Positioning & Crowding
# -------------------------------------------------------------------------------------------------
from ai_export_ui_panel_positioning_and_crowding import render_ai_export_panel
from ai_export_builder_positioning_and_crowding import (
    build_macro_insight_snapshot_positioning_and_crowding,
)

# -------------------------------------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Positioning & Crowding", layout="wide")
st.title("Positioning & Crowding")
st.caption(
    "*Review leveraged positioning, crowding, percentile extremes, and recent positioning turns "
    "across core futures markets.*"
)

with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="Intermarket & Correlation Dashboard")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------------------------
window_options = [26, 52, 104, 156, 260]

# -------------------------------------------------------------------------------------------------
# Sidebar — Market Selection
# -------------------------------------------------------------------------------------------------
available_markets = get_available_positioning_markets()

market_lookup = {
    label: slug
    for slug, label in available_markets
}

selected_label = st.sidebar.selectbox(
    "Select Positioning Market:",
    options=list(market_lookup.keys())
)

selected_market = market_lookup[selected_label]


lookback_window = st.sidebar.selectbox(
    "Select Historical Lookback (weeks):",
    window_options,
    index=1
)

with st.sidebar.expander("ℹ️ Positioning Notes"):
    st.markdown("""
**Net Positioning**
Leveraged long positioning less leveraged short positioning.

**Net Position Share (%)**
Long open-interest share less short open-interest share.

**Percentile**
Shows where current net positioning sits relative to its recent historical range.

**Positioning Turn**
Highlights when net positioning shifts from net short to net long, or from net long to net short.

**Role in the system**
This module is a timing and crowding check. It is not a standalone directional engine.
""")

with st.sidebar.expander("📘 Adding New Assets"):
    st.markdown("""
To add new assets to the Positioning & Crowding module:

- create the positioning CSV
- add the market price series to `cots_assets_default.csv`
- register the asset inside `processing_positioning.py`

Reference the bundled guide:

**README — Adding New Assets**

This ensures positioning overlays, percentile context,
and positioning turn detection work correctly.
""")

# -------------------------------------------------------------------------------------------------
# Load Market Bundle
# -------------------------------------------------------------------------------------------------
bundle = load_positioning_market_bundle(
    market_slug=selected_market,
    lookback_window=lookback_window,
    project_path=PROJECT_PATH
)

positioning_df = bundle.get("positioning_df", pd.DataFrame())
overlay_df = bundle.get("overlay_df", pd.DataFrame())
summary_payload = bundle.get("summary_payload", {})
messages = bundle.get("messages", [])

for msg in messages:
    st.warning(msg)

if positioning_df.empty:
    st.warning("No positioning data available for the selected market.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Derived Summary Metrics
# -------------------------------------------------------------------------------------------------
structural_state = summary_payload.get("structural_state", "N/A")
current_net_position = summary_payload.get("current_net_position")
current_net_pct = summary_payload.get("current_net_pct")
positioning_percentile = summary_payload.get("positioning_percentile")
positioning_turn = summary_payload.get("positioning_turn", "No Recent Regime Turn")
contextual_insight = summary_payload.get(
    "contextual_interpretation",
    "Current positioning conditions are being assessed."
)

summary_df = build_positioning_summary_table(positioning_df)

# -------------------------------------------------------------------------------------------------
# Positioning Conditions Summary
# -------------------------------------------------------------------------------------------------

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        padding: 0.2rem 0.2rem 0.2rem 0.2rem;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Positioning Conditions Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Structural State", structural_state)

with col2:
    st.metric(
        "Net Position",
        f"{current_net_position:,.0f}" if pd.notna(current_net_position) else "N/A"
    )

with col3:
    st.metric(
        "Net Position Share (%)",
        f"{current_net_pct:.1f}" if pd.notna(current_net_pct) else "N/A"
    )

with col4:
    st.metric(
        "Percentile / Turn",
        (
            f"{positioning_percentile:.1f}th | {positioning_turn}"
            if pd.notna(positioning_percentile)
            else f"N/A | {positioning_turn}"
        )
    )

st.markdown("### Structural Interpretation")
st.write(contextual_insight)

with st.expander("Positioning Context"):
    st.markdown(f"**Selected Market:** {selected_market}")
    st.markdown(f"**Lookback Window:** {lookback_window} weeks")

st.divider()

# -------------------------------------------------------------------------------------------------
# Main Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Positioning vs Market Overlay",
    "Extremes & Positioning Turn",
    "Positioning Summary",
    "ℹ️ Help",
])

with tabs[0]:
    render_positioning_overlay(overlay_df)

with tabs[1]:
    render_positioning_extremes_panel(positioning_df)

with tabs[2]:
    st.dataframe(summary_df, width="stretch", hide_index=True)

    with st.expander("Raw Positioning Data"):
        st.dataframe(positioning_df, width="stretch", hide_index=True)

with tabs[3]:
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("Help file not found.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Macro Interaction Setup
# -------------------------------------------------------------------------------------------------
theme_code = "positioning_and_crowding"
theme_title = "Positioning & Crowding"

# -------------------------------------------------------------------------------------------------
# Build Snapshot Insight
# -------------------------------------------------------------------------------------------------
positioning_snapshot_insight = build_macro_insight_snapshot_positioning_and_crowding(
    theme_code=theme_code,
    theme_title=theme_title,
    selected_market=selected_market,
    lookback_window=lookback_window,
    summary_payload=summary_payload
)

# -------------------------------------------------------------------------------------------------
# Sidebar Activation Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_ai_export, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools
# -------------------------------------------------------------------------------------------------
if show_observation or show_log:
    st.markdown("## Macro Interaction Tools")

selected_indicators = [selected_market] if selected_market else []

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_themes=[theme_code],
    selected_indicators=selected_indicators,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

# -------------------------------------------------------------------------------------------------
# AI Export Panel — Positioning & Crowding
# -------------------------------------------------------------------------------------------------
if show_ai_export:
    render_ai_export_panel(
        snapshot_results=positioning_snapshot_insight,
        base_asset=selected_market,
        asset_type_display=theme_title
    )

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
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
            width="stretch",
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width="stretch",
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
    "No trading, investment, or policy advice provided."
)
