# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=import-error, unused-variable
# pylint: disable=invalid-name
# pylint: disable=non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🧼 Data Cleaner & Inspector — Toolbox Utility

Purpose:
Streamlit-based application for uploading, inspecting, cleaning, and formatting financial or
economic CSV datasets. Converts date formats, coerces volume suffixes (e.g. 1.2M → 1,200,000),
detects outliers, and enables optional manual editing before export.

Key Features:
- Upload CSV and preview raw data
- Standardise common formats (price columns, dates, volume, change_pct)
- Highlight outliers using IQR method
- Edit cleaned data interactively and export as CSV
- Works across "Securities" and "Economic Indicators"

Intended Use:
Quick-formatting tool for preparing user-uploaded data for use in the Financial Insight Tools suite.
Can also be used to create user-ready preloaded datasets or debug problematic sources.

Limitations:
This module does not enforce schema validation. Users are expected to align cleaned output
with internal conventions (date, open, high, low, close, volume).

Part of: Toolbox & Calculators — Insight Launcher
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup — Adjust based on your module's location relative to the project root.
# Path to project root (level_up_3) — for markdown, branding, etc.
# Path to apps directory (level_up_2) — for `use_cases`, `helpers`, etc.
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders, sidebar links etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_data_cleaning_toolbox.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Data Cleaner & Inspector", layout="wide")
st.title('🧼 Data Cleaner & Inspector')
st.caption("*Fix formatting issues, inspect outliers, and validate fields.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_data_cleaning_toolbox.md")

# -------------------------------------------------------------------------------------------------
# Start Sidebar Operations
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠 Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

# Branding
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member
st.sidebar.title("🔎 Select Data Type")

# --- Date Conversion Function ---
def convert_date_to_us_format(dataframe, date_column="date"):
    """
    Converts a specified column to datetime format, coercing invalid values.

    Args:
        dataframe (pd.DataFrame): DataFrame containing a date column.
        date_column (str): Name of the date column to convert.

    Returns:
        pd.DataFrame: Modified DataFrame with datetime-formatted column.
    """
    try:
        dataframe[date_column] = pd.to_datetime(dataframe[date_column], errors='coerce')
    except (ValueError, TypeError) as e:
        st.error(f"Date conversion failed: {e}")
    return dataframe

# --- Volume Cleaning Function ---
def clean_volume_column(dataframe):
    """
    Converts volume strings with suffixes (e.g., '1.2M') into numeric values.

    Args:
        dataframe (pd.DataFrame): DataFrame containing a 'volume' column.

    Returns:
        pd.DataFrame: DataFrame with numeric 'volume' column.
    """
    def volume_converter(volume_str):
        if isinstance(volume_str, str):
            if 'K' in volume_str:
                return float(volume_str.replace('K', '').replace(',', '')) * 1_000
            if 'M' in volume_str:
                return float(volume_str.replace('M', '').replace(',', '')) * 1_000_000
            if 'B' in volume_str:
                return float(volume_str.replace('B', '').replace(',', '')) * 1_000_000_000
            return float(volume_str.replace(',', ''))
        return volume_str

    if 'volume' in dataframe.columns:
        dataframe['volume'] = dataframe['volume'].apply(volume_converter)
    return dataframe

# --- Generic Data Cleaner ---
# pylint: disable=redefined-outer-name
def clean_data(df, data_type="Securities"):
    """
    Standardises and prepares data for downstream analysis.

    Applies:
    - Column renaming to match unified schema
    - Conversion of 'change_pct' strings to floats
    - Date formatting to datetime (US style)
    - Numeric coercion for key price/volume columns
    - Volume suffix expansion (e.g., 1.2M → 1,200,000)
    - De-duplication and chronological sorting

    Args:
        df (pd.DataFrame): Raw financial or economic data.
        data_type (str): Type of dataset ("Securities" or "Economic Indicators")

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    column_mapping = {
        'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Price': 'close', 'Last': 'close',
        'Volume': 'volume', 'Vol.': 'volume'
    }
    df = df.rename(columns=column_mapping)
    df = convert_date_to_us_format(df, 'date')

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace(',', '', regex=False)

    numeric_columns = ['open', 'high', 'low', 'close']
    if data_type == "Securities":
        numeric_columns.append('volume')

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = clean_volume_column(df)
    df = df.drop_duplicates()
    df = df.sort_values(by='date')
    return df

# --- Outlier Detector ---
def detect_outliers(series):
    """Identifies outliers using the IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)
    return (series < lower) | (series > upper)

# --- Streamlit App Start ---

if 'previous_type' not in st.session_state:
    st.session_state.previous_type = None

data_type = st.sidebar.radio("Select Data Type", ["Securities", "Economic Indicators"])

if data_type != st.session_state.previous_type:
    for key in list(st.session_state.keys()):
        if key not in ["previous_type"]:
            del st.session_state[key]
    st.session_state.previous_type = data_type
    st.rerun()

st.sidebar.write("Upload your data (CSV) for inspection, cleaning, and optional manual editing.")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Uploaded Data:")
    st.dataframe(df.head())

    if st.checkbox("🔎 Show Missing Values Summary"):
        st.write(df.isnull().sum())

    cleaned_df = clean_data(df.copy(), data_type)

    if st.checkbox("🔎 Highlight Outliers"):
        highlight_columns = [
        col for col in ['open', 'high', 'low', 'close', 'volume'] if col in cleaned_df.columns
        ]

        def highlight_outliers(s):
            """Apply conditional styling for outlier highlighting."""
            outliers = detect_outliers(s)
            return ["background-color: yellow" if val else "" for val in outliers]

        styled_df = cleaned_df.style.apply(highlight_outliers, subset=highlight_columns)
        st.dataframe(styled_df, width='stretch')

    if st.checkbox("🧹 Show Auto Cleaned Data"):
        st.dataframe(cleaned_df.head())

    st.write("### ✏️ Edit Data Manually (Optional):")
    edited_df = st.data_editor(cleaned_df, width='stretch', num_rows="dynamic")

    base_name = os.path.splitext(uploaded_file.name)[0]
    cleaned_filename = f"{base_name}_cleaned.csv"

    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Cleaned & Edited Data CSV",
        data=csv,
        file_name=cleaned_filename
    )
else:
    st.info("Please upload a CSV file to start.")

st.divider()

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    with open(os.path.join(PROJECT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            width='stretch',
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width='stretch',
        )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
    No trading, investment, or policy advice provided.")
