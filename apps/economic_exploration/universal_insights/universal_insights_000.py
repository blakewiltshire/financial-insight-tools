# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧠 Universal Insight Map — Structured Narrative Layer (Theme-Independent Template)
-------------------------------------------------------------------------------

This module defines universal, plain-language insights and bias classifications for system-wide
macroeconomic signals. It serves as the primary interpretive layer supporting AI narratives,
insight panels, macro alignment scoring, and external DSS agents.

✅ System Role:
- Delivers standardised insight text and directional bias for all signals across themes
- Supports AI export narratives, scoring overlays, and structured observation pipelines
- Used automatically when no local override is present in `insight_XXX.py` modules

🧠 AI Persona Alignment Notes:
- Insight functions return:
    • Textual insight strings (e.g., "Growth remains above trend")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona reflection and export modules

⚙️ System Structure & Compatibility:
1️⃣ **Strict String Matching**
    - Signal names must match exactly the outputs from `indicator_map_XXX.py` functions.
    - No inference or dynamic mapping allowed.

2️⃣ **Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`
    (or approved equivalents)

3️⃣ **Dispatcher Consistency**
    - Interface includes:
        - `indicator` (signal key)
        - `value` (signal string)
        - `timeframe` (pass-through parameter)
        - `extra_value` (optional; unused for universal module but preserved for
        interface consistency)

4️⃣ **No Embedded Logic**
    - This module performs no calculations or evaluations.
    - All inputs are fully processed signal strings passed from upstream evaluation logic.

🧭 Governance Note:
- This universal insight map is system-stable and globally applied.
- Country-specific or theme-specific extensions occur via local `insight_XXX.py` files only.
"""


# -------------------------------------------------------------------------------------------------
# Insight Map with Embedded Bias Labels (Neutral Format)
# -------------------------------------------------------------------------------------------------
insights = {
    "001_signal_a": {
        "Signal A1": {
            "bias": "Supportive",
            "text": "Condition A1 indicates favourable alignment or constructive trend development."
        },
        "Signal A2": {
            "bias": "Warning",
            "text": "Condition A2 may reflect weakening fundamentals or emerging headwinds."
        },
        "Signal A3": {
            "bias": "Neutral",
            "text": "Condition A3 is broadly consistent with past norms or indecisive behaviour."
        }
    },
    "002_signal_b": {
        "Signal B1": {
            "bias": "Supportive",
            "text": "Signal B1 suggests directional strength and alignment with key drivers."
        },
        "Signal B2": {
            "bias": "Warning",
            "text": "Signal B2 may indicate volatility, reversals, or structural dislocations."
        },
        "Signal B3": {
            "bias": "Neutral",
            "text": "Signal B3 reflects stable or muted momentum — further monitoring warranted."
        }
    },
    "003_signal_c": {
        "Signal C1": {
            "bias": "Supportive",
            "text": "Outcome C1 supports confidence in sustained directional positioning."
        },
        "Signal C2": {
            "bias": "Warning",
            "text": "Outcome C2 reflects divergence or inconsistency across components."
        },
        "Signal C3": {
            "bias": "Neutral",
            "text": "Outcome C3 remains within expected bounds — no actionable divergence noted."
        }
    }
}

# -------------------------------------------------------------------------------------------------
# Dispatcher Function
# -------------------------------------------------------------------------------------------------
def generate_universal_econ_insights(indicator: str, value: str, timeframe: str, extra_value=None) -> tuple[str, str]:
    """
    Returns universal insight text and bias classification for a given indicator signal.

    Parameters:
        indicator (str): Indicator key
        value (str): Signal output string (strict string match)
        timeframe (str): Timeframe (pass-through)
        extra_value: (optional, unused for universal, provided for interface compatibility)

    Returns:
        tuple[str, str]: (Insight narrative, bias classification)
    """
    try:
        data = insights[indicator][value]
        return data["text"], data.get("bias", "Neutral")
    except Exception:
        return "No insight available for this signal.", "Neutral"
