# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Local Use Case Definitions — Thematic Module
------------------------------------------------

Defines the insight use cases presented to the user for this theme.
Each use case describes a core economic interpretation (e.g. "Unemployment Context").

Structure:
- Simple list of strings representing available analysis lenses
- Must align with logic in the universal visual dispatcher
- Must match entries in `indicator_map` and `visual_config`

AI Notes:
- Use cases drive both insight panels and alignment scoring
- Ensure consistency across `use_cases`, `indicator_map`, and visuals

Usage:
- Loaded by the theme module to populate sidebar selectors
- Override only when adjusting thematic focus or use case names
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Add universal use case path explicitly
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_use_cases"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# Import and merge use cases
# -------------------------------------------------------------------------------------------------
from universal_use_cases_000 import get_use_cases as get_universal_use_cases

USE_CASES = dict(get_universal_use_cases())  # Shallow copy for local extension

# Optionally extend below
USE_CASES.update({
    # "Macro Composite Signals (Local)": {
    #     "Indicators": [
    #         "Composite Output Index",
    #         "National Activity Tracker",
    #         "Local Economic Uncertainty Index",
    #         "Regional PMI Series"
    #     ],
    #     "Categories": ["Macro Composite"],
    #     "Description": "Tracks short-term national macro momentum using composite indicators —
    #     including growth, sentiment, and uncertainty dynamics."
    # }
})


def get_use_cases():
    """
    Returns the combined dictionary of universal and localised use cases.

    Returns:
        dict: Merged use cases with optional local overrides or additions.
    """
    return USE_CASES


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
