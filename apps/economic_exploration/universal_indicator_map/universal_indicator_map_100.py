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
# Real GDP Indicator Logic
# -------------------------------------------------------------------------------------------------
def calculate_qoq_change(df):
    """Calculates quarter-on-quarter change in Real GDP."""
    df = df.copy()
    df["QoQ Change"] = df["Real GDP QoQ Annualized"].diff()
    return df


def gdp_growth_trend(df, period=None):  # pylint: disable=unused-argument

    """
    Detects acceleration or deceleration in Real GDP growth.

    Returns:
        str: Growth signal classification.
    """
    df = calculate_qoq_change(df)
    series = df["QoQ Change"].dropna()
    if series.empty:
        return "Insufficient Data"
    last = df["QoQ Change"].iloc[-1]

    if last > 0:
        return "Accelerating Growth"
    if last < 0:
        return "Decelerating Growth"
    return "Flat or Reversing"


def gdp_volatility_context(df, period=None):    # pylint: disable=unused-argument
    """
    Flags whether current GDP is near recent volatility extremes.

    Returns:
        str: Position within 12-quarter range.
    """
    recent = df.tail(12)
    series = recent["Real GDP QoQ Annualized"].dropna()
    if series.empty:
        return "Insufficient Data"
    max_val = recent["Real GDP QoQ Annualized"].max()
    min_val = recent["Real GDP QoQ Annualized"].min()
    current = df["Real GDP QoQ Annualized"].iloc[-1]

    if current == max_val:
        return "Near 12M High"
    if current == min_val:
        return "Near 12M Low"
    return "Stable Range"


def calculate_yoy_gdp(df):
    """Computes YoY GDP growth and rolling average."""
    df = df.copy()
    df["GDP YoY"] = df["Real GDP (Level)"].pct_change(periods=4) * 100
    df["GDP YoY Avg"] = df["GDP YoY"].rolling(4).mean()
    return df


def yoy_vs_average_signal(df, period=None): # pylint: disable=unused-argument
    """
    Compares current YoY GDP growth against recent average.

    Returns:
        str: Signal indicating strength vs average.
    """
    df = calculate_yoy_gdp(df)
    series = df[["GDP YoY", "GDP YoY Avg"]].dropna()
    if series.empty:
        return "Insufficient Data"
    latest = df["GDP YoY"].iloc[-1]
    avg = df["GDP YoY Avg"].iloc[-1]
    if latest > avg:
        return "YoY Growth Above Avg"
    if latest < avg:
        return "YoY Growth Below Avg"
    return "Neutral"


options_gdp_growth_rate_map = {
    "Growth Trend Evaluation": gdp_growth_trend,
    "Volatility & Extremes": gdp_volatility_context,
    "Policy & Sentiment Shifts": yoy_vs_average_signal
}

# -------------------------------------------------------------------------------------------------
# Nominal GDP Indicator Logic
# -------------------------------------------------------------------------------------------------
def nominal_gdp_size_signal(df, period=4):
    """
    Evaluates headline nominal GDP value relative to historic highs/lows.

    Returns:
        str: Market size signal.
    """
    if df is None or "Nominal GDP" not in df.columns:
        return "Insufficient Data"
    series = df["Nominal GDP"].dropna()
    if series.empty or len(series) < period:
        return "Insufficient Data"
    latest = series.iloc[-1]
    max_val = series.max()
    min_val = series.min()
    if latest >= 0.97 * max_val:
        return "Near Historic High"
    if latest <= 1.03 * min_val:
        return "Near Historic Low"
    return "Within Normal Range"


def nominal_trend_consistency(df, period=4):
    """
    Measures volatility in recent nominal GDP growth.

    Returns:
        str: Signal indicating growth consistency.
    """
    if df is None or "Nominal GDP" not in df.columns:
        return "Insufficient Data"
    series = df["Nominal GDP"].dropna()
    if series.empty or len(series) < period:
        return "Insufficient Data"
    pct_changes = series.pct_change().dropna()
    if len(pct_changes) < 2:
        return "Insufficient Data"
    std_dev = pct_changes.std()
    if std_dev < 0.01:
        return "Stable Nominal Growth"
    if std_dev > 0.03:
        return "Volatile Nominal Trend"
    return "Moderate Nominal Variation"


