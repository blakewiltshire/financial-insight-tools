# -------------------------------------------------------------------------------------------------
# 🧠 AI Export Bundle Builder — Platinum Canonical Build (Filename Aligned, Production Locked)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Generates full AI export bundles across country modules with scoring metadata,
fully merged indicator weights (universal + local), user observations, and registry metadata.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import json
import importlib.util
from typing import List, Dict
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Path Resolution (Strict Canonical Absolute Path)
# -------------------------------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
APPS_PATH = os.path.join(PROJECT_BASE, "economic_exploration")

# Unified AI Bundles storage location
AI_BUNDLES_FOLDER = os.path.join(PROJECT_BASE, "observation_engine", "storage", "ai_bundles", "economic_exploration")
os.makedirs(AI_BUNDLES_FOLDER, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# External Imports (Registry + Observations)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(PROJECT_BASE, "registry"))
from thematic_groupings import THEMATIC_GROUPS  # pylint: disable=import-error

from observation_handler_economic_exploration import export_observations_for_ai

# -------------------------------------------------------------------------------------------------
# Build AI Bundle
# -------------------------------------------------------------------------------------------------
def create_theme_ai_bundle(
    country: str,
    theme_code: str,
    theme_title: str,
    use_case_scores: Dict[str, float],
    use_case_labels: Dict[str, str],
    use_case_explanations: Dict[str, str],
    summary_table_map: Dict[str, pd.DataFrame],
    selected_timeframe: str
) -> dict:
    """
    Build full AI bundle for given country + theme.
    """
    theme_data = THEMATIC_GROUPS.get(theme_code, {})
    if not theme_data:
        raise ValueError(f"No theme data found for theme_code: {theme_code}")

    indicator_weights = load_country_indicator_weights(country, theme_code)

    # 🔧 Unified observation loading — filename-aligned version
    all_user_obs = export_observations_for_ai(
        module_type="economic_exploration",
        country=country,
        theme_code=theme_code
    )

    bundle = {
        "country": country,
        "theme": {
            "code": theme_code,
            "title": theme_data.get("theme_title"),
            "introduction": theme_data.get("theme_introduction"),
            "navigating_the_theme": theme_data.get("navigating_the_theme"),
            "data_points": theme_data.get("data_points", []),
            "conclusion": theme_data.get("conclusion_and_further_exploration"),
        },
        "scoring_methodology": {
            "bias_reference": "Growth Supportive",
            "weights": indicator_weights,
            "bias_logic": {
                "align": "+1.0 * weight",
                "neutral": "+0.5 * weight",
                "contradict": "-1.0 * weight"
            },
            "explanation": (
                "Each indicator signal is compared against its bias reference. "
                "Alignment applies full weight, neutral applies half, contradiction subtracts full weight."
            )
        },
        "use_cases": []
    }

    memberships = theme_data.get("memberships", {})

    for use_case in use_case_scores:
        score = use_case_scores.get(use_case)
        label = use_case_labels.get(use_case)
        explanation = use_case_explanations.get(use_case)
        signal_df = summary_table_map.get(use_case)

        user_observations = [
            obs for obs in all_user_obs
            if obs.get("theme", "").strip().lower() == theme_title.strip().lower()
            and obs.get("indicator") == use_case
            and obs.get("timeframe") == selected_timeframe
        ]

        metadata = []
        for indicator_id, meta in memberships.items():
            if (
                meta.get("Use Case", "").strip().lower() == use_case.strip().lower()
                or meta.get("title", "").strip().lower() == use_case.strip().lower()
            ):
                metadata.append({
                    "use_case_metric": meta.get("title") or use_case,
                    "overview": meta.get("overview"),
                    "why_it_matters": meta.get("why_it_matters"),
                    "temporal_categorisation": meta.get("temporal_categorisation"),
                    "investment_action_importance": meta.get("investment_action_importance"),
                    "personal_impact_importance": meta.get("personal_impact_importance"),
                    "recommended_time_periods": meta.get("recommended_time_periods")
                })

        use_case_entry = {
            "name": use_case,
            "timeframe": selected_timeframe,
            "macro_score": f"{score:.1f}" if score is not None else None,
            "score_label": label,
            "score_explanation": explanation,
            "macro_signals": signal_df.to_dict(orient="records") if signal_df is not None else [],
            "user_observations": user_observations,
            "metadata": metadata
        }
        bundle["use_cases"].append(use_case_entry)

    return bundle

# -------------------------------------------------------------------------------------------------
# Load Country Indicator Weights
# -------------------------------------------------------------------------------------------------
def load_country_indicator_weights(country: str, theme_code: str) -> dict:
    """
    Load fully merged weights from local scoring files.
    """
    local_path = os.path.join(
        PROJECT_BASE, "economic_exploration",
        country, "scoring_weights_labels",
        f"scoring_weights_labels_{theme_code}.py"
    )

    if not os.path.isfile(local_path):
        raise FileNotFoundError(f"Missing scoring file for country: {country}, theme: {theme_code}")

    spec = importlib.util.spec_from_file_location("scoring_weights_labels", local_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.indicator_weights

# -------------------------------------------------------------------------------------------------
# Save AI Bundle to File
# -------------------------------------------------------------------------------------------------
def save_ai_bundle_to_file(bundle: dict, replace_existing: bool = True) -> str:
    """
    Save AI bundle JSON using strict filename logic with country + theme + use_case + timeframe.
    """
    country = bundle.get("country", "unknown_country")
    theme_code = bundle.get("theme", {}).get("code", "unknown_theme")
    use_case = bundle.get("use_cases", [{}])[0].get("name", "unknown_use_case")
    timeframe = bundle.get("use_cases", [{}])[0].get("timeframe", "unknown_timeframe")

    filename = f"economic_exploration__{country}__{theme_code}__{use_case.lower().replace(' ', '_')}__{timeframe}.json"
    file_path = os.path.join(AI_BUNDLES_FOLDER, filename)

    if os.path.exists(file_path) and not replace_existing:
        return f"⚠️ File already exists: {filename}"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=4)

    return f"📁 Snapshot saved to: {filename}"


# -------------------------------------------------------------------------------------------------
# END — Platinum Canonical AI Export Builder
# -------------------------------------------------------------------------------------------------
