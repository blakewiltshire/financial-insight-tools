# -------------------------------------------------------------------------------------------------
# Market Structure Review
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Market Structure Review
-----------------------

Structured review surface for ownership, float, supply events,
institutional participation, index eligibility, and market structure context.

This module is observational and non-advisory.
It does not provide trading, investment, valuation, portfolio, or IPO participation recommendations.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_market_structure_review.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_market_structure_review.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Engine Imports
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "trade_portfolio_structuring", "market_structure_engine"))
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

from market_structure_loader import (
    load_curated_market_structure_dataset,
    load_curated_market_structure_events,
    get_market_structure_template,
    get_market_structure_events_template,
)
from market_structure_validator import (
    validate_market_structure_df,
    validate_market_structure_events_df,
)
from market_structure_summary import build_market_structure_summary
from market_structure_interpretation import build_market_structure_interpretation
from market_structure_visualisation import (
    render_market_structure_table,
    render_supply_events_table,
    render_focus_supply_events_table,
    render_focus_asset_panels,
    render_structure_context_panels,
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools — Sidebar + Observation Panel Integration + AI Export Tools
# -------------------------------------------------------------------------------------------------

from render_macro_interaction_tools_panel_market_structure_review import (
    render_macro_interaction_tools_panel,
)
from macro_insight_sidebar_panel_market_structure_review import (
    render_macro_sidebar_tools,
)

from observation_handler_market_structure_review import (
    observation_input_form,
    display_observation_log,
)

from ai_export_ui_panel_market_structure_review import render_ai_export_panel
from ai_export_builder_market_structure_review import (
    build_macro_insight_snapshot_market_structure_review,
)

# -------------------------------------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Market Structure Review", layout="wide")
st.title("Market Structure Review")
st.caption(
    "*Review ownership, float, supply events, institutional participation, "
    "index eligibility, and market structure context across selected assets.*"
)

with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("About file not found.")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="Trade and Portfolio Structuring")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)

# -------------------------------------------------------------------------------------------------
# Sidebar — Dataset Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.markdown("### Market Structure Dataset Setup")

dataset_option = st.sidebar.selectbox(
    "Select Dataset:",
    [
        "High-Profile IPOs",
        "User Upload",
    ],
)

uploaded_profile_file = None
uploaded_events_file = None

if dataset_option == "User Upload":
    uploaded_profile_file = st.sidebar.file_uploader(
        "Upload market structure profile CSV",
        type="csv",
        key="market_structure_profile_upload",
    )

    uploaded_events_file = st.sidebar.file_uploader(
        "Upload market structure supply events CSV",
        type="csv",
        key="market_structure_events_upload",
    )

    profile_template_df = get_market_structure_template()
    st.sidebar.download_button(
        label="Get Market Structure Profile Template",
        data=profile_template_df.to_csv(index=False).encode("utf-8"),
        file_name="market_structure_profile_template.csv",
        mime="text/csv",
    )

    events_template_df = get_market_structure_events_template()
    st.sidebar.download_button(
        label="Get Supply Events Template",
        data=events_template_df.to_csv(index=False).encode("utf-8"),
        file_name="market_structure_supply_events_template.csv",
        mime="text/csv",
    )

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------------------------------
if dataset_option == "User Upload":
    if uploaded_profile_file is None or uploaded_events_file is None:
        st.info("Upload both a market structure profile CSV and a supply events CSV to begin.")
        st.stop()

    profile_df = pd.read_csv(uploaded_profile_file)
    events_df = pd.read_csv(uploaded_events_file)
else:
    profile_df = load_curated_market_structure_dataset(
        dataset_name=dataset_option,
        project_path=APPS_PATH,
    )
    events_df = load_curated_market_structure_events(
        dataset_name=dataset_option,
        project_path=APPS_PATH,
    )

# -------------------------------------------------------------------------------------------------
# Validate + Prepare
# -------------------------------------------------------------------------------------------------
profile_validation = validate_market_structure_df(profile_df)

if not profile_validation["valid"]:
    st.error("⚠️ Issues found in market structure profile dataset:")
    for err in profile_validation["errors"]:
        st.markdown(f"- {err}")
    st.stop()

profile_df = profile_validation["cleaned_df"]

events_validation = validate_market_structure_events_df(events_df)

if not events_validation["valid"]:
    st.error("⚠️ Issues found in market structure supply events dataset:")
    for err in events_validation["errors"]:
        st.markdown(f"- {err}")
    st.stop()

events_df = events_validation["cleaned_df"]

# -------------------------------------------------------------------------------------------------
# Focus Asset Selection
# -------------------------------------------------------------------------------------------------
if "Ticker" not in profile_df.columns or profile_df.empty:
    st.error("Market structure dataset requires at least one Ticker value.")
    st.stop()

focus_options_df = profile_df[["Company", "Ticker"]].copy()
focus_options_df["Company"] = focus_options_df["Company"].astype(str).str.strip()
focus_options_df["Ticker"] = focus_options_df["Ticker"].astype(str).str.strip()
focus_options_df = focus_options_df[focus_options_df["Ticker"] != ""]

if focus_options_df.empty:
    st.error("No valid focus assets found in the market structure dataset.")
    st.stop()

