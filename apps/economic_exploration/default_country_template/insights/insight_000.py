# -------------------------------------------------------------------------------------------------
# Insight Generator (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Insight Summaries — Thematic Module
------------------------------------------------

Provides structured textual insights for each use case based on evaluated signals.
Intended to support user understanding, AI augmentation, and export-ready summaries.

Structure:
- One function per use case (e.g., `summarise_employment_trends(...)`)
- Each function should accept a dictionary of signal values

AI Notes:
- Designed for hybrid manual + AI insight generation
- Avoid advisory language; maintain analytical, factual tone

Usage:
- Called by insight panels and export routines
- Override if local narratives or signal emphasis differs from the default
"""

# -------------------------------------------------------------------------------------------------
# Imports and Path Setup
# -------------------------------------------------------------------------------------------------
import os
import sys

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_insights"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Universal Insight Import
# -------------------------------------------------------------------------------------------------
from universal_insights_000 import generate_universal_econ_insights

# -------------------------------------------------------------------------------------------------
# Local Insight Definitions (Optional)
# -------------------------------------------------------------------------------------------------
LOCAL_INSIGHTS = {
    # Placeholder for local indicator-specific insights
    # "Labour Market Pulse": {
    #     "Strengthening": "Recent labour data suggests tightening conditions.",
    #     "Weakening": "Indicators point to a cooling employment trend."
    # }
}

# -------------------------------------------------------------------------------------------------
# Combined Dispatcher
# -------------------------------------------------------------------------------------------------
def generate_econ_insights(indicator: str, value: str, timeframe: str) -> str:
    """
    Returns a structured insight statement based on indicator and macro signal.

    Priority:
    1. Local insight override (if defined)
    2. Universal insight fallback (ensures coverage for all templates)

    Parameters:
        indicator (str): Indicator name (as listed in use case map)
        value (str): Signal classification (e.g., 'Accelerating Growth')
        timeframe (str): Timeframe label for context-specific insights

    Returns:
        str: Contextualised macro insight statement
    """
    local_map = LOCAL_INSIGHTS.get(indicator, {})
    return local_map.get(value) or generate_universal_econ_insights(indicator, value, timeframe)
