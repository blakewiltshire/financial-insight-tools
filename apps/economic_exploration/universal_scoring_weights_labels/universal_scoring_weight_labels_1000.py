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
# --- Generic Scoring Label Dispatcher
# -------------------------------------------------------------------------------------------------

def get_alignment_score_label(alignment_ratio: float, use_case: str):
    """
    Return placeholder label and description based on a score ratio and use case.

    Parameters:
        alignment_ratio (float): Numeric score, e.g. 0.85
        use_case (str): Label such as "Placeholder Use Case A"

    Returns:
        tuple[str, str]: Status label and explanation
    """
    if alignment_ratio >= 0.85:
        return ("✅ Strong Alignment", f"The indicators for {use_case} show strong structural alignment.")
    if alignment_ratio >= 0.33:
        return ("⚠️ Mixed Signals", f"The indicators for {use_case} show partial alignment.")
    if alignment_ratio >= -0.2:
        return ("⚠️ Weak Alignment", f"The indicators for {use_case} show inconsistent signals.")
    return ("🚨 Misaligned", f"The indicators for {use_case} suggest divergence or reversal.")

# -------------------------------------------------------------------------------------------------
# --- Placeholder Indicator Weights
# -------------------------------------------------------------------------------------------------

indicator_weights = {
    "Signal A": 1,
    "Signal B": 1,
    "Signal C": 1
}

def get_indicator_weight(indicator_name: str) -> int:
    """
    Return relative weight for placeholder indicators.

    Parameters:
        indicator_name (str)

    Returns:
        int
    """
    return indicator_weights.get(indicator_name, 1)
