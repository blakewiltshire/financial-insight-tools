# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Universal Routing Logic — Thematic Module Dispatcher
------------------------------------------------------

Provides the deterministic dataset routing logic for all themes within the Economic Exploration suite.

Role in the System:
- Routes each indicator name to its correct cleaned dataset for signal evaluation
- Prevents routing ambiguity across mixed-frequency or multi-source datasets
- Governs which dataframe slice (e.g. primary, secondary, extended, full) each signal function operates on

AI Persona Notes:
- This routing map operates strictly on exact string matching.
- No data manipulation occurs — pure dataframe dispatch.

Structural Governance:
Each indicator name must match entries from `indicator_map_XXX.py`
Output routing keys must match `df_dict` keys (e.g., "df_primary_slice", "df_secondary_slice")
FULL_HISTORY_INDICATORS allows designation of indicators requiring full-length data (if applicable).

Governance Note:
- This file is maintained centrally for each thematic grouping.
- Local routing extensions exist only if special country-specific overrides are required.

"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Universal Routing Dispatcher
# -------------------------------------------------------------------------------------------------
def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    """
    Determines which dataframe to use for a given indicator name based on universal logic.

    Parameters:
        indicator_name (str): The name of the indicator.
        df_dict (dict): Dictionary of available dataframes.

    Returns:
        pd.DataFrame | None: Routed dataframe input.
    """

    # ---------------------------------------------------------------------------------------------
    # Currency Regime Framework
    # ---------------------------------------------------------------------------------------------
    if indicator_name == "Currency Strength Position":
        return df_dict.get("df_primary_slice")

    if indicator_name == "Reserve Stability Conditions":
        return df_dict.get("df_secondary_slice")

    if indicator_name == "Current Account Support":
        return df_dict.get("df_tertiary_slice")

    # ---------------------------------------------------------------------------------------------
    # Fallback
    # ---------------------------------------------------------------------------------------------
    return df_dict.get("df_primary_slice")
