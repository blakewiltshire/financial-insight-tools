# -------------------------------------------------------------------------------------------------
# Load / Restore Panel — Insight Bundles, AI Responses, and Research Notes
# -------------------------------------------------------------------------------------------------

import os
import sys
import json
import re
from pathlib import Path

import streamlit as st

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from core.helpers import get_named_paths  # pylint: disable=import-error

PATHS = get_named_paths(__file__)

EXPORT_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "exports"
RETURN_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "returns"
RESEARCH_NOTES_FOLDER = Path(__file__).parent / "storage" / "research_notes"

EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)
RETURN_FOLDER.mkdir(parents=True, exist_ok=True)
RESEARCH_NOTES_FOLDER.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------------------------------------
# Shared Helpers
# -------------------------------------------------------------------------------------------------
def _safe_filename(value: str, suffix: str = ".md") -> str:
    """
    Converts a user-facing note title into a safe markdown filename.
    """
    if not value:
        return f"untitled{suffix}"

    name = value.strip().lower()
    name = name.replace("&", "and")
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")

    if not name:
        name = "untitled"

    if not name.endswith(suffix):
        name = f"{name}{suffix}"

    return name


def _display_name_from_file(path: Path) -> str:
    """
    Converts a stored filename into a readable display label.
    """
    text = path.stem.replace("_", " ").title()

    replacements = {
        "Ai": "AI",
        "Usd": "USD",
        "Gbp": "GBP",
        "Aud": "AUD",
        "Jpy": "JPY",
        "Ust": "UST",
        "Vix": "VIX",
        "Ipo": "IPO",
        "Ipos": "IPOs",
        "S And P": "S&P",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def _read_text_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_text_file(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# -------------------------------------------------------------------------------------------------
# Tab 1 — Insight Bundles
# -------------------------------------------------------------------------------------------------
def _render_insight_bundles_tab():
    st.subheader("Insight Bundles")
    st.caption("Review exported investigation bundles created from selected snapshots and observations.")

    bundle_files = sorted(EXPORT_FOLDER.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

    selected = st.selectbox(
        "Select JSON Bundle",
        ["None"] + [f.name for f in bundle_files],
        key="load_restore_bundle_select",
    )

    if selected == "None":
        st.info("No bundle selected.")
        return

    filepath = EXPORT_FOLDER / selected
    st.markdown(f"**File:** `{filepath.name}`")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        st.error(f"Failed to load bundle: {exc}")
        return

    st.json(data)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            "Download JSON",
            data=json.dumps(data, indent=2, ensure_ascii=False),
            file_name=filepath.name,
            mime="application/json",
            width="stretch",
        )

    with col2:
        if st.button("🗑️ Delete Bundle", key=f"delete_bundle_{filepath.name}"):
            filepath.unlink()
            st.success(f"Deleted `{filepath.name}`.")
            st.rerun()


# -------------------------------------------------------------------------------------------------
# Tab 2 — AI Responses
# -------------------------------------------------------------------------------------------------
def _render_ai_responses_tab():
    st.subheader("AI Responses")
    st.caption("Upload, preview, download, or delete saved AI response files.")

    uploaded_file = st.file_uploader(
        "Upload AI Response (.md)",
        type=["md"],
        key="ai_response_upload",
    )

    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")

        st.markdown("#### Preview")
        st.markdown(uploaded_text)

        if st.button("Save to AI Responses", key="save_ai_response"):
            save_path = RETURN_FOLDER / uploaded_file.name
            _write_text_file(save_path, uploaded_text)
            st.success(f"Saved to `{save_path.name}`.")
            st.rerun()

    st.divider()

    st.markdown("### Saved AI Responses")

    md_files = sorted(RETURN_FOLDER.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)

    selected_md = st.selectbox(
        "Select Markdown File",
        ["None"] + [f.name for f in md_files],
        key="ai_response_select",
    )

    if selected_md == "None":
        st.info("No AI response selected.")
        return

    filepath = RETURN_FOLDER / selected_md
    md_content = _read_text_file(filepath)

    st.markdown(f"**File:** `{filepath.name}`")

    with st.expander("Preview AI Response", expanded=True):
        st.markdown(md_content)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.download_button(
            "Download Markdown",
            data=md_content,
            file_name=filepath.name,
            mime="text/markdown",
            width="stretch",
        )

    with col2:
        if st.button("🗑️ Delete AI Response", key=f"delete_ai_response_{filepath.name}"):
            filepath.unlink()
            st.success(f"Deleted `{filepath.name}`.")
            st.rerun()


# -------------------------------------------------------------------------------------------------
# Tab 3 — Research Notes
# -------------------------------------------------------------------------------------------------
def _render_research_notes_tab():
    st.subheader("Research Notes")
    st.caption(
        "Preserve longer-term context, questions, and observations that may span multiple investigations. "
        "Research Notes are stored as simple Markdown files and can be copied into future AI bundles or prompts."
    )

    st.markdown("### Create or Update Research Note")

    default_template = """# Research Note

## Things to Remember

-

## Open Questions

-

## Context to Revisit

-
"""

    # Initialise editor state before widgets are instantiated.
    if "research_note_title" not in st.session_state:
        st.session_state["research_note_title"] = ""

    if "research_note_draft" not in st.session_state:
        st.session_state["research_note_draft"] = default_template

    # Handle requested state changes before widgets are instantiated.
    if st.session_state.get("research_note_clear_requested"):
        st.session_state["research_note_title"] = ""
        st.session_state["research_note_draft"] = default_template
        st.session_state["research_note_clear_requested"] = False

    note_title = st.text_input(
        "Note Title",
        placeholder="Example: Tesla, Gold, AI Infrastructure, Labour Markets",
        key="research_note_title",
    )

    note_body = st.text_area(
        "Markdown Note",
        height=300,
        key="research_note_draft",
    )

    col_save, col_clear = st.columns([1, 1])

    with col_save:
        if st.button("Save Research Note", key="save_research_note"):
            if not note_title.strip():
                st.error("Please provide a note title before saving.")
            else:
                filename = _safe_filename(note_title)
                save_path = RESEARCH_NOTES_FOLDER / filename
                _write_text_file(save_path, note_body.strip() + "\n")
                st.success(f"Saved research note to `{filename}`.")
                st.rerun()

    with col_clear:
        if st.button("Clear Draft", key="clear_research_note_draft"):
            st.session_state["research_note_clear_requested"] = True
            st.rerun()

    st.divider()

    st.markdown("### Upload Research Note")

    uploaded_note = st.file_uploader(
        "Upload Research Note (.md)",
        type=["md"],
        key="research_note_upload",
    )

    if uploaded_note is not None:
        uploaded_text = uploaded_note.read().decode("utf-8")

        st.markdown("#### Preview")
        st.markdown(uploaded_text)

        if st.button("Save Uploaded Research Note", key="save_uploaded_research_note"):
            save_path = RESEARCH_NOTES_FOLDER / uploaded_note.name
            _write_text_file(save_path, uploaded_text)
            st.success(f"Saved to `{save_path.name}`.")
            st.rerun()

    st.divider()

    st.markdown("### Saved Research Notes")

    note_files = sorted(
        RESEARCH_NOTES_FOLDER.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not note_files:
        st.info("No research notes saved yet.")
        return

    label_map = {
        f"{_display_name_from_file(path)} — {path.name}": path
        for path in note_files
    }

    selected_note = st.selectbox(
        "Select Research Note",
        ["None"] + list(label_map.keys()),
        key="research_note_select",
    )

    if selected_note == "None":
        return

    filepath = label_map[selected_note]
    note_content = _read_text_file(filepath)

    st.markdown(f"**File:** `{filepath.name}`")

    with st.expander("Preview Research Note", expanded=True):
        st.markdown(note_content)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.download_button(
            "Download Markdown",
            data=note_content,
            file_name=filepath.name,
            mime="text/markdown",
            width="stretch",
        )

    with col2:
        if st.button("Load Into Editor", key=f"load_research_note_{filepath.name}"):
            st.session_state["research_note_load_requested"] = {
                "title": _display_name_from_file(filepath),
                "content": note_content,
            }
            st.rerun()

    with col3:
        if st.button("🗑️ Delete Note", key=f"delete_research_note_{filepath.name}"):
            filepath.unlink()
            st.success(f"Deleted `{filepath.name}`.")
            st.rerun()


# -------------------------------------------------------------------------------------------------
# Load / Restore Panel
# -------------------------------------------------------------------------------------------------
def render_load_restore_panel():
    st.header("Load / Restore")
    st.caption(
        "Manage exported investigation bundles, saved AI responses, and longer-term research notes."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Insight Bundles",
            "AI Responses",
            "Research Notes",
        ]
    )

    with tab1:
        _render_insight_bundles_tab()

    with tab2:
        _render_ai_responses_tab()

    with tab3:
        _render_research_notes_tab()
