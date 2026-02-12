# -------------------------------------------------------------------------------------------------
# 🔗 Correlation Harmonisation Engine — Metadata Standardisation Layer (Fully Expanded Version)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
This module provides canonical mappings to standardise metadata fields from ingestion registry.
It enables consistent messaging, diagnostics, and safeguards inside the correlation engine.
"""

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Seasonal Adjustment
# -------------------------------------------------------------------------------------------------
SEASONAL_STANDARDISATION_MAP = {
    "Seasonally Adjusted Annual Rate": "SAAR",
    "Seasonally adjusted at annual rates": "SAAR",
    "Seasonally Adjusted (annualized)": "SAAR",
    "Seasonally Adjusted": "SA",
    "Calendar and seasonally adjusted data [Y]": "SAAR",
    "Not Seasonally Adjusted": "NSA",
    "Non seasonal adjustment annual": "NSA",
    "Not adjusted": "NSA",
    "": "Unknown"
}

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Value Type
# -------------------------------------------------------------------------------------------------
VALUE_TYPE_STANDARDISATION_MAP = {
    "Level": "Level",
    "Component": "Level",
    "Percent": "Percent",
    "Share of GDP": "Percent",
    "Index": "Index",
    "Diffusion Index": "Index",
    "Ratio": "Ratio",
    "Growth Rate": "Rate",
    "Rate": "Rate",
    "": "Unknown"
}

# -------------------------------------------------------------------------------------------------
# Canonical Mappings for Unit Type (Unit Scale Harmonisation)
# -------------------------------------------------------------------------------------------------
UNIT_TYPE_STANDARDISATION_MAP = {
    # United States variants
    "Billions of Dollars": "Billions",
    "Chained Volume Measures, USD Billions": "Billions",

    # UK
    "Chained Volume Measures, GBP Millions": "Billions",
    "GBP Millions": "Billions",

    # Europe
    "Chained Volume Measures, EUR Millions": "Billions",
    "EUR Millions": "Billions",

    # Canada
    "Chained Volume Measures, CAD Millions": "Billions",
    "CAD Millions": "Billions",

    # Japan
    "Chained Volume Measures, Yen Billions": "Billions",

    # General other mappings
    "Millions of Local Currency": "Billions",
    "Thousands of Persons": "Millions",
    "Thousands": "Millions",
    "Millions of Persons": "Millions",
    "Dollars per Hour": "Currency",
    "USD per Hour": "Currency",
    "Percent": "Percent",
    "Index": "Index",
    "Units": "Units",
    "Number": "Units",
    "": "Unknown"
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

# -------------------------------------------------------------------------------------------------
# End of Harmonisation Engine
# -------------------------------------------------------------------------------------------------
