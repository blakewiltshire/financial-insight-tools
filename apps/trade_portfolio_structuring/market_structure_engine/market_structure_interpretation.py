# -------------------------------------------------------------------------------------------------
# Market Structure Interpretation
# -------------------------------------------------------------------------------------------------
"""Plain-English interpretation builder for Market Structure Review."""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Interpretation Builder
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Interpretation Builder
# -------------------------------------------------------------------------------------------------
def build_market_structure_interpretation(
    dataset_name: str,
    profile_df: pd.DataFrame,
    events_df: pd.DataFrame,
    summary_payload: dict,
) -> str:
    """Create a concise focus-asset structural interpretation."""

    focus_context = summary_payload.get("observation_context", {}).get("focus_asset_context", {})

    ownership_structure = focus_context.get("ownership_structure", "N/A")
    float_structure = focus_context.get("float_structure", "N/A")
    supply_structure = focus_context.get("supply_structure", "N/A")
    institutional_participation = focus_context.get("institutional_participation", "N/A")

    return f"""
**Ownership Structure:**
{ownership_structure}

**Float Structure:**
{float_structure}

**Supply Structure:**
{supply_structure}

**Institutional Participation:**
{institutional_participation}

"""
