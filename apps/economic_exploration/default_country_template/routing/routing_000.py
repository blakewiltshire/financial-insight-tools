# -------------------------------------------------------------------------------------------------
# 🔀 Routing Wrapper — Indicator Input Dispatcher
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📍 Local Use Case Routing — Thematic Module
------------------------------------------------

Maps the selected use case to the appropriate indicator functions for evaluation.
This file defines which indicators contribute to each high-level analytical theme.

✅ Structure:
- `options_*_signals_map` assigns indicators to each use case
- Must align with entries in `indicator_map`
- Used by the insight generation and scoring engines

🧠 AI Notes:
- Enables the AI and alignment engine to dynamically dispatch signals
- Helps determine the “macro story” behind observed trends

Usage:
- Imported into the core dispatcher logic for signal evaluation
- Override to emphasise different indicators in local analysis
"""

# -------------------------------------------------------------------------------------------------
# 🧱 Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# 🛠️ Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_routing"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 📦 Universal Routing Import
# -------------------------------------------------------------------------------------------------
from universal_routing_000 import get_indicator_input as get_indicator_input_universal

# -------------------------------------------------------------------------------------------------
# 📊 Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# 🚦 Local Routing Overrides (Optional)
# -------------------------------------------------------------------------------------------------
def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    """
    Retrieves the dataframe corresponding to the given indicator.

    Logic:
    - Checks local override logic first (if defined)
    - Falls back to universal routing dispatcher

    Parameters:
        indicator_name (str): Name of the indicator from use case
        df_dict (dict): Dictionary of available preloaded dataframes

    Returns:
        pd.DataFrame | None: Matching dataframe for the indicator
    """
    return get_indicator_input_universal(indicator_name, df_dict)
