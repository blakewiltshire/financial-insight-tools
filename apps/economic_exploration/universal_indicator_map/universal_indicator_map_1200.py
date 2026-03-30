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
# Forward Production Conditions Indicator Logic
# -------------------------------------------------------------------------------------------------
def business_conditions_signal(df: pd.DataFrame, period=12):
    """
    Evaluates the latest business conditions diffusion reading relative to the recent average.

    Returns:
        str: Business conditions signal.
    """
    if df is None or "Business Conditions Diffusion Index" not in df.columns:
        return "Insufficient Data"

    series = df["Business Conditions Diffusion Index"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent + 2:
        return "Business Conditions Strengthening"
    if latest < avg_recent - 2:
        return "Business Conditions Weakening"
    return "Business Conditions Stable"


def production_activity_signal(df: pd.DataFrame, period=12):
    """
    Evaluates the latest industrial production reading relative to the recent average.

    Returns:
        str: Production activity signal.
    """
    if df is None or "Industrial Production Index" not in df.columns:
        return "Insufficient Data"

    series = df["Industrial Production Index"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.01:
        return "Production Activity Improving"
    if latest < avg_recent * 0.99:
        return "Production Activity Softening"
    return "Production Activity Stable"


def demand_transmission_signal(df: pd.DataFrame, period=12):
    """
    Evaluates the latest manufacturing durable goods orders reading relative to the recent average.

    Returns:
        str: Demand transmission signal.
    """
    if df is None or "Manufacturing Durable Goods Orders" not in df.columns:
        return "Insufficient Data"

    series = df["Manufacturing Durable Goods Orders"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Demand Reinforcing"
    if latest < avg_recent * 0.98:
        return "Demand Weakening"
    return "Demand Stable"

# -------------------------------------------------------------------------------------------------
# Indicator Mapping
# -------------------------------------------------------------------------------------------------
options_forward_production_conditions_map = {
    "Business Conditions": business_conditions_signal,
    "Production Activity": production_activity_signal,
    "Demand Transmission": demand_transmission_signal
}


# -------------------------------------------------------------------------------------------------
# Services Activity Conditions Indicator Logic
# -------------------------------------------------------------------------------------------------
def services_consumption_signal(df: pd.DataFrame, period=12):
    """
    Evaluates the latest nominal services consumption reading relative to the recent average.

    Returns:
        str: Services consumption signal.
    """
    if df is None or "Services Consumption (Nominal)" not in df.columns:
        return "Insufficient Data"

    series = df["Services Consumption (Nominal)"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.02:
        return "Services Consumption Strengthening"
    if latest < avg_recent * 0.98:
        return "Services Consumption Weakening"
    return "Services Consumption Stable"


def real_services_demand_signal(df: pd.DataFrame, period=12):
    """
    Evaluates the latest real services consumption reading relative to the recent average.

    Returns:
        str: Real services demand signal.
    """
    if df is None or "Services Consumption (Real)" not in df.columns:
        return "Insufficient Data"

    series = df["Services Consumption (Real)"].dropna()
    if len(series) < period:
        return "Insufficient Data"

    latest = series.iloc[-1]
    avg_recent = series.tail(period).mean()

    if latest > avg_recent * 1.01:
        return "Real Demand Strengthening"
    if latest < avg_recent * 0.99:
        return "Real Demand Weakening"
    return "Real Demand Stable"


# -------------------------------------------------------------------------------------------------
# Indicator Mapping
# -------------------------------------------------------------------------------------------------
options_services_activity_conditions_map = {
    "Business Conditions": business_conditions_signal,
    "Services Consumption": services_consumption_signal,
    "Real Services Demand": real_services_demand_signal
}
