# -------------------------------------------------------------------------------------------------
# Observation & AI Export — Observations Panel
# -------------------------------------------------------------------------------------------------

import uuid
import pandas as pd
import streamlit as st

from insight_loader import load_all_observations


# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def is_present(value) -> bool:
    """
    Return True only for values that should be displayed in the UI.
    Suppresses None, NaN, empty strings, and literal 'nan' values.
    """
    if value is None:
        return False

    try:
        if pd.isna(value):
            return False
    except Exception:
        pass

    text = str(value).strip()
    if not text:
        return False

    return text.lower() not in {"nan", "none", "null"}


def clean_value(value) -> str:
    """
    Clean a metadata value for display.
    """
    if not is_present(value):
        return ""

    text = str(value).strip()
    text = text.replace("_", " ")
    text = " ".join(text.split())

    return text


def clean_label(value) -> str:
    """
    Human-friendly label formatting with common acronym preservation.
    """
    text = clean_value(value)
    if not text:
        return ""

    text = text.title()

    acronym_map = {
        "Ai": "AI",
        "Dss": "DSS",
        "Ipo": "IPO",
        "Ipos": "IPOs",
        "Aud": "AUD",
        "Gbp": "GBP",
        "Jpy": "JPY",
        "Usd": "USD",
        "Ust": "UST",
        "S&p": "S&P",
        "Vix": "VIX",
    }

    for old, new in acronym_map.items():
        text = text.replace(old, new)

    text = text.replace("Highprofile IPOs", "High-Profile IPOs")
    text = text.replace("High Profile IPOs", "High-Profile IPOs")

    return text


def format_timestamp(value) -> str:
    """
    Display timestamp consistently.
    """
    if not is_present(value):
        return "Unknown"

    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return "Unknown"

    return parsed.strftime("%Y-%m-%d %H:%M")


def format_tags(value) -> str:
    """
    Normalise comma-separated tags for display.
    """
    if not is_present(value):
        return ""

    tags = [
        clean_label(tag)
        for tag in str(value).split(",")
        if is_present(tag)
    ]

    return ", ".join(tags)


def display_module_name(row) -> str:
    """
    Prefer the specific submodule as the primary observation label.
    """
    submodule = clean_label(getattr(row, "module", ""))
    main_module = clean_label(getattr(row, "main_module", ""))

    if submodule:
        return submodule

    if main_module:
        return main_module

    return "Observation"


def display_parent_module(row) -> str:
    """
    Show parent module only when useful.
    """
    submodule = clean_label(getattr(row, "module", ""))
    main_module = clean_label(getattr(row, "main_module", ""))

    if main_module and submodule and main_module != submodule:
        return main_module

    return ""


def build_observation_source_label(obs_path: str) -> str:
    """
    Build a cleaner label for bundled observation source paths.
    """
    if not is_present(obs_path):
        return "Observation"

    filename = str(obs_path).split("/")[-1]
    filename = filename.replace("__user_observations.csv", "")
    parts = filename.split("__")

    if len(parts) >= 2:
        scope = clean_label(parts[0])
        module = clean_label(parts[1])

        if scope.lower() in {"default", "global"}:
            return module or "Observation"

        if scope and module:
            return f"{scope} — {module}"

        return module or scope or "Observation"

    return clean_label(filename.replace(".csv", "")) or "Observation"


def normalise_filter_column(df: pd.DataFrame, column: str) -> None:
    """
    Prepare a string column for filtering without displaying NaN values.
    """
    if column not in df.columns:
        df[column] = ""

    df[column] = df[column].apply(lambda value: clean_value(value))


# -------------------------------------------------------------------------------------------------
# UI — Filter Panel
# -------------------------------------------------------------------------------------------------
def render_observation_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Filter Observations")

    for column in [
        "main_module",
        "module",
        "country",
        "assets_selected",
        "macro_indicators",
        "relevance_tag",
        "sentiment_tag",
        "observation_type",
    ]:
        normalise_filter_column(df, column)

    col1, col2, col3 = st.columns(3)

    with col1:
        modules = sorted([m for m in df["main_module"].unique() if is_present(m)])
        selected_main = st.multiselect("Main Module", modules, key="filter_main_module")
        if selected_main:
            df = df[df["main_module"].isin(selected_main)]

    with col2:
        submodules = sorted([m for m in df["module"].unique() if is_present(m)])
        selected_sub = st.multiselect("Submodule", submodules, key="filter_submodule")
        if selected_sub:
            df = df[df["module"].isin(selected_sub)]

    with col3:
        countries = sorted([c for c in df["country"].unique() if is_present(c)])
        selected_country = st.multiselect("Country", countries, key="filter_country")
        if selected_country:
            df = df[df["country"].isin(selected_country)]

    col4, col5, col6 = st.columns(3)

    with col4:
        macro_indicators = sorted([
            indicator for indicator in df["macro_indicators"].unique()
            if is_present(indicator)
        ])
        selected_indicators = st.multiselect(
            "Macro Indicators",
            macro_indicators,
            key="filter_macro_indicators",
        )
        if selected_indicators:
            df = df[df["macro_indicators"].isin(selected_indicators)]

    with col5:
        assets = sorted([asset for asset in df["assets_selected"].unique() if is_present(asset)])
        selected_assets = st.multiselect("Assets", assets, key="filter_assets")
        if selected_assets:
            df = df[df["assets_selected"].isin(selected_assets)]

    with col6:
        relevance = sorted([
            item for item in df["relevance_tag"].unique()
            if is_present(item)
        ])
        selected_relevance = st.multiselect("Relevance", relevance, key="filter_relevance")
        if selected_relevance:
            df = df[df["relevance_tag"].isin(selected_relevance)]

    col7, col8 = st.columns(2)

    with col7:
        sentiment = sorted([
            item for item in df["sentiment_tag"].unique()
            if is_present(item)
        ])
        selected_sentiment = st.multiselect("Sentiment", sentiment, key="filter_sentiment")
        if selected_sentiment:
            df = df[df["sentiment_tag"].isin(selected_sentiment)]

    with col8:
        timing = sorted([
            item for item in df["observation_type"].unique()
            if is_present(item)
        ])
        selected_timing = st.multiselect("Timing", timing, key="filter_timing")
        if selected_timing:
            df = df[df["observation_type"].isin(selected_timing)]

    return df


