# -------------------------------------------------------------------------------------------------
# AI Export Snapshot Builder — Positioning & Crowding
# -------------------------------------------------------------------------------------------------

from datetime import datetime, UTC


def build_macro_insight_snapshot_positioning_and_crowding(
    theme_code: str,
    theme_title: str,
    selected_market: str,
    lookback_window: int,
    summary_payload: dict
) -> dict:
    """
    Build AI-ready snapshot for Positioning & Crowding.

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
            "selected_market": selected_market
        },
        "analysis_summary": {
            "positioning_context": {
                "selected_market": selected_market,
                "lookback_window": lookback_window,
                "market_label": summary_payload.get("market_label"),
                "market_price_label": summary_payload.get("market_price_label"),
            },
            "positioning_summary": {
                "structural_state": summary_payload.get("structural_state"),
                "current_net_position": summary_payload.get("current_net_position"),
                "current_net_pct": summary_payload.get("current_net_pct"),
                "positioning_percentile": summary_payload.get("positioning_percentile"),
                "positioning_turn": summary_payload.get("positioning_turn"),
                "contextual_interpretation": summary_payload.get("contextual_interpretation"),
            }
        },
        "metadata": {
            "snapshot_notes": (
                "Generated from Positioning & Crowding."
        ),
            "ai_review_instruction": (
                "Review this Positioning & Crowding snapshot as timing and participation context. "
                "Interpret net positioning, percentile extremes, and positioning turns relative to "
                "the selected historical window. Do not treat crowded positioning as an automatic "
                "reversal signal, a positioning flip as confirmation of direction, or percentile "
                "extremes as standalone trade evidence. Identify where positioning may reinforce, "
                "complicate, or challenge a wider investigation, and distinguish observed positioning "
                "from inferred market intent. Do not recommend investments or select trades."
            ),
        },
    }
