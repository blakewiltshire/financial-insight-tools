# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

"""
Relationship Manager — Financial Insight Tools

A pathway-led investigation workspace.

Purpose:
- Record the observation or idea that prompted the investigation
- Begin with a company or business capability
- Show the company's primary and material additional capabilities
- Examine the starting capability directly or traverse curated capability-to-capability pathways
- Surface candidate US large-cap companies at the active investigation capability
- Distinguish primary capability matches from additional capability matches
- Preserve the full exploration environment and any selected pathway

This module does not rank, score, recommend, or analyse securities.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys
import json
from datetime import datetime, timezone

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import load_markdown_file, build_sidebar_links, get_named_paths

# -------------------------------------------------------------------------------------------------
# Resolve Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_relationship_manager.md")
DATA_PATH = os.path.join(
    PROJECT_PATH,
    "apps",
    "data_sources",
    "relationship_mapping",
    "data",
)
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

COMPANY_CAPABILITY_FILE = os.path.join(
    DATA_PATH,
    "us_large_business_capability_map.csv",
)
BUSINESS_REGISTRY_FILE = os.path.join(
    DATA_PATH,
    "business_capability_tag_registry.csv",
)
RELATIONSHIP_FILE = os.path.join(
    DATA_PATH,
    "business_capability_relationship_registry.csv",
)
PRICE_AVAILABILITY_FILE = os.path.join(
    DATA_PATH,
    "fit_price_available_us_large_caps.csv",
)

# -------------------------------------------------------------------------------------------------
# Observation Engine Path
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

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
    """Convert an internal snake_case tag into a readable label."""
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
        "reits": "REITs",
    }
    words = text.replace("-", "_").split("_")
    return " ".join(
        replacements.get(word.lower(), word.capitalize())
        for word in words
        if word
    )


def split_tags(value) -> list:
    """Split a semicolon-delimited capability field."""
    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def normalise_boolean(value) -> bool:
    """Convert common CSV boolean representations into a Python bool."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def format_fit_availability(value, status: str = "") -> str:
    """Return a readable FIT price-data availability label."""
    if normalise_boolean(value):
        return "Core daily price data"

    status_labels = {
        "insufficient_price_history": "Insufficient price history",
        "provisional_listing": "Provisional listing",
        "inactive_or_removed": "Inactive or removed",
        "user_supplied_data_required": "User-supplied price data required",
    }
    return status_labels.get(
        str(status).strip(),
        "User-supplied price data required",
    )


def format_capability_list(value, label_map: dict) -> str:
    """Format a semicolon-delimited capability field."""
    return " • ".join(
        label_map.get(tag, humanise_tag(tag))
        for tag in split_tags(value)
    )


def safe_read_csv(file_path: str, required_columns: set, label: str) -> pd.DataFrame:
    """Load a required CSV and stop the page with a useful message if invalid."""
    try:
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    except FileNotFoundError:
        st.error(f"Missing {label}: {os.path.basename(file_path)}")
        st.stop()

    missing = required_columns.difference(df.columns)
    if missing:
        st.error(
            f"{label} is missing required columns: "
            + ", ".join(sorted(missing))
        )
        st.stop()

    return df


def load_price_availability(file_path: str) -> pd.DataFrame:
    """Load the independent FIT price-availability registry."""
    required = {
        "ticker",
        "company_name",
        "fit_price_available",
        "availability_status",
    }

    try:
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    except FileNotFoundError:
        return pd.DataFrame(columns=sorted(required))

    if required.difference(df.columns):
        return pd.DataFrame(columns=sorted(required))

    df = df[list(required)].copy()
    df["ticker"] = df["ticker"].str.strip().str.upper()
    df["fit_price_available"] = df["fit_price_available"].apply(
        normalise_boolean
    )
    return df.drop_duplicates(subset=["ticker"], keep="last")


def build_company_label(row) -> str:
    """Create a stable company selector label."""
    return f"{row['company_name']} ({row['ticker']})"


def prepare_candidate_display(
    df: pd.DataFrame,
    capability_label: str,
    label_map: dict,
) -> pd.DataFrame:
    """Prepare a readable candidate-company table."""
    display = df.copy()
    display["Capability Role"] = display["capability_role"].map({
        "primary": "Primary capability",
        "additional": "Additional capability",
    })
    display["Primary Capability"] = display["primary_business_tag"].map(
        lambda value: label_map.get(value, humanise_tag(value))
    )
    display["Material Capabilities"] = display["business_tags"].apply(
        lambda value: format_capability_list(value, label_map)
    )
    display["FIT Data"] = display.apply(
        lambda row: format_fit_availability(
            row["fit_price_available"],
            row["availability_status"],
        ),
        axis=1,
    )
    display["Pathway Destination"] = capability_label

    return display[[
        "ticker",
        "company_name",
        "Capability Role",
        "Primary Capability",
        "Material Capabilities",
        "FIT Data",
        "Pathway Destination",
    ]].rename(columns={
        "ticker": "Ticker",
        "company_name": "Company",
    })


# -------------------------------------------------------------------------------------------------
# Streamlit Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Relationship Manager", layout="wide")
st.title("Relationship Manager")
st.caption(
    "*Traverse business-capability pathways to surface candidate assets for further investigation.*"
)

