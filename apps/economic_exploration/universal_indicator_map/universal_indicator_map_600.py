# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Universal Indicator Signal Functions — System Core Logic
-----------------------------------------------------------

This module defines the universal signal-generation functions for the
Economic Exploration suite.
It governs baseline indicator evaluation across all thematic groupings
(themes 100–2100+).

✅ System Role:
- Forms the core signal processing logic across all countries and themes
- Enables insight generation, macro alignment scoring, and AI persona compatibility
- Supports real-time macro summaries, AI export pipelines, and structured DSS workflows

🧠 AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Accelerating", "Stable", "Decelerating", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- No numeric payloads are returned; outputs are pure interpretive classifications

---------------------------------------------------------------
⚙️ System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

1️⃣ **Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

2️⃣ **String-Based Return Values**
- Every function must return a string output suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example return values: `"Uptrend Confirmed"`, `"Mixed Signals"`, `"Flat"`,
`"Insufficient Data"`

3️⃣ **Pure Logic (No Side Effects)**
- No functions may reference hardcoded external data, models, or manual overrides.
- Outputs must derive entirely from the provided dataframe inputs.

4️⃣ **No Numeric Secondary Payloads**
- Signal outputs are always returned as **single strings only**.
- No tuples, numeric scores, or dynamic secondary values are allowed.

5️⃣ **Dispatcher Independence**
- Signal routing and evaluation orchestration is handled externally via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- Do not embed custom routing logic within signal functions.
- Signal functions must never embed sector names, entity labels, or dynamic entity references
directly into their return strings. All entity-specific content is handled downstream
during insight generation.

🧭 Governance Note:
- Universal signal modules form system-wide stable infrastructure.
- User extensions, overrides, or country-specific adaptations occur only within local
`indicator_map_XXX.py` files.

"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Housing Construction Cycle Indicator Logic
# -------------------------------------------------------------------------------------------------
def forward_development_intent_signal(df, period=12):
    """
    Evaluates housing authorizations relative to the recent average.

    Returns:
        str: Forward development intent signal.
    """
    if df is None or "Housing Units Authorized" not in df.columns:
        return "Insufficient Data"

    series = df["Housing Units Authorized"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Approvals Expanding"
    if latest < avg_recent * 0.98:
        return "Approvals Softening"
    return "Approvals Stabilising"


def construction_conversion_flow_signal(df, period=12):
    """
    Evaluates housing starts relative to the recent average.

    Returns:
        str: Construction conversion signal.
    """
    if df is None or "Housing Units Started" not in df.columns:
        return "Insufficient Data"

    series = df["Housing Units Started"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Starts Accelerating"
    if latest < avg_recent * 0.98:
        return "Starts Slowing"
    return "Starts Stabilising"


def supply_delivery_progress_signal(df, period=12):
    """
    Evaluates housing completions relative to the recent average.

    Returns:
        str: Supply delivery signal.
    """
    if df is None or "Housing Units Completed" not in df.columns:
        return "Insufficient Data"

    series = df["Housing Units Completed"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Completions Rising"
    if latest < avg_recent * 0.98:
        return "Completions Falling"
    return "Completions Stable"


options_housing_cycle_map = {
    "Forward Development Intent": forward_development_intent_signal,
    "Construction Conversion Flow": construction_conversion_flow_signal,
    "Supply Delivery Progress": supply_delivery_progress_signal
}


# -------------------------------------------------------------------------------------------------
# Mortgage Financing Conditions Indicator Logic
# -------------------------------------------------------------------------------------------------
def mortgage_borrowing_cost_signal(df, period=12):
    """
    Evaluates 30-year mortgage rates relative to the recent average.

    Returns:
        str: Mortgage borrowing cost signal.
    """
    if df is None or "30-Year Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["30-Year Mortgage Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Borrowing Costs Rising"
    if latest < avg_recent * 0.98:
        return "Borrowing Costs Easing"
    return "Borrowing Costs Stable"


def housing_affordability_pressure_signal(df, period=12):
    """
    Evaluates mortgage rate pressure as a proxy for affordability conditions.

    Returns:
        str: Housing affordability pressure signal.
    """
    if df is None or "30-Year Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["30-Year Mortgage Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Affordability Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Affordability Pressure Easing"
    return "Affordability Pressure Stable"


def financing_condition_shift_signal(df, period=12):
    """
    Evaluates whether mortgage financing conditions are tightening or easing.

    Returns:
        str: Financing condition shift signal.
    """
    if df is None or "30-Year Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["30-Year Mortgage Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Financing Tightening"
    if latest < avg_recent * 0.98:
        return "Financing Easing"
    return "Financing Stable"


options_mortgage_financing_map = {
    "Mortgage Borrowing Cost": mortgage_borrowing_cost_signal,
    "Housing Affordability Pressure": housing_affordability_pressure_signal,
    "Financing Condition Shift": financing_condition_shift_signal
}


# -------------------------------------------------------------------------------------------------
# Yield Curve Structure Indicator Logic
# -------------------------------------------------------------------------------------------------
def curve_slope_positioning_signal(df, period=12):
    """
    Evaluates the latest yield curve spread relative to the recent average.

    Returns:
        str: Curve slope positioning signal.
    """
    if df is None or "Yield Curve Spread" not in df.columns:
        return "Insufficient Data"

    series = df["Yield Curve Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Curve Steepening"
    if latest < avg_recent * 0.98:
        return "Curve Flattening"
    return "Curve Stable"


def macro_expectation_shift_signal(df, period=12):
    """
    Evaluates the yield curve spread as a signal of changing macro expectations.

    Returns:
        str: Macro expectation shift signal.
    """
    if df is None or "Yield Curve Spread" not in df.columns:
        return "Insufficient Data"

    series = df["Yield Curve Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Macro Expectations Improving"
    if latest < avg_recent * 0.98:
        return "Macro Expectations Weakening"
    return "Macro Expectations Stable"


def liquidity_regime_signal(df, period=12):
    """
    Evaluates the yield curve spread as a broad liquidity regime signal.

    Returns:
        str: Liquidity regime signal.
    """
    if df is None or "Yield Curve Spread" not in df.columns:
        return "Insufficient Data"

    series = df["Yield Curve Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Liquidity Conditions Easing"
    if latest < avg_recent * 0.98:
        return "Liquidity Conditions Tightening"
    return "Liquidity Conditions Stable"


options_yield_curve_structure_map = {
    "Curve Slope Positioning": curve_slope_positioning_signal,
    "Macro Expectation Shift": macro_expectation_shift_signal,
    "Liquidity Regime Signal": liquidity_regime_signal
}
