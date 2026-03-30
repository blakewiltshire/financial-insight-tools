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
    "Forward Production Conditions": {
        "Indicators": [
            "Business Conditions",
            "Production Activity",
            "Demand Transmission"
        ],
        "Categories": [
            "Business Conditions",
            "Production",
            "Demand"
        ],
        "Description": "Examines how forward production conditions emerge through the interaction of business sentiment, industrial output, and order-based demand signals."
    },
    "Services Activity Conditions": {
        "Indicators": [
            "Business Conditions",
            "Services Consumption",
            "Real Services Demand"
        ],
        "Categories": [
            "Business Conditions",
            "Services Consumption",
            "Real Demand"
        ],
        "Description": "Examines how services activity conditions emerge through the interaction of business sentiment, nominal consumption trends, and real consumer demand."
    }
}


def get_use_cases():
    """
    Returns the configured use case structure for forward production and services activity conditions.

    Returns:
        dict: Use cases for UI and structural fallback.
    """
    return USE_CASES