# -------------------------------------------------------------------------------------------------
# About
# -------------------------------------------------------------------------------------------------
with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.markdown(
            "Relationship Manager connects companies, material business capabilities, "
            "and curated relationship pathways. It surfaces candidate assets for further "
            "investigation; it does not rank, score, recommend, or predict securities."
        )

# -------------------------------------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="Reference Data & Trusted Sources")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.subheader("Candidate View")
include_additional_matches = st.sidebar.toggle(
    "Include additional-capability matches",
    value=False,
    help=(
        "Off: show companies for which the destination is the primary capability. "
        "On: also include companies for which it is a material additional capability."
    ),
)
fit_available_only = st.sidebar.toggle(
    "Show only core daily price data assets",
    value=False,
)

with st.sidebar.expander("ℹ️ App Usage Notes"):
    st.markdown(
        "Record the observation or idea that prompted the investigation, then enter "
        "through a company or business capability.\n\n"
        "The starting capability can be examined directly or used as a gateway to "
        "a related capability environment.\n\n"
        "Relationship Manager preserves both the complete exploration environment and "
        "any focused capability or pathway selected for closer review.\n\n"
        "Primary matches form the focused candidate universe. Additional-capability "
        "matches can be included to widen the aperture.\n\n"
        "Candidate assets are not rankings, signals, or recommendations. Continue the "
        "investigation in the relevant FIT modules before considering trade structure."
    )

# -------------------------------------------------------------------------------------------------
# Load and Prepare Data
# -------------------------------------------------------------------------------------------------
df_assets = safe_read_csv(
    COMPANY_CAPABILITY_FILE,
    {
        "ticker",
        "company_name",
        "primary_business_tag",
        "business_tags",
        "company_overview",
    },
    "company capability map",
)
df_registry = safe_read_csv(
    BUSINESS_REGISTRY_FILE,
    {"business_tag", "tag_group", "description"},
    "business capability registry",
)
df_relationships = safe_read_csv(
    RELATIONSHIP_FILE,
    {
        "business_tag",
        "related_business_tag",
        "relationship_group",
        "relationship_direction",
        "relationship_description",
    },
    "business capability relationship registry",
)
df_price = load_price_availability(PRICE_AVAILABILITY_FILE)

df_assets["ticker"] = df_assets["ticker"].str.strip().str.upper()
df_assets["primary_business_tag"] = df_assets["primary_business_tag"].str.strip()
df_assets["business_tags"] = df_assets["business_tags"].fillna("")
df_assets["company_label"] = df_assets.apply(build_company_label, axis=1)

df_assets = df_assets.drop(
    columns=["fit_price_available", "availability_status"],
    errors="ignore",
)
df_assets = df_assets.merge(
    df_price[[
        "ticker",
        "fit_price_available",
        "availability_status",
    ]],
    on="ticker",
    how="left",
)
df_assets["fit_price_available"] = (
    df_assets["fit_price_available"]
    .fillna(False)
    .apply(normalise_boolean)
)
df_assets["availability_status"] = (
    df_assets["availability_status"]
    .fillna("user_supplied_data_required")
    .replace("", "user_supplied_data_required")
)

business_label_map = {
    row["business_tag"]: humanise_tag(row["business_tag"])
    for _, row in df_registry.iterrows()
}
business_description_map = {
    row["business_tag"]: row["description"]
    for _, row in df_registry.iterrows()
}
business_group_map = {
    row["business_tag"]: row["tag_group"]
    for _, row in df_registry.iterrows()
}

# -------------------------------------------------------------------------------------------------
# 1. Investigation Context
# -------------------------------------------------------------------------------------------------
st.subheader("1. Investigation Context")
st.markdown(
    "Record the observation, idea, or development that prompted the investigation. "
    "This context is preserved with the relationship environment for later AI review."
)

context_col_1, context_col_2 = st.columns([2, 1])
with context_col_1:
    investigation_observation = st.text_area(
        "Observation or investigative premise",
        placeholder=(
            "Example: Continued manufacturing expansion may extend beyond industrial "
            "manufacturing into electrical equipment, semiconductors, machinery, and "
            "other connected business environments."
        ),
        height=130,
    )
with context_col_2:
    source_type = st.selectbox(
        "Source type",
        [
            "User observation",
            "Economic indicator",
            "Company announcement",
            "Company research",
            "Technological development",
            "Political or regulatory development",
            "Geopolitical development",
            "Market narrative",
            "Other",
        ],
    )
    source_reference = st.text_input(
        "Source reference",
        placeholder="Optional source, release, article, filing, or date",
    )

investigation_context = {
    "observation": investigation_observation.strip(),
    "source_type": source_type,
    "source_reference": source_reference.strip(),
}

# -------------------------------------------------------------------------------------------------
# 2. Investigation Entry
# -------------------------------------------------------------------------------------------------
st.subheader("2. Investigation Entry")
st.markdown(
    "Begin with a company when the investigation starts from a named asset, "
    "or begin with a business capability when the idea starts from an industry, "
    "theme, economic observation, or operating environment."
)

