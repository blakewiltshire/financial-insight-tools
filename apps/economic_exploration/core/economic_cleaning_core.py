import os
import sys
import pandas as pd
from datetime import datetime

# --- Add modules path dynamically ---
PROJECT_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
modules_path = os.path.join(PROJECT_BASE_PATH, "constants")
if modules_path not in sys.path:
    sys.path.append(modules_path)

from economic_series_map import ECONOMIC_SERIES_MAP

def flatten_series_map(econ_series_map: dict) -> dict:
    """
    Flattens nested ECONOMIC_SERIES_MAP to a simple {series_id: metadata} lookup.
    """
    flat_map = {}
    for country_data in econ_series_map.values():
        for theme_data in country_data.values():
            for template_data in theme_data.values():
                for series_id, metadata in template_data.items():
                    flat_map[series_id] = metadata
    return flat_map


# Precompute flattened lookup once
FLAT_SERIES_MAP = flatten_series_map(ECONOMIC_SERIES_MAP)


def clean_economic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a raw economic dataset using the flattened series map.

    - Standardizes date format
    - Renames columns based on series IDs
    - Converts numeric values
    - Derives Real GDP growth metrics
    """

    # Standardize date column
    if "observation_date" in df.columns:
        df.rename(columns={"observation_date": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Rename columns using flattened map
    rename_dict = {}
    for col in df.columns:
        if col in FLAT_SERIES_MAP:
            rename_dict[col] = FLAT_SERIES_MAP[col]["name"]
    df.rename(columns=rename_dict, inplace=True)

    # Convert to numeric
    for col in df.columns:
        if col != "date":
            if df[col].dtype == "object":
                df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort and clean
    df = df.drop_duplicates().sort_values(by="date").reset_index(drop=True)
    df = df.ffill()

    # GDP-specific metrics
    if "Real GDP (Level)" in df.columns:
        df["QoQ % Change"] = df["Real GDP (Level)"].pct_change() * 100
        df["YoY % Change"] = df["Real GDP (Level)"].pct_change(periods=4) * 100
        df["QoQ Annualized"] = ((1 + df["QoQ % Change"] / 100) ** 4 - 1) * 100

    return df

def clean_cblei_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["observation_date"], format="%m/%d/%Y", errors="coerce")
    df.drop(columns=["observation_date"], inplace=True, errors="ignore")

    rename_dict = {col: FLAT_SERIES_MAP[col]["name"] for col in df.columns if col in FLAT_SERIES_MAP}
    df.rename(columns=rename_dict, inplace=True)

    df = df[["date"] + [col for col in df.columns if col != "date"]].dropna()
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def clean_epu_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["observation_date"], format="%m/%d/%Y", errors="coerce")
    df.drop(columns=["observation_date"], inplace=True, errors="ignore")

    rename_dict = {col: FLAT_SERIES_MAP[col]["name"] for col in df.columns if col in FLAT_SERIES_MAP}
    df.rename(columns=rename_dict, inplace=True)

    df = df[["date"] + [col for col in df.columns if col != "date"]].dropna()
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
