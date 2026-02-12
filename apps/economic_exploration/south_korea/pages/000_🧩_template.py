# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name
# pylint: disable=undefined-variable, redefined-outer-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 {display_name} — Thematic Indicator Module
--------------------------------------------------------

This module provides a structured decision-support interface for analysing {short_description}.

It focuses on:
{focus_bullets}

The purpose is not to forecast outcomes, but to surface structural insights and
comparative dynamics across:
- Thematic signal positioning and inflection points
- Systemic trends, volatility patterns, or sectoral breakdowns
- Policy relevance, structural adaptation, or strategic framing

Outputs are standardised and modular, enabling integration with:
- Universal and country-specific use cases
- Weighting and scoring systems
- Observation logs and AI export layers
- Visual diagnostics and trend mapping

This app is one of several thematic modules within the 🌍 Economic Exploration suite of the
Financial Insight Tools system.

Usage Notes:
- This module assumes input from pre-cleaned, structured economic data
- Country-specific files follow a standard template format (e.g., `000_template.csv`)
- All modular logic (insights, weights, visuals, use cases) can be expanded per country
or shared universally

⚠️ This module does not provide forecasts, policy advice, or trading signals.
It provides structural framing for thematic economic exploration and strategic insight.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    get_named_paths
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_4"]
APPS_PATH = PATHS["level_up_3"]
APP_PATH = PATHS["level_up_2"]
PAGES_PATH = PATHS["level_up_1"]

# Add only the required paths to sys.path
include_paths = [
    os.path.join(ROOT_PATH, "constants"),
    os.path.join(APPS_PATH, "components"),
    os.path.join(APPS_PATH, "registry"),
    os.path.join(APPS_PATH, "observation_engine"),
    os.path.join(APP_PATH, "shared"),
    os.path.join(APP_PATH, "universal_insights"),
    os.path.join(APP_PATH, "universal_indicator_map"),
    os.path.join(APP_PATH, "universal_use_cases"),
    os.path.join(APP_PATH, "universal_visual_config"),
    os.path.join(APP_PATH, "universal_scoring_weights_labels"),
    os.path.join(APP_PATH, "universal_routing")
]

for path in include_paths:
    if path not in sys.path:
        sys.path.append(path)

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------
from emoji import FLAGS
from page_icon import PAGE_ICONS
from thematic_groupings import THEMATIC_GROUPS

from economic_cleaning_shared import clean_economic_data

from ux.timeframe_selector import render_timeframe_selector
from ux.timeframe_slicer import slice_data_by_timeframe

from indicator_map.indicator_map_000 import get_indicator_maps

from use_cases.use_case_000 import get_use_cases, render_use_case_selector

from insights.insight_000 import generate_econ_insights

from routing.routing_000 import get_indicator_input

from scoring_weights_labels.scoring_weights_labels_000_template import (
    get_alignment_score_label,
    get_indicator_weight,
)

from visual_config.visual_config_000 import (
    render_all_charts_local
)

# -------------------------------------------------------------------------------------------------
# Import Observation Engine Modules
# -------------------------------------------------------------------------------------------------
from observation_handler_economic_exploration import (
    observation_input_form,
    display_observation_log,
    export_observations_for_ai,
    save_observation
)

from ai_export_builder_economic_exploration import create_theme_ai_bundle, save_ai_bundle_to_file
from macro_insight_sidebar_panel_economic_exploration import render_macro_sidebar_tools
from render_macro_interaction_tools_panel_economic_exploration import render_macro_interaction_tools_panel
from ai_export_ui_panel_economic_exploration import render_ai_export_ui_panel

