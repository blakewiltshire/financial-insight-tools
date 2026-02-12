# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Validator for Trade History & Strategy uploads.
Validates structure, field integrity, and data logic.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# -------------------------------------------------------------------------------------------------
from portfolio_trade_modules.trade_log_template import REQUIRED_TRADE_LOG_COLUMNS

# -------------------------------------------------------------------------------------------------
# Validate uploaded trade log file
# -------------------------------------------------------------------------------------------------
def validate_trade_log(df):
    """
    Validate the structure and integrity of a user-supplied trade log.

    Parameters:
        df (pd.DataFrame): Trade log as DataFrame.

    Returns:
        errors (list[str]): List of error messages. Empty if valid.
    """
    errors = []

    # --- Structural check: Required column presence ---
    missing_columns = [col for col in REQUIRED_TRADE_LOG_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return errors  # Halt early — further checks depend on structural integrity

    # --- Date format checks (ISO format preferred) ---
    date_cols = ["Trade Date (Entry)", "Trade Date (Exit)"]
    for col in date_cols:
        if col in df.columns:
            non_null_dates = df[col].dropna()
            try:
                pd.to_datetime(non_null_dates, format="%Y-%m-%d", errors="raise")
            except Exception:
                errors.append(
                    f"Invalid date format in '{col}'. Use ISO format: YYYY-MM-DD \
                    e.g., 2024-01-10)."
                )

    # --- Logical check: Exit must not be before Entry ---
    if all(col in df.columns for col in date_cols):
        try:
            valid_rows = df.dropna(subset=date_cols).copy()
            entry_dates = pd.to_datetime(valid_rows["Trade Date (Entry)"], format="%Y-%m-%d")
            exit_dates = pd.to_datetime(valid_rows["Trade Date (Exit)"], format="%Y-%m-%d")
            if (exit_dates < entry_dates).any():
                count = (exit_dates < entry_dates).sum()
                errors.append(f"{count} trades have exit dates before entry dates.")
        except Exception:
            pass  # Already handled by formatting exception above

    # --- Logical check: Position Size must be positive ---
    if "Position Size" in df.columns:
        negatives = df[df["Position Size"] <= 0]
        if not negatives.empty:
            errors.append(f"{len(negatives)} trades have non-positive position sizes.")

    # --- Logical check: Realised P&L consistency (only for closed trades) ---
    required_cols = {"P&L (Realised)", "Entry Price", "Exit Price", "Position Size", "Direction"}
    if required_cols.issubset(df.columns):
        try:
            closed_trades = df.dropna(subset=["Exit Price", "Entry Price", "Position Size",
                                              "P&L (Realised)", "Direction"]).copy()
            calc_pnl = closed_trades.apply(
                lambda row: (row["Exit Price"] - row["Entry Price"]) * row["Position Size"]
                if str(row["Direction"]).lower() == "long"
                else (row["Entry Price"] - row["Exit Price"]) * row["Position Size"],
                axis=1
            )
            mismatch = (calc_pnl.round(2) - closed_trades["P&L (Realised)"].round(2)).abs() > 1e-2
            if mismatch.sum() > 0:
                errors.append(f"{mismatch.sum()} closed trades have inconsistent realised P&L.")
        except Exception:
            errors.append("Unable to validate P&L consistency due to data type issues.")

    return errors
