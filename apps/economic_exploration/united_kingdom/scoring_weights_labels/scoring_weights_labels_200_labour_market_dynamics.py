# -------------------------------------------------------------------------------------------------
# Thematic Indicator Scoring — Theme 200 Labour Market Dynamics (Platinum Level)
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
# Universal Imports (for fallback)
# -------------------------------------------------------------------------------------------------
from universal_scoring_weight_labels_200 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)

# -------------------------------------------------------------------------------------------------
# Local Scoring Label Functions (Per Use Case)
# -------------------------------------------------------------------------------------------------

def label_from_thresholds(ratio_val, strong, mixed, soft, stress):
    if ratio_val >= 0.85:
        return ("✅ " + strong[0], strong[1])
    if ratio_val >= 0.33:
        return ("⚠️ " + mixed[0], mixed[1])
    if ratio_val >= -0.2:
        return ("⚠️ " + soft[0], soft[1])
    return ("🚨 " + stress[0], stress[1])

USE_CASE_SCORING_LABELS = {

    "Business Sector Employment Breakdown": lambda ratio_val: label_from_thresholds(
        ratio_val,
        ("Broad Sector Expansion", "Most industries are expanding with strong sector hiring breadth."),
        ("Mixed Sector Momentum", "Some sectors show strength while others are flat or contracting."),
        ("Flat or Uneven Sector Trends", "Minimal dispersion — sector trends are not aligned strongly."),
        ("Widespread Sector Weakness", "Majority of sectors showing contraction — possible macro fragility.")
    ),

    "Full-Time vs Part-Time Employment": lambda ratio_val: label_from_thresholds(
        ratio_val,
        ("Full-Time Driven Expansion", "Full-time roles dominate hiring — healthy labour expansion signal."),
        ("Balanced or Part-Time Led", "Part-time hiring is contributing more — may signal mixed quality."),
        ("Stalled Employment Composition", "Limited shifts between full and part-time roles."),
        ("Part-Time Reliant Growth", "Growth driven by part-time surge — possible underemployment risk.")
    ),

    "Average Hourly Earnings": lambda ratio_val: label_from_thresholds(
        ratio_val,
        ("Accelerating Wage Growth", "Wages rising sharply — income momentum supporting consumption."),
        ("Moderate Wage Gains", "Wages increasing modestly — consistent with balanced growth."),
        ("Weak Wage Growth", "Wage gains limited — labour pricing power subdued."),
        ("Stagnant or Declining Wages", "Wage pressures fading — possible demand weakening.")
    ),

    "Jobless Claims": lambda ratio_val: label_from_thresholds(
        ratio_val,
        ("Low Claims, Low Stress", "Jobless claims stable or falling — supportive labour market health."),
        ("Rising Claims (Mild)", "Early signs of softening, but still manageable."),
        ("Elevated Claims Emerging", "Sustained increases suggest caution in hiring resilience."),
        ("Jobless Claims Spike", "High-frequency data points to sharp deterioration in hiring conditions.")
    )
}

# -------------------------------------------------------------------------------------------------
# Dispatcher — Local First, Fallback to Universal
# -------------------------------------------------------------------------------------------------
def get_alignment_score_label(alignment_ratio: float, use_case: str):
    if use_case in USE_CASE_SCORING_LABELS:
        return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)
    return get_alignment_score_label_universal(alignment_ratio, use_case)

# -------------------------------------------------------------------------------------------------
# Indicator Weights — Labour Market Dynamics (Local Extension)
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    # Business Sector Employment Breakdown
    "Business Sector Employment Breakdown – Momentum": 3,
    "Business Sector Employment Breakdown – Stress": 2,
    "Business Sector Employment Breakdown – Summary": 1,

    # Full-Time vs Part-Time
    "Employment Type Balance": 3,
    "Part-Time Employment Stress": 2,

    # Wages
    "Wage Growth Trend": 3,

    # Jobless Claims
    "Initial Jobless Claims": 3,
    "Continued Jobless Claims": 2
}

# Merge universal weights
indicator_weights.update(universal_indicator_weights)

def get_indicator_weight(indicator_name: str) -> int:
    return indicator_weights.get(indicator_name, 1)
