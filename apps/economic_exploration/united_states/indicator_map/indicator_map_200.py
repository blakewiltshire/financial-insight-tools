# -------------------------------------------------------------------------------------------------
# 🔧 Pylint Global Exceptions
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
# 📦 Imports — Universal Indicator Maps
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_200 import (
    options_employment_signals_map,
    options_unemployment_signals_map,
    options_participation_signals_map
)

# -------------------------------------------------------------------------------------------------
# 📊 Business Sector Employment Breakdown
# -------------------------------------------------------------------------------------------------

def sector_employment_momentum(df, period=None):
    if df is None or df.empty:
        return "Insufficient Data"
    try:
        recent = df.drop(columns=["date"], errors="ignore").dropna().tail(period or 3)
        momentum_scores = recent.diff().mean().sort_values(ascending=False)
        top_sector = momentum_scores.index[0]
        return f"Sector Momentum: {top_sector}"
    except Exception:
        return "Insufficient Data"

def sector_employment_stress(df, period=None):
    if df is None or df.empty:
        return "Insufficient Data"
    try:
        recent = df.drop(columns=["date"], errors="ignore").dropna().tail(period or 3)
        change_scores = recent.diff().mean().sort_values()
        bottom_sector = change_scores.index[0]
        return f"Sector Stress: {bottom_sector}"
    except Exception:
        return "Insufficient Data"

def sector_employment_summary(df, period=None):
    if df is None or df.empty:
        return "Insufficient Data"
    try:
        recent = df.drop(columns=["date"], errors="ignore").dropna().tail(period or 3)
        mean_change = recent.diff().mean().mean()
        if mean_change >= 0.5:
            return "Broad Expansion"
        if mean_change <= -0.5:
            return "Broad Contraction"
        return "Mixed Sector Activity"
    except Exception:
        return "Insufficient Data"

BUSINESS_SECTOR_EMPLOYMENT_SIGNALS = {
    "Business Sector Employment Breakdown – Momentum": sector_employment_momentum,
    "Business Sector Employment Breakdown – Stress": sector_employment_stress,
    "Business Sector Employment Breakdown – Summary": sector_employment_summary,
}

# -------------------------------------------------------------------------------------------------
# 📊 Full-Time vs Part-Time Employment Dynamics
# -------------------------------------------------------------------------------------------------

def employment_type_balance_signal(df, period=None):
    full_col = "Full-Time Employment"
    part_col = "Part-Time Employment"
    if df is None or full_col not in df.columns or part_col not in df.columns:
        return "Insufficient Data"
    try:
        full_recent = df[full_col].dropna().tail(period or 3).diff().mean()
        part_recent = df[part_col].dropna().tail(period or 3).diff().mean()
        if abs(full_recent) < 0.1 and abs(part_recent) < 0.1:
            return "Minimal Shift"
        if full_recent > part_recent:
            return "Full-Time Leading"
        if part_recent > full_recent:
            return "Part-Time Leading"
        return "Indeterminate"
    except Exception:
        return "Insufficient Data"

def part_time_stress_signal(df, period=None, threshold=0.5):
    col = "Part-Time Employment"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    try:
        recent = df[col].dropna().pct_change().iloc[-1] * 100
        if recent > threshold:
            return "Part-Time Surge"
        return "Stable"
    except Exception:
        return "Insufficient Data"

def employment_quality_shift_signal(df, period=None):
    full_col = "Full-Time Employment"
    part_col = "Part-Time Employment"
    if df is None or full_col not in df.columns or part_col not in df.columns:
        return "Insufficient Data"
    try:
        recent_full = df[full_col].dropna().tail(period or 3).diff().mean()
        recent_part = df[part_col].dropna().tail(period or 3).diff().mean()
        if recent_full < 0 and recent_part > 0:
            return "Part-Time Replacing Full-Time"
        if recent_full > 0 and recent_part > 0:
            return "Both Expanding"
        if recent_full < 0 and recent_part < 0:
            return "Both Contracting"
        return "Stable or Mixed"
    except Exception:
        return "Insufficient Data"

FULL_PART_TIME_EMPLOYMENT_SIGNALS = {
    "Employment Type Balance": employment_type_balance_signal,
    "Part-Time Employment Stress": part_time_stress_signal,
    "Employment Quality Shift": employment_quality_shift_signal,
}

# -------------------------------------------------------------------------------------------------
# 📊 Wage Dynamics (Average Hourly Earnings)
# -------------------------------------------------------------------------------------------------

def earnings_trend_signal(df, period=None):
    col = "Average Hourly Earnings (Total Private)"
    if df is None or col not in df.columns or df[col].dropna().shape[0] < 2:
        return "Insufficient Data"
    try:
        recent = df[col].dropna().pct_change().tail(period or 3) * 100
        avg_growth = recent.mean()
        if avg_growth > 0.3:
            return "Wage Acceleration"
        elif avg_growth < 0.1:
            return "Wage Deceleration"
        else:
            return "Stagnant Wages"
    except Exception:
        return "Insufficient Data"

AVERAGE_HOURLY_EARNINGS_SIGNALS = {
    "Wage Growth Trend": earnings_trend_signal,
}

# -------------------------------------------------------------------------------------------------
# 📊 Jobless Claims (High-Frequency Employment Stress)
# -------------------------------------------------------------------------------------------------

def initial_claims_signal(df, period=None, threshold=2.0):
    col = "Initial Jobless Claims"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    try:
        recent = df[col].dropna().pct_change().iloc[-1] * 100
        if recent > threshold:
            return "Initial Claims Surge"
        return "Stable"
    except Exception:
        return "Insufficient Data"

def continued_claims_trend(df, period=None):
    col = "Continued Jobless Claims"
    if df is None or col not in df.columns:
        return "Insufficient Data"
    try:
        growth = df[col].dropna().pct_change().tail(period or 4).mean() * 100
        if growth > 0.5:
            return "Continued Claims Rising"
        if growth < -0.5:
            return "Improving Conditions"
        return "Flat Trend"
    except Exception:
        return "Insufficient Data"

INITIAL_JOBLESS_CLAIMS_SIGNALS = {
    "Initial Jobless Claims": initial_claims_signal
}

CONTINUED_JOBLESS_CLAIMS_SIGNALS = {
    "Continued Jobless Claims": continued_claims_trend
}

# -------------------------------------------------------------------------------------------------
# 🔗 Merge Complete Indicator Maps
# -------------------------------------------------------------------------------------------------

ALL_INDICATOR_MAPS = {
    # --- Universal Shared Use Cases ---
    "Employment Trends": options_employment_signals_map,
    "Unemployment Context": options_unemployment_signals_map,
    "Labour Force Engagement": options_participation_signals_map,

    # --- Local Use Cases ---
    "Business Sector Employment Breakdown": BUSINESS_SECTOR_EMPLOYMENT_SIGNALS,
    "Full-Time vs Part-Time Employment": FULL_PART_TIME_EMPLOYMENT_SIGNALS,
    "Average Hourly Earnings": AVERAGE_HOURLY_EARNINGS_SIGNALS,
    "Jobless Claims": {
        **INITIAL_JOBLESS_CLAIMS_SIGNALS,
        **CONTINUED_JOBLESS_CLAIMS_SIGNALS
    }
}

def get_indicator_maps():
    return ALL_INDICATOR_MAPS
