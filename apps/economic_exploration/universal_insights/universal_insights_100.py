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
    "Growth Trend Evaluation": {
        "Accelerating Growth": {
            "bias": "Growth Supportive",
            "text": "Real GDP growth is gaining momentum over recent quarters—suggests improving "
            "macroeconomic conditions."
        },
        "Decelerating Growth": {
            "bias": "Contraction Warning",
            "text": "Real GDP growth is slowing—may indicate early signs of economic softening."
        },
        "Flat or Reversing": {
            "bias": "Neutral",
            "text": "GDP momentum appears stagnant or reversing—watch for shifts in policy or "
            "market expectations."
        }
    },

    "Volatility & Extremes": {
        "Near 12M High": {
            "bias": "Growth Supportive",
            "text": "GDP is approaching its highest level in the past year—could indicate "
            "overheating or rapid expansion."
        },
        "Near 12M Low": {
            "bias": "Contraction Warning",
            "text": "GDP is near its lowest point in the last year—potential signal of "
            "economic distress or contraction."
        },
        "Stable Range": {
            "bias": "Neutral",
            "text": "GDP has remained within a stable range—macro conditions are "
            "relatively consistent."
        }
    },

    "Policy & Sentiment Shifts": {
        "YoY Growth Above Avg": {
            "bias": "Growth Supportive",
            "text": "Year-over-year GDP is exceeding its historical average—positive "
            "for sentiment and long-term confidence."
        },
        "YoY Growth Below Avg": {
            "bias": "Contraction Warning",
            "text": "GDP growth is lagging its average YoY pace—watch for fiscal or "
            "monetary adjustments."
        },
        "Neutral": {
            "bias": "Neutral",
            "text": "GDP growth aligns with historical norms—no major shift in economic "
            "sentiment detected."
        }
    },

    "Absolute Market Size": {
        "Near Historic High": {
            "bias": "Growth Supportive",
            "text": "Nominal GDP is approaching its highest recorded value—signals strong "
            "headline growth and market size expansion."
        },
        "Near Historic Low": {
            "bias": "Contraction Warning",
            "text": "Nominal GDP is near historic lows—may reflect structural weakness "
            "or incomplete recovery."
        },
        "Within Normal Range": {
            "bias": "Neutral",
            "text": "Nominal GDP remains within historical bounds—suggests a steady "
            "economic scale."
        }
    },

    "Currency Sensitivity Signals": {
        "Price-Led Growth": {
            "bias": "Growth Supportive",
            "text": "Nominal growth exceeds real growth—indicative of price-driven "
            "expansion or currency effects."
        },
        "Real-Driven Growth": {
            "bias": "Contraction Warning",
            "text": "Real GDP outpaces nominal—may signal disinflation or externally-driven "
            "real growth."
        },
        "Balanced Growth": {
            "bias": "Growth Supportive",
            "text": "Nominal and real GDP are well-aligned—suggests healthy, inflation-consistent "
            "expansion."
        }
    },

    "Policy Normalisation Dynamics": {
        "Stable Nominal Growth": {
            "bias": "Growth Supportive",
            "text": "Nominal GDP trends are steady—favours gradual policy normalisation and "
            "rate clarity."
        },
        "Volatile Nominal Trend": {
            "bias": "Contraction Warning",
            "text": "Sharp fluctuations in nominal GDP—can complicate policy setting and "
            "forward guidance."
        },
        "Moderate Nominal Variation": {
            "bias": "Neutral",
            "text": "Nominal GDP shows some variability—warrants continued monitoring for "
            "regime shifts."
        }
    },

    "Consumption vs Investment vs Government": {
        "Personal Consumption Dominant": {
            "bias": "Growth Supportive",
            "text": "Household consumption is the leading driver of GDP—implies strength "
            "in domestic demand."
        },
        "Private Investment Dominant": {
            "bias": "Growth Supportive",
            "text": "Capital investment is the key contributor to growth—can support future "
            "productivity but may be volatile."
        },
        "Government Dominant": {
            "bias": "Contraction Warning",
            "text": "Government expenditure is driving GDP—often signals fiscal intervention "
            "or cyclical support."
        },
        "Personal Consumption Leading": {
            "bias": "Growth Supportive",
            "text": "Consumption is leading, but not overwhelmingly dominant—suggests balanced "
            "but consumer-sensitive growth."
        },
        "Private Investment Leading": {
            "bias": "Neutral",
            "text": "Investment is leading but within a balanced profile—may point to "
            "business optimism."
        },
        "Government Leading": {
            "bias": "Contraction Warning",
            "text": "Public spending is contributing notably—monitor sustainability and "
            "policy dependencies."
        },
        "Broadly Balanced": {
            "bias": "Neutral",
            "text": "No single GDP driver dominates—growth is distributed across consumption, "
            "investment, and government sectors."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Data on GDP components is insufficient to determine dominant domestic "
            "contributors."
        }
    },

    "Export-Import Divergence": {
        "Net Trade Surplus": {
            "bias": "Growth Supportive",
            "text": "Exports are outpacing imports—net trade is contributing positively to "
            "overall GDP."
        },
        "Net Trade Deficit": {
            "bias": "Contraction Warning",
            "text": "Imports exceed exports—net trade is weighing on GDP and may reflect "
            "strong domestic demand or weak competitiveness."
        },
        "Balanced Trade": {
            "bias": "Neutral",
            "text": "Exports and imports are relatively balanced—trade is not a major swing "
            "factor in recent GDP changes."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Trade balance could not be assessed due to missing data (e.g., imports)."
        }
    },

    "Structural Demand Trends": {
        "Stable Composition": {
            "bias": "Growth Supportive",
            "text": "GDP components are evolving steadily—suggests a predictable and "
            "consistent demand structure."
        },
        "Moderate Composition Variation": {
            "bias": "Neutral",
            "text": "Some variation in GDP drivers—warrants attention to emerging "
            "sectoral shifts."
        },
        "Component Shifts Detected": {
            "bias": "Contraction Warning",
            "text": "Notable shifts in component contributions—may indicate structural "
            "changes or macro rebalancing."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Component trends could not be evaluated—data may be missing or incomplete."
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
