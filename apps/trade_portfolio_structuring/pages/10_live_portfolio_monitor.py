# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🧭 Live Portfolio Monitor

This module is part of the Trade & Portfolio Structuring suite in the
Financial Insight Tools system.

It provides real-time diagnostics on active portfolio positions, enabling users to:
- Upload or preview a current trade log (CSV)
- Calculate unrealised P&L and return metrics
- Assess exposure concentration by sector, strategy, and country
- Identify positions that breach structural risk thresholds
- Apply leverage-adjusted diagnostics for portfolio health and tiering

All logic is non-advisory and structurally aligned with DSS architecture.
It supports trade transparency, strategy refinement, and capital allocation awareness
— but does not replace brokerage reporting or account-level analytics.

Inputs:
- Portfolio trade snapshot in a structured CSV format
- Capital base and optional global leverage assumptions

Outputs:
- Summary metrics, sortable tables, and interactive charts
- Validation flags for structural or logic issues
- Diagnostic tiers and concentration overlays for risk signalling

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
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_live_portfolio_monitor.md")
HELP_APP_MD = os.path.join(ROOT_PATH, "docs", "help_live_portfolio_monitor.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
SAMPLE_FILE = os.path.join(
APPS_PATH, "observation_engine", "sample_inputs",
"sample_live_portfolio.csv"
)

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# 🧠 Observation Tools (User Observation Logging — Group A)
# -------------------------------------------------------------------------------------------------
from observation_handler_live_monitor import (
    observation_input_form,
    display_observation_log
)

from render_macro_interaction_tools_panel_live_monitor import render_macro_interaction_tools_panel
from macro_insight_sidebar_panel_trade_portfolio_structuring import render_macro_sidebar_tools

# -------------------------------------------------------------------------------------------------
# 🧭 Live Portfolio Monitor Template + Validator
# -------------------------------------------------------------------------------------------------
from portfolio_trade_modules.live_portfolio_template import get_live_portfolio_template
from portfolio_trade_modules.live_trade_validator import validate_live_trade_log

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
st.set_page_config(page_title="Live Portfolio Monitor", layout="wide")
st.title("🧭 Live Portfolio Monitor")
st.caption(
    "*Monitor open trades, leverage use, and portfolio-level diagnostics.*"
)

# -------------------------------------------------------------------------------------------------
# Info Panel
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_live_portfolio_monitor.md")

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
# Sidebar — Upload and Template
# -------------------------------------------------------------------------------------------------
st.sidebar.markdown("### 📥 Live Portfolio Setup")

uploaded_file = st.sidebar.file_uploader("Upload your portfolio snapshot (.csv)", type="csv")

df_template = get_live_portfolio_template()
st.sidebar.download_button(
    label="📥 Get Portfolio Template",
    data=df_template.to_csv(index=False).encode("utf-8"),
    file_name="live_portfolio_template.csv",
    mime="text/csv",
    help="Download a structured example of the required portfolio format."
)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Sidebar Section Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.markdown("### 📂 Select Portfolio Views")
selected_sections = st.sidebar.multiselect(
    "Choose one or more views:",
    [
        "📋 Position Table",
        "📈 Exposure Breakdown",
        "⚠️ Risk Diagnostics",
        "🛠️ Live Validator"
    ],
    default=[]
)
st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Section 1: Portfolio Summary (Always Active)
# -------------------------------------------------------------------------------------------------
st.subheader("📊 Portfolio Summary")
st.markdown("_Overview of current live positions, exposure, and unrealised returns._")

# -------------------------------------------------------------------------------------------------
# Load and Validate Portfolio
# -------------------------------------------------------------------------------------------------
use_sample = False
if uploaded_file:
    try:
        df_portfolio = pd.read_csv(uploaded_file)
    except Exception:
        st.error("❌ Could not read file. Please ensure it's a valid CSV.")
        df_portfolio = None
else:
    df_portfolio = pd.read_csv(SAMPLE_FILE)
    use_sample = True

# -------------------------------------------------------------------------------------------------
# Apply Validation and Compute Metrics
# -------------------------------------------------------------------------------------------------
validation = None
if df_portfolio is not None:
    validation = validate_live_trade_log(df_portfolio)
    if not validation["valid"]:
        st.error("⚠️ Issues found in Live Portfolio log:")
        for err in validation["errors"]:
            st.markdown(f"- {err}")
        st.divider()
        df = None
        df_filtered = pd.DataFrame()
    else:
        df_clean = validation["cleaned_df"]
        df = df_clean.copy()

        # Capital Configuration
        st.sidebar.markdown("### ⚙️ Capital Configuration")
        capital = st.sidebar.number_input("Account Capital ($)", min_value=1000,
        value=100000, step=1000,
            help=("Used to calculate each position’s % of portfolio. "
                  "This represents your total available account size or funding base. "
                  "Adjusting this changes exposure diagnostics but does not alter P&L or \
                  trade-level metrics."))
        global_leverage = st.sidebar.slider("Global Leverage (default)", min_value=1.0,
        max_value=10.0, value=1.0, step=0.1)

        with st.sidebar.expander("ℹ️ Leverage Rules Explained"):
            st.markdown("""
        - A value of `1.0` for **Leverage Used** means **no leverage** — full capital backing.
        - A value of `0` or a blank cell will default to the configured \
        **Global Leverage** (slider).
        - If **Global Leverage** is set to `1.0`, then no fallback leverage is applied.
        - This structure ensures clarity across mixed product types: equity, crypto, CFDs, and FX.

        ✅ Use `1.0` for capital-only exposure.
        ⚠️ Use `>1.0` for leveraged positions.
        🚫 Avoid `0` — it triggers fallback logic.
            """)

        # Apply leverage fallback
        if "Leverage Used" in df.columns:
            df["Leverage Used"] = pd.to_numeric(df["Leverage Used"], errors="coerce")
            df["Leverage Used"] = df["Leverage Used"].replace(0, pd.NA).fillna(global_leverage)
        else:
            df["Leverage Used"] = global_leverage

        # Calculations
        df["Unrealised P&L"] = (df["Current Price"] - df["Entry Price"]) * df["Position Size"]
        df["Return %"] = (df["Unrealised P&L"] / (df["Entry Price"] * df["Position Size"])) * 100
        df["Position Value"] = df["Current Price"] * df["Position Size"]
        df["Leverage-Adjusted Value"] = df["Position Value"] * df["Leverage Used"]
        df["Percent of Portfolio"] = (df["Leverage-Adjusted Value"] / capital) * 100

# -------------------------------------------------------------------------------------------------
# Global Filter: Apply Once to Shared df
# -------------------------------------------------------------------------------------------------
        df_filtered = df.copy()
        if not df.empty and "Symbol" in df.columns:
            st.sidebar.markdown("### 🔍 Filter Portfolio")
            asset_options = sorted(df["Symbol"].dropna().unique())
            selected_assets = st.sidebar.multiselect(
                "Filter by Symbol",
                options=asset_options,
                default=asset_options,
                help="Select which Symbol to include in all portfolio views."
            )
            df_filtered = df[df["Symbol"].isin(selected_assets)].copy()

        # Sidebar Summary
        st.sidebar.markdown("### 🧾 Portfolio Summary")
        st.sidebar.success("✅ Portfolio loaded successfully.")
        if use_sample:
            st.sidebar.info("📂 Using sample portfolio snapshot.")
        st.sidebar.markdown(f"**Records:** {len(df)}")
        st.sidebar.markdown(f"**Sample:** {'Yes' if use_sample else 'No'}")

        with st.expander("📋 Preview Uploaded Portfolio"):
            st.dataframe(df, use_container_width=True)

        # Display Metrics
        st.markdown(" ")
        gross_exposure = df["Position Value"].sum()
        leverage_adjusted = df["Leverage-Adjusted Value"].sum()
        unrealised_pnl = df["Unrealised P&L"].sum()
        avg_return = df["Return %"].mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Gross Exposure", f"${gross_exposure:,.2f}")
        col2.metric("Leverage-Adjusted", f"${leverage_adjusted:,.2f}")
        col3.metric("Unrealised P&L", f"${unrealised_pnl:,.2f}")
        col4.metric("Avg Return %", f"{avg_return:.2f}%")

        st.caption("Returns shown are unrealised. Per-position leverage is applied where \
        specified. Positions with no leverage or `1.0` are treated as fully capital-backed. \
        No fixed exposure ceiling is applied.")

with st.expander("ℹ️ Interpretation Guidance"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_live_portfolio_monitor.md")

# -------------------------------------------------------------------------------------------------
# Section: 📋 Position Table
# -------------------------------------------------------------------------------------------------
if "📋 Position Table" in selected_sections and df_filtered is not None:
    st.subheader("📋 Live Position Table")
    st.markdown("_Sortable table of open trades with dynamic return calculation._")

    ordered_cols = [
        "Symbol", "Asset", "Entry Date", "Direction", "Entry Price", "Current Price",
        "Position Size", "Position Value", "Unrealised P&L", "Return %", "Sector",
        "Country", "Strategy Tag", "Notes"
    ]
    df_display = df_filtered[[col for col in ordered_cols if col in df_filtered.columns]].copy()

    # Format date to remove timestamp
    if "Entry Date" in df_display.columns:
        df_display["Entry Date"] = pd.to_datetime(df_display["Entry Date"]).dt.strftime("%Y-%m-%d")

    # Clip return %
    if "Return %" in df_display.columns:
        df_display["Return %"] = df_display["Return %"].clip(-9999, 9999).round(2)

    if not df_display.empty:
        cellstyle_profit_loss = JsCode("""
            function(params) {
                if (params.value > 0) {
                    return {'color': 'white', 'backgroundColor': '#4CAF50', 'fontWeight': '400'}
                } else if (params.value < 0) {
                    return {'color': 'white', 'backgroundColor': '#EF5350', 'fontWeight': '400'}
                } else {
                    return {'color': 'white', 'backgroundColor': '#90A4AE', 'fontWeight': '400'}
                }
            }
        """)

        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_grid_options(domLayout='normal', rowHeight=28)
        gb.configure_pagination(paginationPageSize=20)
        gb.configure_default_column(editable=False, filter=True, sortable=True)
        gb.configure_side_bar()

        # Pinned column order: Symbol then Asset
        gb.configure_column("Symbol", pinned="left")
        gb.configure_column("Asset", pinned="left")

        gb.configure_column("Unrealised P&L", type=["numericColumn"], precision=2,
        cellStyle=cellstyle_profit_loss)
        gb.configure_column("Return %", type=["numericColumn"], precision=2,
        cellStyle=cellstyle_profit_loss)
        gb.configure_column("Position Value", type=["numericColumn"], precision=2)

        AgGrid(
            df_display,
            gridOptions=gb.build(),
            enable_enterprise_modules=False,
            fit_columns_on_grid_load=True,
            theme="balham",
            height=440,
            allow_unsafe_jscode=True
        )
    else:
        st.warning("📋 No data available for position table.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Exposure Breakdown Section (Platinum Version)
# -------------------------------------------------------------------------------------------------
if "📈 Exposure Breakdown" in selected_sections and df_filtered is not None:
    st.subheader("📈 Exposure Breakdown")
    st.markdown("_Visualise portfolio concentration across sector, country, and \
    strategy dimensions._")

    exposure_cols = ["Sector", "Country", "Strategy Tag"]
    metric_col = "Leverage-Adjusted Value"

    for dimension in exposure_cols:
        if dimension in df_filtered.columns:
            exp_df = (
                df_filtered.groupby([dimension, "Direction"])[metric_col]
                .sum()
                .reset_index()
            )
            exp_pivot = exp_df.pivot_table(
                index=dimension,
                columns="Direction",
                values=metric_col,
                fill_value=0
            )
            exp_pivot["Total"] = exp_pivot.sum(axis=1)
            exp_pivot["% of Total"] = (exp_pivot["Total"] / exp_pivot["Total"].sum()) * 100
            exp_pivot = exp_pivot.sort_values("Total", ascending=False)

            # Add totals row
            totals_row = pd.DataFrame(exp_pivot.sum(numeric_only=True)).T
            totals_row.index = ["Total"]
            totals_row["% of Total"] = 100.0
            exp_pivot = pd.concat([exp_pivot, totals_row])

            # Display table
            st.markdown(f"### 📊 {dimension} Exposure")
            st.dataframe(exp_pivot.reset_index(), use_container_width=False)

            # Prepare chart data (exclude Total)
            chart_data = exp_pivot.drop(index="Total", errors="ignore").reset_index()
            if "index" in chart_data.columns:
                chart_data.rename(columns={"index": dimension}, inplace=True)

            fig = px.pie(
                chart_data,
                names=dimension,
                values="Total",
                title=f"{dimension} Allocation",
                hole=0.35,
                width=450,
                height=400,
                color_discrete_sequence=["#4CAF50", "#90A4AE", "#EF5350"]
            )
            fig.update_traces(textinfo='label+percent', textfont_size=13)
            fig.update_layout(margin={"t": 40, "b": 10, "l": 10, "r": 10})
            st.plotly_chart(fig, use_container_width=False)

            st.caption("Breakdown includes both long and short positions. Allocation shown \
            as share of total leverage-adjusted exposure.")
        else:
            st.warning(f"Column '{dimension}' not found in uploaded data.")

# -------------------------------------------------------------------------------------------------
# Section: ⚠️ Risk Diagnostics — Platinum Version with Tiering
# -------------------------------------------------------------------------------------------------
if "⚠️ Risk Diagnostics" in selected_sections and df_filtered is not None:
    st.subheader("⚠️ Risk Diagnostics")
    st.markdown("_Identify high-risk exposures based on leverage, position size, \
    and concentration._")

    df_risk = df_filtered.copy()
    warnings_list = []

    # --- Thresholds ---
    max_pct_per_position = 25
    max_pct_asset = 25
    max_pct_sector = 50

    # --- Oversized positions ---
    df_risk["Over Max Exposure"] = (
    df_risk["Leverage-Adjusted Value"] / capital * 100) > max_pct_per_position
    num_over_exposure = df_risk["Over Max Exposure"].sum()
    if num_over_exposure > 0:
        warnings_list.append(
        f"🚨 {num_over_exposure} positions exceed {max_pct_per_position}% of account capital.")

    # --- Asset concentration ---
    asset_group = df_risk.groupby("Asset")["Leverage-Adjusted Value"].sum()
    asset_concentration = (asset_group / capital * 100).reset_index()
    asset_concentration.columns = ["Asset", "% of Capital"]
    high_asset_conc = asset_concentration[asset_concentration["% of Capital"] > max_pct_asset]
    if not high_asset_conc.empty:
        warnings_list.append(f"⚠️ {len(high_asset_conc)} assets exceed {max_pct_asset}% of \
        capital allocation.")

    # --- Sector concentration ---
    if "Sector" in df_risk.columns:
        sector_group = df_risk.groupby("Sector")["Leverage-Adjusted Value"].sum()
        sector_concentration = (sector_group / capital * 100).reset_index()
        sector_concentration.columns = ["Sector", "% of Capital"]
        high_sector_conc = sector_concentration[sector_concentration[
        "% of Capital"] > max_pct_sector
        ]
        if not high_sector_conc.empty:
            warnings_list.append(
            f"📌 {len(high_sector_conc)} sectors exceed {max_pct_sector}% of capital exposure."
            )

    # --- Display summary ---
    if warnings_list:
        for w in warnings_list:
            st.warning(w)
    else:
        st.success("✅ No immediate risk flags detected based on configured thresholds.")

    # --- Flagged Table ---
    st.markdown("### 📋 Positions Exceeding Risk Thresholds")
    flagged = df_risk[df_risk["Over Max Exposure"]]
    if not flagged.empty:
        st.dataframe(flagged[[
            "Asset", "Symbol", "Leverage-Adjusted Value", "Leverage Used", "Return %",
            "Sector", "Country", "Strategy Tag"
        ]], use_container_width=True)
    else:
        st.info("No positions currently exceed risk thresholds.")


    # --- Risk Tier Classification ---
    def classify_risk_tier(pct):
        """
        Classify a position’s portfolio weight into a structural risk tier.

        Parameters:
            pct (float): Position weight as a percentage of total portfolio.

        Returns:
            str: Assigned risk tier label:
                - '🔴 High' for ≥15%
                - '🟡 Moderate' for ≥10%
                - '🟢 Light' for ≥5%
                - '✅ Low' for <5%

        Note:
            Tiers are used for diagnostic clarity only and carry no advisory interpretation.
        """
        if pct >= 15:
            return "🔴 High"
        if pct >= 10:
            return "🟡 Moderate"
        if pct >= 5:
            return "🟢 Light"
        return "✅ Low"

    df_risk["Risk Tier"] = df_risk["Percent of Portfolio"].apply(classify_risk_tier)

    # --- Risk Tier Summary Table ---
    st.markdown("### 🧮 Risk Tier Distribution")
    risk_tier_counts = df_risk["Risk Tier"].value_counts().reset_index()
    risk_tier_counts.columns = ["Risk Tier", "Count"]
    st.dataframe(risk_tier_counts, use_container_width=False)

    # --- Risk Tier Pie Chart ---
    fig_tier = px.pie(
        risk_tier_counts,
        names="Risk Tier",
        values="Count",
        title="Risk Tier Distribution",
        color_discrete_sequence=px.colors.sequential.Tealgrn,
        hole=0.4
    )
    fig_tier.update_layout(margin={"t": 40, "b": 10, "l": 10, "r": 10}, height=400, width=450)
    st.plotly_chart(fig_tier, use_container_width=False)

    # --- Sector Breakdown by Risk Tier ---
    st.markdown("### 📊 Sector Exposure by Risk Tier")
    tier_sector = df_risk.groupby(["Sector", "Risk Tier"]).size().reset_index(name="Count")
    fig_sector = px.bar(
        tier_sector,
        x="Sector",
        y="Count",
        color="Risk Tier",
        barmode="group",
        title="Sector Distribution Across Risk Tiers",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )
    fig_sector.update_layout(margin={"t": 30, "b": 30}, height=450)
    st.plotly_chart(fig_sector, use_container_width=True)

    st.caption("Diagnostics are based on leverage-adjusted position size and "
    "portfolio concentration. Tier classification is structural — not advisory.")

# -------------------------------------------------------------------------------------------------
# Section: 🛠️ Live Validator
# -------------------------------------------------------------------------------------------------
if "🛠️ Live Validator" in selected_sections and validation is not None:
    st.subheader("🛠️ Live Validator")
    st.markdown("_Structure and logic checks from initial upload validation._")

    summary_tabs = st.tabs(["🔍 Summary", "📄 Detail"])

    # --- Summary Tab ---
    with summary_tabs[0]:
        if validation["warnings"]:
            st.warning("⚠️ Structural or logical issues were identified:")
            for w in validation["warnings"]:
                st.markdown(f"- {w}")
        else:
            st.success("✅ No structural or logic warnings detected in uploaded portfolio.")

        st.caption("Warnings include duplicated entries, inactive trades, or unusual values.")

    # --- Detail Tab ---
    with summary_tabs[1]:
        df_valid = validation["cleaned_df"]
        if df_valid is not None:
            # Duplicate symbol + entry date check
            dupes = df_valid[df_valid.duplicated(subset=["Symbol", "Entry Date"], keep=False)]
            if not dupes.empty:
                st.markdown("### 🔁 Duplicate Trades Detected")
                st.dataframe(dupes, use_container_width=True)

            # No price movement check
            no_move = df_valid[df_valid["Current Price"] == df_valid["Entry Price"]]
            if not no_move.empty:
                st.markdown("### ⚠️ No Price Movement")
                st.dataframe(no_move, use_container_width=True)

            # Invalid or fallback leverage check
            fallback_leverage = df_valid[df_valid["Leverage Used"] == global_leverage]
            if not fallback_leverage.empty:
                st.markdown(f"### ⚠️ Default Leverage Applied ({global_leverage}x)")
                st.dataframe(fallback_leverage, use_container_width=True)
        else:
            st.info("ℹ️ No valid records available for deep validation review.")

    st.caption("These diagnostics mirror checks applied during initial file ingestion and \
are intended to improve transparency and ensure future sections operate correctly.")

st.divider()

# -------------------------------------------------------------------------------------------------
# 🧠 Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
theme_code = "live_portfolio"
theme_title = "Live Portfolio Monitor"
selected_use_case = "Portfolio Health Snapshot"

# -------------------------------------------------------------------------------------------------
# 🧠 Activate Observation + Journal Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case
)

# 🎯 No fixed assets selected in live dashboard — use empty list
asset_list_for_observation = []

if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")
    st.caption("*Capture general reflections on trading performance, decision patterns, "
    "or strategic lessons from this review window.*")

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
