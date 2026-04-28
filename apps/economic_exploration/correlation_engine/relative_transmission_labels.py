# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission Labels
# -------------------------------------------------------------------------------------------------

import numpy as np


def get_regime_label(transformation, current_value=None, current_z=None, current_corr=None):
    """
    Transformation-aware regime classification.

    Why:
    - Difference / Ratio / Relative % / Relative Z-Score are spread-style comparisons
    - Rolling Correlation is relationship-state analysis and must be classified separately
    """

    if transformation == "rolling_corr":
        if current_corr is None or np.isnan(current_corr):
            return "N/A"

        if current_corr >= 0.70:
            return "Aligned"
        elif current_corr >= 0.40:
            return "Mild Divergence"
        elif current_corr >= 0.10:
            return "Material Divergence"
        else:
            return "Regime Shift"

    # Default spread-style classification
    if current_z is None or np.isnan(current_z):
        return "N/A"

    z_abs = abs(current_z)

    if z_abs < 0.5:
        return "Aligned"
    elif z_abs < 1.0:
        return "Mild Divergence"
    elif z_abs < 2.0:
        return "Material Divergence"
    else:
        return "Regime Shift"


def get_rolling_state(corr_value):
    """
    Relationship-state classification for the rolling correlation panel.
    """

    if np.isnan(corr_value):
        return "N/A"

    if corr_value >= 0.70:
        return "Re-coupling"

    if corr_value <= 0.30:
        return "Decoupling"

    return "Mixed Transmission"
