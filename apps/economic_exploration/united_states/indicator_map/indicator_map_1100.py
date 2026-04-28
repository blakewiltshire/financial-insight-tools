# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Indicator Map — Thematic Extension Logic
--------------------------------------------------

This module defines local indicator-to-signal function mappings for country-specific
or theme-specific extensions.
It works in parallel with the universal system, providing optional overrides where
local conditions apply.

System Role:
- Allows country-specific or dataset-specific indicator evaluation
- Merges seamlessly into the core Economic Exploration evaluation framework
- Supports expanded insight generation, scoring, and AI-compatible workflows
for local data nuances

AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Expansion Detected", "Decline", "Neutral", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- Numeric payloads, tuples, or dynamic secondary values are **not
permitted** — all returns are pure text strings

---------------------------------------------------------------
System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

**Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

**String-Based Return Values**
- Every function must return a plain text string suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example returns: `"Sector Momentum: Manufacturing"`, `"Both Expanding"`, `"Insufficient Data"`

**Sector-Level Dynamic Labels (Optional)**
- For sectoral breakdowns, string returns may embed dynamic entity names directly
within the signal string (e.g., `"Sector Momentum: Manufacturing"`).
- These dynamic entity names are parsed downstream during insight generation —
not handled inside signal functions.

**No Numeric Payloads**
- Signal outputs must not return any numeric values, tuples, or secondary calculation payloads.
- All quantitative context is handled separately via metrics and charting layers.

**Dispatcher Independence**
- Signal routing and indicator map merging is handled via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- No embedded routing logic or external data references within signal functions.

Governance Note:
- Local indicator maps extend the system only where country-specific or theme-specific
datasets exist.
- Users modify these local modules for custom configurations; universal modules remain
system-stable.
"""

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys
import pandas as pd

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_indicator_map"))

if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_indicator_map_1100 import get_indicator_signal_map


# -------------------------------------------------------------------------------------------------
# Aggregate Equity Allocation Indicator Logic
# -------------------------------------------------------------------------------------------------
def equity_market_value_position_signal(df: pd.DataFrame, period=12):
    required_cols = [
        "Domestic Financial Sector Equities",
        "Nonfinancial Corporate Equities",
    ]

    if df is None or any(col not in df.columns for col in required_cols):
        return "Insufficient Data"

    series = (
        df["Domestic Financial Sector Equities"].fillna(0)
        + df["Nonfinancial Corporate Equities"].fillna(0)
    ).dropna()

    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.05:
        return "Aggregate Equity Value Elevated"
    if latest < avg_recent * 0.95:
        return "Aggregate Equity Value Softening"

    return "Aggregate Equity Value Stable"


def economy_wide_liability_structure_signal(df: pd.DataFrame, period=12):
    required_cols = [
        "Central Government Debt Liabilities",
        "State Local Government Debt Liabilities",
        "Nonfinancial Corporate Debt Liabilities",
        "Household Nonprofit Debt Liabilities",
        "Rest Of World Debt Liabilities",
    ]

    if df is None or any(col not in df.columns for col in required_cols):
        return "Insufficient Data"

    series = (
        df["Central Government Debt Liabilities"].fillna(0)
        + df["State Local Government Debt Liabilities"].fillna(0)
        + df["Nonfinancial Corporate Debt Liabilities"].fillna(0)
        + df["Household Nonprofit Debt Liabilities"].fillna(0)
        + df["Rest Of World Debt Liabilities"].fillna(0)
    ).dropna()

    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.05:
        return "Liability Structure Expanding"
    if latest < avg_recent * 0.95:
        return "Liability Structure Easing"

    return "Liability Structure Stable"


def aggregate_equity_allocation_ratio_signal(df: pd.DataFrame, period=12):
    required_cols = [
        "Domestic Financial Sector Equities",
        "Nonfinancial Corporate Equities",
        "Central Government Debt Liabilities",
        "State Local Government Debt Liabilities",
        "Nonfinancial Corporate Debt Liabilities",
        "Household Nonprofit Debt Liabilities",
        "Rest Of World Debt Liabilities",
    ]

    if df is None or any(col not in df.columns for col in required_cols):
        return "Insufficient Data"

    total_equity_market_value = (
        df["Domestic Financial Sector Equities"].fillna(0)
        + df["Nonfinancial Corporate Equities"].fillna(0)
    )

    total_real_economy_liabilities = (
        df["Central Government Debt Liabilities"].fillna(0)
        + df["State Local Government Debt Liabilities"].fillna(0)
        + df["Nonfinancial Corporate Debt Liabilities"].fillna(0)
        + df["Household Nonprofit Debt Liabilities"].fillna(0)
        + df["Rest Of World Debt Liabilities"].fillna(0)
    )

    allocation_base = (
        total_equity_market_value + total_real_economy_liabilities
    ).replace(0, pd.NA)

    aear_series = (total_equity_market_value / allocation_base).dropna()

    if len(aear_series) < period:
        return "Insufficient Data"

    latest = aear_series.iloc[-1]
    avg_recent = aear_series.tail(period).mean()

    if latest > avg_recent * 1.05:
        return "Equity Allocation Share Elevated"
    if latest < avg_recent * 0.95:
        return "Equity Allocation Share Softening"

    return "Equity Allocation Share Stable"


# -------------------------------------------------------------------------------------------------
# Merge: Universal + Local Indicator Maps
# -------------------------------------------------------------------------------------------------
template_signals = get_indicator_signal_map()

ALL_INDICATOR_MAPS = {
    "Signal A": {
        "Signal A": template_signals["Signal A"],
    },
    "Signal B": {
        "Signal B": template_signals["Signal B"],
    },
    "Signal C": {
        "Signal C": template_signals["Signal C"],
    },
    "Aggregate Equity Allocation": {
        "Equity Market Value Position": equity_market_value_position_signal,
        "Economy Wide Liability Structure": economy_wide_liability_structure_signal,
        "Aggregate Equity Allocation Ratio": aggregate_equity_allocation_ratio_signal,
    },
}


# -------------------------------------------------------------------------------------------------
# Dispatcher
# -------------------------------------------------------------------------------------------------
def get_indicator_maps():
    """
    Returns the complete indicator mapping aligned to signal-level use cases.
    """
    return ALL_INDICATOR_MAPS
