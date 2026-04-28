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

    if use_case == "Housing Construction Cycle":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Pipeline Expanding",
                "Housing pipeline signals are broadly aligned, suggesting forward approvals, construction activity, and supply delivery are moving in a supportive direction."
            ),
            (
                "Mixed Pipeline Signals",
                "Housing pipeline indicators show partial alignment, with some stages holding firmer than others."
            ),
            (
                "Pipeline Softening",
                "Housing pipeline signals are mixed, with forward approvals softening while construction activity and supply delivery continue to reflect earlier momentum."
            ),
            (
                "Pipeline Misalignment",
                "Housing pipeline indicators are diverging, which may indicate pressure between approvals, active construction, and delivered supply."
            )
        )

    if use_case == "Mortgage Financing Conditions":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Financing Conditions Easing",
                "Mortgage financing signals are broadly aligned in a supportive direction, suggesting borrowing conditions and affordability pressures are becoming less restrictive."
            ),
            (
                "Mixed Financing Signals",
                "Mortgage financing indicators show partial alignment, with borrowing cost, affordability, and financing condition signals not moving uniformly."
            ),
            (
                "Financing Pressures Building",
                "Mortgage financing signals suggest some tightening pressure, with affordability or borrowing cost conditions becoming less supportive."
            ),
            (
                "Financing Conditions Tightening",
                "Mortgage financing indicators are aligned in a restrictive direction, suggesting tighter borrowing conditions across housing-sensitive credit activity."
            )
        )

    if use_case == "Yield Curve Structure":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Curve Structure Improving",
                "Yield curve signals are broadly aligned in a supportive direction, suggesting firmer macro expectations and a less compressed financial structure."
            ),
            (
                "Mixed Curve Signals",
                "Yield curve indicators show partial alignment, with slope, macro expectations, and liquidity interpretation not fully reinforcing one another."
            ),
            (
                "Curve Structure Softening",
                "Yield curve signals suggest a softer structure, with some flattening or weaker macro interpretation emerging relative to recent norms."
            ),
            (
                "Curve Compression Warning",
                "Yield curve indicators are aligned in a more restrictive direction, suggesting a flatter or more compressed macro-financial structure."
            )
        )

    if use_case == "Sovereign Debt Sustainability":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Debt Sustainability Improving",
                "Sovereign debt sustainability signals are broadly aligned in a supportive direction, suggesting debt burden, fiscal pressure, and interest burden are becoming less restrictive."
            ),
            (
                "Mixed Sovereign Debt Signals",
                "Sovereign debt sustainability indicators show partial alignment, with debt burden, fiscal balance pressure, and servicing pressure not moving uniformly."
            ),
            (
                "Debt Sustainability Softening",
                "Sovereign debt sustainability signals suggest growing pressure, with one or more debt burden or fiscal stress indicators becoming less supportive."
            ),
            (
                "Debt Sustainability Warning",
                "Sovereign debt sustainability indicators are aligned in a more restrictive direction, suggesting greater structural pressure across debt, fiscal balance, and interest burden."
            )
        )

    if use_case == "Sovereign Liquidity and Refinancing Pressure":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Refinancing Conditions Improving",
                "Sovereign refinancing signals are broadly aligned in a supportive direction, suggesting yield pressure, servicing burden, and liquidity cover conditions are becoming less restrictive."
            ),
            (
                "Mixed Refinancing Signals",
                "Sovereign refinancing indicators show partial alignment, with yield pressure, servicing pressure, and liquidity cover not moving uniformly."
            ),
            (
                "Refinancing Pressures Building",
                "Sovereign refinancing signals suggest growing pressure, with benchmark funding conditions or liquidity cover becoming less supportive."
            ),
            (
                "Refinancing Pressure Warning",
                "Sovereign refinancing indicators are aligned in a more restrictive direction, suggesting tighter funding conditions and weaker liquidity resilience."
            )
        )

    if use_case == "Balance Sheet Expansion and System Constraint":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Constraint Pressures Easing",
                "Public balance sheet signals are broadly aligned in a supportive direction, suggesting debt expansion, balance sheet support, and financing conditions are becoming less restrictive."
            ),
            (
                "Mixed Balance Sheet Signals",
                "Balance sheet expansion and system constraint indicators show partial alignment, with debt expansion, central bank support, and financing conditions not moving uniformly."
            ),
            (
                "Constraint Pressures Building",
                "Balance sheet signals suggest growing financing strain, with debt expansion or system funding conditions becoming less supportive."
            ),
            (
                "System Constraint Warning",
                "Balance sheet and financing indicators are aligned in a more restrictive direction, suggesting greater pressure across sovereign and policy-sensitive funding structures."
            )
        )

    if use_case == "Credit Conditions and Financing Pressure":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Credit Conditions Improving",
                "Credit spread signals are broadly aligned in a supportive direction, suggesting financing pressure is easing across quality tiers."
            ),
            (
                "Mixed Credit Signals",
                "Credit spread indicators show partial alignment, with investment grade, high yield, and distressed spreads not moving uniformly."
            ),
            (
                "Credit Pressures Building",
                "Credit spread signals suggest some deterioration, with one or more financing tiers becoming less supportive."
            ),
            (
                "Credit Stress Warning",
                "Credit spread indicators are aligned in a more restrictive direction, suggesting broader financing stress and tighter capital availability."
            )
        )

    if use_case == "Bank Balance Sheet Liquidity and Credit Capacity":
        return label_from_thresholds(
            alignment_ratio,
            (
                "Bank Capacity Improving",
                "Bank balance sheet signals are broadly aligned in a supportive direction, suggesting liquidity, asset capacity, and balance sheet posture are supportive of credit capacity."
            ),
            (
                "Mixed Bank Balance Sheet Signals",
                "Bank balance sheet indicators show partial alignment, with liquidity, asset capacity, and defensive positioning not moving uniformly."
            ),
            (
                "Bank Capacity Softening",
                "Bank balance sheet signals suggest some weakening, with liquidity or balance sheet posture becoming less supportive for credit capacity."
            ),
            (
                "Bank Credit Capacity Warning",
                "Bank balance sheet indicators are aligned in a more restrictive direction, suggesting weaker liquidity support and a more defensive credit posture."
            )
        )

    return ("⚠️ No Scoring", "No use case-specific alignment logic was found.")


