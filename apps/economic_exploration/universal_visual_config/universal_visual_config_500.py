# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Visualisation Engine — Economic Exploration Suite
-----------------------------------------------------------------

Defines the universal chart rendering functions for thematic modules (Themes 100–2100+)
within the Economic Exploration platform. This module serves as the foundation for
consistent charting across countries and themes.

Role in the System:
- Provides reusable chart functions for any theme where local visuals are not extended.
- Ensures consistent UI presentation across all countries using shared indicators.
- Supports Streamlit tab structures and AI-export-ready visual formats.

System Design Notes:
- Visual rendering operates fully independently of indicator signals and insights.
- **Use Case selection controls chart rendering**, not indicator map output.
- Charts respond to the selected Use Case from `use_cases_XXX.py`.
- Chart data slices are passed via `df_map` based on timeframe logic configured in `visual_config_XXX.py`.
- Indicator signals (computed via `indicator_map_XXX.py`) are not used inside chart functions.

Architecture Summary:
- Universal visuals serve as default chart renderers across all countries.
- Local visual_config modules (e.g., `visuals_100.py`, `visuals_200.py`) can optionally override and extend visuals.
- Each Use Case maps to one or more visual tabs and subtabs defined within local visual_config files.
- Chart keys are uniquely managed using `display_chart_with_fallback()` to prevent Streamlit key collisions.
- Visual system is fully modular, country-agnostic, and AI export-compatible.

Usage:
- Universal visual functions are imported automatically by the main theme modules.
- Local visual dispatchers dynamically call universal functions when extending visuals.
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
import uuid
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -------------------------------------------------------------------------------------------------
# Chart Display Wrapper with Fallback
# -------------------------------------------------------------------------------------------------
def display_chart_with_fallback(
    fig: go.Figure,
    label: str = "Chart",
    allow_partial: bool = True,
    partial_warning: bool = False,
    custom_key: str = None
) -> None:
    """
    Displays a Plotly figure or shows a warning if data is invalid or empty.
    """
    if not fig or not fig.data or not any(
        hasattr(trace, "y") and trace.y is not None and len(trace.y) > 0
        for trace in fig.data
    ):
        st.warning(f"⚠️ {label} not available — no data or rendering issue.")
        return

    unique_key = custom_key if custom_key else f"{label}_{uuid.uuid4().hex}"
    st.plotly_chart(fig, width="stretch", key=unique_key)

    if allow_partial and partial_warning:
        st.info(f"ℹ️ {label} displayed with partial data.")


# -------------------------------------------------------------------------------------------------
# Money Supply and Velocity Dynamics Charts
# -------------------------------------------------------------------------------------------------
def plot_money_supply_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders M1 and M2 money supply.
    """
    required_cols = ["date", "M1 Money Supply", "M2 Money Supply"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["M1 Money Supply"],
        mode="lines",
        name="M1 Money Supply"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["M2 Money Supply"],
        mode="lines",
        name="M2 Money Supply"
    ))

    fig.update_layout(
        title="Money Supply",
        xaxis_title="Date",
        yaxis_title="Level",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def plot_money_velocity_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders M1 and M2 money velocity.
    """
    required_cols = ["date", "M1 Money Velocity", "M2 Money Velocity"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["M1 Money Velocity"],
        mode="lines",
        name="M1 Money Velocity"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["M2 Money Velocity"],
        mode="lines",
        name="M2 Money Velocity"
    ))

    fig.update_layout(
        title="Money Velocity",
        xaxis_title="Date",
        yaxis_title="Velocity",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Interest Rate Regime and Transmission Charts
# -------------------------------------------------------------------------------------------------
def plot_policy_rate_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders Central Bank Policy Rate.
    """
    required_cols = ["date", "Central Bank Policy Rate"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Central Bank Policy Rate"],
        mode="lines",
        name="Central Bank Policy Rate"
    ))

    fig.update_layout(
        title="Policy Rate Positioning",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=420,
        template="plotly_white"
    )

    return fig


def plot_funding_conditions_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders overnight funding and short funding averages.
    """
    required_cols = [
        "date",
        "Overnight Funding Rate",
        "30-Day Overnight Funding Average",
        "90-Day Overnight Funding Average"
    ]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Overnight Funding Rate"],
        mode="lines",
        name="Overnight Funding Rate"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["30-Day Overnight Funding Average"],
        mode="lines",
        name="30-Day Overnight Funding Average"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["90-Day Overnight Funding Average"],
        mode="lines",
        name="90-Day Overnight Funding Average"
    ))

    fig.update_layout(
        title="Funding Rate Conditions",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def plot_lending_and_mortgage_chart(df_daily: pd.DataFrame, df_weekly: pd.DataFrame) -> go.Figure:
    """
    Renders bank lending rate and mortgage rate conditions.
    """
    fig = go.Figure()

    if df_daily is not None and not df_daily.empty and all(
        col in df_daily.columns for col in ["date", "Prime Lending Rate"]
    ):
        fig.add_trace(go.Scatter(
            x=df_daily["date"],
            y=df_daily["Prime Lending Rate"],
            mode="lines",
            name="Prime Lending Rate"
        ))

    if df_weekly is not None and not df_weekly.empty and all(
        col in df_weekly.columns for col in ["date", "Long-Term Mortgage Rate"]
    ):
        fig.add_trace(go.Scatter(
            x=df_weekly["date"],
            y=df_weekly["Long-Term Mortgage Rate"],
            mode="lines",
            name="Long-Term Mortgage Rate"
        ))

    if not fig.data:
        return go.Figure()

    fig.update_layout(
        title="Lending and Mortgage Conditions",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def plot_curve_structure_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders yield curve spread and 10-year sovereign yield.
    """
    required_cols = ["date", "Yield Curve Spread", "10-Year Sovereign Yield"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Yield Curve Spread"],
        mode="lines",
        name="Yield Curve Spread"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["10-Year Sovereign Yield"],
        mode="lines",
        name="10-Year Sovereign Yield",
        yaxis="y2"
    ))

    fig.update_layout(
        title="Treasury Curve Structure",
        xaxis_title="Date",
        yaxis=dict(title="Spread (%)"),
        yaxis2=dict(
            title="10-Year Yield (%)",
            overlaying="y",
            side="right"
        ),
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def plot_real_policy_proxy_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders effective and Policy Rate Proxy.
    """
    required_cols = ["date", "Effective Policy Rate", "Policy Rate Proxy"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Effective Policy Rate"],
        mode="lines",
        name="Effective Policy Rate"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Policy Rate Proxy"],
        mode="lines",
        name="Policy Rate Proxy"
    ))

    fig.update_layout(
        title="Real Policy Rate Proxy",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
