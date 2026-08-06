# -------------------------------------------------------------------------------------------------
# Relationship Mapping Loader — Financial Insight Tools
# -------------------------------------------------------------------------------------------------
"""
Loads Relationship Manager seed data.

This loader is intentionally thin:
- regional company maps describe which businesses possess each capability
- business capability tags define the canonical vocabulary
- capability relationships define how an investigation may travel
- FIT modules perform the actual market examination
"""

from __future__ import annotations

import os
from typing import Iterable, List, Optional

import pandas as pd


REGIONAL_CAPABILITY_FILES = {
    "United States": "us_large_business_capability_map.csv",
    "Europe": "emea_large_business_capability_map.csv",
}


def load_business_capability_map(
    base_path: str,
    region: str = "United States",
) -> pd.DataFrame:
    """Load the company capability map for the selected relationship region."""
    if region not in REGIONAL_CAPABILITY_FILES:
        supported = ", ".join(REGIONAL_CAPABILITY_FILES)
        raise ValueError(
            f"Unsupported relationship region: {region}. Supported regions: {supported}"
        )

    path = os.path.join(base_path, REGIONAL_CAPABILITY_FILES[region])
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Missing {region} business capability map: {path}"
        )

    required_columns = {
        "ticker",
        "company_name",
        "country",
        "primary_business_tag",
        "business_tags",
        "company_overview",
    }
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(
            f"{region} business capability map is missing required columns: "
            + ", ".join(sorted(missing))
        )

    return df


def load_business_tag_registry(base_path: str) -> pd.DataFrame:
    """Load the canonical business capability tag registry."""
    path = os.path.join(base_path, "business_capability_tag_registry.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing business capability registry: {path}")

    required_columns = {"business_tag", "tag_group", "description"}
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(
            "Business capability registry is missing required columns: "
            + ", ".join(sorted(missing))
        )

    return df


def load_business_relationship_registry(base_path: str) -> pd.DataFrame:
    """Load the canonical capability-to-capability relationship registry."""
    path = os.path.join(
        base_path,
        "business_capability_relationship_registry.csv",
    )
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Missing business capability relationship registry: {path}"
        )

    required_columns = {
        "business_tag",
        "related_business_tag",
        "relationship_group",
        "relationship_direction",
        "relationship_description",
    }
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(
            "Business capability relationship registry is missing required columns: "
            + ", ".join(sorted(missing))
        )

    return df


# Backwards-compatible alias for older imports.
def load_relationship_tag_registry(base_path: str) -> pd.DataFrame:
    """Load the canonical capability relationship registry."""
    return load_business_relationship_registry(base_path)


def _normalise_tags(value: object) -> List[str]:
    """Normalise semicolon-separated tag strings into a clean list."""
    if pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(";") if item.strip()]


def filter_by_any_tag(
    df: pd.DataFrame,
    selected_tags: Iterable[str],
    column: str,
) -> pd.DataFrame:
    """Filter rows where any selected tag appears in a semicolon-separated field."""
    selected = {str(tag).strip() for tag in selected_tags if str(tag).strip()}
    if not selected:
        return df.copy()

    if column not in df.columns:
        return df.iloc[0:0].copy()

    mask = df[column].apply(
        lambda value: bool(selected.intersection(_normalise_tags(value)))
    )
    return df[mask].copy()


def search_companies(
    df: pd.DataFrame,
    text: Optional[str] = None,
    business_tags: Optional[Iterable[str]] = None,
    countries: Optional[Iterable[str]] = None,
    fit_price_available_only: bool = False,
) -> pd.DataFrame:
    """
    Search candidate companies by text, canonical capability, country and
    optional FIT price-data availability.
    """
    result = df.copy()

    if text:
        term = text.lower().strip()
        searchable_columns = [
            "ticker",
            "company_name",
            "country",
            "company_overview",
            "primary_business_tag",
            "business_tags",
        ]
        masks = [
            result[column]
            .astype(str)
            .str.lower()
            .str.contains(term, regex=False, na=False)
            for column in searchable_columns
            if column in result.columns
        ]
        if masks:
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = combined_mask | mask
            result = result[combined_mask]

    result = filter_by_any_tag(
        result,
        business_tags or [],
        "business_tags",
    )

    selected_countries = {
        str(country).strip()
        for country in (countries or [])
        if str(country).strip()
    }
    if selected_countries and "country" in result.columns:
        result = result[result["country"].isin(selected_countries)]

    if fit_price_available_only and "fit_price_available" in result.columns:
        result = result[
            result["fit_price_available"]
            .astype(str)
            .str.lower()
            .isin(["true", "1", "yes"])
        ]

    return result.reset_index(drop=True)
