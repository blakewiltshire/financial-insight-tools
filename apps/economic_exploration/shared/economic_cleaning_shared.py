# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Shared economic data cleaning utilities.

Includes:
- flatten_series_map: Flattens ECONOMIC_SERIES_MAP to a flat lookup.
- FLAT_SERIES_MAP: Precomputed universal lookup dictionary.
- clean_economic_data: Cleans generic economic time series using shared schema.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import copy

# -------------------------------------------------------------------------------------------------
# Add universal use case path explicitly
# -------------------------------------------------------------------------------------------------
PROJECT_BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
CONSTANTS_PATH = os.path.join(PROJECT_BASE_PATH, "constants")
if CONSTANTS_PATH not in sys.path:
    sys.path.append(CONSTANTS_PATH)

# -------------------------------------------------------------------------------------------------
# Series Metadata Map (Used for Renaming and Enrichment)
# -------------------------------------------------------------------------------------------------
from economic_series_map import ECONOMIC_SERIES_MAP  # noqa: E402

def flatten_series_map(econ_series_map: dict) -> dict:
    """
    Flattens nested ECONOMIC_SERIES_MAP into a flat series_id → metadata lookup.
    Flattens all nested dict fields like 'release_schedule' for safe access.
    """
    flat_map = {}

    for country, country_data in econ_series_map.items():
        for theme, theme_data in country_data.items():
            for template, series_dict in theme_data.items():
                if isinstance(series_dict, dict):
                    for series_id, metadata in series_dict.items():
                        clean_meta = copy.deepcopy(metadata)

                        if "release_schedule" in clean_meta and isinstance(clean_meta["release_schedule"], dict):
                            for k, v in clean_meta["release_schedule"].items():
                                clean_meta[f"release_schedule:{k}"] = v
                            del clean_meta["release_schedule"]

                        flat_map[series_id] = clean_meta

    return flat_map

# --- Precomputed Lookup Map ---
FLAT_SERIES_MAP = flatten_series_map(ECONOMIC_SERIES_MAP)



def clean_economic_data(df: pd.DataFrame, theme: str = None) -> pd.DataFrame:
    """
    Cleans raw economic time series data using standardised metadata logic.

    Steps:
    - Rename 'observation_date' to 'date'
    - Apply friendly name mapping from FLAT_SERIES_MAP
    - Convert string values to numerics
    - Apply unit_multiplier if defined
    - Forward-fill missing values
    - Add theme component metrics where applicable

    Args:
        df (pd.DataFrame): Raw time series data from CSV or external API.
        theme (str): The theme module identifier for targeted logic (optional)

    Returns:
        pd.DataFrame: Cleaned, enriched, and chronologically ordered time series.
    """
    print(f"[DEBUG] Incoming data type: {type(df)}")

    if df is None or not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a valid pandas DataFrame.")

    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    if "observation_date" in df.columns:
        df.rename(columns={"observation_date": "date"}, inplace=True)

    if "date" not in df.columns:
        raise ValueError("Missing required 'date' column in dataset.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isna().all():
        raise ValueError("Failed to parse any valid dates in 'date' column.")

    df = df.dropna(subset=["date"])

    rename_dict = {
        col: FLAT_SERIES_MAP[col]["name"]
        for col in df.columns
        if col in FLAT_SERIES_MAP
    }
    df.rename(columns=rename_dict, inplace=True)

    reverse_rename_dict = {v: k for k, v in rename_dict.items()}

    for col in df.columns:
        if col != "date" and isinstance(col, str) and col in df:
            try:
                if df[col].dtype == object:
                    df[col] = df[col].str.replace(",", "", regex=False)
                df[col] = pd.to_numeric(df[col], errors="coerce")

                original_col = reverse_rename_dict.get(col)
                if original_col and original_col in FLAT_SERIES_MAP:
                    multiplier = FLAT_SERIES_MAP[original_col].get("unit_multiplier", 1)
                    if isinstance(multiplier, (int, float)) and multiplier != 1:
                        df[col] = df[col] * multiplier

            except Exception as e:
                print(f"[CLEANER ERROR] Failed on column: {col} — {type(e).__name__}: {str(e)}")


    df = df.drop_duplicates().sort_values(by="date").reset_index(drop=True)
    df = df.ffill()

    # --- THEME-SPECIFIC LOGIC ---
    if theme in [None, "100_economic_growth_stability"]:
        if "Real GDP (Level)" in df.columns:
            df["Real GDP QoQ % Change"] = df["Real GDP (Level)"].pct_change() * 100
            df["Real GDP YoY % Change"] = df["Real GDP (Level)"].pct_change(periods=4) * 100
            df["Real GDP QoQ Annualized"] = ((1 + df["Real GDP QoQ % Change"] / 100) ** 4 - 1) * 100

            component_prefixes = [
                "Real Personal Consumption Expenditures",
                "Real Gross Private Domestic Investment",
                "Government Consumption Expenditures and Gross Investment",
                "Real Exports of Goods and Services",
                "Real Imports of Goods and Services"
            ]
            for col in component_prefixes:
                if col in df.columns:
                    df[f"{col} QoQ % Change"] = df[col].pct_change() * 100
                    df[f"{col} YoY % Change"] = df[col].pct_change(periods=4) * 100

    elif theme == "000_template":
        pass

    elif theme == "200_labour_market_dynamics":
        pass

    elif theme == "300_consumer_behaviour_confidence":
        pass

    elif theme == "400_inflation_price_dynamics":
        pass

    elif theme == "500_monetary_indicators_policy_effects":
        pass

    elif theme == "600_financial_conditions_risk_analysis":
        pass

    elif theme == "700_global_trade_economic_relations":
        pass

    elif theme == "800_supply_chains_logistics":
        pass

    elif theme == "900_commodity_markets_pricing":
        pass

    elif theme == "1000_currency_exchange_movements":
        pass

    elif theme == "1100_market_trends_financial_health":
        pass

    elif theme == "1200_industry_performance_production":
        pass

    elif theme == "1300_sustainability_green_economy":
        pass

    elif theme == "1400_digital_economy_ecommerce":
        pass

    elif theme == "1500_innovation_rd_investment":
        pass

    elif theme == "1600_urbanisation_and_smart_cities":
        pass

    elif theme == "1700_healthcare_economics":
        pass

    elif theme == "1800_education_and_human_capital":
        pass

    elif theme == "1900_social_impact_and_inequality":
        pass

    elif theme == "2000_geopolitical_risks_and_global_stability":
        pass

    elif theme == "2010_frontier_sectors":
        pass

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Cleaned output is not a DataFrame — got: {type(df)}")

        if df.empty:
            raise ValueError("Cleaned DataFrame is empty.")

        return df


    print(f"[DEBUG] Returning data type: {type(df)} — Shape: {df.shape if isinstance(df, pd.DataFrame) else 'N/A'}")

    return df
