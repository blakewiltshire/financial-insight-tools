# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
#  Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Indicator Signal Functions — System Core Logic
-----------------------------------------------------------

This module defines the universal signal-generation functions for the
Economic Exploration suite.
It governs baseline indicator evaluation across all thematic groupings
(themes 100–2100+).

System Role:
- Forms the core signal processing logic across all countries and themes
- Enables insight generation, macro alignment scoring, and AI persona compatibility
- Supports real-time macro summaries, AI export pipelines, and structured DSS workflows

AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Accelerating", "Stable", "Decelerating", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- No numeric payloads are returned; outputs are pure interpretive classifications

---------------------------------------------------------------
System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

**Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

**String-Based Return Values**
- Every function must return a string output suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example return values: `"Uptrend Confirmed"`, `"Mixed Signals"`, `"Flat"`,
`"Insufficient Data"`

**Pure Logic (No Side Effects)**
- No functions may reference hardcoded external data, models, or manual overrides.
- Outputs must derive entirely from the provided dataframe inputs.

**No Numeric Secondary Payloads**
- Signal outputs are always returned as **single strings only**.
- No tuples, numeric scores, or dynamic secondary values are allowed.

**Dispatcher Independence**
- Signal routing and evaluation orchestration is handled externally via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- Do not embed custom routing logic within signal functions.
- Signal functions must never embed sector names, entity labels, or dynamic entity references
directly into their return strings. All entity-specific content is handled downstream
during insight generation.

