# -------------------------------------------------------------------------------------------------
# 🎯 Thematic Indicator Scoring — Local Wrapper
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
# 📦 Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# 🛠 Path Configuration
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_scoring_labels"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 📥 Universal Imports
# -------------------------------------------------------------------------------------------------
from universal_scoring_weight_labels_1500 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)

# -------------------------------------------------------------------------------------------------
# 🧭 Local Scoring Label Definitions (Optional)
# -------------------------------------------------------------------------------------------------
USE_CASE_SCORING_LABELS = {
    # Example:
    # "Signal A": lambda ratio: ("🟢 Strong Alignment", "All indicators show consistent strength.")
}

# -------------------------------------------------------------------------------------------------
# 🔁 Dispatcher — Label Fallback Logic
# -------------------------------------------------------------------------------------------------
def get_alignment_score_label(alignment_ratio: float, use_case: str) -> tuple[str, str]:
    """
    Retrieves scoring label and explanation based on alignment ratio and use case.

    Priority:
    - First checks for local override in `USE_CASE_SCORING_LABELS`
    - Falls back to universal logic if none found

    Args:
        alignment_ratio (float): Composite score for selected indicators
        use_case (str): Label of the active use case

    Returns:
        tuple[str, str]: (Short label, Long explanation)
    """
    if use_case in USE_CASE_SCORING_LABELS:
        return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)
    return get_alignment_score_label_universal(alignment_ratio, use_case)

# -------------------------------------------------------------------------------------------------
# ⚖️ Indicator Weights — Influence Over Composite Score
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    # Optional: "Signal A": 3, "Signal B": 2
}
indicator_weights.update(universal_indicator_weights)

def get_indicator_weight(indicator_name: str) -> int:
    """
    Returns the relative weight (1–3) for a given macroeconomic indicator.

    Args:
        indicator_name (str): Display label of the indicator

    Returns:
        int: Assigned weight, defaults to 1
    """
    return indicator_weights.get(indicator_name, 1)
