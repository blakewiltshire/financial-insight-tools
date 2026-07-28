# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission Engine
# -------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd

from relative_transmission_labels import (
    get_regime_label,
    get_rolling_state,
)


# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def zscore(series):
    """
    Standardise a series across its available history.
    """
    std_dev = series.std()

    if pd.isna(std_dev) or std_dev == 0:
        return pd.Series(np.nan, index=series.index, dtype=float)

    return (series - series.mean()) / std_dev


def _safe_last(series):
    """
    Return the last non-null value from a series, otherwise NaN.
    """
    clean_series = series.replace([np.inf, -np.inf], np.nan).dropna()

    if clean_series.empty:
        return np.nan

    return clean_series.iloc[-1]


def _rolling_change(rolling_corr, lookback=6):
    """
    Return the recent rolling-correlation change over the selected lookback.
    """
    clean_corr = rolling_corr.replace([np.inf, -np.inf], np.nan).dropna()

    if len(clean_corr) <= lookback:
        return np.nan

    return float(clean_corr.iloc[-1] - clean_corr.iloc[-(lookback + 1)])


# -------------------------------------------------------------------------------------------------
# Public Engine
# -------------------------------------------------------------------------------------------------
def compute_transmission(pair_df, transformation="difference", window=12):
    """
    Core comparative transmission engine.

    The rolling-correlation result separates:
    - current relationship level;
    - historical percentile;
    - recent strengthening / weakening / stability.
    """
    if pair_df is None or pair_df.empty or pair_df.shape[1] < 2:
        raise ValueError("pair_df must contain at least two aligned series")

    if window < 2:
        raise ValueError("window must be at least 2")

    a = pd.to_numeric(pair_df.iloc[:, 0], errors="coerce")
    b = pd.to_numeric(pair_df.iloc[:, 1], errors="coerce")

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

    current_value = _safe_last(derived)
    current_z = _safe_last(spread_z)
    current_corr = _safe_last(rolling_corr)

    valid_derived = derived.replace([np.inf, -np.inf], np.nan).dropna()

    if valid_derived.empty:
        percentile = np.nan
    else:
        percentile = float(valid_derived.rank(pct=True).iloc[-1] * 100)

    correlation_lookback = 6
    current_corr_change = _rolling_change(
        rolling_corr=rolling_corr,
        lookback=correlation_lookback,
    )

    result = {
        "overlay_df": pair_df,
        "derived_df": derived.to_frame(name="derived_metric"),
        "rolling_df": rolling_corr.to_frame(name="rolling_correlation"),
        "current_value": current_value,
        "current_z": current_z,
        "current_corr": current_corr,
        "current_corr_change": current_corr_change,
        "correlation_lookback": correlation_lookback,
        "percentile": percentile,
        "regime_label": get_regime_label(
            transformation=transformation,
            current_value=current_value,
            current_z=current_z,
            current_corr=current_corr,
        ),
        "rolling_state": get_rolling_state(
            rolling_corr=rolling_corr,
            lookback=correlation_lookback,
        ),
        "summary": {
            "max": valid_derived.max() if not valid_derived.empty else np.nan,
            "min": valid_derived.min() if not valid_derived.empty else np.nan,
            "mean": valid_derived.mean() if not valid_derived.empty else np.nan,
            "std_dev": valid_derived.std() if not valid_derived.empty else np.nan,
            "current": current_value,
        },
    }

    return result
