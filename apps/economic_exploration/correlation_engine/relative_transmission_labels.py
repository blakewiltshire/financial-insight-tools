# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission Labels
# -------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Rolling Correlation — Current Relationship Level
# -------------------------------------------------------------------------------------------------
def _get_correlation_level_label(current_corr):
    """
    Classify the current rolling-correlation level.

    Important:
    - This describes the present relationship level only.
    - It does not infer strengthening, weakening, decoupling, or re-coupling.
    """
    if current_corr is None or np.isnan(current_corr):
        return "N/A"

    if current_corr >= 0.70:
        return "Strong Positive Transmission"

    if current_corr >= 0.40:
        return "Moderate Positive Transmission"

    if current_corr >= 0.10:
        return "Weak Positive Transmission"

    if current_corr > -0.10:
        return "Low Transmission"

    if current_corr > -0.40:
        return "Weak Inverse Transmission"

    if current_corr > -0.70:
        return "Moderate Inverse Transmission"

    return "Strong Inverse Transmission"


# -------------------------------------------------------------------------------------------------
# Public Regime Classification
# -------------------------------------------------------------------------------------------------
def get_regime_label(transformation, current_value=None, current_z=None, current_corr=None):
    """
    Transformation-aware regime classification.

    Rolling Correlation:
    - classifies the current relationship level using the current correlation.

    Difference / Ratio / Relative % / Relative Z-Score:
    - retain the existing spread-style classification using the absolute
      standardised spread value.
    """
    if transformation == "rolling_corr":
        return _get_correlation_level_label(current_corr)

    if current_z is None or np.isnan(current_z):
        return "N/A"

    z_abs = abs(current_z)

    if z_abs < 0.5:
        return "Aligned"

    if z_abs < 1.0:
        return "Mild Divergence"

    if z_abs < 2.0:
        return "Material Divergence"

    return "Regime Shift"


# -------------------------------------------------------------------------------------------------
# Rolling Correlation — Recent Direction
# -------------------------------------------------------------------------------------------------
def get_rolling_state(rolling_corr, lookback=6, change_threshold=0.10):
    """
    Classify the recent direction of the rolling-correlation relationship.

    Parameters
    ----------
    rolling_corr : pandas.Series
        Full rolling-correlation series.
    lookback : int
        Number of observations used to compare the current relationship with
        its recent past.
    change_threshold : float
        Minimum absolute correlation change required to classify the recent
        path as strengthening or weakening.

    Returns
    -------
    str
        Strengthening Transmission, Weakening Transmission,
        Stable Transmission, or N/A.

    Notes
    -----
    This deliberately avoids "re-coupling" and "decoupling" because those
    labels require a stronger transition model than a single lookback change.
    """
    if rolling_corr is None:
        return "N/A"

    if not isinstance(rolling_corr, pd.Series):
        rolling_corr = pd.Series(rolling_corr)

    clean_corr = rolling_corr.replace([np.inf, -np.inf], np.nan).dropna()

    if len(clean_corr) <= lookback:
        return "N/A"

    current_corr = float(clean_corr.iloc[-1])
    prior_corr = float(clean_corr.iloc[-(lookback + 1)])
    change = current_corr - prior_corr

    if change >= change_threshold:
        return "Strengthening Transmission"

    if change <= -change_threshold:
        return "Weakening Transmission"

    return "Stable Transmission"
