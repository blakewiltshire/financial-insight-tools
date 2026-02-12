# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📏 Break-Even Distance Calculator

Calculate the minimum move needed to cover costs and reach profitability.
Useful for determining the distance an asset must move in favour of the position to offset fees,
spreads, and slippage.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_break_even_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_break_even_calculator.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Break-Even Distance Calculator", layout="wide")
st.title("📏 Break-Even Distance Calculator")
st.caption("*Estimate the minimum price shift required to cover trading costs.*")

# -------------------------------------------------------------------------------------------------
# Info Panels
# -------------------------------------------------------------------------------------------------
with st.expander("📘 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_break_even_calculator.md")

with st.expander("ℹ️ How to interpret break-even distance"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_break_even_calculator.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠️ Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Break-Even Calculator Inputs
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📊 Cost and Trade Inputs")
entry_price = st.sidebar.number_input("Entry Price ($)", min_value=0.01, value=100.0, step=0.1)
spread = st.sidebar.number_input("Spread (Per Side, $)", min_value=0.0, value=0.5, step=0.1,
    help="Bid/Ask spread cost per side. Doubled to reflect round-trip.")
slippage = st.sidebar.number_input("Estimated Slippage ($)", min_value=0.0, value=0.5, step=0.1)
fixed_fee = st.sidebar.number_input("Platform / Fixed Fees ($)", min_value=0.0, value=0.25,
step=0.1)
shares = st.sidebar.number_input("Number of Shares", min_value=1, value=1, step=1)

# -------------------------------------------------------------------------------------------------
# Calculation Logic
# -------------------------------------------------------------------------------------------------
per_share_cost = (spread * 2) + slippage + (fixed_fee / shares)
break_even_per_share = entry_price + per_share_cost
break_even_percent = (break_even_per_share - entry_price) / entry_price * 100

total_cost = per_share_cost * shares
total_entry = entry_price * shares
total_break_even = break_even_per_share * shares

# -------------------------------------------------------------------------------------------------
# Summary Output
# -------------------------------------------------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Break-Even Summary")
    st.markdown(f"- **Entry Price:** `${entry_price:.2f}`")
    st.markdown(f"- **Shares:** `{shares}`")
    st.markdown(f"- **Total Trading Cost:** `${total_cost:.2f}`")
    st.markdown(f"- **Break-Even Price Per Share:** `${break_even_per_share:.2f}`")
    st.markdown(f"- **Total Break-Even Value:** `${total_break_even:.2f}`")
    st.markdown(f"- **Distance to Break Even:** `{break_even_percent:.2f}%`")
    st.caption("This is the minimum price movement required in your favour to offset costs.")

# -------------------------------------------------------------------------------------------------
# Chart Output
# -------------------------------------------------------------------------------------------------
with col2:
    tabs = st.tabs(["📈 Per Share View", "📊 Total Value View"])

    # Dynamically widen buffer based on how far break-even deviates from entry
    buffer_per_share = max(5, abs(break_even_per_share - entry_price) * 1.5)
    price_range = np.linspace(entry_price - buffer_per_share, entry_price + buffer_per_share, 200)

    # --- Per Share Chart ---
    with tabs[0]:
        pnl_per_share = price_range - entry_price - per_share_cost
        hover_text = [
        f"Exit Price: ${x:.2f}<br>P&L: ${y:.2f}" for x, y in zip(price_range, pnl_per_share)
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_range,
            y=pnl_per_share,
            mode="lines",
            name="P&L per Share",
            line={"color": "black", "width": 2},
            hoverinfo="text",
            text=hover_text
        ))

        fig.add_trace(go.Scatter(
            x=[break_even_per_share, break_even_per_share],
            y=[min(pnl_per_share), max(pnl_per_share)],
            mode="lines",
            line={"color": "blue", "width": 2, "dash": "dot"},
            showlegend=False
        ))

        fig.add_annotation(
            x=break_even_per_share,
            y=max(pnl_per_share),
            text="Min Required Move",
            showarrow=False,
            yshift=20,
            font={"color": "blue", "size": 12}
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="Break-Even",
            annotation_position="bottom left",
            annotation_font={"size": 12},
            annotation={"yshift": -30}
        )

        fig.update_layout(
            title={"text": "Break-Even per Share", "x": 0.5, "font": {"size": 18}},
            xaxis_title="Exit Price ($)",
            yaxis_title="P&L per Share ($)",
            template="simple_white",
            height=460,
            margin={"l": 40, "r": 40, "t": 80, "b": 60},
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "📉 This chart shows net profit or loss per share as the exit price changes. "
            "The blue marker highlights the minimum break-even level — where total "
            "trading costs are recovered."
        )

    # --- Total Value Chart ---
    with tabs[1]:
        total_break_even_deviation = abs(total_break_even - total_entry)
        buffer_total = max(5 * shares, total_break_even_deviation * 1.5)
        total_prices = np.linspace(total_entry - buffer_total, total_entry + buffer_total, 200)
        pnl_total = total_prices - total_entry - total_cost
        hover_text_total = [
        f"Exit Value: ${x:.2f}<br>Total P&L: ${y:.2f}" for x, y in zip(total_prices, pnl_total)
        ]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=total_prices,
            y=pnl_total,
            mode="lines",
            name="Net P&L",
            line={"color": "black", "width": 2},
            hoverinfo="text",
            text=hover_text_total
        ))

        fig2.add_trace(go.Scatter(
            x=[total_break_even, total_break_even],
            y=[min(pnl_total), max(pnl_total)],
            mode="lines",
            line={"color": "blue", "width": 2, "dash": "dot"},
            showlegend=False
        ))

        fig2.add_annotation(
            x=total_break_even,
            y=max(pnl_total),
            text="Min Required Move",
            showarrow=False,
            yshift=20,
            font={"color": "blue", "size": 12}
        )

        fig2.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="Break-Even",
            annotation_position="bottom left",
            annotation_font={"size": 12},
            annotation={"yshift": -30}
        )

        fig2.update_layout(
            title={"text": "Total Trade Break-Even", "x": 0.5, "font": {"size": 18}},
            xaxis_title="Total Exit Value ($)",
            yaxis_title="Net P&L ($)",
            template="simple_white",
            height=460,
            margin={"l": 40, "r": 40, "t": 80, "b": 60},
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.caption(
            "📉 This chart shows net profit or loss for the entire position as the exit value "
            "changes. The blue marker highlights the minimum break-even level — where "
            "total trading costs are recovered."
        )

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    with open(os.path.join(PROJECT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
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
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
           "No trading, investment, or policy advice provided.")