entry_route = st.radio(
    "Starting point",
    ["Start with a company", "Start with a business capability"],
    horizontal=True,
    label_visibility="collapsed",
)

starting_company = None
starting_capability = ""
starting_capability_role = ""
source_context = {}

if entry_route == "Start with a company":
    company_options = (
        df_assets.sort_values(["company_name", "ticker"])["company_label"].tolist()
    )
    selected_company_label = st.selectbox(
        "Company",
        company_options,
        index=None,
        placeholder="Select a company",
    )

    if selected_company_label:
        starting_company = df_assets.loc[
            df_assets["company_label"].eq(selected_company_label)
        ].iloc[0]

        primary_tag = starting_company["primary_business_tag"]
        all_company_tags = split_tags(starting_company["business_tags"])
        additional_tags = [
            tag for tag in all_company_tags if tag != primary_tag
        ]

        st.markdown(f"### {starting_company['company_name']} · {starting_company['ticker']}")
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown("**Primary Business Capability**")
            st.markdown(
                f"### {business_label_map.get(primary_tag, humanise_tag(primary_tag))}"
            )
            st.caption(
                business_description_map.get(
                    primary_tag,
                    "No capability description is available.",
                )
            )
        with col_b:
            st.markdown("**Material Additional Capabilities**")
            if additional_tags:
                st.markdown(
                    " • ".join(
                        business_label_map.get(tag, humanise_tag(tag))
                        for tag in additional_tags
                    )
                )
            else:
                st.caption("No material additional capabilities are currently assigned.")

        with st.expander("View detailed company overview"):
            st.write(starting_company["company_overview"])

        capability_choices = [primary_tag] + additional_tags
        capability_display = {
            tag: (
                f"{business_label_map.get(tag, humanise_tag(tag))} "
                f"— {'Primary' if tag == primary_tag else 'Additional'}"
            )
            for tag in capability_choices
        }
        starting_capability = st.selectbox(
            "Capability to explore",
            capability_choices,
            format_func=lambda tag: capability_display[tag],
        )
        starting_capability_role = (
            "primary" if starting_capability == primary_tag else "additional"
        )
        source_context = {
            "entry_route": "company",
            "starting_ticker": starting_company["ticker"],
            "starting_company": starting_company["company_name"],
            "starting_capability": starting_capability,
            "starting_capability_role": starting_capability_role,
        }

else:
    capability_options = sorted(
        df_registry["business_tag"].tolist(),
        key=lambda tag: business_label_map.get(tag, humanise_tag(tag)),
    )
    starting_capability = st.selectbox(
        "Business capability",
        capability_options,
        index=None,
        placeholder="Select a business capability",
        format_func=lambda tag: business_label_map.get(tag, humanise_tag(tag)),
    )

    if starting_capability:
        capability_label = business_label_map.get(
            starting_capability,
            humanise_tag(starting_capability),
        )
        capability_group = business_group_map.get(starting_capability, "")
        st.markdown(f"### {capability_label}")
        if capability_group:
            st.caption(capability_group)
        st.write(
            business_description_map.get(
                starting_capability,
                "No capability description is available.",
            )
        )

        focused_count = int(
            df_assets["primary_business_tag"].eq(starting_capability).sum()
        )
        expanded_count = int(
            df_assets["business_tags"].apply(
                lambda value: starting_capability in split_tags(value)
            ).sum()
        )
        col_a, col_b = st.columns(2)
        col_a.metric("Primary company universe", focused_count)
        col_b.metric("Expanded company universe", expanded_count)

        source_context = {
            "entry_route": "business_capability",
            "starting_capability": starting_capability,
            "starting_capability_role": "selected",
        }

# -------------------------------------------------------------------------------------------------
# 3. Investigation Pathway
# -------------------------------------------------------------------------------------------------
st.subheader("3. Investigation Pathway")

selected_relationship = None
destination_capability = ""
active_candidate_capability = ""
investigation_route = ""
full_pathway_df = pd.DataFrame()

if not starting_capability:
    st.info(
        "Select a starting company or business capability to reveal its candidate "
        "environment and related pathways."
    )
