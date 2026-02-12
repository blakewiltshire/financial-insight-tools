# -------------------------------------------------------------------------------------------------
# 📈 Economic Growth Stability — Indicator Map (Local Extension Scaffold)
# -------------------------------------------------------------------------------------------------
# This module defines the signal mapping logic for macroeconomic indicators within
# the Economic Growth & Stability theme (Theme 100), for the current country.
#
# It extends the universal indicator mapping with optional local definitions.
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Local Indicator Map — Thematic Extension Logic
--------------------------------------------------

This module defines local indicator-to-signal function mappings for country-specific
or theme-specific extensions.
It works in parallel with the universal system, providing optional overrides where
local conditions apply.

✅ System Role:
- Allows country-specific or dataset-specific indicator evaluation
- Merges seamlessly into the core Economic Exploration evaluation framework
- Supports expanded insight generation, scoring, and AI-compatible workflows
for local data nuances

🧠 AI Persona Alignment Notes:
- Signal functions must return strict string-based classifications
  (e.g., "Expansion Detected", "Decline", "Neutral", "Insufficient Data")
- Output strings are consumed directly by external AI workflows, structured
insights panels, and DSS scoring engines
- Numeric payloads, tuples, or dynamic secondary values are **not
permitted** — all returns are pure text strings

---------------------------------------------------------------
⚙️ System Structure — Integration & Compatibility Requirements
---------------------------------------------------------------

1️⃣ **Function Signature Consistency**
- All signal functions must accept:
    - `df` (input dataframe)
    - `period=None` (optional parameter, always included for compatibility)
- Signature: `def signal_function(df, period=None): ...`

2️⃣ **String-Based Return Values**
- Every function must return a plain text string suitable for:
    - Signal summaries
    - Insight generation
    - DSS scoring alignment
- Example returns: `"Sector Momentum: Manufacturing"`, `"Both Expanding"`, `"Insufficient Data"`

3️⃣ **Sector-Level Dynamic Labels (Optional)**
- For sectoral breakdowns, string returns may embed dynamic entity names directly
within the signal string (e.g., `"Sector Momentum: Manufacturing"`).
- These dynamic entity names are parsed downstream during insight generation —
not handled inside signal functions.

4️⃣ **No Numeric Payloads**
- Signal outputs must not return any numeric values, tuples, or secondary calculation payloads.
- All quantitative context is handled separately via metrics and charting layers.

5️⃣ **Dispatcher Independence**
- Signal routing and indicator map merging is handled via:
    - `get_indicator_maps()`
    - `compute_econ_alignment()`
- No embedded routing logic or external data references within signal functions.

🧭 Governance Note:
- Local indicator maps extend the system only where country-specific or theme-specific
datasets exist.
- Users modify these local modules for custom configurations; universal modules remain
system-stable.
"""

# -------------------------------------------------------------------------------------------------
# 🧱 Standard Library and Pathing
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# 📦 Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd  # Required for compatibility with custom indicator functions

# -------------------------------------------------------------------------------------------------
# 🧭 Path Setup: Add Universal Indicator Map to System Path
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_indicator_map"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 🔁 Imports: Universal Indicators (Do Not Modify)
# -------------------------------------------------------------------------------------------------
from universal_indicator_map_100 import (
    options_gdp_growth_rate_map,
    options_nominal_gdp_map,
    options_gdp_components_map
)

# -------------------------------------------------------------------------------------------------
# 🏛️ Local Indicator Mappings (Optional — Extend as Needed)
# -------------------------------------------------------------------------------------------------
# Structure Example:
# custom_local_map = {
#     "National Activity Index": national_activity_signal_function,
#     ...
# }

# For now, local indicators are omitted (placeholder for extension).

# -------------------------------------------------------------------------------------------------
# 🧩 Combined Indicator Map (Universal + Local)
# -------------------------------------------------------------------------------------------------
ALL_INDICATOR_MAPS = {
    # Universal GDP indicators (required across all countries)
    "Real GDP": options_gdp_growth_rate_map,
    "Nominal GDP": options_nominal_gdp_map,
    "GDP Components Breakdown": options_gdp_components_map,

    # Local thematic indicators (if any) go here
    # "National Activity Index": custom_local_map,
}

def get_indicator_maps():
    """
    Returns the full indicator mapping dictionary for the Economic Growth Stability theme.

    Returns:
        dict: Mapping of use case names to corresponding indicator dictionaries.
    """
    return ALL_INDICATOR_MAPS
