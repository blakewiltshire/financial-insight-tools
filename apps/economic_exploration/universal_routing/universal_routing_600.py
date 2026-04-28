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
    FULL_HISTORY_INDICATORS = set()

    # ---------------------------------------------------------------------------------------------
    # Full History Override
    # ---------------------------------------------------------------------------------------------
    if indicator_name in FULL_HISTORY_INDICATORS:
        if indicator_name in {
            "Forward Development Intent",
            "Construction Conversion Flow",
            "Supply Delivery Progress",
        }:
            return df_dict.get("df_full")

        if indicator_name in {
            "Mortgage Borrowing Cost",
            "Housing Affordability Pressure",
            "Financing Condition Shift",
        }:
            return df_dict.get("df_secondary_full")

        if indicator_name in {
            "Curve Slope Positioning",
            "Macro Expectation Shift",
            "Liquidity Regime Signal",
        }:
            return df_dict.get("df_extended_full")

        if indicator_name in {
            "Government Debt Burden",
            "Public Debt Expansion",
        }:
            return df_dict.get("df_quarterly_sovereign_full")

        if indicator_name in {
            "Fiscal Balance Pressure",
            "Interest Burden on Output",
            "Interest Servicing Pressure",
            "Liquidity Cover Conditions",
        }:
            return df_dict.get("df_annual_sovereign_full")

        if indicator_name in {
            "Sovereign Yield Pressure",
            "Central Bank Balance Sheet Expansion",
            "System Financing Constraint",
        }:
            return df_dict.get("df_weekly_sovereign_full")

        if indicator_name in {
            "Investment Grade Spread Pressure",
            "High Yield Spread Pressure",
            "Distressed Credit Pressure",
        }:
            return df_dict.get("df_daily_credit_full")

        if indicator_name in {
            "Bank Cash Liquidity Conditions",
            "Bank Asset Capacity",
            "Bank Defensive Positioning",
        }:
            return df_dict.get("df_weekly_credit_full")

    # ---------------------------------------------------------------------------------------------
    # Housing Construction Cycle
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Forward Development Intent",
        "Construction Conversion Flow",
        "Supply Delivery Progress",
    }:
        return df_dict.get("df_primary_slice")

    # ---------------------------------------------------------------------------------------------
    # Mortgage Financing Conditions
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Mortgage Borrowing Cost",
        "Housing Affordability Pressure",
        "Financing Condition Shift",
    }:
        return df_dict.get("df_secondary_slice")

    # ---------------------------------------------------------------------------------------------
    # Yield Curve Structure
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Curve Slope Positioning",
        "Macro Expectation Shift",
        "Liquidity Regime Signal",
    }:
        return df_dict.get("df_extended_slice")

    # ---------------------------------------------------------------------------------------------
    # Sovereign Debt Sustainability
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Government Debt Burden",
        "Public Debt Expansion",
    }:
        return df_dict.get("df_quarterly_sovereign_slice")

    if indicator_name in {
        "Fiscal Balance Pressure",
        "Interest Burden on Output",
    }:
        return df_dict.get("df_annual_sovereign_slice")

    # ---------------------------------------------------------------------------------------------
    # Sovereign Liquidity and Refinancing Pressure
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Sovereign Yield Pressure",
        "System Financing Constraint",
        "Central Bank Balance Sheet Expansion",
    }:
        return df_dict.get("df_weekly_sovereign_slice")

    if indicator_name in {
        "Interest Servicing Pressure",
        "Liquidity Cover Conditions",
    }:
        return df_dict.get("df_annual_sovereign_slice")

    # ---------------------------------------------------------------------------------------------
    # Credit Conditions and Financing Pressure
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Investment Grade Spread Pressure",
        "High Yield Spread Pressure",
        "Distressed Credit Pressure",
    }:
        return df_dict.get("df_daily_credit_slice")

    # ---------------------------------------------------------------------------------------------
    # Bank Balance Sheet Liquidity and Credit Capacity
    # ---------------------------------------------------------------------------------------------
    if indicator_name in {
        "Bank Cash Liquidity Conditions",
        "Bank Asset Capacity",
        "Bank Defensive Positioning",
    }:
        return df_dict.get("df_weekly_credit_slice")

    # ---------------------------------------------------------------------------------------------
    # Default Fallback
    # ---------------------------------------------------------------------------------------------
    return df_dict.get("df_primary_slice")
