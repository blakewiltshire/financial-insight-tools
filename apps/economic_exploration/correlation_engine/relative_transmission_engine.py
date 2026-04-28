# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission Engine
# -------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd

from relative_transmission_labels import (
    get_regime_label,
    get_rolling_state
)


def zscore(series):
    return (series - series.mean()) / series.std()


def compute_transmission(pair_df, transformation="difference", window=12):
    """
    Core comparative transmission engine.
    """

    a = pair_df.iloc[:, 0]
    b = pair_df.iloc[:, 1]

    if transformation == "difference":
        derived = a - b

    elif transformation == "ratio":
        derived = a / b.replace(0, np.nan)

    elif transformation == "relative_pct":
        derived = ((a - b) / b.replace(0, np.nan)) * 100

    elif transformation == "zscore_spread":
        derived = zscore(a - b)

    elif transformation == "rolling_corr":
        derived = a.rolling(window).corr(b)

    else:
        raise ValueError("Invalid transformation")

    rolling_corr = a.rolling(window).corr(b)

    spread_z = zscore(a - b)

    current_value = derived.iloc[-1]
    current_z = spread_z.iloc[-1]
    current_corr = rolling_corr.iloc[-1]

    percentile = derived.rank(pct=True).iloc[-1] * 100

    result = {
        "overlay_df": pair_df,
        "derived_df": derived.to_frame(name="derived_metric"),
        "rolling_df": rolling_corr.to_frame(name="rolling_correlation"),
        "current_value": current_value,
        "current_z": current_z,
        "current_corr": current_corr,
        "percentile": percentile,
        "regime_label": get_regime_label(
            transformation=transformation,
            current_value=current_value,
            current_z=current_z,
            current_corr=current_corr,
        ),
        "rolling_state": get_rolling_state(current_corr),
        "summary": {
            "max": derived.max(),
            "min": derived.min(),
            "mean": derived.mean(),
            "std_dev": derived.std(),
            "current": current_value,
        }
    }

    return result
