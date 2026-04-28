# -------------------------------------------------------------------------------------------------
# Relative Transmission Interpretation
# -------------------------------------------------------------------------------------------------

"""
Reusable structural interpretation layer for Relative Macro Transmission.

Purpose:
- Keep page orchestration clean
- Provide stronger, scalable, non-leading interpretation text
- Avoid weak fallbacks like:
  'The relationship between X and Y is being assessed.'
"""

# -------------------------------------------------------------------------------------------------
# Helpers — Context Naming
# -------------------------------------------------------------------------------------------------
def _extract_country_from_label(label):
    if not label:
        return "The selected system"

    if " — " in label:
        return label.split(" — ", maxsplit=1)[0].strip()

    return label


def _extract_surface_from_label(label):
    if not label:
        return "selected surface"

    if " — " in label:
        return label.split(" — ", maxsplit=1)[1].strip()

    return label


def _extract_anchor_currency_name(fx_label):
    if not fx_label:
        return "anchor currency"

    mapping = {
        "Dollar Strength Benchmark": "broad dollar terms",
        "Euro Dollar Pair": "USD",
        "Dollar Yen Pair": "JPY",
        "Sterling Dollar Pair": "USD",
        "Dollar Swiss Franc Pair": "CHF",
        "Australian Dollar Pair": "USD",
        "New Zealand Dollar Pair": "USD",
        "Dollar Canadian Dollar Pair": "CAD",
        "Dollar Norwegian Krone Pair": "NOK",
        "Dollar Yuan Pair": "CNY",
        "Dollar Hong Kong Dollar Pair": "HKD",
        "Dollar Singapore Dollar Pair": "SGD",
        "Dollar Rupee Pair": "INR",
        "Dollar Brazilian Real Pair": "BRL",
        "Dollar Mexican Peso Pair": "MXN",
        "Dollar Rand Pair": "ZAR",
        "Euro Sterling Pair": "GBP",
        "Euro Yen Pair": "JPY",
        "Australian Dollar Yen Pair": "JPY",
    }

    surface = _extract_surface_from_label(fx_label)
    return mapping.get(surface, surface)


# -------------------------------------------------------------------------------------------------
# Structural Interpretation Templates
# -------------------------------------------------------------------------------------------------

STATE_TEMPLATES = {
    "Aligned": (
        "{a} and {b} remain broadly aligned relative to their recent historical range."
    ),

    "Mild Divergence": (
        "{a} and {b} are beginning to move apart relative to their recent historical range."
    ),

    "Material Divergence": (
        "{a} and {b} shows a more visible divergence relative to its recent historical range."
    ),

    "Regime Shift": (
        "The relationship between {a} and {b} has shifted materially relative to its recent historical pattern."
    ),

    "Re-coupling": (
        "{a} and {b} are moving back towards their recent historical relationship."
    ),

    "N/A": (
        "{a} and {b} do not yet have enough stable overlap for structural classification."
    ),
}


USE_CASE_SUFFIX = {
    "Custom Comparison": (
        "This reflects whether the relationship is stabilising, diverging, or moving back towards alignment."
    ),

    "Relative Wealth": (
        "Relative return leadership and currency-adjusted wealth conditions remain central to the comparison."
    ),

    "Interest Rate Differential & Carry": (
        "Rate structure and carry conditions shape how financing pressure moves across the selected systems."
    ),

    "External Balance & Capital Flow": (
        "External funding conditions and capital movement determine how balance and constraint develop across the selected systems."
    ),

    "Commodity & FX Transmission": (
        "Commodity-linked pricing and foreign exchange conditions shape how external pressure moves through the comparison."
    ),

    "Sovereign vs Equity Divergence": (
        "Funding conditions and market performance often diverge before broader repricing becomes visible."
    ),

    "Positioning & Market Structure": (
        "Exposure concentration and market structure help explain how pressure builds beneath price movement."
    ),
}


# -------------------------------------------------------------------------------------------------
# Public Builder
# -------------------------------------------------------------------------------------------------
def build_contextual_insight(use_case, result, observation_context):
    """
    User-first structural interpretation.

    Design principle:
    - generic by state
    - specific by use case
    - useful for screenshots and narrative outputs
    - non-leading
    """

    state = result.get("regime_label", "N/A")

    primary_label = observation_context.get("primary")
    comparison_label = observation_context.get("comparison")
    anchor_pair_label = observation_context.get("anchor_pair")

    primary_country = _extract_country_from_label(primary_label)
    comparison_country = _extract_country_from_label(comparison_label)
    primary_surface = _extract_surface_from_label(primary_label)
    comparison_surface = _extract_surface_from_label(comparison_label)
    anchor_currency = _extract_anchor_currency_name(anchor_pair_label)

    # Relative Wealth is the only case where we want a slightly different surface description
    # because the comparison is equity surface + anchor FX pair.
    if use_case == "Relative Wealth":
        wealth_surface = f"{primary_country}'s equity wealth surface in {anchor_currency} terms"
        state_sentence = STATE_TEMPLATES.get(
            state,
            "{a} and {b} are being compared across the selected historical range."
        ).format(
            a=wealth_surface,
            b="its recent historical baseline",
        ).replace(" and its recent historical baseline", "")
        suffix = USE_CASE_SUFFIX[use_case]
        return f"{state_sentence} {suffix}"

    state_sentence = STATE_TEMPLATES.get(
        state,
        "{a} and {b} are being compared across the selected historical range."
    ).format(
        a=primary_surface,
        b=comparison_surface,
    )

    suffix = USE_CASE_SUFFIX.get(
        use_case,
        "This highlights how the selected conditions are evolving relative to one another."
    )

    return f"{state_sentence} {suffix}"
