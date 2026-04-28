# -------------------------------------------------------------------------------------------------
# Insight Generator (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Insight Map — Country-Specific Narrative Extensions
-------------------------------------------------------------------------------

This module defines localised insight narratives and bias classifications for country-level
customisation within the Economic Exploration suite. It allows country-specific or theme-specific
extensions to the system-wide universal insight map.

System Role:
- Provides extended or overridden insight text for local indicators
- Supports AI narratives, macro scoring, observation journals, and external DSS agents
- Used when local indicators exist or where country-level nuance is required

AI Persona Alignment Notes:
- Insight mappings return:
    • Textual insight strings (e.g., "Full-time employment is leading expansion")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Contraction Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona export narratives

System Structure & Compatibility:
**Strict Key Matching**
    - Keys must match exactly the signal output strings from `indicator_map_XXX.py`
    - Any sector-level tuple disaggregation handled upstream before calling insights

**Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`, `"Caution"`

**String-Based Substitution Only**
    - Text templates may include `{sector}` or `{value}` placeholders if dynamic context is passed
    - No numeric payloads returned — insight output always resolves to pure
    text + bias classification

**Dispatcher Consistency**
    - Interface includes:
        - `indicator` (use case signal)
        - `signal_result` (strict string match)
        - `timeframe` (pass-through)
        - `extra_value` (optional sector string substitution where applicable)

**No Embedded Evaluation Logic**
    - This module performs no calculations.
    - All logic and signal evaluation occurs upstream in indicator map functions.

Governance Note:
- This local insight map overrides universal logic where defined.
- If no local match exists, the system falls back automatically to `universal_insights_XXX.py`.
- This ensures full global-local modular consistency across countries and themes.
"""

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_insights"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_insights_100 import generate_universal_econ_insights

# -------------------------------------------------------------------------------------------------
# Local Insight Definitions (Bias + Text)
# -------------------------------------------------------------------------------------------------
LOCAL_INSIGHTS = {
    "Leading Economic Index (Conference Board)": {
        "Uptrend Confirmed": {
            "bias": "Growth Supportive",
            "text": "The Leading Growth Index is trending higher—signals possible expansionary phase ahead."
        },
        "Downtrend Confirmed": {
            "bias": "Contraction Warning",
            "text": "Leading indicators are weakening—suggests potential macroeconomic deceleration."
        },
        "Flat or Reversing": {
            "bias": "Neutral",
            "text": "Composite signals appear directionless or reversing—indicates uncertainty in forward trajectory."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Leading Growth Index signal could not be generated—check data completeness."
        }
    },
    "Weekly Economic Index (NY Fed)": {
        "Momentum Strengthening": {
            "bias": "Growth Supportive",
            "text": "Weekly Economic Index shows rising momentum—near-term conditions are improving."
        },
        "Momentum Weakening": {
            "bias": "Contraction Warning",
            "text": "Recent weekly trends are softening—suggests growth moderation or volatility."
        },
        "Stagnant or Mixed": {
            "bias": "Neutral",
            "text": "Weekly signals are flat or mixed—near-term economic bias unclear."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Weekly index data unavailable or incomplete—signal cannot be derived."
        }
    },
    "Uncertainty Index Impact": {
        "High Volatility Risk": {
            "bias": "Contraction Warning",
            "text": "Economic uncertainty has surged—may increase regime instability and reduce forward visibility."
        },
        "Moderate Uncertainty": {
            "bias": "Neutral",
            "text": "Uncertainty indicators are elevated but stable—can signal caution or delay in business/policy decisions."
        },
        "Low Uncertainty Environment": {
            "bias": "Growth Supportive",
            "text": "Uncertainty measures remain subdued—suggests stable sentiment and clearer economic expectations."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "Uncertainty index signal unavailable—data insufficient."
        }
    },
    "National Activity Composite": {
        "Above Trend Activity": {
            "bias": "Growth Supportive",
            "text": "National Activity Index indicates above-trend economic strength—broad-based improvement across sectors."
        },
        "Below Trend Activity": {
            "bias": "Contraction Warning",
            "text": "Activity index shows below-trend conditions—broad economic momentum may be weakening."
        },
        "Near Neutral Benchmark": {
            "bias": "Neutral",
            "text": "Activity is consistent with long-term trend—macro pressures appear balanced."
        },
        "Insufficient Data": {
            "bias": "Neutral",
            "text": "National Activity Index data insufficient for meaningful signal."
        }
    }
}

# -------------------------------------------------------------------------------------------------
# Dispatcher — Universal Fallback with Local Override
# -------------------------------------------------------------------------------------------------
def generate_econ_insights(indicator: str, signal_result: str, timeframe: str, extra_value=None) -> tuple[str, str]:
    """
    Local-first insight generator — falls back to universal if no local match found.
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

    # Always fall back to universal
    return generate_universal_econ_insights(indicator, signal_result, timeframe, extra_value)
