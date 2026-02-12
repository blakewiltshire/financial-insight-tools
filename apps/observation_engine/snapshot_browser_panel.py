# -------------------------------------------------------------------------------------------------
# 🧠 Snapshot Browser Panel — Final Platinum-Grade Version
# -------------------------------------------------------------------------------------------------

import os
import streamlit as st
import pandas as pd
import json
import uuid
from typing import List, Dict
from datetime import datetime

from insight_loader import load_all_snapshots

def extract_metadata(bundle: Dict) -> Dict:
    """
    Extract and format snapshot metadata for display and filtering,
    with strict rules for module-specific visibility.
    """
    source = bundle.get("source_file", "")
    raw = bundle.get("raw", {})
    module_code = bundle.get("module_code", "unknown")
    filename = os.path.basename(source)

    # Base fields
    timestamp = parse_timestamp(bundle.get("timestamp"))
    timeframe = extract_timeframe_from_filename(source)
    asset = bundle.get("asset") or extract_filename_asset(source)
    use_case = bundle.get("use_case", "")
    theme_title = bundle.get("theme_title", "")

    # 📊 Economic Exploration
    if module_code.startswith("100") or "economic_exploration" in source:
        return {
            "title": "📊 Economic Exploration",
            "module": "Economic Exploration",
            "theme_title": theme_title or "Unknown",
            "use_case": use_case or "Unknown",
            "country": asset,
            "asset": "",  # suppress in card
            "timeframe": timeframe,
            "timestamp": timestamp,
            "source_file": source,
        }

    # 📊 Market Volatility
    if "market_volatility" in source:
        stat_groups = extract_statistical_groupings(raw)
        return {
            "title": "📊 Market Volatility",
            "module": "Market Volatility",
            "theme_title": "",  # suppress misleading grouping
            "use_case": "",     # not applicable
            "country": "",      # not applicable
            "asset": asset,
            "stat_groups": stat_groups,
            "timeframe": timeframe,
            "timestamp": timestamp,
            "source_file": source,
        }

    # 📊 Price Action
    if "price_action" in source:
        if use_case == "Unknown" and "__unknown__" in filename:
            use_case = "Naked Charts (Unknown)"
        return {
            "title": "📊 Price Action",
            "module": "Price Action",
            "theme_title": "",
            "use_case": use_case or "",
            "country": "",
            "asset": asset,
            "timeframe": timeframe,
            "timestamp": timestamp,
            "source_file": source,
        }

    # 📊 Trade Timing
    if "trade_timing" in source:
        if use_case == "Unknown" and "__unknown__" in filename:
            use_case = "Naked Charts (Unknown)"
        return {
            "title": "📊 Trade Timing",
            "module": "Trade Timing",
            "theme_title": "",
            "use_case": use_case or "",
            "country": "",
            "asset": asset,
            "timeframe": timeframe,
            "timestamp": timestamp,
            "source_file": source,
        }

    # 🗂️ Unknown Module
    return {
        "title": "📁 Unknown Module",
        "module": "Unknown",
        "theme_title": "",
        "use_case": "",
        "country": "",
        "asset": asset,
        "timeframe": timeframe,
        "timestamp": timestamp,
        "source_file": source,
    }

def render_snapshot_browser_panel():
    st.header("📂 Snapshot Browser")
    st.caption("Browse all AI-generated snapshot files from across modules.")


    if st.button("🔄 Reload Snapshot List", key="reload_snapshot_list_browser"):
        st.rerun()

    bundles = load_all_snapshots()
    if not bundles:
        st.warning("No snapshots found.")
        return

    metadata_list = [extract_metadata(b) for b in bundles]
    df_meta = extract_filterable_metadata(metadata_list)

    df_meta["parsed_timestamp"] = pd.to_datetime(df_meta["timestamp"], errors="coerce")
    df_meta = df_meta.sort_values(by="parsed_timestamp", ascending=False).drop(columns="parsed_timestamp")

    df_filtered = render_snapshot_filters(df_meta)

    st.markdown(f"**🔢 {len(df_filtered)} snapshots matched your filters**")
    st.markdown("---")

    # Match only the unique filtered source files
    filtered_sources = set(df_filtered["source_file"])
    filtered_bundles = [b for b in bundles if b.get("source_file") in filtered_sources]

    for bundle in filtered_bundles:
        metadata = extract_metadata(bundle)
        source_id = metadata["source_file"]

        already_added = any(s["source_file"] == source_id for s in st.session_state["bundle_snapshots"])

        with st.container(border=True):
            st.markdown(f"### {metadata['title']}")

            if metadata['module'] == "Economic Exploration":
                st.markdown(f"**Thematic Grouping:** {metadata['theme_title']}")
                st.markdown(f"**Use Case:** {metadata['use_case']}")
                st.markdown(f"**Country:** {metadata['country']}")
            elif metadata['module'] in ["Market Volatility", "Price Action", "Trade Timing"]:
                st.markdown(f"**Asset:** {metadata['asset']}")
                if metadata['use_case']:
                    st.markdown(f"**Use Case:** {metadata['use_case']}")
                for idx, group in enumerate(metadata.get("stat_groups", []), start=1):
                    st.markdown(f"**Statistical Grouping {idx}:** {group}")

            if metadata.get("timeframe"):
                st.markdown(f"**Timeframe Periods:** {metadata['timeframe']}")
            st.markdown(f"**Timestamp:** {metadata['timestamp']}")
            st.markdown(f"**📄 Source:** `{metadata['source_file']}`")

            with st.expander("📦 Preview JSON"):
                st.json(bundle['raw'])

            col1, _ = st.columns([6, 1])
            with col1:
                btn_key = f"add_snapshot_{source_id}"
                if not already_added:
                    if st.button("➕ Add to Bundle", key=btn_key):
                        st.session_state["bundle_snapshots"].append(bundle)
                        st.rerun()
                else:
                    st.markdown("✅ **Already Added to Bundle**")

    # -------------------------------------------------------------------------------------------------
    # 📦 Current Bundle Contents
    # -------------------------------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📦 Current Bundle Contents")

    if st.session_state["bundle_snapshots"]:
        snapshots_to_keep = []
        for snap in st.session_state["bundle_snapshots"]:
            snap_meta = extract_metadata(snap)
            source_id = snap_meta["source_file"]
            safe_id = source_id.replace("/", "_").replace(".", "_")

            col1, col2 = st.columns([6, 1])
            with col1:
                label = (
                    f"{snap_meta.get('module')} — "
                    f"{snap_meta.get('use_case') or snap_meta.get('theme_title') or snap_meta.get('asset') or 'Unknown'}"
                )
                st.markdown(f"**{label}**")
                st.markdown(f"`{snap_meta['source_file']}`")

            with col2:
                remove_key = f"remove_snapshot_{safe_id}"
                if st.button("❌ Remove", key=remove_key):
                    # Mark this snapshot for removal
                    continue  # Skip appending to keep list

            snapshots_to_keep.append(snap)

        # Finalise update (only once after loop)
        if len(snapshots_to_keep) != len(st.session_state["bundle_snapshots"]):
            st.session_state["bundle_snapshots"] = snapshots_to_keep
            st.rerun()
    else:
        st.info("No snapshots currently in bundle.")


