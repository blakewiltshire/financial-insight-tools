# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Use Case Definitions — Economic Exploration Core System
-----------------------------------------------------------------------

This module defines the default universal use case mappings for thematic modules within
the Economic Exploration suite. It governs UI structure, scoring alignment, and AI-supported
framing for any theme not explicitly overridden at country level.

System Role:
- Supplies standardised use case definitions to:
    • Charting engines (tab ordering, dropdown generation)
    • Macro alignment scoring panels
    • AI persona narrative structures and DSS exports
    • Placeholder rendering for unconfigured modules

AI Persona & DSS Notes:
- Use case keys must match entries used in:
    • `indicator_map_XXX.py`
    • `insight_XXX.py`
    • Scoring alignment modules `scoring_weights_labels_XXX.py`

- Clean, stable, interpretable keys are critical for:
    • AI export narratives
    • Observational journaling
    • Triangular navigation pathways across DSS

Structure & Interface Governance:
**Strict Key Consistency**
    - Use case names in this module must exactly match those referenced across indicator maps and insights.

**Indicator Registry**
    - Each use case includes a list of indicator signal labels used for scoring and insight evaluation.
    - These indicators must exist within the corresponding universal indicator maps.

**Metadata Inclusion**
    - Each use case includes:
        - `"Indicators"` → List of signals
        - `"Categories"` → UI grouping tags (used for streamlit tabs, filters)
        - `"Description"` → AI-assist narrative frame

Governance Note:
- This universal use case map provides system-wide default scaffolding.
- Local overrides per country or theme occur via local `use_cases_XXX.py`.
- No universal entries are modified by users directly — universal remains stable foundation.
"""

# -------------------------------------------------------------------------------------------------
# Use Cases
# -------------------------------------------------------------------------------------------------
USE_CASES = {
    "Housing Construction Cycle": {
        "Indicators": [
            "Forward Development Intent",
            "Construction Conversion Flow",
            "Supply Delivery Progress"
        ],
        "Categories": [
            "Housing Units Authorized",
            "Housing Units Started",
            "Housing Units Completed"
        ],
        "Description": (
            "Tracks the housing construction pipeline from approvals to active "
            "construction and completed supply delivery."
        )
    },
    "Mortgage Financing Conditions": {
        "Indicators": [
            "Mortgage Borrowing Cost",
            "Housing Affordability Pressure",
            "Financing Condition Shift"
        ],
        "Categories": [
            "Long-Term Mortgage Rate"
        ],
        "Description": (
            "Tracks long-term mortgage borrowing costs as a structural signal for "
            "housing affordability, credit-sensitive demand, and financing conditions."
        )
    },
    "Yield Curve Structure": {
        "Indicators": [
            "Curve Slope Positioning",
            "Macro Expectation Shift",
            "Liquidity Regime Signal"
        ],
        "Categories": [
            "Yield Curve Spread"
        ],
        "Description": (
            "Tracks the spread between long- and short-term government yields to "
            "observe macro expectations, liquidity conditions, and recession-sensitive "
            "financial structure."
        )
    },
    "Sovereign Debt Sustainability": {
        "Indicators": [
            "Government Debt Burden",
            "Fiscal Balance Pressure",
            "Interest Burden on Output"
        ],
        "Categories": [
            "Government Debt to GDP Ratio",
            "Government S/D % GDP",
            "Interest / GDP"
        ],
        "Description": (
            "Tracks sovereign debt burden, fiscal balance pressure, and interest burden "
            "relative to output to observe debt sustainability under changing macro conditions."
        )
    },
    "Sovereign Liquidity and Refinancing Pressure": {
        "Indicators": [
            "Sovereign Yield Pressure",
            "Interest Servicing Pressure",
            "Liquidity Cover Conditions"
        ],
        "Categories": [
            "US 10 Year Treasury Benchmark",
            "Interest / GDP",
            "Liquidity"
        ],
        "Description": (
            "Tracks sovereign refinancing conditions through benchmark yields, interest burden, "
            "and liquidity cover to observe fiscal pressure and rollover sensitivity."
        )
    },
    "Balance Sheet Expansion and System Constraint": {
        "Indicators": [
            "Public Debt Expansion",
            "Central Bank Balance Sheet Expansion",
            "System Financing Constraint"
        ],
        "Categories": [
            "Government Debt to GDP Ratio",
            "CB Balance Sheet as % of GDP",
            "US 10 Year Treasury Benchmark",
            "Liquidity"
        ],
        "Description": (
            "Tracks sovereign and central bank balance sheet expansion alongside financing "
            "conditions to observe how system constraint and policy capacity evolve."
        )
    },
    "Credit Conditions and Financing Pressure": {
        "Indicators": [
            "Investment Grade Spread Pressure",
            "High Yield Spread Pressure",
            "Distressed Credit Pressure"
        ],
        "Categories": [
            "Investment Grade Spread",
            "High Yield Spread",
            "CCC and Lower Spread"
        ],
        "Description": (
            "Tracks credit spread conditions across quality tiers to observe financing pressure, "
            "risk repricing, and capital availability across the system."
        )
    },
    "Bank Balance Sheet Liquidity and Credit Capacity": {
        "Indicators": [
            "Bank Cash Liquidity Conditions",
            "Bank Asset Capacity",
            "Bank Defensive Positioning"
        ],
        "Categories": [
            "Cash Assets",
            "Total Assets",
            "Treasury and Agency Securities"
        ],
        "Description": (
            "Tracks bank balance sheet liquidity, asset capacity, and defensive positioning "
            "to observe potential credit support or constraint within the banking system."
        )
    }
}


def get_use_cases():
    """
    Returns the placeholder use case structure for unconfigured thematic modules.

    Returns:
        dict: Generic use cases for UI and structural fallback.
    """
    return USE_CASES
