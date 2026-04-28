# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Statistical Profile
# -------------------------------------------------------------------------------------------------
def calculate_statistical_profile(series: pd.Series) -> pd.DataFrame:
    """
    Returns descriptive statistics for the selected series.
    """
    series = pd.to_numeric(series, errors="coerce").dropna()

    if series.empty:
        return pd.DataFrame(columns=["Metric", "Value"])

    stats = {
        "Mean": series.mean(),
        "Standard Error": series.sem(),
        "Median": series.median(),
        "Mode": series.mode().iloc[0] if not series.mode().empty else None,
        "Standard Deviation": series.std(),
        "Sample Variance": series.var(),
        "Kurtosis": series.kurtosis(),
        "Skewness": series.skew(),
        "Range": series.max() - series.min(),
        "Minimum": series.min(),
        "Maximum": series.max(),
        "Sum": series.sum(),
        "Count": int(series.count()),
    }

    stats_df = pd.DataFrame({
        "Metric": list(stats.keys()),
        "Value": list(stats.values())
    })

    def format_value(metric, value):
        if pd.isna(value):
            return ""
        if metric == "Count":
            return f"{int(value)}"
        return f"{value:,.4f}"

    stats_df["Value"] = [
        format_value(metric, value)
        for metric, value in zip(stats_df["Metric"], stats_df["Value"])
    ]

    return stats_df
