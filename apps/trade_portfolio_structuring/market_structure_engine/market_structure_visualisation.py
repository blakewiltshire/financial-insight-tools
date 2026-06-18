# -------------------------------------------------------------------------------------------------
# Market Structure Visualisation
# -------------------------------------------------------------------------------------------------
"""Rendering helpers for Market Structure Review."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Tables
# -------------------------------------------------------------------------------------------------
def render_market_structure_table(profile_df: pd.DataFrame) -> None:
    """Render the market structure profile table."""
    display_cols = [
        "Company",
        "Ticker",
        "Exchange",
        "Structure_Type",
        "Ownership_Structure",
        "Float_Structure",
        "Supply_Structure",
        "Institutional_Participation",
        "Index_Eligibility",
        "Major_Supply_Events",
        "Structural_Notes",
    ]

    available_cols = [col for col in display_cols if col in profile_df.columns]

    st.dataframe(
        profile_df[available_cols],
        width="stretch",
        hide_index=True,
    )


def render_supply_events_table(events_df: pd.DataFrame) -> None:
    """Render the market structure supply events table."""
    display_cols = [
        "Company",
        "Ticker",
        "Event_Type",
        "Event_Date",
        "Event_Label",
        "Portion_Unlocked_Pct",
        "Condition",
        "Source_Note",
    ]

    available_cols = [col for col in display_cols if col in events_df.columns]

    st.dataframe(
        events_df[available_cols],
        width="stretch",
        hide_index=True,
    )


def render_focus_supply_events_table(events_df: pd.DataFrame, focus_ticker: str) -> None:
    """Render supply events for the selected focus asset."""
    if events_df.empty or "Ticker" not in events_df.columns:
        st.info("No supply event data available.")
        return

    focus_events_df = events_df[
        events_df["Ticker"].astype(str).str.strip().str.upper() == str(focus_ticker).upper()
    ].copy()

    if focus_events_df.empty:
        st.info("No mapped supply events found for the selected focus asset.")
        return

    render_supply_events_table(focus_events_df)

# -------------------------------------------------------------------------------------------------
# Panels
# -------------------------------------------------------------------------------------------------
def render_focus_asset_panels(summary_payload: dict) -> None:
    """Render focus-asset DSS context panels."""
    focus_context = summary_payload.get("observation_context", {}).get("focus_asset_context", {})
    asset = focus_context.get("asset", {})

    st.markdown("### Focus Asset Structure")
    st.caption(
        "Review the selected asset across ownership, float, supply, participation, and index context."
    )

    st.markdown(
        f"**{asset.get('company', 'N/A')} ({asset.get('ticker', 'N/A')})**  "
        f"— {asset.get('exchange', 'N/A')} · {asset.get('structure_type', 'N/A')}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Ownership Structure")
        st.write(focus_context.get("ownership_structure", "N/A"))

        st.markdown("#### Float Structure")
        st.write(focus_context.get("float_structure", "N/A"))

        st.markdown("#### Institutional Participation")
        st.write(focus_context.get("institutional_participation", "N/A"))

    with col2:
        st.markdown("#### Supply Structure")
        st.write(focus_context.get("supply_structure", "N/A"))

        st.markdown("#### Index Eligibility")
        st.write(focus_context.get("index_eligibility", "N/A"))

        st.markdown("#### Structural Notes")
        st.write(focus_context.get("structural_notes", "N/A"))


def render_structure_context_panels(summary_payload: dict) -> None:
    """Render DSS-style context panels."""
    st.markdown("### AI Handoff Context")
    st.caption(
        "Review focus-asset and comparison context prepared for downstream observation and AI export."
    )

    focus_context = summary_payload.get("observation_context", {}).get("focus_asset_context", {})
    comparison_context = summary_payload.get("observation_context", {}).get("comparison_context", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Focus Asset Context")
        st.json(focus_context)

    with col2:
        st.markdown("#### Comparison Context")
        st.json(comparison_context)

    st.markdown("#### Perspective Lenses")
    st.json(summary_payload.get("observation_context", {}).get("perspective_lenses", {}))
