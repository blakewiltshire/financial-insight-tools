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
# Insight Map with Embedded Bias Labels (Neutral Format)
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Insight Map
# -------------------------------------------------------------------------------------------------
insights = {
    "Consumer Price Pressure": {
        "Consumer Inflationary Pressure": {
            "bias": "Contraction Warning",
            "text": "Consumer price pressures are building, suggesting broader inflationary "
            "conditions across household goods, services, and cost-of-living sensitive areas."
        },
        "Consumer Prices Stable": {
            "bias": "Neutral",
            "text": "Consumer prices are broadly stable relative to recent levels, indicating "
            "no material shift in headline inflation pressure at present."
        },
        "Consumer Deflationary Pressure": {
            "bias": "Growth Supportive",
            "text": "Consumer prices are easing relative to recent levels, suggesting "
            "deflationary pressure or temporary relief across consumer-facing costs."
        }
    },

    "Core Consumer Inflation": {
        "Core Inflation Firm": {
            "bias": "Contraction Warning",
            "text": "Core consumer inflation remains firm, suggesting underlying price "
            "pressures remain embedded beyond short-term volatility."
        },
        "Core Inflation Stable": {
            "bias": "Neutral",
            "text": "Core consumer inflation is broadly stable, indicating that underlying "
            "price persistence is holding within recent norms."
        },
        "Core Inflation Softening": {
            "bias": "Growth Supportive",
            "text": "Core consumer inflation is softening, suggesting underlying price "
            "pressures may be moderating across the wider system."
        }
    },

    "Producer Price Pressure": {
        "Producer Inflationary Pressure": {
            "bias": "Contraction Warning",
            "text": "Producer price pressures are rising, suggesting increased upstream "
            "input costs and potential transmission into downstream pricing."
        },
        "Producer Prices Stable": {
            "bias": "Neutral",
            "text": "Producer prices are broadly stable, indicating limited recent change "
            "in upstream pricing conditions."
        },
        "Producer Deflationary Pressure": {
            "bias": "Growth Supportive",
            "text": "Producer prices are easing, suggesting reduced upstream cost pressure "
            "and potential relief in future price transmission."
        }
    },

    "Core Producer Inflation": {
        "Core Producer Inflation Firm": {
            "bias": "Contraction Warning",
            "text": "Core producer inflation remains firm, suggesting underlying upstream "
            "cost pressures remain embedded within the production chain."
        },
        "Core Producer Inflation Stable": {
            "bias": "Neutral",
            "text": "Core producer inflation is broadly stable, indicating that underlying "
            "production cost pressure is holding near recent norms."
        },
        "Core Producer Inflation Softening": {
            "bias": "Growth Supportive",
            "text": "Core producer inflation is softening, suggesting upstream cost "
            "pressures may be easing within the production system."
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