else:
    starting_label = business_label_map.get(
        starting_capability,
        humanise_tag(starting_capability),
    )

    pathway_choice = st.radio(
        "How would you like to continue?",
        [
            "Examine the starting capability",
            "Follow a relationship",
        ],
        horizontal=True,
    )

    if pathway_choice == "Examine the starting capability":
        investigation_route = "examine_starting_capability"
        active_candidate_capability = starting_capability

        st.markdown(f"### {starting_label}")
        route_col_1, route_col_2 = st.columns(2)
        route_col_1.metric("Investigation route", "Starting capability")
        route_col_2.metric("Active candidate capability", starting_label)
        st.info(
            "The selected business capability is the current investigation environment. "
            "Candidate assets can be reviewed directly without following another pathway."
        )

        pathway_df = df_relationships.loc[
            df_relationships["business_tag"].eq(starting_capability)
        ].copy()
        if "display_order" in pathway_df.columns:
            pathway_df["display_order_numeric"] = pd.to_numeric(
                pathway_df["display_order"], errors="coerce"
            )
            pathway_df = pathway_df.sort_values([
                "display_order_numeric", "relationship_group", "related_business_tag"
            ])
        else:
            pathway_df = pathway_df.sort_values([
                "relationship_group", "related_business_tag"
            ])
        full_pathway_df = pathway_df.copy()

        with st.expander("View available relationship pathways"):
            if full_pathway_df.empty:
                st.caption("No additional relationship pathways are currently available.")
            else:
                pathway_display = full_pathway_df.copy()
                pathway_display["Related Capability"] = pathway_display[
                    "related_business_tag"
                ].map(lambda value: business_label_map.get(value, humanise_tag(value)))
                st.dataframe(
                    pathway_display[[
                        "Related Capability", "relationship_group",
                        "relationship_direction", "relationship_description"
                    ]].rename(columns={
                        "relationship_group": "Relationship",
                        "relationship_direction": "Direction",
                        "relationship_description": "Description",
                    }),
                    width="stretch", hide_index=True,
                )

    else:
        investigation_route = "follow_relationship"
        pathway_df = df_relationships.loc[
            df_relationships["business_tag"].eq(starting_capability)
        ].copy()
        if "display_order" in pathway_df.columns:
            pathway_df["display_order_numeric"] = pd.to_numeric(
                pathway_df["display_order"], errors="coerce"
            )
            pathway_df = pathway_df.sort_values([
                "display_order_numeric", "relationship_group", "related_business_tag"
            ])
        else:
            pathway_df = pathway_df.sort_values([
                "relationship_group", "related_business_tag"
            ])
        full_pathway_df = pathway_df.copy()

        if pathway_df.empty:
            st.warning("No relationship pathways are currently available for this capability.")
        else:
            st.markdown(
                f"Explore where an investigation beginning with **{starting_label}** may travel."
            )
            group_options = ["All pathway groups"] + sorted(
                pathway_df["relationship_group"].dropna().unique().tolist()
            )
            selected_group = st.selectbox("Pathway group", group_options)
            if selected_group != "All pathway groups":
                pathway_df = pathway_df.loc[
                    pathway_df["relationship_group"].eq(selected_group)
                ].copy()
            pathway_df["pathway_label"] = pathway_df.apply(
                lambda row: (
                    f"{business_label_map.get(row['related_business_tag'], humanise_tag(row['related_business_tag']))}"
                    f" — {row['relationship_group']} · {row['relationship_direction']}"
                ),
                axis=1,
            )
            selected_pathway_label = st.selectbox(
                "Related capability",
                pathway_df["pathway_label"].tolist(),
                index=None,
                placeholder="Select a pathway to continue the investigation",
            )
            if selected_pathway_label:
                selected_relationship = pathway_df.loc[
                    pathway_df["pathway_label"].eq(selected_pathway_label)
                ].iloc[0]
                destination_capability = selected_relationship["related_business_tag"]
                active_candidate_capability = destination_capability
                destination_label = business_label_map.get(
                    destination_capability, humanise_tag(destination_capability)
                )
                st.markdown(f"### {starting_label} → {destination_label}")
                meta_1, meta_2, meta_3 = st.columns(3)
                meta_1.metric("Relationship", selected_relationship["relationship_group"])
                meta_2.metric("Direction", selected_relationship["relationship_direction"])
                meta_3.metric("Active candidate capability", destination_label)
                st.info(selected_relationship["relationship_description"])
# -------------------------------------------------------------------------------------------------
# Session Exploration Collection — Setup
# -------------------------------------------------------------------------------------------------
collection_key = "relationship_manager_exploration_collection"
collection_context_key = "relationship_manager_collection_context"

if collection_key not in st.session_state:
    st.session_state[collection_key] = []
if collection_context_key not in st.session_state:
    st.session_state[collection_context_key] = None

active_capability_label = (
    business_label_map.get(
        active_candidate_capability,
        humanise_tag(active_candidate_capability),
    )
    if active_candidate_capability
    else ""
)

pathway_context = {
    **source_context,
    "investigation_route": investigation_route,
    "starting_capability_label": (
        business_label_map.get(
            starting_capability,
            humanise_tag(starting_capability),
        )
        if starting_capability
        else ""
    ),
    "active_candidate_capability": active_candidate_capability,
    "active_candidate_capability_label": active_capability_label,
    "destination_capability": destination_capability,
    "destination_capability_label": (
        business_label_map.get(
            destination_capability,
            humanise_tag(destination_capability),
        )
        if destination_capability
        else ""
    ),
    "relationship_group": (
        selected_relationship["relationship_group"]
        if selected_relationship is not None
        else ""
    ),
    "relationship_direction": (
        selected_relationship["relationship_direction"]
        if selected_relationship is not None
        else ""
    ),
    "relationship_description": (
        selected_relationship["relationship_description"]
        if selected_relationship is not None
        else ""
    ),
}

if investigation_route == "examine_starting_capability":
    current_branch_label = (
        f"Starting Capability — {active_capability_label}"
        if active_capability_label
        else "Starting Capability"
    )
elif investigation_route == "follow_relationship" and selected_relationship is not None:
    current_branch_label = (
        f"{selected_relationship['relationship_group']} — "
        f"{pathway_context['starting_capability_label']} → {active_capability_label}"
    )
else:
    current_branch_label = "Current Exploration Branch"

