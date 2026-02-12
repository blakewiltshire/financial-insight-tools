# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Local Indicator Map — Thematic Extension Logic
--------------------------------------------------

This module defines local indicator-to-signal function mappings for country-specific
or theme-specific extensions.
It works in parallel with the universal system, providing optional overrides where
local conditions apply.

✅ System Role:
- Allows country-specific or dataset-specific indicator evaluation
- Merges seamlessly into the core Economic Exploration evaluation framework
- Supports expanded insight generation, scoring, and AI-compatible workflows
for local data nuances

🧠 AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Expansion Detected", "Decline", "Neutral", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- Numeric payloads, tuples, or dynamic secondary values are **not
permitted** — all returns are pure text strings

---------------------------------------------------------------
⚙️ System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

1️⃣ **Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

2️⃣ **String-Based Return Values**
- Every function must return a plain text string suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example returns: `"Sector Momentum: Manufacturing"`, `"Both Expanding"`, `"Insufficient Data"`

3️⃣ **Sector-Level Dynamic Labels (Optional)**
- For sectoral breakdowns, string returns may embed dynamic entity names directly
within the signal string (e.g., `"Sector Momentum: Manufacturing"`).
- These dynamic entity names are parsed downstream during insight generation —
not handled inside signal functions.

4️⃣ **No Numeric Payloads**
- Signal outputs must not return any numeric values, tuples, or secondary calculation payloads.
- All quantitative context is handled separately via metrics and charting layers.

5️⃣ **Dispatcher Independence**
- Signal routing and indicator map merging is handled via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- No embedded routing logic or external data references within signal functions.

🧭 Governance Note:
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
# Imports — Universal Indicators
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_100 import (
    options_gdp_growth_rate_map,
    options_nominal_gdp_map,
    options_gdp_components_map
)

# Optionally extend below
def conference_board_leading_signal(df, period=3):
    """Evaluates directional momentum of the US Leading Index (CB)."""
    col = "US Leading Index (Conference Board)"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    recent = df[col].dropna().tail(period)
    if len(recent) < period:
        return "Insufficient Data"
    trend = recent.diff().mean()
    if trend > 0.1:
        return "Uptrend Confirmed"
    if trend < -0.1:
        return "Downtrend Confirmed"
    return "Flat or Reversing"


def weekly_economic_index_signal(df, period=4):
    """Evaluates weekly trends in the Weekly Economic Index (NY Fed)."""
    col = "Weekly Economic Index (Lewis-Mertens-Stock)"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    recent = df[col].dropna().tail(period)
    if len(recent) < period:
        return "Insufficient Data"
    trend = recent.diff().mean()
    if trend > 0.02:
        return "Momentum Strengthening"
    if trend < -0.02:
        return "Momentum Weakening"
    return "Stagnant or Mixed"


def uncertainty_index_signal(df_recent, df_full=None, period=3):
    """Compares recent vs long-term economic policy uncertainty."""
    col = "Economic Policy Uncertainty Index"
    try:
        recent = df_recent[col].dropna().tail(period)
        if len(recent) < period:
            return "Insufficient Data"
        avg = recent.mean()
        long_term = df_full[col].dropna().rolling(12).mean().iloc[-1]
        if pd.isna(long_term):
            return "Insufficient Data"
        ratio = avg / long_term
        if ratio >= 1.25:
            return "High Volatility Risk"
        if ratio <= 0.85:
            return "Low Uncertainty Environment"
        return "Moderate Uncertainty"
    except Exception as e:
        print("⚠️ Signal error:", e)
        return "Insufficient Data"


def chicago_fed_national_index_signal(df, period=3):
    """Evaluates economic momentum from CFNAI."""
    col = "Chicago Fed National Activity Index"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    recent = df[col].dropna().tail(period)
    if len(recent) < period:
        return "Insufficient Data"
    mean_val = recent.mean()
    if mean_val > 0.25:
        return "Above Trend Activity"
    if mean_val < -0.25:
        return "Below Trend Activity"
    return "Near Neutral Benchmark"


# --- US-Specific Indicator Mapping ---
options_us_macro_composite_map = {
    "Leading Growth Index (CB)": conference_board_leading_signal,
    "Weekly Economic Index (NY Fed)": weekly_economic_index_signal,
    "Uncertainty Index Impact": uncertainty_index_signal,
    "National Activity Composite": chicago_fed_national_index_signal
}

# -------------------------------------------------------------------------------------------------
# Merge: Universal + Local Indicator Maps
# -------------------------------------------------------------------------------------------------
ALL_INDICATOR_MAPS = {
    # Universal Indicators
    "Real GDP": options_gdp_growth_rate_map,
    "Nominal GDP": options_nominal_gdp_map,
    "GDP Components Breakdown": options_gdp_components_map,
    # Local to Coutry (If applicable)
    "Macro Composite Signals": options_us_macro_composite_map
}

def get_indicator_maps():
    """
    Returns the full set of indicators applicable to the current country
    for Economic Growth and Stability.
    """
    return ALL_INDICATOR_MAPS
