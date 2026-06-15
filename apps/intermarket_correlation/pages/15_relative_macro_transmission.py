# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Relative Macro Transmission
---------------------------

Comparative transmission engine for curated macro and market series.

Use cases:
- Custom Comparison
- Relative Wealth
- Interest Rate Differential & Carry
- External Balance & Capital Flow
- Commodity & FX Transmission
- Sovereign vs Equity Divergence
- Positioning & Market Structure

Outputs:
- Transmission Conditions Summary (DSS-light)
- Standardised Overlay
- Derived Metric Chart
- Rolling Transmission Panel
- Structural Summary Table

This module is intentionally use-case-led, with a generic comparison engine underneath.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup (Canonical)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities (Canonical)
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# Resolve Named Paths
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_relative_macro_transmission.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_relative_macro_transmission.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Engine & Registry Imports
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "registry"))
sys.path.append(os.path.join(APPS_PATH, "economic_exploration", "correlation_engine"))
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

from relative_transmission_data_loader import (  # pylint: disable=import-error
    build_relative_series_pool,
    load_relative_pair,
)
from relative_transmission_engine import compute_transmission  # pylint: disable=import-error
from relative_transmission_summary import build_summary_table  # pylint: disable=import-error
from relative_transmission_visualisation import (  # pylint: disable=import-error
    render_overlay,
    render_derived_metric,
    render_rolling_panel,
)
from relative_transmission_interpretation import (  # pylint: disable=import-error
    build_contextual_insight,
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools — Sidebar + Observation Panel Integration
# -------------------------------------------------------------------------------------------------
from render_macro_interaction_tools_panel_relative_macro_transmission import render_macro_interaction_tools_panel
from macro_insight_sidebar_panel_relative_macro_transmission import render_macro_sidebar_tools

from observation_handler_relative_macro_transmission import (
    observation_input_form,
    display_observation_log
)

# -------------------------------------------------------------------------------------------------
# AI Export Tools — Relative Macro Transmission
# -------------------------------------------------------------------------------------------------
from ai_export_ui_panel_relative_macro_transmission import render_ai_export_panel
from ai_export_builder_relative_macro_transmission import (
    build_macro_insight_snapshot_relative_macro_transmission
)

# -------------------------------------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Relative Macro Transmission", layout="wide")
st.title("Relative Macro Transmission")
st.caption(
    "*Analyse cross-system differentials, spread dynamics, and transmission states "
    "between curated macro and market series.*"
)

with st.expander("ℹ️ About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="Intermarket & Correlation Dashboard")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------------------------
comparison_modes = [
    "Macro vs Macro",
    "Macro vs Market",
    "Market vs Market",
]

transform_options = {
    "Difference": "difference",
    "Ratio": "ratio",
    "Relative %": "relative_pct",
    "Relative Z-Score": "zscore_spread",
    "Rolling Correlation": "rolling_corr",
}

window_options = [12, 24, 36, 60]

RMT_USE_CASE_SURFACE_MAP = {
    "Relative Wealth": {
        "left": ["equity_surface"],
        "right": ["fx_pair"],
    },
    "Interest Rate Differential & Carry": {
        "left": ["carry_rate"],
        "right": ["carry_rate", "sovereign_yield"],
    },
    "External Balance & Capital Flow": {
        "left": ["external_balance"],
        "right": ["external_balance"],
    },
    "Commodity & FX Transmission": {
        "left": ["commodity_surface"],
        "right": ["fx_pair", "equity_surface"],
    },
    "Sovereign vs Equity Divergence": {
        "left": ["sovereign_yield"],
        "right": ["equity_surface"],
    },
    "Positioning & Market Structure": {
        "left": ["equity_surface", "fx_pair", "sovereign_yield", "market_structure"],
        "right": ["equity_surface", "fx_pair", "sovereign_yield", "market_structure"],
    },
}

USE_CASE_CONFIG = {
    "Custom Comparison": {
        "comparison_mode": None,
        "default_transform": "difference",
        "default_window": 24,
        "description": "Flexible comparison surface for any two eligible macro or market series.",
        "schema": "custom",
    },
    "Relative Wealth": {
        "comparison_mode": "Market vs Market",
        "default_transform": "relative_pct",
        "default_window": 24,
        "description": (
            "Derive an anchor-currency wealth surface using a country equity proxy or broad market "
            "surface and a selected anchor FX pair."
        ),
        "schema": "relative_wealth",
    },
    "Interest Rate Differential & Carry": {
        "comparison_mode": "Market vs Market",
        "default_transform": "difference",
        "default_window": 24,
        "description": (
            "Compare short-end rate differentials across systems."
        ),
        "schema": "rate_differential",
    },
    "External Balance & Capital Flow": {
        "comparison_mode": "Macro vs Macro",
        "default_transform": "difference",
        "default_window": 24,
        "description": (
            "Compare external balance, trade flow, reserve, and capital flow conditions across systems."
        ),
        "schema": "external_balance",
    },
    "Commodity & FX Transmission": {
        "comparison_mode": "Market vs Market",
        "default_transform": "rolling_corr",
        "default_window": 24,
        "description": (
            "Assess whether commodity benchmarks and FX-linked market surfaces are diverging, "
            "aligning, or re-coupling."
        ),
        "schema": "commodity_fx",
    },
    "Sovereign vs Equity Divergence": {
        "comparison_mode": "Market vs Market",
        "default_transform": "zscore_spread",
        "default_window": 24,
        "description": (
            "Compare sovereign pricing against equity wealth surfaces to assess divergence in domestic conditions."
        ),
        "schema": "sovereign_equity",
    },
    "Positioning & Market Structure": {
        "comparison_mode": "Market vs Market",
        "default_transform": "zscore_spread",
        "default_window": 24,
        "description": (
            "Assess spread behaviour, concentration, crowding, and market structure transition states."
        ),
        "schema": "positioning_market_structure",
    },
}

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _sort_pool(pool):
    """
    Sort + remove duplicate labels for cleaner RMT selectors.

    Important:
    RMT should only show unique user-facing entries.
    Duplicate labels exist because the same underlying datasource
    is used across multiple thematic groupings for DSS / TC routing.

    For Relative Macro Transmission, duplicates reduce usability
    and create poor production workflow, so we collapse to unique labels.
    """
    seen = set()
    unique_pool = []

    for item in sorted(pool, key=lambda x: x["label"]):
        label = item.get("label")

        if not label:
            continue

        if label in seen:
            continue

        seen.add(label)
        unique_pool.append(item)

    return unique_pool


def _default_index(options, preferred_value):
    try:
        return options.index(preferred_value)
    except ValueError:
        return 0


def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return np.nan


def _filter_pool_by_mode(pool, comparison_mode):
    """
    High-level mode filter.
    Only used for Custom Comparison.
    """
    if comparison_mode == "Macro vs Macro":
        return [x for x in pool if x.get("series_type") == "macro"]

    if comparison_mode == "Macro vs Market":
        return [x for x in pool if x.get("series_type") in ["macro", "market"]]

    if comparison_mode == "Market vs Market":
        return [x for x in pool if x.get("series_type") == "market"]

    return pool


def _filter_by_series_type(pool, wanted_type):
    if wanted_type is None:
        return pool
    return [x for x in pool if x.get("series_type") == wanted_type]


def _build_label_map(pool):
    return {x["label"]: x for x in pool}


# -------------------------------------------------------------------------------------------------
# Helpers — Use Case Filtering
# -------------------------------------------------------------------------------------------------
def _classify_surface_type(item):
    """
    Prefer explicit registry classification where available.
    Fall back to label-based classification so the module still works cleanly now.
    """
    explicit_surface = item.get("rmt_surface_type")
    if explicit_surface:
        return explicit_surface

    label = item.get("label", "")

    fx_markers = [
        "Pair",
        "Dollar Strength Benchmark",
        "Euro Sterling Pair",
        "Euro Yen Pair",
        "Australian Dollar Yen Pair",
    ]
    if any(marker in label for marker in fx_markers):
        return "fx_pair"

    equity_markers = [
        "Country Equity Proxy",
        "Broad Equity Index",
        "Blue Chip Equity Index",
        "Growth Oriented Index",
        "Small Cap Equity Index",
        "Global Equity Index",
    ]
    if any(marker in label for marker in equity_markers):
        return "equity_surface"

    commodity_markers = [
        "Brent Oil",
        "Crude Oil",
        "Gold",
        "Silver",
        "Platinum",
        "Copper",
        "Natural Gas",
        "US Coffee",
        "US Wheat",
    ]
    if any(marker in label for marker in commodity_markers):
        return "commodity_surface"

    external_markers = [
        "Exports",
        "Imports",
        "Trade Balance",
        "Current Account",
        "Foreign Exchange Reserves",
        "Official Reserves Excluding Gold",
        "Reserves",
        "Net International Investment Position",
        "Balance of Payments",
    ]
    if any(marker in label for marker in external_markers):
        return "external_balance"

    if "Sovereign Yield" in label:
        return "sovereign_yield"

    carry_markers = [
        "Central Bank Funds Rate",
        "Policy Rate",
        "Cash Rate",
        "Overnight Rate",
        "Interbank Rate",
        "Short-Term Rate",
        "Short Term Rate",
        "Money Market Rate",
        "Reference Rate",
        "Funding Rate",
    ]
    if any(marker in label for marker in carry_markers):
        return "carry_rate"

    if "Sector" in label or "Market Volatility Index" in label:
        return "market_structure"

    return None


def _filter_pool_by_surface(pool, allowed_surface_types):
    return [
        x for x in pool
        if _classify_surface_type(x) in allowed_surface_types
    ]


# -------------------------------------------------------------------------------------------------
# Build Relative Wealth Pair
# -------------------------------------------------------------------------------------------------
def _build_relative_wealth_pair_df(equity_obj, fx_obj, project_path):
    """
    Build derived relative wealth dataframe:
    wealth_series = equity_series * fx_series

    Returns:
        pair_df          : dataframe used by generic compute engine
        overlay_df       : underlying equity + fx series for visual overlay
        derived_series   : wealth series for display/context
        messages         : load status messages
    """
    equity_df, equity_messages = load_relative_pair(
        series_a_obj=equity_obj,
        series_b_obj=equity_obj,
        project_path=project_path,
    )

    fx_df, fx_messages = load_relative_pair(
        series_a_obj=fx_obj,
        series_b_obj=fx_obj,
        project_path=project_path,
    )

    messages = []
    messages.extend(equity_messages)
    messages.extend(fx_messages)

    if equity_df.empty or fx_df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.Series(dtype=float), messages

    equity_series = equity_df.iloc[:, 0].copy()
    fx_series = fx_df.iloc[:, 0].copy()

    overlay_df = pd.concat([equity_series, fx_series], axis=1, join="inner").dropna()

    if overlay_df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.Series(dtype=float), messages

    equity_series = overlay_df.iloc[:, 0]
    fx_series = overlay_df.iloc[:, 1]

    wealth_series = (equity_series * fx_series).dropna()
    wealth_series.name = f"{equity_obj['country']} — Relative Wealth Surface"

    pair_df = pd.concat([wealth_series, equity_series], axis=1, join="inner").dropna()

    return pair_df, overlay_df, wealth_series, messages


# -------------------------------------------------------------------------------------------------
# Build Full Pool
# -------------------------------------------------------------------------------------------------
full_pool = _sort_pool(build_relative_series_pool())

if not full_pool:
    st.warning("No eligible series found for Relative Macro Transmission.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Sidebar — Use Case First
# -------------------------------------------------------------------------------------------------
use_case = st.sidebar.selectbox(
    "Select Use Case:",
    list(USE_CASE_CONFIG.keys())
)

config = USE_CASE_CONFIG[use_case]

with st.sidebar.expander("ℹ️ Use Case Notes", expanded=True):
    st.markdown(config["description"])

manual_override = st.sidebar.checkbox(
    "Override transform and window defaults",
    value=(use_case == "Custom Comparison"),
    help="Use case presets apply recommended transformation and rolling window. "
         "Enable override to adjust them manually."
)

# -------------------------------------------------------------------------------------------------
# Comparison Mode
# -------------------------------------------------------------------------------------------------
if use_case == "Custom Comparison":
    comparison_mode = st.sidebar.selectbox(
        "Select Comparison Mode:",
        comparison_modes,
        index=0
    )
    mode_filtered_pool = _filter_pool_by_mode(full_pool, comparison_mode)
else:
    comparison_mode = config["comparison_mode"]
    mode_filtered_pool = _filter_pool_by_mode(full_pool, comparison_mode)
    st.sidebar.markdown(f"**Comparison Mode:** {comparison_mode}")

if not mode_filtered_pool:
    st.warning("No eligible series found for the selected comparison mode.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Input Schema by Use Case
# -------------------------------------------------------------------------------------------------
series_a_obj = None
series_b_obj = None
anchor_pair_obj = None
custom_overlay_df = None
derived_series_override = None

if config["schema"] == "relative_wealth":
    schema = RMT_USE_CASE_SURFACE_MAP["Relative Wealth"]

    equity_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
    fx_pool = _sort_pool(_filter_pool_by_surface(full_pool, schema["right"]))

    if not fx_pool or not equity_pool:
        st.warning("No eligible FX pairs or equity surfaces available for Relative Wealth.")
        st.stop()

    fx_labels = [x["label"] for x in fx_pool]
    equity_labels = [x["label"] for x in equity_pool]

    anchor_pair_label = st.sidebar.selectbox("Select Anchor FX Pair:", fx_labels)
    equity_surface_label = st.sidebar.selectbox("Select Country Equity Surface:", equity_labels)

    fx_map = _build_label_map(fx_pool)
    equity_map = _build_label_map(equity_pool)

    anchor_pair_obj = fx_map[anchor_pair_label]
    series_a_obj = equity_map[equity_surface_label]

else:
    if config["schema"] == "custom":
        if comparison_mode == "Macro vs Macro":
            series_a_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "macro"))
            series_b_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "macro"))
            primary_label = "Select Primary Series:"
            comparison_label = "Select Comparison Series:"
        elif comparison_mode == "Macro vs Market":
            series_a_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "macro"))
            series_b_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "market"))
            primary_label = "Select Primary Series:"
            comparison_label = "Select Comparison Series:"
        else:
            series_a_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "market"))
            series_b_pool = _sort_pool(_filter_by_series_type(mode_filtered_pool, "market"))
            primary_label = "Select Primary Series:"
            comparison_label = "Select Comparison Series:"

    elif config["schema"] == "rate_differential":
        schema = RMT_USE_CASE_SURFACE_MAP["Interest Rate Differential & Carry"]
        series_a_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
        series_b_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["right"]))
        primary_label = "Select Primary Carry Rate Surface:"
        comparison_label = "Select Comparison Carry Rate Surface:"

    elif config["schema"] == "external_balance":
        schema = RMT_USE_CASE_SURFACE_MAP["External Balance & Capital Flow"]
        series_a_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
        series_b_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["right"]))
        primary_label = "Select Primary External Surface:"
        comparison_label = "Select Comparison External Surface:"

    elif config["schema"] == "commodity_fx":
        schema = RMT_USE_CASE_SURFACE_MAP["Commodity & FX Transmission"]
        series_a_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
        series_b_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["right"]))
        primary_label = "Select Primary Commodity Surface:"
        comparison_label = "Select Comparison FX or Market Surface:"

    elif config["schema"] == "sovereign_equity":
        schema = RMT_USE_CASE_SURFACE_MAP["Sovereign vs Equity Divergence"]
        series_a_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
        series_b_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["right"]))
        primary_label = "Select Primary Sovereign Surface:"
        comparison_label = "Select Comparison Equity Surface:"

    elif config["schema"] == "positioning_market_structure":
        schema = RMT_USE_CASE_SURFACE_MAP["Positioning & Market Structure"]
        series_a_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["left"]))
        series_b_pool = _sort_pool(_filter_pool_by_surface(mode_filtered_pool, schema["right"]))
        primary_label = "Select Primary Market Structure Surface:"
        comparison_label = "Select Comparison Surface:"

    else:
        st.warning("Unsupported input schema.")
        st.stop()

    if not series_a_pool or not series_b_pool:
        st.warning("No eligible series available for the selected use case.")
        st.stop()

    series_a_labels = [x["label"] for x in series_a_pool]
    series_b_labels = [x["label"] for x in series_b_pool]

    series_a_label = st.sidebar.selectbox(primary_label, series_a_labels)

    series_b_candidates = [label for label in series_b_labels if label != series_a_label]
    if not series_b_candidates:
        st.warning("No valid comparison series available once the primary selection is applied.")
        st.stop()

    series_b_label = st.sidebar.selectbox(comparison_label, series_b_candidates)

    series_a_map = _build_label_map(series_a_pool)
    series_b_map = _build_label_map(series_b_pool)

    series_a_obj = series_a_map[series_a_label]
    series_b_obj = series_b_map[series_b_label]