current_context_signature = {
    "observation": investigation_context.get("observation", ""),
    "source_type": investigation_context.get("source_type", ""),
    "source_reference": investigation_context.get("source_reference", ""),
    "entry_route": source_context.get("entry_route", ""),
    "starting_company": source_context.get("starting_company", ""),
    "starting_ticker": source_context.get("starting_ticker", ""),
    "starting_capability": starting_capability,
}

branch_identity = {
    "investigation_route": investigation_route,
    "starting_capability": starting_capability,
    "active_candidate_capability": active_candidate_capability,
    "relationship_group": pathway_context.get("relationship_group", ""),
    "relationship_direction": pathway_context.get("relationship_direction", ""),
}
branch_key = json.dumps(branch_identity, sort_keys=True)

# -------------------------------------------------------------------------------------------------
# 4. Candidate Assets
# -------------------------------------------------------------------------------------------------
st.subheader("4. Candidate Assets")
st.caption(
    "Primary matches form the focused capability universe. "
    "Enable additional-capability matches in the sidebar to widen the candidate set."
)

df_candidates = df_assets.iloc[0:0].copy()
selected_df = df_assets.iloc[0:0].copy()
selected_display_df = pd.DataFrame()

if not active_candidate_capability:
    if investigation_route == "follow_relationship":
        st.info("Select a relationship pathway to surface candidate companies.")
    else:
        st.info("Select a starting company or business capability to surface candidate companies.")
else:
    active_capability_label = business_label_map.get(
        active_candidate_capability, humanise_tag(active_candidate_capability)
    )
    primary_mask = df_assets["primary_business_tag"].eq(active_candidate_capability)
    additional_mask = df_assets["business_tags"].apply(
        lambda value: active_candidate_capability in split_tags(value)
        and active_candidate_capability != ""
    ) & ~primary_mask

    df_primary = df_assets.loc[primary_mask].copy()
    df_primary["capability_role"] = "primary"
    df_additional = df_assets.loc[additional_mask].copy()
    df_additional["capability_role"] = "additional"

    if include_additional_matches:
        df_candidates = pd.concat([df_primary, df_additional], ignore_index=True)
    else:
        df_candidates = df_primary.copy()

    if fit_available_only:
        df_candidates = df_candidates.loc[df_candidates["fit_price_available"]].copy()

    st.markdown(f"### {active_capability_label} Candidate Universe")
    search_text = st.text_input(
        "Search candidate companies",
        placeholder="Search ticker, company, primary capability, or company overview",
    )
    if search_text.strip():
        query = search_text.strip().lower()
        search_mask = (
            df_candidates["ticker"].str.lower().str.contains(query, regex=False, na=False)
            | df_candidates["company_name"].str.lower().str.contains(query, regex=False, na=False)
            | df_candidates["primary_business_tag"].str.lower().str.contains(query, regex=False, na=False)
            | df_candidates["company_overview"].str.lower().str.contains(query, regex=False, na=False)
        )
        df_candidates = df_candidates.loc[search_mask].copy()

    role_order = {"primary": 0, "additional": 1}
    df_candidates["role_order"] = df_candidates["capability_role"].map(role_order)
    df_candidates = df_candidates.sort_values(
        ["role_order", "company_name", "ticker"]
    ).drop(columns=["role_order"]).reset_index(drop=True)

    focused_total = int(primary_mask.sum())
    expanded_total = int((primary_mask | additional_mask).sum())
    visible_total = len(df_candidates)
    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("Primary universe", focused_total)
    metric_2.metric("Expanded universe", expanded_total)
    metric_3.metric("Visible candidates", visible_total)

    if df_candidates.empty:
        st.warning("No candidate companies match the current capability and view options.")
    else:
        df_display = prepare_candidate_display(
            df_candidates, active_capability_label, business_label_map
        )
        selection_event = st.dataframe(
            df_display,
            width="stretch",
            hide_index=True,
            selection_mode="multi-row",
            on_select="rerun",
            key="relationship_manager_candidate_table",
        )
        selected_rows = (
            selection_event.selection.rows
            if selection_event and selection_event.selection else []
        )
        selected_df = (
            df_candidates.iloc[selected_rows].copy()
            if selected_rows else df_candidates.iloc[0:0].copy()
        )
        selected_display_df = (
            df_display.iloc[selected_rows].copy()
            if selected_rows else df_display.iloc[0:0].copy()
        )
        if selected_rows:
            tickers = " • ".join(selected_display_df["Ticker"].astype(str).tolist())
            st.success(f"Selected candidate assets ({len(selected_rows)}): {tickers}")
        else:
            st.info(
                "Select one or more candidate rows to preserve in the focused investigation bundle."
            )
        with st.expander("View selected candidate details", expanded=bool(selected_rows)):
            if selected_rows:
                st.dataframe(selected_display_df, width="stretch", hide_index=True)
            else:
                st.caption("No candidate assets selected yet.")

        add_branch_clicked = st.button(
            "Add Current Branch to Exploration",
            width="stretch",
            disabled=not bool(selected_rows),
            help=(
                "Select one or more candidate rows, then add this capability or "
                "relationship branch to the current session exploration."
            ),
            key="relationship_manager_add_current_branch",
        )

        if add_branch_clicked:
            saved_context = st.session_state[collection_context_key]
            if (
                saved_context is not None
                and saved_context != current_context_signature
            ):
                st.warning(
                    "The current observation or starting capability differs from "
                    "the existing session collection. Download or clear the "
                    "current collection before beginning a separate investigation."
                )
            else:
                selected_asset_fields = [
                    "ticker",
                    "company_name",
                    "primary_business_tag",
                    "business_tags",
                    "capability_role",
                    "fit_price_available",
                    "availability_status",
                ]
                branch_record = {
                    "branch_key": branch_key,
                    "branch_sequence": 0,
                    "branch_label": current_branch_label,
                    "added_at": datetime.now(timezone.utc).isoformat(),
                    "investigation_context": investigation_context,
                    "pathway": pathway_context,
                    "candidate_view": {
                        "include_additional_capability_matches": (
                            include_additional_matches
                        ),
                        "core_daily_price_data_only": fit_available_only,
                        "visible_candidate_count": int(len(df_candidates)),
                        "selected_asset_count": int(len(selected_df)),
                    },
                    "selected_assets": selected_df[
                        selected_asset_fields
                    ].to_dict(orient="records"),
                    "workflow_note": (
                        "This branch preserves the selected capability environment "
                        "and candidate assets for later combined review."
                    ),
                }

                collection = st.session_state[collection_key]
                existing_index = next(
                    (
                        index
                        for index, item in enumerate(collection)
                        if item.get("branch_key") == branch_key
                    ),
                    None,
                )

                if existing_index is None:
                    branch_record["branch_sequence"] = len(collection) + 1
                    collection.append(branch_record)
                    st.success(f"Added: {current_branch_label}")
                else:
                    branch_record["branch_sequence"] = collection[
                        existing_index
                    ].get("branch_sequence", existing_index + 1)
                    collection[existing_index] = branch_record
                    st.success(f"Updated: {current_branch_label}")

                st.session_state[collection_key] = collection
                st.session_state[collection_context_key] = (
                    current_context_signature
                )
