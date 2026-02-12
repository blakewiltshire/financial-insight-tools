# -------------------------------------------------------------------------------------------------
# 🧠 Observation Handler — Platinum Canonical Build (Production Locked, Filename Aligned)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
Handles all observation data storage, retrieval, journaling, and AI export preparation.

Observations are now saved per country and theme_code using:

📂 /observation_engine/storage/user_observations/{module_type}/{country}__{theme_code}__user_observations.csv
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import csv
import datetime
from typing import List
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Storage Path Definitions
# -------------------------------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
USER_OBSERVATION_FOLDER = os.path.join(STORAGE_FOLDER, "user_observations")

# -------------------------------------------------------------------------------------------------
# Ensure Module Folder Exists (on demand)
# -------------------------------------------------------------------------------------------------
def ensure_module_folder(module_type: str) -> str:
    folder = os.path.join(USER_OBSERVATION_FOLDER, module_type)
    os.makedirs(folder, exist_ok=True)
    return folder

# -------------------------------------------------------------------------------------------------
# Observation Input Form (Platinum Canonical — Full User Guidance, AI-Aligned)
# -------------------------------------------------------------------------------------------------
def observation_input_form(
    module_type: str,
    country: str,
    theme_code: str,
    theme_title: str,
    indicator: str,
    use_case: str,
    timeframe: str,
    form_key="observation_form"
) -> None:

    clear_key = f"{form_key}_clear"
    if st.button("🧹 Clear Observation Form", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_relevance"] = "None"
        st.session_state[f"{form_key}_sentiment"] = "None"
        st.session_state[f"{form_key}_obs_type"] = "Data-Matched"
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("📌 Record Your Observation")

        st.caption("✏️ **Observation Text** — Write your insight or comment linked to this use case. Highlight any pattern, contradiction, or relevant factor influencing the macro condition.")

        observation_text = st.text_area(
            "Observation",
            height=100,
            key=f"{form_key}_text"
        )

        st.caption("🎯 **Relevance Level** — How significant is this observation for the current macro context?")

        relevance_tag = st.selectbox(
            "Relevance Level", [
                "None",
                "🌱 Early Observation",
                "📊 Relevant to This Use Case",
                "🚨 Potential Macro Shift"
            ],
            key=f"{form_key}_relevance"
        )

        st.caption("⚖️ **Sentiment Bias** — Does this observation support or contradict the directional macro bias?")

        sentiment_tag = st.selectbox(
            "Sentiment Bias", [
                "None",
                "✅ Supportive",
                "⚠️ Neutral",
                "🚨 Contradictory"
            ],
            key=f"{form_key}_sentiment"
        )

        st.caption("⏱ **Observation Timing** — Indicate whether this is a live note, directly linked to a data point, or a retrospective comment.")

        observation_type = st.selectbox(
            "Observation Timing", [
                "Now",
                "Data-Matched",
                "Retrospective"
            ],
            key=f"{form_key}_obs_type"
        )

        st.caption("🏷 **Optional Tags** — Attach thematic tags to improve future AI referencing and cross-theme context mapping.")

        optional_tags = st.multiselect(
            "Optional Tags (select applicable themes):", [
                "Macroeconomy", "AI", "Automation", "Geopolitics", "Supply Chain",
                "Consumer Sentiment", "Manufacturing", "Finance", "Retail",
                "Energy", "Tech", "Rates", "Dollar", "Commodities"
            ],
            key=f"{form_key}_tags",
            help="Tags assist AI engines to cluster observations into sectors, drivers, and macro themes."
        )

        submitted = st.form_submit_button("Save Observation")
        if submitted and observation_text.strip():
            save_observation(
                module_type=module_type,
                country=country,
                theme_code=theme_code,
                theme_title=theme_title,
                indicator=indicator,
                use_case=use_case,
                observation_text=observation_text.strip(),
                relevance_tag=relevance_tag,
                sentiment_tag=sentiment_tag,
                timeframe=timeframe,
                observation_type=observation_type,
                tags=optional_tags
            )
            st.success("✅ Observation saved.")

# -------------------------------------------------------------------------------------------------
# Save Observation Entry
# -------------------------------------------------------------------------------------------------
def save_observation(
    module_type: str,
    country: str,
    theme_code: str,
    theme_title: str,
    indicator: str,
    use_case: str,
    observation_text: str,
    relevance_tag: str,
    sentiment_tag: str,
    timeframe: str,
    tags: List[str],
    observation_type: str
) -> None:

    folder = ensure_module_folder(module_type)
    filename = f"{country}__economic_exploration__{theme_code}__user_observations.csv"
    file_path = os.path.join(folder, filename)

    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "country": country,
        "theme_code": theme_code,
        "theme_title": theme_title,
        "indicator": indicator,
        "use_case": use_case,
        "observation_text": observation_text,
        "relevance_tag": relevance_tag,
        "sentiment_tag": sentiment_tag,
        "timeframe": timeframe,
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
# Observation Journal Viewer
# -------------------------------------------------------------------------------------------------
def display_observation_log(module_type: str, country: str, theme_code: str) -> None:

    folder = ensure_module_folder(module_type)
    filename = f"{country}__economic_exploration__{theme_code}__user_observations.csv"
    file_path = os.path.join(folder, filename)

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

# -------------------------------------------------------------------------------------------------
# Export Observations for AI (Structured Load for AI Bundle Integration)
# -------------------------------------------------------------------------------------------------
def export_observations_for_ai(module_type: str, country: str, theme_code: str) -> list:

    folder = ensure_module_folder(module_type)
    filename = f"{country}__economic_exploration__{theme_code}__user_observations.csv"
    file_path = os.path.join(folder, filename)

    if not os.path.exists(file_path):
        return []

    df = pd.read_csv(file_path)
    structured = []
    for _, row in df.iterrows():
        entry = {
            "timestamp": row.get("timestamp"),
            "country": row.get("country", ""),
            "theme_code": row.get("theme_code", ""),
            "theme_title": row.get("theme_title", ""),
            "indicator": row.get("indicator"),
            "use_case": row.get("use_case"),
            "user_observation": row.get("observation_text"),
            "relevance_level": row.get("relevance_tag"),
            "sentiment_bias": row.get("sentiment_tag"),
            "timeframe": row.get("timeframe"),
            "observation_type": row.get("observation_type", "Data-Matched"),
            "tags": [tag.strip() for tag in str(row.get("tags", "")).split(",") if tag.strip()]
        }
        structured.append(entry)

    return structured
