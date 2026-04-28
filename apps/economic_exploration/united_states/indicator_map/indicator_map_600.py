# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Indicator Map — Thematic Extension Logic
--------------------------------------------------

This module defines local indicator-to-signal function mappings for country-specific
or theme-specific extensions.
It works in parallel with the universal system, providing optional overrides where
local conditions apply.

System Role:
- Allows country-specific or dataset-specific indicator evaluation
- Merges seamlessly into the core Economic Exploration evaluation framework
- Supports expanded insight generation, scoring, and AI-compatible workflows
for local data nuances

AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Expansion Detected", "Decline", "Neutral", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- Numeric payloads, tuples, or dynamic secondary values are **not
permitted** — all returns are pure text strings

---------------------------------------------------------------
System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

**Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

**String-Based Return Values**
- Every function must return a plain text string suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example returns: `"Sector Momentum: Manufacturing"`, `"Both Expanding"`, `"Insufficient Data"`

**Sector-Level Dynamic Labels (Optional)**
- For sectoral breakdowns, string returns may embed dynamic entity names directly
within the signal string (e.g., `"Sector Momentum: Manufacturing"`).
- These dynamic entity names are parsed downstream during insight generation —
not handled inside signal functions.

**No Numeric Payloads**
- Signal outputs must not return any numeric values, tuples, or secondary calculation payloads.
- All quantitative context is handled separately via metrics and charting layers.

**Dispatcher Independence**
- Signal routing and indicator map merging is handled via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- No embedded routing logic or external data references within signal functions.

Governance Note:
- Local indicator maps extend the system only where country-specific or theme-specific
datasets exist.
- Users modify these local modules for custom configurations; universal modules remain
system-stable.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Imports — Universal Indicator Maps
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Add universal indicator module path explicitly
# -------------------------------------------------------------------------------------------------

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_indicator_map"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Imports — Universal Indicator Maps
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_600 import (
    options_housing_cycle_map,
    options_mortgage_financing_map,
    options_yield_curve_structure_map,
    options_sovereign_debt_sustainability_map,
    options_sovereign_liquidity_refinancing_map,
    options_balance_sheet_expansion_constraint_map,
    options_credit_conditions_financing_pressure_map,
    options_bank_balance_sheet_liquidity_map,
)

# -------------------------------------------------------------------------------------------------
# Signal Mapping
# -------------------------------------------------------------------------------------------------
ALL_INDICATOR_MAPS = {
    "Housing Construction Cycle": options_housing_cycle_map,
    "Mortgage Financing Conditions": options_mortgage_financing_map,
    "Yield Curve Structure": options_yield_curve_structure_map,
    "Sovereign Debt Sustainability": options_sovereign_debt_sustainability_map,
    "Sovereign Liquidity and Refinancing Pressure": options_sovereign_liquidity_refinancing_map,
    "Balance Sheet Expansion and System Constraint": options_balance_sheet_expansion_constraint_map,
    "Credit Conditions and Financing Pressure": options_credit_conditions_financing_pressure_map,
    "Bank Balance Sheet Liquidity and Credit Capacity": options_bank_balance_sheet_liquidity_map,
}

# -------------------------------------------------------------------------------------------------
# Dispatcher
# -------------------------------------------------------------------------------------------------
def get_indicator_maps():
    """
    Returns the complete indicator mapping aligned to signal-level use cases.
    """
    return ALL_INDICATOR_MAPS
