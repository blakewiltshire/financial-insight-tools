# -------------------------------------------------------------------------------------------------
# 🔗 Universal Correlation Data Loader (Hardened - Full Production Grade)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Core ingestion loader for correlation engine:
- Fully harmonised ingestion with mixed formatting tolerance
- Robust numeric parsing with thousands separator
- Date parsing fully neutralised for mixed regional exports
- Frequency harmonisation to monthly
- Returns full metadata for downstream diagnostics
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'registry')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'correlation_engine')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Load Ingestion Registry and Harmonisation Engine
# -------------------------------------------------------------------------------------------------
from economic_series_map import ECONOMIC_SERIES_MAP
from harmonisation_engine import standardise_metadata_fields

# -------------------------------------------------------------------------------------------------
# Country Code Mapping (ISO ➔ Folder Code)
# -------------------------------------------------------------------------------------------------
COUNTRY_FOLDER_MAP = {
    "United States": "us",
    "United Kingdom": "uk",
    "Germany": "de",
    "France": "fr",
    "Italy": "it",
    "Japan": "jp",
    "Canada": "ca",
    "Australia": "au",
    "China": "cn",
    "India": "in",
    "Brazil": "br",
    "Korea": "kr",
    "Euro Area": "ea"
}

# -------------------------------------------------------------------------------------------------
# Main Loader Function
# -------------------------------------------------------------------------------------------------

def load_indicator_data(indicator_obj, root_path):
    """
    Loads single indicator series from file based on ingestion object.

    Args:
        indicator_obj (dict): indicator metadata from ingestion selector
        root_path (str): base root path from get_named_paths()

    Returns:
        pd.Series: time series of indicator values (monthly harmonised)
        dict: standardised metadata fields
        str: status message (empty if success)
    """

    country = indicator_obj["country"]
    country_code = COUNTRY_FOLDER_MAP.get(country)

    if not country_code:
        return None, None, f"No folder mapping for country: {country}"

    theme_code = indicator_obj["theme_code"]
    indicator_id = indicator_obj["indicator_id"]

    try:
        metadata = ECONOMIC_SERIES_MAP[country][theme_code]
        for template_key in metadata:
            if indicator_obj["indicator_name"] in metadata[template_key]:
                entry = metadata[template_key][indicator_obj["indicator_name"]]
                folder = entry["folder"]
                filename = entry["filename"]
                frequency_raw = entry.get("frequency", "")
                seasonal_raw = entry.get("seasonal_adjustment", "")
                value_type_raw = entry.get("value_type", "")
                unit_type_raw = entry.get("unit_type", "")
                break
        else:
            return None, None, f"Indicator metadata not found for {indicator_id}"
    except Exception:
        return None, None, f"Metadata not found for {country} ➔ {theme_code}"

    full_path = os.path.join(
        root_path, "apps", "data_sources", "economic_data", country_code, folder, filename
    )

    if not os.path.exists(full_path):
        return None, None, f"File not found: {full_path}"

    # -------------------------------------------------------------------------------------------------
    # Universal Safe CSV Parsing (handles thousands separator)
    # -------------------------------------------------------------------------------------------------
    try:
        df = pd.read_csv(full_path, thousands=',')
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
        df.set_index("date", inplace=True)
    except Exception as e:
        return None, None, f"Error reading file: {full_path} ({str(e)})"

    column_name = indicator_obj["indicator_name"]

    if column_name not in df.columns:
        return None, None, f"Column '{column_name}' not found in file: {filename}"

    series = df[column_name].dropna()

    if series.empty:
        return None, None, f"No data available for: {country} — {column_name}"

    # -------------------------------------------------------------------------------------------------
    # Apply Frequency Harmonisation to Monthly
    # -------------------------------------------------------------------------------------------------

    frequency_raw_lower = frequency_raw.lower()

    if "quarter" in frequency_raw_lower:
        series.index = series.index.to_period('Q').to_timestamp('Q')
        series = series.resample('M').ffill()
    elif "month" in frequency_raw_lower:
        series = series.resample('M').ffill()
    elif "week" in frequency_raw_lower:
        series = series.resample('W').mean()
        series = series.resample('M').mean()
    else:
        series = series.resample('M').ffill()

    series.name = f"{country} — {column_name}"

    # -------------------------------------------------------------------------------------------------
    # Apply Metadata Standardisation for Diagnostics
    # -------------------------------------------------------------------------------------------------

    seasonal, value_type, unit_type = standardise_metadata_fields({
        "seasonal_adjustment": seasonal_raw,
        "value_type": value_type_raw,
        "unit_type": unit_type_raw
    })

    metadata_standardised = {
        "country": country,
        "indicator": column_name,
        "seasonal": seasonal,
        "value_type": value_type,
        "unit_type": unit_type
    }

    return series, metadata_standardised, ""

# -------------------------------------------------------------------------------------------------
# End of Correlation Data Loader
# -------------------------------------------------------------------------------------------------
