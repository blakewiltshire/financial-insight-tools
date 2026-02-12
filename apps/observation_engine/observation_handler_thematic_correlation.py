# -------------------------------------------------------------------------------------------------
# 🧠 Observation Handler — Thematic Correlation Explorer (Platinum Canonical Build)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Handles observation storage, retrieval, and log editing for Thematic Correlation Explorer.

Observations are saved centrally to:
📂 /observation_engine/storage/user_observations/thematic_correlation/global__thematic_correlation__user_observations.csv
"""

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
MODULE_TYPE = "thematic_correlation"
FIXED_FILENAME = "global__thematic_correlation__user_observations.csv"

# -------------------------------------------------------------------------------------------------
# Ensure Folder Exists
# -------------------------------------------------------------------------------------------------
def ensure_module_folder() -> str:
    folder = os.path.join(USER_OBSERVATION_FOLDER, MODULE_TYPE)
    os.makedirs(folder, exist_ok=True)
    return folder

# -------------------------------------------------------------------------------------------------
# Observation Input Form
# -------------------------------------------------------------------------------------------------
def observation_input_form(
    theme_title: str,
    themes_selected: List[str],
    indicators_selected: List[str],
    form_key: str = "observation_form"
) -> None:
    """
    Renders the observation input form and saves entries with full metadata context.
    """
    clear_key = f"{form_key}_clear"
    if st.button("🧹 Clear Observation Form", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_relevance"] = "None"
        st.session_state[f"{form_key}_sentiment"] = "None"
        st.session_state[f"{form_key}_obs_type"] = "Data-Matched"
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("📌 Record Your Observation")
        st.caption(f"✏️ **Observation Context** — {theme_title}")

        st.markdown(f"**🧩 Themes Selected:** {', '.join(themes_selected)}")
        st.markdown(f"**📊 Indicators Selected:** {', '.join(indicators_selected)}")

        st.caption("✏️ **Observation Text** — Write your insight or comment linked to "
        "this module. Highlight any pattern, contradiction, or relevant factor "
        "influencing the condition.")

        observation_text = st.text_area("Observation", height=100, key=f"{form_key}_text")

        st.caption("🎯 **Relevance Level** — How significant is this observation for "
        "the current context?")

        relevance_tag = st.selectbox("Relevance Level", [
            "None", "🌱 Early Observation", "📊 Relevant to This Use Case", "🚨 Potential Macro Shift"
        ], key=f"{form_key}_relevance")

        st.caption("⚖️ **Sentiment Bias** — Does this observation support or contradict the directional macro bias?")

        sentiment_tag = st.selectbox("Sentiment Bias", [
            "None", "✅ Supportive", "⚠️ Neutral", "🚨 Contradictory"
        ], key=f"{form_key}_sentiment")

        st.caption("⏱ **Observation Timing** — Indicate whether this is a live note, directly linked to a data point, or a retrospective comment.")

        observation_type = st.selectbox("Observation Timing", [
            "Now", "Data-Matched", "Retrospective"
        ], key=f"{form_key}_obs_type")

        st.caption("🏷 **Optional Tags** — Attach thematic tags to improve future AI referencing and cross-theme context mapping.")

        optional_tags = st.multiselect("Optional Tags:", [
            "Macroeconomy", "AI", "Automation", "Geopolitics", "Supply Chain",
            "Consumer Sentiment", "Manufacturing", "Finance", "Retail",
            "Energy", "Tech", "Rates", "Dollar", "Commodities"
        ], key=f"{form_key}_tags")
        help="Tags assist AI engines to cluster observations into sectors, drivers, and macro themes."

        submitted = st.form_submit_button("Save Observation")
        if submitted and observation_text.strip():
            save_observation(
                theme_title=theme_title,
                themes_selected=themes_selected,
                indicators_selected=indicators_selected,
                observation_text=observation_text.strip(),
                relevance_tag=relevance_tag,
                sentiment_tag=sentiment_tag,
                observation_type=observation_type,
                tags=optional_tags
            )
            st.success("✅ Observation saved.")

# -------------------------------------------------------------------------------------------------
# Save Observation Entry
# -------------------------------------------------------------------------------------------------
def save_observation(
    theme_title: str,
    themes_selected: List[str],
    indicators_selected: List[str],
    observation_text: str,
    relevance_tag: str,
    sentiment_tag: str,
    observation_type: str,
    tags: List[str]
) -> None:
    """
    Saves the observation as a new row in the module log file.
    Output fields follow the canonical DSS format.
    """
    folder = ensure_module_folder()
    file_path = os.path.join(folder, FIXED_FILENAME)

    entry = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "country": "Global",  # Fixed for thematic correlation
        "theme_code": ", ".join(themes_selected),
        "theme_title": theme_title,
        "indicator": ", ".join(indicators_selected),
        "observation_text": observation_text,
        "relevance_tag": relevance_tag,
        "sentiment_tag": sentiment_tag,
        "timeframe": "",  # Not used in this module
        "observation_type": observation_type,
        "tags": ", ".join(tags) if tags else ""
    }

    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

# -------------------------------------------------------------------------------------------------
# Display Observation Journal Log
# -------------------------------------------------------------------------------------------------
def display_observation_log() -> None:
    """
    Displays saved observations with inline edit and delete features.
    """
    folder = ensure_module_folder()
    file_path = os.path.join(folder, FIXED_FILENAME)

    st.subheader("🗂️ Observation Journal")

    if not os.path.exists(file_path):
        st.info("No observations recorded yet.")
        return

    if st.button("🔄 Refresh Observation Log"):
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
        height=500,
        num_rows="dynamic",
        key="observation_editor"
    )

    if st.button("💾 Save Journal Updates"):
        edited_df.to_csv(file_path, index=False)
        st.success("✅ Journal updated successfully.")