# -------------------------------------------------------------------------------------------------
# --- Universal Indicator Weights (1–3 scale)
# -------------------------------------------------------------------------------------------------
indicator_weights = {
    "Forward Development Intent": 3,
    "Construction Conversion Flow": 2,
    "Supply Delivery Progress": 2,

    "Mortgage Borrowing Cost": 3,
    "Housing Affordability Pressure": 2,
    "Financing Condition Shift": 3,

    "Curve Slope Positioning": 3,
    "Macro Expectation Shift": 2,
    "Liquidity Regime Signal": 3,

    "Government Debt Burden": 3,
    "Fiscal Balance Pressure": 2,
    "Interest Burden on Output": 3,

    "Sovereign Yield Pressure": 3,
    "Interest Servicing Pressure": 2,
    "Liquidity Cover Conditions": 3,

    "Public Debt Expansion": 3,
    "Central Bank Balance Sheet Expansion": 2,
    "System Financing Constraint": 3,

    "Investment Grade Spread Pressure": 2,
    "High Yield Spread Pressure": 3,
    "Distressed Credit Pressure": 3,

    "Bank Cash Liquidity Conditions": 3,
    "Bank Asset Capacity": 2,
    "Bank Defensive Positioning": 2,
}


def get_indicator_weight(indicator_name: str) -> int:
    """
    Return the relative weight for a given indicator.

    Defaults to 1 if indicator is not explicitly defined.
    """
    return indicator_weights.get(indicator_name, 1)
