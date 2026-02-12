# -------------------------------------------------------------------------------------------------
# 🧠 Observation Handler — Trade History & Strategy (Reflections on Past Trades)
# -------------------------------------------------------------------------------------------------

import os, csv, datetime
from typing import List
import pandas as pd
import streamlit as st

# 📁 Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
USER_OBSERVATION_FOLDER = os.path.join(STORAGE_FOLDER, "user_observations")
MODULE_TYPE = "trade_portfolio_structuring/trade_history"
FILENAME = "default__trade_history__user_observations.csv"

def ensure_module_folder() -> str:
    folder = os.path.join(USER_OBSERVATION_FOLDER, MODULE_TYPE)
    os.makedirs(folder, exist_ok=True)
    return folder

def observation_input_form(form_key: str = "th_observation_form") -> None:
    clear_key = f"{form_key}_clear"
    if st.button("🧹 Clear Reflection", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("📝 Trade Review Reflection")
        st.caption("Use this to reflect on past trades, recurring patterns, or behavioural lessons.")
        observation_text = st.text_area("Reflection Note", height=120, key=f"{form_key}_text")

        optional_tags = st.multiselect("Optional Tags:", [
            "Overconfidence", "Perfect Entry", "Missed Exit", "Chased Trade",
            "Followed Plan", "Ignored Signal", "Good Risk Control"
        ], key=f"{form_key}_tags")

        submitted = st.form_submit_button("Save Reflection")
        if submitted and observation_text.strip():
            save_observation(observation_text.strip(), optional_tags)
            st.success("✅ Reflection saved.")

def save_observation(observation_text: str, tags: List[str]) -> None:
    file_path = os.path.join(ensure_module_folder(), FILENAME)
    entry = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "observation_text": observation_text,
        "tags": ", ".join(tags) if tags else ""
    }
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def display_observation_log() -> None:
    """
    Displays saved observations with inline edit and delete features.
    """
    file_path = os.path.join(ensure_module_folder(), FILENAME)

    st.subheader("📘 Reflections on Historical Trades")

    if not os.path.exists(file_path):
        st.info("No reflections recorded yet.")
        return

    if st.button("🔄 Refresh Reflections"):
        st.rerun()

    df = pd.read_csv(file_path).sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.markdown("""
    🔎 **Edit or Delete Entries:**
    - Directly edit any field inline.
    - To delete a row: select row → click trash bin icon 🗑️ next to row.
    - Changes will only be permanently saved when you click **Save Journal Updates**.
    """)


    edited_df = st.data_editor(df, width='stretch', height=450, key="th_editor")

    if st.button("💾 Save Updates"):
        edited_df.to_csv(file_path, index=False)
        st.success("✅ Reflections updated.")
