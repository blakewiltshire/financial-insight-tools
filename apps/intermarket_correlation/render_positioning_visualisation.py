# -------------------------------------------------------------------------------------------------
# Positioning Visualisation
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Visualisation helpers for the Positioning & Crowding module.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_positioning_overlay(overlay_df: pd.DataFrame) -> None:
    """
    Renders asset price against positioning commitment using Net Position Share (%) as the
    primary positioning surface.

    Net Position Share (%) = open_interest_long_pct - open_interest_short_pct

    Purpose:
    - Show whether price is aligning with speculative commitment
    - Surface divergence between market behaviour and positioning
    - Avoid using raw net contracts as the primary overlay measure
    """
    if overlay_df.empty:
        st.info("No overlay data available.")
        return

    chart_df = overlay_df.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"], errors="coerce")
    chart_df = chart_df.dropna(subset=["date"]).sort_values("date")

    # Build Net Position Share (%) if not already present
    if "net_position_share_pct" not in chart_df.columns:
        if all(col in chart_df.columns for col in ["open_interest_long_pct", "open_interest_short_pct"]):
            chart_df["net_position_share_pct"] = (
                chart_df["open_interest_long_pct"].fillna(0)
                - chart_df["open_interest_short_pct"].fillna(0)
            )

    if "net_position_share_pct" not in chart_df.columns and "market_price" not in chart_df.columns:
        st.info("No positioning or market price data available.")
        return

    fig = go.Figure()

    if "net_position_share_pct" in chart_df.columns and chart_df["net_position_share_pct"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["net_position_share_pct"],
                mode="lines",
                name="Net Position Share (%)",
                yaxis="y1",
            )
        )

    if "market_price" in chart_df.columns and chart_df["market_price"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["market_price"],
                mode="lines",
                name="Market Price",
                yaxis="y2",
            )
        )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_width=1,
        annotation_text="Zero Line",
        annotation_position="top right",
    )

    fig.update_layout(
        title="Positioning vs Market Overlay",
        xaxis_title="Date",
        yaxis=dict(title="Net Position Share (%)"),
        yaxis2=dict(
            title="Market Price",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h"),
        margin=dict(l=30, r=30, t=50, b=30),
    )

    st.plotly_chart(fig, width="stretch")


def render_positioning_extremes_panel(positioning_df: pd.DataFrame) -> None:
    """
    Renders a crowding / reversal-pressure surface using Net Position Share (%) as the primary
    signal, with historical extreme bands and a positioning-turn marker.

    Purpose:
    - Show whether positioning is near crowded conditions
    - Show whether speculative commitment has crossed through zero
    - Complement the price overlay rather than duplicating it
    """
    if positioning_df.empty:
        st.info("No positioning data available.")
        return

    chart_df = positioning_df.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"], errors="coerce")
    chart_df = chart_df.dropna(subset=["date"]).sort_values("date")

    # Build Net Position Share (%) if not already present
    if "net_position_share_pct" not in chart_df.columns:
        if all(col in chart_df.columns for col in ["open_interest_long_pct", "open_interest_short_pct"]):
            chart_df["net_position_share_pct"] = (
                chart_df["open_interest_long_pct"].fillna(0)
                - chart_df["open_interest_short_pct"].fillna(0)
            )

    if "net_position_share_pct" not in chart_df.columns or chart_df["net_position_share_pct"].dropna().empty:
        st.info("No positioning share data available.")
        return

    net_position_share_series = chart_df["net_position_share_pct"].dropna()
    upper_extreme = net_position_share_series.quantile(0.90)
    lower_extreme = net_position_share_series.quantile(0.10)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["date"],
            y=chart_df["net_position_share_pct"],
            mode="lines",
            name="Net Position Share (%)",
            line=dict(width=2),
        )
    )

    # Optional raw net positioning line, hidden by default
    if "net_position" in chart_df.columns and chart_df["net_position"].notna().any():
        fig.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["net_position"],
                mode="lines",
                name="Net Positioning",
                visible="legendonly",
                yaxis="y2",
                line=dict(dash="dot"),
            )
        )

    fig.add_hrect(
        y0=upper_extreme,
        y1=float(net_position_share_series.max()),
        fillcolor="rgba(239, 68, 68, 0.10)",
        line_width=0,
        annotation_text="Upper Extreme",
        annotation_position="top left",
    )

    fig.add_hrect(
        y0=float(net_position_share_series.min()),
        y1=lower_extreme,
        fillcolor="rgba(59, 130, 246, 0.10)",
        line_width=0,
        annotation_text="Lower Extreme",
        annotation_position="bottom left",
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_width=1,
        annotation_text="Zero Line",
        annotation_position="top right",
    )

    # Positioning turn marker when Net Position Share (%) crosses zero
    if len(chart_df) >= 2:
        turn_valid = chart_df[["date", "net_position_share_pct"]].dropna()
        if len(turn_valid) >= 2:
            prev_val = turn_valid["net_position_share_pct"].iloc[-2]
            curr_val = turn_valid["net_position_share_pct"].iloc[-1]

            if (prev_val <= 0 < curr_val) or (prev_val >= 0 > curr_val):
                fig.add_trace(
                    go.Scatter(
                        x=[turn_valid["date"].iloc[-1]],
                        y=[turn_valid["net_position_share_pct"].iloc[-1]],
                        mode="markers",
                        marker=dict(size=11, symbol="diamond"),
                        name="Positioning Turn",
                    )
                )

    fig.update_layout(
        title="Crowding Extremes and Positioning Turn",
        xaxis_title="Date",
        yaxis=dict(title="Net Position Share (%)"),
        yaxis2=dict(
            title="Net Positioning",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h"),
        margin=dict(l=30, r=30, t=50, b=30),
    )

    st.plotly_chart(fig, width="stretch")