# -------------------------------------------------------------------------------------------------
# 5. Preserve Exploration
# -------------------------------------------------------------------------------------------------
st.divider()
st.subheader("5. Preserve Exploration")
st.markdown(
    "Review the branches saved during this session and download the combined exploration "
    "when required. Individual full and focused exports remain available below."
)

asset_fields = [
    "ticker", "company_name", "primary_business_tag", "business_tags",
    "capability_role", "fit_price_available", "availability_status",
]
relationship_fields = [
    "business_tag", "related_business_tag", "relationship_group",
    "relationship_direction", "relationship_description",
]
if "display_order" in df_relationships.columns:
    relationship_fields.append("display_order")
full_relationships = (
    full_pathway_df[relationship_fields].to_dict(orient="records")
    if not full_pathway_df.empty else []
)

starting_primary_mask = (
    df_assets["primary_business_tag"].eq(starting_capability)
    if starting_capability else pd.Series(False, index=df_assets.index)
)
starting_additional_mask = (
    df_assets["business_tags"].apply(lambda value: starting_capability in split_tags(value))
    & ~starting_primary_mask
    if starting_capability else pd.Series(False, index=df_assets.index)
)
starting_primary_assets = df_assets.loc[starting_primary_mask].copy()
starting_primary_assets["capability_role"] = "primary"
starting_additional_assets = df_assets.loc[starting_additional_mask].copy()
starting_additional_assets["capability_role"] = "additional"
starting_capability_assets = pd.concat(
    [starting_primary_assets, starting_additional_assets], ignore_index=True
)
if fit_available_only:
    starting_capability_assets = starting_capability_assets.loc[
        starting_capability_assets["fit_price_available"]
    ].copy()

full_candidate_universe = []
if not full_pathway_df.empty:
    for _, relationship_row in full_pathway_df.iterrows():
        related_tag = relationship_row["related_business_tag"]
        primary_mask_all = df_assets["primary_business_tag"].eq(related_tag)
        additional_mask_all = df_assets["business_tags"].apply(
            lambda value: related_tag in split_tags(value)
        ) & ~primary_mask_all
        primary_assets = df_assets.loc[primary_mask_all].copy()
        primary_assets["capability_role"] = "primary"
        additional_assets = df_assets.loc[additional_mask_all].copy()
        additional_assets["capability_role"] = "additional"
        pathway_assets = pd.concat([primary_assets, additional_assets], ignore_index=True)
        if fit_available_only:
            pathway_assets = pathway_assets.loc[pathway_assets["fit_price_available"]].copy()
        full_candidate_universe.append({
            "related_business_tag": related_tag,
            "related_business_label": business_label_map.get(related_tag, humanise_tag(related_tag)),
            "relationship_group": relationship_row["relationship_group"],
            "relationship_direction": relationship_row["relationship_direction"],
            "relationship_description": relationship_row["relationship_description"],
            "primary_candidate_count": int(primary_mask_all.sum()),
            "expanded_candidate_count": int((primary_mask_all | additional_mask_all).sum()),
            "assets": (
                pathway_assets[asset_fields].to_dict(orient="records")
                if not pathway_assets.empty else []
            ),
        })

