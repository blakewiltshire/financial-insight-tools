# -------------------------------------------------------------------------------------------------
# Market Structure Summary
# -------------------------------------------------------------------------------------------------
"""Build DSS-ready summary payloads for Market Structure Review."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_value(record: dict, key: str, default: str = "N/A") -> str:
    value = record.get(key, default)
    if pd.isna(value):
        return default
    text = str(value).strip()
    return text if text else default

def _clean_sentence_text(value: str) -> str:
    if not value or value == "N/A":
        return ""

    text = str(value).strip()
    text = text.rstrip(".")
    return text


def _records(df: pd.DataFrame) -> list[dict]:
    if df is None or df.empty:
        return []
    clean_df = df.copy()
    clean_df = clean_df.astype(object).where(pd.notna(clean_df), "")
    return clean_df.to_dict(orient="records")


def _first_record(df: pd.DataFrame) -> dict:
    if df is None or df.empty:
        return {}
    return df.fillna("").iloc[0].to_dict()


def _contains_any(text: str, keywords: list[str]) -> bool:
    text_lower = str(text or "").lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def _build_structural_summary(
    focus_company: str,
    focus_ticker: str,
    focus_structure_type: str,
    focus_context: dict,
    focus_event_count: int,
    comparison_count: int,
) -> str:
    """
    Build a concise synthesis of the selected asset's market structure.

    This intentionally avoids repeating every profile field. It connects ownership,
    float, supply, participation, and index context into an AI-ready framing note.
    """
    ownership = focus_context.get("ownership_structure", "")
    float_structure = focus_context.get("float_structure", "")
    supply = focus_context.get("supply_structure", "")
    participation = focus_context.get("institutional_participation", "")
    index_eligibility = focus_context.get("index_eligibility", "")
    major_supply_events = focus_context.get("major_supply_events", "")

    traits = []

    if _contains_any(ownership, ["founder", "early-investor", "strategic", "concentration", "dominant"]):
        traits.append("concentrated ownership")
    elif ownership and ownership != "N/A":
        traits.append("a defined ownership structure")

    if _contains_any(float_structure, ["limited", "constrained", "initial", "small"]):
        traits.append("a constrained public float")
    elif _contains_any(float_structure, ["broad", "immediate", "no traditional"]):
        traits.append("a broader initial liquidity structure")
    elif float_structure and float_structure != "N/A":
        traits.append("a defined float structure")

    if _contains_any(supply, ["phased", "tranche", "schedule", "lock-up", "lockup"]):
        traits.append("a structured supply-release process")
    elif _contains_any(supply, ["direct listing", "immediate"]):
        traits.append("immediate ownership liquidity")
    elif _contains_any(supply, ["sale", "sales", "secondary", "partial"]):
        traits.append("supply expansion through shareholder sales")
    elif supply and supply != "N/A":
        traits.append("defined supply-event characteristics")

    if _contains_any(participation, ["index", "institutional", "eligibility", "participation"]):
        traits.append("potential changes in institutional participation")
    elif participation and participation != "N/A":
        traits.append("defined participation dynamics")

    if not traits:
        traits.append("ownership, float, supply, and participation characteristics")

    if len(traits) == 1:
        trait_text = traits[0]
    elif len(traits) == 2:
        trait_text = f"{traits[0]} and {traits[1]}"
    else:
        trait_text = f"{', '.join(traits[:-1])}, and {traits[-1]}"

    if _contains_any(supply, ["phased", "tranche", "schedule"]):
        supply_sentence = (
            "Rather than relying on a single supply event, the structure indicates that "
            "available shares may expand through multiple release points."
        )
    elif _contains_any(supply, ["direct listing", "immediate"]):
        supply_sentence = (
            "Because liquidity was available immediately, price discovery began without the "
            "same staged lock-up structure seen in many traditional IPOs."
        )
    elif _contains_any(supply, ["lock-up", "lockup"]):
        supply_sentence = (
            "The supply structure is shaped by lock-up dynamics, making the timing of available "
            "shares an important observation point."
        )
    elif _contains_any(supply, ["sale", "sales", "secondary", "partial"]):
        supply_sentence = (
            "Shareholder sale activity forms part of the supply context, linking ownership changes "
            "with market participation and liquidity."
        )
    else:
        supply_sentence = (
            "The supply structure provides a reference point for observing how available shares, "
            "liquidity, and participation may change through time."
        )

    index_sentence = ""
    if index_eligibility and index_eligibility != "N/A":
        if _contains_any(index_eligibility, ["nasdaq", "index", "eligibility", "fast-entry"]):
            index_sentence = (
                "Index eligibility may add a further participation layer if methodology, size, "
                "liquidity, and float conditions are satisfied. "
            )
        else:
            index_sentence = f"Index context: {index_eligibility} "

    event_sentence = ""
    if focus_event_count > 0:
        event_sentence = (
            f"The review maps {focus_event_count} supply-related event(s) for the focus asset"
        )
        clean_events = _clean_sentence_text(major_supply_events)

        if clean_events:
            event_sentence += f", including {clean_events}"
        event_sentence += ". "

    comparison_sentence = ""
    if comparison_count > 0:
        comparison_sentence = (
            f"The wider comparison group provides {comparison_count} reference structure(s) for "
            "reviewing how different listing, ownership, and supply designs can shape post-listing market context."
        )

    return (
        f"{focus_company} ({focus_ticker}) combines {trait_text}. "
        f"{supply_sentence} "
        f"{index_sentence}"
        f"{event_sentence}"
        f"{comparison_sentence}"
    ).strip()

# -------------------------------------------------------------------------------------------------
# Summary Builder
# -------------------------------------------------------------------------------------------------
def build_market_structure_summary(
    profile_df: pd.DataFrame,
    events_df: pd.DataFrame,
    focus_ticker: str | None = None,
) -> dict:
    """Build focus-asset and dataset-level summary payload for Market Structure Review."""
    asset_count = len(profile_df) if profile_df is not None else 0
    event_count = len(events_df) if events_df is not None else 0

    # Resolve focus ticker safely.
    if focus_ticker is None and profile_df is not None and not profile_df.empty:
        focus_ticker = str(profile_df.iloc[0].get("Ticker", "")).strip()

    focus_ticker = str(focus_ticker or "").strip()

    focus_profile_df = pd.DataFrame()
    if profile_df is not None and not profile_df.empty and "Ticker" in profile_df.columns:
        focus_profile_df = profile_df[
            profile_df["Ticker"].astype(str).str.strip().str.upper() == focus_ticker.upper()
        ].copy()

    focus_events_df = pd.DataFrame()
    if events_df is not None and not events_df.empty and "Ticker" in events_df.columns:
        focus_events_df = events_df[
            events_df["Ticker"].astype(str).str.strip().str.upper() == focus_ticker.upper()
        ].copy()

    comparison_profile_df = profile_df.copy() if profile_df is not None else pd.DataFrame()
    if not comparison_profile_df.empty and "Ticker" in comparison_profile_df.columns:
        comparison_profile_df = comparison_profile_df[
            comparison_profile_df["Ticker"].astype(str).str.strip().str.upper() != focus_ticker.upper()
        ].copy()

    focus_profile = _first_record(focus_profile_df)
    focus_company = _safe_value(focus_profile, "Company", focus_ticker or "N/A")
    focus_structure_type = _safe_value(focus_profile, "Structure_Type")

    event_counts_by_type = {}
    if events_df is not None and not events_df.empty and "Event_Type" in events_df.columns:
        event_counts_by_type = events_df["Event_Type"].value_counts(dropna=False).to_dict()

    focus_event_counts_by_type = {}
    if not focus_events_df.empty and "Event_Type" in focus_events_df.columns:
        focus_event_counts_by_type = focus_events_df["Event_Type"].value_counts(dropna=False).to_dict()

    focus_context = {
        "asset": {
            "company": focus_company,
            "ticker": focus_ticker,
            "exchange": _safe_value(focus_profile, "Exchange"),
            "structure_type": focus_structure_type,
        },
        "ownership_structure": _safe_value(focus_profile, "Ownership_Structure"),
        "float_structure": _safe_value(focus_profile, "Float_Structure"),
        "supply_structure": _safe_value(focus_profile, "Supply_Structure"),
        "institutional_participation": _safe_value(focus_profile, "Institutional_Participation"),
        "index_eligibility": _safe_value(focus_profile, "Index_Eligibility"),
        "major_supply_events": _safe_value(focus_profile, "Major_Supply_Events"),
        "structural_notes": _safe_value(focus_profile, "Structural_Notes"),
        "supply_events": _records(focus_events_df),
        "event_counts_by_type": focus_event_counts_by_type,
    }

    comparison_context = {
        "comparison_assets": _records(comparison_profile_df),
        "comparison_count": len(comparison_profile_df),
        "dataset_event_counts_by_type": event_counts_by_type,
    }

    structural_summary = _build_structural_summary(
        focus_company=focus_company,
        focus_ticker=focus_ticker,
        focus_structure_type=focus_structure_type,
        focus_context=focus_context,
        focus_event_count=len(focus_events_df),
        comparison_count=len(comparison_profile_df),
    )

    observation_context = {
        "focus_asset_context": focus_context,
        "comparison_context": comparison_context,
        "dataset_context": {
            "asset_count": asset_count,
            "event_count": event_count,
            "available_tickers": profile_df["Ticker"].dropna().astype(str).tolist()
            if profile_df is not None and "Ticker" in profile_df.columns else [],
        },
        "structural_summary": structural_summary,
        "perspective_lenses": {
            "Fundamental Analyst": "What assumptions appear embedded within the current valuation?",
            "Risk Analyst": "Which future expectations appear most critical to sustaining current pricing?",
            "Portfolio Manager": "How might changing supply conditions influence participation, liquidity, and market behaviour?",
            "Economic Systems Architect": "How do expectations, ownership structures, liquidity, and price discovery interact through time?",
        },
    }

    focus_summary_labels = {
        "ownership_label": _safe_value(focus_profile, "Ownership_Structure")[:64],
        "float_label": _safe_value(focus_profile, "Float_Structure")[:64],
        "supply_label": _safe_value(focus_profile, "Supply_Structure")[:64],
        "participation_label": _safe_value(focus_profile, "Institutional_Participation")[:64],
    }

    return {
        "asset_count": asset_count,
        "event_count": event_count,
        "focus_ticker": focus_ticker,
        "focus_company": focus_company,
        "focus_structure_type": focus_structure_type,
        "focus_event_count": len(focus_events_df),
        "focus_profile": focus_profile,
        "focus_events": _records(focus_events_df),
        "comparison_profiles": _records(comparison_profile_df),
        "event_counts_by_type": event_counts_by_type,
        "focus_event_counts_by_type": focus_event_counts_by_type,
        "focus_summary_labels": focus_summary_labels,
        "structural_summary": structural_summary,
        "observation_context": observation_context,
    }
