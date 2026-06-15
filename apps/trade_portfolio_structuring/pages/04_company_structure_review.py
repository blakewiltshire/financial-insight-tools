# -------------------------------------------------------------------------------------------------
# Company Structure Review
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Company Structure Review
------------------------

Structured company comparison surface for valuation, growth, profitability,
market expectations, and market scepticism.

This module is observational and non-advisory.
It does not provide trading, investment, valuation, or portfolio recommendations.
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
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_company_structure_review.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_company_structure_review.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Engine Imports
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "trade_portfolio_structuring", "company_structure_engine"))
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

from company_structure_loader import (
    load_curated_company_dataset,
    get_company_valuation_template,
)
from company_structure_validator import validate_company_structure_df
from company_structure_summary import build_company_structure_summary
from company_structure_interpretation import build_company_structure_interpretation
from company_structure_visualisation import (
    render_valuation_comparison,
    render_growth_quality_panel,
    render_market_skepticism_panel,
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools — Sidebar + Observation Panel Integration + AI Export Tools
# -------------------------------------------------------------------------------------------------

from render_macro_interaction_tools_panel_company_structure_review import (
    render_macro_interaction_tools_panel,
)
from macro_insight_sidebar_panel_company_structure_review import (
    render_macro_sidebar_tools,
)

from observation_handler_company_structure_review import (
    observation_input_form,
    display_observation_log,
)

from ai_export_ui_panel_company_structure_review import render_ai_export_panel
from ai_export_builder_company_structure_review import (
    build_macro_insight_snapshot_company_structure_review,
)

# -------------------------------------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Company Structure Review", layout="wide")
st.title("Company Structure Review")
st.caption(
    "*Compare valuation, growth, profitability, market expectations, and market scepticism "
    "across companies and peer groups.*"
)

with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

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
st.sidebar.markdown("### Company Dataset Setup")

dataset_option = st.sidebar.selectbox(
    "Select Dataset:",
    [
        "Equities - Magnificent Seven",
        "Equities - Sector Constituents",
        "User Upload",
    ],
)

uploaded_file = None

if dataset_option == "User Upload":
    uploaded_file = st.sidebar.file_uploader(
        "Upload company valuation CSV",
        type="csv",
    )

    template_df = get_company_valuation_template()
    st.sidebar.download_button(
        label="Get Company Valuation Template",
        data=template_df.to_csv(index=False).encode("utf-8"),
        file_name="company_valuation_template.csv",
        mime="text/csv",
    )

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------------------------------
if dataset_option == "User Upload":
    if uploaded_file is None:
        st.info("Upload a company valuation CSV to begin.")
        st.stop()

    df = pd.read_csv(uploaded_file)
else:
    df = load_curated_company_dataset(
        dataset_name=dataset_option,
        project_path=APPS_PATH,
    )

# -------------------------------------------------------------------------------------------------
# Validate + Prepare
# -------------------------------------------------------------------------------------------------
validation = validate_company_structure_df(df)

if not validation["valid"]:
    st.error("⚠️ Issues found in company valuation dataset:")
    for err in validation["errors"]:
        st.markdown(f"- {err}")
    st.stop()

df = validation["cleaned_df"]

# Ensure PE spread is calculated internally
df["PE_Spread"] = df["Trailing_PE"] - df["Forward_PE"]

summary_payload = build_company_structure_summary(df)
contextual_insight = build_company_structure_interpretation(
    dataset_name=dataset_option,
    df=df,
    summary_payload=summary_payload,
)

# -------------------------------------------------------------------------------------------------
# Company Structure Summary
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

st.subheader("Company Structure Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Highest Trailing Valuation",
        summary_payload.get("highest_trailing_pe_label", "N/A"),
    )

with col2:
    st.metric(
        "Highest Revenue Growth",
        summary_payload.get("highest_growth_label", "N/A"),
    )

with col3:
    st.metric(
        "Highest Operating Profitability",
        summary_payload.get("highest_margin_label", "N/A"),
    )

with col4:
    st.metric(
        "Highest Short Interest",
        summary_payload.get("highest_short_interest_label", "N/A"),
    )

st.markdown("### Structural Interpretation")
st.write(contextual_insight)

with st.expander("Company Structure Context"):
    st.markdown(f"**Dataset:** {dataset_option}")
    st.markdown(f"**Companies Reviewed:** {len(df)}")

st.divider()

# -------------------------------------------------------------------------------------------------
# helpers
# -------------------------------------------------------------------------------------------------
def render_peer_context_table(
    peer_difference_df: pd.DataFrame,
    metric: str,
    metric_label: str,
):
    metric_cols = [
        "Company",
        "Ticker",
        metric,
        f"{metric}_Peer_Avg",
        f"{metric}_Diff",
        f"{metric}_Diff_Pct",
    ]

    available_cols = [
        col for col in metric_cols
        if col in peer_difference_df.columns
    ]

    if len(available_cols) < 4:
        st.info(f"No peer context available for {metric_label}.")
        return

    display_df = peer_difference_df[available_cols].copy()

    display_df = display_df.rename(columns={
        metric: metric_label,
        f"{metric}_Peer_Avg": "Peer Average",
        f"{metric}_Diff": "Difference",
        f"{metric}_Diff_Pct": "Difference %",
    })

    if "Difference %" in display_df.columns:
        display_df = display_df.sort_values("Difference %", ascending=False)

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )

