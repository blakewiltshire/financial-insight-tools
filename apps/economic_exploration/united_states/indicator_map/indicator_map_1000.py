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
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Add universal indicator module path explicitly
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_indicator_map"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Imports — Universal Indicator Maps
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_1000 import options_currency_regime_framework_map


# -------------------------------------------------------------------------------------------------
# Local Indicator Logic — Dollar Strength and Global Transmission
# -------------------------------------------------------------------------------------------------
def dollar_strength_positioning_signal(df, period=20):
    """
    Evaluates dollar strength positioning relative to the recent average.

    Args:
        df (pd.DataFrame): Daily dataframe containing 'Trade Weighted Currency Index'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Dollar strength positioning signal.
    """
    if df is None or "Trade Weighted Currency Index" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Trade Weighted Currency Index"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Dollar Strength Firming"
    if latest < avg_recent * 0.98:
        return "Dollar Strength Softening"
    return "Dollar Strength Stable"


def trade_weighted_dollar_pressure_signal(df, period=20):
    """
    Evaluates trade-weighted dollar pressure relative to the recent average.

    Args:
        df (pd.DataFrame): Daily dataframe containing 'Trade Weighted Currency Index'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Trade-weighted dollar pressure signal.
    """
    if df is None or "Trade Weighted Currency Index" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Trade Weighted Currency Index"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Trade Weighted Pressure Rising"
    if latest < avg_recent * 0.98:
        return "Trade Weighted Pressure Easing"
    return "Trade Weighted Pressure Stable"


def cross_market_transmission_signal(df, period=20):
    """
    Evaluates the trade-weighted dollar index as a proxy for wider cross-market transmission pressure.

    Args:
        df (pd.DataFrame): Daily dataframe containing 'Trade Weighted Currency Index'.
        period (int): Lookback window for recent average comparison.

    Returns:
        str: Cross-market transmission signal.
    """
    if df is None or "Trade Weighted Currency Index" not in df.columns:
        return "Insufficient Data"

    series = pd.to_numeric(df["Trade Weighted Currency Index"], errors="coerce").dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Transmission Pressure Building"
    if latest < avg_recent * 0.98:
        return "Transmission Pressure Easing"
    return "Transmission Pressure Stable"


options_dollar_strength_global_transmission_map = {
    "Dollar Strength Positioning": dollar_strength_positioning_signal,
    "Trade Weighted Dollar Pressure": trade_weighted_dollar_pressure_signal,
    "Cross Market Transmission": cross_market_transmission_signal,
}


# -------------------------------------------------------------------------------------------------
# Signal Mapping
# -------------------------------------------------------------------------------------------------
ALL_INDICATOR_MAPS = {
    "Currency Regime Framework": options_currency_regime_framework_map,
    "Dollar Strength and Global Transmission": options_dollar_strength_global_transmission_map,
}


# -------------------------------------------------------------------------------------------------
# Dispatcher
# -------------------------------------------------------------------------------------------------
def get_indicator_maps():
    """
    Returns the complete indicator mapping aligned to signal-level use cases.
    """
    return ALL_INDICATOR_MAPS
