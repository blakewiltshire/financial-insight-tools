# -------------------------------------------------------------------------------------------------
# 📈 Visual Config (Local Extension) — Theme 200 Labour Market Dynamics (Platinum+)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, unused-argument, unused-import

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📈 Local Visual Configuration — Economic Exploration Suite
-----------------------------------------------------------------

Defines the country- or theme-specific visual rendering extensions for
Economic Exploration modules (Themes 100–2100+). This module extends the
universal charting engine, enabling more granular visualisation layers.

✅ Role in the System:
- Adds localised chart overlays, sector breakdowns, and country-specific displays.
- Controls tab and subtab layouts per Use Case.
- Dynamically routes visual rendering based on the selected Use Case.

🧠 System Design Notes:
- Visual rendering is fully independent of indicator signal evaluation.
- **Use Case selection controls visual rendering**, with charts configured here.
- Chart data slices are passed via `df_map`, based on timeframe windows handled locally.
- Visual keys, tab names, subtab structures, and display logic are fully controlled here.
- This local module **does not reference indicator_map_XXX.py or insights** directly.

⚙️ Architecture Summary:
- Each Use Case receives its own visualisation block inside `render_all_charts_local()`.
- Subtabs are always required (even for single-chart cases) to ensure consistent UI structure.
- Chart keys are managed via `display_chart_with_fallback()` to prevent Streamlit key conflicts.
- Local visuals may call universal chart functions (e.g., from `universal_visual_config_XXX.py`) for consistency.

Usage:
- Invoked automatically from the main theme module (`100_📈_economic_growth_stability.py`, `200_💼_labour_market_dynamics.py`, etc.)
- Required only when country- or theme-specific visuals are implemented.
- If no local visual config exists, universal visuals render by default.

🧠 AI Implementation Notes:
- Visual tab structure is critical for AI narrative consistency and export accuracy.
- Subtab names, chart labels, and layout stability directly influence AI macro narrative parsing.

