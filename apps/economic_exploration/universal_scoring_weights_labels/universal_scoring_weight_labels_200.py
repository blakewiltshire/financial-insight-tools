# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧮 Universal Scoring & Weighting Labels — Economic Exploration System
-----------------------------------------------------------------------

Defines the core alignment scoring framework for all thematic modules in the Economic Exploration suite.
This module transforms raw signal outputs into structured alignment labels, insight narratives,
and composite scoring weights applied across the entire decision-support system.

✅ System Role:
- Converts macro alignment ratios into labelled narrative outputs for:
    • Macro Conditions Summaries
    • AI personas and insight generators
    • Scoring dashboards and composite panels
- Provides default indicator weightings to determine signal importance

🧠 AI Persona & DSS Notes:
- Alignment labels returned by `get_alignment_score_label()` directly drive:
    • AI narrative generation
    • Macro scorecard reporting
    • Triangular navigation program reflections

- All label keys must match use case entries defined in:
    • `use_cases_XXX.py`
    • `indicator_map_XXX.py`
    • `insight_XXX.py`

⚙️ Structural Rules:
1️⃣ **Score Label Dispatcher**
- `get_alignment_score_label(alignment_ratio, use_case)` returns:
    • A concise label (emoji + text)
    • A long-form AI-compatible explanation

- Threshold logic is consistent across all themes:
    • ≥ 0.85 → Strong Alignment
    • 0.33–0.85 → Mixed Alignment
    • −0.2–0.33 → Soft Misalignment
    • < −0.2 → Clear Misalignment

2️⃣ **Weighting System**
- `get_indicator_weight(indicator_name)` maps indicators to relative weights (scale 1–3)
- Weighting influences composite thematic scoring totals
- Defaults to weight 1 if not explicitly assigned

3️⃣ **Universal Stability**
- This universal module is imported across all countries and themes
- Local modules (e.g., `scoring_weights_labels_XXX.py`) extend or override mappings as needed

🧭 Governance Note:
- This scoring module forms core system infrastructure.
- User configuration occurs via local extensions only — universal logic remains stable across releases.
"""

# -------------------------------------------------------------------------------------------------
# --- Scoring Label Dispatcher
# -------------------------------------------------------------------------------------------------

def get_alignment_score_label(alignment_ratio: float, use_case: str):
    """
    Return a structured alignment label and explanation for labour market indicators.

    Parameters:
        alignment_ratio (float): Numeric score between -1 and 1.
        use_case (str): Use case label ("Employment Trends", etc.)

    Returns:
        tuple[str, str]: (Emoji-tagged label, explanation)
    """
    def label_from_thresholds(
    ratio_val: float, strong_msg: tuple[str, str], mixed_msg: tuple[str, str],
                              soft_msg: tuple[str, str], misaligned_msg: tuple[str, str]):
        if ratio_val >= 0.85:
            return ("✅ " + strong_msg[0], strong_msg[1])
        if ratio_val >= 0.33:
            return ("⚠️ " + mixed_msg[0], mixed_msg[1])
        if ratio_val >= -0.2:
            return ("⚠️ " + soft_msg[0], soft_msg[1])
        return ("🚨 " + misaligned_msg[0], misaligned_msg[1])

    if use_case == "Employment Trends":
        return label_from_thresholds(
            alignment_ratio,
            ("Robust Employment Momentum", "Employment signals suggest strong hiring trends and "
            "expansion in the formal economy."),
            ("Mixed Employment Signals", "Hiring is occurring but with inconsistent pace or weak "
            "sector breadth."),
            ("Soft Hiring Conditions", "Employment growth is sluggish or volatile, possibly "
            "early-cycle or defensive."),
            ("Labour Market Weakness", "Employment indicators suggest deterioration or reversal "
            "in hiring dynamics.")
        )

    if use_case == "Unemployment Context":
        return label_from_thresholds(
            alignment_ratio,
            ("Tight Labour Conditions", "Unemployment signals indicate a tightening market with "
            "low slack."),
            ("Mixed Unemployment Signals", "Some pressure remains, but improvement trends exist."),
            ("Residual Slack", "Elevated unemployment or reversal from gains may signal "
            "structural or cyclical fragility."),
            ("Labour Market Stress", "Unemployment data points to rising slack or "
            "macroeconomic stress.")
        )

    if use_case == "Labour Force Engagement":
        return label_from_thresholds(
            alignment_ratio,
            ("Strong Participation Engagement", "Workforce engagement is improving, supporting "
            "structural output potential."),
            ("Moderate Participation Trends", "Stable participation rates with some variation "
            "by cohort or region."),
            ("Weak Engagement Signals", "Participation is flat or declining, hinting at "
            "demographic or inclusion barriers."),
            ("Structural Disengagement", "Labour force participation is near historic "
            "lows, suggesting systemic disengagement.")
        )

    return ("⚠️ No Scoring", "No use case-specific alignment logic was found.")

# -------------------------------------------------------------------------------------------------
# --- Indicator Weight Mapping (1–3 scale)
# -------------------------------------------------------------------------------------------------

indicator_weights = {
    # --- Employment Trends ---
    "Job Creation Momentum": 3,
    "Volatility in Hiring Activity": 2,
    "Cyclical Turning Points": 2,

    # --- Unemployment Context ---
    "Unemployment Shifts": 3,
    "Stress or Slack Indicators": 2,
    "Reversion from Extremes": 2,

    # --- Labour Force Engagement ---
    "Participation Stability": 2,
    "Demographic or Structural Shifts": 1,
    "Engagement Trend Change": 2
}

def get_indicator_weight(indicator_name: str) -> int:
    """
    Return relative weight for a given signal name.

    Parameters:
        indicator_name (str): Name of the indicator used in scoring logic.

    Returns:
        int: Weight (1–3)
    """
    return indicator_weights.get(indicator_name, 1)
