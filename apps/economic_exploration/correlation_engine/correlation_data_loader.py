# -------------------------------------------------------------------------------------------------
# 🔗 Universal Correlation Data Loader (Hardened - Production Grade)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Core ingestion loader for correlation engine:
- Robust CSV parsing (thousands separators, mixed formats)
- Defensive date handling (mixed exports, bad rows, duplicates)
- Frequency harmonisation to monthly (weekly/quarterly/monthly)
- Returns standardised metadata for downstream diagnostics
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys
from typing import Any, Dict, Optional, Tuple

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "registry")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "correlation_engine")))

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
    "Euro Area": "ea",
}

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_series_cleanup(series: pd.Series) -> pd.Series:
    """
    Ensures:
    - datetime index
    - sorted index
    - no NaT
    - no duplicate timestamps (keep last)
    - numeric dtype (coerce invalid to NaN, then drop)
    """
    if series is None or series.empty:
        return series

    idx = pd.to_datetime(series.index, errors="coerce")
    series = series.copy()
    series.index = idx

    # Drop bad dates
    series = series[~series.index.isna()]

    # Sort
    series = series.sort_index()

    # Drop duplicate timestamps (critical for resample/reindex)
    series = series[~series.index.duplicated(keep="last")]

    # Numeric coercion (read_csv(thousands=',' ) helps, but some columns still arrive as object)
    series = pd.to_numeric(series, errors="coerce").dropna()

    return series


def _harmonise_to_monthly(series: pd.Series, frequency_raw: str) -> pd.Series:
    """
    Harmonise a series to monthly frequency.

    Rules:
    - Quarterly: convert to quarter-end timestamps, dedupe, then forward-fill to monthly.
    - Monthly: forward-fill to month-end.
    - Weekly: aggregate to weekly mean, then monthly mean.
    - Unknown: forward-fill to monthly (best-effort).
    """
    if series is None or series.empty:
        return series

    freq = (frequency_raw or "").strip().lower()

    # Always clean before any resample
    series = _safe_series_cleanup(series)

    if series.empty:
        return series

    if "quarter" in freq:
        # Collapse to quarter-end, then monthly
        series.index = series.index.to_period("Q").to_timestamp("Q")
        series = series.sort_index()
        series = series[~series.index.duplicated(keep="last")]
        series = series.resample("M").ffill()

    elif "month" in freq:
        series = series.resample("M").ffill()

    elif "week" in freq:
        # Weekly -> Monthly (mean)
        series = series.resample("W").mean()
        series = series.resample("M").mean()

    else:
        # Best-effort: treat as low frequency and forward-fill
        series = series.resample("M").ffill()

    # Final cleanup (ensures resample didn't create oddities)
    series = _safe_series_cleanup(series)

    return series


def _find_registry_entry(
    indicator_obj: Dict[str, Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Find the indicator entry within ECONOMIC_SERIES_MAP for this indicator_obj.

    Returns:
        (entry_dict, error_message)
    """
    try:
        country = indicator_obj["country"]
        theme_code = indicator_obj["theme_code"]
        indicator_name = indicator_obj["indicator_name"]

        theme_block = ECONOMIC_SERIES_MAP[country][theme_code]

        for template_key in theme_block:
            if indicator_name in theme_block[template_key]:
                return theme_block[template_key][indicator_name], None

        return None, f"Indicator metadata not found for '{indicator_name}' in {country} ➔ {theme_code}"

    except KeyError as e:
        return None, f"Metadata key missing: {str(e)}"
    except Exception:
        return None, f"Metadata not found for {indicator_obj.get('country')} ➔ {indicator_obj.get('theme_code')}"


# -------------------------------------------------------------------------------------------------
# Main Loader Function
# -------------------------------------------------------------------------------------------------
def load_indicator_data(
    indicator_obj: Dict[str, Any],
    root_path: str,
) -> Tuple[Optional[pd.Series], Optional[Dict[str, Any]], str]:
    """
    Loads a single indicator series from file based on ingestion object.

    Args:
        indicator_obj (dict): indicator metadata from ingestion selector
        root_path (str): base root path from get_named_paths()

    Returns:
        pd.Series | None: time series (monthly harmonised)
        dict | None: standardised metadata fields
        str: status message (empty if success)
    """

    # --- Validate country mapping ---
    country = indicator_obj.get("country")
    country_code = COUNTRY_FOLDER_MAP.get(country)

    if not country_code:
        return None, None, f"No folder mapping for country: {country}"

    # --- Resolve registry entry ---
    entry, err = _find_registry_entry(indicator_obj)
    if err:
        return None, None, err

    folder = entry.get("folder", "")
    filename = entry.get("filename", "")
    frequency_raw = entry.get("frequency", "")
    seasonal_raw = entry.get("seasonal_adjustment", "")
    value_type_raw = entry.get("value_type", "")
    unit_type_raw = entry.get("unit_type", "")

    if not folder or not filename:
        return None, None, f"Invalid registry entry (missing folder/filename) for {country}: {indicator_obj.get('indicator_name')}"

    full_path = os.path.join(
        root_path,
        "apps",
        "data_sources",
        "economic_data",
        country_code,
        folder,
        filename,
    )

    if not os.path.exists(full_path):
        return None, None, f"File not found: {full_path}"

    # --- Read CSV safely ---
    try:
        df = pd.read_csv(full_path, thousands=",")
    except Exception as e:
        return None, None, f"Error reading file: {full_path} ({str(e)})"

    if "date" not in df.columns:
        return None, None, f"Missing 'date' column in file: {filename}"

    # Parse date column; drop invalid
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).copy()
    df = df.sort_values("date")
    df = df.set_index("date")

    # --- Extract column ---
    column_name = indicator_obj.get("indicator_name")
    if not column_name:
        return None, None, "Indicator name missing in indicator_obj"

    if column_name not in df.columns:
        return None, None, f"Column '{column_name}' not found in file: {filename}"

    series = df[column_name].dropna()
    series = _safe_series_cleanup(series)

    if series is None or series.empty:
        return None, None, f"No data available for: {country} — {column_name}"

    # --- Harmonise frequency to monthly ---
    try:
        series = _harmonise_to_monthly(series, frequency_raw)
    except Exception as e:
        return None, None, f"Frequency harmonisation failed for {country} — {column_name}: {str(e)}"

    if series is None or series.empty:
        return None, None, f"No usable data after harmonisation for: {country} — {column_name}"

    series.name = f"{country} — {column_name}"

    # --- Metadata standardisation for diagnostics ---
    seasonal, value_type, unit_type = standardise_metadata_fields(
        {
            "seasonal_adjustment": seasonal_raw,
            "value_type": value_type_raw,
            "unit_type": unit_type_raw,
        }
    )

    metadata_standardised = {
        "country": country,
        "indicator": column_name,
        "frequency_raw": frequency_raw,
        "seasonal": seasonal,
        "value_type": value_type,
        "unit_type": unit_type,
    }

    return series, metadata_standardised, ""
