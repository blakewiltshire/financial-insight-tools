# -------------------------------------------------------------------------------------------------
# 🧠 Observation & AI Export — Tab 2: Observation Browser Panel (Final)
# -------------------------------------------------------------------------------------------------

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List
import uuid
import hashlib

from insight_loader import load_all_observations

# -------------------------------------------------------------------------------------------------
# UI — Filter Panel (Platinum-Grade, Finalised Labelling)
# -------------------------------------------------------------------------------------------------

def render_observation_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("🔍 Filter Observations")

    # Fill and strip all required labels
    df["main_module"] = df["main_module"].fillna("").str.strip()
    df["module"] = df["module"].fillna("").str.strip()
    df["country"] = df["country"].fillna("").str.strip()
    df["assets_selected"] = df["assets_selected"].fillna("").str.strip()
    df["macro_indicators"] = df["macro_indicators"].fillna("").str.strip()
    df["relevance_tag"] = df["relevance_tag"].fillna("").str.strip()
    df["sentiment_tag"] = df["sentiment_tag"].fillna("").str.strip()
    df["observation_type"] = df["observation_type"].fillna("").str.strip()

    col1, col2, col3 = st.columns(3)
    with col1:
        modules = sorted(df["main_module"].dropna().unique())
        selected_main = st.multiselect("🧠 Main Module", modules, key="filter_main_module")
        if selected_main:
            df = df[df["main_module"].isin(selected_main)]

    with col2:
        submodules = sorted(df["module"].dropna().unique())
        selected_sub = st.multiselect("🔧 Submodule", submodules, key="filter_submodule")
        if selected_sub:
            df = df[df["module"].isin(selected_sub)]

    with col3:
        countries = sorted(df["country"].dropna().unique())
        selected_country = st.multiselect("🌍 Country", countries, key="filter_country")
        if selected_country:
            df = df[df["country"].isin(selected_country)]

    col4, col5, col6 = st.columns(3)
    with col4:
        macro_indicators = sorted(df["macro_indicators"].dropna().unique())
        selected_indicators = st.multiselect("🧠 Macro Indicators", macro_indicators, key="filter_macro_indicators")
        if selected_indicators:
            df = df[df["macro_indicators"].isin(selected_indicators)]

    with col5:
        assets = sorted(df["assets_selected"].dropna().unique())
        selected_assets = st.multiselect("📈 Assets Selected", assets, key="filter_assets")
        if selected_assets:
            df = df[df["assets_selected"].isin(selected_assets)]

    with col6:
        relevance = sorted(df['relevance_tag'].dropna().unique())
        selected_relevance = st.multiselect("🎯 Relevance", relevance, key="filter_relevance")
        if selected_relevance:
            df = df[df['relevance_tag'].isin(selected_relevance)]

    col7, col8 = st.columns(2)
    with col7:
        sentiment = sorted(df['sentiment_tag'].dropna().unique())
        selected_sentiment = st.multiselect("⚖️ Sentiment", sentiment, key="filter_sentiment")
        if selected_sentiment:
            df = df[df['sentiment_tag'].isin(selected_sentiment)]

    with col8:
        timing = sorted(df['observation_type'].dropna().unique())
        selected_timing = st.multiselect("⏱ Timing", timing, key="filter_timing")
        if selected_timing:
            df = df[df['observation_type'].isin(selected_timing)]

    return df

def render_observation_browser_panel():
    st.title("📋 Observation Browser")
    st.caption("Review your recorded insights and user notes across modules and time.")

    # ------------------------
    # ✅ Session State Bootstrap
    # ------------------------
    if "bundle_observations" not in st.session_state:
        st.session_state["bundle_observations"] = []

    # ------------------------
    # 🔁 Reload Trigger
    # ------------------------
    if st.button("🔄 Reload Observation List", key="reload_observation_list_browser"):
        st.rerun()

    # ------------------------
    # 📥 Load Observations
    # ------------------------
    df = load_all_observations()
    if df.empty:
        st.warning("No user observations found.")
        return

    df = render_observation_filters(df)
    df = df.sort_values(by="timestamp", ascending=False)

    # ------------------------
    # 📋 Render Each Observation Card
    # ------------------------
    for i, row in enumerate(df.itertuples(), start=1):
        source_file = getattr(row, "source_file", "")
        timestamp = getattr(row, "timestamp", "")
        uuid_key = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{source_file}_{timestamp}"))
        already_added = source_file in st.session_state["bundle_observations"]

        with st.container(border=True):
            ts_display = pd.to_datetime(timestamp, errors="coerce").strftime("%Y-%m-%d %H:%M") if pd.notnull(timestamp) else "Unknown"

            st.markdown(f"**📅 Timestamp:** {ts_display}")
            st.markdown(f"**🧠 Module:** {row.main_module}  |  🔧 **Submodule:** {row.module}")
            if row.country:
                st.markdown(f"**🌍 Country:** {row.country}")
            if row.assets_selected:
                st.markdown(f"**📈 Asset(s):** {row.assets_selected}")
            if row.macro_indicators:
                st.markdown(f"**📊 Macro Indicators:** {row.macro_indicators}")

            meta_line = []
            if row.relevance_tag:
                meta_line.append(f"🎯 **Relevance**: {row.relevance_tag}")
            if row.sentiment_tag:
                meta_line.append(f"⚖️ **Sentiment**: {row.sentiment_tag}")
            if row.observation_type:
                meta_line.append(f"⏱ **Timing**: {row.observation_type}")
            if row.tags:
                meta_line.append(f"🏷 **Tags**: {row.tags}")
            if meta_line:
                st.markdown(" | ".join(meta_line))

            with st.expander("📝 Observation Detail", expanded=False):
                st.markdown(row.observation_text, unsafe_allow_html=True)

            col1, _ = st.columns([6, 1])
            with col1:
                add_key = f"add_obs_{uuid_key}"
                if not already_added:
                    if st.button("📦 Add to Bundle", key=add_key):
                        st.session_state["bundle_observations"].append(source_file)
                        st.rerun()
                else:
                    st.markdown("✅ **Already Added to Bundle**")

    # ------------------------
    # 📦 Current Bundle Contents
    # ------------------------
    st.markdown("---")
    st.subheader("📦 Current Bundle Contents")

    if st.session_state["bundle_observations"]:
        updated_bundle = []
        for i, obs_path in enumerate(st.session_state["bundle_observations"]):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**Observation Source:** `{obs_path}`")

            with col2:
                remove_key = f"remove_obs_{str(uuid.uuid5(uuid.NAMESPACE_DNS, obs_path))}"
                if st.button("❌ Remove", key=remove_key):
                    continue  # skip adding to updated bundle
            updated_bundle.append(obs_path)

        if updated_bundle != st.session_state["bundle_observations"]:
            st.session_state["bundle_observations"] = updated_bundle
            st.rerun()
    else:
        st.info("No observations currently in bundle.")
