# -------------------------------------------------------------------------------------------------
# 🧠 Observation Handler — Trade Structuring & Risk Planning (Reflection Notes Only)
# -------------------------------------------------------------------------------------------------

import os
import csv
import datetime
from typing import List
import pandas as pd
import streamlit as st


# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
USER_OBSERVATION_FOLDER = os.path.join(STORAGE_FOLDER, "user_observations")
MODULE_TYPE = "trade_portfolio_structuring/trade_structuring"
FIXED_FILENAME = "default__trade_structuring__user_observations.csv"

def ensure_module_folder() -> str:
    folder = os.path.join(USER_OBSERVATION_FOLDER, MODULE_TYPE)
    os.makedirs(folder, exist_ok=True)
    return folder

def observation_input_form(form_key: str = "ts_observation_form") -> None:
    clear_key = f"{form_key}_clear"
    if st.button("🧹 Clear Reflection", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("📝 Trade Planning Reflection")
        st.caption("Optional free-form notes on why you're preparing this trade.")
        observation_text = st.text_area("Planning Note", height=120, key=f"{form_key}_text")

        optional_tags = st.multiselect("Optional Tags:", [
            "Confluence", "Macro Setup", "Price Action", "Reversal", "Breakout",
            "Sentiment Signal", "Technical Structure", "Event Risk", "Sector Play"
        ], key=f"{form_key}_tags")

        submitted = st.form_submit_button("Save Reflection")
        if submitted and observation_text.strip():
            save_observation(observation_text.strip(), optional_tags)
            st.success("✅ Reflection saved.")

def save_observation(observation_text: str, tags: List[str]) -> None:
    folder = ensure_module_folder()
    file_path = os.path.join(folder, FIXED_FILENAME)

    entry = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "observation_text": observation_text,
        "tags": ", ".join(tags) if tags else ""
    }

    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def display_observation_log() -> None:
    folder = ensure_module_folder()
    file_path = os.path.join(folder, FIXED_FILENAME)

    st.subheader("📘 Planning Reflections Journal")

    if not os.path.exists(file_path):
        st.info("No reflections recorded yet.")
        return

    if st.button("🔄 Refresh Reflections"):
        st.rerun()

    df = pd.read_csv(file_path)
    df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.markdown("""
    🔎 **Edit or Delete Entries:**
    - Directly edit any field inline.
    - To delete a row: select row → click trash bin icon 🗑️ next to row.
    - Changes will only be permanently saved when you click **Save Journal Updates**.
    """)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        height=450,
        num_rows="dynamic",
        key="ts_reflection_editor"
    )

    if st.button("💾 Save Updates"):
        edited_df.to_csv(file_path, index=False)
        st.success("✅ Reflections updated.")
