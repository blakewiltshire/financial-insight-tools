# -------------------------------------------------------------------------------------------------
# Relative Transmission Summary
# -------------------------------------------------------------------------------------------------

import pandas as pd


def build_summary_table(result):
    summary = result["summary"]

    return pd.DataFrame({
        "Statistic": [
            "Max",
            "Min",
            "Mean",
            "Std Dev",
            "Current",
            "Regime",
            "Rolling State",
            "Percentile"
        ],
        "Value": [
            summary["max"],
            summary["min"],
            summary["mean"],
            summary["std_dev"],
            summary["current"],
            result["regime_label"],
            result["rolling_state"],
            round(result["percentile"], 2)
        ]
    })
