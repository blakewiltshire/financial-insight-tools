# -------------------------------------------------------------------------------------------------
# 🔧 Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📄 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Local Indicator Map — Thematic Configuration
------------------------------------------------

Defines indicator-to-signal function mappings for a specific thematic module.
This file extends the universal setup by assigning concrete indicator labels to use cases.

✅ Structure:
- Each use case maps to one or more labelled indicators
- Labels must exactly match the CSV column names in the dataset
- Must align with logic in `options_*_signals_map`

🧠 AI Notes:
- Used in dynamic evaluation via `compute_econ_alignment(...)`
- Indicator functions must support `period=None` in their signature

Usage:
- Imported by the local theme module at runtime
- Override only if adding or renaming indicators from the default template
"""

# -------------------------------------------------------------------------------------------------
# 📦 Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_indicator_map"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 🔁 Universal Template Signal Import
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_000 import get_indicator_signal_map

# -------------------------------------------------------------------------------------------------
# 🧠 Signal Mapping (Signal A, B, C)
# -------------------------------------------------------------------------------------------------
template_signals = get_indicator_signal_map()

ALL_INDICATOR_MAPS = {
    "Signal A": {
        "Signal A": template_signals["Signal A"]
    },
    "Signal B": {
        "Signal B": template_signals["Signal B"]
    },
    "Signal C": {
        "Signal C": template_signals["Signal C"]
    }
}

# -------------------------------------------------------------------------------------------------
# 🔁 Dispatcher
# -------------------------------------------------------------------------------------------------
def get_indicator_maps():
    """
    Returns the complete indicator mapping aligned to signal-level use cases.
    """
    return ALL_INDICATOR_MAPS
