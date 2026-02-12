# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name
# pylint: disable=too-many-locals, too-many-statements
# pylint: disable=too-many-arguments

"""
Classification Schema Viewer — Financial Insight Tools

Explore structured classification datasets across geopolitics, sovereign risk, market status,
and global company registries. Includes region-level forum membership, credit ratings,
and US large-cap corporate profiling.
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
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import load_markdown_file, build_sidebar_links, get_named_paths

# -------------------------------------------------------------------------------------------------
# Data Loaders
# -------------------------------------------------------------------------------------------------
from apps.data_sources.classification_schemas.classification_loader import (
    load_all_classification_data
)

# -------------------------------------------------------------------------------------------------
# Resolve Key Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]
APPS_PATH = PATHS["level_up_2"]
APP_PATH = PATHS["level_up_1"]

ABOUT_APP_MD = os.path.join(PROJECT_PATH, "docs", "about_classification_schema_viewer.md")
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------------------------------------
DATA_PATH = os.path.join(PROJECT_PATH, "apps", "data_sources", "classification_schemas")
classification_data = load_all_classification_data(DATA_PATH)

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# 🧠 Observation Tools (User Observation Logging — Group A)
# -------------------------------------------------------------------------------------------------
from observation_handler_classification_schema import (
    observation_input_form,
    display_observation_log
)

from render_macro_interaction_tools_panel_classification_schema import render_macro_interaction_tools_panel
from macro_insight_sidebar_panel_reference import render_macro_sidebar_tools


# -------------------------------------------------------------------------------------------------
# Defensive getter with fallback to avoid KeyError
# -------------------------------------------------------------------------------------------------
def safe_get(df_dict, key):
    """
    Safely retrieve a value from a dictionary-like object.

    Args:
        df_dict (dict): The dictionary to search.
        key (str): The key to retrieve.

    Returns:
        object: Value if key exists, else None.
    """
    return df_dict.get(key, pd.DataFrame())

df_forum = safe_get(classification_data, "forum")
df_political = safe_get(classification_data, "political")
df_market = safe_get(classification_data, "market")
df_company = safe_get(classification_data, "company_base")
df_largecap = safe_get(classification_data, "company_largecap")

# -------------------------------------------------------------------------------------------------
# Streamlit Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Classification Schema Viewer", layout="wide")
st.title("📚 Classification Schema Viewer")
st.caption(
    "*Explore political, economic, market, and company classifications across "
    "countries and sectors.*"
)

# -------------------------------------------------------------------------------------------------
# Info Panel
# -------------------------------------------------------------------------------------------------
with st.expander("📖 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.warning("Missing: docs/about_classification_schema_viewer.md")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link("app.py", label="📚 Reference Data & Trusted Sources")
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()
st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.subheader("🗂️ View Options")
classification_view = st.sidebar.radio(
    "Choose Classification Dataset",
    [
        "Forum Membership",
        "Political Stability",
        "Market Ratings",
        "Company Register — Global",
        "Company Register — US Large-Cap"
    ],
    key="view_selector"
)

with st.sidebar.expander("ℹ️ App Usage Notes"):
    st.markdown(
        "**Data Source Disclaimer**  \n"
        "All classification and reference data shown are sourced from publicly available datasets. "
        "No values are generated, rated, or interpreted by this tool.\n\n"
        "**Usage Tip**  \n"
        "If you encounter display issues (e.g., blank tables or errors), use the navigation sidebar to "
        "return to the main 📚 Reference Data & Trusted Sources module, then re-enter this viewer.\n\n"
        "This can help reset the rendering state if filters or tabs were changed rapidly."
    )


# -------------------------------------------------------------------------------------------------
# --- FORUM MEMBERSHIP VIEW ---
# -------------------------------------------------------------------------------------------------
def render_forum_view(df):
    """
    Displays the Forum Membership Matrix for filtering countries based on regional blocs,
    political alliances, and economic groupings.

    This view supports targeted filtering by region, country, and membership category,
    including global economic blocs, emerging alliances, European groups, and trade/regional pacts.
    It enables structured comparison of international alignment patterns across countries.

    Filtering is made safe to prevent frontend runtime issues and supports dynamic bloc parsing
    from selected membership categories.

    Args:
        df (pd.DataFrame): The full dataset containing forum membership information and
                           related country-level metadata.
    """

    st.subheader("🌐 Forum Membership Matrix")
    st.markdown("Filter country participation across global economic and political groupings.")

    bloc_categories = [
        "Global Economic Bloc",
        "Emerging Alliance",
        "European Group",
        "Trade & Regional Pacts"
    ]

    region = []
    bloc_category = bloc_categories[0]
    bloc_list = []
    selected_blocs = []
    country = []

    with st.expander("🔎 Filter Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            region = st.multiselect("🌐 Region", sorted(df["Region"].dropna().unique()),
            key="region_forum")
            bloc_category = st.selectbox("🏛️ Membership Category", bloc_categories,
            key="bloc_category")

        with col2:
            country = st.multiselect("🌍 Country", sorted(df["Country"].dropna().unique()),
            key="country_forum")
        with col3:
            if bloc_category in df.columns:
                bloc_raw = df[bloc_category].dropna().astype(str).tolist()
                bloc_split = [
                item.strip() for sublist in bloc_raw for item in sublist.split(",") if item.strip()
                ]
                bloc_list = sorted(set(bloc_split))
            selected_blocs = st.multiselect("🤝 Bloc Membership (Any Match)", options=bloc_list,
            key="bloc_filter")

    df_filtered = df.copy()
    if region:
        df_filtered = df_filtered[df_filtered["Region"].isin(region)]
    if country:
        df_filtered = df_filtered[df_filtered["Country"].isin(country)]
    if selected_blocs and bloc_category in df.columns:
        def has_match(cell):
            if pd.isna(cell):
                return False
            return any(bloc in str(cell).split(", ") for bloc in selected_blocs)
        df_filtered = df_filtered[df_filtered[bloc_category].apply(has_match)]

    st.dataframe(df_filtered, width='stretch')


# -------------------------------------------------------------------------------------------------
# --- POLITICAL STABILITY VIEW ---
# -------------------------------------------------------------------------------------------------
def render_political_view(df):
    """
    Displays the Political and Economic Environment panel, allowing structured filtering by
    regional classification, income level, institutional development, and growth potential.

    This view enables multi-criteria filtering across key variables such as:
    - Region
    - Country
    - GNI per Capita
    - Political Stability
    - Market Infrastructure
    - Economic Growth Rate

    Designed for comparative analysis of national governance capacity, economic development, and
    structural stability. All filters include null-safe handling to ensure frontend robustness.

    Args:
        df (pd.DataFrame): The full dataset containing political, economic, and institutional
                           environment classifications for countries.
    """
    st.subheader("🛡️ Political and Economic Environment")
    st.markdown("Filter political stability and development classifications.")

    with st.expander("🔎 Filter Options – Political Stability & Structure"):
        col1, col2, col3 = st.columns(3)

        with col1:
            region = st.multiselect(
                "🌐 Region", df["Region"].dropna().unique(),
                key="region_political"
            )
            gni = st.multiselect(
                "💰 GNI per Capita", df["GNI per Capita"].dropna().unique(),
                key="gni_political"
            )

        with col2:
            country = st.multiselect(
                "🌍 Country", df["Country"].dropna().unique(),
                key="country_political"
            )
            stability = st.multiselect(
                "🗳️ Political Stability", df["Political Stability"].dropna().unique(),
                key="stability_political"
            )

        with col3:
            infra = st.multiselect(
                "🏗️ Market Infrastructure", df["Market Infrastructure"].dropna().unique(),
                key="infra_political"
            )
            growth = st.multiselect(
                "📈 Economic Growth Rate", df["Economic Growth Rate"].dropna().unique(),
                key="growth_political"
            )


    df_filtered = df.copy()
    if region:
        df_filtered = df_filtered[df_filtered["Region"].isin(region)]
    if country:
        df_filtered = df_filtered[df_filtered["Country"].isin(country)]
    if gni:
        df_filtered = df_filtered[df_filtered["GNI per Capita"].isin(gni)]
    if stability:
        df_filtered = df_filtered[df_filtered["Political Stability"].isin(stability)]
    if infra:
        df_filtered = df_filtered[df_filtered["Market Infrastructure"].isin(infra)]
    if growth:
        df_filtered = df_filtered[df_filtered["Economic Growth Rate"].isin(growth)]

    st.dataframe(df_filtered, width='stretch')

# -------------------------------------------------------------------------------------------------
# --- MARKET RATINGS VIEW ---
# -------------------------------------------------------------------------------------------------
def render_market_view(df):
    """
    Displays the Market Credit Ratings and Classification panel for sovereign credit profiles.

    Provides structured filters across:
    - Region
    - Country
    - Market Status (e.g., Developed, Emerging, Frontier)
    - Credit Ratings from S&P, Moody's, and Fitch (supports partial string match)

    Designed to support analysis of sovereign credit risk, investability,
    and market classification.
    Includes partial text search for credit ratings and handles null values gracefully to avoid
    frontend rendering issues.

    Args:
        df (pd.DataFrame): Sovereign ratings and market status dataset for global economies.
    """
    st.subheader("📈 Market Credit Ratings and Classification")
    st.markdown("Filter sovereign credit profiles and market classification.")

    with st.expander("🔎 Filter Options – Market Ratings & Access"):
        col1, col2, col3 = st.columns(3)

        with col1:
            region = st.multiselect(
                "🌐 Region", df["Region"].dropna().unique(),
                key="region_market"
            )
            status = st.multiselect(
                "📊 Market Status", df["Market Status"].dropna().unique(),
                key="status_market"
            )

        with col2:
            country = st.multiselect(
                "🌍 Country", df["Country"].dropna().unique(),
                key="country_market"
            )

        with col3:
            rating_input = st.text_input(
                "🔍 Search Ratings (e.g. AAA, BB)", "",
                key="rating_market"
            )

    df_filtered = df.copy()
    if region:
        df_filtered = df_filtered[df_filtered["Region"].isin(region)]
    if country:
        df_filtered = df_filtered[df_filtered["Country"].isin(country)]
    if status:
        df_filtered = df_filtered[df_filtered["Market Status"].isin(status)]
    if rating_input:
        mask = df_filtered[["S&P Rating", "Moody Rating", "Fitch Rating"]].apply(
            lambda col: col.str.contains(rating_input, na=False, case=False)
        ).any(axis=1)
        df_filtered = df_filtered[mask]

    st.dataframe(df_filtered, width='stretch')

# -------------------------------------------------------------------------------------------------
# --- GLOBAL COMPANY REGISTER VIEW ---
# -------------------------------------------------------------------------------------------------
def render_company_base_view(df):
    """
    Renders the Global Company Register with tabbed views:
    - Company Overview: filters by region, exchange, industry tag, and name/ticker.
    - Identifiers & Listings: includes CUSIP, ISIN, SEDOL, FIGI, CIK, Exchange, MIC.
    """
    st.subheader("🏢 Global Company Register")
    st.markdown("Explore company records across global regions, exchanges, industry tags, and listings.")

    tab1, tab2 = st.tabs(["🌍 Company Overview", "🔐 Identifiers & Listings"])

    # --------------------------------
    # COMPANY OVERVIEW TAB
    # --------------------------------
    with tab1:
        with st.expander("🔎 Filter Options – Company Register"):
            col1, col2, col3 = st.columns(3)

            with col1:
                region = st.multiselect("🌐 Region", sorted(df["Regions"].dropna().unique()), key="region_base")
                exchange = st.multiselect("🏛️ Exchange", sorted(df["Exchange"].dropna().unique()), key="exchange_base")

            with col2:
                country = st.multiselect("🌍 Country", sorted(df["Country"].dropna().unique()), key="country_base")
                currency = st.multiselect("💱 Market Currency", sorted(df["Market Currency"].dropna().unique()), key="currency_base")

            with col3:
                industry = st.multiselect("🏷️ Industry Tag", sorted(df["Industry Tag"].dropna().unique()), key="industry_base")
                search_term = st.text_input("🔍 Search Ticker or Name", key="search_base")

        df_filtered = df.copy()
        if region:
            df_filtered = df_filtered[df_filtered["Regions"].isin(region)]
        if country:
            df_filtered = df_filtered[df_filtered["Country"].isin(country)]
        if exchange:
            df_filtered = df_filtered[df_filtered["Exchange"].isin(exchange)]
        if currency:
            df_filtered = df_filtered[df_filtered["Market Currency"].isin(currency)]
        if industry:
            df_filtered = df_filtered[df_filtered["Industry Tag"].isin(industry)]
        if search_term:
            term = search_term.lower()
            df_filtered = df_filtered[
                df_filtered["Company Name"].str.lower().str.contains(term, na=False) |
                df_filtered["Ticker"].str.lower().str.contains(term, na=False)
            ]

        st.dataframe(
            df_filtered[[
                "Ticker", "Company Name", "Industry Tag", "Exchange",
                "Country", "Market Currency"
            ]],
            width='stretch'
        )

    # --------------------------------
    # IDENTIFIERS & LISTINGS TAB
    # --------------------------------
    with tab2:
        with st.expander("🔎 Filter Options – Identifiers"):
            col1, col2 = st.columns(2)
            id_search = col1.text_input("🔍 Search by Ticker or Name", key="id_search")
            mic_filter = col2.text_input("🔁 MIC Code (e.g., XNYS, XLON)", key="mic_filter")

        df_id = df.copy()
        if id_search:
            term = id_search.lower()
            df_id = df_id[
                df_id["Company Name"].str.lower().str.contains(term, na=False) |
                df_id["Ticker"].str.lower().str.contains(term, na=False)
            ]
        if mic_filter:
            df_id = df_id[df_id["MIC Code"].str.upper().str.contains(mic_filter.upper(), na=False)]

        st.dataframe(
            df_id[[
                "Ticker", "Company Name", "Country", "Exchange", "MIC Code",
                "CUSIP", "ISIN", "SEDOL", "FIGI", "CIK"
            ]],
            width='stretch'
        )


# -------------------------------------------------------------------------------------------------
# COMPANY REGISTER — GLOBAL: IDENTIFIERS & LISTINGS VIEW
# -------------------------------------------------------------------------------------------------
def render_company_identifiers_view(df):
    """
    Renders the Identifiers & Listings tab for global company register.
    Includes major security identifiers and maps MIC Code to primary exchange.

    Args:
        df (pd.DataFrame): Global company register dataframe with security metadata.
    """
    st.subheader("🔐 Identifiers & Listings")
    st.markdown("Cross-reference major global security identifiers and exchange listings."
                " This tab highlights CUSIP, ISIN, SEDOL, FIGI, and CIK codes — as well as"
                " primary exchange names and MIC codes.")

    with st.expander("🔎 Filter Options – Identifiers & Listings"):
        col1, col2, col3 = st.columns(3)
        region = col1.multiselect("🌐 Region", sorted(df["Regions"].dropna().unique()), key="region_ids")
        country = col2.multiselect("🌍 Country", sorted(df["Country"].dropna().unique()), key="country_ids")
        exchange = col3.multiselect("🏛️ Primary Exchange", sorted(df["Exchange"].dropna().unique()), key="exchange_ids")

        col4, col5, col6 = st.columns(3)
        cusip = col4.text_input("🔐 CUSIP", key="cusip_ids")
        isin = col5.text_input("🌍 ISIN", key="isin_ids")
        sedol = col6.text_input("🇬🇧 SEDOL", key="sedol_ids")

        col7, col8, col9 = st.columns(3)
        figi = col7.text_input("📊 FIGI", key="figi_ids")
        cik = col8.text_input("📁 CIK", key="cik_ids")
        mic = col9.text_input("🆔 MIC Code", key="mic_ids")

    df_ids = df.copy()
    if region:
        df_ids = df_ids[df_ids["Regions"].isin(region)]
    if country:
        df_ids = df_ids[df_ids["Country"].isin(country)]
    if exchange:
        df_ids = df_ids[df_ids["Exchange"].isin(exchange)]

    if cusip:
        df_ids = df_ids[df_ids["CUSIP"].astype(str).str.contains(cusip, case=False, na=False)]
    if isin:
        df_ids = df_ids[df_ids["ISIN"].astype(str).str.contains(isin, case=False, na=False)]
    if sedol:
        df_ids = df_ids[df_ids["SEDOL"].astype(str).str.contains(sedol, case=False, na=False)]
    if figi:
        df_ids = df_ids[df_ids["FIGI"].astype(str).str.contains(figi, case=False, na=False)]
    if cik:
        df_ids = df_ids[df_ids["CIK"].astype(str).str.contains(cik, case=False, na=False)]
    if mic:
        df_ids = df_ids[df_ids["MIC Code"].astype(str).str.contains(mic, case=False, na=False)]

    st.data_editor(
        df_ids[[
            "Ticker", "Company Name", "Exchange", "MIC Code",
            "CUSIP", "ISIN", "SEDOL", "FIGI", "CIK",
            "Regions", "Country", "Market Currency"
        ]],
        column_config={
            "MIC Code": st.column_config.TextColumn("🆔 MIC Code"),
            "Exchange": st.column_config.TextColumn("🏛️ Primary Exchange"),
            "ISIN": st.column_config.TextColumn("🌍 ISIN"),
            "CUSIP": st.column_config.TextColumn("🔐 CUSIP"),
            "CIK": st.column_config.TextColumn("📁 CIK")
        },
        width='stretch',
        disabled=True
    )


# -------------------------------------------------------------------------------------------------
# ADDITION TO US LARGE-CAP: INCLUDE PRIMARY EXCHANGE MAPPED TO MIC
# -------------------------------------------------------------------------------------------------
# This addition is made within the data display of tab1 (Profile) and other tabs as needed.
# Add column: "Exchange" after "Nasdaq 100" for improved clarity.
# Example snippet (insert inside st.dataframe call in US Large-Cap view):
# "S&P 500", "DJIA", "Nasdaq 100", "Exchange", "MIC Code",



# -------------------------------------------------------------------------------------------------
# US LARGE-CAP COMPANY PROFILES (REFINED TABBED VIEW)
# -------------------------------------------------------------------------------------------------
def render_company_largecap_view(df):
    """
    Renders a tabbed view of US large-cap companies, segmented into:
    - Profile: metadata, index inclusion, and firm info.
    - Social & Links: verified external media and websites.
    - Classification Crosswalk: SIC and NAICS-based sector/industry matching.

    Args:
        df (pd.DataFrame): Large-cap company register with classification and index tags.
    """
    st.subheader("🇺🇸 US Large-Cap Classification Viewer")
    st.markdown("Structured exploration of S&P 500, DJIA, and Nasdaq 100 constituents with "
    "sector and industry crosswalks.")

    tab1, tab2, tab3 = st.tabs(["💼 Profile", "📱 Social & Links", "🎯 Classification Crosswalk"])

    # ------------------------
    # PROFILE TAB
    # ------------------------
    with tab1:
        with st.expander("🔎 Filter Options – Profile"):
            col0, col1, col2 = st.columns(3)
            search_ticker = col0.text_input("🔁 Search Ticker", key="profile_ticker")
            search_name = col1.text_input("🧾 Search Company Name", key="profile_name")
            index_membership = col2.multiselect("📈 Index Membership", [
                "S&P 500", "DJIA", "Nasdaq 100"
            ], key="index_lc1")

            col3, col4 = st.columns(2)
            country = col3.multiselect(
                "🌍 Country", sorted(df["Country"].dropna().unique()), key="country_lc1"
            )
            year = col4.multiselect(
                "🏗️ Year Incorporated", sorted(df["Year Incorporated"].dropna().unique()), key="year_lc1"
            )

        df_filtered = df.copy()
        if search_ticker:
            df_filtered = df_filtered[df_filtered[
            "Ticker"].str.contains(search_ticker, case=False, na=False)]
        if search_name:
            df_filtered = df_filtered[df_filtered[
            "Company Name"].str.contains(search_name, case=False, na=False)]
        for idx in index_membership:
            if idx in df.columns:
                df_filtered = df_filtered[df_filtered[idx].notna()]
        if country:
            df_filtered = df_filtered[df_filtered["Country"].isin(country)]
        if year:
            df_filtered = df_filtered[df_filtered["Year Incorporated"].isin(year)]

        st.dataframe(df_filtered[[
            "Ticker", "Company Name", "S&P 500", "DJIA", "Nasdaq 100",
            "Regions", "Country", "Company Description", "Year Incorporated", "Headquarters"
        ]], width='stretch')

    # ------------------------
    # SOCIAL & LINKS TAB
    # ------------------------
    with tab2:
        with st.expander("🔎 Filter Options – Social Media"):
            col0, col1 = st.columns(2)
            search_ticker = col0.text_input("🔁 Search Ticker", key="social_ticker")
            search_name = col1.text_input("🧾 Search Company Name", key="social_name")

        df_social = df.copy()
        if search_ticker:
            df_social = df_social[df_social[
            "Ticker"].str.contains(search_ticker, case=False, na=False)]
        if search_name:
            df_social = df_social[df_social[
            "Company Name"].str.contains(search_name, case=False, na=False)]

        st.data_editor(
            df_social[[
                "Ticker", "Company Name", "S&P 500", "DJIA", "Nasdaq 100",
                "Regions", "Country", "Website", "Wiki", "X"
            ]],
            column_config={
                "Website": st.column_config.LinkColumn("Website"),
                "Wiki": st.column_config.LinkColumn("Wikipedia"),
                "X": st.column_config.LinkColumn("X/Twitter")
            },
            width='stretch',
            disabled=True
        )

    # ------------------------
    # CLASSIFICATION CROSSWALK TAB
    # ------------------------
    with tab3:
        with st.expander("🔎 Filter Options – Classification"):
            col0, col1 = st.columns(2)
            search_ticker = col0.text_input("🔁 Search Ticker", key="class_ticker")
            search_name = col1.text_input("🧾 Search Company Name", key="class_name")

            col2, col3, col4 = st.columns(3)
            sic_code = col2.text_input("🔢 SIC Code", key="sic_code")
            sic_title = col3.text_input("🏷️ SIC Industry Title", key="sic_title")
            naics_sector_code = col4.text_input("🔢 NAICS Sector Code", key="naics_sector_code")

            col5, col6, col7 = st.columns(3)
            naics_sector = col5.text_input("🏷️ NAICS Sector", key="naics_sector")
            naics_national_code = col6.text_input("🔢 NAICS National Industry Code", key="naics_nat_code")
            naics_national = col7.text_input("🏷️ NAICS National Industry", key="naics_nat")


        df_class = apply_classification_filters(
            df.copy(),
            search_ticker,
            search_name,
            sic_code,
            sic_title,
            naics_sector_code,
            naics_sector,
            naics_national_code,
            naics_national
        )

        st.dataframe(df_class[[
            "Ticker", "Company Name",
            "Sec SIC Code", "Sec SIC Industry Title",
            "NAICS Sector Code", "NAICS Sector",
            "NAICS Subsector Code", "NAICS Subsector",
            "NAICS Industry Group Code", "NAICS Industry Group",
            "NAICS Industry Code", "NAICS Industry",
            "NAICS National Industry Code", "NAICS National Industry",
            "DJIA", "Nasdaq 100", "Regions", "Country"
        ]], width='stretch')


# -------------------------------------------------------------------------------------------------
# Classification filter helper (reduced branches/statements)
# -------------------------------------------------------------------------------------------------
def apply_classification_filters(df, ticker, name, sic_code, sic_title,
                                  naics_sec_code, naics_sec, naics_nat_code, naics_nat):
    """
    Apply multi-field classification filters for US company register crosswalk tab.
    """
    if ticker:
        df = df[df["Ticker"].str.contains(ticker, case=False, na=False)]
    if name:
        df = df[df["Company Name"].str.contains(name, case=False, na=False)]
    if sic_code:
        df = df[df["Sec SIC Code"].astype(str).str.startswith(sic_code)]
    if sic_title:
        df = df[df["Sec SIC Industry Title"].str.contains(sic_title, case=False, na=False)]
    if naics_sec_code:
        df = df[df["NAICS Sector Code"].astype(str).str.startswith(naics_sec_code)]
    if naics_sec:
        df = df[df["NAICS Sector"].str.contains(naics_sec, case=False, na=False)]
    if naics_nat_code:
        df = df[df["NAICS National Industry Code"].astype(str).str.startswith(naics_nat_code)]
    if naics_nat:
        df = df[df["NAICS National Industry"].str.contains(naics_nat, case=False, na=False)]
    return df

# -------------------------------------------------------------------------------------------------
# View Dispatcher
# -------------------------------------------------------------------------------------------------
if classification_view == "Forum Membership":
    render_forum_view(df_forum)
elif classification_view == "Political Stability":
    render_political_view(df_political)
elif classification_view == "Market Ratings":
    render_market_view(df_market)
elif classification_view == "Company Register — Global":
    render_company_base_view(df_company)
elif classification_view == "Company Register — US Large-Cap":
    render_company_largecap_view(df_largecap)

st.divider()

# -------------------------------------------------------------------------------------------------
# 🧠 Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
theme_code = "classification_schema_viewer"
theme_title = "Classification Schema Viewer"
selected_use_case = "Classification Schema Viewer Snapshot"

# -------------------------------------------------------------------------------------------------
# 🧠 Activate Observation + Journal Toggles
# -------------------------------------------------------------------------------------------------
show_observation, show_log = render_macro_sidebar_tools(
    theme_readable=theme_title,
    theme_code=theme_code,
    selected_use_case=selected_use_case
)

# 🎯 No fixed assets selected in live dashboard — use empty list
asset_list_for_observation = []

if show_observation or show_log:
    st.markdown("## 🧠 Macro Interaction Tools")
    st.caption("*.*")

render_macro_interaction_tools_panel(
    show_observation=show_observation,
    show_log=show_log,
    observation_input_callback=observation_input_form,
    observation_log_callback=display_observation_log
)


# -------------------------------------------------------------------------------------------------
# About Us
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
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, \
investment, or policy advice provided."
)
