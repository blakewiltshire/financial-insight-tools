# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

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
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import uuid

# -------------------------------------------------------------------------------------------------
# Visualisation Fallback Helpers
# -------------------------------------------------------------------------------------------------
def display_chart_with_fallback(
    fig: go.Figure,
    label: str = "Chart",
    allow_partial: bool = True,
    partial_warning: bool = False,
    custom_key: str = None
) -> None:
    """
    Displays a Plotly figure or emits a warning if data is missing or structurally empty.

    Args:
        fig (go.Figure): The Plotly chart to display.
        label (str): Logical name of the chart (used in messages and fallback key).
        allow_partial (bool): If True, renders charts even if some data components are missing.
        partial_warning (bool): If True, displays info message for partially rendered figures.
        custom_key (str): Optional Streamlit key. If None, a unique key is auto-generated.

    Returns:
        None
    """
    if not fig or not fig.data or not any(
        hasattr(trace, "y") and trace.y is not None and len(trace.y) > 0
        for trace in fig.data
    ):
        st.warning(
            f"⚠️ {label} not available: This visual could not be generated due to \
            insufficient or missing data."
        )
        return

    unique_key = custom_key if custom_key else f"{label}_{uuid.uuid4().hex}"

    st.plotly_chart(fig, width='stretch', key=unique_key)

# -------------------------------------------------------------------------------------------------
# Renders a line chart across all real or nominal economic data
# -------------------------------------------------------------------------------------------------
def plot_indicator_line_chart(df, y_column, title, yaxis_title, marker=False):
    df = df.copy()
    if "date" not in df.columns or y_column not in df.columns or df[y_column].dropna().empty:
        print(f"⚠️ Skipping plot — Missing or empty column: {y_column} or 'date'")
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df[y_column],
        mode="lines+markers" if marker else "lines",
        name=y_column
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        height=480,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Real GDP Visuals
# -------------------------------------------------------------------------------------------------

def plot_gdp_growth_comparison(df: pd.DataFrame) -> go.Figure:
    if "date" not in df.columns or df.dropna(how='all').empty:
        print("⚠️ Skipping chart — Insufficient GDP growth data")
        return None

    fig = go.Figure()

    if "Real GDP QoQ % Change" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["Real GDP QoQ % Change"],
            mode="lines+markers", name="Real GDP QoQ % Change",
            line={"width": 1.5, "color": "#1f77b4"}
        ))

    if "Real GDP YoY % Change" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["Real GDP YoY % Change"],
            mode="lines+markers", name="Real GDP YoY % Change",
            line={"width": 1.2, "color": '#ff7f0e', "dash": 'dot'}
        ))

    if "Real GDP QoQ Annualized" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["Real GDP QoQ Annualized"],
            mode="lines+markers", name="Real GDP QoQ Annualized",
            line={"width": 1.2, "color": '#2ca02c', "dash": 'dash'}
        ))

    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.update_layout(
        title="🧭 Real GDP Growth – Comparative View",
        xaxis_title="Date",
        yaxis_title="% Change",
        height=480,
        template="plotly_white"
    )
    return fig

def plot_gdp_real_level_with_extremes(
df: pd.DataFrame, value_column: str, title: str, yaxis_title: str) -> go.Figure:
    if value_column not in df.columns or df[value_column].dropna().empty:
        print(f"⚠️ Skipping chart — column '{value_column}' missing or empty.")
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[value_column],
        mode="lines", name=value_column,
        line={"color": 'darkgreen'}
    ))

    min_val = df[value_column].min()
    max_val = df[value_column].max()
    min_date = df[df[value_column] == min_val]["date"].iloc[0]
    max_date = df[df[value_column] == max_val]["date"].iloc[0]

    fig.add_trace(go.Scatter(x=[min_date], y=[min_val], mode="markers",
                             name="Visible Range Low", marker={"color": 'red', "size": 10}))
    fig.add_trace(go.Scatter(x=[max_date], y=[max_val], mode="markers",
                             name="Visible Range High", marker={"color": 'green', "size": 10}))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        yaxis_tickformat=",.0f",
        height=480,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# GDP Real – QoQ Growth with Rolling Average
