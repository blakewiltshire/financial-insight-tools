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
# Country External Balance Indicator Logic
# -------------------------------------------------------------------------------------------------
def export_conditions_signal(df, period=12):
    """
    Evaluates total exports of goods and services relative to the recent average.

    Returns:
        str: Export conditions signal.
    """
    if df is None or "Exports of Goods and Services" not in df.columns:
        return "Insufficient Data"

    series = df["Exports of Goods and Services"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Export Conditions Strengthening"
    if latest < avg_recent * 0.98:
        return "Export Conditions Softening"
    return "Export Conditions Stable"


def import_conditions_signal(df, period=12):
    """
    Evaluates total imports of goods and services relative to the recent average.

    Returns:
        str: Import conditions signal.
    """
    if df is None or "Imports of Goods and Services" not in df.columns:
        return "Insufficient Data"

    series = df["Imports of Goods and Services"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Import Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Import Pressure Easing"
    return "Import Conditions Stable"


def trade_balance_position_signal(df, period=12):
    """
    Evaluates the trade balance in goods and services relative to the recent average.

    Higher values imply improvement in the trade balance position
    (e.g. smaller deficit or larger surplus).

    Returns:
        str: Trade balance position signal.
    """
    if df is None or "Trade Balance Goods and Services" not in df.columns:
        return "Insufficient Data"

    series = df["Trade Balance Goods and Services"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Trade Balance Improving"
    if latest < avg_recent * 0.98:
        return "Trade Balance Deteriorating"
    return "Trade Balance Stable"


def current_account_position_signal(df, period=8):
    """
    Evaluates the current account balance relative to the recent average.

    Higher values imply improvement in the current account position
    (e.g. smaller deficit or larger surplus).

    Returns:
        str: Current account position signal.
    """
    if df is None or "Current Account Balance" not in df.columns:
        return "Insufficient Data"

    series = df["Current Account Balance"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Current Account Improving"
    if latest < avg_recent * 0.98:
        return "Current Account Weakening"
    return "Current Account Stable"


def reserve_layer_support_signal(df, period=12):
    """
    Evaluates official reserves excluding gold relative to the recent average.

    Returns:
        str: Reserve layer support signal.
    """
    if df is None or "Official Reserves Excluding Gold" not in df.columns:
        return "Insufficient Data"

    series = df["Official Reserves Excluding Gold"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Reserve Support Strengthening"
    if latest < avg_recent * 0.98:
        return "Reserve Support Softening"
    return "Reserve Support Stable"


options_country_external_balance_map = {
    "Export Conditions": export_conditions_signal,
    "Import Conditions": import_conditions_signal,
    "Trade Balance Position": trade_balance_position_signal,
    "Current Account Position": current_account_position_signal,
    "Reserve Layer Support": reserve_layer_support_signal,
}


# -------------------------------------------------------------------------------------------------
# External Constraint Capital Flow Indicator Logic
# -------------------------------------------------------------------------------------------------
def current_account_anchor_signal(df, period=8):
    """
    Evaluates the current account balance relative to the recent average.

    Higher values imply a firmer external anchor
    (e.g. smaller deficit or larger surplus).

    Returns:
        str: Current account anchor signal.
    """
    if df is None or "Current Account Balance" not in df.columns:
        return "Insufficient Data"

    series = df["Current Account Balance"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "External Anchor Improving"
    if latest < avg_recent * 0.98:
        return "External Anchor Weakening"
    return "External Anchor Stable"


def net_international_position_signal(df, period=8):
    """
    Evaluates the quarterly net international investment position relative to the recent average.

    Higher values imply an improving net international position
    (e.g. less negative or more positive).

    Returns:
        str: Net international position signal.
    """
    if df is None or "Net International Investment Position Quarterly" not in df.columns:
        return "Insufficient Data"

    series = df["Net International Investment Position Quarterly"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Net International Position Improving"
    if latest < avg_recent * 0.98:
        return "Net International Position Deteriorating"
    return "Net International Position Stable"


def investment_income_pressure_signal(df, period=8):
    """
    Evaluates primary investment income payments relative to the recent average.

    Higher values imply greater outward income pressure.

    Returns:
        str: Investment income pressure signal.
    """
    if df is None or "Primary Investment Income payments" not in df.columns:
        return "Insufficient Data"

    series = df["Primary Investment Income payments"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Investment Income Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Investment Income Pressure Easing"
    return "Investment Income Pressure Stable"


def reserve_support_conditions_signal(df, period=12):
    """
    Evaluates official reserves excluding gold relative to the recent average.

    Returns:
        str: Reserve support conditions signal.
    """
    if df is None or "Official Reserves Excluding Gold" not in df.columns:
        return "Insufficient Data"

    series = df["Official Reserves Excluding Gold"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Reserve Conditions Strengthening"
    if latest < avg_recent * 0.98:
        return "Reserve Conditions Softening"
    return "Reserve Conditions Stable"


options_external_constraint_capital_flow_map = {
    "Current Account Anchor": current_account_anchor_signal,
    "Net International Position": net_international_position_signal,
    "Investment Income Pressure": investment_income_pressure_signal,
    "Reserve Support Conditions": reserve_support_conditions_signal,
}
