# -------------------------------------------------------------------------------------------------
# Manage Snapshots Panel (Platinum Implementation)
# -------------------------------------------------------------------------------------------------

import os
import streamlit as st

from insight_loader import list_all_files, resolve_snapshot_metadata
from snapshot_browser_panel import extract_metadata, build_snapshot_label

# -------------------------------------------------------------------------------------------------
# Snapshot Display Label
# -------------------------------------------------------------------------------------------------
def build_snapshot_display_label(filepath: str) -> str:
    """
    Builds a clean, human-readable display label using the same metadata
    resolution path as Snapshot Browser.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            import json
            content = json.load(f)

        bundle = resolve_snapshot_metadata(content, filepath)
        meta = extract_metadata(bundle)
        return build_snapshot_label(meta)

    except Exception:
        filename = os.path.basename(filepath).replace(".json", "")
        return f"🗂️ {filename.replace('_', ' ').title()}"

# -------------------------------------------------------------------------------------------------
# Manage AI Snapshots Panel
# -------------------------------------------------------------------------------------------------
def render_manage_snapshots_panel():
    st.header("Manage Snapshots")
    st.caption("Review or delete AI-generated snapshot files across modules.")

    if st.button("Reload Snapshot List", key="reload_snapshot_list"):
        st.rerun()

    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "storage", "ai_bundles")
    )

    all_json_files = list_all_files(base_path, extension=".json")

    if not all_json_files:
        st.warning("No snapshot files found.")
        return

    label_map = {}
    for file_path in all_json_files:
        label = build_snapshot_display_label(file_path)

        # Avoid accidental collisions if two files produce the same label.
        if label in label_map:
            label = f"{label} — {os.path.basename(file_path)}"

        label_map[label] = file_path

    selected_label = st.selectbox("Select Snapshot File", options=list(label_map.keys()))
    selected_file = label_map[selected_label]

    st.markdown(f"**File Path:** `{selected_file}`")

    try:
        with open(selected_file, "r", encoding="utf-8") as f:
            raw_json = f.read()
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        return

    with st.expander("View Snapshot JSON"):
        st.code(raw_json, language="json")

    if st.button("🗑️ Delete This Snapshot"):
        try:
            os.remove(selected_file)
            st.success(f"Deleted `{os.path.basename(selected_file)}`.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to delete file: {e}")
