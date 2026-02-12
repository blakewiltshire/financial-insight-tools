# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🧠 Kelly Criterion Calculator

Helps estimate optimal bet size based on risk-reward scenarios and win probability.
Supports manual configuration or automated inference from trade history.

Key Features:
- Input win probability and payoff ratios manually, or upload trade results.
- Auto-calculate optimal Kelly allocation from historic trade data.
- Visualise risk-reward structure.
- Reference tool for Trade Structuring & Risk Planning modules.

Note: This tool supports structural decision logic — it does not prescribe or advise.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys
from glob import glob

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

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_kelly_criterion_calculator.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_kelly_criterion_calculator.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")
TRADE_HISTORY_PATH = os.path.join(PROJECT_PATH, "apps", "data_sources",
"financial_data", "trade_history")

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Kelly Criterion Calculator", layout="wide")
st.title("🧠 Kelly Criterion Calculator")
st.caption("*Optimise position sizing based on probability and reward-to-risk ratios.*")

# -------------------------------------------------------------------------------------------------
# Info Panels
# -------------------------------------------------------------------------------------------------
with st.expander("📘 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_kelly_criterion_calculator.md")

with st.expander("ℹ️ How to interpret Kelly sizing"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_kelly_criterion_calculator.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠️ Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Load Latest Trade History Automatically
# -------------------------------------------------------------------------------------------------
def get_latest_trade_history():
    """
    Retrieve the most recent trade history CSV from the data directory.

    Returns:
        pd.DataFrame or None: The contents of the latest trade history file
        as a DataFrame, or None if no matching files are found.
    """
    history_dir = os.path.join(PROJECT_PATH, "apps", "data_sources", "financial_data",
    "trade_history")
    files = glob(os.path.join(history_dir, "trade_history_*.csv"))
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return pd.read_csv(latest_file)

# -------------------------------------------------------------------------------------------------
# Load Default Trade History If Available
# -------------------------------------------------------------------------------------------------
df = None
default_trade_history = get_latest_trade_history()
if default_trade_history is not None:
    df = default_trade_history
    auto_loaded = True

# -------------------------------------------------------------------------------------------------
# Trade History Upload or Auto-load
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📄 Upload Trade History (Optional)")

with st.sidebar.expander("ℹ️ Upload Format Guide"):
    st.markdown("""
Upload a simple trade history file to estimate Kelly Criterion from actual results.

**Required Columns:**
- `result`: must be `"win"` or `"loss"`
- `win`: profit amount (leave blank if loss)
- `loss`: loss amount (leave blank if win)

**Example Format:**

| result | win   | loss  |
|--------|-------|-------|
| win    | 5000  |       |
| loss   |       | 3000  |
| win    | 12000 |       |
| loss   |       | 4500  |

Use a CSV file with these three columns. No header adjustments are required.
""")

uploaded_file = st.sidebar.file_uploader("Upload CSV (Override)", type="csv")

use_uploaded = False
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    use_uploaded = True
else:
    df = get_latest_trade_history()
    use_uploaded = df is not None

if use_uploaded:
    try:
        wins = df[df['result'] == 'win']['win'].sum()
        losses = df[df['result'] == 'loss']['loss'].sum()
        n_wins = df[df['result'] == 'win'].shape[0]
        n_total = df.shape[0]
        win_prob = n_wins / n_total if n_total > 0 else 0.0
        avg_win = wins / n_wins if n_wins > 0 else 0.0
        avg_loss = losses / (n_total - n_wins) if (n_total - n_wins) > 0 else 0.0
        R = avg_win / avg_loss if avg_loss > 0 else 0.0
    except (KeyError, ZeroDivisionError, pd.errors.ParserError, TypeError) as e:
        st.sidebar.error("Invalid format. Expecting columns: result, win, loss")
        use_uploaded = False


# -------------------------------------------------------------------------------------------------
# Kelly Formula Logic
# -------------------------------------------------------------------------------------------------
# pylint: disable=redefined-outer-name
def calculate_kelly_fraction(p, R):
    """
    Calculate the optimal Kelly fraction for trade sizing.

    Parameters:
        p (float): Probability of winning the trade (0 < p < 1).
        R (float): Reward-to-risk ratio (expected return per unit risk).

    Returns:
        float: Fraction of capital to allocate based on Kelly criterion.
               Returns 0.0 if R is zero or result is negative.
    """
    q = 1 - p
    return max(p - q / R, 0.0) if R != 0 else 0.0

# -------------------------------------------------------------------------------------------------
# User Input or Derived Metrics
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📊 Kelly Inputs")

if use_uploaded:
    st.sidebar.success("Trade history detected. Using derived inputs.")
    st.sidebar.caption(
        "This module has automatically calculated win rates and reward/risk ratios "
        "from your trade history file. These values inform the Kelly Fraction below."
    )
    win_probability = win_prob
    reward_risk_ratio = R
else:
    st.sidebar.warning("No trade file detected. Using default manual values.")
    win_probability = st.sidebar.slider("Win Probability (%)", 10, 100, 60) / 100
    reward_risk_ratio = st.sidebar.slider("Reward-to-Risk Ratio (R)", 0.1, 10.0, 2.0)

scaling_factor = st.sidebar.slider(
    "Capital Allocation (% of Kelly)", min_value=10, max_value=100, value=100
) / 100
st.sidebar.caption(
    "Adjust how much of the calculated Kelly position size to apply. "
    "Lower values reduce exposure while preserving signal integrity."
)

kelly_fraction = calculate_kelly_fraction(win_probability, reward_risk_ratio)
adjusted_fraction = kelly_fraction * scaling_factor


# -------------------------------------------------------------------------------------------------
# Main Display
# -------------------------------------------------------------------------------------------------
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### Optimal Kelly Positioning")
    st.markdown(
    f"- **Estimated Kelly Fraction:** `{kelly_fraction:.4f}` ({kelly_fraction*100:.2f}%)")
    st.markdown(
    f"- **Applied Fraction (Scaled):** `{adjusted_fraction:.4f}` ({adjusted_fraction*100:.2f}%)")
    st.markdown(f"- **Observed Win Probability:** `{win_probability*100:.1f}%`")
    st.markdown(f"- **Observed Reward-to-Risk Ratio (R):** `{reward_risk_ratio:.2f}`")

    if use_uploaded:
        st.markdown(
        f"- **Derived from:** `{n_total} trades` — `{n_wins} wins`, `{n_total - n_wins} losses`"
        )

    st.caption(
        "This output represents the theoretical allocation percentage that maximises expected "
        "long-term growth based on the Kelly criterion. The applied fraction allows optional "
        "scaling to reflect partial staking, risk preferences, or volatility considerations.\n\n"
        "The results do not recommend action but provide a lens into how historic "
        "trade performance might influence position sizing logic."
    )

with col2:
    x = np.linspace(0, 1.0, 200)
    y = [(win_probability * reward_risk_ratio - (1 - win_probability)) * f -
         0.5 * reward_risk_ratio * f**2 for f in x]

    fig = go.Figure()

    # Main growth curve
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="Expected Growth Curve",
        line={"color": "black", "width": 2},
        hovertemplate="Capital Allocated: %{x:.2f}<br>Expected Return: %{y:.4f}<extra></extra>"
    ))

    # Kelly dots
    raw_kelly_y = (
    win_probability * reward_risk_ratio - (
    1 - win_probability)) * kelly_fraction - 0.5 * reward_risk_ratio * kelly_fraction**2

    applied_kelly_y = (
    win_probability * reward_risk_ratio - (
    1 - win_probability)) * adjusted_fraction - 0.5 * reward_risk_ratio * adjusted_fraction**2

    # Conditional y-offset for annotations
    vertical_spacing = 20  # lower vertical distance from top
    horizontal_offset = 0.000  # x offset for clarity of required

    # Raw Kelly
    fig.add_trace(go.Scatter(
        x=[kelly_fraction],
        y=[raw_kelly_y],
        mode="markers",
        marker={"color": "green", "size": 6},
        name="Raw Kelly",
        hovertemplate="Raw Kelly Fraction: %{x:.2%}<extra></extra>"
    ))

    fig.add_annotation(
        x=kelly_fraction - horizontal_offset,
        y=raw_kelly_y,
        text="Raw Kelly",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-vertical_spacing,
        font={"color": "green", "size": 12},
        arrowcolor="green"
    )

    # Applied Kelly
    fig.add_trace(go.Scatter(
        x=[adjusted_fraction],
        y=[applied_kelly_y],
        mode="markers",
        marker={"color": "blue", "size": 6},
        name="Applied Kelly",
        hovertemplate="Applied Kelly Fraction: %{x:.2%}<extra></extra>"
    ))

    fig.add_annotation(
        x=adjusted_fraction + horizontal_offset,
        y=applied_kelly_y,
        text="Applied Kelly",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-vertical_spacing,
        font={"color": "blue", "size": 12},
        arrowcolor="blue"
    )

    # Layout polish
    fig.update_layout(
        title={
            "text": "Growth vs. Capital Allocation",
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.90,
            "font": {"size": 18}
        },
        xaxis_title="Fraction of Capital Allocated",
        yaxis_title="Expected Return Proxy",
        template="simple_white",
        height=460,
        margin={"l": 40, "r": 40, "t": 80, "b": 60},
        showlegend=False
    )

    st.plotly_chart(fig, width='stretch')

    st.caption(
        "📉 This chart visualises expected growth relative to capital allocation under a given "
        "risk–reward profile. The curve reflects theoretical return potential across different "
        "sizing fractions. Markers highlight both the raw Kelly fraction "
        "(optimal theoretical sizing) and the applied fraction (user-adjusted sizing), offering "
        "a visual guide to trade-off dynamics."
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
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
No trading, investment, or policy advice provided.")