# -------------------------------------------------------------------------------------------------
# Transformation + Window
# -------------------------------------------------------------------------------------------------
reverse_transform_lookup = {v: k for k, v in transform_options.items()}
transform_keys = list(transform_options.keys())

if use_case == "Custom Comparison" or manual_override:
    transform_label = st.sidebar.selectbox(
        "Select Transformation:",
        transform_keys,
        index=_default_index(
            transform_keys,
            reverse_transform_lookup.get(config["default_transform"], "Difference")
        )
    )
    transformation = transform_options[transform_label]

    window = st.sidebar.selectbox(
        "Select Rolling Window:",
        window_options,
        index=_default_index(window_options, config["default_window"])
    )
else:
    transformation = config["default_transform"]
    window = config["default_window"]
    st.sidebar.markdown(
        f"**Transformation:** {reverse_transform_lookup.get(transformation, transformation)}"
    )
    st.sidebar.markdown(f"**Rolling Window:** {window}")

with st.sidebar.expander("ℹ️ Transmission Notes"):
    st.markdown("""
**Difference**
Best for spread analysis, rate differentials, and divergence monitoring.

**Ratio**
Best for relative scale comparisons and structural proportionality.

**Relative %**
Best for outperformance and benchmark-relative comparisons.

**Relative Z-Score**
Best for regime framing and historical standardisation.

**Rolling Correlation**
Best for identifying decoupling, re-coupling, and transmission shifts.
""")