# -------------------------------------------------------------------------------------------------
# 📊 Snapshot Metadata Filter Extraction
# -------------------------------------------------------------------------------------------------
def extract_filterable_metadata(meta_list: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame([
        {
            "module": m.get("module"),
            "title": m.get("title"),
            "theme_title": m.get("theme_title"),
            "use_case": m.get("use_case"),
            "country": m.get("country") or "",
            "asset": m.get("asset") or "",
            "timeframe": m.get("timeframe"),
            "timestamp": m.get("timestamp"),
            "source_file": m.get("source_file")
        }
        for m in meta_list
    ])

# -------------------------------------------------------------------------------------------------
# 🔍 Snapshot Filter Panel (Module-aware)
# -------------------------------------------------------------------------------------------------
def render_snapshot_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("🔍 Filter Snapshots")
    col1, col2, col3 = st.columns(3)

    with col1:
        modules = st.multiselect("🧠 Module", sorted(df['module'].dropna().unique()))
        if modules:
            df = df[df['module'].isin(modules)]

    current_modules = set(df['module'].unique())

    with col2:
        if "Economic Exploration" in current_modules:
            themes = st.multiselect("📘 Thematic Grouping", sorted(df['theme_title'].dropna().unique()))
            if themes:
                df = df[df['theme_title'].isin(themes)]

    with col3:
        if any(m in current_modules for m in ["Market Volatility", "Price Action", "Trade Timing"]):
            assets = st.multiselect("💼 Asset", sorted(df['asset'].dropna().unique()))
            if assets:
                df = df[df['asset'].isin(assets)]

    col4, col5 = st.columns(2)
    with col4:
        if "Economic Exploration" in current_modules:
            countries = st.multiselect("🌍 Country", sorted(df['country'].dropna().unique()))
            if countries:
                df = df[df['country'].isin(countries)]

    with col5:
        if df['use_case'].dropna().nunique() > 0:
            use_cases = st.multiselect("🧪 Use Case", sorted(df['use_case'].dropna().unique()))
            if use_cases:
                df = df[df['use_case'].isin(use_cases)]

    return df

# -------------------------------------------------------------------------------------------------
# 🔧 Shared Helpers
# -------------------------------------------------------------------------------------------------
def extract_filename_asset(source_file: str) -> str:
    try:
        filename = os.path.basename(source_file)
        parts = filename.split("__")
        return parts[-2].replace("_", " ").title() if len(parts) >= 3 else "Unknown"
    except Exception:
        return "Unknown"

def extract_timeframe_from_filename(source_file: str) -> str:
    try:
        filename = os.path.basename(source_file).replace(".json", "")
        parts = filename.split("__")
        candidate = parts[-1].upper()
        if candidate.endswith("M") or candidate.endswith("Y"):
            return candidate
        return None
    except Exception:
        return None

def parse_timestamp(timestamp_raw) -> str:
    try:
        if isinstance(timestamp_raw, (int, float)):
            return datetime.fromtimestamp(timestamp_raw).strftime("%Y-%m-%d %H:%M")
        return datetime.fromisoformat(timestamp_raw).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "Unknown"

def extract_statistical_groupings(raw: Dict) -> List[str]:
    results = []
    try:
        macro_signals = raw.get("macro_signals", [])
        for entry in macro_signals:
            section = entry.get("section", "").strip()
            subgroup = entry.get("subgroup", "").strip()
            if section and subgroup:
                label = f"{section}: {subgroup}"
                if label not in results:
                    results.append(label)
    except Exception:
        pass
    return results