# -------------------------------------------------------------------------------------------------
# 🧭 CONFIGURATION INSTRUCTIONS (MINIMUM SETUP FOR COUNTRY MODULE)
# -------------------------------------------------------------------------------------------------
# ✅ REQUIRED USER INPUT TO ACTIVATE THIS MODULE:
#
# 1. COUNTRY_NAME
#    - Used for display titles, flag rendering, and AI persona exports.
#    - Must match entry in constants/emoji.py (e.g., "South Korea").
#
# 2. COUNTRY_CODE
#    - Two-letter lowercase code (e.g., "kr").
#    - Used to locate subdirectory under /data_sources/economic_data/
#    - This is required for file path resolution.
#
# 🔒 DO NOT MODIFY THEME, TEMPLATE, TEMPLATE_1, or DEFAULT_USE_CASE unless:
#     - You are configuring a real dataset for this theme
#     - You have created or copied a valid folder structure under your country directory
#
#     Example (for USA):
#         THEME = "economic_growth_stability"
#         TEMPLATE = "100_gdp_template"
#         TEMPLATE_1 = "100_gdp_macro_composite_template"
#         DEFAULT_USE_CASE = "Real GDP"
#
#     These link the app to the correct data source, visual configuration, and use case logic.
#     Leave them as-is when bootstrapping the template —
#     update only when preparing full country coverage.
#
# ⚠️ All CSV files must be properly structured (e.g., ISO 8601 `date` columns, matching schema),
#     and located under the correct folder path defined in TEMPLATE or TEMPLATE_1.
#
# Example bootstrapping:
#     COUNTRY_NAME = "South Korea"
#     COUNTRY_CODE = "kr"

# --- 🌍 COUNTRY-SPECIFIC SETTINGS ---

COUNTRY_NAME = "South Korea"      # Display name (used for titles, flags)
COUNTRY_CODE = "000"  # Pulls CSV from /datasource/000/ — switch to e.g. 'us' after data is sourced

# 📊 THEME CONFIGURATION (align with thematic_groupings.py)

THEME = "template"  # Theme slug (used in file lookup, visuals, AI bundles)
THEME_ID = "000"                # Theme ID
STRUCTURAL_FOLDER = "000_generic"   # Primary dataset folder name under /data_sources/
COMPOSITE_FOLDER = ""                 # Optional second template folder (leave blank if unused)
DEFAULT_USE_CASE = "Signal A"   # Default focus in use case selector (must match use_case key)

# -------------------------------------------------------------------------------------------------
# 🧾 DATASET_REGISTRY — REQUIRED INPUTS FOR LOADING AND STRUCTURING DATA
# -------------------------------------------------------------------------------------------------
# This dictionary defines all datasets used in this country + theme module.
#
# • Each key becomes a variable (e.g., df_generic) available across use case logic,
#   scoring, visuals, insights, and AI exports.
#
# • Each entry must include:
#     - label: For UI display and error messaging
#     - file: CSV file name (must be located under
#       /data_sources/economic_data/{country_code}/{STRUCTURAL_FOLDER}/)
#     - folder: The subdirectory name (STRUCTURAL_FOLDER or COMPOSITE_FOLDER)
#     - cleaner: Function to pre-process raw data into usable form
#     - show_in_underlying_data: Whether to show in the raw data viewer
#     - plot: Whether to include in the charting panel
#     - create_slice: Whether to create a timeframe slice (e.g., df_generic_slice)
#
# ⚠️ All CSVs must include a `date` column in ISO format (e.g., 2023-12-31).
# ⚠️ Do NOT alter registry structure unless familiar with downstream logic dependencies
#     (e.g., insights, visuals, scoring functions).
#
# 🔁 If you add country-specific features later (e.g., composite signals, weekly/monthly layers),
#     you can register additional datasets here (e.g., df_macro_monthly_cleaned).
#     These are typically integrated once the module is fully extended.
# -------------------------------------------------------------------------------------------------

DATASET_REGISTRY = {
    "df_primary": {
        "label": "📄 Default Template",
        "file": f"{COUNTRY_CODE}_m_{THEME_ID}_structural.csv",
        "folder": STRUCTURAL_FOLDER,
        "frequency": "monthly",
        "cleaner": clean_economic_data,
        "show_in_underlying_data": True,
        "plot": True,
        "create_slice": True
    }
    # ➕ Add more datasets here if extending this module with additional signal layers
}

# --- End of User Configuration ---

