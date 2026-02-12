# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Template structure for a Trade History & Strategy log (closed trades).
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# ---- Required columns for trade log validation ---
REQUIRED_TRADE_LOG_COLUMNS = [
    "Asset",
    "Trade Date (Entry)",
    "Trade Date (Exit)",
    "Entry Price",
    "Exit Price",
    "Position Size",
    "Direction",
    "Fees",
    "P&L (Realised)",
    "Currency"
]

# ---- Optional (but encouraged) columns for better attribution ---
OPTIONAL_TRADE_LOG_COLUMNS = [
    "Trade ID",
    "Country",
    "Strategy Tag",
    "Sector",
    "Capital Deployed",
    "Leverage Used",
    "Benchmark",
    "Notes"
]

# ---- Get Trade Log Template ---
"""
Trade Log Template Generator

This module provides a clean trade log template with required and optional columns,
enabling users to initialise consistent upload-ready CSV files for portfolio monitoring.

Used by:
- Trade History & Strategy module
- Live Portfolio Monitor
- Validation pipeline

All templates follow ISO date formatting and support structured downstream diagnostics.
"""

def get_trade_log_template(include_optional: bool = True) -> pd.DataFrame:
    """
    Generate an empty trade log DataFrame with standardised headers.

    Parameters:
        include_optional (bool): If True, includes recommended optional fields
                                 such as Strategy Tag and Notes.

    Returns:
        pd.DataFrame: Template with only headers, no data rows.
    """
    if include_optional:
        columns = REQUIRED_TRADE_LOG_COLUMNS + OPTIONAL_TRADE_LOG_COLUMNS
    else:
        columns = REQUIRED_TRADE_LOG_COLUMNS

    return pd.DataFrame(columns=columns)

# ---- Download Trade Log Template ---
def download_trade_log_template_csv(filepath="trade_log_template.csv"):
    """
    Save an empty trade log template to a CSV file.

    Parameters:
        filepath (str): File path to save the CSV template.

    Returns:
        None
    """
    df = get_trade_log_template()
    df.to_csv(filepath, index=False)
