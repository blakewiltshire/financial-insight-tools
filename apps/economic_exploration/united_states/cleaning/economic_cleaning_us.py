"""
United States–specific economic data cleaners.

Includes:
- clean_cblei_csv: Conference Board Leading Economic Index.
- clean_epu_csv: Economic Policy Uncertainty Index.
"""

import pandas as pd
from shared.economic_cleaning_shared import FLAT_SERIES_MAP


def clean_cblei_csv(file_path: str) -> pd.DataFrame:
    """
    Cleans Conference Board Leading Index CSV.

    Args:
        file_path (str): Path to raw CB LEI file.

    Returns:
        pd.DataFrame: Cleaned LEI data with renamed columns.
    """
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(
        df["observation_date"], format="%m/%d/%Y", errors="coerce"
    )
    df.drop(columns=["observation_date"], inplace=True, errors="ignore")

    rename_dict = {
        col: FLAT_SERIES_MAP[col]["name"]
        for col in df.columns if col in FLAT_SERIES_MAP
    }
    df.rename(columns=rename_dict, inplace=True)

    df = df[["date"] + [col for col in df.columns if col != "date"]]
    df = df.dropna().sort_values("date").reset_index(drop=True)

    return df


def clean_epu_csv(file_path: str) -> pd.DataFrame:
    """
    Cleans Economic Policy Uncertainty Index CSV.

    Args:
        file_path (str): Path to raw EPU file.

    Returns:
        pd.DataFrame: Cleaned EPU data with renamed columns.
    """
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(
        df["observation_date"], format="%m/%d/%Y", errors="coerce"
    )
    df.drop(columns=["observation_date"], inplace=True, errors="ignore")

    rename_dict = {
        col: FLAT_SERIES_MAP[col]["name"]
        for col in df.columns if col in FLAT_SERIES_MAP
    }
    df.rename(columns=rename_dict, inplace=True)

    df = df[["date"] + [col for col in df.columns if col != "date"]]
    df = df.dropna().sort_values("date").reset_index(drop=True)

    return df
