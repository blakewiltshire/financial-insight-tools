# -------------------------------------------------------------------------------------------------
# Market Structure Loader
# -------------------------------------------------------------------------------------------------
"""
Loader utilities for Market Structure Review.

Loads curated market-structure profile datasets, curated supply-event datasets,
and user-upload templates.
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
MARKET_STRUCTURE_DATASETS = {
    "High-Profile IPOs": os.path.join(
        "data_sources",
        "financial_data",
        "market_structure",
        "curated",
        "high_profile_ipos_market_structure.csv",
    ),
}

MARKET_STRUCTURE_EVENT_DATASETS = {
    "High-Profile IPOs": os.path.join(
        "data_sources",
        "financial_data",
        "market_structure",
        "curated",
        "high_profile_ipos_supply_events.csv",
    ),
}

MARKET_STRUCTURE_COLUMNS = [
    "Company",
    "Ticker",
    "Exchange",
    "Structure_Type",
    "Ownership_Structure",
    "Float_Structure",
    "Supply_Structure",
    "Institutional_Participation",
    "Index_Eligibility",
    "Major_Supply_Events",
    "Structural_Notes",
]

MARKET_STRUCTURE_EVENT_COLUMNS = [
    "Company",
    "Ticker",
    "Event_Type",
    "Event_Date",
    "Event_Label",
    "Portion_Unlocked_Pct",
    "Condition",
    "Source_Note",
]

# -------------------------------------------------------------------------------------------------
# Templates
# -------------------------------------------------------------------------------------------------
def get_market_structure_template() -> pd.DataFrame:
    """Return an empty market structure profile template."""
    return pd.DataFrame(columns=MARKET_STRUCTURE_COLUMNS)


def get_market_structure_events_template() -> pd.DataFrame:
    """Return an empty market structure supply-events template."""
    return pd.DataFrame(columns=MARKET_STRUCTURE_EVENT_COLUMNS)

# -------------------------------------------------------------------------------------------------
# Curated Dataset Loaders
# -------------------------------------------------------------------------------------------------
def load_curated_market_structure_dataset(dataset_name: str, project_path: str) -> pd.DataFrame:
    """Load a curated market structure profile dataset."""
    if dataset_name not in MARKET_STRUCTURE_DATASETS:
        raise ValueError(f"Unsupported market structure dataset: {dataset_name}")

    csv_path = os.path.join(project_path, MARKET_STRUCTURE_DATASETS[dataset_name])

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Market structure dataset not found: {csv_path}")

    return pd.read_csv(csv_path)


def load_curated_market_structure_events(dataset_name: str, project_path: str) -> pd.DataFrame:
    """Load a curated market structure supply-events dataset."""
    if dataset_name not in MARKET_STRUCTURE_EVENT_DATASETS:
        raise ValueError(f"Unsupported market structure events dataset: {dataset_name}")

    csv_path = os.path.join(project_path, MARKET_STRUCTURE_EVENT_DATASETS[dataset_name])

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Market structure events dataset not found: {csv_path}")

    return pd.read_csv(csv_path)

# -------------------------------------------------------------------------------------------------
# User Upload Loaders
# -------------------------------------------------------------------------------------------------
def load_uploaded_market_structure_dataset(uploaded_file) -> pd.DataFrame:
    """Load an uploaded market structure profile dataset."""
    if uploaded_file is None:
        return get_market_structure_template()

    return pd.read_csv(uploaded_file)


def load_uploaded_market_structure_events(uploaded_file) -> pd.DataFrame:
    """Load an uploaded market structure supply-events dataset."""
    if uploaded_file is None:
        return get_market_structure_events_template()

    return pd.read_csv(uploaded_file)
