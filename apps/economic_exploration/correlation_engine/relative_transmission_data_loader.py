# -------------------------------------------------------------------------------------------------
# Relative Macro Transmission Data Loader
# -------------------------------------------------------------------------------------------------

import pandas as pd

from economic_series_map import ECONOMIC_SERIES_MAP
from correlation_data_loader import load_indicator_data


def build_relative_series_pool():
    """
    Build eligible series pool from registry.

    Priority:
    1. allow_relative_macro_transmission
    2. fallback to allow_correlation

    This keeps the module aligned with the existing registry setup.
    """
    pool = []

    for country, themes in ECONOMIC_SERIES_MAP.items():
        for theme_code, templates in themes.items():
            for _, indicators in templates.items():
                for registry_key, metadata in indicators.items():

                    allow_relative = metadata.get("allow_relative_macro_transmission", None)
                    allow_correlation = metadata.get("allow_correlation", False)

                    if allow_relative is None:
                        is_allowed = allow_correlation
                    else:
                        is_allowed = allow_relative

                    if not is_allowed:
                        continue

                    label = f"{country} — {metadata.get('ui_display_name', metadata.get('name', registry_key))}"

                    series_type = metadata.get("relative_series_type", "macro")

                    pool.append({
                        "label": label,
                        "country": country,
                        "theme_code": theme_code,
                        "registry_key": registry_key,
                        "indicator_name": metadata.get("name"),
                        "series_type": series_type,
                        "rmt_surface_type": metadata.get("rmt_surface_type"),
                    })

    return sorted(pool, key=lambda x: x["label"])


def filter_series_pool(pool, comparison_mode):
    """
    Keep filtering simple and structural.

    If relative_series_type is not yet defined in registry,
    default series_type='macro' ensures items still appear.
    """
    if comparison_mode == "Macro vs Macro":
        return [x for x in pool if x["series_type"] == "macro"]

    if comparison_mode == "Macro vs Market":
        return [x for x in pool if x["series_type"] in ["macro", "market"]]

    if comparison_mode == "Market vs Market":
        return [x for x in pool if x["series_type"] == "market"]

    return pool


def load_relative_pair(series_a_obj, series_b_obj, project_path):
    """
    Load two aligned monthly series.
    """
    series_a, _, status_a = load_indicator_data(series_a_obj, project_path)
    series_b, _, status_b = load_indicator_data(series_b_obj, project_path)

    messages = []

    if status_a:
        messages.append(status_a)

    if status_b:
        messages.append(status_b)

    if status_a or status_b:
        return pd.DataFrame(), messages

    pair_df = pd.concat([series_a, series_b], axis=1, join="inner").dropna()

    return pair_df, messages
