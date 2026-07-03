# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

"""
Relationship Manager — Financial Insight Tools

A lightweight relationship-to-asset framing workspace.

Purpose:
- Select relationship areas and business capability filters
- Surface candidate US large-cap companies from generated business capability tags
- Support candidate asset review, download, and observation/export workflows

This module does not rank, score, recommend, or analyse securities.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys
import json
from datetime import datetime

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import load_markdown_file, build_sidebar_links, get_named_paths

# -------------------------------------------------------------------------------------------------
# Local Loader
# -------------------------------------------------------------------------------------------------
from apps.data_sources.relationship_mapping.relationship_mapping_loader import (
    load_business_capability_map,
    load_business_tag_registry,
    load_relationship_tag_registry,
    search_companies,
)

# -------------------------------------------------------------------------------------------------
# Resolve Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_relationship_manager.md")
DATA_PATH = os.path.join(PROJECT_PATH, "apps", "data_sources", "relationship_mapping", "data")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# Observation Tools (User Observation Logging — Reference Data)
# -------------------------------------------------------------------------------------------------
from observation_handler_relationship_manager import (
    observation_input_form,
    display_observation_log,
)

from render_macro_interaction_tools_panel_relationship_manager import (
    render_macro_interaction_tools_panel,
)
from macro_insight_sidebar_panel_reference import render_macro_sidebar_tools



# -------------------------------------------------------------------------------------------------
# Display Helpers
# -------------------------------------------------------------------------------------------------
def humanise_tag(value: str) -> str:
    """
    Convert internal snake_case tags into human-readable labels.

    Examples:
    - ai_infrastructure -> AI Infrastructure
    - capital_expenditure -> Capital Expenditure
    """
    if value is None:
        return ""

    text = str(value).strip()
    if not text:
        return ""

    replacements = {
        "ai": "AI",
        "it": "IT",
        "rd": "R&D",
        "ev": "EV",
        "fx": "FX",
        "us": "US",
        "uk": "UK",
    }

    words = text.replace("-", "_").split("_")
    return " ".join(replacements.get(word.lower(), word.capitalize()) for word in words if word)


def build_label_map(df, key_col: str) -> dict:
    """
    Build a tag_id -> display label mapping.
    Uses display_name / label columns if present, otherwise humanises the internal tag.
    """
    if df.empty or key_col not in df.columns:
        return {}

    display_col = None
    for candidate in ["display_name", "label", "relationship_label", "business_label"]:
        if candidate in df.columns:
            display_col = candidate
            break

    mapping = {}
    for _, row in df.iterrows():
        tag_id = str(row[key_col]).strip()
        if not tag_id:
            continue
        if display_col and str(row.get(display_col, "")).strip():
            mapping[tag_id] = str(row[display_col]).strip()
        else:
            mapping[tag_id] = humanise_tag(tag_id)
    return mapping


def format_tag_list(value, label_map: dict) -> str:
    """
    Convert a semicolon-separated tag field into a clean human-readable string.
    """
    if value is None:
        return ""

    raw_items = [item.strip() for item in str(value).split(";") if item.strip()]
    labels = [label_map.get(item, humanise_tag(item)) for item in raw_items]
    return " • ".join(labels)


def format_fit_availability(value) -> str:
    """
    Display FIT data availability in a human-readable form.
    """
    if bool(value):
        return "Available in core daily price data"
    return "Requires user-supplied price data"


def map_labels_to_ids(selected_labels: list, inverse_map: dict) -> list:
    """
    Convert selected display labels back into internal tag ids for loader filtering.
    """
    return [inverse_map[label] for label in selected_labels if label in inverse_map]


# -------------------------------------------------------------------------------------------------
# Streamlit Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Relationship Manager", layout="wide")
st.title("Relationship Manager")
st.caption(
    "*Explore how relationship areas and business capabilities may connect to candidate assets.*"
)

# -------------------------------------------------------------------------------------------------
# Info Panel
# -------------------------------------------------------------------------------------------------
with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.warning("Missing: docs/about_relationship_manager.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="Reference Data & Trusted Sources")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member


st.sidebar.subheader("View Options")
fit_available_only = st.sidebar.toggle(
    "Show only core daily price data assets",
    value=False,
)

with st.sidebar.expander("ℹ️ App Usage Notes"):
    st.markdown(
        "Use this workspace to explore how relationship areas and business capabilities "
        "may connect to candidate assets.\n\n"
        "Candidate assets are not rankings, signals, or recommendations. They are starting "
        "points for further review in the wider FIT environment.\n\n"
        "Assets outside the core daily price dataset can be added manually through the relevant "
        "user asset workflow before market examination."
    )

# -------------------------------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------------------------------
df_assets = load_business_capability_map(DATA_PATH)
df_business_tags = load_business_tag_registry(DATA_PATH)
df_relationship_tags = load_relationship_tag_registry(DATA_PATH)

relationship_label_map = build_label_map(df_relationship_tags, "relationship_tag")
business_label_map = build_label_map(df_business_tags, "business_tag")
relationship_inverse_map = {label: tag_id for tag_id, label in relationship_label_map.items()}
business_inverse_map = {label: tag_id for tag_id, label in business_label_map.items()}

# -------------------------------------------------------------------------------------------------
# Relationship Selection
# -------------------------------------------------------------------------------------------------
st.subheader("1. Relationship Areas")
st.markdown(
    "Select relationship areas that may connect a theme, narrative, or observation to companies "
    "and potential market exposures."
)

relationship_options = sorted(relationship_label_map.values())
business_options = sorted(business_label_map.values())

col_rel1, col_rel2 = st.columns(2)
with col_rel1:
    selected_relationship_labels = st.multiselect(
        "Relationship areas",
        relationship_options,
        placeholder="Select relationship areas",
    )
with col_rel2:
    selected_business_labels = st.multiselect(
        "Business capabilities",
        business_options,
        placeholder="Optional: narrow by business capability",
    )

selected_relationships = map_labels_to_ids(selected_relationship_labels, relationship_inverse_map)
selected_business_tags = map_labels_to_ids(selected_business_labels, business_inverse_map)

free_text = st.text_input(
    "Search",
    placeholder="Search company names, descriptions, business capabilities, or relationship areas",
)

# -------------------------------------------------------------------------------------------------
# Candidate Assets
# -------------------------------------------------------------------------------------------------
st.subheader("2. Candidate Assets")
st.caption(
    "Select rows from the table to include candidate assets in the export. "
    "This is a framing step only; market behaviour should be reviewed in the relevant FIT modules."
)

df_candidates = search_companies(
    df_assets,
    text=free_text,
    business_tags=selected_business_tags,
    relationship_tags=selected_relationships,
    fit_price_available_only=fit_available_only,
)

display_cols = [
    "ticker",
    "company_name",
    "business_tags",
    "relationship_candidates_draft",
    "fit_price_available",
]

# Prepare display dataframe without altering source dataframe used for export.
df_display = df_candidates[display_cols].copy()
df_display = df_display.rename(columns={
    "ticker": "Ticker",
    "company_name": "Company",
    "business_tags": "Business Capabilities",
    "relationship_candidates_draft": "Relationship Areas",
    "fit_price_available": "Data Availability",
})
df_display["Business Capabilities"] = df_display["Business Capabilities"].apply(
    lambda value: format_tag_list(value, business_label_map)
)
df_display["Relationship Areas"] = df_display["Relationship Areas"].apply(
    lambda value: format_tag_list(value, relationship_label_map)
)
df_display["Data Availability"] = df_display["Data Availability"].apply(format_fit_availability)

selection_event = st.dataframe(
    df_display,
    width="stretch",
    hide_index=True,
    selection_mode="multi-row",
    on_select="rerun",
)

selected_rows = selection_event.selection.rows if selection_event and selection_event.selection else []
selected_df = df_candidates.iloc[selected_rows].copy() if selected_rows else df_candidates.iloc[0:0].copy()
selected_display_df = df_display.iloc[selected_rows].copy() if selected_rows else df_display.iloc[0:0].copy()

if selected_rows:
    selected_summary = " • ".join(selected_display_df["Ticker"].dropna().astype(str).tolist())
    st.success(f"Selected assets ({len(selected_rows)}): {selected_summary}")
else:
    st.info("Select one or more rows to prepare an export.")

with st.expander("View selected asset details", expanded=bool(selected_rows)):
    if selected_rows:
        st.dataframe(selected_display_df, width="stretch", hide_index=True)
    else:
        st.caption("No candidate assets selected yet.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Export Bundle
# -------------------------------------------------------------------------------------------------
st.subheader("3. Export")

bundle = {
    "created_at": datetime.utcnow().isoformat() + "Z",
    "module": "relationship_manager",
    "selected_relationship_tags": selected_relationships,
    "selected_relationship_labels": selected_relationship_labels,
    "selected_business_tags": selected_business_tags,
    "selected_business_labels": selected_business_labels,
    "candidate_asset_count": int(len(df_candidates)),
    "selected_asset_count": int(len(selected_df)),
    "selected_assets": selected_df[display_cols].to_dict(orient="records"),
    "workflow_note": (
        "Relationship Manager frames candidate assets for investigation. "
        "Use the appropriate FIT modules for market behaviour, volatility, positioning, trend, "
        "correlation, and trade-structure review."
    ),
}

if selected_rows:
    st.download_button(
        "Download Selected Assets CSV",
        data=selected_display_df.to_csv(index=False),
        file_name="relationship_manager_selected_assets.csv",
        mime="text/csv",
        width="stretch",
    )

    st.download_button(
        "Download Relationship Bundle JSON",
        data=json.dumps(bundle, indent=2),
        file_name="relationship_manager_bundle.json",
        mime="application/json",
        width="stretch",
    )
else:
    st.caption("Select rows from the Candidate Assets table to enable downloads.")

with st.expander("View Relationship Bundle JSON"):
    st.json(bundle)


st.divider()

# -------------------------------------------------------------------------------------------------
# Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
theme_code = "relationship_manager"
theme_title = "Relationship Manager"
selected_use_case = "Relationship Manager Snapshot"

# -------------------------------------------------------------------------------------------------
# Activate Observation + Journal Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case,
)

if show_observation or show_log:
    st.markdown("## Macro Interaction Tools")
    st.caption(
        "*Record relationship-mapping observations or review saved notes for later AI export and cross-module review.*"
    )

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log,
)


# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, "
    "investment, or policy advice provided."
)
