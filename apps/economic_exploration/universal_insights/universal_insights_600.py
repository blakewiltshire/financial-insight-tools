# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧠 Universal Insight Map — Structured Narrative Layer (Theme-Independent Template)
-------------------------------------------------------------------------------

This module defines universal, plain-language insights and bias classifications for system-wide
macroeconomic signals. It serves as the primary interpretive layer supporting AI narratives,
insight panels, macro alignment scoring, and external DSS agents.

✅ System Role:
- Delivers standardised insight text and directional bias for all signals across themes
- Supports AI export narratives, scoring overlays, and structured observation pipelines
- Used automatically when no local override is present in `insight_XXX.py` modules

🧠 AI Persona Alignment Notes:
- Insight functions return:
    • Textual insight strings (e.g., "Growth remains above trend")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona reflection and export modules

⚙️ System Structure & Compatibility:
1️⃣ **Strict String Matching**
    - Signal names must match exactly the outputs from `indicator_map_XXX.py` functions.
    - No inference or dynamic mapping allowed.

2️⃣ **Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`
    (or approved equivalents)

3️⃣ **Dispatcher Consistency**
    - Interface includes:
        - `indicator` (signal key)
        - `value` (signal string)
        - `timeframe` (pass-through parameter)
        - `extra_value` (optional; unused for universal module but preserved for
        interface consistency)

4️⃣ **No Embedded Logic**
    - This module performs no calculations or evaluations.
    - All inputs are fully processed signal strings passed from upstream evaluation logic.

🧭 Governance Note:
- This universal insight map is system-stable and globally applied.
- Country-specific or theme-specific extensions occur via local `insight_XXX.py` files only.
"""

# -------------------------------------------------------------------------------------------------
# Insight Map
# -------------------------------------------------------------------------------------------------
insights = {
    "Forward Development Intent": {
        "Approvals Expanding": {
            "bias": "Growth Supportive",
            "text": "Housing authorizations are increasing, suggesting broader forward "
            "development intent within the residential construction pipeline."
        },
        "Approvals Stabilising": {
            "bias": "Neutral",
            "text": "Housing authorizations are broadly stable, indicating that forward "
            "development activity is holding without clear additional expansion."
        },
        "Approvals Softening": {
            "bias": "Contraction Warning",
            "text": "Housing authorizations are moderating, which may indicate softer "
            "forward development intent within the construction pipeline."
        }
    },

    "Construction Conversion Flow": {
        "Starts Accelerating": {
            "bias": "Growth Supportive",
            "text": "Housing starts are increasing, suggesting that approved projects are "
            "converting into active construction more strongly."
        },
        "Starts Stabilising": {
            "bias": "Neutral",
            "text": "Housing starts are broadly stable, indicating that active construction "
            "flow is being maintained without clear acceleration."
        },
        "Starts Slowing": {
            "bias": "Contraction Warning",
            "text": "Housing starts are easing, which may indicate slower conversion from "
            "approvals into active construction."
        }
    },

    "Supply Delivery Progress": {
        "Completions Rising": {
            "bias": "Growth Supportive",
            "text": "Housing completions are increasing, suggesting that new residential "
            "supply is entering the housing stock more actively."
        },
        "Completions Stable": {
            "bias": "Neutral",
            "text": "Housing completions are broadly stable, indicating that supply delivery "
            "is continuing without a major shift in pace."
        },
        "Completions Falling": {
            "bias": "Contraction Warning",
            "text": "Housing completions are declining, suggesting that the flow of newly "
            "delivered housing supply is easing."
        }
    },

    "Mortgage Borrowing Cost": {
        "Borrowing Costs Rising": {
            "bias": "Contraction Warning",
            "text": "Mortgage borrowing costs are increasing, suggesting tighter financing "
            "conditions for housing activity and greater sensitivity across credit-dependent demand."
        },
        "Borrowing Costs Stable": {
            "bias": "Neutral",
            "text": "Mortgage borrowing costs are broadly stable, indicating no major recent "
            "shift in baseline housing financing conditions."
        },
        "Borrowing Costs Easing": {
            "bias": "Growth Supportive",
            "text": "Mortgage borrowing costs are easing, suggesting some relief in housing "
            "financing conditions and a potentially more supportive backdrop for credit-sensitive demand."
        }
    },

    "Housing Affordability Pressure": {
        "Affordability Pressure Rising": {
            "bias": "Contraction Warning",
            "text": "Mortgage rate pressure is rising, indicating tighter affordability "
            "conditions for households exposed to housing finance costs."
        },
        "Affordability Pressure Stable": {
            "bias": "Neutral",
            "text": "Mortgage rate pressure is broadly stable, suggesting that affordability "
            "conditions are not shifting materially in the near term."
        },
        "Affordability Pressure Easing": {
            "bias": "Growth Supportive",
            "text": "Mortgage rate pressure is easing, suggesting some improvement in housing "
            "affordability conditions relative to recent levels."
        }
    },

    "Financing Condition Shift": {
        "Financing Tightening": {
            "bias": "Contraction Warning",
            "text": "Mortgage financing conditions are tightening, which may constrain housing "
            "demand, refinancing activity, and broader credit-sensitive construction momentum."
        },
        "Financing Stable": {
            "bias": "Neutral",
            "text": "Mortgage financing conditions are broadly stable, indicating limited "
            "recent change in the housing credit backdrop."
        },
        "Financing Easing": {
            "bias": "Growth Supportive",
            "text": "Mortgage financing conditions are easing, suggesting a more supportive "
            "credit environment for housing demand and construction-sensitive activity."
        }
    },

    "Curve Slope Positioning": {
        "Curve Steepening": {
            "bias": "Growth Supportive",
            "text": "The yield curve is steepening relative to its recent average, suggesting "
            "an improving slope structure often associated with firmer macro expectations and less compressed financial conditions."
        },
        "Curve Stable": {
            "bias": "Neutral",
            "text": "The yield curve is broadly stable, indicating little recent change in "
            "overall slope positioning across the maturity structure."
        },
        "Curve Flattening": {
            "bias": "Contraction Warning",
            "text": "The yield curve is flattening relative to its recent average, suggesting "
            "a more compressed macro structure often associated with softer expectations or tighter conditions."
        }
    },

    "Macro Expectation Shift": {
        "Macro Expectations Improving": {
            "bias": "Growth Supportive",
            "text": "The yield curve structure is improving relative to recent norms, suggesting "
            "firmer macro expectations across growth, inflation, or policy-sensitive interpretation."
        },
        "Macro Expectations Stable": {
            "bias": "Neutral",
            "text": "The yield curve is broadly unchanged versus recent history, indicating "
            "no major current shift in macro expectation structure."
        },
        "Macro Expectations Weakening": {
            "bias": "Contraction Warning",
            "text": "The yield curve structure is weakening relative to recent norms, which may "
            "indicate softer macro expectations or a more cautious market interpretation."
        }
    },

    "Liquidity Regime Signal": {
        "Liquidity Conditions Easing": {
            "bias": "Growth Supportive",
            "text": "The yield curve spread is widening relative to recent levels, suggesting "
            "a less compressed liquidity regime and a somewhat more supportive financial backdrop."
        },
        "Liquidity Conditions Stable": {
            "bias": "Neutral",
            "text": "The yield curve spread is broadly stable, indicating little recent shift "
            "in the wider liquidity regime signal."
        },
        "Liquidity Conditions Tightening": {
            "bias": "Contraction Warning",
            "text": "The yield curve spread is compressing relative to recent levels, suggesting "
            "a tighter liquidity regime and a more constrained financial backdrop."
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
