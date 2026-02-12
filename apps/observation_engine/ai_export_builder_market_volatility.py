# -------------------------------------------------------------------------------------------------
# 📦 FINAL AI Export Snapshot Builder — No Leakage of Raw Blocks
# -------------------------------------------------------------------------------------------------

import os
import sys
from datetime import datetime

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from registry.stats_metadata_registry import STATISTICAL_METADATA

# -------------------------------------------------------------------------------------------------
# 🔒 Metadata Indicator Mapping — Keys match lowercase registry keys
# -------------------------------------------------------------------------------------------------
metadata_indicators = {
    "descriptive_statistics": [
        "Measure of Central Tendency",
        "Measures of Dispersion",
        "Measures of Shape",
        "Basic Statistics"
    ],
    "risk_and_uncertainty_analysis": [
        "Risk-Adjusted Returns (Sharpe Ratio)",
        "Downside Risk Measure (Sortino Ratio)",
        "Probability of Hitting DPT"
    ],
    "market_dynamics": [
        "Volatility Ratio",
        "ATR (Average True Range)"
    ],
    "performance_metrics": [
        "Annualised Return",
        "Maximum Drawdown",
        "Volatility-Adjusted Return",
        "Return on Investment (ROI)",
        "Volume vs ATR Correlation"
    ]
}

# -------------------------------------------------------------------------------------------------
# 🧠 Build AI-Ready Snapshot
# -------------------------------------------------------------------------------------------------
def build_macro_insight_snapshot_market_volatility(
    base_asset: str,
    asset_type_display: str,
    snapshot_results: dict,
    metadata_indicators: dict
) -> dict:
    """
    Builds AI-ready macro insight snapshot without exposing raw statistical_analysis block.
    """
    macro_signals = []
    context_parameters = snapshot_results.get("statistical_analysis", {}).get("context_parameters", {})

    for section_key, indicators in metadata_indicators.items():
        for indicator in indicators:
            try:
                value = snapshot_results.get("statistical_analysis", {}).get(section_key, {}).get(indicator)
                if value is None:
                    continue

                metadata = STATISTICAL_METADATA.get(section_key, {}).get(indicator, {})

                macro_signals.append({
                    "section": section_key,
                    "indicator": indicator,
                    "value": value,
                    "overview": metadata.get("overview", ""),
                    "why_it_matters": metadata.get("why_it_matters", ""),
                    "temporal_categorisation": metadata.get("temporal_categorisation", ""),
                    "investment_action_importance": metadata.get("investment_action_importance", "")
                })
            except Exception:
                continue

    return {
        "snapshot_metadata": {
            "base_asset": base_asset,
            "theme": {
                "code": "market_scanner",
                "title": "Market & Volatility Scanner"
            },
            "snapshot_timestamp": datetime.utcnow().isoformat(),
            "asset_type": asset_type_display
        },
        "context_parameters": context_parameters,
        "macro_signals": macro_signals,
        "metadata": snapshot_results.get("metadata", {})
    }
