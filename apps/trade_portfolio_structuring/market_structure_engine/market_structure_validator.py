# -------------------------------------------------------------------------------------------------
# Market Structure Validator
# -------------------------------------------------------------------------------------------------
"""Validation and light cleaning for Market Structure Review datasets."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Required Columns
# -------------------------------------------------------------------------------------------------
REQUIRED_MARKET_STRUCTURE_COLUMNS = [
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

REQUIRED_MARKET_STRUCTURE_EVENT_COLUMNS = [
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
# Helpers
# -------------------------------------------------------------------------------------------------
def _clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == "object":
            cleaned_df[col] = cleaned_df[col].fillna("").astype(str).str.strip()
    return cleaned_df


def _validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    return [col for col in required_columns if col not in df.columns]

# -------------------------------------------------------------------------------------------------
# Profile Validation
# -------------------------------------------------------------------------------------------------
def validate_market_structure_df(df: pd.DataFrame) -> dict:
    """Validate market structure profile dataframe."""
    errors = []

    if df is None or df.empty:
        errors.append("Market structure profile dataset is empty.")
        return {"valid": False, "errors": errors, "cleaned_df": pd.DataFrame()}

    missing_cols = _validate_required_columns(df, REQUIRED_MARKET_STRUCTURE_COLUMNS)
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")

    if errors:
        return {"valid": False, "errors": errors, "cleaned_df": df}

    cleaned_df = _clean_text_columns(df)

    if cleaned_df["Company"].eq("").any():
        errors.append("Company column contains blank values.")

    if cleaned_df["Ticker"].eq("").any():
        errors.append("Ticker column contains blank values.")

    return {
        "valid": not errors,
        "errors": errors,
        "cleaned_df": cleaned_df,
    }

# -------------------------------------------------------------------------------------------------
# Events Validation
# -------------------------------------------------------------------------------------------------
def validate_market_structure_events_df(df: pd.DataFrame) -> dict:
    """Validate market structure supply-events dataframe."""
    errors = []

    if df is None or df.empty:
        errors.append("Market structure supply events dataset is empty.")
        return {"valid": False, "errors": errors, "cleaned_df": pd.DataFrame()}

    missing_cols = _validate_required_columns(df, REQUIRED_MARKET_STRUCTURE_EVENT_COLUMNS)
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")

    if errors:
        return {"valid": False, "errors": errors, "cleaned_df": df}

    cleaned_df = _clean_text_columns(df)

    if cleaned_df["Company"].eq("").any():
        errors.append("Company column contains blank values in supply events dataset.")

    if cleaned_df["Ticker"].eq("").any():
        errors.append("Ticker column contains blank values in supply events dataset.")

    return {
        "valid": not errors,
        "errors": errors,
        "cleaned_df": cleaned_df,
    }
