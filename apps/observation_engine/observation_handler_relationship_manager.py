# -------------------------------------------------------------------------------------------------
# Observation Handler — Relationship Manager
# -------------------------------------------------------------------------------------------------

"""
Observation logging for the Relationship Manager module.

This handler captures contextual notes that sit alongside relationship-area and candidate-asset
review. It does not rank, score, recommend, or analyse securities.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os
import csv
import datetime
from typing import List

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Storage Paths
# -------------------------------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FOLDER = os.path.join(CURRENT_DIR, "storage")
USER_OBSERVATION_FOLDER = os.path.join(STORAGE_FOLDER, "user_observations")
MODULE_TYPE = "reference_data"
FILENAME = "default__relationship_manager__user_observations.csv"


def ensure_module_folder() -> str:
    """
    Ensures the folder path for this module's observation storage exists.

    Returns:
        str: Full folder path.
    """
    folder = os.path.join(USER_OBSERVATION_FOLDER, MODULE_TYPE)
    os.makedirs(folder, exist_ok=True)
    return folder


def observation_input_form(form_key: str = "relationship_manager_observation_form") -> None:
    """
    Renders the user observation input form for Relationship Manager.

    Notes may be contextualised with optional tags and saved for later review,
    AI export, or cross-module observation workflows.
    """
    clear_key = f"{form_key}_clear"
    if st.button("Clear Form", key=clear_key):
        st.session_state[f"{form_key}_text"] = ""
        st.session_state[f"{form_key}_tags"] = []

    with st.form(form_key):
        st.subheader("Relationship Manager — Observation Note")
        st.caption(
            "Log context, assumptions, questions, or uncertainty that emerged while mapping "
            "relationships and candidate assets."
        )

        observation_text = st.text_area(
            "Observation",
            height=120,
            key=f"{form_key}_text",
            placeholder=(
                "Example: Alphabet's AI talent departures may be less about one share-price "
                "move and more about competitive positioning, human capital, and future AI capability."
            ),
        )

        optional_tags = st.multiselect(
            "Optional Tags", [
            "AI Infrastructure",
            "AI Disruption",
            "Brain Drain",
            "Talent Migration",
            "Human Capital",
            "Competitive Positioning",
            "Narrative Shift",
            "Market Expectations",
            "Candidate Asset Review",
            "Cross-Sector Relationship",
            "Intra-Sector Relationship",
            "Supply Chain Exposure",
            "Business Capability Mapping",
            "Sector Mapping",
            "Data Availability Gap",
            "Monitoring",
            "User Assumption",
            "Uncertainty Preserved",
            "AI Review"
        ], key=f"{form_key}_tags",)

        submitted = st.form_submit_button("Save Observation")
        if submitted and observation_text.strip():
            save_observation(observation_text.strip(), optional_tags)
            st.success("Observation saved successfully.")


def save_observation(observation_text: str, tags: List[str]) -> None:
    """
    Saves the user observation entry to the CSV log.

    Args:
        observation_text (str): Observation note text.
        tags (List[str]): Optional contextual tags.
    """
    file_path = os.path.join(ensure_module_folder(), FILENAME)
    entry = {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "observation_text": observation_text,
        "tags": ", ".join(tags) if tags else "",
    }

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


def display_observation_log() -> None:
    """
    Displays the editable observation log with option to refresh or save inline edits.
    """
    file_path = os.path.join(ensure_module_folder(), FILENAME)
    st.subheader("Saved Observations — Relationship Manager")

    if not os.path.exists(file_path):
        st.info("No observations recorded yet.")
        return

    if st.button("Refresh Observations"):
        st.rerun()

    df = pd.read_csv(file_path).sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.markdown("Edit or delete entries inline, then click **Save Updates** to apply changes.")
    edited_df = st.data_editor(
        df,
        width="stretch",
        height=450,
        key="relationship_manager_observation_editor",
    )

    if st.button("Save Updates"):
        edited_df.to_csv(file_path, index=False)
        st.success("Observations updated.")