def nominal_growth_vs_real(df, period=4):
    """
    Compares nominal and real GDP growth to infer price-driven trends.

    Returns:
        str: Signal showing nominal vs real divergence.
    """
    if df is None or "Nominal GDP" not in df.columns or "Real GDP (Level)" not in df.columns:
        return "Insufficient Data"
    nominal = df["Nominal GDP"].dropna()
    real = df["Real GDP (Level)"].dropna()
    if nominal.empty or real.empty or len(nominal) < period or len(real) < period:
        return "Insufficient Data"
    nominal_growth = nominal.pct_change().mean()
    real_growth = real.pct_change().mean()
    if pd.isna(nominal_growth) or pd.isna(real_growth):
        return "Insufficient Data"
    diff = nominal_growth - real_growth
    if diff > 0.01:
        return "Price-Led Growth"
    if diff < -0.01:
        return "Real-Driven Growth"
    return "Balanced Growth"


options_nominal_gdp_map = {
    "Absolute Market Size": nominal_gdp_size_signal,
    "Currency Sensitivity Signals": nominal_growth_vs_real,
    "Policy Normalization Dynamics": nominal_trend_consistency
}

# -------------------------------------------------------------------------------------------------
# GDP Component Indicator Logic
# -------------------------------------------------------------------------------------------------
def gdp_domestic_composition(df, period=4):
    """
    Assesses dominant contributor among personal consumption,
    private investment, and government spending.

    Returns:
        str: Dominance classification.
    """
    cols = [
        "Real Personal Consumption Expenditures",
        "Real Gross Private Domestic Investment",
        "Government Consumption Expenditures and Gross Investment"
    ]
    if not all(col in df.columns for col in cols):
        return "Insufficient Data"
    recent = df[cols].dropna().tail(period)
    if recent.empty or len(recent) < period:
        return "Insufficient Data"
    avg = recent.mean()
    dominant = avg.idxmax()
    share = avg[dominant] / avg.sum()
    if share >= 0.5:
        return f"{_normalize_label(dominant)} Dominant"
    if share <= 0.35:
        return "Broadly Balanced"
    return f"{_normalize_label(dominant)} Leading"

def gdp_trade_contribution_signal(df, period=4):
    """
    Evaluates trade contribution balance to GDP.

    Returns:
        str: Trade surplus, deficit, or balanced.
    """
    required = [
        "Real Exports of Goods and Services",
        "Real Imports of Goods and Services"
    ]
    if not all(col in df.columns for col in required):
        return "Insufficient Data"
    exports = df[required[0]].dropna()
    imports = df[required[1]].dropna()
    if exports.empty or imports.empty or len(exports) < period or len(imports) < period:
        return "Insufficient Data"
    avg_export = exports.tail(period).mean()
    avg_import = imports.tail(period).mean()
    if abs(avg_export - avg_import) / max(avg_export, avg_import) < 0.05:
        return "Balanced Trade"
    if avg_export > avg_import:
        return "Net Trade Surplus"
    return "Net Trade Deficit"


def gdp_structural_trend_shift(df, period=4):
    """
    Measures variability in GDP component growth to flag structural change.

    Returns:
        str: Degree of compositional shift.
    """
    components = [
        "Real Personal Consumption Expenditures",
        "Real Gross Private Domestic Investment",
        "Government Consumption Expenditures and Gross Investment",
        "Real Exports of Goods and Services"
    ]
    if not all(col in df.columns for col in components):
        return "Insufficient Data"
    recent = df[components].dropna().tail(period)
    if recent.empty or len(recent) < period:
        return "Insufficient Data"
    std_dev = recent.pct_change().std()
    mean_std = std_dev.mean()
    if mean_std < 0.015:
        return "Stable Composition"
    if mean_std > 0.035:
        return "Component Shifts Detected"
    return "Moderate Composition Variation"


def _normalize_label(label):
    """
    Converts technical column labels to readable segments.

    Returns:
        str: Simplified label for display.
    """
    if "Consumption" in label:
        return "Personal Consumption"
    if "Private" in label:
        return "Private Investment"
    if "Government" in label:
        return "Government"
    return "Other"


options_gdp_components_map = {
    "Consumption vs Investment vs Government": gdp_domestic_composition,
    "Export-Import Divergence": gdp_trade_contribution_signal,
    "Structural Demand Trends": gdp_structural_trend_shift
}
