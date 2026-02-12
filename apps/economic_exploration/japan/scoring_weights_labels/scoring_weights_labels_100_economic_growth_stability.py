# -------------------------------------------------------------------------------------------------
# 📈 Economic Growth Stability — Scoring Label Generator (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# This module provides scoring labels and indicator weightings for the
# Economic Growth Stability theme (Theme 100) within a given country context.
#
# It wraps universal logic with optional local overrides for label phrasing
# or scoring weight adjustments.
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧮 Local Scoring Weights & Alignment Labels — Thematic Module Extension
-----------------------------------------------------------------------

This module defines the country-specific scoring weights and alignment labels
for individual use cases within a given thematic grouping. It extends the universal scoring framework
to account for national context, additional indicators, and refined interpretations.

✅ System Role:
- Provides localised scoring narratives for macro alignment ratios
- Overrides or supplements universal logic as new use cases are added
- Supports fully integrated AI narratives, macro summaries, and DSS scorecards

🧠 AI Persona & DSS Notes:
- Returned labels directly drive AI export summaries, scoring panels, and triangular navigation flows
- Alignment scoring logic remains consistent across themes:
    • ≥ 0.85 → Strong Alignment
    • 0.33–0.85 → Mixed Alignment
    • −0.2–0.33 → Soft Misalignment
    • < −0.2 → Clear Misalignment

⚙️ Structural Governance:
1️⃣ **Label Mapping Dispatcher**
- `get_alignment_score_label(alignment_ratio, use_case)` applies local thresholds per use case.
- Always checks for a local override first, otherwise falls back to the universal dispatcher.

2️⃣ **Indicator Weighting System (Extended)**
- `get_indicator_weight(indicator_name)` returns a 1–3 weight scale per indicator.
- Local weights supplement and merge with the universal indicator weight registry.
- Supports composite macro scoring logic across all scoring layers.

3️⃣ **Interface Consistency**
- Function names and use case names must strictly match:
    • `use_cases_XXX.py`
    • `indicator_map_XXX.py`
    • `insight_XXX.py`
    • Universal scoring contract remains stable — local extensions must integrate seamlessly.

🧭 Governance Note:
- Local scoring files are only created when country-specific indicators or signal groupings exist.
- If no local scoring exists, the universal scoring contract fully governs system operation.
"""

# -------------------------------------------------------------------------------------------------
# 🧱 Standard Library and Pathing
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# 🧭 Path Setup: Add Universal Scoring Module to System Path
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_scoring_labels"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 🔁 Imports: Universal Scoring Logic (Do Not Modify)
# -------------------------------------------------------------------------------------------------
from universal_scoring_weight_labels_100 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)

# -------------------------------------------------------------------------------------------------
# 🏛️ Local Use Case Scoring Labels (Optional)
# -------------------------------------------------------------------------------------------------
# Provide per-use-case override functions here if necessary.
# Structure: { "Use Case Label": function(alignment_ratio) → (label, explanation) }

USE_CASE_SCORING_LABELS = {
    # "Real GDP": lambda ratio: ("⚠️ Custom Label", "Custom Explanation...")
}

# -------------------------------------------------------------------------------------------------
# 🧩 Dispatcher — Local First, Fallback to Universal
# -------------------------------------------------------------------------------------------------
def get_alignment_score_label(alignment_ratio: float, use_case: str) -> tuple[str, str]:
    """
    Returns a summary label and explanation for the computed macro alignment score.

    Priority:
    1. Local label function override
    2. Universal fallback

    Args:
        alignment_ratio (float): Score ratio (0.0–1.0)
        use_case (str): Use case label (e.g., "Real GDP")

    Returns:
        tuple[str, str]: (Short label with emoji, Long-form explanation)
    """
    if use_case in USE_CASE_SCORING_LABELS:
        return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)
    return get_alignment_score_label_universal(alignment_ratio, use_case)

# -------------------------------------------------------------------------------------------------
# ⚖️ Indicator Weights (Merged: Universal + Local Overrides)
# -------------------------------------------------------------------------------------------------
# Local weight overrides (if any)
indicator_weights = {
    # Example: "Real GDP": 2,
}

# Apply universal defaults unless locally overridden
indicator_weights.update(universal_indicator_weights)

def get_indicator_weight(indicator_name: str) -> int:
    """
    Returns the scoring weight assigned to a macroeconomic indicator.

    Default is 1 unless overridden locally or defined in the universal set.

    Args:
        indicator_name (str): Name of the indicator used in scoring

    Returns:
        int: Relative weight (1–3 recommended)
    """
    return indicator_weights.get(indicator_name, 1)
