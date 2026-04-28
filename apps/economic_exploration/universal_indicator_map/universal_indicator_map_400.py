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
# Inflation Pressure and Transmission Indicator Logic
# -------------------------------------------------------------------------------------------------
def consumer_price_pressure_signal(df, period=12):
    """
    Evaluates headline CPI relative to the recent average.

    Returns:
        str: Consumer price pressure signal.
    """
    if df is None or "Headline CPI" not in df.columns:
        return "Insufficient Data"

    series = df["Headline CPI"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Consumer Inflationary Pressure"
    if latest < avg_recent * 0.98:
        return "Consumer Deflationary Pressure"
    return "Consumer Prices Stable"


def core_consumer_inflation_signal(df, period=12):
    """
    Evaluates core CPI relative to the recent average.

    Returns:
        str: Core consumer inflation signal.
    """
    if df is None or "Core CPI" not in df.columns:
        return "Insufficient Data"

    series = df["Core CPI"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Core Inflation Firm"
    if latest < avg_recent * 0.98:
        return "Core Inflation Softening"
    return "Core Inflation Stable"


def producer_price_pressure_signal(df, period=12):
    """
    Evaluates headline PPI relative to the recent average.

    Returns:
        str: Producer price pressure signal.
    """
    if df is None or "Headline PPI" not in df.columns:
        return "Insufficient Data"

    series = df["Headline PPI"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Producer Inflationary Pressure"
    if latest < avg_recent * 0.98:
        return "Producer Deflationary Pressure"
    return "Producer Prices Stable"


def core_producer_inflation_signal(df, period=12):
    """
    Evaluates core PPI relative to the recent average.

    Returns:
        str: Core producer inflation signal.
    """
    if df is None or "Core PPI" not in df.columns:
        return "Insufficient Data"

    series = df["Core PPI"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Core Producer Inflation Firm"
    if latest < avg_recent * 0.98:
        return "Core Producer Inflation Softening"
    return "Core Producer Inflation Stable"


options_inflation_pressure_and_transmission_map = {
    "Consumer Price Pressure": consumer_price_pressure_signal,
    "Core Consumer Inflation": core_consumer_inflation_signal,
    "Producer Price Pressure": producer_price_pressure_signal,
    "Core Producer Inflation": core_producer_inflation_signal
}