"""

# -------------------------------------------------------------------------------------------------
# 🧱 Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_pills import pills

# -------------------------------------------------------------------------------------------------
# 🛠 Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_visual_config"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Chart Imports (Theme 200)
# ----------------------------------- --------------------------------------------------------------
from universal_visual_config_200 import (
    display_chart_with_fallback,
    plot_labour_line_chart,
    plot_labour_with_extremes,
    plot_labour_volatility,
    plot_labour_momentum
)

# -------------------------------------------------------------------------------------------------
# 📊 Sector Columns and Icons Mapping
# -------------------------------------------------------------------------------------------------
SECTOR_COLUMNS = [
    "Mining and Logging",
    "Construction", "Manufacturing",
    "Trade Transportation and Utilities", "Information", "Financial Activities",
    "Professional and Business Services", "Education and Health Services",
    "Leisure and Hospitality", "Other Services", "Government"
]

SECTOR_ICONS = {
    "Mining and Logging": "⛏️",
    "Construction": "🚧", "Manufacturing": "⚙️",
    "Trade Transportation and Utilities": "🚚", "Information": "💻", "Financial Activities": "💰",
    "Professional and Business Services": "📈", "Education and Health Services": "🏥",
    "Leisure and Hospitality": "🎯", "Other Services": "🔧", "Government": "🏛️"
}

# -------------------------------------------------------------------------------------------------
# 📌 Visual Section Titles Mapping
# -------------------------------------------------------------------------------------------------
def get_visual_section_titles():
    return {
        "Employment Trends": "📈 Employment Growth and Hiring Activity",
        "Unemployment Context": "📉 Unemployment Rates and Volatility",
        "Labour Force Engagement": "🧠 Participation and Labour Supply Trends",
        "Business Sector Employment Breakdown": "🏭 Sector-Level Employment Dynamics",
        "Employment Type and Wage Dynamics": "🧮 Employment Type, Wage and Jobless Claims"
    }

# -------------------------------------------------------------------------------------------------
# Chart Helpers for Local Extensions
# -------------------------------------------------------------------------------------------------

def plot_sector_employment(df, sector):
    df = df.copy()
    if "date" not in df.columns or sector not in df.columns:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df[sector], mode="lines+markers"))
    fig.update_layout(title=f"{SECTOR_ICONS.get(sector, '🏭')} {sector}",
                      xaxis_title="Date", yaxis_title="Employment (000s)",
                      template="plotly_white", height=460)
    return fig

def plot_simple_line(df, column, title, yaxis):
    if "date" not in df.columns or column not in df.columns:
        return go.Figure()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df[column], mode="lines+markers"))
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis,
        template="plotly_white",
        height=460
    )
    return fig

def plot_ft_pt_ratio(df):
    if "date" not in df.columns or "Full-Time Employment" not in df.columns or "Part-Time Employment" not in df.columns:
        return go.Figure()
    df = df.copy()
    df["FT/PT Ratio"] = df["Full-Time Employment"] / df["Part-Time Employment"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["FT/PT Ratio"], mode="lines+markers"))
    fig.update_layout(
        title="Full-Time / Part-Time Ratio",
        xaxis_title="Date",
        yaxis_title="Ratio",
        template="plotly_white",
        height=460
    )
    return fig

def plot_wage_yoy(df):
    if "date" not in df.columns or "Average Hourly Earnings (Total Private)" not in df.columns:
        return go.Figure()
    df = df.copy()
    df["AHE YoY %"] = df["Average Hourly Earnings (Total Private)"].pct_change(12) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["AHE YoY %"], mode="lines+markers"))
    fig.update_layout(
        title="📈 YoY Wage Growth (%)",
        xaxis_title="Date",
        yaxis_title="% Change",
        template="plotly_white",
        height=460
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Chart Helper — Jobless Claims (Initial + Continued Combined)
# -------------------------------------------------------------------------------------------------
def plot_jobless_claims(df):
    df = df.copy()
    if "date" not in df.columns or \
       "Initial Jobless Claims" not in df.columns or \
       "Continued Jobless Claims" not in df.columns:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Initial Jobless Claims"],
        mode="lines+markers",
        name="Initial Claims",
        line={"color": "#1f77b4"}
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Continued Jobless Claims"],
        mode="lines+markers",
        name="Continued Claims",
        line={"color": "#ff7f0e"}
    ))

    fig.update_layout(
        title="Jobless Claims Overview",
        xaxis_title="Date",
        yaxis_title="Number of Claims",
        template="plotly_white",
        height=460
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Universal Labour Tabs
# -------------------------------------------------------------------------------------------------
def render_universal_labour_tabs(selected_use_case: str, df: pd.DataFrame, tab_key: str) -> bool:
    """
    Universal UI (consistent across all countries) for:
    - Employment Trends
    - Unemployment Context
    - Labour Force Engagement

    Returns True if it handled the use case, else False.
    """
    # --- Employment Trends ---
    if selected_use_case == "Employment Trends":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Hiring Momentum",
            "📉 Volatility Context",
            "🔁 Inflection Points"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Number of People in Employment",
                    "Employment Trends",
                    "Employment Level"
                ),
                label=f"{tab_key}_HiringMomentum"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Number of People in Employment",
                    "Hiring Volatility",
                    "Employment Level"
                ),
                label=f"{tab_key}_HiringVolatility"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_momentum(
                    df,
                    "Number of People in Employment",
                    "Turning Points in Employment",
                    "Employment Level"
                ),
                label=f"{tab_key}_EmploymentInflection"
            )
        return True

    # --- Unemployment Context ---
    if selected_use_case == "Unemployment Context":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Unemployment Direction",
            "📈 Extremes & Reversion",
            "🌪️ Volatility"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Unemployment Rate",
                    "Unemployment Direction",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentDirection"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_with_extremes(
                    df,
                    "Unemployment Rate",
                    "Reversion from Extremes",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentReversion"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Unemployment Rate",
                    "Volatility in Unemployment",
                    "Unemployment Rate (%)"
                ),
                label=f"{tab_key}_UnemploymentVolatility"
            )
        return True

    # --- Labour Force Engagement ---
    if selected_use_case == "Labour Force Engagement":
        subtab1, subtab2, subtab3 = st.tabs([
            "📈 Participation Direction",
            "🔄 Structural Variability",
            "📉 Historical Extremes"
        ])

        with subtab1:
            display_chart_with_fallback(
                plot_labour_line_chart(
                    df,
                    "Labour Participation Rate",
                    "Participation Trend",
                    "Participation Rate (%)"
                ),
                label=f"{tab_key}_ParticipationTrend"
            )

        with subtab2:
            display_chart_with_fallback(
                plot_labour_volatility(
                    df,
                    "Labour Participation Rate",
                    "Variability in Participation",
                    "Volatility (percentage points)",
                    window=6
                ),
                label=f"{tab_key}_ParticipationVariability"
            )

        with subtab3:
            display_chart_with_fallback(
                plot_labour_with_extremes(
                    df,
                    "Labour Participation Rate",
                    "Reversion from Historical Extremes",
                    "Participation Rate (%)"
                ),
                label=f"{tab_key}_ParticipationExtremes"
            )
        return True

    return False


# -------------------------------------------------------------------------------------------------
# 🚦 Chart Dispatcher — Universal Charts First, Local Extensions After
# -------------------------------------------------------------------------------------------------
def render_all_charts_local(selected_use_case, tab_mapping, df_map):

    period_options = [3, 6, 12, 24, 60, None]
    composite_tabs = list(tab_mapping.keys())[:6]

    for tab, data_slice in tab_mapping.items():
        with tab:
            df = data_slice.reset_index()

            # --- Universal (consistent across countries) ---
            handled = render_universal_labour_tabs(selected_use_case, df, tab)
            if handled:
                continue

            # --- Local Extensions (Business Sector Employment Breakdown) ---
            elif selected_use_case == "Business Sector Employment Breakdown":

                current_periods = None
                for tab_label, periods in zip(composite_tabs, period_options):
                    if tab == tab_label:
                        current_periods = periods
                        break

                df_secondary_full = df_map["df_secondary"].reset_index()
                df_secondary = (
                    df_secondary_full.tail(current_periods)
                    if current_periods is not None else df_secondary_full
                )

                sectors = [sector for sector in SECTOR_COLUMNS if sector in df_secondary.columns]
                if not sectors:
                    st.info("⚠️ No sector-level data available for this dataset slice.")
                    return

                selected_sector = pills(
                    "📌 Select Sector",
                    options=sectors,
                    icons=[SECTOR_ICONS.get(sector, "🏭") for sector in sectors],
                    key=f"{tab}_sector_pills"
                )

                if selected_sector:
                    sector = selected_sector
                    df_sector = df_secondary[sector]

                    latest_val = df_sector.iloc[-1]
                    period_avg = df_sector.mean()
                    net_change = df_sector.iloc[-1] - df_sector.iloc[0]
                    min_val = df_sector.min()
                    max_val = df_sector.max()
                    range_val = max_val - min_val

                    yoy_change = None
                    if len(df_secondary) >= 12:
                        shifted_val = df_secondary_full[sector].shift(12).iloc[-1]
                        if pd.notna(shifted_val):
                            yoy_change = (latest_val / shifted_val - 1) * 100

                    display_chart_with_fallback(
                        plot_sector_employment(df_secondary, sector),
                        label=f"{tab}_{sector}"
                    )

                    row1 = st.columns(3)
                    row1[0].metric("Latest Level", f"{latest_val:,.0f}")
                    row1[1].metric("Period Avg", f"{period_avg:,.0f}")
                    row1[2].metric("Net Change", f"{net_change:+,.0f}")

                    row2 = st.columns(3)
                    row2[0].metric("Max", f"{max_val:,.0f}")
                    row2[1].metric("Min", f"{min_val:,.0f}")
                    row2[2].metric("Range", f"{range_val:,.0f}")

                    if yoy_change is not None:
                        st.metric("YoY % Change", f"{yoy_change:,.2f}%")

                summary_data = []
                for sector in sectors:
                    df_sector = df_secondary[sector]
                    latest_val = df_sector.iloc[-1]
                    period_avg = df_sector.mean()
                    net_change = df_sector.iloc[-1] - df_sector.iloc[0]
                    min_val = df_sector.min()
                    max_val = df_sector.max()
                    range_val = max_val - min_val
                    yoy_change = None
                    if len(df_secondary) >= 12:
                        shifted_val = df_secondary_full[sector].shift(12).iloc[-1]
                        if pd.notna(shifted_val):
                            yoy_change = (latest_val / shifted_val - 1) * 100

                    summary_data.append({
                        "Sector": sector,
                        "Latest": latest_val,
                        "Avg": period_avg,
                        "Net Change": net_change,
                        "Min": min_val,
                        "Max": max_val,
                        "Range": range_val,
                        "YoY % Change": yoy_change
                    })

                summary_df = pd.DataFrame(summary_data).sort_values(by="Sector")
                summary_df["YoY % Change"] = summary_df["YoY % Change"].fillna("N/A")

                with st.expander("📋 Full Sector Summary Table", expanded=False):
                    st.dataframe(
                        summary_df.style.format({
                            "Latest": "{:,.0f}",
                            "Avg": "{:,.0f}",
                            "Net Change": "{:+,.0f}",
                            "Min": "{:,.0f}",
                            "Max": "{:,.0f}",
                            "Range": "{:,.0f}",
                            "YoY % Change": lambda x: f"{x:,.2f}%" if isinstance(x, (int, float)) else x
                        }),
                        width='stretch'
                    )

            # --- Full-Time vs Part-Time Employment ---
            elif selected_use_case == "Full-Time vs Part-Time Employment":

                current_periods = None
                for tab_label, periods in zip(composite_tabs, period_options):
                    if tab == tab_label:
                        current_periods = periods
                        break

                df_secondary_full = df_map["df_secondary"].reset_index()
                df_secondary = df_secondary_full.tail(current_periods) if current_periods else df_secondary_full

                subtab1, subtab2, subtab3 = st.tabs([
                    "🧑‍💼 Full-Time Employment",
                    "🧑‍🎓 Part-Time Employment",
                    "⚖️ Full-Time / Part-Time Ratio"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_simple_line(df_secondary, "Full-Time Employment", "Full-Time Employment", "Employment (000s)"),
                        label=f"{tab}_FullTime"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_simple_line(df_secondary, "Part-Time Employment", "Part-Time Employment", "Employment (000s)"),
                        label=f"{tab}_PartTime"
                    )

                with subtab3:
                    display_chart_with_fallback(
                        plot_ft_pt_ratio(df_secondary),
                        label=f"{tab}_FTPT"
                    )

            # --- Average Hourly Earnings ---
            elif selected_use_case == "Average Hourly Earnings":

                current_periods = None
                for tab_label, periods in zip(composite_tabs, period_options):
                    if tab == tab_label:
                        current_periods = periods
                        break

                df_secondary_full = df_map["df_secondary"].reset_index()
                df_secondary = df_secondary_full.tail(current_periods) if current_periods else df_secondary_full

                subtab1, subtab2 = st.tabs([
                    "💰 Average Hourly Earnings",
                    "📈 YoY Wage Growth"
                ])

                with subtab1:
                    display_chart_with_fallback(
                        plot_simple_line(df_secondary, "Average Hourly Earnings (Total Private)", "Average Hourly Earnings", "Wage"),
                        label=f"{tab}_Wage"
                    )

                with subtab2:
                    display_chart_with_fallback(
                        plot_wage_yoy(df_secondary),
                        label=f"{tab}_WageYoY"
                    )

            # --- Jobless Claims ---
            elif selected_use_case == "Jobless Claims":
                current_periods = next((p for t, p in zip(composite_tabs, period_options) if t == tab), None)
                df_extended_full = df_map["df_extended"].reset_index()
                df_extended = df_extended_full.tail(current_periods) if current_periods else df_extended_full

                display_chart_with_fallback(
                    plot_jobless_claims(df_extended), label=f"{tab}_JoblessClaims")
