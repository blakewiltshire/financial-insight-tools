# -------------------------------------------------------------------------------------------------
# Relationship Mapping Loader — Financial Insight Tools
# -------------------------------------------------------------------------------------------------
"""
Loads Relationship Manager seed data.

This loader is intentionally thin:
- business capability tags describe what companies do
- relationship tags describe why a company may matter to an observation
- FIT modules perform the actual market examination
"""

from __future__ import annotations

import os
from typing import Iterable, List, Optional

import pandas as pd


def load_business_capability_map(base_path: str) -> pd.DataFrame:
    """Load the generated US large-cap business capability map."""
    path = os.path.join(base_path, "us_large_business_capability_map.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing business capability map: {path}")
    return pd.read_csv(path)


def load_business_tag_registry(base_path: str) -> pd.DataFrame:
    """Load the business capability tag registry."""
    path = os.path.join(base_path, "business_capability_tag_registry.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing business tag registry: {path}")
    return pd.read_csv(path)


def load_relationship_tag_registry(base_path: str) -> pd.DataFrame:
    """Load the relationship tag registry."""
    path = os.path.join(base_path, "relationship_tag_registry_v1.csv")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing relationship tag registry: {path}")
    return pd.read_csv(path)


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
    """
    Filter rows where any selected tag appears in a semicolon-separated tag column.
    """
    selected = {tag.strip() for tag in selected_tags if str(tag).strip()}
    if not selected:
        return df.copy()

    mask = df[column].apply(lambda value: bool(selected.intersection(_normalise_tags(value))))
    return df[mask].copy()


def search_companies(
    df: pd.DataFrame,
    text: Optional[str] = None,
    business_tags: Optional[Iterable[str]] = None,
    relationship_tags: Optional[Iterable[str]] = None,
    fit_price_available_only: bool = False,
) -> pd.DataFrame:
    """
    Search candidate companies by free text, business tags, relationship-candidate tags,
    and current FIT price-data availability.
    """
    result = df.copy()

    if text:
        term = text.lower().strip()
        result = result[
            result["ticker"].astype(str).str.lower().str.contains(term, na=False)
            | result["company_name"].astype(str).str.lower().str.contains(term, na=False)
            | result["company_overview"].astype(str).str.lower().str.contains(term, na=False)
            | result["business_tags"].astype(str).str.lower().str.contains(term, na=False)
            | result["relationship_candidates_draft"].astype(str).str.lower().str.contains(term, na=False)
        ]

    result = filter_by_any_tag(result, business_tags or [], "business_tags")
    result = filter_by_any_tag(result, relationship_tags or [], "relationship_candidates_draft")

    if fit_price_available_only and "fit_price_available" in result.columns:
        result = result[result["fit_price_available"].astype(str).str.lower().isin(["true", "1", "yes"])]

    return result.reset_index(drop=True)
