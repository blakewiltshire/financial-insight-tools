# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Insight Map — Structured Narrative Layer (Theme-Independent Template)
-------------------------------------------------------------------------------

This module defines universal, plain-language insights and bias classifications for system-wide
macroeconomic signals. It serves as the primary interpretive layer supporting AI narratives,
insight panels, macro alignment scoring, and external DSS agents.

System Role:
- Delivers standardised insight text and directional bias for all signals across themes
- Supports AI export narratives, scoring overlays, and structured observation pipelines
- Used automatically when no local override is present in `insight_XXX.py` modules

AI Persona Alignment Notes:
- Insight functions return:
    • Textual insight strings (e.g., "Growth remains above trend")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona reflection and export modules

System Structure & Compatibility:
**Strict String Matching**
    - Signal names must match exactly the outputs from `indicator_map_XXX.py` functions.
    - No inference or dynamic mapping allowed.

**Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`
    (or approved equivalents)

**Dispatcher Consistency**
    - Interface includes:
        - `indicator` (signal key)
        - `value` (signal string)
        - `timeframe` (pass-through parameter)
        - `extra_value` (optional; unused for universal module but preserved for
        interface consistency)

**No Embedded Logic**
    - This module performs no calculations or evaluations.
    - All inputs are fully processed signal strings passed from upstream evaluation logic.

Governance Note:
- This universal insight map is system-stable and globally applied.
- Country-specific or theme-specific extensions occur via local `insight_XXX.py` files only.
"""

# -------------------------------------------------------------------------------------------------
# Insight Map
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Insight Map
# -------------------------------------------------------------------------------------------------
insights = {
    "Currency Strength Position": {
        "Currency Pressure Rising": {
            "bias": "Contraction Warning",
            "text": "The trade-weighted currency index is strengthening relative to recent levels, "
            "suggesting firmer exchange pressure and a potentially more restrictive external backdrop."
        },
        "Currency Pressure Stable": {
            "bias": "Neutral",
            "text": "The trade-weighted currency index is broadly stable, indicating limited recent "
            "change in overall exchange pressure conditions."
        },
        "Currency Pressure Easing": {
            "bias": "Growth Supportive",
            "text": "The trade-weighted currency index is softening relative to recent levels, "
            "suggesting some easing in exchange pressure across the wider currency regime."
        }
    },

    "Reserve Stability Conditions": {
        "Reserve Position Strengthening": {
            "bias": "Growth Supportive",
            "text": "Official reserves excluding gold are improving relative to recent norms, "
            "suggesting a somewhat stronger reserve stability backdrop."
        },
        "Reserve Position Stable": {
            "bias": "Neutral",
            "text": "Official reserves excluding gold are broadly stable, indicating limited "
            "recent change in reserve conditions."
        },
        "Reserve Position Softening": {
            "bias": "Contraction Warning",
            "text": "Official reserves excluding gold are weakening relative to recent norms, "
            "which may indicate softer reserve stability conditions."
        }
    },

    "Current Account Support": {
        "External Balance Support Improving": {
            "bias": "Growth Supportive",
            "text": "The current account position is improving relative to recent norms, "
            "suggesting stronger external balance support within the currency regime."
        },
        "External Balance Support Stable": {
            "bias": "Neutral",
            "text": "The current account position is broadly stable, indicating limited recent "
            "change in external balance support."
        },
        "External Balance Support Weakening": {
            "bias": "Contraction Warning",
            "text": "The current account position is weakening relative to recent norms, which "
            "may indicate softer external balance support across the regime structure."
        }
    },
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
