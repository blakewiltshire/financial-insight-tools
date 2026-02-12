# -------------------------------------------------------------------------------------------------
# 📥 Load / Restore Panel — Final Build with AI Response Upload, Save, and Management
# -------------------------------------------------------------------------------------------------

import os
import sys
import json
from pathlib import Path

import streamlit as st
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.helpers import get_named_paths  # pylint: disable=import-error

PATHS = get_named_paths(__file__)
EXPORT_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "exports"
RETURN_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "returns"

EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)
RETURN_FOLDER.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# 📅 Load / Restore Panel
# -------------------------------------------------------------------------------------------------
def render_load_restore_panel():
    st.title("📥 Load / Restore")
    st.caption("Manage insight bundles and AI responses. Preview contents, download, or delete entries.")

    tab1, tab2 = st.tabs(["📦 Insight Bundles", "🧠 AI Responses"])

    # -------------------------------------------------------------------------------------------------
    # Tab 1: Insight Bundles (JSON)
    # -------------------------------------------------------------------------------------------------
    with tab1:
        st.subheader("📦 Insight Bundles")
        bundle_files = list(EXPORT_FOLDER.glob("*.json"))
        selected = st.selectbox("Select JSON Bundle", ["None"] + [f.name for f in bundle_files])

        if selected != "None":
            filepath = EXPORT_FOLDER / selected
            st.markdown(f"**📂 File:** `{filepath.name}`")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                st.json(data)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button("📥 Download JSON", data=json.dumps(data, indent=2), file_name=filepath.name)
            with col2:
                if st.button("🗑️ Delete File"):
                    filepath.unlink()
                    st.success(f"Deleted {filepath.name}")
                    st.rerun()

    # -------------------------------------------------------------------------------------------------
    # Tab 2: AI Responses (Markdown)
    # -------------------------------------------------------------------------------------------------
    with tab2:
        st.subheader("🧠 AI Responses")

        # Section: Upload a New AI Response
        # Section: Upload a New AI Response
        uploaded_file = st.file_uploader("📂 Upload AI Response (.md)", type=["md"])
        if uploaded_file is not None:
            uploaded_text = uploaded_file.read().decode("utf-8")
            st.markdown("**🔍 Preview:**")
            st.markdown(uploaded_text)

            if st.button("📥 Save to AI Returns Library"):
                save_path = RETURN_FOLDER / uploaded_file.name
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(uploaded_text)
                st.success(f"Saved to: `{save_path}`")
                st.rerun()

        st.divider()

        # Section: Manage Saved Responses
        st.markdown("### 🧠 Saved AI Responses")
        md_files = list(RETURN_FOLDER.glob("*.md"))
        selected_md = st.selectbox("Select Markdown File", ["None"] + [f.name for f in md_files], key="ai_response_select")

        if selected_md != "None":
            filepath = RETURN_FOLDER / selected_md
            st.markdown(f"**📂 File:** `{filepath.name}`")
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
                st.markdown(md_content)

            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button("📥 Download Markdown", data=md_content, file_name=filepath.name)
            with col2:
                if st.button("🗑️ Delete File", key="delete_md"):
                    filepath.unlink()
                    st.success(f"Deleted {filepath.name}")
                    st.rerun()
