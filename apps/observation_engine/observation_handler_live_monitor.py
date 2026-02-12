# -------------------------------------------------------------------------------------------------
# 🧠 Observation Handler — Live Portfolio Monitor (Real-Time Portfolio Health Notes)
# -------------------------------------------------------------------------------------------------

import os, csv, datetime
from typing import List
import pandas as pd
import streamlit as st

# 📁 Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
USER_OBSERVATION_FOLDER = os.path.join(STORAGE_FOLDER, "user_observations")
MODULE_TYPE = "trade_portfolio_structuring/live_portfolio"
FILENAME = "default__live_portfolio__user_observations.csv"

def ensure_module_folder() -> str:
    folder = os.path.join(USER_OBSERVATION_FOLDER, MODULE_TYPE)
    os.makedirs(folder, exist_ok=True)
    return folder

def observation_input_form(form_key: str = "lp_observation_form") -> None:
    clear_key = f"{form_key}_clear"
    if st.button("🧹 Clear Note", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("📈 Portfolio Status Note")
        st.caption("Log current concerns or views on your open portfolio exposures.")
        observation_text = st.text_area("Portfolio Note", height=120, key=f"{form_key}_text")

        optional_tags = st.multiselect("Optional Tags:", [
            "Overexposed", "Hedged", "Earnings Risk", "Diversified", "High Conviction",
            "Macro Headwinds", "Sector Imbalance", "Low Liquidity"
        ], key=f"{form_key}_tags")

        submitted = st.form_submit_button("Save Note")
        if submitted and observation_text.strip():
            save_observation(observation_text.strip(), optional_tags)
            st.success("✅ Portfolio note saved.")

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
    file_path = os.path.join(ensure_module_folder(), FILENAME)
    st.subheader("📘 Live Portfolio Notes")

    if not os.path.exists(file_path):
        st.info("No notes recorded yet.")
        return

    if st.button("🔄 Refresh Notes"):
        st.rerun()

    df = pd.read_csv(file_path).sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.markdown("✏️ Edit or delete rows inline, then click **Save Updates** to confirm.")
    edited_df = st.data_editor(df, width='stretch', height=450, key="lp_editor")

    if st.button("💾 Save Updates"):
        edited_df.to_csv(file_path, index=False)
        st.success("✅ Notes updated.")