focus_labels = {
    f"{row.Company} ({row.Ticker})": row.Ticker
    for row in focus_options_df.itertuples(index=False)
}

# Prefer SpaceX / SPCX when present because this dataset is currently built around the topical case.
default_focus_index = 0
for idx, label in enumerate(focus_labels.keys()):
    if "SPCX" in label.upper():
        default_focus_index = idx
        break

focus_label = st.sidebar.selectbox(
    "Select Focus Asset:",
    list(focus_labels.keys()),
    index=default_focus_index,
)
focus_ticker = focus_labels[focus_label]

summary_payload = build_market_structure_summary(
    profile_df=profile_df,
    events_df=events_df,
    focus_ticker=focus_ticker,
)
contextual_insight = build_market_structure_interpretation(
    dataset_name=dataset_option,
    profile_df=profile_df,
    events_df=events_df,
    summary_payload=summary_payload,
)

# -------------------------------------------------------------------------------------------------
# Market Structure Summary
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
    unsafe_allow_html=True,
)

st.subheader("Market Structure Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Focus Asset",
        summary_payload.get("focus_ticker", "N/A"),
    )

with col2:
    st.metric(
        "Focus Supply Events",
        summary_payload.get("focus_event_count", "N/A"),
    )

with col3:
    st.metric(
        "Structure Type",
        summary_payload.get("focus_structure_type", "N/A"),
    )

with col4:
    st.metric(
        "Comparison Assets",
        max(summary_payload.get("asset_count", 0) - 1, 0),
    )

st.markdown("### Structural Summary")
st.markdown(summary_payload.get("structural_summary", "No structural summary available."))

with st.expander("Market Structure Context"):
    st.markdown(f"**Dataset:** {dataset_option}")
    st.markdown(f"**Focus Asset:** {summary_payload.get('focus_company', 'N/A')} ({summary_payload.get('focus_ticker', 'N/A')})")
    st.markdown(f"**Assets Reviewed:** {len(profile_df)}")
    st.markdown(f"**Supply Events Reviewed:** {len(events_df)}")

st.divider()

# -------------------------------------------------------------------------------------------------
# Main Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Focus Asset",
    "Structure Profiles",
    "Supply Events",
    "Structural Summary",
    "Perspective Lenses",
    "ℹ️ Help",
])

with tabs[0]:
    render_focus_asset_panels(summary_payload)

    st.markdown("### Focus Asset Supply Events")
    st.caption(
        "Mapped events for the selected focus asset. These provide structured context for "
        "ownership, liquidity, available supply, and price-discovery review."
    )
    render_focus_supply_events_table(events_df, summary_payload.get("focus_ticker", ""))

with tabs[1]:
    st.markdown("### Structure Profiles")
    st.caption(
        "Review ownership, float, supply structure, institutional participation, "
        "index eligibility, and structural notes across the selected dataset."
    )
    render_market_structure_table(profile_df)

    st.download_button(
        label="Download Market Structure Profiles CSV",
        data=profile_df.to_csv(index=False).encode("utf-8"),
        file_name="market_structure_profiles.csv",
        mime="text/csv",
    )

with tabs[2]:
    st.markdown("### Supply Events")
    st.caption(
        "Review lock-up releases, insider sale windows, direct listings, secondary offerings, "
        "index-related float changes, and other supply-related events."
    )
    render_supply_events_table(events_df)

    st.download_button(
        label="Download Market Structure Supply Events CSV",
        data=events_df.to_csv(index=False).encode("utf-8"),
        file_name="market_structure_supply_events.csv",
        mime="text/csv",
    )

with tabs[3]:
    render_structure_context_panels(summary_payload)

with tabs[4]:
    st.markdown("### Observation Context Scaffold")
    st.caption(
        "Structured context prepared for observation capture and downstream AI narrative review."
    )
    st.json(summary_payload.get("observation_context", {}))

with tabs[5]:
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("Help file not found.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Macro Interaction Setup
# -------------------------------------------------------------------------------------------------
theme_code = "market_structure_review"
theme_title = "Market Structure Review"

# -------------------------------------------------------------------------------------------------
# Build Snapshot Insight
# -------------------------------------------------------------------------------------------------
market_structure_snapshot_insight = build_macro_insight_snapshot_market_structure_review(
    theme_code=theme_code,
    theme_title=theme_title,
    dataset_name=dataset_option,
    profile_df=profile_df,
    events_df=events_df,
    summary_payload=summary_payload,
    contextual_insight=contextual_insight,
)

# -------------------------------------------------------------------------------------------------
# Sidebar Activation Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_ai_export, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
)


# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools
# -------------------------------------------------------------------------------------------------
selected_indicators = (
    profile_df["Company"].dropna().astype(str).tolist()
    if "Company" in profile_df.columns
    else []
)

if show_observation or show_log:
    st.markdown("## Macro Interaction Tools")

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_themes=[theme_code],
    selected_indicators=selected_indicators,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log,
)

# -------------------------------------------------------------------------------------------------
# AI Export Panel
# -------------------------------------------------------------------------------------------------
if show_ai_export:
    render_ai_export_panel(
        snapshot_results=market_structure_snapshot_insight,
        base_asset=dataset_option,
        asset_type_display=theme_title,
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
    "No trading, investment, valuation, IPO participation, or portfolio advice provided."
)
