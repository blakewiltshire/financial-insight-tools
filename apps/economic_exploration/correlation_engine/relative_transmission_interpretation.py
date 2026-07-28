# -------------------------------------------------------------------------------------------------
# Relative Transmission Interpretation
# -------------------------------------------------------------------------------------------------

"""
Reusable structural interpretation layer for Relative Macro Transmission.

Purpose:
- Keep page orchestration clean
- Provide transformation-aware, evidence-bounded interpretation
- Describe the metric that was actually calculated
- Separate current level, historical position, and recent direction
- Avoid causal, predictive, or unsupported transition claims

Important engine contract:
- Difference regime state is based on the z-score of the difference series.
- Ratio and Relative % values/percentiles describe their own derived series, but the current
  regime state supplied by the engine is still based on the z-score of the difference series.
- Relative Z-Score regime state is based on the same standardised difference shown as the metric.
- Rolling Correlation has separate level and directional classifications.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import math


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


def _normalise_transformation_name(value):
    mapping = {
        "rolling_corr": "Rolling Correlation",
        "difference": "Difference",
        "ratio": "Ratio",
        "relative_pct": "Relative %",
        "zscore_spread": "Relative Z-Score",
    }

    return mapping.get(value, value)


# -------------------------------------------------------------------------------------------------
# Helpers — Safe Formatting
# -------------------------------------------------------------------------------------------------
def _as_finite_float(value):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(parsed):
        return None

    return parsed


def _format_number(value, decimals=3, signed=False):
    parsed = _as_finite_float(value)

    if parsed is None:
        return "unavailable"

    if signed:
        return f"{parsed:+.{decimals}f}"

    return f"{parsed:.{decimals}f}"


def _format_ordinal(value):
    parsed = _as_finite_float(value)

    if parsed is None:
        return None

    number = int(round(parsed))

    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd",
        }.get(number % 10, "th")

    return f"{number}{suffix}"


def _historical_position_sentence(percentile, metric_name):
    ordinal = _format_ordinal(percentile)

    if ordinal is None:
        return (
            f"A stable historical percentile is not yet available for the {metric_name}."
        )

    parsed = _as_finite_float(percentile)

    if parsed is None:
        position = "within its available historical distribution"
    elif parsed <= 10:
        position = "near the lower extreme of its available historical distribution"
    elif parsed <= 25:
        position = "in the lower part of its available historical distribution"
    elif parsed < 40:
        position = "below the centre of its available historical distribution"
    elif parsed <= 60:
        position = "around the middle of its available historical distribution"
    elif parsed < 75:
        position = "above the centre of its available historical distribution"
    elif parsed < 90:
        position = "in the upper part of its available historical distribution"
    else:
        position = "near the upper extreme of its available historical distribution"

    return (
        f"This sits at the {ordinal} percentile, placing the {metric_name} {position}."
    )


def _z_position_sentence(current_z):
    z_value = _as_finite_float(current_z)

    if z_value is None:
        return "A stable standardised spread position is not yet available."

    magnitude = abs(z_value)

    if magnitude < 0.005:
        return "The difference spread is effectively at its historical mean."

    direction = "above" if z_value > 0 else "below"

    return (
        f"The difference spread is {magnitude:.3f} standard deviations "
        f"{direction} its historical mean."
    )


def _clean_state_label(value):
    if not value:
        return "N/A"

    return str(value).strip()


# -------------------------------------------------------------------------------------------------
# Helpers — Use-Case Context
# -------------------------------------------------------------------------------------------------
USE_CASE_CONTEXT = {
    "Custom Comparison": (
        "The result describes the selected comparative measure and does not, by itself, "
        "establish causality or future direction."
    ),
    "Relative Wealth": (
        "The result provides a relative wealth comparison; interpretation remains dependent "
        "on the selected equity and currency construction."
    ),
    "Interest Rate Differential & Carry": (
        "The measure provides context for relative rate and carry conditions without determining "
        "the direction of subsequent asset pricing."
    ),
    "External Balance & Capital Flow": (
        "The measure provides context for relative external-balance conditions without identifying "
        "a causal transmission channel by itself."
    ),
    "Commodity & FX Transmission": (
        "The measure describes the selected commodity and market relationship without establishing "
        "that one series is driving the other."
    ),
    "Sovereign vs Equity Divergence": (
        "The measure identifies relative displacement between sovereign and equity surfaces; "
        "additional evidence is required before attributing a repricing mechanism."
    ),
    "Positioning & Market Structure": (
        "The measure provides comparative market-structure context and should be considered alongside "
        "liquidity, participation, positioning, and event evidence."
    ),
}


def _use_case_context_sentence(use_case):
    return USE_CASE_CONTEXT.get(
        use_case,
        "The result describes the selected relationship and does not, by itself, establish causality.",
    )


# -------------------------------------------------------------------------------------------------
# Transformation Builders
# -------------------------------------------------------------------------------------------------
def _build_difference_insight(
    use_case,
    result,
    primary_surface,
    comparison_surface,
):
    current_value = result.get("current_value")
    current_z = result.get("current_z")
    percentile = result.get("percentile")
    regime_label = _clean_state_label(result.get("regime_label"))

    return " ".join([
        (
            f"The current constructed difference between {primary_surface} and "
            f"{comparison_surface} is {_format_number(current_value)}."
        ),
        _historical_position_sentence(percentile, "difference"),
        _z_position_sentence(current_z),
        (
            f"The difference-spread regime is classified as {regime_label.lower()} "
            "relative to its available history."
        ),
        _use_case_context_sentence(use_case),
    ])


def _build_ratio_insight(
    use_case,
    result,
    primary_surface,
    comparison_surface,
):
    current_value = result.get("current_value")
    current_z = result.get("current_z")
    percentile = result.get("percentile")
    regime_label = _clean_state_label(result.get("regime_label"))

    return " ".join([
        (
            f"The current constructed ratio of {primary_surface} to "
            f"{comparison_surface} is {_format_number(current_value)}."
        ),
        _historical_position_sentence(percentile, "ratio"),
        (
            "The ratio should be interpreted as a relative-scale measure within this selected pair, "
            "rather than as a unit-free economic multiple unless the underlying series are directly comparable."
        ),
        _z_position_sentence(current_z),
        (
            f"The displayed regime state, {regime_label.lower()}, is based on the engine's "
            "underlying difference-spread classification rather than on the ratio value itself."
        ),
        _use_case_context_sentence(use_case),
    ])


def _build_relative_pct_insight(
    use_case,
    result,
    primary_surface,
    comparison_surface,
):
    current_value = result.get("current_value")
    current_z = result.get("current_z")
    percentile = result.get("percentile")
    regime_label = _clean_state_label(result.get("regime_label"))

    return " ".join([
        (
            f"The current relative-percentage measure for {primary_surface} against "
            f"{comparison_surface} is {_format_number(current_value)}%."
        ),
        _historical_position_sentence(percentile, "relative-percentage measure"),
        (
            "This expresses the current difference relative to the comparison-series value and is "
            "most meaningful where the selected series have a defensible proportional relationship."
        ),
        _z_position_sentence(current_z),
        (
            f"The displayed regime state, {regime_label.lower()}, is derived from the "
            "standardised difference between the selected series."
        ),
        _use_case_context_sentence(use_case),
    ])


def _build_relative_zscore_insight(
    use_case,
    result,
    primary_surface,
    comparison_surface,
):
    current_value = result.get("current_value")
    percentile = result.get("percentile")
    regime_label = _clean_state_label(result.get("regime_label"))
    z_value = _as_finite_float(current_value)

    if z_value is None:
        z_sentence = (
            f"A stable relative z-score is not yet available for {primary_surface} "
            f"and {comparison_surface}."
        )
    elif abs(z_value) < 0.005:
        z_sentence = (
            f"The standardised difference between {primary_surface} and {comparison_surface} "
            "is effectively at its historical mean."
        )
    else:
        direction = "above" if z_value > 0 else "below"
        z_sentence = (
            f"The standardised difference between {primary_surface} and {comparison_surface} "
            f"is {abs(z_value):.3f} standard deviations {direction} its historical mean."
        )

    return " ".join([
        z_sentence,
        _historical_position_sentence(percentile, "relative z-score"),
        (
            f"The standardised-spread regime is classified as {regime_label.lower()} "
            "relative to its available history."
        ),
        (
            "The sign identifies the direction of the displacement; the magnitude indicates "
            "how unusual that displacement is, not whether it will persist or reverse."
        ),
        _use_case_context_sentence(use_case),
    ])


def _build_rolling_correlation_insight(
    use_case,
    result,
    observation_context,
    primary_surface,
    comparison_surface,
):
    current_corr = _as_finite_float(result.get("current_corr"))
    percentile = result.get("percentile")
    current_corr_change = _as_finite_float(result.get("current_corr_change"))
    correlation_lookback = result.get("correlation_lookback", 6)
    regime_label = _clean_state_label(result.get("regime_label"))
    rolling_state = _clean_state_label(result.get("rolling_state"))
    window = observation_context.get("window")

    if current_corr is None:
        return (
            f"{primary_surface} and {comparison_surface} do not yet have enough stable overlap "
            "for rolling-correlation interpretation."
        )

    window_text = f"{window}-period " if window else ""

    if rolling_state == "Strengthening Transmission":
        direction_sentence = (
            f"Compared with {correlation_lookback} observations earlier, the rolling correlation "
            "has strengthened."
        )
    elif rolling_state == "Weakening Transmission":
        direction_sentence = (
            f"Compared with {correlation_lookback} observations earlier, the rolling correlation "
            "has weakened."
        )
    elif rolling_state == "Stable Transmission":
        direction_sentence = (
            f"Compared with {correlation_lookback} observations earlier, the rolling correlation "
            "has remained broadly stable."
        )
    else:
        direction_sentence = (
            "There is not yet enough recent rolling history to classify the direction of the relationship."
        )

    if current_corr_change is None:
        change_sentence = ""
    else:
        change_sentence = (
            f" The measured change over that comparison period is "
            f"{_format_number(current_corr_change, signed=True)}."
        )

    return " ".join([
        (
            f"The {window_text}rolling correlation between {primary_surface} and "
            f"{comparison_surface} is {current_corr:.3f}, indicating "
            f"{regime_label.lower()}."
        ),
        _historical_position_sentence(percentile, "rolling correlation"),
        f"{direction_sentence}{change_sentence}",
        (
            "Correlation describes the direction and strength of co-movement; it does not establish "
            "causality or guarantee that the relationship will continue."
        ),
        _use_case_context_sentence(use_case),
    ])


# -------------------------------------------------------------------------------------------------
# Relative Wealth Naming
# -------------------------------------------------------------------------------------------------
def _resolve_surfaces(
    use_case,
    primary_label,
    comparison_label,
    anchor_pair_label,
):
    primary_country = _extract_country_from_label(primary_label)
    primary_surface = _extract_surface_from_label(primary_label)
    comparison_surface = _extract_surface_from_label(comparison_label)

    if use_case != "Relative Wealth":
        return primary_surface, comparison_surface

    anchor_currency = _extract_anchor_currency_name(anchor_pair_label)
    wealth_surface = (
        f"{primary_country}'s equity wealth surface in {anchor_currency} terms"
    )

    return wealth_surface, primary_surface


# -------------------------------------------------------------------------------------------------
# Public Builder
# -------------------------------------------------------------------------------------------------
def build_contextual_insight(use_case, result, observation_context):
    """
    Build a transformation-aware structural interpretation.

    The function reports:
    - what the selected transformation measures;
    - the current derived value;
    - the derived metric's historical percentile;
    - the regime basis actually supplied by the engine;
    - directional evidence only where the engine calculates it.

    No sentence should imply causality, prediction, convergence, divergence through time,
    or reversion unless that property is explicitly measured.
    """
    primary_label = observation_context.get("primary")
    comparison_label = observation_context.get("comparison")
    anchor_pair_label = observation_context.get("anchor_pair")
    transformation = _normalise_transformation_name(
        observation_context.get("transformation")
    )

    primary_surface, comparison_surface = _resolve_surfaces(
        use_case=use_case,
        primary_label=primary_label,
        comparison_label=comparison_label,
        anchor_pair_label=anchor_pair_label,
    )

    builders = {
        "Difference": _build_difference_insight,
        "Ratio": _build_ratio_insight,
        "Relative %": _build_relative_pct_insight,
        "Relative Z-Score": _build_relative_zscore_insight,
    }

    if transformation == "Rolling Correlation":
        return _build_rolling_correlation_insight(
            use_case=use_case,
            result=result,
            observation_context=observation_context,
            primary_surface=primary_surface,
            comparison_surface=comparison_surface,
        )

    builder = builders.get(transformation)

    if builder is None:
        return (
            f"{primary_surface} and {comparison_surface} are being assessed using the selected "
            "comparative transformation. A transformation-specific interpretation is not available."
        )

    return builder(
        use_case=use_case,
        result=result,
        primary_surface=primary_surface,
        comparison_surface=comparison_surface,
    )