# -------------------------------------------------------------------------------------------------
# Load / Build Pair
# -------------------------------------------------------------------------------------------------
if config["schema"] == "relative_wealth":
    pair_df, custom_overlay_df, derived_series_override, messages = _build_relative_wealth_pair_df(
        equity_obj=series_a_obj,
        fx_obj=anchor_pair_obj,
        project_path=PROJECT_PATH
    )
else:
    pair_df, messages = load_relative_pair(
        series_a_obj=series_a_obj,
        series_b_obj=series_b_obj,
        project_path=PROJECT_PATH
    )

for msg in messages:
    st.warning(msg)

if pair_df.empty:
    st.warning("No data available for the selected comparison.")
    st.stop()

if len(pair_df) < max(window, 12):
    st.warning("Insufficient overlapping history for the selected window.")
    st.stop()

# -------------------------------------------------------------------------------------------------
# Compute Transmission Result
# -------------------------------------------------------------------------------------------------
result = compute_transmission(
    pair_df=pair_df,
    transformation=transformation,
    window=window
)

if config["schema"] == "relative_wealth" and custom_overlay_df is not None and not custom_overlay_df.empty:
    result["overlay_df"] = custom_overlay_df.copy()

if config["schema"] == "relative_wealth" and derived_series_override is not None and not derived_series_override.empty:
    result["derived_df"] = derived_series_override.to_frame(name="derived_metric")

