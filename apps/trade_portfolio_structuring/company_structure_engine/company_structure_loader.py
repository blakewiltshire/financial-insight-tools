# -------------------------------------------------------------------------------------------------
# Company Structure Loader
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring

"""
Company Structure Loader
------------------------

Loads curated or user-supplied company valuation datasets for the
Company Structure Review module.

This loader does not fetch live market data. It reads structured CSV files
and returns dataframes for downstream validation, peer comparison, and
AI-ready observation export.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------------------------
COMPANY_VALUATION_DATASETS = {
    "Equities - Magnificent Seven": os.path.join(
        "data_sources",
        "financial_data",
        "company_valuation",
        "curated",
        "equities_mag7_valuations.csv",
    ),
    "Equities - Sector Constituents": os.path.join(
        "data_sources",
        "financial_data",
        "company_valuation",
        "curated",
        "equities_constituents_valuations.csv",
    ),
}


COMPANY_VALUATION_COLUMNS = [
    "Company",
    "Ticker",
    "Trailing_PE",
    "Forward_PE",
    "Revenue_Growth_Pct",
    "Operating_Margin_Pct",
    "Short_Interest_Pct",
]


# -------------------------------------------------------------------------------------------------
# Template
# -------------------------------------------------------------------------------------------------
def get_company_valuation_template() -> pd.DataFrame:
    return pd.DataFrame(
        columns=COMPANY_VALUATION_COLUMNS
    )


# -------------------------------------------------------------------------------------------------
# Curated Dataset Loader
# -------------------------------------------------------------------------------------------------
def load_curated_company_dataset(dataset_name: str, project_path: str) -> pd.DataFrame:
    if dataset_name not in COMPANY_VALUATION_DATASETS:
        raise ValueError(f"Unsupported company valuation dataset: {dataset_name}")

    csv_path = os.path.join(
        project_path,
        COMPANY_VALUATION_DATASETS[dataset_name],
    )

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Company valuation dataset not found: {csv_path}")

    return pd.read_csv(csv_path)


# -------------------------------------------------------------------------------------------------
# User Upload Loader
# -------------------------------------------------------------------------------------------------
def load_uploaded_company_dataset(uploaded_file) -> pd.DataFrame:
    if uploaded_file is None:
        return pd.DataFrame(columns=COMPANY_VALUATION_COLUMNS)

    return pd.read_csv(uploaded_file)
