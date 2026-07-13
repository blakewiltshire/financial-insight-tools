# -------------------------------------------------------------------------------------------------
# AI Export Snapshot Builder — Relative Macro Transmission
# -------------------------------------------------------------------------------------------------

from datetime import datetime, UTC


def build_macro_insight_snapshot_relative_macro_transmission(
    theme_code: str,
    theme_title: str,
    use_case: str,
    series_a_obj: dict | None,
    series_b_obj: dict | None,
    anchor_pair_obj: dict | None,
    comparison_mode: str,
    transformation: str,
    window: int,
    result: dict,
    contextual_insight: str
) -> dict:
    """
    Build AI-ready snapshot for Relative Macro Transmission.

    This is intentionally light-touch and page-native:
    - no Market & Volatility statistical registry logic
    - no macro signal expansion
    - no unnecessary metadata plumbing
    """

    return {
        "snapshot_metadata": {
            "theme": {
                "code": theme_code,
                "title": theme_title
            },
            "snapshot_timestamp": datetime.now(UTC).isoformat(),
            "use_case": use_case
        },
        "analysis_summary": {
            "comparison_context": {
                "primary": series_a_obj["label"] if series_a_obj else None,
                "comparison": series_b_obj["label"] if series_b_obj else None,
                "anchor_pair": anchor_pair_obj["label"] if anchor_pair_obj else None,
                "comparison_mode": comparison_mode,
                "transformation": transformation,
                "window": window
            },
            "transmission_summary": {
                "structural_state": result.get("regime_label"),
                "current_differential": result.get("current_value"),
                "percentile": result.get("percentile"),
                "rolling_state": result.get("rolling_state"),
                "contextual_interpretation": contextual_insight
            }
        },
        "metadata": {
            "snapshot_notes": (
                "Generated from Relative Macro Transmission."
            ),
            "ai_review_instruction": (
                "Review this Relative Macro Transmission snapshot as comparative structural context. "
                "Interpret the current differential, percentile, rolling state, transformation, and "
                "selected window together. Do not infer causation, stable transmission, predictive "
                "power, or trade direction from relative movement alone. Identify whether the observed "
                "relationship appears persistent, changing, unusual, or incomplete, and note which "
                "additional evidence would be required for interpretation."
            ),
        },
    }
