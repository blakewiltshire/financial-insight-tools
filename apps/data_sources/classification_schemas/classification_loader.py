# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Classification Loader Module

Provides structured loading for classification schema datasets, including geopolitical ratings,
market status, and company-level registry data. Company register data is separated into a global
registry (across regions) and a dedicated US large-cap combined profile and classification file.

Returns:
    dict: A dictionary containing DataFrames for:
        - "forum": Forum membership matrix
        - "political": Political and economic classifications
        - "market": Sovereign credit ratings
        - "company_base": Global company register (Amer/APAC/EMEA)
        - "company_largecap": US large-cap combined profile and classification table
Raises:
    FileNotFoundError: If any required dataset is missing
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Load All Classification Datasets
# -------------------------------------------------------------------------------------------------
def load_all_classification_data(base_path):
    """
    Loads classification schema datasets from the given base path.

    Args:
        base_path (str): Absolute path to the classification_schemas/ directory.

    Returns:
        dict: Dictionary containing all loaded and structured classification data.
    """
    data_path = os.path.join(base_path, "data")

    # Expected files
    expected_files = {
        "forum": "Grouped_Forum_Membership_Matrix.csv",
        "political": "political_stability_ratings.csv",
        "market": "market_ratings.csv",
        "amer": "amer_company_register.csv",
        "apac": "apac_company_register.csv",
        "emea": "emea_company_register.csv",
        "largecap_combined": "us_large_cap_combined.csv"
    }

    # Validate existence
    for label, filename in expected_files.items():
        file_path = os.path.join(data_path, filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Missing required dataset: '{filename}' ({label})")

    # Load general classification datasets
    df_forum = pd.read_csv(os.path.join(data_path, expected_files["forum"]))
    df_political = pd.read_csv(os.path.join(data_path, expected_files["political"]))
    df_market = pd.read_csv(os.path.join(data_path, expected_files["market"]))

    # Load global company register
    amer = pd.read_csv(os.path.join(data_path, expected_files["amer"]))
    apac = pd.read_csv(os.path.join(data_path, expected_files["apac"]))
    emea = pd.read_csv(os.path.join(data_path, expected_files["emea"]))
    df_company_base = pd.concat([amer, apac, emea], ignore_index=True)

    # Load US large-cap combined file (profiles + crosswalk)
    df_company_largecap = pd.read_csv(os.path.join(data_path, expected_files["largecap_combined"]))

    return {
        "forum": df_forum,
        "political": df_political,
        "market": df_market,
        "company_base": df_company_base,
        "company_largecap": df_company_largecap
    }
