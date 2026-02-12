# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
💸 Compounding Calculator

Visualise how recurring investments grow with compounding over time.
Supports monthly or annual contributions and allows inflation and tax drag adjustment.
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
import pandas as pd
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

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_compounding_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_compounding_calculator.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Compounding Calculator", layout="wide")
st.title("💸 Compounding Calculator")
st.caption("*Understand how contributions and time impact portfolio outcomes.*")

# -------------------------------------------------------------------------------------------------
# Info Panels
# -------------------------------------------------------------------------------------------------
with st.expander("📘 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_compounding_calculator.md")

with st.expander("ℹ️ How to interpret investment compounding"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_compounding_calculator.md")

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
# Input Parameters
# -------------------------------------------------------------------------------------------------
st.sidebar.title("💳 Investment Parameters")
initial = st.sidebar.number_input("Initial Investment ($)", min_value=0, value=1000, step=100)
contribution = st.sidebar.number_input("Recurring Contribution ($)", min_value=0,
value=200, step=50)
frequency = st.sidebar.selectbox("Contribution Frequency", ["Monthly", "Annually"])
years = st.sidebar.slider("Time Horizon (Years)", min_value=1, max_value=50, value=20)
rate = st.sidebar.slider("Expected Annual Return (%)", min_value=1.0, max_value=20.0, value=7.0)
adjust_for_inflation = st.sidebar.checkbox("Adjust for Inflation (2%)", value=False)
estimated_tax_drag = st.sidebar.slider(
    "Estimated Annual Tax Drag (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.1,
    help="Optional. Applies an annualised adjustment to account for tax-related return reductions."
)

# Apply tax drag to the nominal return
effective_rate = rate * (1 - estimated_tax_drag / 100)

# -------------------------------------------------------------------------------------------------
# Compounding Logic
# -------------------------------------------------------------------------------------------------
# pylint: disable=redefined-outer-name, too-many-arguments
def calculate_compound_growth(initial, contribution, frequency, years, rate, inflation):
    """
    Calculate compound growth over time with optional inflation adjustment.

    Parameters:
        initial (float): Initial investment amount.
        contribution (float): Recurring contribution per period.
        frequency (str): "Monthly" or "Annually", determines compounding frequency.
        years (int): Total investment duration in years.
        rate (float): Nominal annual return rate (in percent).
        inflation (bool): Whether to adjust for inflation using a fixed 2% annual rate.

    Returns:
        pd.DataFrame: A DataFrame containing period-by-period breakdown of:
            - Balance (after growth and inflation)
            - Cumulative contributions
            - Growth (net of contributions)
    """
    periods = years * (12 if frequency == "Monthly" else 1)
    rate_per_period = (rate / 100) / (12 if frequency == "Monthly" else 1)
    inflation_rate = 0.02 / (12 if frequency == "Monthly" else 1) if inflation else 0

    values, contributions = [], []
    balance = initial
    for i in range(periods):
        balance *= (1 + rate_per_period)
        balance += contribution
        balance /= (1 + inflation_rate)
        values.append(balance)
        contributions.append(initial + contribution * (i + 1))

    return pd.DataFrame({
        "Period": list(range(1, periods + 1)),
        "Balance": values,
        "Contributions": contributions,
        "Growth": [v - c for v, c in zip(values, contributions)]
    })

results_df = calculate_compound_growth(initial, contribution, frequency, years, effective_rate,
adjust_for_inflation)

# -------------------------------------------------------------------------------------------------
# Summary Output
# -------------------------------------------------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Summary")
    st.markdown(f"- **Final Balance:** `${results_df['Balance'].iloc[-1]:,.2f}`")
    st.markdown(f"- **Total Contributions:** `${results_df['Contributions'].iloc[-1]:,.2f}`")
    st.markdown(f"- **Total Growth:** `${results_df['Growth'].iloc[-1]:,.2f}`")
    st.markdown(f"- **Periods:** `{len(results_df)}` ({frequency})")
    if adjust_for_inflation:
        st.caption("Inflation-adjusted to 2% annual.")
    if estimated_tax_drag > 0:
        st.caption(f"📉 Adjusted return used for compounding: {effective_rate:.2f}% "
                   f"(after {estimated_tax_drag:.1f}% tax drag)")

with col2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=results_df["Period"],
        y=results_df["Balance"],
        name="Total Balance",
        line={"color": "green", "width": 2}
    ))
    fig.add_trace(go.Scatter(
        x=results_df["Period"],
        y=results_df["Contributions"],
        name="Total Contributions",
        line={"color": "gray", "dash": "dot"}
    ))
    fig.update_layout(
        title="Investment Growth Over Time",
        xaxis_title="Period",
        yaxis_title="Amount ($)",
        template="simple_white",
        margin={"l": 20, "r": 20, "t": 60, "b": 40}
    )
    st.plotly_chart(fig, width='stretch')

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
            width='stretch',
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width='stretch',
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
           "No trading, investment, or policy advice provided.")
