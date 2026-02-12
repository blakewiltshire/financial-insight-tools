# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""Template structure for a live portfolio position log (open trades)."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Required + Optional Columns for Live Portfolio Upload
# -------------------------------------------------------------------------------------------------
REQUIRED_LIVE_PORTFOLIO_COLUMNS = [
    "Asset",
    "Symbol",
    "Entry Date",
    "Entry Price",
    "Current Price",
    "Position Size",
    "Direction",
    "Sector",
    "Country",
    "Strategy Tag",
    "Notes",
    "Leverage Used"  # Optional but encouraged for realistic leverage diagnostics
]

# -------------------------------------------------------------------------------------------------
# Get Live Portfolio Template (Empty)
# -------------------------------------------------------------------------------------------------
def get_live_portfolio_template():
    """
    Return an empty DataFrame structured for a live portfolio snapshot.

    Returns:
        pd.DataFrame: Template with column headers only.
    """
    return pd.DataFrame(columns=REQUIRED_LIVE_PORTFOLIO_COLUMNS)

# -------------------------------------------------------------------------------------------------
# Save Live Portfolio Template (Optional Download Method)
# -------------------------------------------------------------------------------------------------
def download_live_portfolio_template_csv(filepath="live_portfolio_template.csv"):
    """
    Save the live portfolio template as an empty CSV file.

    Parameters:
        filepath (str): Destination file path.

    Returns:
        None
    """
    df = get_live_portfolio_template()
    df.to_csv(filepath, index=False)
