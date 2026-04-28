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
# Inflation Comparison Chart
# -------------------------------------------------------------------------------------------------
def plot_inflation_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders headline and core inflation across consumer and producer layers.
    """

    required_cols = ["date", "Headline CPI", "Core CPI", "Headline PPI", "Core PPI"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Headline CPI"],
        mode="lines",
        name="Headline CPI"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Core CPI"],
        mode="lines",
        name="Core CPI"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Headline PPI"],
        mode="lines",
        name="Headline PPI"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Core PPI"],
        mode="lines",
        name="Core PPI"
    ))

    fig.update_layout(
        title="Inflation Pressure and Transmission",
        xaxis_title="Date",
        yaxis_title="Index Level",
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
# Consumer Inflation Chart
# -------------------------------------------------------------------------------------------------
def plot_consumer_inflation_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders headline and core consumer inflation.
    """

    required_cols = ["date", "Headline CPI", "Core CPI"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Headline CPI"],
        mode="lines",
        name="Headline CPI"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Core CPI"],
        mode="lines",
        name="Core CPI"
    ))

    fig.update_layout(
        title="Consumer Inflation",
        xaxis_title="Date",
        yaxis_title="Index Level",
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
# Producer Inflation Chart
# -------------------------------------------------------------------------------------------------
def plot_producer_inflation_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders headline and core producer inflation.
    """

    required_cols = ["date", "Headline PPI", "Core PPI"]
    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Headline PPI"],
        mode="lines",
        name="Headline PPI"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Core PPI"],
        mode="lines",
        name="Core PPI"
    ))

    fig.update_layout(
        title="Producer Inflation",
        xaxis_title="Date",
        yaxis_title="Index Level",
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
