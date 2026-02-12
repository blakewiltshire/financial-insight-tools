# -------------------------------------------------------------------------------------------------
# 📈 Economic Growth Stability — Routing Logic
# -------------------------------------------------------------------------------------------------
# This module provides the country-specific routing for indicator inputs used in the
# Economic Growth & Stability thematic grouping. It extends or overrides the default
# universal routing logic as needed.
#
# If no local modifications are necessary, the universal function is reused as-is.
#
# ✅ Safe to leave unmodified unless country-specific routing logic is required.
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

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
# 📦 Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys
import pandas as pd

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_routing"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_routing_100 import get_indicator_input as get_indicator_input_universal

# -------------------------------------------------------------------------------------------------
# 🔁 Indicator Routing Entry Point
# -------------------------------------------------------------------------------------------------
def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    """
    Returns the appropriate input DataFrame for a given indicator.

    Args:
        indicator_name (str): Name of the economic indicator (from indicator map).
        df_dict (dict): Dictionary of cleaned and sliced DataFrames (standardised keys).

    Returns:
        pd.DataFrame | None: Dataset used for signal generation.
    """
    return get_indicator_input_universal(indicator_name, df_dict)
