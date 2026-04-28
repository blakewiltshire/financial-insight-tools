# -------------------------------------------------------------------------------------------------
# Timeframe Slicer (Platinum Canonical — Period-Based Labeling)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Timeframe Slicer — Economic Exploration Suite (Period-Based Processing)
---------------------------------------------------------------

System Role:
- Converts user timeframe selections into precise row-based data slices.
- Fully decoupled from calendar frequencies (monthly, quarterly, weekly agnostic).

Key Design Principle:
- All downstream signal evaluation modules receive data already pre-sliced.
- Slicing governance remains fully centralized within this module.

Allowed Input Keys:
- 'Latest', '3P', '6P', '12P', '24P', '60P', 'Full'

Usage Alignment:
- Paired with `timeframe_selector.py` UI component
- Called in all `df_primary_slice` and related slicing operations across thematic modules.

---------------------------------------------------------------
Canonical Platinum Rule — System Locked:
- Never embed slicing logic within downstream insight or signal functions.
- Only this module governs slice window definitions.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Timeframe Slicer Core Logic
# -------------------------------------------------------------------------------------------------
def slice_data_by_timeframe(df: pd.DataFrame, selected: str) -> pd.DataFrame:
    """
    Return a period-sliced subset of the input DataFrame based on selected timeframe key.

    Args:
        df (pd.DataFrame): Input cleaned dataset.
        selected (str): Timeframe key ("Latest", "3P", "6P", "12P", "24P", "60P", or "Full").

    Returns:
        pd.DataFrame: Filtered dataframe for downstream processing.
    """
    period_map = {
        "Latest": 1,
        "3P": 3,
        "6P": 6,
        "12P": 12,
        "24P": 24,
        "60P": 60,
        "Full": None
    }

    periods = period_map.get(selected, None)
    if periods is None:
        return df  # Full History
    return df.tail(periods)