# -------------------------------------------------------------------------------------------------
# 📄 FILE PATHS (Static — Driven by THEME or ROOT)
# -------------------------------------------------------------------------------------------------
# These paths load markdown and branding files required for each app instance.
#
# ABOUT_APP_MD       = Theme-specific app overview (auto-shown under "📌 What is this app about?")
# HELP_APP_MD        = Theme-specific instructions (may be used in future Help panel)
# ABOUT_SUPPORT_MD   = Universal help/support metadata (displayed system-wide)
# BRAND_LOGO_PATH    = Blake logo (displayed in sidebar/footer)
# -------------------------------------------------------------------------------------------------

ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", f"about_{THEME}.md")
HELP_APP_MD = os.path.join(ROOT_PATH, "docs", f"help_{THEME}.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# 🎨 THEMATIC VISUALS & COUNTRY FLAG MAPPING
# -------------------------------------------------------------------------------------------------
# These constants drive page icons, flag visuals, and AI module alignment.
#
# THEME_DATA = theme-level metadata used by AI and DSS logic
# PAGE_ICON  = emoji shown in the browser tab and Streamlit header
# FLAG       = emoji flag shown beside country name (must match country key in emoji.py)
# -------------------------------------------------------------------------------------------------
THEME_CODE = f"{THEME_ID}_{THEME}"
THEME_DATA = THEMATIC_GROUPS.get(THEME, {})       # Metadata for this thematic group
PAGE_ICON = PAGE_ICONS.get(THEME, '❓')            # UI tab/page icon fallback = ❓
FLAG = FLAGS.get(COUNTRY_NAME, '🏳️')               # Default fallback = white flag

# ✅ Sidebar logo
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# 🚀 Streamlit Page Configuration
# -------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title=f"{COUNTRY_NAME} - {THEME.replace('_', ' ').title()}",
    page_icon=PAGE_ICON,
    layout="wide"
)

st.title(f"{FLAG} {COUNTRY_NAME} - {PAGE_ICON} {THEME.replace('_', ' ').title()}")
st.caption("*Generic Template.*")

# -------------------------------------------------------------------------------------------------
# 📌 App Info Panel (Displays about_{THEME}.md contents)
# -------------------------------------------------------------------------------------------------

with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error(f"❌ App info file not found: docs/about_{THEME}.md")


# -------------------------------------------------------------------------------------------------
# 🔁 LOAD REGISTERED DATASETS INTO MEMORY
# -------------------------------------------------------------------------------------------------
# This section loads all datasets defined in DATASET_REGISTRY into memory.
#
# For each entry:
# - Loads the CSV from the correct country + folder path
# - Applies the cleaning function defined in the registry
# - Filters columns if specified (optional)
# - Sets the 'date' column as index
# - Registers cleaned DataFrame in globals() for app-wide access
#
# ✅ Result: All datasets are available by variable name (e.g., df_primary)
# -------------------------------------------------------------------------------------------------

loaded_datasets = {}

for varname, cfg in DATASET_REGISTRY.items():
    try:
        file_path = os.path.join(
            APPS_PATH, "data_sources", "economic_data", COUNTRY_CODE,
            cfg["folder"], cfg["file"]
        )

        # --- Load raw CSV ---
        df_raw = pd.read_csv(file_path)

        # --- Apply cleaning function ---
        df_cleaned = cfg["cleaner"](df_raw)

        # --- Optional: Restrict to defined columns ---
        columns = cfg.get("columns")
        if columns:
            required_cols = ["date"] + [col for col in columns if col != "date"]
            df_cleaned = df_cleaned[[col for col in required_cols if col in df_cleaned.columns]]

        # --- Final validation: Ensure non-empty and date-indexed ---
        if df_cleaned is not None and not df_cleaned.empty:
            df_cleaned.set_index("date", inplace=True)
            loaded_datasets[varname] = {"df": df_cleaned, "label": cfg["label"]}
            globals()[varname] = df_cleaned  # Makes variable globally available
        else:
            st.warning(
                f"⚠️ Dataset loaded but contains no usable data: **{cfg['label']}**"
            )

    except FileNotFoundError:
        st.warning(
            f"⚠️ File not found: **{cfg['label']}** — expected: `{cfg['file']}` in folder `{cfg['folder']}`"
        )
    except pd.errors.ParserError:
        st.warning(
            f"⚠️ Parsing error while loading **{cfg['label']}** — check file structure or delimiters"
        )
    except Exception as e:  # pylint: disable=broad-except
        st.warning(
            f"⚠️ Failed to load dataset: **{cfg['label']}** — {type(e).__name__}: {str(e)}"
        )

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="🔙 Back to Country Overview")
st.sidebar.divider()


# --- Timeframe Selection ---
selected_timeframe, selected_label = render_timeframe_selector()

# --- Render Use Case Sidebar ---
selected_use_case, USE_CASES = render_use_case_selector(get_use_cases)

