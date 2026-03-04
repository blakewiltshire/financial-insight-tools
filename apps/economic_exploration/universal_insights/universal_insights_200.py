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
# Insight Mapping
# -------------------------------------------------------------------------------------------------
insights = {
    # Employment Trends
    "Job Creation Momentum": {
        "Strong Momentum": {
            "bias": "Growth Supportive",
            "text": "Recent job creation significantly exceeds historical trends—consistent with stronger labour demand."
        },
        "Weak or Reversing": {
            "bias": "Contraction Warning",
            "text": "Employment growth is fading or negative—consistent with softer labour demand or rising macro friction."
        },
        "Neutral Hiring Trend": {
            "bias": "Neutral",
            "text": "Hiring trends are aligned with long-term norms—no strong signal of acceleration or reversal."
        }
    },
    "Volatility in Hiring Activity": {
        "Volatile Hiring Patterns": {
            "bias": "Contraction Warning",
            "text": "Employment changes are erratic—may reflect business uncertainty or fragile labour dynamics."
        },
        "Stable Employment Growth": {
            "bias": "Growth Supportive",
            "text": "Hiring appears consistent and stable—supports continued macro resilience."
        },
        "Moderate Volatility": {
            "bias": "Neutral",
            "text": "Some variability in employment, but not extreme—conditions remain broadly steady."
        }
    },
    "Cyclical Turning Points": {
        "Turning Positive": {
            "bias": "Growth Supportive",
            "text": "Employment growth has shifted from decline to expansion—potential early change in direction."
        },
        "Turning Negative": {
            "bias": "Contraction Warning",
            "text": "Employment momentum has shifted from growth to contraction—potential loss of labour market momentum."
        },
        "No Recent Inflection": {
            "bias": "Neutral",
            "text": "Employment growth direction is stable—no inflection signal currently detected."
        }
    },

    # Unemployment Context
    "Unemployment Shifts": {
        "Unemployment Rising": {
            "bias": "Contraction Warning",
            "text": "Unemployment is rising—may reflect declining labour demand or macro stress."
        },
        "Unemployment Falling": {
            "bias": "Growth Supportive",
            "text": "Unemployment is declining—labour market is tightening and employment is improving."
        },
        "Unchanged": {
            "bias": "Neutral",
            "text": "Unemployment rate has not changed—trend direction is indeterminate."
        }
    },
    "Stress or Slack Indicators": {
        "Near Cycle Low": {
            "bias": "Growth Supportive",
            "text": "Unemployment is near cyclical lows—indicates strong hiring and minimal slack."
        },
        "Near Cycle High": {
            "bias": "Contraction Warning",
            "text": "Unemployment is near recent highs—consistent with elevated labour slack."
        },
        "Mid-Range Level": {
            "bias": "Neutral",
            "text": "Unemployment remains in a mid-range band—no extreme stress or tightness detected."
        }
    },
    "Reversion from Extremes": {
        "Unemployment Volatility Elevated": {
            "bias": "Contraction Warning",
            "text": "Unemployment readings have become more volatile—macro or sectoral risk may be rising."
        },
        "Stable Unemployment Readings": {
            "bias": "Growth Supportive",
            "text": "Unemployment variability is low—labour conditions appear well-anchored."
        },
        "Moderate Volatility": {
            "bias": "Neutral",
            "text": "Some fluctuation in unemployment, but not extreme—conditions moderately stable."
        }
    },

    # Labour Force Engagement
    "Participation Stability": {
        "Participation Increasing": {
            "bias": "Growth Supportive",
            "text": "More individuals are entering or remaining in the workforce—consistent with stronger labour engagement and output capacity."
        },
        "Participation Declining": {
            "bias": "Contraction Warning",
            "text": "Participation is falling—may reflect discouragement, demographic drag, or long-run disengagement."
        },
        "Stable Engagement": {
            "bias": "Neutral",
            "text": "Participation is steady—no strong directional signal in workforce engagement."
        }
    },
    "Demographic or Structural Shifts": {
        "Structural Shifts Detected": {
            "bias": "Contraction Warning",
            "text": "Volatility in participation rates may reflect structural realignment or systemic disengagement."
        },
        "Stable Participation Rate": {
            "bias": "Growth Supportive",
            "text": "Participation patterns are consistent—demographic and structural foundations remain stable."
        },
        "Mild Variability": {
            "bias": "Neutral",
            "text": "Some variation in participation behaviour—could reflect seasonal or temporary factors."
        }
    },
    "Engagement Trend Change": {
        "Near Multi-Year High": {
            "bias": "Growth Supportive",
            "text": "Labour participation is near its highest level in recent years—indicates broad inclusion and economic pull."
        },
        "Near Multi-Year Low": {
            "bias": "Contraction Warning",
            "text": "Participation is near a multi-year low—structural disengagement or demographic softness may be present."
        },
        "Mid-Cycle Engagement Level": {
            "bias": "Neutral",
            "text": "Participation sits within typical multi-year range—no strong signal in either direction."
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