# -------------------------------------------------------------------------------------------------
def plot_gdp_real_qoq_with_average(
    df: pd.DataFrame,
    column: str = "Real GDP (% Change QoQ)",
    window: int = 4
) -> go.Figure:
    """
    Plots real GDP QoQ change alongside a rolling average for trend smoothing.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and specified column.
        column (str): Real GDP QoQ change column.
        window (int): Rolling average window in quarters.

    Returns:
        go.Figure: Plotly line chart.
    """
    df = df.copy()
    if "date" not in df.columns or column not in df.columns:
        return go.Figure()

    df[f"{column} (Avg)"] = df[column].rolling(window).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df[column], mode="lines", name=column))
    fig.add_trace(go.Scatter(x=df["date"], y=df[f"{column} (Avg)"], mode="lines",
                             name=f"{window}-Q Avg", line={"dash": 'dot'}))

    fig.update_layout(
        title=f"{column} with {window}-Quarter Average",
        xaxis_title="Date",
        yaxis_title=column,
        height=480,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Nominal GDP – Level Plot
# -------------------------------------------------------------------------------------------------
def plot_gdp_nominal_level(
    df: pd.DataFrame,
    value_column: str = "Nominal GDP",
    title: str = "Nominal GDP Level",
    yaxis_title: str = "Billions (Local Currency)",
    height: int = 480,
    template: str = "plotly_white",
    yaxis_tickformat: str = ",.0f"
) -> go.Figure:
    """
    Plots nominal GDP level with visible range min/max markers.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and value_column.
        value_column (str): Column to plot.
        title (str): Chart title.
        yaxis_title (str): Label for y-axis.
        height (int): Chart height in pixels.
        template (str): Plotly theme.
        yaxis_tickformat (str): Format for y-axis values.

    Returns:
        go.Figure: Line chart with annotated extremes.
    """
    df = df.copy()
    if "date" not in df.columns or value_column not in df.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[value_column],
        mode="lines", name=value_column,
        line={"color": 'darkblue'}
    ))

    # Defensive check for empty series
    if df[value_column].dropna().empty:
        return fig

    min_val = df[value_column].min()
    max_val = df[value_column].max()
    try:
        min_date = df[df[value_column] == min_val]["date"].iloc[0]
        max_date = df[df[value_column] == max_val]["date"].iloc[0]
    except IndexError:
        return fig

    fig.add_trace(go.Scatter(x=[min_date], y=[min_val], mode="markers",
                             name="Visible Range Low", marker={"color": 'red', "size": 10}))
    fig.add_trace(go.Scatter(x=[max_date], y=[max_val], mode="markers",
                             name="Visible Range High", marker={"color": 'green', "size": 10}))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        yaxis_tickformat=yaxis_tickformat,
        height=height,
        template=template
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Nominal GDP – YoY Growth
# -------------------------------------------------------------------------------------------------
def plot_gdp_nominal_yoy_growth(df: pd.DataFrame) -> go.Figure:
    """
    Plots Year-on-Year % change in nominal GDP.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and 'Nominal GDP'.

    Returns:
        go.Figure: YoY growth chart for nominal GDP.
    """
    df = df.copy()
    if "date" not in df.columns or "Nominal GDP" not in df.columns:
        return go.Figure()

    df["YoY Nominal % Change"] = df["Nominal GDP"].pct_change(periods=4) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["YoY Nominal % Change"],
        mode="lines+markers",
        name="YoY Nominal GDP Growth",
        line={"color": '#636EFA', "width": 2}
    ))

    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        title="🧭 Nominal GDP – YoY Growth Rate",
        xaxis_title="Date",
        yaxis_title="% Change",
        height=480,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# GDP Component Breakdown Visuals (Defensive, Production-Grade)
# -------------------------------------------------------------------------------------------------

def plot_gdp_domestic_components_lines(df: pd.DataFrame) -> go.Figure:
    """
    Plots main domestic GDP components: consumption, investment, government spending.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and standard component columns.

    Returns:
        go.Figure: Multi-line Plotly chart.
    """
    df = df.copy()
    if "date" not in df.columns:
        return go.Figure()

    components = {
        "Real Personal Consumption Expenditures": "Personal Consumption",
        "Real Gross Private Domestic Investment": "Private Investment",
        "Government Consumption Expenditures and Gross Investment": "Government"
    }

    fig = go.Figure()
    plotted = False

    for column, label in components.items():
        if column in df.columns:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df[column],
                mode="lines+markers",
                name=label
            ))
            plotted = True

    if not plotted:
        return go.Figure()

    fig.update_layout(
        title="🧭 Domestic GDP Components – Consumption, Investment, Government",
        xaxis_title="Date",
        yaxis_title="Billions (Real, Local Currency)",
        yaxis_tickformat=",.0f",
        height=480,
        template="plotly_white"
    )
    return fig


