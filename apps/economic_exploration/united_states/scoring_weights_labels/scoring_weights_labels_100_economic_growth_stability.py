# -------------------------------------------------------------------------------------------------
# Thematic Indicator Scoring — Local Wrapper
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Scoring Weights & Alignment Labels — Thematic Module Extension
-----------------------------------------------------------------------

This module defines the country-specific scoring weights and alignment labels
for individual use cases within a given thematic grouping. It extends the universal scoring framework
to account for national context, additional indicators, and refined interpretations.

System Role:
- Provides localised scoring narratives for macro alignment ratios
- Overrides or supplements universal logic as new use cases are added
- Supports fully integrated AI narratives, macro summaries, and DSS scorecards

AI Persona & DSS Notes:
- Returned labels directly drive AI export summaries, scoring panels, and triangular navigation flows
- Alignment scoring logic remains consistent across themes:
    • ≥ 0.85 → Strong Alignment
    • 0.33–0.85 → Mixed Alignment
    • −0.2–0.33 → Soft Misalignment
    • < −0.2 → Clear Misalignment

Structural Governance:
**Label Mapping Dispatcher**
- `get_alignment_score_label(alignment_ratio, use_case)` applies local thresholds per use case.
- Always checks for a local override first, otherwise falls back to the universal dispatcher.

**Indicator Weighting System (Extended)**
- `get_indicator_weight(indicator_name)` returns a 1–3 weight scale per indicator.
- Local weights supplement and merge with the universal indicator weight registry.
- Supports composite macro scoring logic across all scoring layers.

**Interface Consistency**
- Function names and use case names must strictly match:
    • `use_cases_XXX.py`
    • `indicator_map_XXX.py`
    • `insight_XXX.py`
    • Universal scoring contract remains stable — local extensions must integrate seamlessly.

Governance Note:
- Local scoring files are only created when country-specific indicators or signal groupings exist.
- If no local scoring exists, the universal scoring contract fully governs system operation.
"""

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_scoring_labels"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_scoring_weight_labels_100 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)

# -------------------------------------------------------------------------------------------------
# Local Scoring Label Map (Optional)
# -------------------------------------------------------------------------------------------------
USE_CASE_SCORING_LABELS = {
    "Macro Composite Signals": lambda ratio_val: (
        ("✅ Strong Macro Composite Alignment", "Composite indicators suggest improving forward conditions and broad strength.")
        if ratio_val >= 0.85 else
        ("⚠️ Mixed Composite Signals", "Mixed leading and breadth signals—watch for divergence in expectations vs structure.")
        if ratio_val >= 0.33 else
        ("⚠️ Soft Composite Misalignment", "Momentum may be weakening—signals suggest muted trends or instability.")
        if ratio_val >= -0.2 else
        ("🚨 Composite Misalignment", "Leading indicators show deterioration—uncertainty and weak breadth dominate.")
    )
}

# -------------------------------------------------------------------------------------------------
# Dispatcher — Local First, Fallback to Universal
# -------------------------------------------------------------------------------------------------
def get_alignment_score_label(alignment_ratio: float, use_case: str) -> tuple[str, str]:
    """
    Returns scoring label and explanation for a given alignment ratio and use case.

    Logic:
    - Checks local scoring map first
    - Falls back to universal dispatcher if undefined

    Parameters:
        alignment_ratio (float): Calculated macro alignment score
        use_case (str): Use case label string

    Returns:
        tuple[str, str]: (Short label with emoji, Long explanation)
    """
    if use_case in USE_CASE_SCORING_LABELS:
        return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)
    return get_alignment_score_label_universal(alignment_ratio, use_case)

# -------------------------------------------------------------------------------------------------
# Indicator Weights (Local Overrides or Extensions)
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    "Leading Economic Index (Conference Board)": 3,
    "Weekly Economic Index (NY Fed)": 2,
    "National Activity Composite": 2,
    "Uncertainty Index Impact": 1
}

indicator_weights.update(universal_indicator_weights)

def get_indicator_weight(indicator_name: str) -> int:
    return indicator_weights.get(indicator_name, 1)
