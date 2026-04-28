# -------------------------------------------------------------------------------------------------
# Insight Generator (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Insight Map — Country-Specific Narrative Extensions
-------------------------------------------------------------------------------

This module defines localised insight narratives and bias classifications for country-level
customisation within the Economic Exploration suite. It allows country-specific or theme-specific
extensions to the system-wide universal insight map.

System Role:
- Provides extended or overridden insight text for local indicators
- Supports AI narratives, macro scoring, observation journals, and external DSS agents
- Used when local indicators exist or where country-level nuance is required

AI Persona Alignment Notes:
- Insight mappings return:
    • Textual insight strings (e.g., "Full-time employment is leading expansion")
    • Bias labels (e.g., "Growth Supportive", "Neutral", "Contraction Warning")
- Output strings directly feed:
    • Insight panels
    • DSS macro condition summaries
    • AI persona export narratives

System Structure & Compatibility:
**Strict Key Matching**
    - Keys must match exactly the signal output strings from `indicator_map_XXX.py`
    - Any sector-level tuple disaggregation handled upstream before calling insights

**Bias Labels Aligned to Scoring Framework**
    - Valid bias tags: `"Growth Supportive"`, `"Neutral"`, `"Contraction Warning"`, `"Caution"`

**String-Based Substitution Only**
    - Text templates may include `{sector}` or `{value}` placeholders if dynamic context is passed
    - No numeric payloads returned — insight output always resolves to pure
    text + bias classification

**Dispatcher Consistency**
    - Interface includes:
        - `indicator` (use case signal)
        - `signal_result` (strict string match)
        - `timeframe` (pass-through)
        - `extra_value` (optional sector string substitution where applicable)

**No Embedded Evaluation Logic**
    - This module performs no calculations.
    - All logic and signal evaluation occurs upstream in indicator map functions.

Governance Note:
- This local insight map overrides universal logic where defined.
- If no local match exists, the system falls back automatically to `universal_insights_XXX.py`.
- This ensures full global-local modular consistency across countries and themes.
"""

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys
import pandas as pd

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_routing"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

from universal_routing_100 import get_indicator_input as get_indicator_input_universal

# -------------------------------------------------------------------------------------------------
# Indicator Routing Entry Point
# -------------------------------------------------------------------------------------------------
def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
    """
    Returns the appropriate input DataFrame for a given indicator.

    Args:
        indicator_name (str): Name of the economic indicator (from indicator map).
        df_dict (dict): Dictionary of cleaned and sliced DataFrames (standardised keys).

    Returns:
        pd.DataFrame | None: Dataset used for signal generation.
    """
    return get_indicator_input_universal(indicator_name, df_dict)
