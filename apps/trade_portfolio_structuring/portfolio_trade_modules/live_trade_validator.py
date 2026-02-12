# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""Validator for live portfolio snapshot uploads.
Validates structure, field integrity, and data logic for real-time position monitoring."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Import Template Column Definitions
# -------------------------------------------------------------------------------------------------
from portfolio_trade_modules.live_portfolio_template import REQUIRED_LIVE_PORTFOLIO_COLUMNS

# -------------------------------------------------------------------------------------------------
# Helper Validation Functions
# -------------------------------------------------------------------------------------------------
def validate_required_columns(df, required_columns):
    """
    Identify any required columns missing from the input DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame to check.
        required_columns (list[str]): List of expected column names.

    Returns:
        list[str]: List of missing column names.
    """
    missing = [col for col in required_columns if col not in df.columns]
    return missing


def validate_date_format(df, col):
    """
    Validate that a date column is formatted using ISO standard (YYYY-MM-DD).

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        col (str): Name of the date column to validate.

    Returns:
        str | None: Error message if invalid, None if format is valid.
    """
    try:
        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d", errors="raise")
        return None
    except Exception:
        return f"Invalid date format in '{col}'. Use ISO format: YYYY-MM-DD (e.g., 2024-01-10)."


def validate_positive_values(df, cols):
    """
    Ensure that specified columns contain only positive values.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        cols (list[str]): Columns to check.

    Returns:
        list[str]: List of error messages for columns with non-positive values.
    """
    errors = []
    for col in cols:
        if col in df.columns:
            non_positive = df[df[col] <= 0]
            if not non_positive.empty:
                errors.append(f"{len(non_positive)} rows have non-positive values in '{col}'.")
    return errors


def validate_direction_column(df):
    """
    Standardise and validate the 'Direction' column.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'Direction' column.

    Returns:
        str | None: Error message for invalid entries, or None if valid.
    """
    df["Direction"] = df["Direction"].astype(str).str.strip().str.capitalize()
    valid_directions = {"Long", "Short"}
    invalid = df[~df["Direction"].isin(valid_directions)]
    if not invalid.empty:
        return f"{len(invalid)} rows have invalid 'Direction' values. Must be 'Long' \
        or 'Short' (case-insensitive)."
    return None


def validate_leverage_column(df):
    """
    Validate and parse the 'Leverage Used' column, returning warnings and errors.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        tuple[list[str], list[str]]: (errors, warnings)
    """
    warnings = []
    errors = []

    if "Leverage Used" in df.columns:
        try:
            df["Leverage Used"] = pd.to_numeric(df["Leverage Used"], errors="coerce")
            leverage_nan = df["Leverage Used"].isna().sum()
            leverage_zero = (df["Leverage Used"] == 0).sum()
            leverage_neg = (df["Leverage Used"] < 0).sum()

            if leverage_nan > 0:
                warnings.append(f"⚠️ {leverage_nan} row(s) have missing or invalid \
                'Leverage Used'. Global default will be applied.")
            if leverage_zero > 0:
                warnings.append(f"⚠️ {leverage_zero} row(s) have zero leverage. \
                Global default will be applied.")
            if leverage_neg > 0:
                errors.append(f"{leverage_neg} row(s) have negative leverage, \
                which is invalid.")
        except Exception:
            warnings.append("⚠️ Unable to parse 'Leverage Used' column. Global \
            default will apply.")

    return errors, warnings


def detect_duplicate_symbols(df):
    """
    Identify duplicate 'Symbol' and 'Entry Date' combinations.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        str | None: Warning message if duplicates exist, else None.
    """
    duplicates = df.duplicated(subset=["Symbol", "Entry Date"], keep=False)
    if duplicates.any():
        return f"🔁 {duplicates.sum()} rows have duplicate 'Symbol + Entry Date' \
        combinations. May reflect repeated lots."
    return None


def detect_no_price_movement(df):
    """
    Detect positions where 'Entry Price' equals 'Current Price'.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        str | None: Warning message if no movement detected, else None.
    """
    if "Current Price" in df.columns and "Entry Price" in df.columns:
        no_movement = df[df["Current Price"] == df["Entry Price"]]
        if not no_movement.empty:
            return f"⚠️ {len(no_movement)} rows show no price movement (Current = Entry). \
            May indicate new or inactive trades."
    return None


# -------------------------------------------------------------------------------------------------
# Main Validation Function
# -------------------------------------------------------------------------------------------------
def validate_live_trade_log(df):
    """
    Validate the structure and content of a user-uploaded live portfolio snapshot.

    Parameters:
        df (pd.DataFrame): Uploaded DataFrame.

    Returns:
        dict: {
            "valid": bool,
            "errors": list of blocking error messages,
            "warnings": list of non-blocking warnings,
            "cleaned_df": pd.DataFrame (normalised and ready for use)
        }
    """
    errors = []
    warnings = []
    df = df.copy()

    # Required Columns
    missing = validate_required_columns(df, REQUIRED_LIVE_PORTFOLIO_COLUMNS)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
        return {"valid": False, "errors": errors, "warnings": warnings, "cleaned_df": None}

    # Date Format
    date_error = validate_date_format(df, "Entry Date")
    if date_error:
        errors.append(date_error)

    # Positive Values
    errors += validate_positive_values(df, ["Entry Price", "Current Price", "Position Size"])

    # Direction
    dir_error = validate_direction_column(df)
    if dir_error:
        errors.append(dir_error)

    # Leverage
    lev_errors, lev_warnings = validate_leverage_column(df)
    errors += lev_errors
    warnings += lev_warnings

    # Duplicates
    dup_warn = detect_duplicate_symbols(df)
    if dup_warn:
        warnings.append(dup_warn)

    # Flat Prices
    price_warn = detect_no_price_movement(df)
    if price_warn:
        warnings.append(price_warn)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "cleaned_df": df if len(errors) == 0 else None
    }