Governance Note:
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
    Evaluates Long-Term Mortgage Rates relative to the recent average.

    Returns:
        str: Mortgage borrowing cost signal.
    """
    if df is None or "Long-Term Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Long-Term Mortgage Rate"].dropna()
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
    if df is None or "Long-Term Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Long-Term Mortgage Rate"].dropna()
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
    if df is None or "Long-Term Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Long-Term Mortgage Rate"].dropna()
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

# -------------------------------------------------------------------------------------------------
# Sovereign Debt Sustainability Indicator Logic
# -------------------------------------------------------------------------------------------------
def government_debt_burden_signal(df, period=12):
    """
    Evaluates sovereign debt-to-GDP burden relative to the recent average.

    Returns:
        str: Government debt burden signal.
    """
    if df is None or "Sovereign Debt Percentage of GDP" not in df.columns:
        return "Insufficient Data"

    series = df["Sovereign Debt Percentage of GDP"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Debt Burden Rising"
    if latest < avg_recent * 0.98:
        return "Debt Burden Easing"
    return "Debt Burden Stable"


def fiscal_balance_pressure_signal(df, period=12):
    """
    Evaluates fiscal balance pressure relative to the recent average.

    Returns:
        str: Fiscal balance pressure signal.
    """
    if df is None or "Government Fiscal Balance" not in df.columns:
        return "Insufficient Data"

    series = df["Government Fiscal Balance"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest < avg_recent * 0.98:
        return "Fiscal Pressure Rising"
    if latest > avg_recent * 1.02:
        return "Fiscal Pressure Easing"
    return "Fiscal Pressure Stable"


def interest_burden_on_output_signal(df, period=12):
    """
    Evaluates government interest outlays relative to the recent average.

    Returns:
        str: Interest burden on output signal.
    """
    if df is None or "Government Interest Outlays" not in df.columns:
        return "Insufficient Data"

    series = df["Government Interest Outlays"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Interest Burden Rising"
    if latest < avg_recent * 0.98:
        return "Interest Burden Easing"
    return "Interest Burden Stable"


options_sovereign_debt_sustainability_map = {
    "Government Debt Burden": government_debt_burden_signal,
    "Fiscal Balance Pressure": fiscal_balance_pressure_signal,
    "Interest Burden on Output": interest_burden_on_output_signal
}


# -------------------------------------------------------------------------------------------------
# Sovereign Liquidity and Refinancing Pressure Indicator Logic
# -------------------------------------------------------------------------------------------------
def sovereign_yield_pressure_signal(df, period=12):
    """
    Evaluates sovereign benchmark yield pressure relative to the recent average.

    Returns:
        str: Sovereign yield pressure signal.
    """
    if df is None or "10-Year Sovereign Yield" not in df.columns:
        return "Insufficient Data"

    series = df["10-Year Sovereign Yield"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Yield Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Yield Pressure Easing"
    return "Yield Pressure Stable"


def interest_servicing_pressure_signal(df, period=12):
    """
    Evaluates sovereign interest servicing pressure relative to the recent average.

    Returns:
        str: Interest servicing pressure signal.
    """
    if df is None or "Government Interest Outlays" not in df.columns:
        return "Insufficient Data"

    series = df["Government Interest Outlays"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Servicing Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Servicing Pressure Easing"
    return "Servicing Pressure Stable"


def liquidity_cover_conditions_signal(df, period=12):
    """
    Evaluates sovereign liquidity cover conditions using government receipts.

    Returns:
        str: Liquidity cover conditions signal.
    """
    if df is None or "Government Receipts" not in df.columns:
        return "Insufficient Data"

    series = df["Government Receipts"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest < avg_recent * 0.98:
        return "Liquidity Cover Weakening"
    if latest > avg_recent * 1.02:
        return "Liquidity Cover Improving"
    return "Liquidity Cover Stable"


options_sovereign_liquidity_refinancing_map = {
    "Sovereign Yield Pressure": sovereign_yield_pressure_signal,
    "Interest Servicing Pressure": interest_servicing_pressure_signal,
    "Liquidity Cover Conditions": liquidity_cover_conditions_signal
}


# -------------------------------------------------------------------------------------------------
# Balance Sheet Expansion and System Constraint Indicator Logic
# -------------------------------------------------------------------------------------------------
def public_debt_expansion_signal(df, period=12):
    """
    Evaluates sovereign debt burden relative to the recent average.

    Returns:
        str: Public debt expansion signal.
    """
    if df is None or "Sovereign Debt Percentage of GDP" not in df.columns:
        return "Insufficient Data"

    series = df["Sovereign Debt Percentage of GDP"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Debt Expansion Rising"
    if latest < avg_recent * 0.98:
        return "Debt Expansion Easing"
    return "Debt Expansion Stable"


def central_bank_balance_sheet_expansion_signal(df, period=12):
    """
    Evaluates central bank balance sheet expansion relative to the recent average.

    Returns:
        str: Central bank balance sheet expansion signal.
    """
    if df is None or "Central Bank Total Assets" not in df.columns:
        return "Insufficient Data"

    series = df["Central Bank Total Assets"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Balance Sheet Expanding"
    if latest < avg_recent * 0.98:
        return "Balance Sheet Contracting"
    return "Balance Sheet Stable"


def system_financing_constraint_signal(df, period=12):
    """
    Evaluates sovereign financing conditions using benchmark yields.

    Returns:
        str: System financing constraint signal.
    """
    if df is None or "10-Year Sovereign Yield" not in df.columns:
        return "Insufficient Data"

    series = df["10-Year Sovereign Yield"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Financing Constraint Tightening"
    if latest < avg_recent * 0.98:
        return "Financing Constraint Easing"
    return "Financing Constraint Stable"


options_balance_sheet_expansion_constraint_map = {
    "Public Debt Expansion": public_debt_expansion_signal,
    "Central Bank Balance Sheet Expansion": central_bank_balance_sheet_expansion_signal,
    "System Financing Constraint": system_financing_constraint_signal
}


# -------------------------------------------------------------------------------------------------
# Credit Conditions and Financing Pressure Indicator Logic
# -------------------------------------------------------------------------------------------------
def investment_grade_spread_pressure_signal(df, period=12):
    """
    Evaluates investment grade spread pressure relative to the recent average.

    Returns:
        str: Investment grade spread pressure signal.
    """
    if df is None or "Corporate Credit Spread" not in df.columns:
        return "Insufficient Data"

    series = df["Corporate Credit Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Investment Grade Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Investment Grade Pressure Easing"
    return "Investment Grade Pressure Stable"


def high_yield_spread_pressure_signal(df, period=12):
    """
    Evaluates high yield spread pressure relative to the recent average.

    Returns:
        str: High yield spread pressure signal.
    """
    if df is None or "High Yield Credit Spread" not in df.columns:
        return "Insufficient Data"

    series = df["High Yield Credit Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "High Yield Pressure Rising"
    if latest < avg_recent * 0.98:
        return "High Yield Pressure Easing"
    return "High Yield Pressure Stable"


def distressed_credit_pressure_signal(df, period=12):
    """
    Evaluates distressed credit spread pressure relative to the recent average.

    Returns:
        str: Distressed credit pressure signal.
    """
    if df is None or "CCC and Lower Credit Spread" not in df.columns:
        return "Insufficient Data"

    series = df["CCC and Lower Credit Spread"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Distressed Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Distressed Pressure Easing"
    return "Distressed Pressure Stable"


options_credit_conditions_financing_pressure_map = {
    "Investment Grade Spread Pressure": investment_grade_spread_pressure_signal,
    "High Yield Spread Pressure": high_yield_spread_pressure_signal,
    "Distressed Credit Pressure": distressed_credit_pressure_signal
}


# -------------------------------------------------------------------------------------------------
# Bank Balance Sheet Liquidity and Credit Capacity Indicator Logic
# -------------------------------------------------------------------------------------------------
def bank_cash_liquidity_conditions_signal(df, period=12):
    """
    Evaluates bank cash liquidity conditions relative to the recent average.

    Returns:
        str: Bank cash liquidity conditions signal.
    """
    if df is None or "Bank Cash Assets" not in df.columns:
        return "Insufficient Data"

    series = df["Bank Cash Assets"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Cash Liquidity Improving"
    if latest < avg_recent * 0.98:
        return "Cash Liquidity Weakening"
    return "Cash Liquidity Stable"


def bank_asset_capacity_signal(df, period=12):
    """
    Evaluates bank total asset capacity relative to the recent average.

    Returns:
        str: Bank asset capacity signal.
    """
    if df is None or "Bank Total Assets" not in df.columns:
        return "Insufficient Data"

    series = df["Bank Total Assets"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Asset Capacity Expanding"
    if latest < avg_recent * 0.98:
        return "Asset Capacity Contracting"
    return "Asset Capacity Stable"


def bank_defensive_positioning_signal(df, period=12):
    """
    Evaluates defensive positioning using treasury and agency securities holdings.

    Returns:
        str: Bank defensive positioning signal.
    """
    if df is None or "Treasury and Agency Securities Holdings" not in df.columns:
        return "Insufficient Data"

    series = df["Treasury and Agency Securities Holdings"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Defensive Positioning Rising"
    if latest < avg_recent * 0.98:
        return "Defensive Positioning Easing"
    return "Defensive Positioning Stable"


options_bank_balance_sheet_liquidity_map = {
    "Bank Cash Liquidity Conditions": bank_cash_liquidity_conditions_signal,
    "Bank Asset Capacity": bank_asset_capacity_signal,
    "Bank Defensive Positioning": bank_defensive_positioning_signal
}