# -------------------------------------------------------------------------------------------------
# Main Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Company Comparison",
    "Market Expectations",
    "Growth & Quality",
    "Market Skepticism",
    "Peer Analysis",
    "ℹ️ Help",
])

with tabs[0]:
    st.markdown("### Company Comparison")
    st.caption(
        "Review the selected company group across valuation, growth, profitability, "
        "and market scepticism metrics."
    )

    display_cols = [
        "Company",
        "Ticker",
        "Trailing_PE",
        "Forward_PE",
        "PE_Spread",
        "Revenue_Growth_Pct",
        "Operating_Margin_Pct",
        "Short_Interest_Pct",
    ]

    available_display_cols = [
        col for col in display_cols
        if col in df.columns
    ]

    st.dataframe(
        df[available_display_cols],
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        label="Download Company Comparison CSV",
        data=df[available_display_cols].to_csv(index=False).encode("utf-8"),
        file_name="company_structure_comparison.csv",
        mime="text/csv",
    )

with tabs[1]:
    render_valuation_comparison(df)

with tabs[2]:
    render_growth_quality_panel(df)

with tabs[3]:
    render_market_skepticism_panel(df)

with tabs[4]:
    st.markdown("### Peer Analysis")
    st.caption(
        "Compare peer averages, medians, rankings, and differences from peer averages. "
        "These tables provide structural context for downstream review and AI export."
    )

    peer_average_df = summary_payload.get("peer_average_df", pd.DataFrame())
    ranking_df = summary_payload.get("ranking_df", pd.DataFrame())
    peer_difference_df = summary_payload.get("peer_difference_df", pd.DataFrame())

    st.markdown("#### Peer Group Metrics")
    if not peer_average_df.empty:
        st.dataframe(
            peer_average_df,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No peer group metrics available.")

    st.markdown("#### Peer Rankings")
    if not ranking_df.empty:
        st.dataframe(
            ranking_df,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No peer ranking data available.")

    st.markdown("#### Peer Context by Metric")
    st.caption(
        "Each table compares the selected company metric against the peer-group average. "
        "Repeated peer averages are intentionally shown as the common comparison anchor."
    )

    if not peer_difference_df.empty:
        st.markdown("##### Valuation Context")
        st.caption("Compare valuation metrics relative to peer-group averages.")

        st.markdown("###### Trailing P/E")
        render_peer_context_table(
            peer_difference_df,
            "Trailing_PE",
            "Trailing P/E",
        )

        st.markdown("###### Forward P/E")
        render_peer_context_table(
            peer_difference_df,
            "Forward_PE",
            "Forward P/E",
        )

        st.markdown("###### P/E Spread")
        render_peer_context_table(
            peer_difference_df,
            "PE_Spread",
            "P/E Spread",
        )

        st.markdown("##### Growth Context")
        st.caption("Review revenue growth relative to peer-group averages.")

        st.markdown("###### Revenue Growth")
        render_peer_context_table(
            peer_difference_df,
            "Revenue_Growth_Pct",
            "Revenue Growth (%)",
        )

        st.markdown("##### Quality Context")
        st.caption("Review operating profitability relative to peer-group averages.")

        st.markdown("###### Operating Margin")
        render_peer_context_table(
            peer_difference_df,
            "Operating_Margin_Pct",
            "Operating Margin (%)",
        )

        st.markdown("##### Market Skepticism Context")
        st.caption("Review short-interest levels relative to peer-group averages.")

        st.markdown("###### Short Interest")
        render_peer_context_table(
            peer_difference_df,
            "Short_Interest_Pct",
            "Short Interest (%)",
        )
    else:
        st.info("No peer context data available.")

    with st.expander("Observation Context Scaffold"):
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
theme_code = "company_structure_review"
theme_title = "Company Structure Review"

# -------------------------------------------------------------------------------------------------
# Build Snapshot Insight
# -------------------------------------------------------------------------------------------------
company_structure_snapshot_insight = build_macro_insight_snapshot_company_structure_review(
    theme_code=theme_code,
    theme_title=theme_title,
    dataset_name=dataset_option,
    df=df,
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
    df["Company"].dropna().astype(str).tolist()
    if "Company" in df.columns
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
        snapshot_results=company_structure_snapshot_insight,
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

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
    "No trading, investment, valuation, or portfolio advice provided."
)