candidate_curation_instruction = (
    "Review the supplied Relationship Manager exploration as an opportunity-set "
    "and candidate-universe review. Use the investigation observation, starting "
    "capability, investigation route, selected relationship context where applicable, "
    "company capability roles, and candidate assets to assess whether the exploration "
    "captures sufficiently relevant and differentiated capabilities, relationships, "
    "and candidate exposures associated with the observation. "
    "Treat a focused investigation bundle as one selected branch of the wider "
    "observation. Assess the supplied candidates within the active capability or "
    "relationship environment without assuming that they represent the complete "
    "investigation. Identify direct and indirect exposures, materially different "
    "operating models, potentially duplicated exposures, weak or ambiguous capability "
    "mappings, and important relationship pathways or candidate types that may be "
    "missing. Do not reduce the candidate universe solely to produce a shorter list. "
    "Retain candidates that provide useful breadth or materially different exposure, "
    "and deprioritise candidates only where their relevance appears weak, incidental, "
    "unsupported, or unnecessarily duplicative. Do not perform detailed market or "
    "company analysis at this stage. Do not use share-price performance, charts, recent "
    "returns, technical indicators, valuation, price-to-earnings ratios, analyst targets, "
    "forecasts, or expected performance to rank companies. These factors may be examined "
    "separately through the relevant Financial Insight Tools modules where required by "
    "the investigation. Organise the review into Opportunity-Set Coverage, Core "
    "Investigation Candidates, Distinct or Diversifying Candidates, Secondary or "
    "Ambiguous Candidates, Deprioritised Candidates, Missing Pathways or Candidate Types, "
    "and Information Requiring Verification. Conclude by stating whether the supplied "
    "universe should be retained, retained but organised, expanded, or narrowed before "
    "further examination through Financial Insight Tools. Do not recommend investments, "
    "predict performance, select trades, or imply that a retained company is expected "
    "to outperform."
)

full_exploration_bundle = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "module": "relationship_manager",
    "workflow": "full_relationship_exploration",
    "investigation_context": investigation_context,
    "entry": source_context,
    "starting_capability": {
        "business_tag": starting_capability,
        "display_label": (
            business_label_map.get(starting_capability, humanise_tag(starting_capability))
            if starting_capability else ""
        ),
        "description": business_description_map.get(starting_capability, ""),
        "primary_candidate_count": int(starting_primary_mask.sum()),
        "expanded_candidate_count": int((starting_primary_mask | starting_additional_mask).sum()),
        "assets": (
            starting_capability_assets[asset_fields].to_dict(orient="records")
            if not starting_capability_assets.empty else []
        ),
    },
    "relationship_environment": full_relationships,
    "candidate_environment": {
        "core_daily_price_data_only": fit_available_only,
        "pathway_count": int(len(full_relationships)),
        "pathways": full_candidate_universe,
    },
    "ai_review_instruction": candidate_curation_instruction,
    "workflow_note": (
        "This bundle preserves the starting capability, its complete candidate universe, "
        "and the wider relationship environment before the user narrows the investigation."
    ),
}

focused_investigation_bundle = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "module": "relationship_manager",
    "workflow": (
        "selected_capability_environment"
        if investigation_route == "examine_starting_capability"
        else "selected_relationship_pathway"
    ),
    "investigation_context": investigation_context,
    "pathway": pathway_context,
    "candidate_view": {
        "include_additional_capability_matches": include_additional_matches,
        "core_daily_price_data_only": fit_available_only,
        "visible_candidate_count": int(len(df_candidates)),
        "selected_asset_count": int(len(selected_df)),
    },
    "selected_assets": (
        selected_df[asset_fields].to_dict(orient="records")
        if not selected_df.empty else []
    ),
    "ai_review_instruction": candidate_curation_instruction,
    "workflow_note": (
        "This bundle preserves the selected capability environment and candidate assets "
        "retained for closer review. Candidate assets are not rankings, signals, "
        "predictions, or recommendations."
    ),
}

# -------------------------------------------------------------------------------------------------
# Saved Session Branches
# -------------------------------------------------------------------------------------------------
st.markdown("### Saved Exploration Branches")
st.caption(
    "Review, remove, clear, or download the branches added beneath the candidate table."
)

saved_branches = st.session_state[collection_key]