# -------------------------------------------------------------------------------------------------
# Observation Context Scaffold
# -------------------------------------------------------------------------------------------------
observation_context = {
    "module": "Relative Macro Transmission",
    "use_case": use_case,
    "comparison_mode": comparison_mode,
    "primary": series_a_obj["label"] if series_a_obj else None,
    "comparison": series_b_obj["label"] if series_b_obj else None,
    "anchor_pair": anchor_pair_obj["label"] if anchor_pair_obj else None,
    "transformation": reverse_transform_lookup.get(transformation, transformation),
    "window": window,
    "state": result.get("regime_label"),
    "rolling_state": result.get("rolling_state"),
    "percentile": result.get("percentile"),
}

summary_df = build_summary_table(result)
contextual_insight = build_contextual_insight(use_case, result, observation_context)

# -------------------------------------------------------------------------------------------------
# Transmission Conditions Summary (DSS-Light)
# -------------------------------------------------------------------------------------------------

st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        padding: 0.2rem 0.2rem 0.2rem 0.2rem;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Transmission Conditions Summary")

metric_label = "Current Correlation" if transformation == "rolling_corr" else "Current Differential"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Regime State", result["regime_label"])

with col2:
    st.metric(
        metric_label,
        (
            f"{result['current_value']:.3f}"
            if pd.notna(result["current_value"])
            else "N/A"
        )
    )

