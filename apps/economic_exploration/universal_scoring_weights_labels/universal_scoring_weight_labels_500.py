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

    if use_case == "Money Supply and Velocity Dynamics":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Liquidity and Circulation Strengthening",
                "Money supply and velocity signals are broadly aligned in a supportive direction, "
                "suggesting liquidity expansion and monetary circulation are reinforcing wider system activity."
            ),
            (
                "Mixed Liquidity Signals",
                "Money supply and velocity indicators show partial alignment, with liquidity expansion "
                "and monetary circulation not moving uniformly."
            ),
            (
                "Liquidity Conditions Softening",
                "Money supply and velocity signals suggest softer monetary conditions, with liquidity or "
                "circulation losing some support relative to recent norms."
            ),
            (
                "Liquidity and Circulation Tightening",
                "Money supply and velocity indicators are aligned in a weaker direction, suggesting "
                "tightening liquidity conditions and slower system circulation."
            )
        )

    if use_case == "Interest Rate Regime and Transmission":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Rate Conditions Easing",
                "Interest rate signals are broadly aligned in a more supportive direction, suggesting "
                "policy, funding, lending, mortgage, and curve conditions are becoming less restrictive."
            ),
            (
                "Mixed Rate Signals",
                "Interest rate indicators show partial alignment, with policy stance, funding conditions, "
                "lending pressure, mortgage conditions, and curve structure not moving uniformly."
            ),
            (
                "Rate Pressures Building",
                "Interest rate signals suggest some tightening pressure, with parts of the rate structure "
                "becoming less supportive even if conditions are not fully restrictive."
            ),
            (
                "Rate Regime Tightening",
                "Interest rate indicators are aligned in a restrictive direction, suggesting tighter "
                "policy, funding, lending, or curve conditions across the system."
            )
        )

    return ("⚠️ No Scoring", "No use case-specific alignment logic was found.")


# -------------------------------------------------------------------------------------------------
# --- Universal Indicator Weights (1–3 scale)
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    "Narrow Money Conditions": 3,
    "Broad Money Conditions": 3,
    "Narrow Money Velocity": 2,
    "Broad Money Velocity": 2,
    "Policy Rate Positioning": 3,
    "Funding Rate Conditions": 3,
    "Bank Lending Rate Pressure": 2,
    "Mortgage Rate Conditions": 2,
    "Treasury Curve Structure": 3,
    "Real Policy Rate Proxy": 2,
}


def get_indicator_weight(indicator_name: str) -> int:
    """
    Return the relative weight for a given indicator.

    Defaults to weight 1 if indicator is not explicitly defined.
    """
    return indicator_weights.get(indicator_name, 1)
