# -------------------------------------------------------------------------------------------------
# Routing Wrapper — Indicator Input Dispatcher
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Routing Logic — Thematic Module Extension
---------------------------------------------------

Defines any country-specific or theme-specific routing overrides for indicators
requiring different dataframes than the universal default.

Role in the System:
- Allows precise control where local data structures differ from global templates
- Ensures correct dataframe selection for signal evaluation during alignment scoring
- Pure string-matching logic based on full indicator names

AI Notes:
- Always performs exact string-based matching.
- No transformations occur; routing selects the correct cleaned dataframe slice.
- Use only where local extensions or composite datasets are implemented.

Governance Structure:
- Universal routing remains active as the global fallback.
- This file extends or overrides routing for localised data structures.
- All keys must match indicator names defined in `indicator_map_XXX.py`.

Governance Note:
- Local routing files are optional.
- They exist **only** when country-specific composite indicators or dataset disaggregation require adjustments.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------

import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_routing"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_routing_100 import get_indicator_input as get_indicator_input_universal

# -------------------------------------------------------------------------------------------------
# Local Routing Overrides (Optional)
# -------------------------------------------------------------------------------------------------
COMPOSITE_MONTHLY_INDICATORS = {
    "National Activity Composite",     # CFNAI
    "Leading Economic Index (Conference Board)",       # CBLEI
    "Uncertainty Index Impact"         # EPU
}

COMPOSITE_WEEKLY_INDICATORS = {
    "Weekly Economic Index (NY Fed)"   # WEI
}

def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    if indicator_name in COMPOSITE_MONTHLY_INDICATORS:
        return df_dict.get("df_secondary_slice")
    if indicator_name in COMPOSITE_WEEKLY_INDICATORS:
        return df_dict.get("df_extended_slice")
    return get_indicator_input_universal(indicator_name, df_dict)
