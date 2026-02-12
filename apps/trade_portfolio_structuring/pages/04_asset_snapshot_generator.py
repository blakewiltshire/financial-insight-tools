# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught
# pylint: disable=redefined-outer-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Streamlit-based utility app for scanning and summarising financial data files across categories.

This version leverages the shared data processing pipeline from Trade & Portfolio Structuring,
including preloaded asset logic and shared cleaning utilities. Designed to generate snapshot
summaries (last close, % change, 52w range) across all asset categories and export the results
as a pickle or CSV file.

Key Features:
- Scans a local directory for structured financial CSVs
- Uses centralised data cleaning logic for consistency
- Generates summaries per category and visualises recent returns
- Outputs snapshot as both displayable tables and exportable formats
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
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict

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
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_asset_snapshot_scanner.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# These should be structured clearly by function:
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Reminder: __init__.py
# Ensure all relevant folders (e.g., /helpers, /use_cases, /data_sources etc)
# contain an empty __init__.py file.
# This marks them as Python packages and allows import resolution (especially important when
# running via Streamlit or exporting to other Python environments).
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Category Mapping: Folder → Snapshot Category Label
# -------------------------------------------------------------------------------------------------
CATEGORY_MAP = {
    "equities_mag7": "Equities - Magnificent Seven",
    "equities_constituents": "Equities - Sector Constituents",
    "market_indices": "Market Indices",
    "currencies": "Currencies",
    "cryptocurrencies": "Cryptocurrency",
    "commodities": "Commodities",
    "etf_popular": "ETFs - Popular",
    "etf_sectors": "ETFs - Sectors",
    "etf_countries": "ETFs - Countries",
    "short_term_bonds": "Short-Term Bonds",
    "long_term_bonds": "Long-Term Bonds"
}

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Asset Snapshot Scanner", layout="wide")
st.title("📋 Asset Snapshot Scanner")
st.caption("*Pull key stats (e.g., last close, % change, 52w range) for preloaded asset folders.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_asset_snapshot_scanner.md")

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='📈 Trade and Portfolio Structuring')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member


# --- Data Source ---
snapshot_source = st.sidebar.radio(
    "📁 Choose Asset Snapshot Source",
    ["Preloaded Asset Types (Default)", "Preloaded Asset Types (User)"],
    index=0
)

st.sidebar.divider()

