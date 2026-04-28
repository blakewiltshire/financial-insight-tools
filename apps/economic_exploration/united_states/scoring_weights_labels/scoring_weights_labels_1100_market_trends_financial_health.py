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
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Configuration
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_scoring_labels"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Imports
# -------------------------------------------------------------------------------------------------
from universal_scoring_weight_labels_1100 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)

# -------------------------------------------------------------------------------------------------
# Local Scoring Label Definitions
# -------------------------------------------------------------------------------------------------
def score_aggregate_equity_allocation(alignment_ratio: float) -> tuple[str, str]:
    if alignment_ratio >= 0.85:
        return (
            "✅ Equity Allocation Conditions Firm",
            "Aggregate equity allocation indicators are broadly aligned in a supportive direction, "
            "suggesting equity market value and the aggregate equity allocation ratio are holding "
            "up relative to the wider liability structure."
        )

    if alignment_ratio >= 0.33:
        return (
            "⚠️ Mixed Allocation Signals",
            "Aggregate equity allocation indicators show partial alignment, with equity value, "
            "liability structure, and allocation share not moving uniformly across the broader system."
        )

    if alignment_ratio >= -0.2:
        return (
            "⚠️ Allocation Conditions Softening",
            "Aggregate equity allocation signals suggest some softening, with parts of the "
            "equity-liability structure losing strength while the wider backdrop remains mixed."
        )

    return (
        "🚨 Liability Structure Dominating",
        "Aggregate equity allocation indicators are aligned in a weaker direction, suggesting "
        "the broader liability structure is expanding faster than equity market value and allocation share."
    )


USE_CASE_SCORING_LABELS = {
    "Aggregate Equity Allocation": score_aggregate_equity_allocation,
}

# -------------------------------------------------------------------------------------------------
# Dispatcher — Label Fallback Logic
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
# Indicator Weights — Influence Over Composite Score
# -------------------------------------------------------------------------------------------------
indicator_weights = dict(universal_indicator_weights)

indicator_weights.update({
    "Equity Market Value Position": 3,
    "Economy Wide Liability Structure": 2,
    "Aggregate Equity Allocation Ratio": 3,
})


def get_indicator_weight(indicator_name: str) -> int:
    """
    Returns the relative weight (1–3) for a given macroeconomic indicator.

    Priority:
    - Local indicator weights override universal defaults
    - Universal template weights remain available for Signal A / B / C
    - Falls back to 1 if no explicit weight is defined

    Args:
        indicator_name (str): Display label of the indicator

    Returns:
        int: Assigned weight
    """
    return indicator_weights.get(indicator_name, 1)