# --- Retrieve Applicable Indicator Maps (Universal + Local) ---
# This call merges standard indicators with country-specific signal sets,
# as defined in: indicator_modules/indicator_map_<country_code>_<theme_id>.py
# Ensures modularity, avoids direct hardcoding, and enables consistent cross-country logic.
all_indicator_maps = get_indicator_maps()

# --- Resolve Indicator Map for Selected Use Case ---
indicator_map = all_indicator_maps.get(selected_use_case, {})

# --- Indicator Selection ---
selected_indicators = []
if selected_use_case in USE_CASES:
    selected_indicators = USE_CASES[selected_use_case]["Indicators"]

# --- Sidebar Expander for Customisation ---
with st.sidebar.expander("🎯 Customise Indicators"):
    selected_indicators = st.multiselect(
        "Select Evaluation Metrics",
        options=list(indicator_map.keys()),
        default=selected_indicators
    )

# -------------------------------------------------------------------------------------------------
# 🔒 Generic Slice (Always Present — Fixed Variable Name)
#
# This core slice anchors visualisation panels, AI augmentation, and thematic summaries.
# Do not rename. This is a hardcoded dependency across downstream logic.
# -------------------------------------------------------------------------------------------------
df_primary_slice = slice_data_by_timeframe(df_primary, selected_timeframe)

# -------------------------------------------------------------------------------------------------
# 🔁 Auto-Slice All Registered Datasets with Slicing Enabled
#
# Datasets with `"create_slice": True` are dynamically sliced using their registry keys.
# -------------------------------------------------------------------------------------------------

for df_var, config in DATASET_REGISTRY.items():
    if config.get("create_slice", False) and df_var != "df_primary":
        df_cleaned = globals().get(df_var)
        if df_cleaned is not None:
            slice_var = f"{df_var.replace('_cleaned', '')}_slice"
            globals()[slice_var] = slice_data_by_timeframe(df_cleaned, selected_timeframe)

# --- Routing Dictionary ---
df_dict = {
    "df_primary_slice": df_primary_slice,
    "df_full": df_primary,
    # "df_secondary_slice": df_secondary_slice,
    # "df_extended_slice": df_extended_slice
}

# --- Alignment Score (Platinum-Grade Unified Version) ---
def compute_econ_alignment(
    df_dict: dict,
    indicators: list[str],
    get_indicator_input=None
) -> tuple[pd.DataFrame, float, float]:
    """
    Computes economic alignment score and generates full insight summaries.

    ✅ Fully supports string-based signals.
    ✅ Automatically parses advanced signals with dynamic sector or value payloads.
    ✅ Fully backward compatible across universal and local modules.

    Parameters:
        df_dict (dict): Cleaned data dictionary.
        indicators (list[str]): Selected indicators.
        get_indicator_input (callable): Routing function to obtain correct dataframe.

    Returns:
        tuple:
            - pd.DataFrame: Insights table.
            - float: Score.
            - float: Maximum possible score.
    """
    summary = []
    score, max_score = 0, 0

    for name in indicators:
        func = indicator_map.get(name)
        if not func:
            continue

        df_input = get_indicator_input(name, df_dict)

        if df_input is None or not isinstance(df_input, pd.DataFrame) or df_input.empty:
            summary.append([
                name,
                "Insufficient Data",
                "⚠️ Missing or invalid data",
                "No insight generated due to missing input.",
                "Neutral"
            ])
            continue

        signal = func(df_input, period=4)
        weight = get_indicator_weight(name)

        # --- New platinum parsing block ---
        if isinstance(signal, str) and ":" in signal:
            signal_main, extra_value = signal.split(":", 1)
            signal_main = signal_main.strip()
            extra_value = extra_value.strip()
        else:
            signal_main = signal
            extra_value = None

        insight_text, bias_class = generate_econ_insights(name, signal_main, selected_timeframe, extra_value)

        if signal_main == "Insufficient Data":
            confirmation = f"⚠️ {signal_main}"
            summary.append([name, signal, confirmation, insight_text, bias_class])
            continue

        if bias_class == "Growth Supportive":
            score += weight
            confirmation = f"✅ {signal_main} aligns"
        elif bias_class == "Neutral":
            score += 0.5 * weight
            confirmation = f"ℹ️ {signal_main} suggests neutral"
        else:
            score -= weight
            confirmation = f"⚠️ {signal_main} contradicts"

        summary.append([name, signal, confirmation, insight_text, bias_class])
        max_score += weight

    return pd.DataFrame(
        summary, columns=["Indicator", "Signal", "Confirmation", "Insight", "Bias"]
    ), score, max_score


