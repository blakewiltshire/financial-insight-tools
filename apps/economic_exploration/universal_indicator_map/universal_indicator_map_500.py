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
# Money Supply and Velocity Dynamics Indicator Logic
# -------------------------------------------------------------------------------------------------
def narrow_money_conditions_signal(df, period=12):
    """
    Evaluates M1 money supply relative to the recent average.

    Returns:
        str: Narrow money conditions signal.
    """
    if df is None or "M1 Money Supply" not in df.columns:
        return "Insufficient Data"

    series = df["M1 Money Supply"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Narrow Liquidity Expanding"
    if latest < avg_recent * 0.98:
        return "Narrow Liquidity Contracting"
    return "Narrow Liquidity Stable"


def broad_money_conditions_signal(df, period=12):
    """
    Evaluates M2 money supply relative to the recent average.

    Returns:
        str: Broad money conditions signal.
    """
    if df is None or "M2 Money Supply" not in df.columns:
        return "Insufficient Data"

    series = df["M2 Money Supply"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Broad Liquidity Expanding"
    if latest < avg_recent * 0.98:
        return "Broad Liquidity Contracting"
    return "Broad Liquidity Stable"


def narrow_money_velocity_signal(df, period=8):
    """
    Evaluates M1 money velocity relative to the recent average.

    Returns:
        str: Narrow money velocity signal.
    """
    if df is None or "M1 Money Velocity" not in df.columns:
        return "Insufficient Data"

    series = df["M1 Money Velocity"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Narrow Money Circulation Accelerating"
    if latest < avg_recent * 0.98:
        return "Narrow Money Circulation Slowing"
    return "Narrow Money Circulation Stable"


def broad_money_velocity_signal(df, period=8):
    """
    Evaluates M2 money velocity relative to the recent average.

    Returns:
        str: Broad money velocity signal.
    """
    if df is None or "M2 Money Velocity" not in df.columns:
        return "Insufficient Data"

    series = df["M2 Money Velocity"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Broad Money Circulation Accelerating"
    if latest < avg_recent * 0.98:
        return "Broad Money Circulation Slowing"
    return "Broad Money Circulation Stable"


options_money_supply_and_velocity_dynamics_map = {
    "Narrow Money Conditions": narrow_money_conditions_signal,
    "Broad Money Conditions": broad_money_conditions_signal,
    "Narrow Money Velocity": narrow_money_velocity_signal,
    "Broad Money Velocity": broad_money_velocity_signal,
}

# -------------------------------------------------------------------------------------------------
# Interest Rate Regime and Transmission Indicator Logic
# -------------------------------------------------------------------------------------------------
def policy_rate_positioning_signal(df, period=12):
    """
    Evaluates the central bank funds rate relative to the recent average.

    Returns:
        str: Policy rate positioning signal.
    """
    if df is None or "Central Bank Funds Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Central Bank Funds Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Policy Stance Tightening"
    if latest < avg_recent * 0.98:
        return "Policy Stance Easing"
    return "Policy Stance Stable"


def funding_rate_conditions_signal(df, period=20):
    """
    Evaluates overnight funding conditions relative to the recent average.

    Returns:
        str: Funding rate conditions signal.
    """
    if df is None or "Overnight Funding Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Overnight Funding Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Funding Conditions Tightening"
    if latest < avg_recent * 0.98:
        return "Funding Conditions Easing"
    return "Funding Conditions Stable"


def bank_lending_rate_pressure_signal(df, period=20):
    """
    Evaluates prime lending rate pressure relative to the recent average.

    Returns:
        str: Bank lending rate pressure signal.
    """
    if df is None or "Prime Lending Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Prime Lending Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Bank Lending Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Bank Lending Pressure Easing"
    return "Bank Lending Pressure Stable"


def mortgage_rate_conditions_signal(df, period=12):
    """
    Evaluates mortgage rate conditions relative to the recent average.

    Returns:
        str: Mortgage rate conditions signal.
    """
    if df is None or "Long-Term Mortgage Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Long-Term Mortgage Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Mortgage Conditions Tightening"
    if latest < avg_recent * 0.98:
        return "Mortgage Conditions Easing"
    return "Mortgage Conditions Stable"


def treasury_curve_structure_signal(df, period=20):
    """
    Evaluates the yield curve spread relative to the recent average.

    Returns:
        str: Treasury curve structure signal.
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


def real_policy_rate_proxy_signal(df, period=12):
    """
    Evaluates the proxy central bank funds rate relative to the recent average.

    Returns:
        str: Real policy rate proxy signal.
    """
    if df is None or "Proxy Central Bank Funds Rate" not in df.columns:
        return "Insufficient Data"

    series = df["Proxy Central Bank Funds Rate"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Real Policy Constraint Rising"
    if latest < avg_recent * 0.98:
        return "Real Policy Constraint Easing"
    return "Real Policy Constraint Stable"


options_interest_rate_regime_and_transmission_map = {
    "Policy Rate Positioning": policy_rate_positioning_signal,
    "Funding Rate Conditions": funding_rate_conditions_signal,
    "Bank Lending Rate Pressure": bank_lending_rate_pressure_signal,
    "Mortgage Rate Conditions": mortgage_rate_conditions_signal,
    "Treasury Curve Structure": treasury_curve_structure_signal,
    "Real Policy Rate Proxy": real_policy_rate_proxy_signal,
}
