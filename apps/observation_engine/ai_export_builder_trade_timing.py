# -------------------------------------------------------------------------------------------------
# 🧠 AI Export Bundle Builder — Trade Timing & Confirmation (Platinum Production Build)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Builds the full machine-readable AI export bundle for Trade Timing modules.
Includes scoring metadata, indicator alignment summaries, and theme metadata for AI ingestion.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------------------------------------
import os
import sys
import json
from typing import Dict, List, Tuple
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Path Setup — Enable cross-module resolution
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # level_up_3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))        # level_up_2

# -------------------------------------------------------------------------------------------------
# Core Helpers and Path Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import get_named_paths

PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

# -------------------------------------------------------------------------------------------------
# Registry + Storage Setup
# -------------------------------------------------------------------------------------------------
REGISTRY_PATH = os.path.join(APPS_PATH, "registry")
STORAGE_FOLDER = os.path.join(APP_PATH, "observation_engine", "storage", "ai_bundles", "trade_timing")
os.makedirs(STORAGE_FOLDER, exist_ok=True)
sys.path.append(REGISTRY_PATH)

# -------------------------------------------------------------------------------------------------
# Metadata Registry — Trade Timing Definitions
# -------------------------------------------------------------------------------------------------
from registry.indicator_metadata_registry import TRADE_TIMING_METADATA

# -------------------------------------------------------------------------------------------------
# ✅ Static Use Case to Indicator Mapping
# -------------------------------------------------------------------------------------------------
metadata_indicators = {
    "Naked Charts": [],
    "General Market Overview": ["Simple Moving Average", "Bollinger Bands"],
    "Trend Strength & Direction": ["Average Directional Index", "Simple Moving Average", "Exponential Moving Average"],
    "Reversal Identification": ["Average Directional Index", "Super Trend", "Parabolic SAR"],
    "Momentum Reversal Signals": ["Moving Average Convergence Divergence", "Relative Strength Index", "Chande Momentum Oscillator"],
    "Institutional Activity & Trend Validity": ["On Balance Volume", "Accumulation/Distribution Line"],
    "Risk & Expected Price Swings": ["Average True Range", "Bollinger Bands", "Standard Deviation"],
    "Reversal & Continuation Patterns": ["Candlestick Patterns", "Head & Shoulders", "Flags & Pennants", "Double Tops/Bottoms"]
}

# -------------------------------------------------------------------------------------------------
# AI Export Bundle Builder — Trade Timing
# -------------------------------------------------------------------------------------------------
def build_macro_insight_snapshot_trade_timing(
    asset: str,
    summary_df: pd.DataFrame,
    timeframe_summary: Dict[str, str],
    execution_readiness_label: str,
    score_explanation: str,
    predisposition: str,
    use_case_name: str,
    indicator_weights: Dict[str, int],
    theme_code: str = "trade_timing",
    metadata_lookup: Dict = None
) -> Tuple[bool, str]:
    """
    Builds and saves a full AI export bundle for Trade Timing using summary_df and TRADE_TIMING_METADATA.
    Returns:
        Tuple[bool, str]: (True, filename) if successful, else (False, error message)
    """
    try:
        # -- Load Metadata Source --
        use_case_metadata = metadata_lookup if metadata_lookup else TRADE_TIMING_METADATA.get(use_case_name, {})
        indicator_block = use_case_metadata.get("indicators", {})

        # -- Static Indicator Mapping --
        indicators_present = metadata_indicators.get(use_case_name, [])

        # -- Metadata for Present Indicators Only --
        metadata_entries = {}
        primary_meta = TRADE_TIMING_METADATA.get(use_case_name, {}).get("indicators", {})

        for indicator in indicators_present:
            # Prefer metadata from the current use case
            if indicator in primary_meta:
                metadata_entries[indicator] = primary_meta[indicator]
            else:
                # Fallback: search all use cases
                for meta in TRADE_TIMING_METADATA.values():
                    if "indicators" in meta and indicator in meta["indicators"]:
                        metadata_entries[indicator] = meta["indicators"][indicator]
                        break

        # -- Weights for Present Indicators Only --
        active_weights = {k: v for k, v in indicator_weights.items() if k in indicators_present and v > 0}

        # -- Signal Translation Mapping --
        def translate_signal(raw_signal: str) -> str:
            raw_signal = raw_signal.lower()
            if "align" in raw_signal or "confirm" in raw_signal or "support" in raw_signal:
                return "Aligns"
            elif "contradict" in raw_signal or "oppose" in raw_signal or "weaken" in raw_signal or "mean reversion" in raw_signal:
                return "Contradict"
            else:
                return "Neutral"

        # -- Macro Signals Block (Translated) --
        macro_signals = []
        for _, row in summary_df.iterrows():
            raw_signal = str(row.get("Signal", "")).strip()
            translated = translate_signal(raw_signal)

            macro_signals.append({
                "Timeframe": str(row.get("Timeframe", "")),
                "Indicator": str(row.get("Indicator", "")),
                "Signal": translated,
                "Predisposition": str(predisposition),
                "Confirmation": str(row.get("Confirmation", "")),
                "Insight": str(row.get("Insight", ""))
            })

        # -- Timeframe Execution Readiness --
        timeframe_readiness = [
            {"Timeframe": tf, "Execution Readiness": msg}
            for tf, msg in timeframe_summary.items()
        ]

        # -- Theme Section (Exclude Empty Fields) --
        theme_block = {
            "code": theme_code,
            "title": use_case_name
        }
        if use_case_metadata.get("overview"):
            theme_block["overview"] = use_case_metadata["overview"]
        if use_case_metadata.get("why_it_matters"):
            theme_block["why_it_matters"] = use_case_metadata["why_it_matters"]
        if use_case_metadata.get("Categories"):
            theme_block["categories"] = use_case_metadata["Categories"]
        if use_case_metadata.get("Description"):
            theme_block["description"] = use_case_metadata["Description"]

        # -- Export Bundle --
        export_bundle = {
            "base_asset": asset,
            "predisposition": predisposition,
            "theme": theme_block,
            "scoring_methodology": {
                "weights": active_weights,
                "bias_logic": {
                    "align": "+1.0 * weight",
                    "neutral": "0.0",
                    "contradict": "-1.0 * weight"
                },
                "explanation": "Each indicator is scored based on its alignment with the "
                "trade bias. Alignment adds weight, contradiction subtracts, neutral "
                "is zero-weighted."
            },
            "use_case": use_case_name,
            "timeframe": None,
            "execution_alignment_score": 0.0,
            "execution_readiness_label": execution_readiness_label,
            "score_explanation": score_explanation,
            "timeframe_readiness": timeframe_readiness,
            "macro_signals": macro_signals,
            "metadata": metadata_entries
        }
        return True, export_bundle


    except Exception as e:
        return False, str(e)

# -------------------------------------------------------------------------------------------------
# ✅ END — Final Export Builder for Trade Timing
# -------------------------------------------------------------------------------------------------
