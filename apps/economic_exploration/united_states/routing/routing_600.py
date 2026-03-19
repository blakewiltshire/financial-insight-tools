# -------------------------------------------------------------------------------------------------
# 🔀 Routing Wrapper — Indicator Input Dispatcher
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📍 Local Routing Logic — Thematic Module Extension
---------------------------------------------------

Defines any country-specific or theme-specific routing overrides for indicators
requiring different dataframes than the universal default.

✅ Role in the System:
- Allows precise control where local data structures differ from global templates
- Ensures correct dataframe selection for signal evaluation during alignment scoring
- Pure string-matching logic based on full indicator names

🧠 AI Notes:
- Always performs exact string-based matching.
- No transformations occur; routing selects the correct cleaned dataframe slice.
- Use only where local extensions or composite datasets are implemented.

⚙️ Governance Structure:
1️⃣ Universal routing remains active as the global fallback.
2️⃣ This file extends or overrides routing for localised data structures.
3️⃣ All keys must match indicator names defined in `indicator_map_XXX.py`.

🧭 Governance Note:
- Local routing files are optional.
- They exist **only** when country-specific composite indicators or dataset disaggregation require adjustments.
"""

# -------------------------------------------------------------------------------------------------
# 🧱 Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# 🛠️ Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_routing"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 📦 Universal Routing Import
# -------------------------------------------------------------------------------------------------
from universal_routing_600 import get_indicator_input as get_indicator_input_universal

# -------------------------------------------------------------------------------------------------
# 📊 Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# 🚦 Local Routing Overrides
# -------------------------------------------------------------------------------------------------
WEEKLY_INDICATORS = {
    "Mortgage Borrowing Cost",
    "Housing Affordability Pressure",
    "Financing Condition Shift",
}

DAILY_INDICATORS = {
    "Curve Slope Positioning",
    "Macro Expectation Shift",
    "Liquidity Regime Signal",
}

def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    """
    Retrieves the dataframe corresponding to the given indicator.

    Logic:
    - Weekly mortgage indicators route to df_secondary_slice
    - Daily yield curve indicators route to df_extended_slice
    - Everything else falls back to universal routing dispatcher

    Parameters:
        indicator_name (str): Name of the indicator from use case
        df_dict (dict): Dictionary of available preloaded dataframes

    Returns:
        pd.DataFrame | None: Matching dataframe for the indicator
    """
    if indicator_name in WEEKLY_INDICATORS:
        return df_dict.get("df_secondary_slice")

    if indicator_name in DAILY_INDICATORS:
        return df_dict.get("df_extended_slice")

    return get_indicator_input_universal(indicator_name, df_dict)