# -------------------------------------------------------------------------------------------------
# Main Renderer
# -------------------------------------------------------------------------------------------------
def render_observation_browser_panel():
    st.header("Observations")
    st.caption("Review recorded observations, context notes, and investigation commentary.")

    if "bundle_observations" not in st.session_state:
        st.session_state["bundle_observations"] = []

    if st.button("Reload Observation List", key="reload_observation_list_browser"):
        st.rerun()

    df = load_all_observations()

    if df.empty:
        st.warning("No user observations found.")
        return

    df = render_observation_filters(df)

    if "timestamp" in df.columns:
        df["_parsed_timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values(by="_parsed_timestamp", ascending=False).drop(
            columns="_parsed_timestamp"
        )

    for row in df.itertuples(index=False):
        source_file = getattr(row, "source_file", "")
        timestamp = getattr(row, "timestamp", "")
        uuid_key = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{source_file}_{timestamp}"))
        already_added = source_file in st.session_state["bundle_observations"]

        with st.container(border=True):
            st.markdown(f"### {display_module_name(row)}")

            parent_module = display_parent_module(row)
            if parent_module:
                st.markdown(f"**Parent Module:** {parent_module}")

            st.markdown(f"**Timestamp:** {format_timestamp(timestamp)}")

            country = clean_label(getattr(row, "country", ""))
            if country:
                st.markdown(f"**Country:** {country}")

            assets = clean_label(getattr(row, "assets_selected", ""))
            if assets:
                st.markdown(f"**Asset:** {assets}")

            macro_indicators = clean_label(getattr(row, "macro_indicators", ""))
            if macro_indicators:
                st.markdown(f"**Macro Indicators:** {macro_indicators}")

            meta_line = []

            relevance = clean_label(getattr(row, "relevance_tag", ""))
            if relevance:
                meta_line.append(f"**Relevance:** {relevance}")

            sentiment = clean_label(getattr(row, "sentiment_tag", ""))
            if sentiment:
                meta_line.append(f"**Sentiment:** {sentiment}")

            timing = clean_label(getattr(row, "observation_type", ""))
            if timing:
                meta_line.append(f"**Timing:** {timing}")

            tags = format_tags(getattr(row, "tags", ""))
            if tags:
                meta_line.append(f"**Tags:** {tags}")

            if meta_line:
                st.markdown(" | ".join(meta_line))

            observation_text = clean_value(getattr(row, "observation_text", ""))
            if observation_text:
                with st.expander("Observation Detail", expanded=False):
                    st.markdown(observation_text, unsafe_allow_html=True)

            col1, _ = st.columns([6, 1])
            with col1:
                add_key = f"add_obs_{uuid_key}"

                if not already_added:
                    if st.button("Add to Bundle", key=add_key):
                        st.session_state["bundle_observations"].append(source_file)
                        st.rerun()
                else:
                    st.markdown("**Already Added to Bundle**")

    # -------------------------------------------------------------------------------------------------
    # Current Bundle Contents
    # -------------------------------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("Current Bundle Contents")

    if st.session_state["bundle_observations"]:
        updated_bundle = []

        for obs_path in st.session_state["bundle_observations"]:
            col1, col2 = st.columns([6, 1])

            with col1:
                st.markdown(f"**{build_observation_source_label(obs_path)}**")
                st.markdown(f"`{obs_path}`")

            with col2:
                remove_key = f"remove_obs_{str(uuid.uuid5(uuid.NAMESPACE_DNS, obs_path))}"
                if st.button("❌ Remove", key=remove_key):
                    continue

            updated_bundle.append(obs_path)

        if updated_bundle != st.session_state["bundle_observations"]:
            st.session_state["bundle_observations"] = updated_bundle
            st.rerun()
    else:
        st.info("No observations currently in bundle.")