if saved_branches:
    branch_summary_rows = []
    for branch in saved_branches:
        tickers = [
            str(asset.get("ticker", ""))
            for asset in branch.get("selected_assets", [])
            if asset.get("ticker")
        ]
        branch_summary_rows.append({
            "Sequence": branch.get("branch_sequence"),
            "Branch": branch.get("branch_label"),
            "Selected Assets": len(tickers),
            "Tickers": " • ".join(tickers),
        })

    st.dataframe(
        pd.DataFrame(branch_summary_rows).sort_values("Sequence"),
        width="stretch",
        hide_index=True,
    )

    branch_labels = {
        f"{branch.get('branch_sequence')}. {branch.get('branch_label')}": branch.get(
            "branch_key"
        )
        for branch in saved_branches
    }
    management_col_1, management_col_2 = st.columns([3, 1])
    with management_col_1:
        branch_to_remove_label = st.selectbox(
            "Saved branch to remove",
            ["Select a saved branch"] + list(branch_labels.keys()),
        )
    with management_col_2:
        st.write("")
        st.write("")
        remove_disabled = branch_to_remove_label == "Select a saved branch"
        if st.button(
            "Remove Branch",
            disabled=remove_disabled,
            width="stretch",
        ):
            remove_key = branch_labels[branch_to_remove_label]
            st.session_state[collection_key] = [
                branch
                for branch in saved_branches
                if branch.get("branch_key") != remove_key
            ]
            if not st.session_state[collection_key]:
                st.session_state[collection_context_key] = None
            st.rerun()

    # Build a deduplicated asset index while retaining every branch reason for inclusion.
    asset_index = {}
    for branch in st.session_state[collection_key]:
        provenance = {
            "branch_sequence": branch.get("branch_sequence"),
            "branch_label": branch.get("branch_label"),
            "investigation_route": branch.get("pathway", {}).get(
                "investigation_route",
                "",
            ),
            "active_candidate_capability": branch.get("pathway", {}).get(
                "active_candidate_capability",
                "",
            ),
            "relationship_group": branch.get("pathway", {}).get(
                "relationship_group",
                "",
            ),
            "relationship_direction": branch.get("pathway", {}).get(
                "relationship_direction",
                "",
            ),
        }
        for asset in branch.get("selected_assets", []):
            ticker = str(asset.get("ticker", "")).strip().upper()
            if not ticker:
                continue
            if ticker not in asset_index:
                asset_index[ticker] = {
                    **asset,
                    "included_through": [],
                }
            asset_index[ticker]["included_through"].append(provenance)

    chained_exploration_bundle = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "module": "relationship_manager",
        "workflow": "chained_relationship_exploration",
        "investigation_context": st.session_state[collection_context_key],
        "branch_count": len(st.session_state[collection_key]),
        "saved_branches": sorted(
            st.session_state[collection_key],
            key=lambda branch: branch.get("branch_sequence", 0),
        ),
        "deduplicated_asset_count": len(asset_index),
        "deduplicated_assets": list(asset_index.values()),
        "ai_review_instruction": candidate_curation_instruction,
        "workflow_note": (
            "This bundle preserves selected branches from one Relationship Manager "
            "investigation. Review each branch independently before considering their "
            "combined coverage. Multiple appearances preserve pathway provenance and do "
            "not imply greater attractiveness or expected performance."
        ),
    }

    collection_export_col_1, collection_export_col_2 = st.columns(2)
    with collection_export_col_1:
        st.download_button(
            "Download Chained Exploration JSON",
            data=json.dumps(chained_exploration_bundle, indent=2),
            file_name="relationship_manager_chained_exploration.json",
            mime="application/json",
            width="stretch",
        )
    with collection_export_col_2:
        if st.button("Clear Session Collection", width="stretch"):
            st.session_state[collection_key] = []
            st.session_state[collection_context_key] = None
            st.rerun()

    with st.expander("View Chained Exploration JSON"):
        st.json(chained_exploration_bundle)
else:
    st.info(
        "No branches have been added. Select candidate assets above and click "
        "Add Current Branch to Exploration."
    )

st.markdown("### Individual Exploration Exports")

if starting_capability:
    export_col_1, export_col_2 = st.columns(2)
    with export_col_1:
        st.download_button(
            "Download Full Exploration JSON",
            data=json.dumps(full_exploration_bundle, indent=2),
            file_name="relationship_manager_full_exploration.json",
            mime="application/json",
            width="stretch",
        )
    with export_col_2:
        if active_candidate_capability and not selected_display_df.empty:
            st.download_button(
                "Download Focused Investigation JSON",
                data=json.dumps(focused_investigation_bundle, indent=2),
                file_name="relationship_manager_focused_investigation.json",
                mime="application/json",
                width="stretch",
            )
        else:
            st.button(
                "Download Focused Investigation JSON",
                disabled=True,
                width="stretch",
                help="Select one or more candidate assets from the active capability universe.",
            )
    if not selected_display_df.empty:
        st.download_button(
            "Download Selected Assets CSV",
            data=selected_display_df.to_csv(index=False),
            file_name="relationship_manager_selected_assets.csv",
            mime="text/csv",
            width="stretch",
        )
    with st.expander("View Full Exploration JSON"):
        st.json(full_exploration_bundle)
    with st.expander("View Focused Investigation JSON"):
        st.json(focused_investigation_bundle)
else:
    st.caption(
        "Select a starting company or business capability to create the full exploration export."
    )

# -------------------------------------------------------------------------------------------------
# Observation and Journal
# -------------------------------------------------------------------------------------------------
st.divider()

theme_code = "relationship_manager"
theme_title = "Relationship Manager"
selected_use_case = "Relationship Exploration"

show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case,
)

if show_observation or show_log:
    st.markdown("## Observation & Investigation Continuity")
    st.caption(
        "*Record what the exploration suggests, where the evidence is incomplete, "
        "which relationships or assets warrant further examination, and why the "
        "investigation may need to narrow or change direction.*"
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
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
    "No trading, investment, or policy advice provided."
)
