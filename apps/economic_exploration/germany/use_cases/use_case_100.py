# -------------------------------------------------------------------------------------------------
# 📈 Economic Growth Stability — Use Case Definitions (Local Wrapper)
# -------------------------------------------------------------------------------------------------
# This module defines and renders use cases for Theme 100 (Economic Growth Stability),
# combining universal GDP-related logic with optional national extensions.
#
# Used within the thematic module to guide insight generation and scoring alignment.
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, line-too-long, unused-argument

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
🧩 Local Use Case Definitions — Thematic Module Extensions (Country-Specific)
-----------------------------------------------------------------------

This module defines country-specific use case mappings for a given thematic module
within the Economic Exploration suite. It extends the universal system scaffolding
to incorporate national datasets, special signals, or additional analytical focus.

✅ System Role:
- Provides merged use case dictionaries combining:
    • Universal scaffolding (imported from `universal_use_cases_XXX.py`)
    • Local country-specific extensions (added in this module)

- Controls UI rendering for:
    • Use case dropdown selectors
    • Tab ordering and visualization layers
    • Scoring alignment consistency

🧠 AI Persona & DSS Notes:
- Use case keys here must exactly match those defined in:
    • Local `indicator_map_XXX.py`
    • Local `insight_XXX.py`
    • Local `scoring_weights_labels_XXX.py`

- Output structure drives:
    • AI export pathways
    • Macro alignment summaries
    • Observational journaling flows
    • Triangular navigation program architecture

⚙️ Structure & Interface Governance:
1️⃣ **Universal Merge Foundation**
    - This file imports the corresponding universal use case map as the default base.
    - Local updates must preserve universal structure integrity.

2️⃣ **Strict Key Matching**
    - Added local use cases must ensure indicator keys match local indicator maps exactly.

3️⃣ **Metadata Fields**
    - `"Indicators"` → List of signal functions attached to the use case
    - `"Categories"` → System UI grouping for streamlit interface alignment
    - `"Description"` → Narrative framing for AI personas and DSS journaling

🧭 Governance Note:
- Local use case modules allow flexible adaptation by country.
- The universal scaffolding remains stable and externally governed.
- Local users configure national extensions here — but must preserve structural integrity.
"""

# -------------------------------------------------------------------------------------------------
# 📦 Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import streamlit as st

# -------------------------------------------------------------------------------------------------
# 🧭 Universal Use Case Path Setup
# -------------------------------------------------------------------------------------------------
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))
UNIVERSAL_PATH = os.path.abspath(os.path.join(LOCAL_PATH, "..", "universal_use_cases"))
if UNIVERSAL_PATH not in sys.path:
    sys.path.append(UNIVERSAL_PATH)

# -------------------------------------------------------------------------------------------------
# 🔁 Import and Merge Use Cases
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
# 🔓 Getter — Unified Use Case Dictionary
# -------------------------------------------------------------------------------------------------
def get_use_cases() -> dict:
    """
    Returns the merged set of universal and local use cases.

    Returns:
        dict: Use case definitions with labels, indicators, and descriptions.
    """
    return USE_CASES

# -------------------------------------------------------------------------------------------------
# 🎛️ Sidebar Use Case Selector
# -------------------------------------------------------------------------------------------------
def render_use_case_selector(get_use_cases_fn) -> tuple[str, dict]:
    """
    Renders a Streamlit sidebar selector and contextual detail display for use cases.

    Args:
        get_use_cases_fn (callable): Function that returns the available use cases.

    Returns:
        tuple:
            selected_use_case (str): Selected use case label.
            use_cases (dict): Full dictionary of available use cases.
    """
    try:
        use_cases = get_use_cases_fn()
    except Exception as e:
        st.error(f"❌ Could not load use cases: {type(e).__name__} – {str(e)}")
        return None, {}

    st.sidebar.title("📌 Select a Use Case")
    selected = st.sidebar.selectbox("Insight Use Case", list(use_cases.keys()), index=0)

    with st.sidebar.expander("🎯 Use Cases for This Theme", expanded=False):
        for label, config in use_cases.items():
            st.markdown(f"**🔹 {label}**")
            st.markdown(f"*Indicators:* {', '.join(config.get('Indicators', []))}*")
            st.markdown(f"*Focus Areas:* {', '.join(config.get('Categories', []))}*")
            st.markdown(config.get("Description", "—"))
            st.markdown("---")

    return selected, use_cases
