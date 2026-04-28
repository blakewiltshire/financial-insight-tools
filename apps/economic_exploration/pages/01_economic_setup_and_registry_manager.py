# -------------------------------------------------------------------------------------------------
# Economic Setup & Registry Manager (Reference Guide)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Economic Setup & Registry Manager
---------------------------------
Reference guide for expanding the FIT macroeconomic framework.

This page separates three implementation paths:
1. Registry-only series for Thematic Correlation, Relative Macro Transmission, or Custom Comparison.
2. Full Economic Exploration country scaffolding.
3. Full Economic Exploration DSS theme integration.

The module is intentionally instructional. It does not automate setup actions.
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
import importlib.util
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import (
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

# -------------------------------------------------------------------------------------------------
# Resolve Paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
PROJECT_PATH = PATHS["level_up_3"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_thematic_registry_explorer.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Registry Paths
# -------------------------------------------------------------------------------------------------
GROUPINGS_PATH = os.path.join(PROJECT_PATH, "apps", "registry", "thematic_groupings.py")
INDICATOR_MAP_PATH = os.path.join(PROJECT_PATH, "apps", "registry", "economic_series_map.py")


# -------------------------------------------------------------------------------------------------
# Load module helper
# -------------------------------------------------------------------------------------------------
def load_module(module_name, file_path):
    """
    Dynamically load a Python module from a file path.

    Args:
        module_name (str): Name assigned to the loaded module.
        file_path (str): Full path to the Python file.

    Returns:
        module: Loaded Python module.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -------------------------------------------------------------------------------------------------
# Load constants into memory
# -------------------------------------------------------------------------------------------------
groupings_module = load_module("thematic_groupings", GROUPINGS_PATH)
indicator_module = load_module("economic_series_map", INDICATOR_MAP_PATH)

THEMATIC_GROUPS = groupings_module.THEMATIC_GROUPS
ECONOMIC_SERIES_MAP = indicator_module.ECONOMIC_SERIES_MAP

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Economic Setup & Registry Manager", layout="wide")
st.title("Economic Setup & Registry Manager")
st.caption(
    "*Reference guide for configuring registry series, Economic Exploration countries, "
    "and thematic modules across the FIT macroeconomic system.*"
)

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='Economic Exploration')

for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.info("""
**Economic Setup & Registry Manager**

This page provides the implementation reference for expanding the Financial Insight Tools
macroeconomic framework.

It distinguishes between three setup paths:

• **Registry Series** — add data for Thematic Correlation, Relative Macro Transmission,
  or Custom Comparison without creating a full Economic Exploration dashboard.

• **Economic Exploration Country** — create a full country scaffold with launcher routing,
  metadata, template validation, and dashboard availability.

• **Economic Exploration Theme** — add a full DSS module to an existing Economic Exploration
  country, including use cases, indicators, scoring, insights, visuals, routing, and CSVs.

Universal layers define shared methods, routing expectations, reusable scaffolds,
and analytical behaviour.

Country and registry implementations define available datasets, source mappings,
local folders, CSV files, and enabled indicators.
""")

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

    st.caption("Reference documents bundled with this distribution:")

    crafting_pdf = os.path.join(PROJECT_PATH, "docs", "crafting-financial-frameworks.pdf")
    if os.path.exists(crafting_pdf):
        with open(crafting_pdf, "rb") as f:
            st.download_button(
                "📘 Crafting Financial Frameworks",
                f.read(),
                file_name="crafting-financial-frameworks.pdf",
                mime="application/pdf",
                width='stretch',
            )

    glossary_pdf = os.path.join(PROJECT_PATH, "docs", "fit-unified-index-and-glossary.pdf")
    if os.path.exists(glossary_pdf):
        with open(glossary_pdf, "rb") as f:
            st.download_button(
                "📚 FIT — Unified Index & Glossary",
                f.read(),
                file_name="fit-unified-index-and-glossary.pdf",
                mime="application/pdf",
                width='stretch',
            )

# -------------------------------------------------------------------------------------------------
# Tabs
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "Choose Setup Path",
    "Add Registry Series",
    "Add Economic Exploration Country",
    "Add Economic Exploration Theme",
    "View Theme Definitions & Indicator Registry",
])

# -------------------------------------------------------------------------------------------------
# Tab 1: Choose Setup Path
# -------------------------------------------------------------------------------------------------
with tabs[0]:
    st.header("Choose the Correct Setup Path")

    st.markdown("""
Before adding folders, CSV files, or registry entries, decide which setup path applies.

The FIT macroeconomic system supports three distinct implementation routes. These routes are
separate by design. Not every country needs a full Economic Exploration dashboard.

Some countries are only needed for Thematic Correlation, Relative Macro Transmission, or
Custom Comparison. In those cases, registry-only setup is the correct path.
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
### Route A — Registry Series Only

Use when data is needed for:

- Thematic Correlation
- Relative Macro Transmission
- Custom Comparison

Requires:

- country-code data folder
- source/theme folder
- CSV file(s)
- `economic_series_map.py` entry
- TC/RMT flags

Does **not** require Economic Exploration country scaffolding.
""")

    with col2:
        st.markdown("""
### Route B — Economic Exploration Country

Use when a country should appear inside the Economic Exploration dashboard.

Requires:

- launcher entry
- sidebar navigation
- country routing
- metadata
- template page
- validation data

No live indicators are required at this stage.
""")

    with col3:
        st.markdown("""
### Route C — Economic Exploration Theme

Use when an existing Economic Exploration country needs a full DSS theme.

Requires:

- theme page
- use cases
- indicator maps
- scoring and labels
- insights
- visual configuration
- routing
- CSV integration
""")

    st.info(
        "Registry-only setup is the clean route for countries or markets used in TC/RMT "
        "without a full dashboard. Full Economic Exploration setup is only needed when the "
        "country should appear as a dashboard country."
    )

# -------------------------------------------------------------------------------------------------
# Tab 2: Add Registry Series
# -------------------------------------------------------------------------------------------------
with tabs[1]:
    st.header("➕ Add Registry Series")

    st.markdown("""
Use this section to add indicators for Thematic Correlation, Relative Macro Transmission,
or Custom Comparison without creating a full Economic Exploration country dashboard.

This route is commonly used for countries or markets that support comparative macro structure,
for example sovereign yields, equity indices, FX pairs, reserves, external balances, or other
series needed by TC/RMT surfaces.
""")

    with st.expander("1️⃣ Create the Country Data Folder", expanded=True):
        st.markdown("""
Create a country-code folder inside:

```text
apps/data_sources/economic_data/
```

Example:

```text
apps/data_sources/economic_data/ch
```

Use the same country code convention applied elsewhere in the system:

- `us` = United States
- `uk` = United Kingdom
- `ch` = Switzerland
- `au` = Australia
""")

    with st.expander("2️⃣ Create the Theme or Source Folder", expanded=True):
        st.markdown("""
Inside the country folder, create the thematic folder required by the registry entry.

Examples:

- `600_sovereign_yields`
- `1100_equity_index`
- `400_headline_core_inflation`

Example structure:

```text
apps/data_sources/economic_data/ch
├── 1100_equity_index
│   └── ch_m_1100_structural.csv
└── 600_sovereign_yields
    └── ch_m_600_structural.csv
```
""")

    with st.expander("3️⃣ Create the CSV File", expanded=True):
        st.markdown("""
Use the same generic column headings where possible.

Example:

```text
date,CH2YT,CH10YT
2024-01-01,0.85,1.12
2024-02-01,0.88,1.16
```

Important:

- Column names must exactly match the `name` field in `economic_series_map.py`
- Maintain consistent naming across countries where the structure is universal
- Use country-specific labels only when the series is genuinely local or source-specific
- Keep numeric values clean, without symbols, commas, or mixed text
- All datasets must use the standard international date format: `YYYY-MM-DD`
""")

    with st.expander("4️⃣ Register in `economic_series_map.py`", expanded=True):
        st.markdown("""
Add the indicator entry inside:

```text
apps/registry/economic_series_map.py
```

Minimum required fields for registry-only TC/RMT use:

- `use_case`
- `name`
- `ui_display_name`
- `indicator_id`
- `source_indicator`
- `theme`
- `template`
- `unit_type`
- `unit_multiplier`
- `frequency`
- `seasonal_adjustment`
- `value_type`
- `country`
- `source`
- `source_url`
- `folder`
- `filename`
- `release_schedule_final`
- `note`
- `allow_correlation`
- `allow_relative_macro_transmission`
- `relative_series_type`
- `rmt_surface_type`

Example:

```python
"Switzerland": {
    "600_financial_conditions_risk_analysis": {
        "600_sovereign_yields_template": {
            "CH10YT": {
                "use_case": "Not Applicable",
                "name": "CH10YT",
                "ui_display_name": "Long-Term Sovereign Yield (10Y)",
                "indicator_id": "Not Applicable",
                "source_indicator": "CH10YT=RR",
                "theme": "600_financial_conditions_risk_analysis",
                "template": "interest_rate_template",
                "unit_type": "Prices",
                "unit_multiplier": 1,
                "frequency": "Monthly",
                "seasonal_adjustment": "Not Applicable",
                "value_type": "Index",
                "country": "Switzerland",
                "source": "Investing.com",
                "source_url": "https://www.investing.com/rates-bonds/switzerland-10-year-bond-yield-historical-data",
                "folder": "600_sovereign_yields",
                "filename": "ch_m_600_structural.csv",
                "release_schedule_final": "End of Month",
                "note": "",
                "allow_correlation": True,
                "allow_relative_macro_transmission": True,
                "relative_series_type": "market",
                "rmt_surface_type": "sovereign_yield",
            },
        }
    }
}
```
""")

    with st.expander("5️⃣ Set Correlation and RMT Flags", expanded=True):
        st.markdown("""
These flags determine where the indicator becomes available.

```python
"allow_correlation": True
```

Makes the series available inside Thematic Correlation.

```python
"allow_relative_macro_transmission": True
```

Makes the series available inside Relative Macro Transmission and Custom Comparison.

```python
"relative_series_type": "macro"
```

or

```python
"relative_series_type": "market"
```

Defines whether the series behaves as a macro or market series inside RMT.

```python
"rmt_surface_type": "sovereign_yield"
```

Assigns the indicator to a primary RMT surface, such as:

- `sovereign_yield`
- `carry_rate`
- `external_balance`

Use a blank value when the series should only be available for Custom Comparison and does not
belong to a named RMT surface:

```python
"rmt_surface_type": ""
```
""")

    with st.expander("6️⃣ Validate the Integration", expanded=True):
        st.markdown("""
After registration:

- Confirm the series appears inside Thematic Correlation where expected
- Confirm the series appears inside Relative Macro Transmission where expected
- Test Custom Comparison selection
- Confirm charts render correctly
- Confirm no missing-column errors exist

If the series is not visible, check:

- folder mismatch
- filename mismatch
- CSV column mismatch
- incorrect `country` naming
- incorrect `allow_correlation` or `allow_relative_macro_transmission` flag
- incorrect `relative_series_type`
- unexpected `rmt_surface_type`
""")

# -------------------------------------------------------------------------------------------------
# Tab 3: Add Economic Exploration Country
# -------------------------------------------------------------------------------------------------
with tabs[2]:
    st.header("➕ Add an Economic Exploration Country")

    st.markdown("""
Use this section only when a country should appear inside the Economic Exploration dashboard.

This full scaffold is not required when adding series only for Thematic Correlation,
Relative Macro Transmission, or Custom Comparison. For those workflows, use
**Add Registry Series**.

For demonstration purposes, this walkthrough uses the United States as the example country.
""")

    with st.expander("📘 Integration Context", expanded=True):
        st.markdown("""
The Economic Exploration country setup creates the full dashboard scaffold.

It prepares:

- `/apps/economic_exploration/<country_name>/`
- `.streamlit/` configuration
- country `app.py`
- indicator map, insight, routing, scoring, use case, and visual folders
- a starter template page
- country metadata in shared constants
- validation data copied from `000/` templates

This step creates the dashboard shell only. Live theme data is added later through
**Add Economic Exploration Theme**.
""")

    with st.expander("1️⃣ Prepare the Country Directory"):
        st.markdown("""
Create the folder for the new country inside:

```text
apps/economic_exploration/
```

Example:

```bash
mkdir apps/economic_exploration/united_states
```

Windows:

```cmd
mkdir apps\\economic_exploration\\united_states
```
""")

    with st.expander("2️⃣ Copy `default_country_template` Contents"):
        st.markdown("""
Copy all contents of:

```text
apps/economic_exploration/default_country_template/
```

into the new country folder.

macOS / Linux:

```bash
cp -r apps/economic_exploration/default_country_template/ apps/economic_exploration/united_states/
```

Windows:

```cmd
xcopy apps\\economic_exploration\\default_country_template\\* apps\\economic_exploration\\united_states\\ /E /I /H
```

This copies the app shell, hidden configuration, and local module folders.
""")

    with st.expander("3️⃣ Add the Universal Starter Page"):
        st.markdown("""
Copy the universal starter module:

```text
apps/economic_exploration/pages_template/000_template.py
```

into:

```text
apps/economic_exploration/<country_name>/pages/
```

Example:

```bash
cp apps/economic_exploration/pages_template/000_template.py apps/economic_exploration/united_states/pages/
```
""")

    with st.expander("4️⃣ Create the Validation Data Folder"):
        st.markdown("""
Create a country-code folder inside:

```text
apps/data_sources/economic_data/
```

Example:

```bash
mkdir apps/data_sources/economic_data/us
```

Copy only the validation files from the `000/` template area:

- `000_generic/`
- `000_m_000_structural.csv`

Then rename:

```text
000_m_000_structural.csv → us_m_000_structural.csv
```

These placeholder files validate the country scaffold. They are not live source data.
""")

    with st.expander("5️⃣ Update Shared Metadata"):
        st.markdown("""
Update shared configuration so the country appears correctly in the launcher.

Examples:

```python
# constants/regions.py
"United States": (35.9078, 127.7669)

# constants/emoji.py
"United States": "🇺🇸"
```

Update the country app metadata:

```python
COUNTRY_NAME = "United States"
COUNTRY_CODE = "us"
```
""")

    with st.expander("6️⃣ Verify Launch"):
        st.markdown("""
Restart the launcher and confirm:

- Country appears in the expected region / sub-region
- Country dashboard opens without error
- Sidebar shows the starter Template page
- Placeholder charts and summaries render
- No unresolved paths, missing configs, or undefined variables appear

Once verified, the country is ready for full theme integration.
""")

# -------------------------------------------------------------------------------------------------
# Tab 4: Add Economic Exploration Theme
# -------------------------------------------------------------------------------------------------
with tabs[3]:
    st.header("➕ Add an Economic Exploration Theme")

    st.markdown("""
Use this section when a country already exists inside Economic Exploration and you want to add
a full DSS theme such as Labour Market Dynamics, Inflation Price Dynamics, Financial Conditions
and Risk Analysis or Market Trends Financial Health.

This route is different from registry-only setup. It creates a full dashboard surface with use
cases, scoring, charts, insight logic, routing, data loading, and optional AI export context.
""")

    theme_tabs = st.tabs([
        "Step 1: Copy and Activate Theme Module",
        "Step 2: Review and Validate Mapping",
        "Step 3: Prepare and Upload CSV",
        "Step 4: Advanced Configuration",
    ])

    with theme_tabs[0]:
        st.subheader("Step 1: Copy and Activate Theme Module")

        st.markdown("""
Each thematic grouping is identified by a numeric prefix, for example:

- `200_labour_market_dynamics.py` → theme app page
- `indicator_map_200.py` → indicator signal mapping
- `insight_200.py` → insight text and bias mapping
- `routing_200.py` → data routing
- `use_case_200.py` → use case definitions
- `visual_config_200.py` → chart rendering
- `scoring_weights_labels_200_labour_market_dynamics.py` → weighting and labels

Copy the required files from:

```text
apps/economic_exploration/modules_template/
```

into the matching folders for the target country:

```text
apps/economic_exploration/<country_name>/
```

Set the country metadata inside the copied page:

```python
COUNTRY_NAME = "United States"
COUNTRY_CODE = "000"  # temporary validation mode
```

Use `COUNTRY_CODE = "000"` first to validate layout and placeholder logic. Switch to the
real country code once live CSV data is ready.
""")

    with theme_tabs[1]:
        st.subheader("Step 2: Review and Validate Mapping")

        st.markdown("""
Before uploading data, define how the system interprets each indicator.

`economic_series_map.py` is the shared metadata layer connecting CSV columns to:

- Economic Exploration DSS use cases
- chart labels and source metadata
- Thematic Correlation availability
- Relative Macro Transmission and Custom Comparison availability
- AI-facing metadata context where applicable

Use the registry viewer tab to inspect existing structures before adding new entries.
""")

        st.markdown("""
### Mapping File Structure

```python
{
    "<Country Name>": {
        "<Theme ID>": {
            "<Template Group>": {
                "<Indicator Key>": {
                    ...
                }
            }
        }
    }
}
```
""")

        st.markdown("""
### Required Fields per Indicator

| Field | Purpose |
|---|---|
| `use_case` | Logical DSS use case, e.g. `Employment Trends`. |
| `name` | Must exactly match the CSV column name. |
| `ui_display_name` | Friendly label used in charts, selectors, and summaries. |
| `indicator_id` | Internal ID used for DSS logic and thematic metadata mapping. |
| `source_indicator` | Source series code or source-native identifier. |
| `theme` | Theme ID, e.g. `200_labour_market_dynamics`. |
| `template` | Template group within the theme. |
| `unit_type` | Unit description, e.g. `Index`, `%`, `Thousands of Persons`. |
| `unit_multiplier` | Multiplier used to standardise values. |
| `frequency` | Observation frequency. |
| `seasonal_adjustment` | Seasonal status. |
| `value_type` | Level, index, YoY %, QoQ %, etc. |
| `country` | Country implementation name. |
| `source` | Full data source name. |
| `source_url` | Source reference URL. |
| `folder` | Dataset folder under the country data source path. |
| `filename` | CSV filename containing the indicator. |
| `release_schedule_final` | Optional release timing or publication note. |
| `note` | Optional clarification or source caveat. |
| `allow_correlation` | Enables the indicator for Thematic Correlation. |
| `allow_relative_macro_transmission` | Enables the indicator for RMT / Custom Comparison. |
| `relative_series_type` | RMT classification: `macro` or `market`. |
| `rmt_surface_type` | Optional named RMT surface. Blank is valid for Custom Comparison-only availability. |
""")

        st.markdown("""
### Correlation and Relative Macro Transmission Flags

Indicators can be exposed beyond Economic Exploration through routing flags:

```python
"allow_correlation": True,
"allow_relative_macro_transmission": True,
"relative_series_type": "macro",
"rmt_surface_type": "",
```

A blank `rmt_surface_type` is valid when the indicator should be available for Custom Comparison
but does not belong to a named RMT surface.
""")

        st.markdown("""
### Example Entry

```python
"Number of People in Employment - Employment Trends": {
    "use_case": "Employment Trends",
    "name": "Number of People in Employment",
    "ui_display_name": "Number of People in Employment (Thousands)",
    "indicator_id": "201_total_employment",
    "source_indicator": "PAYEMS",
    "theme": "200_labour_market_dynamics",
    "template": "employment_template",
    "unit_type": "Thousands of Persons",
    "unit_multiplier": 0.001,
    "frequency": "Monthly",
    "seasonal_adjustment": "Seasonally Adjusted Annual Rate",
    "value_type": "Level",
    "country": "United States",
    "source": "FRED Economic Data (BLS)",
    "source_url": "https://fred.stlouisfed.org/series/PAYEMS",
    "folder": "200_employment",
    "filename": "us_m_200_structural.csv",
    "release_schedule_final": "First Friday after month-end (BLS Employment Situation Report)",
    "note": "Primary US employment measure excluding farm workers and military.",
    "allow_correlation": True,
    "allow_relative_macro_transmission": True,
    "relative_series_type": "macro",
    "rmt_surface_type": "",
},
```
""")

    with theme_tabs[2]:
        st.subheader("Step 3: Prepare and Upload CSV")

        st.markdown("""
Prepare a clean CSV aligned to the indicators configured in `economic_series_map.py`.

Required CSV format:

- UTF-8 encoded
- first column named `date`
- date format: standard international format (`YYYY-MM-DD`)
- column headers exactly match `name` fields in `economic_series_map.py`
- numeric values only; no commas, symbols, or mixed strings

File naming pattern:

```text
{country_code}_{frequency_tag}_{theme_id}_structural.csv
{country_code}_{frequency_tag}_{theme_id}_composite.csv
```

Examples:

- `us_q_100_structural.csv`
- `uk_m_200_structural.csv`
- `us_w_200_composite.csv`

After uploading the file, switch the theme page from validation mode to the live country code:

```python
COUNTRY_CODE = "us"
```
""")

    with theme_tabs[3]:
        st.subheader("Step 4: Advanced Configuration")

        st.markdown("""
Advanced configuration is used when a default Economic Exploration theme needs to move beyond
the universal scaffold.

This is where a country-specific theme becomes meaningful.

The core principle is:

**Universal = scaffold**
**Local = meaning**

Universal files prove the default module structure works.
Local files define the real country-specific interpretation.

This walkthrough uses the proven implementation:

```text
🇺🇸 United States - Market Trends Financial Health
Use Case: Aggregate Equity Allocation
Theme ID: 1100
```

Use this example as the reference pattern when extending other local country modules.
""")

        st.info(
            "Reference example: 🇺🇸 United States - Market Trends Financial Health "
            "with the local use case Aggregate Equity Allocation."
        )

        st.markdown("""
### What Advanced Configuration Adds

Use advanced configuration when adding:

- real local use cases
- country-specific indicators
- local signal logic
- custom insight text
- scoring weights and labels
- local routing rules
- custom visual sections
- additional datasets or frequencies
- statistical profile panels
- AI-ready local context

Do **not** modify the universal layer unless you are deliberately changing the reusable scaffold
for every country using that theme.
""")

        st.markdown("""
### Default Scaffold vs Local Meaning

A default theme may begin with placeholder use cases such as:

```text
Signal A
Signal B
Signal C
```

These are not real indicators. They exist to prove the module plumbing works:

- page loading
- use case selection
- indicator dispatch
- scoring display
- visual rendering
- AI bundle structure
- template validation

When a local use case is added, the country module extends the scaffold:

```text
Signal A
Signal B
Signal C
Aggregate Equity Allocation
```

The placeholder signals remain available, but the page should open on the real local
implementation where appropriate:

```python
DEFAULT_USE_CASE = "Aggregate Equity Allocation"
```
""")

        st.markdown("---")

        st.subheader("Local Modules Commonly Updated")

        st.markdown("""
When extending a theme locally, the following files are commonly updated:

```text
use_cases/use_case_<theme>.py
indicator_map/indicator_map_<theme>.py
insights/insight_<theme>.py
scoring_weights_labels/scoring_weights_labels_<theme>.py
routing/routing_<theme>.py
visual_config/visual_config_<theme>.py
pages/<theme_page>.py
```

The main page usually controls:

- `COUNTRY_NAME`
- `COUNTRY_CODE`
- `THEME`
- `THEME_ID`
- `STRUCTURAL_FOLDER`
- `COMPOSITE_FOLDER`
- `DEFAULT_USE_CASE`
- `DATASET_REGISTRY`
- `df_dict`
- `df_map`
- chart dispatcher call signature
""")

        st.markdown("""
### Required String Alignment

Most integration issues come from string mismatches.

Keep exact alignment across:

```text
CSV headers
→ economic_series_map.py
→ use_cases
→ indicator_map
→ insights
→ scoring_weights_labels
→ routing
→ visual_config
→ page registry
```

If one label differs, the system may still load, but signals, insights, scoring,
visuals, or routing may silently fail or return insufficient data.
""")

        with st.expander("1️⃣ Use Cases — Define the Local User-Facing Surface"):
            st.markdown("""
`use_cases` defines what appears in the sidebar dropdown.

A local extension should import universal use cases first, then add country-specific use cases.

Example pattern:

```python
from universal_use_cases_1100 import get_use_cases as get_universal_use_cases

USE_CASES = dict(get_universal_use_cases())

USE_CASES.update({
    "Aggregate Equity Allocation": {
        "Indicators": [
            "Equity Market Value Position",
            "Economy Wide Liability Structure",
            "Aggregate Equity Allocation Ratio"
        ],
        "Categories": [
            "Equity Value Numerator",
            "Liability Denominator"
        ],
        "Description": (
            "Tracks aggregate equity market value against economy-wide liability structure "
            "to observe long-cycle allocation conditions, capital positioning, and broader market context."
        )
    }
})


def get_use_cases():
    return USE_CASES
```

If the local use case should open first, call the selector with the page default:

```python
selected_use_case, USE_CASES = render_use_case_selector(
    get_use_cases,
    default_use_case=DEFAULT_USE_CASE,
)
```
""")

        with st.expander("2️⃣ Indicator Map — Connect Use Cases to Signal Functions"):
            st.markdown("""
`indicator_map` connects each selected indicator to a signal function.

The local file should:

1. import universal placeholder signal maps
2. define local signal functions
3. merge universal and local indicator maps

Example structure:

```python
from universal_indicator_map_1100 import get_indicator_signal_map

template_signals = get_indicator_signal_map()

ALL_INDICATOR_MAPS = {
    "Signal A": {
        "Signal A": template_signals["Signal A"]
    },
    "Signal B": {
        "Signal B": template_signals["Signal B"]
    },
    "Signal C": {
        "Signal C": template_signals["Signal C"]
    },
    "Aggregate Equity Allocation": {
        "Equity Market Value Position": equity_market_value_position_signal,
        "Economy Wide Liability Structure": economy_wide_liability_structure_signal,
        "Aggregate Equity Allocation Ratio": aggregate_equity_allocation_ratio_signal,
    },
}


def get_indicator_maps():
    return ALL_INDICATOR_MAPS
```

The indicator names in `use_cases` must match the keys inside the local indicator map.
""")

        with st.expander("3️⃣ Insights — Map Signal Outputs to Narrative Context"):
            st.markdown("""
`insights` maps signal outputs to narrative text and bias labels.

The local insight file should:

1. import the universal insight dispatcher
2. define local insight text for real local signals
3. fall back to universal insight logic for placeholder signals

Example:

```python
LOCAL_INSIGHTS = {
    "Aggregate Equity Allocation Ratio": {
        "Equity Allocation Share Elevated": {
            "bias": "Growth Supportive",
            "text": (
                "The aggregate equity allocation ratio is strengthening relative to recent norms, "
                "suggesting a larger share of the combined equity-and-liability structure is being "
                "accounted for by equity market value."
            ),
        },
        "Equity Allocation Share Stable": {
            "bias": "Neutral",
            "text": (
                "The aggregate equity allocation ratio is broadly stable, indicating limited recent "
                "change in long-cycle allocation balance between equity value and economy-wide liabilities."
            ),
        },
        "Equity Allocation Share Softening": {
            "bias": "Contraction Warning",
            "text": (
                "The aggregate equity allocation ratio is easing relative to recent norms, suggesting "
                "equity market value is accounting for a smaller share of the combined structure."
            ),
        },
    },
}


def generate_econ_insights(indicator, signal_result, timeframe, extra_value=None):
    local_map = LOCAL_INSIGHTS.get(indicator, {})

    if signal_result in local_map:
        entry = local_map[signal_result]
        return entry["text"], entry["bias"]

    return generate_universal_econ_insights(
        indicator,
        signal_result,
        timeframe,
        extra_value
    )
```

Bias labels should stay aligned with the scoring framework:

```text
Growth Supportive
Neutral
Contraction Warning
```
""")

        with st.expander("4️⃣ Scoring Weights & Labels — Set Local Interpretation Weight"):
            st.markdown("""
`scoring_weights_labels` defines how indicator results contribute to the thematic alignment score.

Local scoring should:

1. import universal scoring labels and weights
2. define local use-case scoring labels
3. merge universal weights first
4. apply local weights second

Example:

```python
from universal_scoring_weight_labels_1100 import (
    get_alignment_score_label as get_alignment_score_label_universal,
    indicator_weights as universal_indicator_weights
)


def score_aggregate_equity_allocation(alignment_ratio):
    if alignment_ratio >= 0.85:
        return (
            "✅ Equity Allocation Conditions Firm",
            "Aggregate equity allocation indicators are broadly aligned in a supportive direction."
        )

    if alignment_ratio >= 0.33:
        return (
            "⚠️ Mixed Allocation Signals",
            "Aggregate equity allocation indicators show partial alignment."
        )

    if alignment_ratio >= -0.2:
        return (
            "⚠️ Allocation Conditions Softening",
            "Aggregate equity allocation signals suggest some softening."
        )

    return (
        "🚨 Liability Structure Dominating",
        "The broader liability structure appears to be dominating the allocation backdrop."
    )


USE_CASE_SCORING_LABELS = {
    "Aggregate Equity Allocation": score_aggregate_equity_allocation,
}


def get_alignment_score_label(alignment_ratio, use_case):
    if use_case in USE_CASE_SCORING_LABELS:
        return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)

    return get_alignment_score_label_universal(alignment_ratio, use_case)


indicator_weights = dict(universal_indicator_weights)

indicator_weights.update({
    "Equity Market Value Position": 3,
    "Economy Wide Liability Structure": 2,
    "Aggregate Equity Allocation Ratio": 3,
})


def get_indicator_weight(indicator_name):
    return indicator_weights.get(indicator_name, 1)
```

This preserves placeholder scoring while allowing the local use case to carry its own weightings.
""")

        with st.expander("5️⃣ Routing — Send Each Indicator to the Correct Dataset"):
            st.markdown("""
`routing` connects each indicator to the correct dataframe.

Local routing should:

1. route country-specific indicators first
2. fall back to universal routing for template signals
3. avoid pandas truth-value checks such as `df_a or df_b`

Use explicit `is not None` checks.

Example:

```python
from universal_routing_1100 import get_indicator_input as get_indicator_input_universal


def get_indicator_input(indicator_name, df_dict):
    aggregate_equity_indicators = {
        "Equity Market Value Position",
        "Economy Wide Liability Structure",
        "Aggregate Equity Allocation Ratio",
    }

    if indicator_name in aggregate_equity_indicators:
        df_local_slice = df_dict.get("df_aggregate_equity_allocation_slice")
        df_local_full = df_dict.get("df_aggregate_equity_allocation_full")
        df_fallback = df_dict.get("df_primary_slice")

        if df_local_slice is not None:
            return df_local_slice

        if df_local_full is not None:
            return df_local_full

        return df_fallback

    return get_indicator_input_universal(indicator_name, df_dict)
```

Routing is especially important where the local use case uses a different dataset or frequency
from the default template signals.
""")

        with st.expander("6️⃣ Visual Configuration — Keep Local Charts Local"):
            st.markdown("""
`visual_config` controls how use cases are displayed.

The visual layer follows the same architecture:

```text
Universal visuals = default scaffold charts
Local visuals = real country/use-case charts
```

Universal should only contain generic template plots such as:

```python
plot_signal_a_chart
plot_signal_b_chart
plot_signal_c_chart
display_chart_with_fallback
```

Real local visuals should be defined in the local visual file.

Example imports:

```python
from universal_visual_config_1100 import (
    display_chart_with_fallback,
    plot_signal_a_chart,
    plot_signal_b_chart,
    plot_signal_c_chart,
)

from universal_visual_shared import calculate_statistical_profile
```

Then define local chart helpers such as:

```python
plot_equity_market_value_chart
plot_liability_structure_chart
plot_aggregate_equity_allocation_ratio_chart
build_aear_statistical_series_map
```

Do not put local use-case chart logic into universal unless it is intended to become reusable
for every country using that theme.
""")

        with st.expander("7️⃣ Visual Dispatcher — Template vs Local Extension"):
            st.markdown("""
There are two valid dispatcher patterns.

### Default Template Page

For simple placeholder themes using only Signal A / Signal B / Signal C:

```python
render_all_charts_local(
    selected_use_case=selected_use_case,
    tab_mapping=tab_mapping,
    df_map=df_map
)
```

This is lightweight and sufficient where local tab-container control is not required.

---

### Local Extended Page

For local use cases with nested chart tabs, statistical profiles, or multi-dataset visuals:

```python
render_all_charts_local(
    selected_use_case=selected_use_case,
    tabs_dict=tabs_dict,
    tab_mapping=tab_mapping,
    df_map=df_map,
)
```

Use this when local visuals need access to the actual Streamlit tab containers.

This avoids treating a dataframe as a tab object and supports richer local chart rendering.

---

### Important Rule

Do not change the page-wide timeframe tab architecture unless necessary.

Adapt the local visual dispatcher to the existing page structure rather than refactoring every page.
""")

        with st.expander("8️⃣ Main Page Dataset Registry — Register Local Datasets"):
            st.markdown("""
The main page defines which datasets exist and how they are loaded.

For local extensions, add new datasets to `DATASET_REGISTRY`.

Example:

```python
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
    },

    "df_aggregate_equity_allocation": {
        "label": "Aggregate Equity Allocation Dataset",
        "file": f"{COUNTRY_CODE}_q_{THEME_ID}_structural.csv",
        "folder": "1100_equity_allocations",
        "frequency": "quarterly",
        "cleaner": clean_economic_data,
        "show_in_underlying_data": True,
        "plot": True,
        "create_slice": True
    },

    "df_market_context": {
        "label": "Aggregate Equity Allocation Market Context Dataset",
        "file": f"{COUNTRY_CODE}_m_{THEME_ID}_structural.csv",
        "folder": "1100_equity_index",
        "frequency": "monthly",
        "cleaner": clean_economic_data,
        "show_in_underlying_data": False,
        "plot": False,
        "create_slice": False
    }
}
```

Then expose the relevant datasets through `df_dict` and `df_map`:

```python
df_dict = {
    "df_primary_slice": df_primary_slice,
    "df_full": df_primary,
    "df_aggregate_equity_allocation_slice": globals().get("df_aggregate_equity_allocation_slice"),
    "df_aggregate_equity_allocation_full": globals().get("df_aggregate_equity_allocation"),
    "df_market_context": globals().get("df_market_context"),
}

df_map = {
    "df_primary": df_primary,
    "df_aggregate_equity_allocation": globals().get("df_aggregate_equity_allocation"),
    "df_market_context": globals().get("df_market_context"),
}
```
""")

        with st.expander("9️⃣ economic_series_map.py — When Registry Metadata Is Needed"):
            st.markdown("""
`economic_series_map.py` is primarily used for:

- Thematic Correlation
- Relative Macro Transmission
- Custom Comparison
- source metadata
- source URLs
- AI bundle context
- registry visibility

Do not add placeholder entries to `economic_series_map.py`.

Only add an entry when:

- the data is actually sourced
- the series should be visible to TC / RMT / Custom Comparison
- the local EE DSS needs full metadata support
- the series should appear in registry-backed AI context

A user who only wants to add a TC/RMT comparison series does not need a full Economic Exploration
theme page.

They may only need:

```text
local data source folder
CSV file
economic_series_map.py entry
```

This keeps **Add Registry Series** separate from **Add Economic Exploration Theme**.
""")

        with st.expander("🔟 Validation Checklist"):
            st.markdown("""
Before treating a local extension as complete, confirm:

### Use Case

- local use case appears in the sidebar
- `DEFAULT_USE_CASE` opens the correct local use case
- placeholder signals remain available if inherited from universal

### Data

- files exist in the expected country folder
- CSV headers match indicator names or source column logic
- date column loads cleanly
- correct frequency is declared

### Indicator Logic

- every selected indicator has a function
- every function returns a string signal
- insufficient data is handled safely

### Insights

- every possible signal string maps to insight text
- bias labels use the correct scoring vocabulary

### Scoring

- local weights override universal where needed
- use-case scoring labels return clean labels and explanations
- `score / max_score` behaves as expected

### Routing

- each local indicator receives the correct dataframe
- no pandas dataframe is evaluated in an `or` chain
- local routing falls back to universal safely

### Visuals

- local charts are defined locally
- universal charts remain scaffold-only
- chart dispatcher signature matches the page call
- tabs are not confused with dataframe slices

### Page Integration

- `DATASET_REGISTRY` contains every required dataset
- `df_dict` supports scoring and routing
- `df_map` supports visual rendering
- underlying data expander shows only intended datasets
""")

        st.markdown("---")

        st.subheader("Final Rule")

        st.markdown("""
If the feature is reusable across every country, it may belong in universal.

If the feature depends on a specific country, dataset, source, scoring assumption,
visual interpretation, or local use case, it belongs in local.

```text
Universal = scaffold
Local = meaning
```

That rule should govern every advanced configuration decision.
""")

# -------------------------------------------------------------------------------------------------
# Tab 5: View Theme Definitions & Indicator Registry
# -------------------------------------------------------------------------------------------------
with tabs[4]:
    st.header("View Theme Definitions & Indicator Registry")
    st.caption("Browse high-level themes, inspect country-specific indicator maps, and validate registry structure.")

    with st.expander("ℹ️ Help"):
        content = load_markdown_file(HELP_APP_MD)
        if content:
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.warning("Missing: docs/help_thematic_registry_explorer.md")

    sub_tabs = st.tabs(["Thematic Groupings", "Indicator Map", "Audit Panel"])

    # ---------------------------------------------------------------------------------------------
    # Sub-tab 1: Thematic Groupings
    # ---------------------------------------------------------------------------------------------
    with sub_tabs[0]:
        st.subheader("Thematic Groupings Overview")
        st.markdown("*Browse high-level theme definitions and indicator memberships.*")

        theme_data = []
        for theme_id, theme in THEMATIC_GROUPS.items():
            title = theme.get("theme_title", "")
            intro = theme.get("theme_introduction", "")
            templates = ", ".join(theme.get("template", {}).keys())
            memberships = theme.get("memberships", {})
            use_cases = sorted({entry.get("Use Case", entry.get("use_case", "")) for entry in memberships.values()})
            theme_data.append({
                "Theme ID": theme_id,
                "Theme Title": title,
                "Templates": templates,
                "Use Cases": ", ".join([u for u in use_cases if u]),
                "Introduction": intro[:180] + "..." if len(intro) > 180 else intro,
            })

        theme_df = pd.DataFrame(theme_data)
        gb = GridOptionsBuilder.from_dataframe(theme_df)
        gb.configure_default_column(wrapText=True, autoHeight=True, filter=True, sortable=True, resizable=True)
        gb.configure_column("Theme ID", pinned="left", width=140)
        gb.configure_pagination(paginationAutoPageSize=True)
        grid_options = gb.build()
        AgGrid(theme_df, gridOptions=grid_options, height=340, fit_columns_on_grid_load=True)

        def sort_key(k):
            try:
                return int(str(k).split("_")[0])
            except ValueError:
                return float("inf")

        sorted_theme_options = sorted(THEMATIC_GROUPS.keys(), key=sort_key)
        st.divider()
        selected_theme = st.selectbox("Explore Membership of a Theme", options=sorted_theme_options)
        selected_members = THEMATIC_GROUPS[selected_theme].get("memberships", {})

        member_data = []
        for code, entry in selected_members.items():
            overview = entry.get("overview", "")
            member_data.append({
                "Indicator Code": code,
                "Use Case": entry.get("Use Case", entry.get("use_case", "")),
                "Title": entry.get("title", ""),
                "Overview": overview[:180] + "..." if len(overview) > 180 else overview,
                "Investment Impact": entry.get("investment_action_importance", ""),
                "Personal Impact": entry.get("personal_impact_importance", ""),
                "Recommended Periods": ", ".join(entry.get("recommended_time_periods", [])),
            })

        membership_df = pd.DataFrame(member_data)
        st.markdown(f"#### Membership Details for **{selected_theme}**")
        if not membership_df.empty:
            gb = GridOptionsBuilder.from_dataframe(membership_df)
            gb.configure_default_column(wrapText=True, autoHeight=True, filter=True, sortable=True, resizable=True)
            gb.configure_column("Indicator Code", pinned="left", width=140)
            gb.configure_pagination(paginationAutoPageSize=True)
            grid_options = gb.build()
            AgGrid(membership_df, gridOptions=grid_options, height=420, fit_columns_on_grid_load=True)
        else:
            st.info("No membership entries found for this theme.")

    # ---------------------------------------------------------------------------------------------
    # Sub-tab 2: Indicator Map
    # ---------------------------------------------------------------------------------------------
    with sub_tabs[1]:
        st.subheader("Indicator Map Explorer")
        st.markdown("*Query indicators by country, theme, template, source, and module flags.*")

        indicator_records = []
        for country, themes in ECONOMIC_SERIES_MAP.items():
            for theme, templates in themes.items():
                for template, indicators in templates.items():
                    for code, entry in indicators.items():
                        indicator_records.append({
                            "Country": country,
                            "Theme": theme,
                            "Template": template,
                            "Indicator Code": code,
                            "Use Case": entry.get("use_case", entry.get("Use Case", "")),
                            "Name": entry.get("name", ""),
                            "Display Name": entry.get("ui_display_name", entry.get("name", "")),
                            "Indicator ID": entry.get("indicator_id", ""),
                            "Source Indicator": entry.get("source_indicator", ""),
                            "Unit": entry.get("unit_type", ""),
                            "Frequency": entry.get("frequency", ""),
                            "Seasonal Adj.": entry.get("seasonal_adjustment", ""),
                            "Value Type": entry.get("value_type", ""),
                            "Source": entry.get("source", ""),
                            "Source URL": entry.get("source_url", ""),
                            "Folder": entry.get("folder", ""),
                            "Filename": entry.get("filename", ""),
                            "Allow Correlation": entry.get("allow_correlation", False),
                            "Allow RMT": entry.get("allow_relative_macro_transmission", False),
                            "Relative Series Type": entry.get("relative_series_type", ""),
                            "RMT Surface Type": entry.get("rmt_surface_type", ""),
                            "Release Final": entry.get("release_schedule_final", entry.get("release_schedule: final", "")),
                            "Note": entry.get("note", ""),
                        })

        indicator_df = pd.DataFrame(indicator_records)

        if indicator_df.empty:
            st.warning("No indicator records found.")
        else:
            col1, col2, col3 = st.columns(3)
            country_filter = col1.multiselect("Country", sorted(indicator_df["Country"].dropna().unique()))
            theme_filter = col2.multiselect("Theme", sorted(indicator_df["Theme"].dropna().unique()))
            use_case_filter = col3.multiselect("Use Case", sorted(indicator_df["Use Case"].dropna().unique()))

            col4, col5, col6 = st.columns(3)
            source_filter = col4.text_input("Source Contains", "")
            correlation_only = col5.toggle("Correlation Enabled Only", value=False)
            rmt_only = col6.toggle("RMT Enabled Only", value=False)

            filtered_df = indicator_df.copy()
            if country_filter:
                filtered_df = filtered_df[filtered_df["Country"].isin(country_filter)]
            if theme_filter:
                filtered_df = filtered_df[filtered_df["Theme"].isin(theme_filter)]
            if use_case_filter:
                filtered_df = filtered_df[filtered_df["Use Case"].isin(use_case_filter)]
            if source_filter:
                filtered_df = filtered_df[filtered_df["Source"].str.contains(source_filter, case=False, na=False)]
            if correlation_only:
                filtered_df = filtered_df[filtered_df["Allow Correlation"] == True]
            if rmt_only:
                filtered_df = filtered_df[filtered_df["Allow RMT"] == True]

            show_all = st.toggle("Show All Columns", value=False)
            default_cols = [
                "Country", "Theme", "Use Case", "Display Name", "Frequency", "Source",
                "Folder", "Filename", "Allow Correlation", "Allow RMT", "RMT Surface Type",
            ]
            table_df = filtered_df if show_all else filtered_df[default_cols].copy()

            st.markdown(f"#### Filtered Indicator Table ({len(table_df)} records)")
            gb = GridOptionsBuilder.from_dataframe(table_df)
            gb.configure_default_column(wrapText=True, autoHeight=True, filter=True, sortable=True, resizable=True)
            if "Country" in table_df.columns:
                gb.configure_column("Country", pinned="left", width=120)
            gb.configure_pagination(paginationAutoPageSize=True)
            grid_options = gb.build()
            AgGrid(table_df, gridOptions=grid_options, height=520, fit_columns_on_grid_load=True)

    # ---------------------------------------------------------------------------------------------
    # Sub-tab 3: Audit Panel
    # ---------------------------------------------------------------------------------------------
    with sub_tabs[2]:
        st.subheader("Registry Audit Panel")
        st.markdown("*Check common registry issues across CSV routing and TC/RMT flags.*")

        audit_records = []
        for country, themes in ECONOMIC_SERIES_MAP.items():
            for theme, templates in themes.items():
                for template, indicators in templates.items():
                    for code, entry in indicators.items():
                        issues = []

                        required = ["name", "theme", "template", "country", "folder", "filename"]
                        for field in required:
                            if not entry.get(field):
                                issues.append(f"Missing `{field}`")

                        if entry.get("allow_relative_macro_transmission") and not entry.get("relative_series_type"):
                            issues.append("RMT enabled but `relative_series_type` is blank")

                        if entry.get("allow_correlation") is None:
                            issues.append("Missing `allow_correlation` flag")

                        if entry.get("allow_relative_macro_transmission") is None:
                            issues.append("Missing `allow_relative_macro_transmission` flag")

                        if issues:
                            audit_records.append({
                                "Country": country,
                                "Theme": theme,
                                "Template": template,
                                "Indicator Code": code,
                                "Name": entry.get("name", ""),
                                "Issues": "; ".join(issues),
                            })

        audit_df = pd.DataFrame(audit_records)
        if audit_df.empty:
            st.success("No common registry issues detected.")
        else:
            st.warning(f"{len(audit_df)} potential issue(s) found.")
            gb = GridOptionsBuilder.from_dataframe(audit_df)
            gb.configure_default_column(wrapText=True, autoHeight=True, filter=True, sortable=True, resizable=True)
            gb.configure_column("Country", pinned="left", width=120)
            gb.configure_pagination(paginationAutoPageSize=True)
            grid_options = gb.build()
            AgGrid(audit_df, gridOptions=grid_options, height=520, fit_columns_on_grid_load=True)
