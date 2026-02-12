# -------------------------------------------------------------------------------------------------
# 🔗 Correlation Engine — Z-Score Standardisation & Matrix Builder (Universal Canonical)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
This module applies full correlation calculation pipeline:
- Aligns multiple input series
- Applies z-score standardisation per column
- Builds correlation matrix
- Returns clean DataFrame for visualisation layer
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

# -------------------------------------------------------------------------------------------------
# Core Correlation Engine Function
# -------------------------------------------------------------------------------------------------

def build_correlation_matrix(series_list):
    """
    Builds correlation matrix from list of aligned pd.Series objects.

    Args:
        series_list (list): List of pd.Series (all aligned on same datetime index)

    Returns:
        pd.DataFrame: Correlation matrix (standardised)
    """

    if not series_list:
        return None

    # Combine series into dataframe
    df_raw = pd.concat(series_list, axis=1, join="inner")

    # Apply z-score standardisation
    df_standardised = (df_raw - df_raw.mean()) / df_raw.std()

    # Compute correlation matrix
    corr_matrix = df_standardised.corr()

    return corr_matrix

# -------------------------------------------------------------------------------------------------
# End of Correlation Engine
# -------------------------------------------------------------------------------------------------