# --- Compute alignment with full modular routing ---
summary_df, score, max_score = compute_econ_alignment(
    df_dict=df_dict,
    indicators=selected_indicators,
    get_indicator_input=get_indicator_input
)

# --- Check for universal "Insufficient Data" case ---
insufficient_signals = summary_df["Signal"].str.contains("Insufficient Data").sum()
if insufficient_signals == len(selected_indicators):
    label = "⚠️ Not Enough Data for Evaluation"
    explanation = (
        "No macro signal summary could be generated for the selected timeframe. "
        "Consider expanding the time horizon or reviewing the dataset coverage below."
    )
    ratio = 0.0  # Optional: show as 0.0 / 0 for clarity
    score = 0
    max_score = 0
else:
    ratio = score / max_score if max_score > 0 else 0
    label, explanation = get_alignment_score_label(ratio, selected_use_case)

# --- Macro Conditions Summary ---
st.subheader("📊 Macro Conditions Summary")
st.caption(f"Timeframe evaluated: **{selected_label}**")

st.markdown(
    f"**Thematic Alignment Score:** `{score:.1f} / {max_score}` → **{label}**"
)
st.markdown(explanation)

# -------------------------------------------------------------------------------------------------
# Generate AI Export Bundle
# -------------------------------------------------------------------------------------------------
ai_bundle = create_theme_ai_bundle(
    country=COUNTRY_NAME.lower().replace(" ", "_"),
    theme_code=THEME_CODE,
    theme_title=THEME_DATA.get("theme_title", "N/A"),
    selected_timeframe=selected_timeframe,
    use_case_scores={selected_use_case: score},
    use_case_labels={selected_use_case: label},
    use_case_explanations={selected_use_case: explanation},
    summary_table_map={selected_use_case: summary_df}
)

# -------------------------------------------------------------------------------------------------
# 📊 Charting Visuals
#
# This section controls the visualisation output for the selected thematic module.
#
# ▪ Only datasets flagged with `"plot": True` in the DATASET_REGISTRY will be shown.
# ▪ `df_map` must include all plot-enabled datasets using the same key names as the registry.
# ▪ If adding country-specific charts or secondary datasets, extend `df_map` accordingly.
#
# ⚠️ No user changes are required unless expanding the visual dataset scope.
# -------------------------------------------------------------------------------------------------

# st.write("🔍 Columns in df_primary_slice:", df_primary_slice.columns.tolist())
# st.write("📅 df_primary_slice timeframe:", df_primary_slice["date"].min(), "to", df_primary_slice["date"].max())


# -------------------------------------------------------------------------------------------------
# 🗂️ Timeframe Tab Definition Based on Observations (Frequency-Agnostic)
# -------------------------------------------------------------------------------------------------
def define_timeframe_tabs_and_mapping(base_df: pd.DataFrame) -> tuple[dict, dict]:
    """
    Defines Streamlit timeframe tabs and maps each to a sliced DataFrame view.

    This version uses generic 'Observation' labels to remain agnostic of data frequency
    (weekly, monthly, quarterly, etc.), avoiding misleading time-based interpretations.

    Args:
        base_df (pd.DataFrame): The reference DataFrame for slicing.

    Returns:
        tuple: (tabs_dict, tab_mapping) — tab layout and corresponding data slices.
    """
    tab_3, tab_6, tab_12, tab_24, tab_60, tab_full = st.tabs([
        "📉 Last 3 Periods",
        "📊 Last 6 Periods",
        "📈 Last 12 Periods",
        "🕰️ Last 24 Periods",
        "🧭 Last 60 Periods",
        "🗂️ Full History"
    ])

    tabs_dict = {
        "3": tab_3,
        "6": tab_6,
        "12": tab_12,
        "24": tab_24,
        "60": tab_60,
        "full": tab_full
    }

    tab_mapping = {
        tab_3: base_df.tail(3),
        tab_6: base_df.tail(6),
        tab_12: base_df.tail(12),
        tab_24: base_df.tail(24),
        tab_60: base_df.tail(60),
        tab_full: base_df
    }

    return tabs_dict, tab_mapping

# --- Timeframe Tabs and Mapping (Frequency-Agnostic Style) ---
tabs_dict, tab_mapping = define_timeframe_tabs_and_mapping(df_primary)

