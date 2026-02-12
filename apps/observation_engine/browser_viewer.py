# -------------------------------------------------------------------------------------------------
# 🔍 Insight Browser Viewer — Embedded Panel for Observations and Snapshots
# -------------------------------------------------------------------------------------------------

import streamlit as st
from typing import Optional
from apps.observation_engine.insight_loader import load_all_observations, load_all_snapshots


def render_insight_browser(
    title: str = "📘 Insight Browser",
    filter_module: Optional[str] = None,
    filter_context: Optional[str] = None,
    show_snapshots: bool = True,
    show_observations: bool = True
) -> None:
    """
    Renders the Insight Browser panel, showing user observations and/or AI snapshots.

    Args:
        title (str): The title of the panel.
        filter_module (str): Filter observations by module_type (e.g., 'economic_exploration').
        filter_context (str): Filter observations by context (e.g., 'united_states__100_economic_growth_stability').
        show_snapshots (bool): Whether to include AI export snapshot previews.
        show_observations (bool): Whether to include user observation logs.
    """
    st.markdown(f"### {title}")
    st.caption("Browse previously saved user observations and AI export snapshots.")

    if show_observations:
        _render_observations(filter_module, filter_context)

    if show_snapshots:
        _render_ai_snapshots(filter_context)


# -------------------------------------------------------------------------------------------------
# 📋 User Observations Display
# -------------------------------------------------------------------------------------------------

def _render_observations(filter_module: Optional[str], filter_context: Optional[str]) -> None:
    st.subheader("📝 User Observations")
    df = load_all_observations()
    if df.empty:
        st.info("No user observations found.")
        return

    if filter_module:
        df = df[df["module_type"] == filter_module]
    if filter_context:
        df = df[df["context"] == filter_context]

    if df.empty:
        st.warning("No matching observations for this module or context.")
        return

    df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)
    st.dataframe(df[["timestamp", "observation_text", "tags", "module_type", "context"]], use_container_width=True)


# -------------------------------------------------------------------------------------------------
# 📦 AI Snapshots Display
# -------------------------------------------------------------------------------------------------

# 📦 AI Snapshots Display
def _render_ai_snapshots(filter_context: Optional[str]) -> None:
    st.subheader("🧠 AI Snapshot Exports")
    bundles = load_all_snapshots()
    if not bundles:
        st.info("No AI export snapshots found.")
        return

    if filter_context:
        bundles = [b for b in bundles if filter_context in b["source_file"]]

    if not bundles:
        st.warning("No matching snapshots for this context.")
        return

    # ✅ FIXED SORTING
    for bundle in sorted(bundles, key=lambda b: str(b.get("theme", "")) + str(b.get("use_case", ""))):
        with st.expander(f"📦 {bundle.get('theme', '?')} — {bundle.get('use_case', '?')}"):
            st.markdown(f"**Macro Score**: `{bundle.get('macro_score', '')}`  \n"
                        f"**Label**: `{bundle.get('score_label', '')}`  \n"
                        f"**Timeframe**: `{bundle.get('timeframe', '')}`  \n"
                        f"**Source**: `{bundle.get('source_file', '')}`")

            # Layout-safe alternative to nested expanders
            st.markdown("**📖 Score Explanation**")
            st.markdown(bundle.get("score_explanation", "No explanation provided."))

            st.markdown("**🧬 Full Snapshot (JSON)**")
            st.json(bundle.get("raw", {}), expanded=False)
