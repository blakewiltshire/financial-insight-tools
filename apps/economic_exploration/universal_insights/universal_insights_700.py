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
    # Country External Balance
    # ---------------------------------------------------------------------------------------------
    "Export Conditions": {
        "Export Conditions Strengthening": {
            "bias": "Growth Supportive",
            "text": (
                "Exports of goods and services are strengthening relative to recent norms, "
                "suggesting firmer external demand and improved support from trade-facing activity."
            )
        },
        "Export Conditions Stable": {
            "bias": "Neutral",
            "text": (
                "Exports of goods and services are broadly stable, indicating limited recent "
                "change in external demand conditions."
            )
        },
        "Export Conditions Softening": {
            "bias": "Contraction Warning",
            "text": (
                "Exports of goods and services are softening relative to recent norms, which may "
                "suggest weaker external demand and reduced support from trade-facing activity."
            )
        }
    },

    "Import Conditions": {
        "Import Pressure Rising": {
            "bias": "Contraction Warning",
            "text": (
                "Imports of goods and services are rising relative to recent norms, suggesting "
                "greater external outflow pressure across the trade balance structure."
            )
        },
        "Import Conditions Stable": {
            "bias": "Neutral",
            "text": (
                "Imports of goods and services are broadly stable, indicating limited recent "
                "change in external demand leakage through imports."
            )
        },
        "Import Pressure Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Imports of goods and services are easing relative to recent norms, suggesting "
                "some moderation in external outflow pressure."
            )
        }
    },

    "Trade Balance Position": {
        "Trade Balance Improving": {
            "bias": "Growth Supportive",
            "text": (
                "The trade balance is improving relative to recent norms, suggesting stronger "
                "external balance conditions across goods and services."
            )
        },
        "Trade Balance Stable": {
            "bias": "Neutral",
            "text": (
                "The trade balance is broadly stable, indicating limited recent change in "
                "external balance conditions."
            )
        },
        "Trade Balance Deteriorating": {
            "bias": "Contraction Warning",
            "text": (
                "The trade balance is deteriorating relative to recent norms, which may indicate "
                "weaker external balance conditions across goods and services."
            )
        }
    },

    "Current Account Position": {
        "Current Account Improving": {
            "bias": "Growth Supportive",
            "text": (
                "The current account position is improving relative to recent norms, suggesting "
                "firmer external balance support at the broader economy level."
            )
        },
        "Current Account Stable": {
            "bias": "Neutral",
            "text": (
                "The current account position is broadly stable, indicating limited recent change "
                "in the wider external balance backdrop."
            )
        },
        "Current Account Weakening": {
            "bias": "Contraction Warning",
            "text": (
                "The current account position is weakening relative to recent norms, which may "
                "suggest softer external balance support."
            )
        }
    },

    "Reserve Layer Support": {
        "Reserve Support Strengthening": {
            "bias": "Growth Supportive",
            "text": (
                "Official reserves excluding gold are strengthening relative to recent norms, "
                "suggesting a firmer reserve support layer within the external balance structure."
            )
        },
        "Reserve Support Stable": {
            "bias": "Neutral",
            "text": (
                "Official reserves excluding gold are broadly stable, indicating limited recent "
                "change in reserve layer support."
            )
        },
        "Reserve Support Softening": {
            "bias": "Contraction Warning",
            "text": (
                "Official reserves excluding gold are softening relative to recent norms, which may "
                "indicate a weaker reserve support layer."
            )
        }
    },

    # ---------------------------------------------------------------------------------------------
    # External Constraint Capital Flow
    # ---------------------------------------------------------------------------------------------
    "Current Account Anchor": {
        "External Anchor Improving": {
            "bias": "Growth Supportive",
            "text": (
                "The current account anchor is improving relative to recent norms, suggesting "
                "firmer external funding support and reduced balance pressure."
            )
        },
        "External Anchor Stable": {
            "bias": "Neutral",
            "text": (
                "The current account anchor is broadly stable, indicating limited recent change "
                "in external funding conditions."
            )
        },
        "External Anchor Weakening": {
            "bias": "Contraction Warning",
            "text": (
                "The current account anchor is weakening relative to recent norms, which may "
                "suggest softer external funding support and greater balance pressure."
            )
        }
    },

    "Net International Position": {
        "Net International Position Improving": {
            "bias": "Growth Supportive",
            "text": (
                "The net international investment position is improving relative to recent norms, "
                "suggesting a firmer external asset-liability backdrop."
            )
        },
        "Net International Position Stable": {
            "bias": "Neutral",
            "text": (
                "The net international investment position is broadly stable, indicating limited "
                "recent change in the external asset-liability structure."
            )
        },
        "Net International Position Deteriorating": {
            "bias": "Contraction Warning",
            "text": (
                "The net international investment position is deteriorating relative to recent norms, "
                "which may indicate a weaker external asset-liability backdrop."
            )
        }
    },

    "Investment Income Pressure": {
        "Investment Income Pressure Rising": {
            "bias": "Contraction Warning",
            "text": (
                "Primary investment income payments are rising relative to recent norms, suggesting "
                "greater outward income pressure across the external accounts."
            )
        },
        "Investment Income Pressure Stable": {
            "bias": "Neutral",
            "text": (
                "Primary investment income payments are broadly stable, indicating limited recent "
                "change in outward income pressure."
            )
        },
        "Investment Income Pressure Easing": {
            "bias": "Growth Supportive",
            "text": (
                "Primary investment income payments are easing relative to recent norms, suggesting "
                "some moderation in outward income pressure across the external accounts."
            )
        }
    },

    "Reserve Support Conditions": {
        "Reserve Conditions Strengthening": {
            "bias": "Growth Supportive",
            "text": (
                "Official reserves excluding gold are strengthening relative to recent norms, "
                "suggesting firmer reserve support within the broader external constraint structure."
            )
        },
        "Reserve Conditions Stable": {
            "bias": "Neutral",
            "text": (
                "Official reserves excluding gold are broadly stable, indicating limited recent "
                "change in reserve support conditions."
            )
        },
        "Reserve Conditions Softening": {
            "bias": "Contraction Warning",
            "text": (
                "Official reserves excluding gold are softening relative to recent norms, which may "
                "indicate weaker reserve support within the broader external constraint structure."
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
