# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧩 Universal Use Case Definitions — Economic Exploration Core System
-----------------------------------------------------------------------

This module defines the default universal use case mappings for thematic modules within
the Economic Exploration suite. It governs UI structure, scoring alignment, and AI-supported
framing for any theme not explicitly overridden at country level.

✅ System Role:
- Supplies standardised use case definitions to:
    • Charting engines (tab ordering, dropdown generation)
    • Macro alignment scoring panels
    • AI persona narrative structures and DSS exports
    • Placeholder rendering for unconfigured modules

🧠 AI Persona & DSS Notes:
- Use case keys must match entries used in:
    • `indicator_map_XXX.py`
    • `insight_XXX.py`
    • Scoring alignment modules `scoring_weights_labels_XXX.py`

- Clean, stable, interpretable keys are critical for:
    • AI export narratives
    • Observational journaling
    • Triangular navigation pathways across DSS

⚙️ Structure & Interface Governance:
1️⃣ **Strict Key Consistency**
    - Use case names in this module must exactly match those referenced across indicator maps and insights.

2️⃣ **Indicator Registry**
    - Each use case includes a list of indicator signal labels used for scoring and insight evaluation.
    - These indicators must exist within the corresponding universal indicator maps.

3️⃣ **Metadata Inclusion**
    - Each use case includes:
        - `"Indicators"` → List of signals
        - `"Categories"` → UI grouping tags (used for streamlit tabs, filters)
        - `"Description"` → AI-assist narrative frame

🧭 Governance Note:
- This universal use case map provides system-wide default scaffolding.
- Local overrides per country or theme occur via local `use_cases_XXX.py`.
- No universal entries are modified by users directly — universal remains stable foundation.
"""

# -------------------------------------------------------------------------------------------------
# Use Cases
# -------------------------------------------------------------------------------------------------
USE_CASES = {
    "Real GDP": {
        "Indicators": [
            "Growth Trend Evaluation",
            "Volatility & Extremes",
            "Policy & Sentiment Shifts"
        ],
        "Categories": ["Real GDP"],
        "Description": "Tracks economic expansion/contraction via real GDP, evaluates volatility, \
        and links macro cycles to market sentiment."
    },
    "Nominal GDP": {
        "Indicators": [
            "Absolute Market Size",
            "Currency Sensitivity Signals",
            "Policy Normalization Dynamics"
        ],
        "Categories": ["Nominal GDP"],
        "Description": "Assesses nominal growth potential, implications for monetary policy, and \
        relevance to currency and interest rate expectations."
    },
    "GDP Components Breakdown": {
        "Indicators": [
            "Consumption vs Investment vs Government",
            "Export-Import Divergence",
            "Structural Demand Trends"
        ],
        "Categories": ["GDP Components"],
        "Description": "Deconstructs GDP drivers, highlighting shifts in consumer, business, \
        and external trade contributions."
    }
}

def get_use_cases():
    """
    Return Use cases
    """
    return USE_CASES
