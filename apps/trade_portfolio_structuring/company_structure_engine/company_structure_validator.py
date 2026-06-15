# -------------------------------------------------------------------------------------------------
# Company Structure Validator
# -------------------------------------------------------------------------------------------------
# pylint: disable=missing-function-docstring

"""
Company Structure Validator
---------------------------

Validates uploaded and curated company valuation datasets used by the
Company Structure Review module.

Responsibilities:
- Validate required columns
- Standardise data types
- Preserve NaN values
- Clean common formatting issues
- Return validation metadata
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Required Schema
# -------------------------------------------------------------------------------------------------
REQUIRED_COLUMNS = [
    "Company",
    "Ticker",
    "Trailing_PE",
    "Forward_PE",
    "Revenue_Growth_Pct",
    "Operating_Margin_Pct",
    "Short_Interest_Pct",
]

NUMERIC_COLUMNS = [
    "Trailing_PE",
    "Forward_PE",
    "Revenue_Growth_Pct",
    "Operating_Margin_Pct",
    "Short_Interest_Pct",
]


# -------------------------------------------------------------------------------------------------
# Validation
# -------------------------------------------------------------------------------------------------
def validate_company_structure_df(df: pd.DataFrame) -> dict:
    """
    Validate Company Structure Review dataframe.

    Returns
    -------
    dict
        {
            "valid": bool,
            "errors": list,
            "warnings": list,
            "cleaned_df": DataFrame
        }
    """

    errors = []
    warnings = []

    # ---------------------------------------------------------------------------------------------
    # Empty DataFrame
    # ---------------------------------------------------------------------------------------------
    if df is None or df.empty:
        errors.append("Dataset is empty.")
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "cleaned_df": pd.DataFrame(),
        }

    df_clean = df.copy()

    # ---------------------------------------------------------------------------------------------
    # Required Columns
    # ---------------------------------------------------------------------------------------------
    missing_cols = [
        col for col in REQUIRED_COLUMNS
        if col not in df_clean.columns
    ]

    if missing_cols:
        errors.append(
            f"Missing required columns: {', '.join(missing_cols)}"
        )

    if errors:
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "cleaned_df": pd.DataFrame(),
        }

    # ---------------------------------------------------------------------------------------------
    # Company Cleanup
    # ---------------------------------------------------------------------------------------------
    df_clean["Company"] = (
        df_clean["Company"]
        .astype(str)
        .str.strip()
    )

    # ---------------------------------------------------------------------------------------------
    # Ticker Cleanup
    # ---------------------------------------------------------------------------------------------
    df_clean["Ticker"] = (
        df_clean["Ticker"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ---------------------------------------------------------------------------------------------
    # Numeric Conversion
    # ---------------------------------------------------------------------------------------------
    for col in NUMERIC_COLUMNS:
        df_clean[col] = pd.to_numeric(
            df_clean[col],
            errors="coerce",
        )

    # ---------------------------------------------------------------------------------------------
    # Duplicate Company Check
    # ---------------------------------------------------------------------------------------------
    duplicate_companies = df_clean[
        df_clean.duplicated(subset=["Company"], keep=False)
    ]

    if not duplicate_companies.empty:
        warnings.append(
            f"{len(duplicate_companies)} duplicate company records detected."
        )

    # ---------------------------------------------------------------------------------------------
    # Duplicate Ticker Check
    # ---------------------------------------------------------------------------------------------
    duplicate_tickers = df_clean[
        df_clean.duplicated(subset=["Ticker"], keep=False)
    ]

    if not duplicate_tickers.empty:
        warnings.append(
            f"{len(duplicate_tickers)} duplicate ticker records detected."
        )

    # ---------------------------------------------------------------------------------------------
    # Missing Data Warnings
    # ---------------------------------------------------------------------------------------------
    for col in NUMERIC_COLUMNS:
        missing_count = df_clean[col].isna().sum()

        if missing_count > 0:
            warnings.append(
                f"{col}: {missing_count} missing value(s)."
            )

    # ---------------------------------------------------------------------------------------------
    # Remove Fully Empty Rows
    # ---------------------------------------------------------------------------------------------
    df_clean = df_clean.dropna(
        how="all",
        subset=[
            "Trailing_PE",
            "Forward_PE",
            "Revenue_Growth_Pct",
            "Operating_Margin_Pct",
            "Short_Interest_Pct",
        ],
    )

    # ---------------------------------------------------------------------------------------------
    # Sort
    # ---------------------------------------------------------------------------------------------
    df_clean = df_clean.sort_values(
        by="Company"
    ).reset_index(drop=True)

    return {
        "valid": True,
        "errors": errors,
        "warnings": warnings,
        "cleaned_df": df_clean,
    }
