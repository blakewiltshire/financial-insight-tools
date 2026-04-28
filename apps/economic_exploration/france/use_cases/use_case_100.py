# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Use Case Definitions — Thematic Module Extensions (Country-Specific)
-----------------------------------------------------------------------

This module defines country-specific use case mappings for a given thematic module
within the Economic Exploration suite. It extends the universal system scaffolding
to incorporate national datasets, special signals, or additional analytical focus.

System Role:
- Provides merged use case dictionaries combining:
    • Universal scaffolding (imported from `universal_use_cases_XXX.py`)
    • Local country-specific extensions (added in this module)

- Controls UI rendering for:
    • Use case dropdown selectors
    • Tab ordering and visualization layers
    • Scoring alignment consistency

AI Persona & DSS Notes:
- Use case keys here must exactly match those defined in:
    • Local `indicator_map_XXX.py`
    • Local `insight_XXX.py`
    • Local `scoring_weights_labels_XXX.py`

- Output structure drives:
    • AI export pathways
    • Macro alignment summaries
    • Observational journaling flows
    • Triangular navigation program architecture

Structure & Interface Governance:
**Universal Merge Foundation**
    - This file imports the corresponding universal use case map as the default base.
    - Local updates must preserve universal structure integrity.

**Strict Key Matching**
    - Added local use cases must ensure indicator keys match local indicator maps exactly.

**Metadata Fields**
    - `"Indicators"` → List of signal functions attached to the use case
    - `"Categories"` → System UI grouping for streamlit interface alignment
    - `"Description"` → Narrative framing for AI personas and DSS journaling

Governance Note:
- Local use case modules allow flexible adaptation by country.
- The universal scaffolding remains stable and externally governed.
- Local users configure national extensions here — but must preserve structural integrity.
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Universal Use Case Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_use_cases"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Import and Merge Use Cases
# -------------------------------------------------------------------------------------------------
from universal_use_cases_100 import get_use_cases as get_universal_use_cases

USE_CASES = dict(get_universal_use_cases())  # Shallow copy to allow safe local extension

# -------------------------------------------------------------------------------------------------
# ➕ Local Extensions (Optional)
# -------------------------------------------------------------------------------------------------
USE_CASES.update({
    # "Macro Composite Signals (Local)": {
    #     "Indicators": [
    #         "Composite Output Index",
    #         "National Activity Tracker",
    #         "Local Economic Uncertainty Index",
    #         "Regional PMI Series"
    #     ],
    #     "Categories": ["Macro Composite"],
    #     "Description": "Tracks short-term national macro momentum using composite indicators — "
    #                    "including growth, sentiment, and uncertainty dynamics."
    # }
})

# -------------------------------------------------------------------------------------------------
# Getter — Unified Use Case Dictionary
# -------------------------------------------------------------------------------------------------
def get_use_cases() -> dict:
    """
    Returns the merged set of universal and local use cases.

    Returns:
        dict: Use case definitions with labels, indicators, and descriptions.
    """
    return USE_CASES

# -------------------------------------------------------------------------------------------------
# Sidebar Use Case Selector
# -------------------------------------------------------------------------------------------------
def render_use_case_selector(get_use_cases_fn, default_use_case=None):
    """
    Renders the Streamlit sidebar selector for use cases and displays contextual detail.

    This selector supports both universal placeholder themes and fully configured local themes.

    Behaviour:
    - Loads the available use cases from the provided callable
    - Applies `default_use_case` if it exists in the available options
    - Falls back to the first available use case if no valid default is provided
    - Displays a contextual expandable summary of all available use cases

    This ensures:
    - Universal templates can safely default to placeholder signals (e.g. Signal A)
    - Local thematic modules can default to the primary real use case
      (e.g. Aggregate Equity Allocation)
    - The selector remains stable without relying on dictionary ordering

    Args:
        get_use_cases_fn (function):
            Callable that returns a dictionary of use cases.

        default_use_case (str, optional):
            Preferred default selection for the dropdown.
            Must match an existing use case key.
            If not found, index defaults to the first available option.

    Returns:
        tuple:
            selected_use_case (str):
                The currently selected use case key.

            use_cases (dict):
                Full dictionary of available use cases.
    """
    try:
        use_cases = get_use_cases_fn()
    except Exception as e:
        st.error(f"❌ Could not load use cases: {type(e).__name__} – {str(e)}")
        return None, {}

    options = list(use_cases.keys())

    default_index = 0
    if default_use_case and default_use_case in options:
        default_index = options.index(default_use_case)

    st.sidebar.title("Select a Use Case")

    selected = st.sidebar.selectbox(
        "Insight Use Case",
        options,
        index=default_index
    )

    with st.sidebar.expander("Use Cases for This Theme", expanded=False):
        for label, config in use_cases.items():
            st.markdown(f"**🔹 {label}**")
            st.markdown(f"*Indicators:* {', '.join(config.get('Indicators', []))}*")
            st.markdown(f"*Focus Areas:* {', '.join(config.get('Categories', []))}*")
            st.markdown(config.get("Description", "—"))
            st.markdown("---")

    return selected, use_cases
