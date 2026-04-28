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
# Housing Construction Pipeline — Multi-Series Chart
# -------------------------------------------------------------------------------------------------
def plot_housing_pipeline_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Housing Construction Pipeline chart with:
    - Housing Units Authorized
    - Housing Units Started
    - Housing Units Completed
    - Linear trend line for Housing Units Authorized
    """

    required_cols = [
        "date",
        "Housing Units Authorized",
        "Housing Units Started",
        "Housing Units Completed"
    ]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Housing Units Authorized"],
        mode="lines",
        name="Housing Units Authorized"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Housing Units Started"],
        mode="lines",
        name="Housing Units Started"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Housing Units Completed"],
        mode="lines",
        name="Housing Units Completed"
    ))

    try:
        import numpy as np

        y = df["Housing Units Authorized"].values
        x = np.arange(len(y))

        coeffs = np.polyfit(x, y, 1)
        trend = coeffs[0] * x + coeffs[1]

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=trend,
            mode="lines",
            name="Authorized Trend",
            line=dict(color="grey", dash="dash", width=1)
        ))
    except Exception:
        pass

    fig.update_layout(
        title="Housing Construction Pipeline",
        xaxis_title="Date",
        yaxis_title="Units (SAAR)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Mortgage Financing Conditions — Single-Series Chart
# -------------------------------------------------------------------------------------------------
def plot_mortgage_financing_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Mortgage Financing Conditions chart with:
    - Long-Term Mortgage Rate
    - Linear trend line
    """

    required_cols = ["date", "Long-Term Mortgage Rate"]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Long-Term Mortgage Rate"],
        mode="lines",
        name="Long-Term Mortgage Rate"
    ))

    try:
        import numpy as np

        y = df["Long-Term Mortgage Rate"].values
        x = np.arange(len(y))

        coeffs = np.polyfit(x, y, 1)
        trend = coeffs[0] * x + coeffs[1]

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=trend,
            mode="lines",
            name="Mortgage Rate Trend",
            line=dict(color="grey", dash="dash", width=1)
        ))
    except Exception:
        pass

    fig.update_layout(
        title="Mortgage Financing Conditions",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Yield Curve Structure — Single-Series Chart
# -------------------------------------------------------------------------------------------------
def plot_yield_curve_structure_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders the Yield Curve Structure chart with:
    - Yield Curve Spread
    - Zero reference line
    - Linear trend line
    """

    required_cols = ["date", "Yield Curve Spread"]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Yield Curve Spread"],
        mode="lines",
        name="Yield Curve Spread"
    ))

    fig.add_hline(y=0, line_dash="dot", line_color="grey", line_width=1)

    try:
        import numpy as np

        y = df["Yield Curve Spread"].values
        x = np.arange(len(y))

        coeffs = np.polyfit(x, y, 1)
        trend = coeffs[0] * x + coeffs[1]

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=trend,
            mode="lines",
            name="Curve Trend",
            line=dict(color="grey", dash="dash", width=1)
        ))
    except Exception:
        pass

    fig.update_layout(
        title="Yield Curve Structure",
        xaxis_title="Date",
        yaxis_title="Spread (%)",
        height=420,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Sovereign Debt Sustainability — Dual-Axis Chart
# -------------------------------------------------------------------------------------------------
def plot_sovereign_debt_sustainability_chart(df_quarterly: pd.DataFrame, df_annual: pd.DataFrame) -> go.Figure:
    """
    Renders sovereign debt sustainability using:
    - Left axis: Sovereign Debt % GDP
    - Right axis: Government Fiscal Balance, Government Interest Outlays
    """
    fig = go.Figure()

    if df_quarterly is not None and not df_quarterly.empty:
        if "Sovereign Debt Percentage of GDP" in df_quarterly.columns:
            fig.add_trace(go.Scatter(
                x=df_quarterly["date"],
                y=df_quarterly["Sovereign Debt Percentage of GDP"],
                mode="lines",
                name="Sovereign Debt % GDP",
                yaxis="y1"
            ))

    if df_annual is not None and not df_annual.empty:
        if "Government Fiscal Balance" in df_annual.columns:
            fig.add_trace(go.Bar(
                x=df_annual["date"],
                y=df_annual["Government Fiscal Balance"],
                name="Government Fiscal Balance",
                yaxis="y2",
                opacity=0.55
            ))

        if "Government Interest Outlays" in df_annual.columns:
            fig.add_trace(go.Scatter(
                x=df_annual["date"],
                y=df_annual["Government Interest Outlays"],
                mode="lines",
                name="Government Interest Outlays",
                yaxis="y2"
            ))

    fig.update_layout(
        title="Sovereign Debt Sustainability",
        xaxis_title="Date",
        yaxis=dict(
            title="Debt Burden (% GDP)",
            side="left"
        ),
        yaxis2=dict(
            title="Fiscal / Interest Levels",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        height=440,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode="overlay"
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Sovereign Liquidity and Refinancing Pressure — Dual-Axis Chart
# -------------------------------------------------------------------------------------------------
def plot_sovereign_liquidity_refinancing_chart(df_weekly: pd.DataFrame, df_annual: pd.DataFrame) -> go.Figure:
    """
    Renders sovereign refinancing conditions using:
    - Left axis: 10-Year Sovereign Yield
    - Right axis: Government Interest Outlays, Government Receipts
    """
    fig = go.Figure()

    if df_weekly is not None and not df_weekly.empty:
        if "10-Year Sovereign Yield" in df_weekly.columns:
            fig.add_trace(go.Scatter(
                x=df_weekly["date"],
                y=df_weekly["10-Year Sovereign Yield"],
                mode="lines",
                name="10-Year Sovereign Yield",
                yaxis="y1"
            ))

    if df_annual is not None and not df_annual.empty:
        if "Government Interest Outlays" in df_annual.columns:
            fig.add_trace(go.Scatter(
                x=df_annual["date"],
                y=df_annual["Government Interest Outlays"],
                mode="lines",
                name="Government Interest Outlays",
                yaxis="y2"
            ))

        if "Government Receipts" in df_annual.columns:
            fig.add_trace(go.Bar(
                x=df_annual["date"],
                y=df_annual["Government Receipts"],
                name="Government Receipts",
                yaxis="y2",
                opacity=0.45
            ))

    fig.update_layout(
        title="Sovereign Liquidity and Refinancing Pressure",
        xaxis_title="Date",
        yaxis=dict(
            title="Yield (%)",
            side="left"
        ),
        yaxis2=dict(
            title="Fiscal Levels",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        height=440,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        barmode="overlay"
    )

    return fig


# -------------------------------------------------------------------------------------------------
# Balance Sheet Expansion and System Constraint — Dual-Axis Chart
# -------------------------------------------------------------------------------------------------
def plot_balance_sheet_expansion_constraint_chart(
    df_weekly: pd.DataFrame,
    df_quarterly: pd.DataFrame
) -> go.Figure:
    """
    Renders sovereign and central bank balance sheet signals using:
    - Left axis: Sovereign Debt % GDP
    - Right axis: Central Bank Total Assets
    """
    fig = go.Figure()

    # Left axis — sovereign debt burden
    if df_quarterly is not None and not df_quarterly.empty:
        if "Sovereign Debt Percentage of GDP" in df_quarterly.columns:
            fig.add_trace(go.Scatter(
                x=df_quarterly["date"],
                y=df_quarterly["Sovereign Debt Percentage of GDP"],
                mode="lines",
                name="Sovereign Debt % GDP",
                yaxis="y1"
            ))

    # Right axis — central bank balance sheet
    if df_weekly is not None and not df_weekly.empty:
        if "Central Bank Total Assets" in df_weekly.columns:
            fig.add_trace(go.Scatter(
                x=df_weekly["date"],
                y=df_weekly["Central Bank Total Assets"],
                mode="lines",
                name="Central Bank Total Assets",
                yaxis="y2"
            ))

    fig.update_layout(
        title="Balance Sheet Expansion and System Constraint",
        xaxis_title="Date",
        yaxis=dict(
            title="Sovereign Debt (% GDP)",
            side="left"
        ),
        yaxis2=dict(
            title="Central Bank Assets ($ Mn)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        height=440,
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
# Credit Conditions and Financing Pressure — Multi-Series Chart
# -------------------------------------------------------------------------------------------------
def plot_credit_conditions_financing_pressure_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders credit spread conditions across quality tiers.
    """
    required_cols = [
        "date",
        "Corporate Credit Spread",
        "High Yield Credit Spread",
        "CCC and Lower Credit Spread",
    ]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Corporate Credit Spread"],
        mode="lines",
        name="Corporate Credit Spread"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["High Yield Credit Spread"],
        mode="lines",
        name="High Yield Credit Spread"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["CCC and Lower Credit Spread"],
        mode="lines",
        name="CCC and Lower Credit Spread"
    ))

    fig.update_layout(
        title="Credit Conditions and Financing Pressure",
        xaxis_title="Date",
        yaxis_title="Spread (%)",
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
# Bank Balance Sheet Liquidity and Credit Capacity — Multi-Series Chart
# -------------------------------------------------------------------------------------------------
def plot_bank_balance_sheet_liquidity_chart(df: pd.DataFrame) -> go.Figure:
    """
    Renders bank liquidity and asset capacity signals.
    """
    required_cols = [
        "date",
        "Bank Cash Assets",
        "Treasury and Agency Securities Holdings",
        "Bank Total Assets",
    ]

    if not all(col in df.columns for col in required_cols):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Bank Cash Assets"],
        mode="lines",
        name="Bank Cash Assets"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Treasury and Agency Securities Holdings"],
        mode="lines",
        name="Treasury and Agency Securities Holdings"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Bank Total Assets"],
        mode="lines",
        name="Bank Total Assets"
    ))

    fig.update_layout(
        title="Bank Balance Sheet Liquidity and Credit Capacity",
        xaxis_title="Date",
        yaxis_title="Level",
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
