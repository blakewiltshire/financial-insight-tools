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
    """

    def label_from_thresholds(
        ratio_val: float,
        strong_msg: tuple[str, str],
        mixed_msg: tuple[str, str],
        soft_msg: tuple[str, str],
        misaligned_msg: tuple[str, str]
    ):
        if ratio_val >= 0.85:
            return ("✅ " + strong_msg[0], strong_msg[1])
        if ratio_val >= 0.33:
            return ("⚠️ " + mixed_msg[0], mixed_msg[1])
        if ratio_val >= -0.2:
            return ("⚠️ " + soft_msg[0], soft_msg[1])
        return ("🚨 " + misaligned_msg[0], misaligned_msg[1])

    if use_case == "Inflation Pressure and Transmission":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Inflation Pressures Building",
                "Inflation indicators are broadly aligned in a restrictive direction, "
                "suggesting consumer and producer price pressures are reinforcing wider system constraint."
            ),
            (
                "Mixed Inflation Signals",
                "Inflation indicators show partial alignment, with consumer and producer price "
                "pressures not moving uniformly across headline and core layers."
            ),
            (
                "Inflation Pressures Softening",
                "Inflation signals suggest some easing, with parts of the price system showing "
                "reduced pressure while underlying inflation remains only partially moderated."
            ),
            (
                "Disinflationary / Deflationary Pressure",
                "Inflation indicators are aligned in a softer direction, suggesting broad-based "
                "easing in consumer and producer price pressures across the system."
            )
        )

    return ("⚠️ No Scoring", "No use case-specific alignment logic was found.")


# -------------------------------------------------------------------------------------------------
# --- Universal Indicator Weights (1–3 scale)
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    "Consumer Price Pressure": 3,
    "Core Consumer Inflation": 3,
    "Producer Price Pressure": 2,
    "Core Producer Inflation": 2,
}


def get_indicator_weight(indicator_name: str) -> int:
    """
    Return the relative weight for a given indicator.

    Defaults to 1 if indicator is not explicitly defined.
    """
    return indicator_weights.get(indicator_name, 1)
