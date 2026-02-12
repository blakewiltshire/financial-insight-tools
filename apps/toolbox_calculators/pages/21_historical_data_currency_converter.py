# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name, broad-exception-caught

"""
Historical Data Currency Converter
Upload, convert, and save OHLC historical data into a unified currency for
better correlation analysis.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
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

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

from data_sources.financial_data.processing_default import load_data_from_file, clean_data_minimal

# -------------------------------------------------------------------------------------------------
# App Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_historical_data_currency_converter.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_historical_data_currency_converter.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")
CONVERTED_DIR = os.path.join(PROJECT_PATH, "apps", "data_sources", "financial_data",
"asset_currency_converted")

# Ensure directory exists
os.makedirs(CONVERTED_DIR, exist_ok=True)

# -------------------------------------------------------------------------------------------------
# Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Historical Data Currency Converter", layout="wide")
st.title("💱 Historical Data Currency Converter")
st.caption("*Standardise asset prices for clean multi-asset correlation.*")

# -------------------------------------------------------------------------------------------------
# App Description and Rationale
# -------------------------------------------------------------------------------------------------
with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_historical_data_currency_converter.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🛠️ Toolbox & Calculators')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# File Upload Section
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📁 Upload Historical File")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")

original_currency = st.sidebar.selectbox("Original Currency", ["USD", "GBP", "EUR", "JPY", "Other"])
target_currency = st.sidebar.selectbox("Target Currency", ["USD", "GBP", "EUR", "JPY", "Other"])
exchange_rate = st.sidebar.number_input(
    "Exchange Rate (1 original = ? target)", min_value=0.0001, value=1.25, format="%.4f"
)

with st.sidebar.expander("💱 Help: Exchange Rate Input"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_historical_data_currency_converter.md")

if uploaded_file and (original_currency != target_currency):
    try:
        # Prepare filename
        original_filename = os.path.splitext(uploaded_file.name)[0]
        safe_name = original_filename.replace("/", "_").replace("\\", "_")
        new_filename = f"{safe_name} [{original_currency}→{target_currency}].csv"
        converted_path = os.path.join(CONVERTED_DIR, new_filename)

        # Load and clean
        df = load_data_from_file(uploaded_file)
        df = clean_data_minimal(df)
        df.columns = [col.lower() for col in df.columns]
        st.success(f"✅ Loaded and cleaned: {safe_name}")

        # Convertible columns
        convertible_cols = ["open", "high", "low", "close"]
        available_cols = [col for col in convertible_cols if col in df.columns]

        # Conversion trigger
        if st.button("🔄 Apply Currency Conversion"):
            if available_cols:
                for col in available_cols:
                    df[col] *= exchange_rate
                st.session_state["converted_df"] = df
                st.session_state["converted_path"] = converted_path
                st.session_state["converted_filename"] = new_filename
                st.success("✅ Currency conversion applied.")
                st.dataframe(df.tail(10))
            else:
                st.warning(
                "⚠️ No convertible price columns found (`open`, `high`, `low`, `close`)."
                )

        # Save button
        if "converted_df" in st.session_state and st.button("💾 Save to Converted Folder"):
            try:
                os.makedirs(CONVERTED_DIR, exist_ok=True)
                st.session_state["converted_df"].to_csv(
                st.session_state["converted_path"], index=False
                )
                saved_filename = st.session_state["converted_filename"]
                st.success(
                    f"✅ File saved to:\n`asset_currency_converted/{saved_filename}`"
                )

            except Exception as e:
                st.error(f"❌ Save failed: {e}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

elif uploaded_file and original_currency == target_currency:
    st.sidebar.warning("Original and target currencies are the same — no conversion will occur.")

st.sidebar.divider()

# --- About & Support ---
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
            use_container_width=True,
        )

    with open(os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf"), "rb") as f:
        st.download_button(
            "📚 FIT — Unified Index & Glossary",
            f.read(),
            file_name="fit-unified-index-and-glossary.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
No trading, investment, or policy advice provided.")
