# -------------------------------------------------------------------------------------------------
# Correlation Harmonisation Engine — Metadata Standardisation Layer
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
This module provides canonical mappings to standardise metadata fields from the ingestion registry.
It enables consistent messaging, diagnostics, and safeguards inside the correlation engine.
"""

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Seasonal Adjustment
# -------------------------------------------------------------------------------------------------
SEASONAL_STANDARDISATION_MAP = {
    "Seasonally Adjusted Annual Rate": "SAAR",
    "Seasonally adjusted at annual rates": "SAAR",
    "Seasonally Adjusted (annualized)": "SAAR",
    "Calendar and seasonally adjusted data [Y]": "SAAR",
    "Seasonally Adjusted": "SA",
    "Not Seasonally Adjusted": "NSA",
    "Non seasonal adjustment annual": "NSA",
    "Not adjusted": "NSA",
    "Not Applicable": "NA", 
    "": "Unknown",
}

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Value Type
# -------------------------------------------------------------------------------------------------
VALUE_TYPE_STANDARDISATION_MAP = {
    "Level": "Level",
    "level": "Level",
    "Component": "Component",
    "Percent": "Percent",
    "percent": "Percent",
    "Share of GDP": "Percent",
    "Index": "Index",
    "index": "Index",
    "Diffusion Index": "Index",
    "Ratio": "Ratio",
    "Rate": "Rate",
    "Growth Rate": "Rate",
    "Spread": "Spread",
    "": "Unknown",
}

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Unit Type
# -------------------------------------------------------------------------------------------------
UNIT_TYPE_STANDARDISATION_MAP = {
    # Real output / volume measures
    "Chained Volume Measures, USD Billions": "Real Billions",
    "Chained Volume Measures, GBP Millions": "Real Millions",
    "Chained Volume Measures, EUR Millions": "Real Millions",
    "Chained Volume Measures, CAD Millions": "Real Millions",
    "Chained Volume Measures, Yen Billions": "Real Billions",

    # Nominal / current-price currency measures
    "Billions of Dollars": "Nominal Billions",
    "Millions of Dollars": "Nominal Millions",
    "Current Prices, USD Billions": "Nominal Billions",
    "GBP Millions": "Nominal Millions",
    "EUR Millions": "Nominal Millions",
    "CAD Millions": "Nominal Millions",
    "Millions of Local Currency": "Nominal Millions",

    # Labour / persons
    "Thousands of Persons": "Millions of Persons",
    "Thousands": "Millions of Persons",
    "Millions of Persons": "Millions of Persons",

    # Earnings / flow rates
    "Dollars per Hour": "Currency Rate",
    "USD per Hour": "Currency Rate",

    # Standard scalar classes
    "Percent": "Percent",
    "Index": "Index",
    "Units": "Units",
    "Number": "Units",

    # Explicit placeholders
    "Unknown": "Unknown",
    "": "Unknown",
}

# -------------------------------------------------------------------------------------------------
# Helper Function to Standardise Single Metadata Entry
# -------------------------------------------------------------------------------------------------
def standardise_metadata_fields(entry):
    """
    Receives raw ingestion entry (dict), returns standardised canonical metadata.
    """
    seasonal_raw = entry.get("seasonal_adjustment", "")
    value_raw = entry.get("value_type", "")
    unit_raw = entry.get("unit_type", "")

    seasonal = SEASONAL_STANDARDISATION_MAP.get(seasonal_raw, "Unknown")
    value_type = VALUE_TYPE_STANDARDISATION_MAP.get(value_raw, "Unknown")
    unit_type = UNIT_TYPE_STANDARDISATION_MAP.get(unit_raw, "Unknown")

    return seasonal, value_type, unit_type
