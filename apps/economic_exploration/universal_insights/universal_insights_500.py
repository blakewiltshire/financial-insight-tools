# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Insight Map — Structured Narrative Layer (Theme-Independent Template)
-------------------------------------------------------------------------------

This module defines universal, plain-language insights and bias classifications for system-wide
macroeconomic signals. It serves as the primary interpretive layer supporting AI narratives,
insight panels, macro alignment scoring, and external DSS agents.

System Role:
- Delivers standardised insight text and directional bias for all signals across themes
- Supports AI export narratives, scoring overlays, and structured observation pipelines
- Used automatically when no local override is present in `insight_XXX.py` modules

AI Persona Alignment Notes:
- Insight functions return:
    • Textual insight strings (e.g., "Growth remains above trend")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona reflection and export modules

System Structure & Compatibility:
**Strict String Matching**
    - Signal names must match exactly the outputs from `indicator_map_XXX.py` functions.
    - No inference or dynamic mapping allowed.

**Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`
    (or approved equivalents)

**Dispatcher Consistency**
    - Interface includes:
        - `indicator` (signal key)
        - `value` (signal string)
        - `timeframe` (pass-through parameter)
        - `extra_value` (optional; unused for universal module but preserved for
        interface consistency)

**No Embedded Logic**
    - This module performs no calculations or evaluations.
    - All inputs are fully processed signal strings passed from upstream evaluation logic.

Governance Note:
- This universal insight map is system-stable and globally applied.
- Country-specific or theme-specific extensions occur via local `insight_XXX.py` files only.
"""

# -------------------------------------------------------------------------------------------------
# Insight Dictionary
# -------------------------------------------------------------------------------------------------
insights = {

    # ---------------------------------------------------------------------------------------------
    # Money Supply and Velocity Dynamics
    # ---------------------------------------------------------------------------------------------
    "Narrow Money Conditions": {
        "Narrow Liquidity Expanding": {
            "bias": "Growth Supportive",
            "text": (
                "Narrow money supply is expanding relative to its recent trend, "
                "suggesting increased liquidity availability and faster short-cycle "
                "monetary transmission across the system."
            )
        },
        "Narrow Liquidity Stable": {
            "bias": "Neutral",
            "text": (
                "Narrow money supply is broadly stable, indicating liquidity conditions "
                "are holding close to recent norms without material expansion or contraction."
            )
        },
        "Narrow Liquidity Contracting": {
            "bias": "Contraction Warning",
            "text": (
                "Narrow money supply is contracting relative to its recent trend, "
                "which may suggest tighter short-cycle liquidity conditions."
            )
        }
    },

    "Broad Money Conditions": {
        "Broad Liquidity Expanding": {
            "bias": "Growth Supportive",
            "text": (
                "Broad money supply is expanding, suggesting wider system liquidity "
                "conditions remain supportive across households, institutions, and credit channels."
            )
        },
        "Broad Liquidity Stable": {
            "bias": "Neutral",
            "text": (
                "Broad money supply is broadly stable, indicating no significant shift "
                "in wider monetary conditions."
            )
        },
        "Broad Liquidity Contracting": {
            "bias": "Contraction Warning",
            "text": (
                "Broad money supply is contracting, suggesting broader liquidity conditions "
                "may be tightening across the financial system."
            )
        }
    },

    "Narrow Money Velocity": {
        "Narrow Money Circulation Accelerating": {
            "bias": "Growth Supportive",
            "text": (
                "Narrow money velocity is accelerating, indicating faster circulation "
                "of short-cycle liquidity through the economy."
            )
        },
        "Narrow Money Circulation Stable": {
            "bias": "Neutral",
            "text": (
                "Narrow money velocity is broadly stable, suggesting circulation "
                "patterns remain close to recent norms."
            )
        },
        "Narrow Money Circulation Slowing": {
            "bias": "Contraction Warning",
            "text": (
                "Narrow money velocity is slowing, which may indicate weaker circulation "
                "and reduced transaction activity."
            )
        }
    },

    "Broad Money Velocity": {
        "Broad Money Circulation Accelerating": {
            "bias": "Growth Supportive",
            "text": (
                "Broad money velocity is accelerating, suggesting faster movement "
                "of liquidity across the wider economy."
            )
        },
        "Broad Money Circulation Stable": {
            "bias": "Neutral",
            "text": (
                "Broad money velocity is broadly stable, indicating system-wide "
                "circulation remains close to recent trends."
            )
        },
        "Broad Money Circulation Slowing": {
            "bias": "Contraction Warning",
            "text": (
                "Broad money velocity is slowing, which may indicate weaker circulation "
                "and softer demand conditions."
            )
        }
    },

    # ---------------------------------------------------------------------------------------------
    # Interest Rate Regime and Transmission
    # ---------------------------------------------------------------------------------------------
    "Policy Rate Positioning": {
        "Policy Stance Tightening": {
            "bias": "Contraction Warning",
            "text": (
                "Central bank policy rates are rising relative to recent norms, "
                "suggesting a tighter monetary stance and greater system constraint."
            )
        },
        "Policy Stance Stable": {
            "bias": "Neutral",
            "text": (
                "Policy rates are broadly stable, indicating no material change "
                "in the central bank policy stance."
            )
        },
        "Policy Stance Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Policy rates are easing relative to recent norms, suggesting a more "
                "supportive monetary stance."
            )
        }
    },

    "Funding Rate Conditions": {
        "Funding Conditions Tightening": {
            "bias": "Contraction Warning",
            "text": (
                "Short-term funding rates are rising, indicating tighter liquidity "
                "conditions within money markets."
            )
        },
        "Funding Conditions Stable": {
            "bias": "Neutral",
            "text": (
                "Funding rates are broadly stable, suggesting liquidity conditions "
                "remain close to recent norms."
            )
        },
        "Funding Conditions Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Funding rates are easing, indicating improved liquidity conditions "
                "within short-term funding markets."
            )
        }
    },

    "Bank Lending Rate Pressure": {
        "Bank Lending Pressure Rising": {
            "bias": "Contraction Warning",
            "text": (
                "Prime lending rates are rising, suggesting tighter borrowing "
                "conditions for credit-sensitive activity."
            )
        },
        "Bank Lending Pressure Stable": {
            "bias": "Neutral",
            "text": (
                "Prime lending rates are broadly stable, indicating borrowing "
                "conditions are holding close to recent norms."
            )
        },
        "Bank Lending Pressure Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Prime lending rates are easing, suggesting less restrictive "
                "credit conditions."
            )
        }
    },

    "Mortgage Rate Conditions": {
        "Mortgage Conditions Tightening": {
            "bias": "Contraction Warning",
            "text": (
                "Mortgage borrowing costs are rising, suggesting tighter "
                "housing financing conditions."
            )
        },
        "Mortgage Conditions Stable": {
            "bias": "Neutral",
            "text": (
                "Mortgage borrowing costs are broadly stable relative to recent norms."
            )
        },
        "Mortgage Conditions Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Mortgage borrowing costs are easing, improving housing financing conditions."
            )
        }
    },

    "Treasury Curve Structure": {
        "Curve Steepening": {
            "bias": "Growth Supportive",
            "text": (
                "The yield curve is steepening relative to recent norms, which may "
                "indicate improving growth expectations and less compressed financial conditions."
            )
        },
        "Curve Stable": {
            "bias": "Neutral",
            "text": (
                "The yield curve structure is broadly stable."
            )
        },
        "Curve Flattening": {
            "bias": "Contraction Warning",
            "text": (
                "The yield curve is flattening, which may indicate tighter "
                "financial conditions or weaker growth expectations."
            )
        }
    },

    "Real Policy Rate Proxy": {
        "Real Policy Constraint Rising": {
            "bias": "Contraction Warning",
            "text": (
                "The proxy policy rate is rising relative to recent norms, "
                "suggesting increasing real policy constraint."
            )
        },
        "Real Policy Constraint Stable": {
            "bias": "Neutral",
            "text": (
                "The proxy policy rate remains broadly stable."
            )
        },
        "Real Policy Constraint Easing": {
            "bias": "Growth Supportive",
            "text": (
                "The proxy policy rate is easing, indicating less restrictive "
                "real policy conditions."
            )
        }
    }
}

# -------------------------------------------------------------------------------------------------
# Dispatcher Function
# -------------------------------------------------------------------------------------------------
def generate_universal_econ_insights(indicator: str, value: str, timeframe: str, extra_value=None) -> tuple[str, str]:
    """
    Returns universal insight text and bias classification for a given indicator signal.

    Parameters:
        indicator (str): Indicator key
        value (str): Signal output string (strict string match)
        timeframe (str): Timeframe (pass-through)
        extra_value: (optional, unused for universal, provided for interface compatibility)

    Returns:
        tuple[str, str]: (Insight narrative, bias classification)
    """
    try:
        data = insights[indicator][value]
        return data["text"], data.get("bias", "Neutral")
    except Exception:
        return "No insight available for this signal.", "Neutral"
