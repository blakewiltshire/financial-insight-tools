# -------------------------------------------------------------------------------------------------
# 📦 Insight Loader — Observations & Snapshots (Platinum-Grade, Filename-Driven Version)
# -------------------------------------------------------------------------------------------------

import os
import json
import re
import pandas as pd
from typing import List, Dict, Optional

# -------------------------------------------------------------------------------------------------
# 📁 Base Paths
# -------------------------------------------------------------------------------------------------

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
OBS_PATH = os.path.join(BASE_PATH, "user_observations")
SNAPSHOT_PATH = os.path.join(BASE_PATH, "ai_bundles")

# -------------------------------------------------------------------------------------------------
# 🧭 Main Module Labels (folder-driven)
# -------------------------------------------------------------------------------------------------

MAIN_MODULE_GROUPS = {
    "economic_exploration": "Economic Exploration",
    "intermarket_correlation": "Intermarket & Correlation",
    "reference_data": "Reference Data & Trusted Sources",
    "trade_portfolio_structuring": "Trade & Portfolio Structuring"
}

# -------------------------------------------------------------------------------------------------
# 🔧 Submodule Labels (filename-driven from second segment)
# -------------------------------------------------------------------------------------------------

MODULE_DISPLAY_LABELS = {
    # 🌍 Economic Exploration
    "economic_exploration": "Economic Exploration",
    "thematic_correlation": "Thematic Correlation",

    # 🔗 Intermarket Correlation
    "correlation_heatmaps": "Correlation Heatmaps & Themes",
    "cross_asset_correlation": "Cross-Asset Correlation",
    "spread_ratio_insights": "Spread & Ratio Insights",

    # 🗂 Reference Data
    "classification_schema": "Classification Schema Viewer",

    # 🧭 Trade & Portfolio Structuring
    "market_scanner": "Market & Volatility Scanner",
    "price_action": "Price Action & Trend Confirmation",
    "trade_timing": "Trade Timing & Confirmation",
    "trade_structuring": "Trade Structuring & Risk Planning",
    "trade_history": "Trade History & Strategy",
    "live_portfolio": "Live Portfolio Monitor"
}

# -------------------------------------------------------------------------------------------------
# 📁 File Utilities
# -------------------------------------------------------------------------------------------------

def list_all_files(base_folder: str, extension: str = ".csv") -> List[str]:
    matches = []
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(extension):
                matches.append(os.path.join(root, file))
    return sorted(matches)

# -------------------------------------------------------------------------------------------------
# 📋 Load User Observations (Filename-Driven Parsing)
# -------------------------------------------------------------------------------------------------

def load_all_observations() -> pd.DataFrame:
    records = []

    for file in list_all_files(OBS_PATH, extension=".csv"):
        try:
            df = pd.read_csv(file)
            rel_path = os.path.relpath(file, BASE_PATH)
            path_parts = rel_path.split(os.sep)
            filename = os.path.basename(file)
            filename_parts = filename.split("__")

            # Parse Main and Submodule from path + filename
            module_type = path_parts[1] if len(path_parts) > 1 else "unknown"
            sub_key = filename_parts[1] if len(filename_parts) > 2 else module_type

            # Apply hardcoded label mapping
            df["main_module"] = MAIN_MODULE_GROUPS.get(module_type, module_type.replace("_", " ").title())
            df["module"] = MODULE_DISPLAY_LABELS.get(sub_key, sub_key.replace("_", " ").title())
            df["context"] = filename.replace("_user_observations.csv", "")
            df["source_file"] = rel_path

            # Assign optional metadata fields
            df["country"] = df["country"] if "country" in df.columns else ""
            df["assets_selected"] = df["indicators_selected"] if "indicators_selected" in df.columns else ""
            df["macro_indicators"] = df["indicator"] if "indicator" in df.columns else ""

            # Fallback timestamp if missing
            if "timestamp" not in df.columns or df["timestamp"].isnull().all():
                df["timestamp"] = pd.to_datetime(os.path.getmtime(file), unit="s")

            # Required columns for unified structure
            required = [
                "timestamp", "country", "theme_code", "theme_title", "indicator", "use_case",
                "observation_text", "relevance_tag", "sentiment_tag", "timeframe",
                "observation_type", "tags", "assets_selected", "macro_indicators"
            ]
            for col in required:
                if col not in df.columns:
                    df[col] = ""

            records.append(df)

        except Exception:
            continue

    return pd.concat(records, ignore_index=True) if records else pd.DataFrame()

# -------------------------------------------------------------------------------------------------
# 🧠 Load AI Snapshots (Used in Snapshot Browser)
# -------------------------------------------------------------------------------------------------

def load_all_snapshots() -> List[Dict]:
    bundles = []
    for file in list_all_files(SNAPSHOT_PATH, extension=".json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = json.load(f)
                bundle = resolve_snapshot_metadata(content, file)
                bundles.append(bundle)
        except Exception:
            continue
    return bundles

def resolve_snapshot_metadata(content: Dict, filepath: str) -> Dict:
    theme = content.get("theme", {})
    theme_title = theme.get("title", "Unknown Module")
    module_code = theme.get("code", "unknown")

    if "snapshot_metadata" in content:
        # Market & Volatility Scanner
        asset = content["snapshot_metadata"].get("base_asset", "Unknown Asset")
        use_case = content.get("macro_signals", [{}])[0].get("section", "Unknown")
        timestamp = content["snapshot_metadata"].get("snapshot_timestamp")

    elif "use_cases" in content:
        # Economic Modules
        use_case_block = content.get("use_cases", [{}])[0]
        use_case = use_case_block.get("name", "Unknown")
        asset = content.get("country", "Unknown Country")
        timestamp = use_case_block.get("macro_signals", [{}])[0].get("timestamp")

    else:
        # Trade Timing or Price Action
        use_case = content.get("use_case", "Naked Charts")
        asset = content.get("base_asset", "Unknown")
        timestamp = content.get("snapshot_timestamp")

    return {
        "theme_title": theme_title,
        "module_code": module_code,
        "use_case": use_case,
        "asset": asset,
        "timestamp": timestamp or os.path.getmtime(filepath),
        "source_file": os.path.relpath(filepath, BASE_PATH),
        "raw": content  # 🛑 Do not remove — required for downstream inspection
    }

def load_snapshot_json(relative_path: str) -> dict:
    """
    Loads a single snapshot file from the canonical base storage path.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
    full_path = os.path.join(base_path, relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
