# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Universal Visualisation Engine — Economic Exploration Suite
-----------------------------------------------------------------

Defines the universal chart rendering functions for thematic modules (Themes 100–2100+)
within the Economic Exploration platform. This module serves as the foundation for
consistent charting across countries and themes.

✅ Role in the System:
- Provides reusable chart functions for any theme where local visuals are not extended.
- Ensures consistent UI presentation across all countries using shared indicators.
- Supports Streamlit tab structures and AI-export-ready visual formats.

🧠 System Design Notes:
- Visual rendering operates fully independently of indicator signals and insights.
- **Use Case selection controls chart rendering**, not indicator map output.
- Charts respond to the selected Use Case from `use_cases_XXX.py`.
- Chart data slices are passed via `df_map` based on timeframe logic configured in `visual_config_XXX.py`.
- Indicator signals (computed via `indicator_map_XXX.py`) are not used inside chart functions.

⚙️ Architecture Summary:
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
# Helper — Z-Score Normalisation
# -------------------------------------------------------------------------------------------------
def zscore_series(series: pd.Series) -> pd.Series:
    """
    Returns a z-score normalised version of a series.
    """
    series = series.dropna()
    if series.empty or series.std() == 0:
        return pd.Series(index=series.index, dtype=float)

    return (series - series.mean()) / series.std()


# -------------------------------------------------------------------------------------------------
# Forward Production Conditions — Trend Comparison Chart
# -------------------------------------------------------------------------------------------------
def plot_forward_production_conditions_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders a standardised overlay for:
    - Business Conditions Diffusion Index
    - Industrial Production Index
    - Manufacturing Durable Goods Orders
    """

    required_cols = [
        "date",
        "Business Conditions Diffusion Index",
        "Industrial Production Index",
        "Manufacturing Durable Goods Orders"
    ]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    plot_df = df[required_cols].copy().dropna()

    if plot_df.empty:
        return go.Figure()

    plot_df["Business Conditions Diffusion Index (Z)"] = zscore_series(
        plot_df["Business Conditions Diffusion Index"]
    )
    plot_df["Industrial Production Index (Z)"] = zscore_series(
        plot_df["Industrial Production Index"]
    )
    plot_df["Manufacturing Durable Goods Orders (Z)"] = zscore_series(
        plot_df["Manufacturing Durable Goods Orders"]
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Business Conditions Diffusion Index (Z)"],
        mode="lines",
        name="Business Conditions Diffusion Index"
    ))

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Industrial Production Index (Z)"],
        mode="lines",
        name="Industrial Production Index"
    ))

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Manufacturing Durable Goods Orders (Z)"],
        mode="lines",
        name="Manufacturing Durable Goods Orders"
    ))

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="grey",
        line_width=1
    )

    fig.update_layout(
        title="Forward Production Conditions",
        xaxis_title="Date",
        yaxis_title="Trend Comparison",
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
# Single-Series Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_single_series_levels_chart(
    df: pd.DataFrame,
    column_name: str,
    chart_title: str,
    yaxis_title: str
) -> go.Figure:
    """
    Renders a single-series levels chart with a simple trend line.
    """
    required_cols = ["date", column_name]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    plot_df = df[required_cols].copy().dropna()

    if plot_df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df[column_name],
        mode="lines",
        name=column_name
    ))

    try:
        import numpy as np

        y = plot_df[column_name].values
        x = np.arange(len(y))

        coeffs = np.polyfit(x, y, 1)
        trend = coeffs[0] * x + coeffs[1]

        fig.add_trace(go.Scatter(
            x=plot_df["date"],
            y=trend,
            mode="lines",
            name="Trend",
            line=dict(color="grey", dash="dash", width=1)
        ))
    except Exception:
        pass

    fig.update_layout(
        title=chart_title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
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
# Business Conditions Diffusion Index — Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_business_conditions_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Business Conditions Diffusion Index levels chart.
    """
    return plot_single_series_levels_chart(
        df=df,
        column_name="Business Conditions Diffusion Index",
        chart_title="Business Conditions Diffusion Index",
        yaxis_title="Levels"
    )


# -------------------------------------------------------------------------------------------------
# Industrial Production Index — Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_industrial_production_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Industrial Production Index levels chart.
    """
    return plot_single_series_levels_chart(
        df=df,
        column_name="Industrial Production Index",
        chart_title="Industrial Production Index",
        yaxis_title="Levels"
    )


# -------------------------------------------------------------------------------------------------
# Manufacturing Durable Goods Orders — Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_manufacturing_orders_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Manufacturing Durable Goods Orders levels chart.
    """
    return plot_single_series_levels_chart(
        df=df,
        column_name="Manufacturing Durable Goods Orders",
        chart_title="Manufacturing Durable Goods Orders",
        yaxis_title="Levels"
    )

# -------------------------------------------------------------------------------------------------
# Services Activity Conditions — Trend Comparison Chart
# -------------------------------------------------------------------------------------------------
def plot_services_activity_conditions_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders a standardised overlay for:
    - Business Conditions Diffusion Index
    - Services Consumption (Nominal)
    - Services Consumption (Real)
    """

    required_cols = [
        "date",
        "Business Conditions Diffusion Index",
        "Services Consumption (Nominal)",
        "Services Consumption (Real)"
    ]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    plot_df = df[required_cols].copy().dropna()

    if plot_df.empty:
        return go.Figure()

    plot_df["Business Conditions Diffusion Index (Z)"] = zscore_series(
        plot_df["Business Conditions Diffusion Index"]
    )
    plot_df["Services Consumption (Nominal) (Z)"] = zscore_series(
        plot_df["Services Consumption (Nominal)"]
    )
    plot_df["Services Consumption (Real) (Z)"] = zscore_series(
        plot_df["Services Consumption (Real)"]
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Business Conditions Diffusion Index (Z)"],
        mode="lines",
        name="Business Conditions Diffusion Index"
    ))

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Services Consumption (Nominal) (Z)"],
        mode="lines",
        name="Services Consumption (Nominal)"
    ))

    fig.add_trace(go.Scatter(
        x=plot_df["date"],
        y=plot_df["Services Consumption (Real) (Z)"],
        mode="lines",
        name="Services Consumption (Real)"
    ))

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="grey",
        line_width=1
    )

    fig.update_layout(
        title="Services Activity Conditions",
        xaxis_title="Date",
        yaxis_title="Trend Comparison",
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
# Services Consumption (Nominal) — Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_services_consumption_nominal_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Services Consumption (Nominal) levels chart.
    """
    return plot_single_series_levels_chart(
        df=df,
        column_name="Services Consumption (Nominal)",
        chart_title="Services Consumption (Nominal)",
        yaxis_title="Levels"
    )


# -------------------------------------------------------------------------------------------------
# Services Consumption (Real) — Levels Chart
# -------------------------------------------------------------------------------------------------
def plot_services_consumption_real_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Services Consumption (Real) levels chart.
    """
    return plot_single_series_levels_chart(
        df=df,
        column_name="Services Consumption (Real)",
        chart_title="Services Consumption (Real)",
        yaxis_title="Levels"
    )
