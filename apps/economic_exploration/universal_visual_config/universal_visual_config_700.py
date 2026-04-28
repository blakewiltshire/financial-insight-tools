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
# Trade Flows Chart
# -------------------------------------------------------------------------------------------------
def plot_trade_flows_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders exports and imports of goods and services.
    """
    required_cols = ["date", "Exports of Goods and Services", "Imports of Goods and Services"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Exports of Goods and Services"],
        mode="lines",
        name="Exports of Goods and Services"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Imports of Goods and Services"],
        mode="lines",
        name="Imports of Goods and Services"
    ))

    fig.update_layout(
        title="Trade Flows",
        xaxis_title="Date",
        yaxis_title="Millions of Dollars",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Trade Balance Chart
# -------------------------------------------------------------------------------------------------
def plot_trade_balance_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders trade balance across total, goods, and services layers.
    """
    required_cols = [
        "date",
        "Trade Balance Goods and Services",
        "Trade Balance Goods",
        "Trade Balance Services"
    ]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Trade Balance Goods and Services"],
        mode="lines",
        name="Trade Balance Goods and Services"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Trade Balance Goods"],
        mode="lines",
        name="Trade Balance Goods"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Trade Balance Services"],
        mode="lines",
        name="Trade Balance Services"
    ))

    fig.update_layout(
        title="Trade Balance Structure",
        xaxis_title="Date",
        yaxis_title="Millions of Dollars",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Reserve Layer Chart
# -------------------------------------------------------------------------------------------------
def plot_reserve_layer_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders official reserves excluding gold.
    """
    required_cols = ["date", "Official Reserves Excluding Gold"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Official Reserves Excluding Gold"],
        mode="lines",
        name="Official Reserves Excluding Gold"
    ))

    fig.update_layout(
        title="Reserve Layer Support",
        xaxis_title="Date",
        yaxis_title="Millions of Dollars",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Current Account Anchor Chart
# -------------------------------------------------------------------------------------------------
def plot_current_account_anchor_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the current account balance.
    """
    required_cols = ["date", "Current Account Balance"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Current Account Balance"],
        mode="lines",
        name="Current Account Balance"
    ))

    fig.update_layout(
        title="Current Account Anchor",
        xaxis_title="Date",
        yaxis_title="Billions / Millions (source scale)",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Net International Position Chart
# -------------------------------------------------------------------------------------------------
def plot_net_international_position_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders quarterly net international investment position.
    """
    required_cols = ["date", "Net International Investment Position Quarterly"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Net International Investment Position Quarterly"],
        mode="lines",
        name="Net International Investment Position Quarterly"
    ))

    fig.update_layout(
        title="Net International Position",
        xaxis_title="Date",
        yaxis_title="Millions of Dollars",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Investment Income Pressure Chart
# -------------------------------------------------------------------------------------------------
def plot_investment_income_pressure_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders primary investment income payments.
    """
    required_cols = ["date", "Primary Investment Income payments"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Primary Investment Income payments"],
        mode="lines",
        name="Primary Investment Income payments"
    ))

    fig.update_layout(
        title="Investment Income Pressure",
        xaxis_title="Date",
        yaxis_title="Millions of Dollars",
        height=420,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig
