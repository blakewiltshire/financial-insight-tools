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
# 📦 Imports
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import uuid

# -------------------------------------------------------------------------------------------------
# 🧩 Chart Display Wrapper with Fallback
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
    st.plotly_chart(fig, width='stretch', key=unique_key)

    if allow_partial and partial_warning:
        st.info(f"ℹ️ {label} displayed with partial data.")

# -------------------------------------------------------------------------------------------------
# 📊 Generic Plot — Signal A: Basic Time Series
# -------------------------------------------------------------------------------------------------
def plot_signal_a_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders a simple time series line chart for 'Signal A'.
    """
    if "date" not in df.columns or "Signal A" not in df.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Signal A"],
        mode="lines+markers", name="Signal A"
    ))

    fig.update_layout(
        title="🔹 Signal A — Time Series Chart",
        xaxis_title="Date",
        yaxis_title="Value",
        height=400,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# 📊 Generic Plot — Signal B: Rolling Average
# -------------------------------------------------------------------------------------------------
def plot_signal_b_chart(df: pd.DataFrame, window: int = 3) -> go.Figure:
    """
    Renders 'Signal B' with an optional rolling average overlay.
    """
    if "date" not in df.columns or "Signal B" not in df.columns:
        return go.Figure()

    df = df.copy()
    df["Rolling Avg"] = df["Signal B"].rolling(window).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Signal B"],
        mode="lines", name="Signal B"
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Rolling Avg"],
        mode="lines", name=f"{window}-Period Avg",
        line={"dash": "dot"}
    ))

    fig.update_layout(
        title="🔹 Signal B — With Rolling Average",
        xaxis_title="Date",
        yaxis_title="Value",
        height=400,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# 📊 Generic Plot — Signal C: Band Highlight
# -------------------------------------------------------------------------------------------------
def plot_signal_c_chart(df: pd.DataFrame) -> go.Figure:
    """
    Plots 'Signal C' with highlighted bands (e.g., thresholds or confidence zone).
    """
    if "date" not in df.columns or "Signal C" not in df.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Signal C"],
        mode="lines", name="Signal C"
    ))

    # Example band (e.g., neutral zone between -1 and 1)
    fig.add_shape(type="rect", xref="paper", yref="y",
                  x0=0, x1=1, y0=-1, y1=1,
                  fillcolor="LightGray", opacity=0.3, line_width=0)

    fig.update_layout(
        title="🔹 Signal C — With Neutral Band",
        xaxis_title="Date",
        yaxis_title="Value",
        height=400,
        template="plotly_white"
    )
    return fig
