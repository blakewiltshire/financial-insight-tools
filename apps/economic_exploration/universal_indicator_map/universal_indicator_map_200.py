# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name
# pylint: disable=undefined-variable, redefined-outer-name

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
# Imports
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Employment (Ex Agriculture) Indicator Logic
# -------------------------------------------------------------------------------------------------
def employment_momentum(df, period=3):
    """Detects hiring momentum vs long-term trend."""
    if df is None or "Employment ex Agriculture" not in df.columns:
        return "Insufficient Data"
    series = df["Employment ex Agriculture"].pct_change().dropna()
    if series.empty or len(series) < period + 12:
        return "Insufficient Data"
    recent = series.tail(period)
    long_term = series.rolling(12).mean().dropna()
    if long_term.empty:
        return "Insufficient Data"
    short_avg = recent.mean()
    long_avg = long_term.iloc[-1]
    if short_avg > long_avg * 1.2:
        return "Strong Momentum"
    if short_avg < long_avg * 0.8:
        return "Weak or Reversing"
    return "Neutral Hiring Trend"


def employment_volatility(df, period=6):
    """Measures employment growth volatility."""
    if df is None or "Employment ex Agriculture" not in df.columns:
        return "Insufficient Data"
    series = df["Employment ex Agriculture"].pct_change().dropna().tail(period)
    if series.empty or len(series) < period:
        return "Insufficient Data"
    std_dev = series.std()
    if std_dev > 0.015:
        return "Volatile Hiring Patterns"
    if std_dev < 0.005:
        return "Stable Employment Growth"
    return "Moderate Volatility"


def employment_inflection(df, period=None):
    """Detects directional inflection in employment."""
    if df is None or "Employment ex Agriculture" not in df.columns:
        return "Insufficient Data"
    series = df["Employment ex Agriculture"].pct_change().dropna()
    if len(series) < 3:
        return "Insufficient Data"
    last = series.iloc[-1]
    prev = series.iloc[-2]
    if last > 0 and prev < 0:
        return "Turning Positive"
    if last < 0 and prev > 0:
        return "Turning Negative"
    return "No Recent Inflection"

options_employment_signals_map = {
    "Job Creation Momentum": employment_momentum,
    "Volatility in Hiring Activity": employment_volatility,
    "Cyclical Turning Points": employment_inflection
}

# -------------------------------------------------------------------------------------------------
# Unemployment Rate Indicator Logic
# -------------------------------------------------------------------------------------------------
def unemployment_direction(df, period=None):
    """Tracks short-term directional change in unemployment."""
    if df is None or "Unemployment Rate" not in df.columns:
        return "Insufficient Data"
    recent = df["Unemployment Rate"].dropna().tail(2)
    if len(recent) < 2:
        return "Insufficient Data"
    if recent.iloc[-1] > recent.iloc[-2]:
        return "Unemployment Rising"
    if recent.iloc[-1] < recent.iloc[-2]:
        return "Unemployment Falling"
    return "Unchanged"


def unemployment_reversion(df, period=None):
    """Flags reversion from cyclical highs/lows in unemployment."""
    if df is None or "Unemployment Rate" not in df.columns:
        return "Insufficient Data"
    series = df["Unemployment Rate"].dropna().tail(12)
    if series.empty or len(series) < 12:
        return "Insufficient Data"
    current = series.iloc[-1]
    max_val = series.max()
    min_val = series.min()
    if current <= min_val + 0.1:
        return "Near Cycle Low"
    if current >= max_val - 0.1:
        return "Near Cycle High"
    return "Mid-Range Level"


def unemployment_volatility(df, period=6):
    """Detects volatility in unemployment readings."""
    if df is None or "Unemployment Rate" not in df.columns:
        return "Insufficient Data"
    series = df["Unemployment Rate"].dropna().tail(period)
    if len(series) < period:
        return "Insufficient Data"
    std_dev = series.std()
    if std_dev > 0.4:
        return "Unemployment Volatility Elevated"
    if std_dev < 0.2:
        return "Stable Unemployment Readings"
    return "Moderate Volatility"

options_unemployment_signals_map = {
    "Unemployment Shifts": unemployment_direction,
    "Stress or Slack Indicators": unemployment_reversion,
    "Reversion from Extremes": unemployment_volatility
}

# -------------------------------------------------------------------------------------------------
# Labour Force Participation Rate Indicator Logic
# -------------------------------------------------------------------------------------------------
def participation_trend(df, period=6):
    """Detects directional shift in labour participation."""
    if df is None or "Labour Participation Rate" not in df.columns:
        return "Insufficient Data"
    series = df["Labour Participation Rate"].dropna().tail(period)
    if len(series) < period:
        return "Insufficient Data"
    avg_change = series.diff().mean()
    if avg_change > 0.05:
        return "Participation Increasing"
    if avg_change < -0.05:
        return "Participation Declining"
    return "Stable Engagement"


def participation_variability(df, period=12):
    """Flags volatility in participation behaviour."""
    if df is None or "Labour Participation Rate" not in df.columns:
        return "Insufficient Data"
    series = df["Labour Participation Rate"].dropna().tail(period)
    if len(series) < period:
        return "Insufficient Data"
    std_dev = series.std()
    if std_dev > 0.4:
        return "Structural Shifts Detected"
    if std_dev < 0.1:
        return "Stable Participation Rate"
    return "Mild Variability"


def participation_extreme_check(df, period=36):
    """Compares current participation to multi-year extremes."""
    if df is None or "Labour Participation Rate" not in df.columns:
        return "Insufficient Data"
    series = df["Labour Participation Rate"].dropna().tail(period)
    if len(series) < period:
        return "Insufficient Data"
    current = series.iloc[-1]
    max_val = series.max()
    min_val = series.min()
    if current >= 0.98 * max_val:
        return "Near Multi-Year High"
    if current <= 1.02 * min_val:
        return "Near Multi-Year Low"
    return "Mid-Cycle Engagement Level"


options_participation_signals_map = {
    "Participation Stability": participation_trend,
    "Demographic or Structural Shifts": participation_variability,
    "Engagement Trend Change": participation_extreme_check
}