# Context message
st.caption(f"📌 Each 'Observation' corresponds to one data entry, based on the dataset's own frequency. (Quarterly, Monthly, Weekly)")

# -------------------------------------------------------------------------------------------------
# 📁 Dataset Map for Chart Dispatcher
#
# This must match keys from the registry that have `"plot": True`.
# Maintain alignment manually across:
#   1. The dataset registry (top of file)
#   2. The cleaned DataFrame assignments
#   3. This df_map (for rendering only)
# -------------------------------------------------------------------------------------------------
df_map = {
    "df_primary": df_primary,
    # "df_secondary": df_secondary,
    # "df_extended": df_extended
}

# --- Chart Dispatcher ---
render_all_charts_local(
    selected_use_case=selected_use_case,
    tab_mapping=tab_mapping,
    df_map=df_map
)

# --- Timeseries Data Missing Info --
st.caption("⚠️ One or more components may be excluded from the chart due to unavailability \
of time series data.")

# -------------------------------------------------------------------------------------------------
# --- Summary Table ---
# -------------------------------------------------------------------------------------------------
st.divider()
st.subheader("🧾 Macro Signal Summary")
gb = GridOptionsBuilder.from_dataframe(summary_df)
gb.configure_default_column(wrapText=True, autoHeight=True)
gb.configure_grid_options(domLayout='autoHeight')
AgGrid(summary_df, gridOptions=gb.build(), height=300, fit_columns_on_grid_load=True)

# -------------------------------------------------------------------------------------------------
# Macro Interaction Panel — Observation + AI Bundle (Platinum Canonical Build)
# -------------------------------------------------------------------------------------------------

# COUNTRY, THEME_CODE, THEME_DATA are already defined earlier in your file
# For reference:
# COUNTRY_NAME = "United States"
# COUNTRY = COUNTRY_NAME.lower().replace(" ", "_")
# THEME_CODE = f"{THEME_ID}_{THEME}"
# THEME_DATA = THEMATIC_GROUPS.get(THEME_CODE, {})

# Sidebar toggles (unchanged)
show_obs, show_ai, show_log = render_macro_sidebar_tools(
    theme_readable=THEME_DATA.get("theme_title", "N/A"),
    theme_code=THEME_CODE,
    selected_use_case=selected_use_case,
    selected_timeframe=selected_timeframe,
    summary_df=summary_df,
    score_label=label,
    explanation=explanation
)

# Main interaction tools — ✅ fully updated call
render_macro_interaction_tools_panel(
    module_type="economic_exploration",
    country=COUNTRY_NAME.lower().replace(" ", "_"),
    theme_code=THEME_CODE,
    theme_title=THEME_DATA.get("theme_title", "N/A"),
    show_observation=show_obs,
    show_log=show_log,
    show_ai_export=show_ai,
    theme_data=THEME_DATA,
    selected_use_case=selected_use_case,
    selected_timeframe=selected_timeframe,
    summary_df=summary_df,
    label=label,
    explanation=explanation,
    ai_bundle=ai_bundle,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)

st.sidebar.divider()


# -------------------------------------------------------------------------------------------------
# 📂 View Underlying Data (Generic, Reusable)
# -------------------------------------------------------------------------------------------------
st.divider()
with st.expander("📂 View Underlying Data"):
    # 📝 Caption explaining potential differences between raw files and displayed data
    st.caption(
        "Note: Some datasets have been standardised for clarity. For instance, time series originally "
        "reported in millions may be converted to billions using a consistent multiplier. These "
        "adjustments are non-destructive and applied only at runtime. The original data structure "
        "remains intact for all analytic purposes."
    )


    valid_sets = {
        meta["label"]: meta["df"]
        for key, meta in loaded_datasets.items()
        if meta["df"] is not None and not meta["df"].empty
        and DATASET_REGISTRY.get(key, {}).get("show_in_underlying_data", True)
    }

    if valid_sets:
        tabs = st.tabs(list(valid_sets.keys()))
        for i, (label, df) in enumerate(valid_sets.items()):
            with tabs[i]:
                st.write(f"**{label}**")
                st.dataframe(df.tail(12))
    else:
        st.warning("No underlying data available for this theme.")


# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    content = load_markdown_file(ABOUT_SUPPORT_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
No trading, investment, or policy advice provided.")
