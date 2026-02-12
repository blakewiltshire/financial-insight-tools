# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📘 Trade History & Strategy

This module provides a structured review of historical trades and strategy execution.
It allows users to upload a validated trade log and perform diagnostics on past performance.

Core features include:
- Structural validation of uploaded trade logs (column integrity, formatting)
- Logical consistency checks (date order, direction values, P&L accuracy)
- Automatic classification of trade status (Open vs Closed)
- Realised P&L computation for completed positions
- Optional filters, summaries, and exportable data views

The module supports insight development by revealing trading behaviour, identifying anomalies,
and helping refine future decision strategies — all within the broader
Financial Insight Tools suite.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup — Adjust based on your module's location relative to the project root.
# Path to project root (level_up_3) — for markdown, branding, etc.
# Path to apps directory (level_up_2) — for `use_cases`, `helpers`, etc.
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders, sidebar links etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_trade_history.md")
HELP_APP_MD = os.path.join(ROOT_PATH, "docs", "help_trade_history.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
SAMPLE_FILE = os.path.join(
APPS_PATH, "observation_engine", "sample_inputs",
"sample_trade_closed_log.csv"
)

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# 🧠 Observation Tools (User Observation Logging — Group A)
# -------------------------------------------------------------------------------------------------
from observation_handler_trade_history import (
    observation_input_form,
    display_observation_log
)

from render_macro_interaction_tools_panel_trade_history import render_macro_interaction_tools_panel
from macro_insight_sidebar_panel_trade_portfolio_structuring import render_macro_sidebar_tools

# -------------------------------------------------------------------------------------------------
# 📘 Trade History & Strategy Template + Validator
# -------------------------------------------------------------------------------------------------
from portfolio_trade_modules.trade_log_template import get_trade_log_template
from portfolio_trade_modules.trade_log_validator import validate_trade_log

# -------------------------------------------------------------------------------------------------
# Reminder: __init__.py
# Ensure all relevant folders (e.g., /helpers, /use_cases, /data_sources etc)
# contain an empty __init__.py file.
# This marks them as Python packages and allows import resolution (especially important when
# running via Streamlit or exporting to other Python environments).
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Trade History & Strategy", layout="wide")
st.title("📘 Trade History & Strategy")
st.caption("*Check for errors, compute P&L, and extract behavioural insights from trade logs.*")

# -------------------------------------------------------------------------------------------------
# Info Panel
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_trade_history.md")

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📈 Trade and Portfolio Structuring')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Sidebar Upload + Template
# -------------------------------------------------------------------------------------------------
st.sidebar.markdown("### 📥 Trade Log Setup")

uploaded_file = st.sidebar.file_uploader("Upload your trade log (.csv)", type="csv")

df_template = get_trade_log_template()
st.sidebar.download_button(
    label="📥 Get Trade Log Template",
    data=df_template.to_csv(index=False).encode("utf-8"),
    file_name="trade_log_template.csv",
    mime="text/csv",
    help="Download a structured example of the required trade log format."
)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Sidebar Section Selection (Excludes Portfolio Snapshot — always shown)
# -------------------------------------------------------------------------------------------------
st.sidebar.markdown("### 📂 Select Additional Sections")
selected_sections = st.sidebar.multiselect(
    "Choose one or more views:",
    [
        "📋 Trade Performance Breakdown",
        "📉 Risk & Return Metrics",
        "🧠 Position Sizing & Optimisation",
        "📈 Performance Visualisation",
        "🛠️ Trade Log Validator"
    ],
    default=[]
)
st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Section 1: Portfolio Snapshot (Always Active)
# -------------------------------------------------------------------------------------------------
st.subheader("📊 Portfolio Snapshot")
st.markdown("_Overview of uploaded or selected portfolio and trade history._")

# -------------------------------------------------------------------------------------------------
# Load Data (Fallback to Sample)
# -------------------------------------------------------------------------------------------------
use_sample = False
if uploaded_file:
    try:
        df_trades = pd.read_csv(uploaded_file)
    except Exception:
        st.error("❌ Could not read file. Please ensure it's a valid CSV.")
        df_portfolio = None
else:
    df_trades = pd.read_csv(SAMPLE_FILE)
    use_sample = True

# -------------------------------------------------------------------------------------------------
# Validate
# -------------------------------------------------------------------------------------------------
if df_trades is not None:
    try:
        df_trades["Trade Status"] = df_trades.apply(
            lambda row: (
                "Open"
                if pd.isna(row["Exit Price"]) or pd.isna(row["Trade Date (Exit)"])
                else "Closed"
            ),
            axis=1
        )
    except KeyError as e:
        st.error(f"❌ Required column missing from uploaded trade log: {str(e)}")
        st.stop()


# Validate file and display output
if df_trades is not None:
    errors = validate_trade_log(df_trades)

    if not errors:
        st.sidebar.markdown("### 🧾 Data Summary")
        if use_sample:
            st.sidebar.info("📂 Using default sample trade log.")
        else:
            st.sidebar.success("✅ Trade log loaded successfully.")

        st.sidebar.markdown(f"**Records:** {len(df_trades)}")
        st.sidebar.markdown(f"**Sample:** {'Yes' if use_sample else 'No'}")

        st.sidebar.markdown("""
        <small>
        ⚠️ `P&L (Realised)` should **not** include fees.
        Record execution costs in the `Fees` column.
        </small>
        """, unsafe_allow_html=True)

        with st.expander("📋 Preview Uploaded Trade Log"):
            st.dataframe(df_trades, use_container_width=True)

        # Portfolio metrics
        st.markdown(" ")

        df_closed = df_trades[df_trades["Trade Status"] == "Closed"]
        df_open = df_trades[df_trades["Trade Status"] == "Open"]

        total_trades = len(df_trades)
        closed_trades = len(df_closed)
        open_trades = len(df_open)

        net_pnl = df_closed["P&L (Realised)"].sum()
        win_rate = (
            df_closed[df_closed["P&L (Realised)"] > 0].shape[0] / closed_trades
            if closed_trades > 0 else 0
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Trades", total_trades)
        col2.metric("Closed Trades", closed_trades)
        col3.metric("Open Trades", open_trades)
        col4.metric("Net P&L (Closed)", f"${net_pnl:,.2f}")

        st.caption(f"Win Rate (closed trades only): {win_rate * 100:.1f}%")

        if open_trades > 0:
            st.info(
                f"{open_trades} open trade(s) detected — active positions are not evaluated "
                "in this module.\n\n"
                "For live exposure, unrealised P&L, and portfolio-level diagnostics, "
                "visit the **🧭 Live Portfolio Monitor**."
            )

    else:
        st.error("⚠️ Issues found in trade log:")
        for err in errors:
            st.markdown(f"- {err}")

with st.expander("ℹ️ Interpretation Guidance"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_trade_history.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Filter Options for Section 2 (Closed Trades Only)
# -------------------------------------------------------------------------------------------------
if df_trades is not None and not errors:
    # Extract only closed trades for filtering context
    closed_trades = df_trades[df_trades["Trade Status"] == "Closed"]

    if not closed_trades.empty and "Asset" in closed_trades.columns:
        st.sidebar.markdown("### 🔍 Filter Trades (Closed Only)")
        asset_options = sorted(closed_trades["Asset"].dropna().unique())
        selected_assets = st.sidebar.multiselect(
            "Filter by Asset",
            options=asset_options,
            default=asset_options,
            help="Select which closed trade assets to include in analysis."
        )
        df_filtered = closed_trades[closed_trades["Asset"].isin(selected_assets)].copy()
    else:
        df_filtered = pd.DataFrame(columns=df_trades.columns)
else:
    df_filtered = None

# -------------------------------------------------------------------------------------------------
# Section 2: Trade Performance Breakdown
# -------------------------------------------------------------------------------------------------
if "📋 Trade Performance Breakdown" in selected_sections:
    if df_filtered is not None and not df_filtered.empty:
        st.subheader("📋 Trade Performance Breakdown")
        st.markdown("_Detailed analysis of individual trade outcomes and aggregate metrics._")

        tabs = st.tabs(["📊 Metrics Overview", "📋 Trade History Table"])

        # ------------------------
        # Tab 1: Metrics Overview
        # ------------------------
        with tabs[0]:
            winners = df_filtered[df_filtered["P&L (Realised)"] > 0]
            losers  = df_filtered[df_filtered["P&L (Realised)"] < 0]
            avg_win = winners["P&L (Realised)"].mean() if not winners.empty else 0.0
            avg_loss = losers["P&L (Realised)"].mean() if not losers.empty else 0.0
            win_rate = len(winners) / len(df_filtered) if len(df_filtered) > 0 else 0.0
            expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

            if "Capital Deployed" in df_filtered.columns:
                total_capital = df_filtered["Capital Deployed"].sum()
                net_pnl = df_filtered["P&L (Realised)"].sum()
                roi = net_pnl / total_capital if total_capital > 0 else 0.0
            else:
                roi = None

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Avg Win", f"${avg_win:,.2f}")
            col2.metric("Avg Loss", f"${avg_loss:,.2f}")
            col3.metric("Expectancy", f"${expectancy:,.2f}")
            col4.metric("ROI", f"{roi * 100:.2f}%" if roi is not None else "N/A")

            st.caption(
                f"Expectancy = Win Rate × Avg Win + Loss Rate × Avg Loss.  "
                f"ROI uses total capital deployed if available.  "
                f"Metrics calculated on {len(df_filtered)} closed trades."
            )

        # ------------------------
        # Tab 2: Trade History Table
        # ------------------------
        with tabs[1]:
            st.markdown("_Sortable, filterable trade log; includes Return % \
            and holding duration._")

            ordered_cols = [
                "Asset", "Trade Date (Entry)", "Direction", "Trade Date (Exit)",
                "Entry Price", "Exit Price", "Position Size", "P&L (Realised)",
                "Capital Deployed", "Fees", "Return %", "Duration (Days)"
            ]
            df_display = df_filtered.copy()
            available_cols = [col for col in ordered_cols if col in df_display.columns]
            df_display = df_display[available_cols]

            # Derived fields
            if "Capital Deployed" in df_display.columns:
                df_display["Return %"] = (
                    df_display["P&L (Realised)"] / df_display["Capital Deployed"] * 100
                ).round(2)
            df_display["Duration (Days)"] = (
                pd.to_datetime(df_display["Trade Date (Exit)"]) -
                pd.to_datetime(df_display["Trade Date (Entry)"])
            ).dt.days

            # Conditional colour logic
            cellstyle_profit_loss = JsCode("""
                function(params) {
                    if (params.value > 0) {
                        return {
                            'color': 'white',
                            'backgroundColor': '#4CAF50',
                            'fontWeight': '400'
                        }
                    } else if (params.value < 0) {
                        return {
                            'color': 'white',
                            'backgroundColor': '#EF5350',
                            'fontWeight': '400'
                        }
                    } else {
                        return {
                            'color': 'white',
                            'backgroundColor': '#90A4AE',
                            'fontWeight': '400'
                        }
                    }
                }
            """)

            gb = GridOptionsBuilder.from_dataframe(df_display)
            gb.configure_grid_options(domLayout='normal', rowHeight=28)
            gb.configure_pagination(paginationPageSize=20)
            gb.configure_default_column(editable=False, filter=True, sortable=True)

            gb.configure_column("Asset", pinned="left")
            gb.configure_column("Trade Date (Entry)", pinned="left")
            # gb.configure_column("Direction", pinned="left")

            if "P&L (Realised)" in df_display.columns:
                gb.configure_column("P&L (Realised)", type=["numericColumn"], precision=2,
                cellStyle=cellstyle_profit_loss)
            if "Return %%" in df_display.columns:
                gb.configure_column("Return %", type=["numericColumn"], precision=2,
                cellStyle=cellstyle_profit_loss)

            gb.configure_column("Duration (Days)", type=["numericColumn"], precision=0)

            AgGrid(
                df_display,
                gridOptions=gb.build(),
                enable_enterprise_modules=False,
                fit_columns_on_grid_load=True,
                theme="balham",
                height=440,
                allow_unsafe_jscode=True
            )
    elif df_trades is not None and errors:
        st.info("📋 Trade Performance Breakdown not shown — trade log failed validation.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Section 3: Risk & Return Metrics
# -------------------------------------------------------------------------------------------------
if "📉 Risk & Return Metrics" in selected_sections and df_filtered is not None and not errors:
    st.subheader("📉 Risk & Return Metrics")
    st.markdown("_Evaluate performance through volatility and downside-adjusted indicators._")

    # Filter closed trades with valid exit dates
    df_sorted = df_filtered.dropna(subset=["Trade Date (Exit)"]).copy()
    df_sorted = df_sorted.sort_values("Trade Date (Exit)")

    # Cumulative P&L and equity
    df_sorted["Equity"] = df_sorted["P&L (Realised)"].cumsum()
    df_sorted["Equity Shifted"] = df_sorted["Equity"].shift(1)
    df_sorted["Daily Return"] = df_sorted["Equity"].pct_change()
    daily_returns = df_sorted["Daily Return"].dropna()

    # --- Metrics ---
    volatility = daily_returns.std() * np.sqrt(252) if not daily_returns.empty else np.nan
    sharpe_ratio = np.nan
    sortino_ratio = np.nan
    annualised_return = np.nan

    downside_returns = daily_returns[daily_returns < 0]
    if not downside_returns.empty and downside_returns.std() > 0:
        downside_std = downside_returns.std()
        sortino_calc = (daily_returns.mean() * 252) / (downside_std * np.sqrt(252))
        sortino_ratio = min(sortino_calc, 10)  # Cap to avoid misleading extreme values

    try:
        start_date = pd.to_datetime(df_sorted["Trade Date (Exit)"].min())
        end_date = pd.to_datetime(df_sorted["Trade Date (Exit)"].max())
        num_days = (end_date - start_date).days

        net_pnl = df_sorted["P&L (Realised)"].sum()
        total_capital = df_sorted["Capital Deployed"].sum()

        if total_capital > 0 and num_days > 0:
            cumulative_return = net_pnl / total_capital
            annualised_return = (1 + cumulative_return) ** (252 / num_days) - 1
            sharpe_ratio = (
                annualised_return / volatility
                if volatility and volatility > 0
                else np.nan
            )
    except Exception:
        pass

    # --- Max Drawdown ---
    max_drawdown = (
        (df_sorted["Equity"].cummax() - df_sorted["Equity"]).max()
        if not df_sorted["Equity"].empty else np.nan
    )

    # --- Display ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
    "Annualised Return", f"{annualised_return*100:.2f}%" if not np.isnan(
    annualised_return) else "N/A"
    )
    col2.metric("Volatility", f"{volatility*100:.2f}%" if not np.isnan(volatility) else "N/A")
    col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}" if not np.isnan(sharpe_ratio) else "N/A")
    col4.metric("Sortino Ratio", f"{sortino_ratio:.2f}" if not np.isnan(sortino_ratio) else "N/A")

    if np.isnan(sortino_ratio):
        st.caption("⚠️ Sortino Ratio is unavailable — no downside volatility in filtered \
        trade set.")

    st.caption("Metrics calculated from cumulative trade performance and filtered holding period. "
               "Annualised return uses capital-weighted growth over elapsed calendar days.")

    st.markdown("### 📉 Maximum Drawdown")
    if not np.isnan(max_drawdown):
        st.metric("Max Drawdown", f"${max_drawdown:,.2f}")
    else:
        st.info("Drawdown unavailable — insufficient equity curve data.")

# -------------------------------------------------------------------------------------------------
# Interpretation and Framing
# -------------------------------------------------------------------------------------------------
if "📉 Risk & Return Metrics" in selected_sections and df_filtered is not None and not errors:
    with st.expander("📌 Metric Interpretation and Context"):
        st.markdown("These indicators summarise the risk-return characteristics of the uploaded "
                    "or filtered trade set.")

        annualised_display = (
            f"{(annualised_return * 100):.2f}%" if annualised_return is not None else "0.00%"
        )
        volatility_display = (
            f"{(volatility * 100):.2f}%" if volatility is not None else "0.00%"
        )
        sharpe_display = (
            f"{sharpe_ratio:.2f}" if sharpe_ratio is not None else "0.00"
        )
        sortino_display = (
            f"{sortino_ratio:.2f}" if sortino_ratio is not None else "0.00"
        )
        drawdown_display = (
            f"${max_drawdown:,.2f}" if max_drawdown is not None else "$0.00"
        )

        st.markdown(f"""
| **Metric** | **Value** | **Interpretation** |
|------------|-----------|--------------------|
| **Annualised Return** | {annualised_display} | Theoretical return extrapolated over 252 \
trading days based on capital deployed. Used for comparability, not forecasting. |
| **Volatility** | {volatility_display} | Standard deviation of equity returns. \
High values often reflect short timeframes, few trades, or inconsistent sizing. |
| **Sharpe Ratio** | {sharpe_display} | Return per unit of total risk. Values above 1 \
suggest efficiency. Below 1 may indicate volatility exceeds benefit. |
| **Sortino Ratio** | {sortino_display} | Return per unit of downside risk. Ignores \
upside variation — more stable in directional strategies. |
| **Max Drawdown** | {drawdown_display} | Largest cumulative loss from peak to trough. \
Helps gauge risk capacity and psychological tolerance. |
""")

        st.markdown("""
**⚠️ Important Notes:**
- Realistic **annualised returns** for most active traders range from 5%–15%. \
Values >100% often result from short timeframes or outlier trades.
- **Volatility** is amplified by:
  - Infrequent trades
  - Highly uneven position sizes
  - Close clustering of wins/losses
- These metrics provide perspective — not certainty. Use them as *diagnostic signals*, \
not forecasts.
""")

    st.divider()


# -------------------------------------------------------------------------------------------------
# Section 4: Position Sizing & Optimisation
# -------------------------------------------------------------------------------------------------
if (
    "🧠 Position Sizing & Optimisation" in selected_sections
    and df_filtered is not None
    and not errors
):
    st.subheader("🧠 Position Sizing & Optimisation")
    st.markdown("_Assess sizing strategies using Kelly and simulate alternate trade weightings._")

    # Filter closed trades
    closed = df_filtered.dropna(subset=["Exit Price", "P&L (Realised)"]).copy()
    closed = closed[closed["P&L (Realised)"] != 0]  # Avoid zero-return trades

    if len(closed) < 5:
        st.warning("⚠️ Not enough closed trades for reliable position sizing simulation. \
        Minimum 5 recommended.")
    else:
        # Calculate Kelly Fraction
        winners = closed[closed["P&L (Realised)"] > 0]
        losers = closed[closed["P&L (Realised)"] < 0]
        win_rate = len(winners) / len(closed)
        avg_win = winners["P&L (Realised)"].mean()
        avg_loss = abs(losers["P&L (Realised)"].mean())

        kelly_fraction = (win_rate - (1 - win_rate) * (
        avg_loss / avg_win)) if avg_win and avg_loss else 0
        kelly_fraction = max(0, round(kelly_fraction, 2))  # Bound to 0+ only

        # Strategy Simulations
        capital = 10000  # Starting capital
        strategy_returns = {
            "Fixed Fractional (2%)": [],
            "Kelly": [],
            "Half Kelly": [],
            "Equal Weight": []
        }

        for i, row in closed.iterrows():
            trade_return = row["P&L (Realised)"]
            capital_deployed = row.get("Capital Deployed", None)

            strategy_returns["Fixed Fractional (2%)"].append(capital * 0.02 * (
            trade_return / capital_deployed) if capital_deployed else 0
            )
            strategy_returns["Kelly"].append(capital * kelly_fraction * (
            trade_return / capital_deployed) if capital_deployed else 0
            )
            strategy_returns["Half Kelly"].append(capital * (kelly_fraction / 2) * (
            trade_return / capital_deployed) if capital_deployed else 0
            )
            strategy_returns["Equal Weight"].append((capital / len(closed)) * (
            trade_return / capital_deployed) if capital_deployed else 0
            )

        # Compute final returns
        strategy_summary = []
        for strategy, returns in strategy_returns.items():
            total_return = sum(returns)
            kelly_used = (
                f"{kelly_fraction * 100:.0f}%" if "Kelly" in strategy
                else "2%" if "Fixed" in strategy
                else f"{(kelly_fraction / 2) * 100:.0f}%"
            )
            strategy_summary.append({
                "Strategy": strategy,
                "Total Return ($)": round(total_return, 2),
                "Kelly Fraction Used": kelly_used
            })

        # Display Table
        st.markdown("### 📊 Sizing Strategy Comparison")
        st.dataframe(pd.DataFrame(strategy_summary), use_container_width=False)


        # Explanation
        st.markdown("""
        **📄 Notes:**
        - **Kelly** sizing uses the full mathematical edge based on historical win \
        rate and payoff ratio.
        - **Fixed Fractional** applies a consistent 2% risk per trade.
        - **Equal Weight** distributes capital evenly across all trades.
        - These results are retrospective simulations — use them for comparative insight, \
        not forecasting.
        """)

st.divider()

# -------------------------------------------------------------------------------------------------
# Section 5: Performance Visualisation
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Section 5: Performance Visualisation
# -------------------------------------------------------------------------------------------------
if "📈 Performance Visualisation" in selected_sections and df_filtered is not None and not errors:
    st.subheader("📈 Performance Visualisation")
    st.caption(
        "Visualise trade outcomes, equity curve development, drawdown cycles, and  "
        "risk-return dynamics. "
        "This section turns numerical performance into structural signals for review  "
        "and strategy refinement."
    )

    with st.expander("📌 Interpretation Guidance"):
        st.markdown("""
This panel visualises the performance of **closed trades only**, using standard analytical views:

---

**Equity Curve & Drawdown**
Cumulative P&L evolution over time, with drawdowns from historical peaks.

**P&L Distribution**
Histogram showing profit/loss distribution across individual trades.

**Realised P&L Timeline**
Bar chart of trade-by-trade outcomes in sequence.

**Duration vs P&L Scatter**
How long trades were held vs their performance — can signal time-risk tradeoffs.

**Sharpe vs Sortino Quadrant**
Compares two risk-adjusted return metrics. Quadrants reflect strategic balance.

---

⚠️ **Note:**
- All visuals are based on uploaded data integrity.
- Open positions are excluded.
- Interpretation is contextual, not predictive.
        """)

    df_viz = df_filtered.dropna(subset=["P&L (Realised)", "Trade Date (Exit)"]).copy()
    df_viz = df_viz.sort_values("Trade Date (Exit)")
    df_viz["Equity"] = df_viz["P&L (Realised)"].cumsum()
    df_viz["Equity Peak"] = df_viz["Equity"].cummax()
    df_viz["Drawdown"] = df_viz["Equity"] - df_viz["Equity Peak"]

    # --- Chart 1: Equity Curve with Drawdown Overlay ---
    fig_equity = px.line(df_viz, x="Trade Date (Exit)", y="Equity", title="Equity Curve")
    fig_drawdown = px.area(df_viz, x="Trade Date (Exit)", y="Drawdown", title="Drawdown Area")

    fig_equity.update_layout(template="plotly_white", yaxis_title="Cumulative P&L")
    fig_drawdown.update_layout(template="plotly_white", yaxis_title="Drawdown", showlegend=False)

    st.plotly_chart(fig_equity, use_container_width=True)
    st.plotly_chart(fig_drawdown, use_container_width=True)

    # --- Chart 2: P&L Distribution Histogram ---
    fig_pnl_hist = px.histogram(
        df_viz,
        x="P&L (Realised)",
        nbins=20,
        title="Distribution of Realised Trade P&L",
        labels={"P&L (Realised)": "Profit or Loss ($)"},
        opacity=0.85,
        marginal="rug",
        template="plotly_white"
    )
    fig_pnl_hist.update_layout(xaxis_title="Realised P&L",
    yaxis_title="Number of Trades", bargap=0.05)
    st.plotly_chart(fig_pnl_hist, use_container_width=True)

    # --- Chart 3: Rolling P&L Timeline ---
    fig_rolling = px.bar(
        df_viz,
        x="Trade Date (Exit)",
        y="P&L (Realised)",
        title="Realised P&L Over Time",
        labels={"P&L (Realised)": "P&L"},
        template="plotly_white"
    )
    fig_rolling.update_layout(xaxis_title="Exit Date", yaxis_title="P&L ($)")
    st.plotly_chart(fig_rolling, use_container_width=True)

    # --- Chart 4: Duration vs Return Scatter ---
    if "Trade Date (Entry)" in df_viz.columns:
        df_viz["Duration (Days)"] = (
            pd.to_datetime(df_viz["Trade Date (Exit)"]) -
            pd.to_datetime(df_viz["Trade Date (Entry)"])
        ).dt.days
        fig_scatter = px.scatter(
            df_viz,
            x="Duration (Days)",
            y="P&L (Realised)",
            title="Trade Duration vs. Realised P&L",
            template="plotly_white",
            hover_data=["Asset", "Strategy Tag", "Country"]
        )
        fig_scatter.update_layout(xaxis_title="Duration (Days)", yaxis_title="P&L ($)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Chart 5: Sharpe vs Sortino Quadrant ---
    # Placeholder: We assume you have metrics from Section 3
    try:
        fig_quadrant = px.scatter(
            x=[sharpe_ratio], y=[sortino_ratio],
            labels={"x": "Sharpe Ratio", "y": "Sortino Ratio"},
            title="Sharpe vs Sortino Quadrant",
            template="plotly_white"
        )

        fig_quadrant.update_traces(marker={"color": "dodgerblue", "size": 14})
        fig_quadrant.add_shape(type="line", x0=1, x1=1, y0=-2, y1=6,
                               line={"color": 'gray', "dash": 'dash'})
        fig_quadrant.add_shape(type="line", x0=-2, x1=6, y0=1, y1=1,
                               line={"color": 'gray', "dash": 'dash'})
        fig_quadrant.update_layout(xaxis_range=[-2, 6], yaxis_range=[-2, 6])
        st.plotly_chart(fig_quadrant, use_container_width=True)
    except Exception:
        st.info("⚠️ Unable to generate Sharpe vs Sortino plot — required metrics not found.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Section 6: Trade Log Validator
# -------------------------------------------------------------------------------------------------
if "🛠️ Trade Log Validator" in selected_sections and df_trades is not None:
    st.subheader("🛠️ Trade Log Validator")
    st.markdown("_Identify structural issues, potential anomalies, and inconsistencies \
    in the uploaded trade log._")

    validator_tabs = st.tabs(["🔍 Summary Diagnostics", "📄 Detailed Checks",
    "📊 Observations & Patterns"])

    # ------------------------
    # Tab 1: Summary Diagnostics
    # ------------------------
    with validator_tabs[0]:
        issues = validate_trade_log(df_trades)
        if issues:
            st.warning("⚠️ Validation Issues Found:")
            for i in issues:
                st.markdown(f"- {i}")
        else:
            st.success("✅ No critical issues found in trade log structure.")

        st.caption("These checks are applied at upload, but summarised here for transparency.")

    # ------------------------
    # Tab 2: Detailed Checks
    # ------------------------
    with validator_tabs[1]:
        st.markdown("### 🔧 Field Integrity Checks")

        missing_exits = df_trades[df_trades["Exit Price"].isna()]
        zero_length = df_trades[
            pd.to_datetime(df_trades["Trade Date (Exit)"], errors='coerce') ==
            pd.to_datetime(df_trades["Trade Date (Entry)"], errors='coerce')
        ]

        col1, col2 = st.columns(2)
        col1.metric("Open Trades", len(missing_exits))
        col2.metric("Zero-Day Trades", len(zero_length))

        if len(zero_length) > 0:
            st.warning(f"{len(zero_length)} trades have entry and exit on the same day.")

        st.markdown("### 🔁 P&L Cross-Check")
        df_closed = df_trades.dropna(subset=["Exit Price"])
        df_closed["Calc P&L"] = df_closed.apply(
            lambda row: (row["Exit Price"] - row["Entry Price"]) * row["Position Size"]
            if str(row["Direction"]).lower() == "long"
            else (row["Entry Price"] - row["Exit Price"]) * row["Position Size"],
            axis=1
        )
        df_closed["Diff"] = (df_closed["Calc P&L"] - df_closed["P&L (Realised)"]).round(2)
        mismatches = df_closed[df_closed["Diff"].abs() > 0.01]

        if not mismatches.empty:
            st.error(f"{len(mismatches)} trades have non-trivial differences between reported \
            and calculated P&L.")
            st.dataframe(mismatches[["Asset", "Entry Price", "Exit Price", "Position Size",
            "Direction", "P&L (Realised)", "Calc P&L", "Diff"]])
        else:
            st.success("✅ All closed trades passed P&L recomputation check.")

    # ------------------------
    # Tab 3: Observations & Patterns
    # ------------------------
    with validator_tabs[2]:
        st.markdown("### 📌 Observational Insights")

        gap_summary = df_trades.sort_values("Trade Date (Entry)").copy()
        gap_summary["Trade Date (Entry)"] = pd.to_datetime(gap_summary["Trade Date (Entry)"],
        errors='coerce')
        gap_summary["Gap"] = gap_summary["Trade Date (Entry)"].diff().dt.days

        st.line_chart(gap_summary["Gap"], use_container_width=True)
        st.caption("Review periods between trades to spot bursts or inactivity.")

        st.markdown("#### Sector/Strategy Consistency")
        summary = df_trades.groupby(["Sector", "Strategy Tag"]).size().reset_index(name="Count")
        st.dataframe(pd.DataFrame(summary), use_container_width=False)

st.divider()

# -------------------------------------------------------------------------------------------------
# 🧠 Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
theme_code = "trade_history"
theme_title = "Trade History & Strategy"
selected_use_case = "Trade History Reflection Snapshot"

# -------------------------------------------------------------------------------------------------
# 🧠 Activate Observation + Journal Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case
)

# 🎯 No assets are relevant for historical trade log reflections
asset_list_for_observation = []

if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")
    st.caption("*Use this space to log portfolio-wide sentiment, risk concerns, or conviction "
    "commentary relevant to your current exposure.*")

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    with open(os.path.join(ROOT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with open(os.path.join(ROOT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()

st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
    No trading, investment, or policy advice provided."
)
