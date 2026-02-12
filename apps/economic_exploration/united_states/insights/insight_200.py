# -------------------------------------------------------------------------------------------------
# 🧠 Insight Generator (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧠 Local Insight Map — Country-Specific Narrative Extensions
-------------------------------------------------------------------------------

This module defines localised insight narratives and bias classifications for country-level
customisation within the Economic Exploration suite. It allows country-specific or theme-specific
extensions to the system-wide universal insight map.

✅ System Role:
- Provides extended or overridden insight text for local indicators
- Supports AI narratives, macro scoring, observation journals, and external DSS agents
- Used when local indicators exist or where country-level nuance is required

🧠 AI Persona Alignment Notes:
- Insight mappings return:
    • Textual insight strings (e.g., "Full-time employment is leading expansion")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Contraction Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona export narratives

⚙️ System Structure & Compatibility:
1️⃣ **Strict Key Matching**
    - Keys must match exactly the signal output strings from `indicator_map_XXX.py`
    - Any sector-level tuple disaggregation handled upstream before calling insights

2️⃣ **Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`, `"Caution"`

3️⃣ **String-Based Substitution Only**
    - Text templates may include `{sector}` or `{value}` placeholders if dynamic context is passed
    - No numeric payloads returned — insight output always resolves to pure
    text + bias classification

4️⃣ **Dispatcher Consistency**
    - Interface includes:
        - `indicator` (use case signal)
        - `signal_result` (strict string match)
        - `timeframe` (pass-through)
        - `extra_value` (optional sector string substitution where applicable)

5️⃣ **No Embedded Evaluation Logic**
    - This module performs no calculations.
    - All logic and signal evaluation occurs upstream in indicator map functions.

🧭 Governance Note:
- This local insight map overrides universal logic where defined.
- If no local match exists, the system falls back automatically to `universal_insights_XXX.py`.
- This ensures full global-local modular consistency across countries and themes.
"""

# -------------------------------------------------------------------------------------------------
# 📦 Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_insights"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 🔀 Universal Insight Import
# -------------------------------------------------------------------------------------------------
from universal_insights_200 import generate_universal_econ_insights

# -------------------------------------------------------------------------------------------------
# 🔠 Local Labour Market Insights Map (String-Matching Strict)
# -------------------------------------------------------------------------------------------------

LOCAL_INSIGHTS = {
    # --- Business Sector Employment Breakdown ---
    "Business Sector Employment Breakdown – Momentum": {
        "Sector Momentum": {
            "bias": "Growth Supportive",
            "text": "Hiring momentum is strongest in the {sector} sector — positive labour market signal."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data to detect sector momentum."
        }
    },
    "Business Sector Employment Breakdown – Stress": {
        "Sector Stress": {
            "bias": "Contraction Warning",
            "text": "The {sector} sector shows the largest decline in hiring — cyclical weakness emerging."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data to detect sector stress."
        }
    },
    "Business Sector Employment Breakdown – Summary": {
        "Sector Summary": {
            "bias": "Neutral",
            "text": "Average sector hiring change stands at {value}k jobs/month."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Sector summary calculation unavailable due to missing data."
        }
    },

    # --- Full-Time vs Part-Time Employment ---
    "Employment Type Balance": {
        "Minimal Shift": {
            "bias": "Neutral",
            "text": "No significant shifts between full-time and part-time hiring."
        },
        "Full-Time Leading": {
            "bias": "Growth Supportive",
            "text": "Full-time employment is leading recent labour market expansion."
        },
        "Part-Time Leading": {
            "bias": "Caution",
            "text": "Part-time roles are driving recent job creation — possible underemployment risk."
        },
        "Indeterminate": {
            "bias": "Neutral",
            "text": "Employment type trends are mixed or ambiguous."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data for employment type balance signal."
        }
    },
    "Part-Time Employment Stress": {
        "Part-Time Surge": {
            "bias": "Contraction Warning",
            "text": "Part-time employment surged — potential signal of labour market stress."
        },
        "Stable": {
            "bias": "Neutral",
            "text": "Part-time employment changes are stable."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data for part-time employment stress signal."
        }
    },
    "Employment Quality Shift": {
        "Part-Time Replacing Full-Time": {
            "bias": "Contraction Warning",
            "text": "Full-time employment is falling while part-time rises — possible sign of hidden underemployment."
        },
        "Both Expanding": {
            "bias": "Growth Supportive",
            "text": "Both full-time and part-time employment are expanding — broad-based labour market growth."
        },
        "Both Contracting": {
            "bias": "Contraction Warning",
            "text": "Both full-time and part-time employment are declining — broad-based contraction."
        },
        "Stable or Mixed": {
            "bias": "Neutral",
            "text": "Full-time and part-time employment show stable or mixed conditions."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data for employment quality shift signal."
        }
    },

    # --- Average Hourly Earnings ---
    "Wage Growth Trend": {
        "Wage Acceleration": {
            "bias": "Growth Supportive",
            "text": "Wage growth accelerating — supports income growth dynamics."
        },
        "Wage Deceleration": {
            "bias": "Contraction Warning",
            "text": "Wage momentum decelerating — may reflect softening demand."
        },
        "Stagnant Wages": {
            "bias": "Neutral",
            "text": "Wage conditions remain stagnant."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient wage data to derive earnings signal."
        }
    },

    # --- Jobless Claims ---
    "Initial Jobless Claims": {
        "Initial Claims Surge": {
            "bias": "Contraction Warning",
            "text": "Initial claims spiked — elevated job market stress emerging."
        },
        "Stable": {
            "bias": "Neutral",
            "text": "Initial jobless claims remain stable."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data for initial claims signal."
        }
    },
    "Continued Jobless Claims": {
        "Continued Claims Rising": {
            "bias": "Contraction Warning",
            "text": "Continued claims rising — elevated long-term unemployment pressure."
        },
        "Improving Conditions": {
            "bias": "Growth Supportive",
            "text": "Continued claims improving — stronger rehiring dynamics."
        },
        "Flat Trend": {
            "bias": "Neutral",
            "text": "Continued claims trend stable."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Insufficient data for continued claims signal."
        }
    }
}

# -------------------------------------------------------------------------------------------------
# 🔄 Dispatcher — Local First, Fallback to Universal
# -------------------------------------------------------------------------------------------------
def generate_econ_insights(indicator: str, signal_result: str, timeframe: str, extra_value=None) -> tuple[str, str]:
    """
    Returns (insight text, bias classification) for given indicator and signal.
    """
    local_map = LOCAL_INSIGHTS.get(indicator, {})
    if signal_result in local_map:
        entry = local_map[signal_result]
        text_template = entry["text"]

        if "{sector}" in text_template and extra_value:
            text_final = text_template.replace("{sector}", str(extra_value))
        elif "{value}" in text_template and extra_value is not None:
            try:
                text_final = text_template.replace("{value}", f"{extra_value:.2f}")
            except:
                text_final = text_template
        else:
            text_final = text_template

        return text_final, entry["bias"]

    return generate_universal_econ_insights(indicator, signal_result, timeframe)
