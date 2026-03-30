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
# Insight Map with Embedded Bias Labels
# -------------------------------------------------------------------------------------------------
insights = {
    "Business Conditions": {
        "Business Conditions Strengthening": {
            "bias": "Growth Supportive",
            "text": "Business conditions are strengthening relative to recent observations, suggesting firmer industrial sentiment and a more supportive forward backdrop for production activity."
        },
        "Business Conditions Weakening": {
            "bias": "Contraction Warning",
            "text": "Business conditions are weakening relative to recent observations, suggesting softer industrial sentiment and a less supportive forward backdrop for production activity."
        },
        "Business Conditions Stable": {
            "bias": "Neutral",
            "text": "Business conditions remain broadly stable relative to recent observations, suggesting limited change in the underlying tone of forward production expectations."
        }
    },

    "Production Activity": {
        "Production Activity Improving": {
            "bias": "Growth Supportive",
            "text": "Industrial production is improving relative to recent trends, indicating firmer realised output across production systems and stronger confirmation of underlying activity."
        },
        "Production Activity Softening": {
            "bias": "Contraction Warning",
            "text": "Industrial production is softening relative to recent trends, indicating reduced output momentum and weaker confirmation of current production conditions."
        },
        "Production Activity Stable": {
            "bias": "Neutral",
            "text": "Industrial production remains broadly stable relative to recent trends, suggesting that realised output conditions are holding without marked acceleration or decline."
        }
    },

    "Demand Transmission": {
        "Demand Reinforcing": {
            "bias": "Growth Supportive",
            "text": "Manufacturing durable goods orders are reinforcing recent conditions, suggesting underlying demand is supporting forward production activity and helping sustain transmission into output."
        },
        "Demand Weakening": {
            "bias": "Contraction Warning",
            "text": "Manufacturing durable goods orders are weakening relative to recent trends, suggesting softer demand transmission and less reinforcement for current production conditions."
        },
        "Demand Stable": {
            "bias": "Neutral",
            "text": "Manufacturing durable goods orders remain broadly stable relative to recent trends, indicating limited change in order-based demand conditions."
        }
    },

    "Services Consumption": {
        "Services Consumption Strengthening": {
            "bias": "Growth Supportive",
            "text": "Nominal services consumption is strengthening relative to recent observations, suggesting firmer consumer-facing demand and improving activity conditions across the services layer."
        },
        "Services Consumption Weakening": {
            "bias": "Contraction Warning",
            "text": "Nominal services consumption is weakening relative to recent observations, suggesting softer consumer-facing demand and less support for current services activity conditions."
        },
        "Services Consumption Stable": {
            "bias": "Neutral",
            "text": "Nominal services consumption remains broadly stable relative to recent observations, indicating limited change in consumer-facing spending conditions."
        }
    },

    "Real Services Demand": {
        "Real Demand Strengthening": {
            "bias": "Growth Supportive",
            "text": "Real services demand is strengthening relative to recent observations, suggesting underlying consumer activity is improving after the effects of price changes are removed."
        },
        "Real Demand Weakening": {
            "bias": "Contraction Warning",
            "text": "Real services demand is weakening relative to recent observations, suggesting underlying consumer activity is softening once price effects are removed."
        },
        "Real Demand Stable": {
            "bias": "Neutral",
            "text": "Real services demand remains broadly stable relative to recent observations, indicating limited change in the underlying pace of consumer activity."
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
        indicator (str): Indicator label from the selected indicator map
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