with col3:
    st.metric(
        "Percentile",
        (
            f"{result['percentile']:.0f}th pct"
            if pd.notna(result["percentile"])
            else "N/A"
        )
    )

with col4:
    st.metric("Rolling State", result["rolling_state"])

st.markdown("### Structural Interpretation")
st.write(contextual_insight)

with st.expander("Comparison Context"):
    if config["schema"] == "relative_wealth":
        st.markdown(f"**Anchor FX Pair:** {anchor_pair_obj['label']}")
        st.markdown(f"**Country Equity Surface:** {series_a_obj['label']}")
    else:
        st.markdown(f"**Primary:** {series_a_obj['label']}")
        st.markdown(f"**Comparison:** {series_b_obj['label']}")

    st.markdown(
        f"**Transformation:** {reverse_transform_lookup.get(transformation, transformation)}"
    )
    st.markdown(f"**Rolling Window:** {window}")

st.divider()

# -------------------------------------------------------------------------------------------------
# Main Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Standardised Overlay",
    "Derived Metric",
    "Rolling Transmission",
    "Structural Summary",
    "ℹ️ Help",
])

with tabs[0]:
    render_overlay(result["overlay_df"])

with tabs[1]:
    render_derived_metric(result["derived_df"])

with tabs[2]:
    render_rolling_panel(result["rolling_df"])

