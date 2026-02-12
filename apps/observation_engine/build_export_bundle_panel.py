# -------------------------------------------------------------------------------------------------
# 🔗 Build Export Bundle Panel
# -------------------------------------------------------------------------------------------------

import os
import json
import streamlit as st
from datetime import datetime
from pathlib import Path

from insight_loader import load_all_observations, load_snapshot_json

# -------------------------------------------------------------------------------------------------
# 📁 Export Path (Canonical Location)
# -------------------------------------------------------------------------------------------------
EXPORT_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "exports"
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 🔧 Bundle Builder — Assemble Current Snapshots & Observations
# -------------------------------------------------------------------------------------------------

def create_ai_export_bundle(bundle_name: str) -> dict:
    snapshot_entries = []
    snapshot_paths = st.session_state.get("bundle_snapshots", [])

    for snapshot_entry in snapshot_paths:
        try:
            path = snapshot_entry["source_file"]  # ✅ Extract string path from dict
            snapshot_data = load_snapshot_json(path)
            snapshot_entries.append(snapshot_data)
        except Exception as e:
            st.warning(f"⚠️ Could not load snapshot: `{snapshot_entry}` — {str(e)}")

    observation_entries = []
    observation_paths = st.session_state.get("bundle_observations", [])
    all_observations_df = load_all_observations()

    for obs_path in observation_paths:
        match = all_observations_df[all_observations_df["source_file"] == obs_path]
        if not match.empty:
            observation_entries.append(match.iloc[0].to_dict())
        else:
            st.warning(f"⚠️ Observation not found: `{obs_path}`")

    bundle = {
        "created_at": datetime.now().isoformat(),
        "bundle_name": bundle_name,
        "snapshots": snapshot_entries,
        "observations": observation_entries,
        "metadata": {
            "snapshot_count": len(snapshot_entries),
            "observation_count": len(observation_entries),
            "generated_by": "Build Export Bundle"
        }
    }

    return bundle

# -------------------------------------------------------------------------------------------------
# 💾 Save Bundle to File
# -------------------------------------------------------------------------------------------------
def save_export_bundle(bundle: dict, filename: str) -> None:
    export_path = EXPORT_FOLDER / filename
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=4)
    st.success(f"✅ Export bundle saved to `{export_path.name}`")

# -------------------------------------------------------------------------------------------------
# 🚀 UI — Build Export Bundle Panel
# -------------------------------------------------------------------------------------------------

def render_build_export_bundle_panel():
    """
    Renders the full export panel UI for assembling and saving a bundle.
    """
    st.title("🔗 Build Export Bundle")
    st.caption("Combine selected snapshots and observations into a structured bundle for AI or strategic export.")

    # ---------------------------
    # 🧾 Bundle Overview
    # ---------------------------
    st.subheader("📦 Current Bundle Overview")

    st.info(
    "🛠️ **Want to make changes to your selections?**\n\n"
    "Please return to the 📂 **Snapshot Browser** or 📋 **Observation Browser** to modify the selected items.\n\n"
    "This screen is only for previewing and exporting your current bundle."
)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**📊 Snapshots Selected:** `{len(st.session_state.get('bundle_snapshots', []))}`")
    with col2:
        st.markdown(f"**📝 Observations Selected:** `{len(st.session_state.get('bundle_observations', []))}`")

    # ---------------------------
    # 📂 Snapshot Previews (Formatted Titles)
    # ---------------------------
    raw_snapshots = st.session_state.get("bundle_snapshots", [])

    if raw_snapshots:
        with st.expander("📂 View Selected Snapshots", expanded=False):
            for entry in raw_snapshots:
                try:
                    # Load from path if string, otherwise assume dict
                    if isinstance(entry, str):
                        snap = load_snapshot_json(entry)
                    elif isinstance(entry, dict):
                        snap = entry
                    else:
                        continue  # Skip unknown formats

                    # Metadata resolution
                    theme = snap.get("theme", {}).get("title", "Unknown Theme")
                    code = snap.get("theme", {}).get("code", "unknown")
                    use_case = snap.get("use_case") or snap.get("macro_signals", [{}])[0].get("section", "Unknown Use Case")
                    country = snap.get("country", snap.get("asset", "Unknown Country"))
                    main_label = snap.get("main_module", "Trade & Portfolio Structuring")

                    # Styled display
                    if main_label == "Economic Exploration":
                        st.markdown(f"🇺🇸 {country.title()} — {code.replace('_', ' ').title()} ({main_label})")
                    else:
                        st.markdown(f"🗂️ {theme} — {country} ({main_label})")

                except Exception as e:
                    st.warning(f"⚠️ Could not preview snapshot: `{entry}` — {str(e)}")
            st.markdown("---")

    # ---------------------------
    # 📋 Observation Previews (Formatted Titles)
    # ---------------------------
    observation_paths = st.session_state.get("bundle_observations", [])
    if observation_paths:
        with st.expander("📋 View Selected Observations", expanded=False):
            obs_df = load_all_observations()
            selected_obs = obs_df[obs_df["source_file"].isin(observation_paths)]

            if selected_obs.empty:
                st.info("No valid observations found.")
            else:
                for _, row in selected_obs.iterrows():
                    country = row.get("country", "Unknown")
                    theme = row.get("theme_title", "Unknown Theme")
                    module = row.get("main_module", "Unknown Module")
                    code = row.get("theme_code", "")
                    label = f"{country.title()} — {code.replace('_', ' ').title()} ({module})"
                    st.markdown(f"🇺🇸 {label}" if "United States" in country else f"🌍 {label}")
                st.markdown("---")


    # ---------------------------
    # 💾 Bundle Builder UI
    # ---------------------------
    bundle_name = st.text_input("📁 Export Bundle Name", value="ai_export_bundle")

    if st.button("💾 Build & Save Bundle", type="primary"):
        if not bundle_name.strip():
            st.error("❌ Please provide a valid bundle name.")
            return

        bundle = create_ai_export_bundle(bundle_name.strip())
        filename = f"{bundle_name.strip()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_export_bundle(bundle, filename)

        st.success("🎉 Your AI export bundle is ready for use!")