# --- About & Support ---
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    with open(os.path.join(ROOT_PATH, "docs", "crafting-financial-frameworks.pdf"), "rb") as f:
        st.download_button(
            "📘 Crafting Financial Frameworks",
            f.read(),
            file_name="crafting-financial-frameworks.pdf",
            mime="application/pdf",
            width='stretch',
        )

    with open(os.path.join(ROOT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            width='stretch',
        )

# -------------------------------------------------------------------------------------------------
# Directory Input (with Exclusions)
# -------------------------------------------------------------------------------------------------
EXCLUDED_DIRS = {
    "sample_data", "shared_data", "__pycache__",
    "preprocessed_user", "preprocessed_default", "preprocessed_snapshot",
    "asset_currency_converted", "processing_correlation",
    "processing_correlation_assets", "trade_history"
}

with st.expander("⚙️ Advanced: Customise Data Directory"):
    default_path = os.path.join(APPS_PATH, "data_sources", "financial_data")
    data_root = st.text_input("📂 Enter path to your local data folder:", value=default_path)

    if not os.path.exists(data_root):
        st.error("⚠️ The provided path does not exist. Please check and try again.")
        st.stop()

    all_dirs = os.listdir(data_root)

    if snapshot_source == "Preloaded Asset Types (User)":
        asset_dirs = [
            d for d in all_dirs
            if d.endswith(
            "_user") and os.path.isdir(os.path.join(data_root, d)) and d not in EXCLUDED_DIRS
        ]
    else:
        asset_dirs = [
            d for d in all_dirs
            if not d.endswith(
            "_user") and os.path.isdir(os.path.join(data_root, d)) and d not in EXCLUDED_DIRS
        ]

# -------------------------------------------------------------------------------------------------
# Helper: Asset Name Cleaner
# -------------------------------------------------------------------------------------------------
def clean_asset_name(filename):
    """
    Standardises an asset file name by removing common suffixes and extensions.

    Args:
        filename (str): The original filename (e.g., "Tesla Stock Price History.csv").

    Returns:
        str: Cleaned asset name (e.g., "Tesla").
    """
    name = filename.replace(" Stock Price History", "").replace(
        " Historical Data", "").replace(".csv", "")
    return name.strip()

# -------------------------------------------------------------------------------------------------
# Helper: Cleaning
# -------------------------------------------------------------------------------------------------
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
    except Exception as date_error:  # pylint: disable=broad-exception-caught
        st.error(f"Date conversion failed: {date_error}")
    return dataframe


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
            volume_str = volume_str.replace(',', '')
            if 'K' in volume_str:
                return float(volume_str.replace('K', '')) * 1_000
            if 'M' in volume_str:
                return float(volume_str.replace('M', '')) * 1_000_000
            if 'B' in volume_str:
                return float(volume_str.replace('B', '')) * 1_000_000_000
            return float(volume_str)
        return volume_str

    if 'volume' in dataframe.columns:
        dataframe['volume'] = dataframe['volume'].apply(volume_converter)
    return dataframe


def clean_data(raw_df):
    """
    Standardises and prepares financial asset data for downstream analysis.

    Applies:
    - Column renaming to match unified schema
    - Conversion of 'change_pct' strings to floats
    - Date formatting to datetime (US style)
    - Numeric coercion for key price/volume columns
    - Volume suffix expansion (e.g., 1.2M → 1,200,000)
    - De-duplication and chronological sorting

    Args:
        raw_df (pd.DataFrame): Raw financial data containing historical price series.

    Returns:
        pd.DataFrame: Cleaned DataFrame ready for summary or visualisation.
    """
    column_mapping = {
        'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Price': 'close', 'Last': 'close',
        'Volume': 'volume', 'Vol.': 'volume', 'Change %': 'change_pct'
    }

    df_cleaned = raw_df.rename(columns=column_mapping)

    # Ensure 'date' exists before attempting to parse
    if 'date' in df_cleaned.columns:
        df_cleaned = convert_date_to_us_format(df_cleaned, 'date')
    else:
        st.error("🛑 The file does not contain a valid 'Date' column.")
        return pd.DataFrame()  # Return empty to prevent crash downstream

    if 'change_pct' in df_cleaned.columns:
        df_cleaned['change_pct'] = df_cleaned['change_pct'].astype(str).str.replace(
        '%', '', regex=False)
        df_cleaned['change_pct'] = pd.to_numeric(df_cleaned['change_pct'], errors='coerce')

    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.replace(',', '', regex=False)
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    df_cleaned = clean_volume_column(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()

    # Again check for 'date' before sort to prevent silent break
    if 'date' in df_cleaned.columns:
        df_cleaned = df_cleaned.sort_values(by='date', ascending=True)
    else:
        st.warning("⚠️ Could not sort by date. Column missing after cleaning.")

    return df_cleaned

# -------------------------------------------------------------------------------------------------
# Summary Generator
# -------------------------------------------------------------------------------------------------
def calculate_summary(input_df):
    """
    Computes a snapshot of financial asset performance for use in summary tables.

    Extracts:
    - Most recent close price
    - 1-month percentage change (if data available)
    - Year-to-date (YTD) percentage change (if data available)
    - 52-week low, high, and the total price range

    Args:
        input_df (pd.DataFrame): Cleaned DataFrame with 'date' and 'close' columns.

    Returns:
        tuple:
            last_close (float): Latest closing price.
            chg_1m (float | None): Change over the past month.
            chg_ytd (float | None): Change since start of current year.
            low_52w (float | None): 52-week low.
            high_52w (float | None): 52-week high.
            range_52w (float | None): Difference between high and low over 52 weeks.

    Raises:
        ValueError: If the input DataFrame is empty after filtering.
    """
    local_df = input_df.copy().sort_values("date").dropna(subset=["close"])
    if local_df.empty:
        raise ValueError("DataFrame is empty after cleaning")

    last_close = local_df["close"].iloc[-1]
    last_date = local_df["date"].iloc[-1]
    one_month_ago = last_date - timedelta(days=32)
    ytd_start = datetime(last_date.year, 1, 1)
    year_ago = last_date - timedelta(days=366)

    try:
        price_1m_ago = local_df[local_df["date"] <= one_month_ago]["close"].iloc[-1]
        chg_1m = ((last_close - price_1m_ago) / price_1m_ago) * 100
    except IndexError:
        chg_1m = None

    try:
        price_ytd = local_df[local_df["date"] <= ytd_start]["close"].iloc[-1]
        chg_ytd = ((last_close - price_ytd) / price_ytd) * 100
    except IndexError:
        chg_ytd = None

    try:
        df_52w = local_df[local_df["date"] >= year_ago]
        low_52w = df_52w["close"].min()
        high_52w = df_52w["close"].max()
        range_52w = high_52w - low_52w
    except ValueError:
        low_52w = high_52w = range_52w = None

    return last_close, chg_1m, chg_ytd, low_52w, high_52w, range_52w

# -------------------------------------------------------------------------------------------------
# Snapshot Processing
# -------------------------------------------------------------------------------------------------
category_data = defaultdict(list)

for folder_name in asset_dirs:
    folder_path = os.path.join(data_root, folder_name)

    for filename in os.listdir(folder_path):
        if not filename.endswith(".csv"):
            continue
        if filename.startswith("asset_snapshot_summary") or filename.endswith(".pkl"):
            continue  # prevent re-processing of exported summaries


        asset_name = clean_asset_name(filename)
        file_path = os.path.join(folder_path, filename)

        try:
            df = pd.read_csv(file_path)
            df = clean_data(df)

            if "date" not in df.columns or "close" not in df.columns or df.empty:
                raise ValueError("Missing required columns or empty after cleaning")

            last_close, chg_1m, chg_ytd, low_52w, high_52w, range_52w = calculate_summary(df)
            last_10_df = df.dropna(subset=["change_pct"]).tail(10)
            last_10_returns = last_10_df["change_pct"].round(2).tolist()

            # Map folder to standard category name
            is_user = folder_name.endswith("_user")
            raw_category = folder_name.replace("_user", "") if is_user else folder_name
            mapped_category = CATEGORY_MAP.get(raw_category, raw_category)
            final_category = f"{mapped_category} (User)" if is_user else mapped_category

            record = {
                "Asset Name": asset_name,
                "Last Close": last_close,
                "1M % Chg": chg_1m,
                "YTD % Chg": chg_ytd,
                "52w Low": low_52w,
                "52w High": high_52w,
                "52w Range": range_52w,
                "Last 10 Days Return": last_10_returns,
                "Category": final_category
            }

            category_data[folder_name].append(record)

        except (
        FileNotFoundError, ValueError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
            st.warning(f"⚠️ Failed to process {asset_name}: {error}"
            )

# -------------------------------------------------------------------------------------------------
# Render Tables
# -------------------------------------------------------------------------------------------------
for category, records in category_data.items():
    df = pd.DataFrame(records)
    if df.empty:
        continue

    st.markdown(f"### 📊 {category}")
    st.data_editor(
        df,
        width='stretch',
        column_config={
            "1M % Chg": st.column_config.NumberColumn(format="%.2f %%"),
            "YTD % Chg": st.column_config.NumberColumn(format="%.2f %%"),
            "Last Close": st.column_config.NumberColumn(format="%.2f"),
            "52w Low": st.column_config.NumberColumn(format="%.2f"),
            "52w High": st.column_config.NumberColumn(format="%.2f"),
            "52w Range": st.column_config.NumberColumn(format="%.2f"),
            "Last 10 Days Return": st.column_config.BarChartColumn(y_min=-10, y_max=15)
        },
        disabled=True,
        hide_index=True
    )

# -------------------------------------------------------------------------------------------------
# Export Snapshot
# -------------------------------------------------------------------------------------------------
# Flatten all records into a single list of dictionaries
full_records = [{**r} for records in category_data.values() for r in records]
df_snapshot = pd.DataFrame(full_records)

# Define export folders
is_user = snapshot_source == "Preloaded Asset Types (User)"
export_folder_name = "preprocessed_user" if is_user else "preprocessed_default"
export_folder_path = os.path.join(data_root, export_folder_name)
csv_snapshot_path = os.path.join(data_root, "preprocessed_snapshot")

# UI Section: Save Snapshot
with st.expander("📦 Export Asset Snapshot Summary"):
    st.markdown("Choose where you'd like to save the cleaned `.pkl` snapshot \
    and download the `.csv`.")

    # Display export path for confirmation
    st.code(f"Saving snapshot to: {export_folder_path}")

    if st.button("✅ Save Snapshot as Pickle"):
        os.makedirs(export_folder_path, exist_ok=True)
        pickle_path = os.path.join(export_folder_path, "preloaded_asset_summary.pkl")
        df_snapshot.to_pickle(pickle_path)
        st.success(f"Snapshot saved as `.pkl` to:\n`{pickle_path}`")

    # Save CSV to snapshot folder and allow download
    csv = df_snapshot.to_csv(index=False).encode("utf-8")
    os.makedirs(csv_snapshot_path, exist_ok=True)
    csv_path = os.path.join(csv_snapshot_path, "asset_snapshot_summary.csv")
    df_snapshot.to_csv(csv_path, index=False)

    st.download_button(
        "📅 Download Snapshot CSV",
        data=csv,
        file_name="asset_snapshot_summary.csv",
        mime="text/csv"
    )

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
    No trading, investment, or policy advice provided.")
