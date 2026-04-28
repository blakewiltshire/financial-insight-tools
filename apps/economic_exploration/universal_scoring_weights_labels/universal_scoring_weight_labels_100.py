# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Scoring & Weighting Labels — Economic Exploration System
-----------------------------------------------------------------------

Defines the core alignment scoring framework for all thematic modules in the Economic Exploration suite.
This module transforms raw signal outputs into structured alignment labels, insight narratives,
and composite scoring weights applied across the entire decision-support system.

System Role:
- Converts macro alignment ratios into labelled narrative outputs for:
    • Macro Conditions Summaries
    • AI personas and insight generators
    • Scoring dashboards and composite panels
- Provides default indicator weightings to determine signal importance

AI Persona & DSS Notes:
- Alignment labels returned by `get_alignment_score_label()` directly drive:
    • AI narrative generation
    • Macro scorecard reporting
    • Triangular navigation program reflections

- All label keys must match use case entries defined in:
    • `use_cases_XXX.py`
    • `indicator_map_XXX.py`
    • `insight_XXX.py`

Structural Rules:
**Score Label Dispatcher**
- `get_alignment_score_label(alignment_ratio, use_case)` returns:
    • A concise label (emoji + text)
    • A long-form AI-compatible explanation

- Threshold logic is consistent across all themes:
    • ≥ 0.85 → Strong Alignment
    • 0.33–0.85 → Mixed Alignment
    • −0.2–0.33 → Soft Misalignment
    • < −0.2 → Clear Misalignment

**Weighting System**
- `get_indicator_weight(indicator_name)` maps indicators to relative weights (scale 1–3)
- Weighting influences composite thematic scoring totals
- Defaults to weight 1 if not explicitly assigned

**Universal Stability**
- This universal module is imported across all countries and themes
- Local modules (e.g., `scoring_weights_labels_XXX.py`) extend or override mappings as needed

Governance Note:
- This scoring module forms core system infrastructure.
- User configuration occurs via local extensions only — universal logic remains stable across releases.
"""

# -------------------------------------------------------------------------------------------------
# --- Scoring Label Dispatcher
# -------------------------------------------------------------------------------------------------

def get_alignment_score_label(alignment_ratio: float, use_case: str):
    """
    Return a structured alignment label and description based on a score ratio and use case.

    Parameters:
        alignment_ratio (float): Numeric score indicating alignment strength, e.g. 0.85
        use_case (str): Category such as "Real GDP", "Nominal GDP", etc.

    Returns:
        tuple[str, str]: A status emoji + label, and a contextual explanation.
    """
    def label_from_thresholds(ratio_val: float, strong_msg: tuple[str, str], mixed_msg: tuple[str, str],
                              soft_msg: tuple[str, str], misaligned_msg: tuple[str, str]):
        if ratio_val >= 0.85:
            return ("✅ " + strong_msg[0], strong_msg[1])
        if ratio_val >= 0.33:
            return ("⚠️ " + mixed_msg[0], mixed_msg[1])
        if ratio_val >= -0.2:
            return ("⚠️ " + soft_msg[0], soft_msg[1])
        return ("🚨 " + misaligned_msg[0], misaligned_msg[1])

    if use_case == "Real GDP":
        return label_from_thresholds(
            alignment_ratio,
            ("Strong Growth Alignment", "In the selected period, Real GDP signals point to strong and broad-based expansion momentum."),
            ("Mixed Signals", "Real GDP indicators show mixed performance—some components support growth while others suggest moderation."),
            ("Soft Misalignment", "Real GDP indicators are diverging, hinting at volatility or early signs of weakening trends."),
            ("Macro Misalignment", "Real GDP signals point to contraction risks, policy drag, or structural weakness.")
        )

    if use_case == "Nominal GDP":
        return label_from_thresholds(
            alignment_ratio,
            ("Strong Nominal Alignment", "Nominal GDP signals suggest robust expansion—potential implications for inflation and rates."),
            ("Mixed Nominal Signals", "Nominal GDP indicators show partial alignment—growing economy with some pricing inconsistencies."),
            ("Soft Nominal Misalignment", "Nominal trends are weakening—may reflect early moderation or reduced demand strength."),
            ("Nominal Misalignment", "Nominal GDP is deteriorating—may reflect contraction, tightening, or external drag.")
        )

    if use_case == "GDP Components Breakdown":
        return label_from_thresholds(
            alignment_ratio,
            ("Strong Component Alignment", "Component signals point to healthy demand structure—broad-based contribution patterns."),
            ("Mixed Component Signals", "Some sectors support growth while others point to imbalance or divergence."),
            ("Soft Component Misalignment", "Signals suggest weak structure—watch for over-reliance on government or trade."),
            ("Component Misalignment", "GDP structure shows imbalance—defensive or policy-led drivers limit sustainable growth.")
        )

    return ("⚠️ No Scoring", "No use case-specific alignment logic was found.")

# -------------------------------------------------------------------------------------------------
# --- Universal Indicator Weights (1–3 scale)
# -------------------------------------------------------------------------------------------------

indicator_weights = {
    # --- Real GDP ---
    "Growth Trend Evaluation": 3,
    "Volatility & Extremes": 2,
    "Policy & Sentiment Shifts": 2,

    # --- Nominal GDP ---
    "Absolute Market Size": 3,
    "Currency Sensitivity Signals": 2,
    "Policy Normalization Dynamics": 2,

    # --- GDP Components Breakdown ---
    "Consumption vs Investment vs Government": 3,
    "Export-Import Divergence": 2,
    "Structural Demand Trends": 2
}


def get_indicator_weight(indicator_name: str) -> int:
    """
    Return the relative weight for a given indicator.

    Defaults to 1 if indicator is not explicitly defined.

    Parameters:
        indicator_name (str): Name of the indicator.

    Returns:
        int: Weight between 1–3
    """
    return indicator_weights.get(indicator_name, 1)
