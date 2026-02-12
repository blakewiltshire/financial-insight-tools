# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

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
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import uuid

# -------------------------------------------------------------------------------------------------
# ✅ Fallback Chart Display Utility (Platinum-grade key management)
# -------------------------------------------------------------------------------------------------
def display_chart_with_fallback(fig, label: str, partial_warning: bool = False, custom_key: str = None):
    """
    Safely display a Plotly chart or fallback placeholder with unique Streamlit key.

    Args:
        fig (go.Figure): Chart figure to display.
        label (str): Logical label of chart.
        partial_warning (bool): Display a soft warning if data may be partial.
        custom_key (str): Optional explicit Streamlit key; if not provided, unique key is generated.

    """
    if fig and fig.data:
        if partial_warning:
            st.caption("⚠️ Partial data — check timeframe or data coverage.")
        unique_key = custom_key if custom_key else f"{label}_{uuid.uuid4().hex}"
        st.plotly_chart(fig, use_container_width=True, key=unique_key)
    else:
        st.info("No chart available — insufficient data or unsupported configuration.")

# -------------------------------------------------------------------------------------------------
# 📈 Reusable Chart Functions
# -------------------------------------------------------------------------------------------------
def plot_labour_line_chart(df: pd.DataFrame, column: str, title: str, yaxis_title: str) -> go.Figure:
    """
    Generic line chart for labour market indicators.

    Args:
        df (pd.DataFrame): Must contain 'date' and the column specified.
        column (str): Column to chart.
        title (str): Chart title.
        yaxis_title (str): Axis label.

    Returns:
        go.Figure: Plotly chart.
    """
    df = df.copy()
    if "date" not in df.columns or column not in df.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df[column],
        mode="lines+markers",
        name=column,
        line={"color": "#1f77b4"}
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        template="plotly_white",
        height=460
    )
    return fig


def plot_labour_with_extremes(df: pd.DataFrame, column: str, title: str, yaxis_title: str) -> go.Figure:
    """
    Line chart with visual annotations for min/max points.

    Args:
        df (pd.DataFrame): Must contain 'date' and the column specified.
        column (str): Column to chart.
        title (str): Chart title.
        yaxis_title (str): Axis label.

    Returns:
        go.Figure: Plotly chart.
    """
    df = df.copy()
    if "date" not in df.columns or column not in df.columns or df[column].dropna().empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df[column],
        mode="lines",
        name=column,
        line={"color": "darkblue"}
    ))

    min_val = df[column].min()
    max_val = df[column].max()

    try:
        min_date = df[df[column] == min_val]["date"].iloc[0]
        max_date = df[df[column] == max_val]["date"].iloc[0]
    except IndexError:
        return fig

    fig.add_trace(go.Scatter(x=[min_date], y=[min_val], mode="markers",
                             name="Visible Range Low", marker={"color": "red", "size": 9}))
    fig.add_trace(go.Scatter(x=[max_date], y=[max_val], mode="markers",
                             name="Visible Range High", marker={"color": "green", "size": 9}))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        template="plotly_white",
        height=460
    )
    return fig
