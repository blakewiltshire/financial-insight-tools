# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name
# pylint: disable=non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📁 User Asset Manager

Module to support inspection, validation, and snapshot preparation of user-uploaded financial data.
Designed for integration with the Preloaded Asset Types (User) system used across multiple tools.

Key Functions:
- Visualise asset upload folders and detect missing or malformed files
- Show basic metadata: shape, date range, column integrity
- Trigger user asset snapshot for downstream use
- Provide structural reminders and currency coherence guidance
- Placeholder for future API vendor integration

Resides under: Trade & Portfolio Structuring
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Path Setup
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

from helpers.asset_name_cleaner import (
    clean_asset_name,
    MARKET_DATA_PROVIDERS
)

# -------------------------------------------------------------------------------------------------
# Module Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_3"]

# -------------------------------------------------------------------------------------------------
# Shared Assets
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_user_asset_manager.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
EXTERNAL_PROVIDERS_MD = os.path.join(ROOT_PATH, "docs", "sidebar_external_providers.md")

# -------------------------------------------------------------------------------------------------
# Folder Definitions
# -------------------------------------------------------------------------------------------------
USER_FOLDERS = [
    "commodities_user", "cryptocurrencies_user", "currencies_user",
    "equities_constituents_user", "equities_mag7_user",
    "etf_countries_user", "etf_popular_user", "etf_sectors_user",
    "long_term_bonds_user", "short_term_bonds_user", "market_indices_user"
]

DATA_ROOT = os.path.join(ROOT_PATH, "apps", "data_sources", "financial_data")

# -------------------------------------------------------------------------------------------------
# Streamlit Config
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="User Asset Manager", layout="wide")
st.title("📁 User Asset Manager")
st.caption("*Structure uploaded datasets for use across Insight Tools.*")

# -------------------------------------------------------------------------------------------------
# About This App
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("docs/about_user_asset_manager.md")

# -------------------------------------------------------------------------------------------------
# Optional Directory Override
# -------------------------------------------------------------------------------------------------
with st.expander("⚙️ Advanced: Customise Data Directory"):
    default_path = os.path.join(ROOT_PATH, "apps", "data_sources", "financial_data")
    DATA_ROOT = st.text_input("📂 Data folder root path:", value=default_path)

    if not os.path.exists(DATA_ROOT):
        st.error("⚠️ The provided path does not exist. Please check and try again.")
        st.stop()

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="📈 Trade and Portfolio Structuring")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)

st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Sidebar: Provider Reference
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("📡 Supported Market Data Providers"):
    for provider, meta in MARKET_DATA_PROVIDERS.items():
        st.markdown(f"- [{provider}]({meta['url']})")

with st.sidebar.expander("🌐 Market Data Providers (Manual Upload Guide)"):
    content = load_markdown_file(EXTERNAL_PROVIDERS_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/sidebar_external_providers.md")

# -------------------------------------------------------------------------------------------------
# Folder Overview and Asset Presence
# -------------------------------------------------------------------------------------------------
st.subheader("📦 Uploaded Folder Overview")
st.markdown("""
Below are the recognised folders for Preloaded Asset Types (User) and the associated uploaded CSVs.
""")

status_table = []
for folder in USER_FOLDERS:
    full_path = os.path.join(DATA_ROOT, folder)
    all_files = os.listdir(full_path) if os.path.exists(full_path) else []
    csv_files = [f for f in all_files if f.lower().endswith(".csv")]

    readable_names = [clean_asset_name(f) for f in csv_files]
    file_list = ", ".join(readable_names) if readable_names else "-"

    status_table.append({
        "Folder": folder,
        "Files Found": len(csv_files),
        "CSV Asset Names": file_list,
        "Status": "✅ Ready" if csv_files else "⚠️ Empty or Missing"
    })

df_status = pd.DataFrame(status_table)

# -------------------------------------------------------------------------------------------------
# Asset Name Filter
# -------------------------------------------------------------------------------------------------
search_term = st.text_input("🔍 Search CSV Asset Names", "")
filtered_df = df_status[df_status["CSV Asset Names"].str.contains(
search_term, case=False)] if search_term else df_status

# -------------------------------------------------------------------------------------------------
# AgGrid Display
# -------------------------------------------------------------------------------------------------
gb = GridOptionsBuilder.from_dataframe(df_status)
gb.configure_column(
"Folder", width=160, maxWidth=170, minWidth=140, headerTooltip="User asset upload folder"
)
gb.configure_column("Files Found", width=110, maxWidth=120)
gb.configure_column("Status", width=130, maxWidth=140)
gb.configure_column(
"CSV Asset Names", wrapText=True, autoHeight=True, minWidth=300, width=400, maxWidth=600,
headerTooltip="Cleaned asset names from uploaded CSVs"
)
gb.configure_grid_options(domLayout="normal")

with st.container():
    st.markdown("### 🗂️ Folder & Asset Summary")
    AgGrid(
        filtered_df,
        gridOptions=gb.build(),
        theme="material",
        height=420,
        fit_columns_on_grid_load=True,
        use_container_width=True
    )

# -------------------------------------------------------------------------------------------------
# Snapshot Manifest
# -------------------------------------------------------------------------------------------------
st.markdown("---")
st.subheader("📥 User Asset Snapshot Manifest")
st.markdown("""
This manifest summarises your uploaded asset files by folder category. It allows you to verify
file presence, naming, and logical grouping before running the full snapshot process.

To generate `.pkl` snapshots used in analytical modules such as:

- 🔎 Market & Volatility Scanner
- 📋 Asset Snapshot Scanner
- 📊 Group Summary & Comparison Views

...please proceed to the **Asset Snapshot Scanner** module after reviewing this summary.
""")

with st.expander("📦 View and Download CSV Manifest"):
    snapshot_records = []
    for folder in USER_FOLDERS:
        folder_path = os.path.join(DATA_ROOT, folder)
        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
            for file in files:
                full_path = os.path.join(folder_path, file)
                snapshot_records.append({
                    "Asset Name": clean_asset_name(file),
                    "Asset Category": folder,
                    "File Path (Relative)": os.path.relpath(full_path, DATA_ROOT)
                })

    if snapshot_records:
        df_snapshot = pd.DataFrame(snapshot_records)
        st.dataframe(df_snapshot, use_container_width=True, height=300)

        csv_bytes = df_snapshot.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV Manifest",
            data=csv_bytes,
            file_name="user_asset_manifest.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No user-uploaded `.csv` files found in any user asset folders.")

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
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
            use_container_width=True,
        )

    with open(os.path.join(ROOT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.markdown("---")
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
No trading, investment, or policy advice provided.")
