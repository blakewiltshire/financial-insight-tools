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
# Currency Regime Framework Indicator Logic
# -------------------------------------------------------------------------------------------------
def currency_strength_position_signal(df, period=20):
    """
    Evaluates the trade-weighted currency index relative to its recent average.

    Args:
        df (pd.DataFrame): Daily dataframe containing 'Trade Weighted Currency Index'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Currency strength positioning signal.
    """
    if df is None or "Trade Weighted Currency Index" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Trade Weighted Currency Index"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Currency Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Currency Pressure Easing"
    return "Currency Pressure Stable"


def reserve_stability_conditions_signal(df, period=12):
    """
    Evaluates official reserves excluding gold relative to the recent average.

    Args:
        df (pd.DataFrame): Monthly dataframe containing 'Official Reserves Excluding Gold'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Reserve stability conditions signal.
    """
    if df is None or "Official Reserves Excluding Gold" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Official Reserves Excluding Gold"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Reserve Position Strengthening"
    if latest < avg_recent * 0.98:
        return "Reserve Position Softening"
    return "Reserve Position Stable"


def current_account_support_signal(df, period=8):
    """
    Evaluates the current account balance relative to the recent average.

    Args:
        df (pd.DataFrame): Quarterly dataframe containing 'Current Account Balance'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Current account support signal.
    """
    if df is None or "Current Account Balance" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Current Account Balance"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "External Balance Support Improving"
    if latest < avg_recent * 0.98:
        return "External Balance Support Weakening"
    return "External Balance Support Stable"


options_currency_regime_framework_map = {
    "Currency Strength Position": currency_strength_position_signal,
    "Reserve Stability Conditions": reserve_stability_conditions_signal,
    "Current Account Support": current_account_support_signal,
}