def plot_gdp_external_sector_trade_lines(df: pd.DataFrame) -> go.Figure:
    """
    Plots real exports and imports of goods and services.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and trade series columns.

    Returns:
        go.Figure: Dual-line Plotly chart.
    """
    df = df.copy()
    required = ["Real Exports of Goods and Services", "Real Imports of Goods and Services"]
    if "date" not in df.columns or not all(col in df.columns for col in required):
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Real Exports of Goods and Services"],
        mode="lines+markers",
        name="Exports",
        line={"color": 'green', "width": 2}
    ))
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Real Imports of Goods and Services"],
        mode="lines+markers",
        name="Imports",
        line={"color": 'red', "width": 2, "dash": 'dot'}
    ))

    fig.update_layout(
        title="🌍 Real Exports vs Imports Over Time",
        xaxis_title="Date",
        yaxis_title="Billions (Real, Local Currency)",
        yaxis_tickformat=",.0f",
        height=480,
        template="plotly_white"
    )
    return fig


def plot_gdp_component_structure_area_share(df: pd.DataFrame) -> go.Figure:
    """
    Plots stacked area chart of GDP component shares over time.

    Args:
        df (pd.DataFrame): DataFrame with domestic component columns and 'date'.

    Returns:
        go.Figure: Area chart with percentage breakdown.
    """
    df = df.copy()
    components = [
        "Real Personal Consumption Expenditures",
        "Real Gross Private Domestic Investment",
        "Government Consumption Expenditures and Gross Investment"
    ]
    if "date" not in df.columns or not all(col in df.columns for col in components):
        return go.Figure()

    df["total"] = df[components].sum(axis=1)
    if df["total"].dropna().eq(0).all():
        return go.Figure()

    for col in components:
        df[f"{col} %"] = df[col] / df["total"] * 100

    fig = go.Figure()
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for i, col in enumerate(components):
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df[f"{col} %"],
            mode="lines",
            name=col.replace("Real ", ""),
            stackgroup="one",
            line={"width": 0.5},
            fillcolor=colors[i % len(colors)]
        ))

    fig.update_layout(
        title="📊 Relative GDP Component Share Over Time",
        xaxis_title="Date",
        yaxis_title="Share (%)",
        height=480,
        template="plotly_white"
    )
    return fig


def plot_gdp_component_growth_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Plots QoQ and YoY growth for all key GDP components including real GDP.

    Args:
        df (pd.DataFrame): DataFrame with 'date' and growth metric columns.

    Returns:
        go.Figure: Comparative growth chart.
    """
    df = df.copy()
    if "date" not in df.columns:
        return go.Figure()

    df["date"] = pd.to_datetime(df["date"])
    legend_name_map = {
        "Real GDP": "Real GDP",
        "Real Personal Consumption Expenditures": "Real Personal Consumption",
        "Real Gross Private Domestic Investment": "Real Private Investment",
        "Government Consumption Expenditures and Gross Investment": "Government",
        "Real Exports of Goods and Services": "Real Exports",
        "Real Imports of Goods and Services": "Real Imports"
    }

    fig = go.Figure()
    plotted = False

    for col in df.columns:
        if col.endswith("QoQ % Change") or col.endswith("YoY % Change"):
            base = col.replace(" QoQ % Change", "").replace(" YoY % Change", "")
            label = legend_name_map.get(base, base)
            style = "solid" if "QoQ" in col else "dot"
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df[col],
                mode="lines",
                name=f"{label} – {'QoQ' if 'QoQ' in col else 'YoY'}",
                line={"dash": style}
            ))
            plotted = True

    if not plotted:
        return go.Figure()

    fig.update_layout(
        title="📊 Comparative Growth of GDP Components (QoQ vs YoY)",
        xaxis_title="Date",
        yaxis_title="Growth Rate (%)",
        legend={
            "orientation": "h",
            "yanchor": "top",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
            "title": None,
            "font": {"size": 11}
        },
        template="plotly_white",
        height=520
    )
    return fig