with tabs[3]:
    st.dataframe(summary_df, width="stretch", hide_index=True)

    with st.expander("Observation Context Scaffold"):
        st.json(observation_context)

with tabs[4]:
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.info("Help file not found.")

st.divider()

# -------------------------------------------------------------------------------------------------
# Macro Interaction Setup
# -------------------------------------------------------------------------------------------------
theme_code = "relative_macro_transmission"
theme_title = "Relative Macro Transmission"

# -------------------------------------------------------------------------------------------------
# Build Snapshot Insight
# -------------------------------------------------------------------------------------------------
rmt_snapshot_insight = build_macro_insight_snapshot_relative_macro_transmission(
    theme_code=theme_code,
    theme_title=theme_title,
    use_case=use_case,
    series_a_obj=series_a_obj,
    series_b_obj=series_b_obj,
    anchor_pair_obj=anchor_pair_obj,
    comparison_mode=comparison_mode,
    transformation=reverse_transform_lookup.get(transformation, transformation),
    window=window,
    result=result,
    contextual_insight=contextual_insight
)

# -------------------------------------------------------------------------------------------------
# Sidebar Activation Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_ai_export, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code
)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Tools
# -------------------------------------------------------------------------------------------------
if show_observation or show_log:
    st.markdown("## Macro Interaction Tools")

selected_indicators = []

if series_a_obj:
    selected_indicators.append(series_a_obj["label"])

if series_b_obj:
    selected_indicators.append(series_b_obj["label"])

if anchor_pair_obj:
    selected_indicators.append(anchor_pair_obj["label"])

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    panel_title=theme_title,
    selected_themes=[theme_code],
    selected_indicators=selected_indicators,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

# -------------------------------------------------------------------------------------------------
# AI Export Panel — Relative Macro Transmission
# -------------------------------------------------------------------------------------------------
if show_ai_export:
    render_ai_export_panel(
        snapshot_results=rmt_snapshot_insight,
        base_asset=use_case,
        asset_type_display=theme_title
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
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
    "No trading, investment, or policy advice provided."
)
