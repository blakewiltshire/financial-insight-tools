# -------------------------------------------------------------------------------------------------
# 📦 Theme Module Creator UI (Messaging-Only Prototype)
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
📚 Theme Module Creation UI (Messaging Only)
Structured messaging interface for managing thematic and country module creation.
This version focuses on user guidance before enabling automation.
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
import importlib.util
import pandas as pd
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
APP_PATH = PATHS["level_up_1"]
ROOT_PATH = PATHS["level_up_4"]

# -------------------------------------------------------------------------------------------------
# Shared Docs & Branding
# -------------------------------------------------------------------------------------------------
ABOUT_SUPPORT_MD = os.path.join(PROJECT_PATH, "docs", "about_and_support.md")
HELP_APP_MD = os.path.join(PROJECT_PATH, "docs", "help_thematic_registry_explorer.md")
BRAND_LOGO_PATH = os.path.join(PROJECT_PATH, "brand", "blake_logo.png")


# -------------------------------------------------------------------------------------------------
# 📦 Load Constants: Thematic Groupings and Indicator Map
# -------------------------------------------------------------------------------------------------

# Define constant file paths
GROUPINGS_PATH = os.path.join(PROJECT_PATH, "apps", "registry", "thematic_groupings.py")
INDICATOR_MAP_PATH = os.path.join(PROJECT_PATH, "apps", "registry", "economic_series_map.py")

# Load module helper
def load_module(module_name, file_path):
    """
    Dynamically loads a Python module from the specified file path.

    Args:
        module_name (str): Desired name to assign to the loaded module.
        file_path (str): Full path to the Python file (.py) to be imported.

    Returns:
        module: The loaded Python module, accessible as an object.

    Notes:
        This is used to import indicator map or thematic data structures at runtime,
        especially where modular separation or local overrides are required.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load constants into memory
groupings_module = load_module("thematic_groupings", GROUPINGS_PATH)
indicator_module = load_module("economic_series_map", INDICATOR_MAP_PATH)

THEMATIC_GROUPS = groupings_module.THEMATIC_GROUPS
ECONOMIC_SERIES_MAP = indicator_module.ECONOMIC_SERIES_MAP

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Economic Setup & Registry Manager", layout="wide")
st.title("🧭 Economic Setup & Registry Manager")
st.caption("*Central interface for configuring countries, applying thematic modules, and "
"validating the full macroeconomic registry system.*")

# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='🌍 Economic Exploration')

for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)
st.sidebar.divider()

st.logo(BRAND_LOGO_PATH)  # pylint: disable=no-member

st.sidebar.info("""
🧭 **Economic Setup & Registry Manager**

Configure new countries or extend existing economic themes through modular scaffolding,
dataset integration, and indicator registration.

Use this module when:

• Adding new countries to 🌍 Economic Exploration

• Extending existing country indicators and scoring logic

• Integrating structured datasets into visualisation and AI export layers

• Aligning country-level configurations with shared system behaviour

The framework distinguishes between shared structural layers (universal logic) and
country-level implementations.

📦 Outputs remain fully compatible with the Insight Launcher and live dashboards.
""")


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
# Tab 1: Add New Country to Economic Exploration
# -------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "➕ Add New Country",
    "🌐 Add Theme",
    "📚 View Theme Definitions & Indicator Registry"
])


with tabs[0]:
    st.header("➕ Add a New Country to Economic Exploration")
    st.markdown("""
This section walks through the step-by-step process of adding a new country to
the **Economic Exploration** framework.

For demonstration purposes, we use the **United States** as a working example.
The setup includes:

- Creating the country folder structure and Streamlit scaffolding
- Adding required entries to system constants (e.g., `regions.py`, `emoji.py`)
- Validating initial configuration using placeholder test data

Once complete, your country is ready to integrate thematic modules.

🔁 This process sets the foundation — it does not require live data at this stage.
""")


    with st.expander("📘 Integration Context"):
        st.markdown("""
    The ➕ **Add New Country** process scaffolds all required components to
    integrate a new country into the **Economic Exploration** system.

    ---

    🔧 **What this step prepares:**

    - Creates the folder structure for `/economic_exploration/{country name}/`
    - Initializes required Streamlit files (e.g., `.streamlit/`, `app.py`)
    - Adds entries to:
      - `constants/regions.py` (country code, name)
      - `constants/emoji.py` (country flag)

    ---

    📄 **What gets copied:**

    - `000_🧩_template.py` → starter page for the new country
    - Placeholder insight modules and configs (from `modules_template/`)
    - Test data from `000_generic/` and `000_m_000_structural.csv`

    ---

    📂 **Outputs include:**

    - Fully scaffolded country folder with correct app routing
    - Country-ready Streamlit Template module (e.g., `000_🧩_template.py`)
    - Placeholder datasets for initial validation (renamed to match country code)

    ---

    ⚠️ **Important Notes:**

    - This is a **structural onboarding** step — no live data or indicators are included
    - All CSVs and config files are placeholders, sourced from default `000/` templates
    - Data and insight logic must be added by the user or aligned from shared universal modules

    ✅ Once scaffolding is complete, the country is ready to begin thematic
    module configuration using
    🌐 **Add Theme to Existing Country**.
    """)

    with st.expander("1️⃣ Prepare the Country Directory"):

        st.markdown("""
📌 **Project Root Assumption:** All commands assume you're in the root folder:
`/FinTechWorkspace/financial-insight-tools/`
""")

        st.markdown("""
Create the folder for your new country within the project’s app structure.

**🖥 Terminal / Command Line Options**

- **macOS / Linux:**
        """)
        st.code("mkdir apps/economic_exploration/united_states", language="bash")

        st.markdown("- **Windows (CMD):**")
        st.code("mkdir apps\\economic_exploration\\united_states", language="cmd")

        st.markdown("""
---

**🖱 File Explorer / Finder Option**

- **macOS**: Use Finder → navigate to `apps/economic_exploration` and create
the folder `united_states`.
- **Windows**: Use File Explorer → navigate to `apps\\economic_exploration`
and create the folder `united_states`.
""")


    with st.expander("2️⃣ Copy `default_country_template` Folder Contents"):
        st.markdown("""
To scaffold the new country module (e.g., **United States**), copy **all contents** of
the `default_country_template/` directory into your new country folder.

This includes hidden configuration files (`.streamlit`) and default folders such
as `app.py`, `indicator_map`, `insights`, `use_cases`, etc.

---

**🖥 Terminal / Command Line Options**

- **macOS / Linux:**
        """)
        st.code("cp -r apps/economic_exploration/default_country_template/ "
        "apps/economic_exploration/united_states/", language="bash")

        st.markdown("- **Windows (CMD):**")
        st.code("xcopy apps\\economic_exploration\\default_country_template"
        "\\* apps\\economic_exploration\\united_states\\ /E /I /H", language="cmd")

        st.markdown("""
---

**🖱 File Explorer / Finder Option**

1. **Enable hidden files**:
   - **macOS Finder:** Press `Cmd + Shift + .`
   - **Windows Explorer:** Go to **View > Hidden items**

2. Navigate to:
   - `apps/economic_exploration/default_country_template/`

3. **Select and copy all contents**

4. Paste into your new country folder:
   - `apps/economic_exploration/united_states/`

✅ This step ensures the default folder structure and config logic are in place.
""")

    with st.expander("3️⃣ Add Thematic Grouping Page (Universal Template)"):

        st.markdown("""
    To validate that the country setup is functioning, begin with
    the **universal starter module** only:

    - `000_🧩_template.py`

    📁 Located at:

    ```bash
    apps/economic_exploration/pages_template/000_🧩_template.py
    ```

    ---

    **🖥 Terminal / Command Line Option (example: Growth Stability):**

    - macOS / Linux:
        """)
        st.code("cp apps/economic_exploration/pages_template/000_🧩_template.py "
        "apps/economic_exploration/united_states/pages/", language="bash")

        st.markdown("- Windows:")
        st.code("copy apps\\economic_exploration\\pages_template\\"
        "000_🧩_template.py apps\\economic_exploration\\"
        "united_states\\pages\\", language="cmd")

        st.markdown("""
    ---

    **🖱 File Explorer / Finder Option:**

    1. Navigate to:
       `apps/economic_exploration/pages_template/`

    2. Copy the desired file(s) — e.g., `000_🧩_template.py`

    3. Paste into:
       `apps/economic_exploration/united_states/pages/`

    """)


    with st.expander("4️⃣ Create Data Source Folder"):
        st.markdown("""
    Each country requires a dedicated folder to store economic data inputs.
    This step establishes the **minimum required structure** using the
    default `000/`-based templates.

    ---

    📂 **Step 1: Create a Folder for Your Country**

    **🖥 Terminal / Command Line**

    - **macOS / Linux:**
    """)
        st.code("mkdir apps/data_sources/economic_data/us", language="bash")

        st.markdown("- **Windows (CMD):**")
        st.code("mkdir apps\\data_sources\\economic_data\\us", language="cmd")

        st.markdown("""
    ---

    **🖱 File Explorer / Finder Option**

    1. Navigate to:
       `apps/data_sources/economic_data/`

    2. Create a new folder and name it using your country code, e.g.:
       - ✅ `us` for United States

    ---

    📂 **Step 2: Copy Validation Template Files**

    Copy only the essential items used to validate country scaffolding:

    **✅ Required files to copy:**
    - `000_generic/` directory
    - `000_m_000_structural.csv` file (monthly composite placeholder)

    These enable basic placeholder charts and insight signals.

    **🖥 Terminal / Command Line**

    - **macOS / Linux:**
    """)
        st.code("""cp -r apps/data_sources/economic_data/000/000_generic/
        apps/data_sources/economic_data/us/
    cp apps/data_sources/economic_data/000/000_m_000_structural.csv
    apps/data_sources/economic_data/us/""", language="bash")

        st.markdown("- **Windows (CMD):**")
        st.code("""xcopy apps\\data_sources\\economic_data\\000\\000_generic\\*
        apps\\data_sources\\economic_data\\us\\000_generic\\ /E /I /H
    copy apps\\data_sources\\economic_data\\000\\000_m_000_structural.csv
    apps\\data_sources\\economic_data\\us\\
    """, language="cmd")

        st.markdown("""
    ---

    **🖱 File Explorer / Finder Option**

    1. Navigate to:
       `apps/data_sources/economic_data/000/`

    2. Copy:
       - the **folder** `000_generic/`
       - the **file** `000_m_000_structural.csv`

    3. Paste them into your country folder, e.g.:
       `apps/data_sources/economic_data/us/`


   ⚠️ **Do not copy the entire `000/` folder** — only these files are required at this stage.


    ---

    📑 **Step 3: Rename the CSV File**

    To align with country-specific processing, rename the placeholder file:

    - `000_m_000_structural.csv` → `us_m_000_structural.csv`

    This ensures it matches the expected prefix used in validation and chart generation.

    ---

    ✅ These files enable:
    - Basic visual and signal rendering
    - Validation of module structure and country setup logic

    """)

    with st.expander("5️⃣ Update Shared Metadata"):
        st.markdown("""
Update all shared config files and app settings:

---

**📌 constants/regions.py**
""")
        st.code('"United States": (35.9078, 127.7669)', language="python")

        st.markdown("**📌 constants/emoji.py**")
        st.code('"United States": "🇺🇸"', language="python")

        st.markdown("""
**📌 app.py (within country folder)**

Update header metadata:
""")
        st.code("""
COUNTRY_NAME = "United States"
        """, language="python")

        st.markdown("""
**📌 000_🧩_template.py**

Update the following variables:
""")
        st.code("""
COUNTRY_NAME = "United States"
COUNTRY_CODE = "us"
        """, language="python")

    with st.expander("6️⃣ Verify Launch"):
        st.markdown("""
    Launch the main dashboard to ensure all shared updates and metadata have been applied.

    🖥️ **Restart Launcher**

    Close any active session of:
    - 🚀 Welcome to Insight Launcher: 🌍 Economic Exploration

    Then relaunch from:
    - 🚀 Welcome to Financial Insight Tools

    ---

    🗺 **Region Selection**

    Once reloaded, select the following from the launcher:

    - **Select a Region:** Americas
    - **Select a Sub-Region:** North America
    - **Select a Country:** United States

    After clicking **Explore United States**, the following confirmation should appear:

    > 🇺🇸 **United States – Insight Launcher: Economic Exploration**

    ---

    📂 **Navigation Confirmation**

    In the left sidebar under **📂 Navigation Menu**, the universal starter module
    should now be visible:

    > **🧩 Template**

    ---

    🧪 **Final Verification**

    Confirm the following to ensure your country scaffolding is correctly in place:

    - ✅ Template page opens without error
    - ✅ Placeholder visuals load correctly from the copied and renamed CSV file.
    - ✅ Country label displays correctly (e.g., `🇺🇸 United States – 🧩 Template`)
    - ✅ No unresolved paths, undefined variables, or missing configs

    📊 Insight Panels

    - ✅ `Insight Use Cases` are populated (e.g., Signal A, B, C)
    - ✅ `📊 Macro Conditions Summary` renders with expected structure
    - ✅ `📈 Charts` tab shows placeholder visuals by use case
    - ✅ `🧾 Macro Signal Summary` evaluates with fallback scoring

    🧠 Macro Interaction Tools Verification

    - ✅ 📝 Add Custom Observation toggle visible in sidebar
    - ✅ Observation form allows full data entry (text, relevance, sentiment, tags)
    - ✅ Observation writes correctly to:

    ```csv
    /apps/observation_engine/storage/user_observations/economic_exploration/{country}__{theme_code}__user_observations.csv
    ```

    - ✅ Observation Journal displays saved entries, allows inline editing, and correctly commits updates
    - ✅ 🧠 Preview AI Export toggle visible in sidebar
    - ✅ AI Export generates full JSON bundle for selected use case
    - ✅ Saved JSON appears under:

    ```json
    /apps/observation_engine/storage/ai_bundles/{country}__{theme_code}__{use_case}__{timeframe}.json
    ```

    🧪 You have now fully validated the country scaffold with complete macro insight system integration.

    🌐 Proceed to Add Theme to Existing Country to configure full thematic modules and begin sourcing live data.
    """)

# -------------------------------------------------------------------------------------------------
# Tab 2: 🌐 Add Theme
# -------------------------------------------------------------------------------------------------

with tabs[1]:
    st.header("🌐 Add Theme")
    st.markdown("""
Use this section to attach a thematic grouping (e.g., **GDP**, **Labour**, **Inflation**)
to a country that has already been configured and scaffolded.

We assume the country — in this walkthrough, **United States** — has already been
created via **➕ Add New Country**.

🧩 For demonstration purposes, we use the **`200_💼_labour_market_dynamics.py`** theme
as the implementation example. This theme includes:

- Live scoring logic
- Signal routing and use case logic
- AI export integration
- Chart and data visualisation modules

This structure applies across all themes. Once familiar with this flow, you can repeat it for
additional groupings (`200_💼_labour_market_dynamics.py`, `300_🔥_inflation_and_prices.py`, etc.).
""")

    theme_tabs = st.tabs([
        "📋 Step 1: Copy and Activate Theme Module",
        "🔍 Step 2: Review and Validate Mapping",
        "📁 Step 3: Prepare and Upload CSV",
        "🧠 Step 4: Advanced Configuration (Optional)"
    ])

    # --- Step 1: Copy and Activate Theme Module ---
    with theme_tabs[0]:
        st.subheader("📋 Step 1: Copy and Activate Theme Module")

        st.markdown("""
        ### 📌 About Theme Suffixes

        Each thematic grouping in the system is identified by a unique
        numeric prefix (e.g., `100`, `200`, etc.).
        This number links the primary theme app file with all its supporting
        logic modules. For example:

        - `200_💼_labour_market_dynamics.py` → Theme app page
        - `insight_200.py`, `routing_200.py`, `use_case_200.py` → Supporting logic modules

        ✅ Always match the suffix (`_100`, `_200`, etc.) between your
        app page and the helper modules.
        """)

        st.markdown("""
### 📁 What to Copy

Each theme includes modular components that must be placed into your country’s folder.

📁 **Source Folder:**
`apps/economic_exploration/modules_template/`

📁 **Destination Folder:**
`apps/economic_exploration/<your_country>/`

**Required Files:**
- `indicator_map/indicator_map_200.py`
- `insights/insight_200.py`
- `routing/routing_200.py`
- `scoring_weights_labels/scoring_weights_labels_200_labour_market_dynamics.py`
- `use_cases/use_case_200.py`
- `visual_config/visual_config_200.py`
- `pages/200_💼_labour_market_dynamics.py`
""")

        st.markdown("""
---

**🖥 Terminal / Command Line Options**

**macOS / Linux:**
```bash
cp apps/economic_exploration/modules_template/indicator_map/indicator_map_200.py
apps/economic_exploration/united_states/indicator_map/
cp apps/economic_exploration/modules_template/insights/insight_200.py
apps/economic_exploration/united_states/insights/
# Repeat for other folders
```

**Windows (CMD):**
```cmd
xcopy apps\\economic_exploration\\modules_template\\insights\\insight_200.py
apps\\economic_exploration\\united_states\\insights\\"
```

---

### 🖱 File Explorer / Finder Option

1. Navigate to: `apps/economic_exploration/modules_template/`
2. For each subfolder (e.g., `indicator_map/`, `insights/`, etc.):
   - Copy the relevant `_200.py` file
   - Paste it into the corresponding subfolder of your country
3. For the app page:
   - Copy `200_💼_labour_market_dynamics.py` from `modules_template/pages/`
   - Paste it into `apps/economic_exploration/<your_country>/pages/`

---

**🔧 Final Activation**

Once copied, open the app file (e.g., 200_💼_labour_market_dynamics.py) and set:

- **COUNTRY_NAME = "United States**"
- **COUNTRY_CODE = "000**"  # Leave as '000' for now to load default test data

🧠 Keeping COUNTRY_CODE = "000" allows the theme to load test signals and visuals
using 000_m_100.csv, while you source and format your real data.

✅ This ensures the app is fully functional with placeholder logic, so you can
immediately validate layout, scoring, and routing before uploading real datasets.

✅ Once complete, the module is fully connected and ready for 🔍 Step 2: Review and Validate Mapping


""")

# --- Review and Validate Mapping ---
with theme_tabs[1]:
    st.subheader("🔍 Step 2: Review and Validate Mapping")

    st.markdown("""
Before uploading any data, you must define how the system interprets your indicators.

📄 **`economic_series_map.py`** is the master metadata file that links your raw CSV columns
to scoring logic, visualisation tools, and AI export layers. This mapping must be complete
before data upload is possible.

---

### 🧭 Purpose of this Step

This is where you tell the system:

- ✅ What each indicator represents
- ✅ Where to find it, and how to scale and label it
- ✅ How it connects to themes, scoring, and routing logic

This mapping bridges your **local dataset** with the system’s **modular analytical framework**.

---

### 📚 Reference the Indicator Registry

Before manually creating entries, use the **📚 View Theme Definitions &
Indicator Registry** tab to:

- Review supported themes and their default indicators
- Understand required use cases for each module
- Inspect examples across existing countries
- Copy structure from completed implementations (e.g., United States, France)

This ensures consistency and reduces duplication when expanding to new countries.

---

### 🔍 Reviewing Use Cases First

Each theme module defines required use cases — e.g., **"Employment Template"**
for `200_💼_labour_market_dynamics.py`.

📁 These use cases are defined in:

apps/economic_exploration/<your_country>/use_cases/use_case_200.py

Review the active use cases before sourcing indicators so you only search for what’s needed.

This step is especially helpful when working with new countries, where source coverage may vary.

---

### 📂 Mapping File Structure

apps/economic_exploration/economic_series_map.py
```
{
  "<Country Name>": {
    "<Theme ID>": {
      "<Template Group>": {
        ...
      }
    }
  }
}
```

---

### 🧩 Required Fields per Indicator

| Field                 | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `name`                | **Must exactly match** the column name in your CSV                      |
| `indicator_id`        | Unique internal ID (e.g., `201_total_employment`) for use case tracking |
| `Use Case`            | Logical group (e.g., `Employment Template`) for internal organisation   |
| `ui_display_name`     | Friendly label for charts and summaries                                 |
| `source_indicator`    | Full source name (e.g., FRED Economic Data)                             |
| `unit_type`           | Thousands of Persons                                                    |
| `unit_multiplier`     | Multiplier to adjust units (e.g., 0.001 to convert millions to billions)|
| `frequency`           | Frequency of observation (e.g., `Monthly`)                            |
| `seasonal_adjustment` | If applicable (e.g., Seasonally Adjusted, NSA)                          |
| `value_type`          | Level or change (e.g., `Level`, `YoY %`, `QoQ %`)                       |
| `source`              | Full source name (e.g., FRED, ABS, ECB)                                 |
| `filename`            | Name of the CSV file this indicator appears in                          |
| `release_schedule`    | Optional — for adding contextual release info                           |
| `note`                | Optional — free text for assumptions or clarification                   |

---

### 📌 Example Entry (United States – Employment Template)
```
"United States": {
    "200_💼_labour_market_dynamics": {
        "employment_template": {
            "Number of People in Employment": {
                "Use Case": "Employment Trends",
                "name": "Number of People in Employment",
                "ui_display_name": "Total Employment Number of People in Employment (Thousands)",
                "indicator_id": "201_total_employment",
                "source_indicator": "PAYEMS",
                "theme": "200_labour_market_dynamics",
                "template": "employment_template",
                "unit_type": "Thousands of Persons",
                "unit_multiplier": 1,
                "frequency": "Monthly",
                "seasonal_adjustment": "Seasonally Adjusted",
                "value_type": "Level",
                "country": "United States",
                "source": "FRED Economic Data (BLS)",
                "source_url": "https://fred.stlouisfed.org/series/PAYEMS",
                "filename": "us_m_200_structural.csv",
                "release_schedule: final": "First Friday after month-end (BLS Employment Situation Report)",
                "note": "Primary US employment measure excluding farm workers and military."
            }
        }
    }
}
```

✅ Once this metadata is complete, proceed to:
📁 Step 3: Prepare and Upload CSV
""")

    # --- Step 3: Prepare and Upload CSV ---
with theme_tabs[2]:
    st.subheader("📁 Step 3: Prepare and Upload CSV")

    st.markdown("""
Before uploading data, you must prepare a clean, structured CSV aligned to
your configured indicators.

This file will be ingested by the system for your selected **country** and **theme module**.

---

### 📂 Use the Provided Template

Each theme module includes a standardised file template.

For `200_💼_labour_market_dynamics.py`, use:

`/apps/data_sources/economic_data/000/200_employment/000_m_200_structural.csv`

To prepare your dataset:

1. **Copy** the template file and folder (e.g., `200_employment/000_m_200_structural.csv`)
   into your country directory:
   `/apps/data_sources/economic_data/<country_code>/`

2. **Rename** the template file using the format:
   `{country_code}_{frequency_tag}_{theme_id}_structural.csv`
   ✅ Example: `us_m_200_structural.csv`

3. **Replace placeholder values** with your sourced indicators,
   ensuring **column names exactly match** those defined in your
   country’s `economic_series_map.py`.

---

### 📌 File Naming Convention

To ensure compatibility, all files must follow this pattern:

`{country_code}_{frequency_tag}_{theme_id}_structural.csv`

or

`{country_code}_{frequency_tag}_{theme_id}_composite.csv`

| Component                 | Meaning                                      |
|-------------------------- |----------------------------------------------|
| `country_code`            | ISO shorthand (e.g., `us`, `uk`, `fr`)       |
| `frequency_tag`           | `q` = quarterly, `m` = monthly, `w` = weekly |
| `theme_id`                | Theme identifier (e.g., `100`, `200`)        |
| structural / composite    | e.g. _structural.csv                         |

#### ✅ Examples:
- `us_q_100_structural.csv` → US quarterly data for Economic Growth
- `uk_m_200_structural.csv` → UK monthly data for Labour Market
- `us_m_100_composite.csv` →  US specific monthly composite data

---

### 🧾 Required CSV Format

Each dataset must meet the following:

- **UTF-8 encoded**
- **Date format**: `YYYY-MM-DD` in the first column
- **Column headers**: Must match `name` fields in `economic_series_map.py`
- **Clean, numeric values** — no formatting, symbols, or mixed types

📁 **Destination Path**:
`/apps/data_sources/economic_data/<country_code>/`

#### 📄 Example Structure:
| Date       | Participation Rate |Number of People in Employment | Unemployment Rate | ... |
|------------|--------------------|--------------------------|-------------------|-----|
| 1948-01-01 | 58.6               | 44679                    | 3.4               |     |

---

### 🧠 Why Not Use an API?

This system is designed for structured, auditable, and externalAI-augmented workflows
using static files.

While you may source data via API externally, this internal system prioritises:

- ✅ **Auditability** — full visibility into each input
- ✅ **Offline compatibility** — works in air-gapped environments
- ✅ **Minimal dependencies** — no API setup required
- ✅ **AI readiness** — structured inputs enable robust augmentation

As long as your CSV follows the template structure, any source is acceptable.

---

### 🔧 Update Metadata (COUNTRY_CODE)

Open your theme app file (e.g., `200_💼_labour_market_dynamics.py`) and set:

`COUNTRY_CODE = "us"`
(This ensures the app pulls from `/data_sources/economic_data/us/`)

---

### 🚀 Verify Launch

After preparing your data:

1. Restart 🌍 Economic Exploration by closing the app and relaunching via:

`🚀 Welcome to Financial Insight Tools`

2. Navigate to your new module:

- Select Region: `Americas`
- Select Sub-Region: `North America`
- Select Country: `United States`
- Click: `Explore United States`

✅ You should see:

`🇺🇸 United States – Insight Launcher: Economic Exploration`

---

### 📂 Navigation Confirmation

In the sidebar under **📂 Navigation Menu**, confirm your theme appears:

> 💼 Labour Market Dynamics

---

### 🧪 Final Verification Checklist (After CSV Upload)

- ✅ App launches without error
- ✅ CSV file loads correctly (renamed according to country code, e.g., us_m_200_composite.csv)
- ✅ All expected columns present and correctly mapped to indicator functions
- ✅ Header displays: 🇺🇸 United States – 💼 Labour Market Dynamics
- ✅ No unresolved paths, missing configs, or import issues

📊 Insight Panels:

- ✅ Insight Use Cases are populated (e.g., Employment Trends, Unemployment Context)
- ✅ 📊 Macro Conditions Summary displays correctly
- ✅ 📈 Charts Tab shows correct visual renderings
- ✅ 🧾 Macro Signal Summary returns evaluated scoring and bias labels

⚠ Critical Validation Rule:

- All CSV column names must exactly match indicator_map_200.py keys.
- No deviations, extra columns, or misspellings permitted.

---

🧠 Congratulations — you’ve now created a default implementation of:

**💼 Labour Market Dynamics for the United States**

---

Advanced users may enhance the module with country-specific insights,
composite overlays, regime triggers, or tailored scoring logic.
🧠 Step 4: Advanced Configuration (Optional)
""")

# --- Step 4: Advanced Configuration (Optional) ---
with theme_tabs[3]:
    st.subheader("🧠 Advanced Configuration (Optional)")

    st.markdown("""
    This step is optional — but often essential.

    It allows you to curate country-specific enhancements that elevate your thematic
    modules beyond the defaults. Whether you’re adding unique indicators, adjusting
    scoring weightings, or embedding system-specific insights, **this is where
    structure meets strategy**.

    The goal isn’t complexity — it’s relevance.

    You’re not just adapting a template; you’re defining the way your system interprets
    context, and potentially how your AI tooling will respond downstream.

    Use this section to:
    - Add new indicators that matter in your national or thematic context
    - Refine signal logic or scoring alignment for greater diagnostic precision
    - Embed interpretations that support AI export and reflection workflows
    """)

    with st.expander("🧠 Why Curate Indicators and Insights?"):
        st.markdown("""
    At the heart of this system lies a foundational principle:
    **Context is not a supplement — it is the primary asset.**

    Whether you’re building a strategy, interrogating trends, or exporting observations
    for AI interpretation, what matters is not how much data you collect — but
    what meaning you choose to embed.

    Adding country-specific indicators or scoring logic isn’t just about tuning precision.
    It’s about **shaping the conditions for intelligence to emerge.**

    Each label, definition, and decision you set becomes part of a structured
    environment — not just powering visuals or summaries, but **conditioning how
    your tools interpret, reflect, and interact** with your view of the world.

    ---

    ### 🎯 Framing Signals, Not Just Data

    This framework treats indicators as signals with weight — economically, personally,
    strategically. Their structure shapes how inference flows through your system:

    - `why_it_matters` clarifies relevance — not universally, but to your context
    - `temporal_categorisation` tags systemic role — leading, lagging, coincident
    - `investment_action_importance` connects signal strength to macro or market logic
    - `personal_impact_importance` anchors insight to lived experience

    You’re not filling out metadata.
    You’re defining how meaning travels.

    ---

    ### 🧠 Context Before Questions

    AI is not embedded into this system — and that’s intentional.

    Instead, structure is built to travel: to a model, a conversation, or a strategic
    prompt — **with clarity, context, and coherence already defined**.

    This isn’t about asking better questions.
    It’s about **designing the conditions** in which better answers can emerge — regardless
    of the platform you choose.
    """)

    st.markdown("---")
    st.subheader("📘 Walkthrough: United States – Labour Market Dynamics")

    st.markdown("""
    To demonstrate how advanced configuration works in context, we’ll walk through the module:
    `200_💼_labour_market_dynamics.py` for the **United States**.

    This example applies the core principles of indicator curation, scoring logic, and insight
    tagging to real-world labour data — covering employment, unemployment,
    and participation trends.

    We’ll explore how:

    - Default templates are extended using locally relevant indicators
    - Signals are assigned structured metadata (e.g. `why_it_matters`, `temporal_categorisation`)
    - Scoring logic is applied to define interpretation flow
    - Visuals and summaries reflect curated insight logic

    This example serves as both **reference implementation** and **repeatable pattern** for
    expanding other country or thematic modules.
    """)

    st.markdown("---")
    st.subheader("🔍 Act 1: Expand the Signal — United States Labour Market Dynamics")

    with st.expander("🧠 Why Extend the Signal?"):
        st.markdown("""
    The default indicators establish a shared foundation. But depending on what matters to you —
    structurally, personally, or strategically — additional signals may
    help sharpen interpretation.

    We apply a simple filter:

    - Can the data be sourced reliably?
    - Does the signal contribute to understanding labour market dynamics?
    - Does it align with investment logic, economic structuring, or personal decision-making?

    Some users might want to explore where jobs are growing, or how sectoral
    resilience shifts over time.
    Others may watch jobless claims or full-time ratios as directional pressure on markets.
    This module doesn't replace deeper sources — but it can frame them, export them,
    or connect them into broader system context.
    """)

    with st.expander("📌 What We’re Adding — Structured, Not Excessive"):
        st.markdown("""
    Each indicator below has been **sourced from FRED**, with its purpose carefully considered.

    #### 🧱 Business Sector Employment (Monthly)
    Breaks down employment by sector — manufacturing, construction, financials, and more.
    - PAYEMS: `Total Nonfarm`
    - USPRIV: `Total Private`
    - USGOOD: `Goods-Producing`
    - USMINE: `Mining and Logging`
    - USCONS: `Construction`
    - MANEMP: `Manufacturing`
    - CES0800000001: `Private Service-Providing`
    - USTPU: `Trade Transportation and Utilities`
    - USINFO: `Information`
    - USFIRE: `Financial Activities`
    - USPBS: `Professional and Business Services`
    - USEHS: `Education and Health Services`
    - USLAH: `Leisure and Hospitality`
    - USSERV: `Other Services`
    - USGOVT: `Government`
    - CES9091000001: `Federal`
    - CES9092000001: `State Government`
    - CES9093000001: `Local Government`

    **Purpose:** Structural signal for sector momentum, labour dispersion, and cyclical exposure
    **Group:** `employment_composite`

    #### 🕓 Full-Time vs Part-Time Employment (Monthly)
    - Full-Time: `LNS12500000`
    - Part-Time: `LNS12600000`

    **Purpose:** Labour quality, underemployment tension, and wage structure implications
    **Group:** `employment_type`

    #### 📉 Jobless Claims (Weekly)
    - Initial Claims: `ICSA`
    - Continued Claims: `CCSA`

    **Purpose:** Directional pressure, stress signals, and timing cues — especially
    when high frequency matters
    **Group:** `jobless_claims`

    #### 💵 Wage Signals (Monthly)
    - Average Hourly Earnings — Total Private (`CES0500000003`)

    **Purpose:** Household income context, policy sensitivity, and contribution to
    inflation narratives
    **Group:** `wage_signals`

    These additions form a curated signal set — extending the module’s relevance across decision
    types, from macro positioning and market risk to personal financial planning
    or career strategy.
    """)

        st.markdown("---")
    st.subheader("🔍 Act 2: Extend the Framework — Implementing United States Labour Market Dynamics")

    with st.expander("🧠 Why Extend the Framework?"):
        st.markdown("""
    A single headline figure—like the unemployment rate—offers a limited view.
    To enable consistent framing across themes, we’ve added supporting inputs including sector-level
    employment, participation dynamics, wage indicators, and jobless claims.

    This act outlines the practical steps taken to build a structured thematic grouping within
    the **Economic Exploration** suite.
    The result: a multi-dimensional framework that supports signal interpretation and downstream
    module alignment.

    ### 🧩 Registry Metadata (Advanced)

    When extending the framework with new indicators, templates, or use cases, you may also update:

    `apps/registry/thematic_groupings.py`

    This file defines the **semantic registry layer** of the Economic Exploration system.
    It provides descriptive metadata used for:

    • theme documentation and registry browsing
    • indicator context and interpretive descriptions
    • AI-facing metadata bundles
    • structural alignment across the thematic framework

    Updating this file is **not required for the application to run**.

    However, it is recommended when:

    • formalising a new indicator within an existing theme
    • introducing a new template structure
    • adding a supported use case within the registry
    • providing richer contextual metadata for AI interpretation

    If an indicator is being used only for **local experimentation**, updating
    `economic_series_map.py` alone is typically sufficient.
    """)

    with st.expander("🛠️ What Was Done — From Registry to Runtime"):
        st.markdown("""
    Each addition is context-aware and integrated across system layers — registry, series mapping,
    templates, and source management — ensuring readiness for structured signal
    use and AI augmentation.

    ### ✅ Key Steps Completed

    **1. Reviewed Theme Definitions**
    • Selected: `200_labour_market_dynamics`
    • Use cases grouped by: Employment, Wage Signals, Jobless Claims
    → Reference: 📚 *View Theme Definitions & Indicator Registry*

    **2. Updated Economic Series Map**
    • Country: `"United States"` → Module: `"200_labour_market_dynamics"`
    • Entries mapped with:
     – FRED series codes (e.g., `PAYEMS`, `ICSA`)
     – Frequency, seasonal adjustment, unit type, value type, source URLs
    • Templates applied:
     – `employment_composite_template` for all series (monthly and weekly)

    **3. Validated CSV Templates**
    • Column headers aligned with registry entries
    • Split by frequency:
     – `us_m_200_composite.csv` (monthly)
     – `us_w_200_composite.csv` (weekly)
    • Stored under:
    ```plaintext
    /apps/data_sources/economic_data/us/200_employment_composite/
    ```

    **4. Created FRED Datalists**
    - Source validation and continuity maintained through FRED watchlists
    - Optional: User can subscribe or visit the project website to retrieve updated datasets.

    #### 🧾 Summary Snapshot

    | Component                    | Status                                                           |
    | ---------------------------- | -----------------------------------------------------------------|
    | Thematic Grouping            | `200_labour_market_dynamics`                                     |
    | Use Cases Covered            | Employment Sectors, Full/Part Time, Wages, Jobless Claims        |
    | Templates Used               | `employment_composite_template` (monthly + weekly)               |
    | Series Map Updated           | ✅ Yes — per-indicator entries with FRED alignment                |
    | Template Column Names        | ✅ Created to match `economic_series_map` keys                    |
    | Data Loaded & Saved          | ✅ `us_m_200_composite.csv`, `us_w_200_composite.csv`                                 |
    | Registry Integrity           | ✅ Confirmed via theme + indicator mappings                       |
    | Source Validity              | ✅ FRED verified with release schedule and units set              |
    | Modular Readiness            | ✅ Ready for AI export & Insight Flow                             |
    | 📚 Viewable Registry Entries | ✅ Available via *View Theme Definitions & Indicator Registry* tab|


    """)

    with st.expander("📦 Source Datalists — FRED Series (External Link)"):
        st.markdown("""
    Curated source datasets are available via official FRED watchlists to support transparency and
    continuity across modules:

    - [🇺🇸 US Labour Market — Monthly Indicators](https://fred.stlouisfed.org/graph/?g=EXAMPLE1)
    - [🇺🇸 US Labour Market — Weekly Indicators](https://fred.stlouisfed.org/graph/?g=EXAMPLE2)

    These Datalists include:
    - Sector employment series (e.g., Manufacturing, Government, Services)
    - Labour status breakdowns (e.g., Full-Time vs Part-Time)
    - Wage signals (e.g., Average Hourly Earnings)
    - High-frequency jobless claims (e.g., ICSA, CCSA)

    Users may review or subscribe to FRED to obtain these lists as needed.
    For broader sourcing principles and ingestion practices, refer to
    *Chapter 5: Building the Data Backbone* in the supplemental guide.
        """)

        st.markdown("---")
    st.subheader("🔍 Act 3: Finalise the Module — Activate Labour Market Dynamics")

    with st.expander("🧠 Use Case Definitions (`use_cases`)"):
        st.markdown("""
    Use cases represent the interpretive layer that ties indicator groups to decision-support logic.
    Each entry defines:

    - **Indicator Groupings**: Sets of related signals from the registry.
    - **Focus Categories**: Framing tags for AI export and insight routing.
    - **Contextual Descriptions**: Used across the sidebar and guide-linked outputs.

    These are derived from the **Thematic Grouping titles** and extended to support downstream
    logic in insights, visuals, and scoring overlays.

    ---

    **`Business Sector Employment Breakdown`** as a structured use case.

    ```python
    USE_CASES.update({
        "Business Sector Employment Breakdown": {
            "Indicators": [
                "Business Sector Employment Breakdown – Momentum",
                "Business Sector Employment Breakdown – Stress",
                "Business Sector Employment Breakdown – Summary"
            ],
            "Categories": ["Labour Market", "Employment Structure"],
            "Description": "Tracks sector hiring acceleration, dispersion and stress signals across industries."
        },

    """)

    with st.expander("🧭 Indicator Mapping (`indicator_map`)"):
        st.markdown("""
    The indicator map connects raw dataset columns to:

    - **Use Case Groupings** (e.g. *Business Sector Employment Breakdown*)
    - **Dashboard Routing**
    - **Scoring Summaries and Signal Outputs**

    This is a foundational module — the labels and logic defined here enable interpretability
    across the platform. These functions act as signal generators, translating recent indicator
    behaviour into context-aware summaries such as:

    - 📈 *Highest Momentum: Professional and Business Services*
    - 📉 *Largest Decline: Information Sector*

    ---

    ✅ **Status:** Labour Market Dynamics template CSVs loaded and signal logic defined.

    ➡️ **Next Step:** Register and activate signal functions for:

    - `us_m_200_composite.csv` — Monthly: Structural employment and wage data
    - `us_w_200_composite.csv` — Weekly: Jobless claims and high-frequency stress signals

    ---

    📦 **Example: Signal Logic and Mapping — Sector Momentum**

    ```python
    def sector_employment_momentum(df, period=None):
        if df is None or df.empty:
            return "Insufficient Data"
        try:
            recent = df.drop(columns=["date"], errors="ignore").dropna().tail(period or 3)
            momentum_scores = recent.diff().mean().sort_values(ascending=False)
            top_sector = momentum_scores.index[0]
            return f"Sector Momentum: {top_sector}"
        except Exception:
            return "Insufficient Data"


    # Sector momentum, stress, and average shifts
    BUSINESS_SECTOR_EMPLOYMENT_SIGNALS = {
        "Business Sector Employment Breakdown – Momentum": sector_employment_momentum,
    }

    # Merge: Universal + Local Indicator Maps
    ALL_INDICATOR_MAPS = {
        # --- Universal Shared Use Cases ---
        "Employment Trends": options_employment_signals_map,
        "Unemployment Context": options_unemployment_signals_map,
        "Labour Force Engagement": options_participation_signals_map,

        # --- Local Use Cases ---
        "Business Sector Employment Breakdown": BUSINESS_SECTOR_EMPLOYMENT_SIGNALS,
        "Full-Time vs Part-Time Employment": FULL_PART_TIME_EMPLOYMENT_SIGNALS,
        "Average Hourly Earnings": AVERAGE_HOURLY_EARNINGS_SIGNALS,
        "Jobless Claims": {
            **INITIAL_JOBLESS_CLAIMS_SIGNALS,
            **CONTINUED_JOBLESS_CLAIMS_SIGNALS
        }
    }

    def get_indicator_maps():
        return ALL_INDICATOR_MAPS
    ```

    💡 **Why this matters:**
    This modular registry architecture ensures each country-theme implementation can combine universal logic with localised signals — without disrupting app-level workflows or requiring downstream code changes.
    """)

    with st.expander("📊 Scoring & Labels (`scoring_weights_labels`)"):
        st.markdown("""
        Assigns interpretation weights and classification labels to mapped indicators.

        This module powers score overlays, alignment interpretation, and broader AI signal synthesis.
        By mapping indicator importance and directional thresholds, it helps translate raw signal trends
        into meaningful human-readable classifications (e.g., "⚠️ Labour Market Stress" or "✅ Resilience Building").

        ---

        ✅ **Status:** Universal and local scoring label dispatchers integrated.
        ➡️ **Next Step:** Extend label logic and weight mappings for:

        - Monthly employment signals (e.g. *Business Sector Breakdown*)
        - Wage growth and participation trends
        - Weekly high-frequency indicators (e.g. *Initial/Continued Jobless Claims*)

        ---

        📦 **Example: Dispatcher and Local Weight Map**

        ```python
        # scoring_weights_labels_200.py

        🏷 Local Scoring Label Functions (Per Use Case)

        def label_from_thresholds(ratio_val, strong, mixed, soft, stress):
            if ratio_val >= 0.85:
                return ("✅ " + strong[0], strong[1])
            if ratio_val >= 0.33:
                return ("⚠️ " + mixed[0], mixed[1])
            if ratio_val >= -0.2:
                return ("⚠️ " + soft[0], soft[1])
            return ("🚨 " + stress[0], stress[1])

        USE_CASE_SCORING_LABELS = {

            "Business Sector Employment Breakdown": lambda ratio_val: label_from_thresholds(
                ratio_val,
                ("Broad Sector Expansion", "Most industries are expanding with strong sector hiring breadth."),
                ("Mixed Sector Momentum", "Some sectors show strength while others are flat or contracting."),
                ("Flat or Uneven Sector Trends", "Minimal dispersion — sector trends are not aligned strongly."),
                ("Widespread Sector Weakness", "Majority of sectors showing contraction — possible macro fragility.")
            ),

        def get_alignment_score_label(alignment_ratio: float, use_case: str):
            if use_case in USE_CASE_SCORING_LABELS:
                return USE_CASE_SCORING_LABELS[use_case](alignment_ratio)
            return get_alignment_score_label_universal(alignment_ratio, use_case)

            🎯 Indicator Weights — Labour Market Dynamics (Local Extension)

            indicator_weights = {
            # Business Sector Employment Breakdown
            "Business Sector Employment Breakdown – Momentum": 3,
            "Business Sector Employment Breakdown – Stress": 2,
            "Business Sector Employment Breakdown – Summary": 1,

            # Full-Time vs Part-Time
            "Employment Type Balance": 3,
            "Part-Time Employment Stress": 2,

            # Wages
            "Wage Growth Trend": 3,

            # Jobless Claims
            "Initial Jobless Claims": 3,
            "Continued Jobless Claims": 2
        }

        # Merge universal weights
        indicator_weights.update(universal_indicator_weights)

        def get_indicator_weight(indicator_name: str) -> int:
            return indicator_weights.get(indicator_name, 1)
        ```

        💡 Why this matters:
        The scoring and weighting layer ensures the system doesn’t treat all indicators equally. It encodes priority,
        strength, and context relevance — forming the bedrock for composite interpretation and AI-enhanced alignment summaries.
        """)


    with st.expander("🧠 Insights Configuration (`insights`)"):
        st.markdown("""
        This module configures structured insight logic tied to each signal. These insights are used across:

        - **Summary Tables:** Auto-generated commentary below each chart group
        - **Macro Framing Tabs:** Dynamic panels that contextualise recent changes
        - **AI Export Overlays:** Embedded in generated reflections and strategy prompts

        These insights are not predictive or advisory — they translate observed patterns into
        **narrative framing** to support comparative and cyclical understanding. Each insight
        includes:

        - 📌 **Signal Outcome** (e.g. *Momentum Strengthening*)
        - 📘 **Insight Text** (e.g. "Weekly Economic Index shows rising momentum...")
        - ⚖️ **Bias Tag** (e.g. *Growth Supportive*, *Neutral*, *Contraction Warning*)

        This allows downstream apps and exports to align reasoning across markets, indicators, and
        user portfolios without requiring hardcoded logic.

        ---

        ✅ **Status:** Labour Market Dynamics insight templates are implemented.

        ➡️ **Next Step:** Continue refining context-aware summaries for:

        - Sector-level employment shifts
        - Real and nominal wage signals
        - Initial and continued jobless claim reversals

        ---

        📦 **Example: Insight Template for Initial Jobless Claims**

        ```python
        LOCAL_INSIGHTS = {
            "Initial Jobless Claims": {
                "Initial Claims Surge": {
                    "bias": "Contraction Warning",
                    "text": "Initial claims spiked — elevated job market stress emerging."
                },
                "Stable": {
                    "bias": "Neutral",
                    "text": "Initial jobless claims remain stable."
                },
                "Insufficient Data": {
                    "bias": "Neutral",
                    "text": "Insufficient data for initial claims signal."
                }
            },

        def generate_econ_insights(indicator: str, signal_result: str, timeframe: str, extra_value=None) -> tuple[str, str]:
            Returns (insight text, bias classification) for given indicator and signal.

            local_map = LOCAL_INSIGHTS.get(indicator, {})
            if signal_result in local_map:
                entry = local_map[signal_result]
                text_template = entry["text"]

                if "{sector}" in text_template and extra_value:
                    text_final = text_template.replace("{sector}", str(extra_value))
                elif "{value}" in text_template and extra_value is not None:
                    try:
                        text_final = text_template.replace("{value}", f"{extra_value:.2f}")
                    except:
                        text_final = text_template
                else:
                    text_final = text_template

                return text_final, entry["bias"]

            return generate_universal_econ_insights(indicator, signal_result, timeframe)
        ```

        💡 **Why this matters:**
        By codifying commentary logic here, you unlock consistent and scalable narrative generation across
        all modules — reducing noise while supporting human-AI collaborative framing.
        """)


    with st.expander("📈 Visual Configuration (`visual_config`)"):
        st.markdown("""
    The `visual_config` module defines how each **Insight Use Case** maps to its corresponding visual layout.

    - Use Case registry (`use_cases`)
    - Visual output rendering (`visual_config`)

    ---

    ### 🔧 Visual Configuration Role

    - Each Use Case triggers its assigned chart logic via `render_all_charts_local()`.
    - Charts are dispatched into visual sections and sub-tabs aligned with user navigation.
    - Helper functions (`plot_*`) handle Plotly figure generation.
    - `display_chart_with_fallback()` ensures stable Streamlit key management.

    This structure guarantees:

    - ✅ **Alignment:** Between Use Case selection, data slices, visual output,
    and AI overlays
    - ✅ **Flexibility:** Country-level extensions remain cleanly decoupled
    - ✅ **Scalability:** Additional Use Cases or charts can be integrated without
    modifying core data ingestion

    ---

    ### 📦 Example Use Case Mapping — *Jobless Claims*

    | Component | Value |
    | --------- | ----- |
    | **Insight Use Case** | `Jobless Claims` |
    | **Indicators** | `Initial Jobless Claims`, `Continued Jobless Claims` |
    | **Categories** | `High-Frequency Stress`, `Labour Market Weakness` |
    | **Description** | *Real-time unemployment stress signals derived from weekly claims data.* |
    | **Visual Layout** | Combined dual-line chart |

    ---

    **Example: 📈 Jobless Claims Visual Logic**

    Each chart helper remains isolated, ensuring clean reusable structure.

    ```python
    def plot_jobless_claims(df):
    Render a combined line chart for Initial and Continued Jobless Claims.
    This chart helper is called directly by the visual dispatcher
    for the relevant use case.
    df = df.copy()
    if "date" not in df.columns or \

       "Initial Jobless Claims" not in df.columns or \

       "Continued Jobless Claims" not in df.columns:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Initial Jobless Claims"],
        mode="lines+markers",
        name="Initial Claims",
        line={"color": "#1f77b4"}
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["Continued Jobless Claims"],
        mode="lines+markers",
        name="Continued Claims",
        line={"color": "#ff7f0e"}
    ))

    fig.update_layout(
        title="📉 Jobless Claims Overview",
        xaxis_title="Date",
        yaxis_title="Number of Claims",
        template="plotly_white",
        height=460
    )
    return fig
    ```

    The dispatcher then calls this helper dynamically:

    ```python
    def render_all_charts_local(selected_use_case, tab_mapping, df_map):
    Visual dispatcher that routes chart rendering based on selected use case.
    Period slicing is controlled per tab dynamically.
    Universal charts are always dispatched first (not shown here),
    followed by local extensions.

    period_options = [3, 6, 12, 24, 60, None]  # Period slicing options for sub-tabs
    composite_tabs = list(tab_mapping.keys())[:6]

    for tab, data_slice in tab_mapping.items():
        with tab:
            df = data_slice.reset_index()

            # --- Local Extension: Jobless Claims Use Case ---
            if selected_use_case == "Jobless Claims":
                current_periods = next((p for t, p in zip(
                composite_tabs, period_options) if t == tab), None)
                df_extended_full = df_map["df_extended"].reset_index()
                df_extended = df_extended_full.tail(
                current_periods) if current_periods else df_extended_full

                display_chart_with_fallback(
                    plot_jobless_claims(df_extended),
                    label=f"{tab}_JoblessClaims"
                )
    ```

    💡 **Why this matters:**
    Visual Configuration acts only on how validated data slices are presented visually.
    The intelligence remains driven by upstream signal logic (indicator_map and insights),
    but is rendered with clean UI control and full AI export compatibility.
    """)

    with st.expander("🔀 Routing (`routing`)"):
        st.markdown("""
    The `routing` module connects each **indicator signal** to its correct data slice.

    This ensures:
    - Monthly indicators pull from `df_secondary`
    - Weekly indicators pull from `df_extended`
    - Fully dynamic dispatcher for insights, scoring, and AI overlays.

    ---

    ### Example: routing_200.py

    ```python
    SECONDARY_DATA_INDICATORS = {
        "Business Sector Employment Breakdown – Momentum",
        "Business Sector Employment Breakdown – Stress",
        "Business Sector Employment Breakdown – Summary",
        "Employment Type Balance",
        "Part-Time Employment Stress",
        "Employment Quality Shift",
        "Wage Growth Trend"
    }

    EXTENDED_DATA_INDICATORS = {
        "Initial Jobless Claims",
        "Continued Jobless Claims"
    }

    def get_indicator_input(indicator_name: str, df_dict: dict) -> pd.DataFrame | None:
        Direct string-matched routing for local labour market indicators.
        Fully consistent across signal maps and insight maps.

        if indicator_name in SECONDARY_DATA_INDICATORS:
            return df_dict.get("df_secondary_slice")

        if indicator_name in EXTENDED_DATA_INDICATORS:
            return df_dict.get("df_extended_slice")

        # Fallback for any universal indicators (e.g. Employment Trends, Unemployment Context etc)
        return get_indicator_input_universal(indicator_name, df_dict)
    ```

    💡 **Why this matters:**

    - ✅ Clean separation between data sources
    - ✅ Enables flexible multi-frequency models
    - ✅ Supports automated expansion for future indicators

    """)

    with st.expander("🧩 Module Runtime Integration (`200_💼_labour_market_dynamics.py`)"):
        st.markdown("""
    Integrates all upstream module logic and dataset configurations into the live Streamlit app.

    Includes dataset registration, use case selection, and dashboard rendering.

    Configuration is strictly tied to this module and is required for it to function correctly with the data prepared in **Act 2**.

    ---

    ### 🧩 Module-Level Updates Required

    | Section                  | Action                                                                 |
    |--------------------------|------------------------------------------------------------------------|
    | `📊 THEME CONFIGURATION` | Add new data source path: `COMPOSITE_FOLDER = "200_employment_composite"` |
    |                          | Ensures access to weekly + composite indicators in addition to monthly core. |
    | `DATASET_REGISTRY`       | Register:                                                               |
    |                          | &nbsp;&nbsp;– `df_secondary` for monthly composites (e.g. wages)        |
    |                          | &nbsp;&nbsp;– `df_extended` for weekly indicators (e.g. jobless claims) |
    | `df_dict`                | Uncomment to enable routing of these dataframes within the app.        |
    | `df_map`                 | Add these datasets for chart rendering and dynamic visual dispatch.     |

    ---

    #### 🗂 Dataset Registry

    Ensure the following `DATASET_REGISTRY` entries are present:

    ```python
    DATASET_REGISTRY = {
    "df_primary": {
        "label": "📄 Employment",
        "file": f"{COUNTRY_CODE}_m_{THEME_ID}_structural.csv",
        "folder": STRUCTURAL_FOLDER,
        "cleaner": clean_economic_data,
        "show_in_underlying_data": True,
        "plot": True,
        "create_slice": True,
        "frequency": "monthly"
    },
    "df_secondary": {
        "label": "📄 Employment Composite",
        "file": f"{COUNTRY_CODE}_m_{THEME_ID}_composite.csv",
        "folder": COMPOSITE_FOLDER,
        "cleaner": clean_economic_data,
        "show_in_underlying_data": True,
        "plot": True,
        "create_slice": True
    },
    "df_extended": {
        "label": "📄 Employment Composite",
        "file": f"{COUNTRY_CODE}_w_{THEME_ID}_composite.csv",
        "folder": COMPOSITE_FOLDER,
        "cleaner": clean_economic_data,
        "show_in_underlying_data": True,
        "plot": True,
        "create_slice": True
    }
    ```

    #### 🔄 Routing Dictionary (df_dict)

    Ensure the following block is active (uncommented):

    ```python
    # --- Routing Dictionary ---
    df_dict = {
        "df_primary_slice": df_primary_slice,
        "df_full": df_primary,
        "df_secondary_slice": df_secondary_slice,
        "df_extended_slice": df_extended_slice
    }
    ```

    #### 📈 Chart Rendering Map (df_map)

    Ensure visuals are linked correctly across all datasets:

    ```python
    df_map = {
        "df_primary": df_primary,
        "df_secondary": df_secondary,
        "df_extended": df_extended
    }
    ```
""")

    with st.expander("✅ Validate & Run Final Checks"):
        st.markdown("""

    ### 🔎 Validation Checklist

    - [x] **Use Cases Defined**: `Business Sector Employment Breakdown, Full-Time vs Part-Time Employment, Average Hourly Earnings, Jobless Claims` present in sidebar and structured.
    - [x] **Indicators Mapped**: All columns in `us_m_200_composite.csv` and `us_w_200_composite.csv` are present in `indicator_map.py`.
    - [x] **Insights Enabled**: Summary commentary functions mapped and returning correct bias labels.
    - [x] **Visuals Assigned**: All datasets flagged with `plot=True` in `DATASET_REGISTRY` correctly routed to visuals.
    - [x] **Scoring Labels Applied**: Weighting files updated and bias mappings assigned.
    - [x] **Routing Active**: Local `routing.py` file correctly maps indicators to dataframes.
    - [x] **Main Module Synced**: Main module `200_💼_labour_market_dynamics.py` reflects updated theme registry and paths.

    ---



    ### 🚀 Next Steps

    Launch the main dashboard to verify full integration of your theme module:

    🖥️ **Restart Launcher**
    - Close any running instance of:
      🚀 *Welcome to Insight Launcher: 🌍 Economic Exploration*

    - Reopen via:
      🚀 *Welcome to Financial Insight Tools*

    🗺 **Region Selection**
    - **Region:** Americas
    - **Sub-Region:** North America
    - **Country:** United States

    You should see:

    > 🇺🇸 **United States – Insight Launcher: Economic Exploration**

    ---

    ### 📂 Navigation Confirmation

    Check the left sidebar Navigation Menu for:

    > **💼 Labour Market Dynamics**

    ---

    ### System-Level Full Verification

    Post Integration Test:

    - ✅ Restart Insight Launcher → Select Country → Enter Economic Exploration
    - ✅ Sidebar Navigation shows 💼 Labour Market Dynamics available
    - ✅ All charts, scoring, and insight evaluations execute cleanly

    ---

    ### 🔧 Structural Ruleset (No Deviation Allowed)

    - ✅ **Strict String Matching:**
    Use Case Names → Indicator Names → CSV Headers → Insight Labels → Visual Config → Routing Keys

    - ✅ **Exact Column Alignment:**
    Every column in CSV must match an indicator function.

    - ✅ **Insight Map Synchronisation:**
    Every signal output must match insight mapping keys, using pure strings only.

    - ✅ **Routing Correctness:**
    Each indicator mapped to correct data slice via routing file.

    - ✅ **Visual Dependency Structure:**
    Visual configs depend strictly on use cases defined.

    - ✅ **Registry Integrity:**

        - economic_series_map.py correctly populated for full AI persona access
        - thematic_groupings.py updated with country → theme integration

    - ✅ **Docstring Compliance:**
        All modules carry full docstrings defining scope for both AI and user guidance.

    """)

# -------------------------------------------------------------------------------------------------
# Tab 3: View Theme Definitions & Indicator Registry
# -------------------------------------------------------------------------------------------------
with tabs[2]:
    st.header("📚 View Theme Definitions & Indicator Registry")
    st.caption("Browse high-level themes, inspect country-specific indicator maps, "
    "and validate registry structure.")

    with st.expander("ℹ️ Help: Thematic Registry Explorer"):
        content = load_markdown_file(HELP_APP_MD)
        if content:
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.warning("Missing: docs/help_thematic_registry_explorer.md")

    sub_tabs = st.tabs(["📑 Thematic Groupings", "📊 Indicator Map", "🧪 Audit Panel"])


    # --- Sub-tab 0: Thematic Groupings ---
    with sub_tabs[0]:
        st.subheader("📑 Thematic Groupings Overview")
        st.markdown("*Browse high-level theme definitions and individual indicator roles \
        within each grouping.*")

        # --- Flatten Theme Overview ---
        theme_data = []
        for theme_id, theme in THEMATIC_GROUPS.items():
            title = theme.get("theme_title", "")
            intro = theme.get("theme_introduction", "")
            templates = ", ".join(theme.get("template", {}).keys())
            use_cases = [entry.get(
            "Use Case", "") for entry in theme.get("memberships", {}).values()]
            theme_data.append({
                "Theme ID": theme_id,
                "Theme Title": title,
                "Templates": templates,
                "Use Cases": ", ".join(use_cases),
                "Introduction": intro[:150] + "..." if len(intro) > 150 else intro
            })
        theme_df = pd.DataFrame(theme_data)

        st.markdown("#### 📘 High-Level Theme Overview")
        gb = GridOptionsBuilder.from_dataframe(theme_df)
        gb.configure_default_column(wrapText=True, autoHeight=True, filter=True, sortable=True,
        resizable=True)
        gb.configure_column("Theme ID", pinned="left", width=120)
        gb.configure_column("Theme Title", width=200)
        gb.configure_column("Templates", width=200)
        gb.configure_column("Use Cases", width=240)
        gb.configure_column("Introduction", width=300)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()

        AgGrid(theme_df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True,
        columns_auto_size_mode='FIT_CONTENTS')

        # --- Theme Selector for Membership Drilldown ---
        def sort_key(k):
            """
            Extracts the numeric prefix from a theme ID string to support sorted display.

            Args:
                k (str): Theme ID string in the format '100_theme_name', '200_theme_name', etc.

            Returns:
                int | float: Integer prefix if successfully parsed; infinity if parsing fails.

            Notes:
                This is used to ensure the thematic dropdown and tables follow an intuitive,
                numerically ordered sequence aligned with internal grouping logic.
            """
            try:
                return int(k.split("_")[0])
            except ValueError:
                return float("inf")

        sorted_theme_options = sorted(THEMATIC_GROUPS.keys(), key=sort_key)

        st.divider()
        selected_theme = st.selectbox("📂 Explore Membership of a Theme",
        options=sorted_theme_options, key="theme_selector")
        st.markdown(f"#### 🧩 Membership Details for **{selected_theme}**")

        selected_members = THEMATIC_GROUPS[selected_theme].get("memberships", {})
        member_data = []
        for code, entry in selected_members.items():
            member_data.append({
                "Indicator Code": code,
                "Use Case": entry.get("Use Case", ""),
                "Title": entry.get("title", ""),
                "Overview": entry.get(
                "overview", "")[:150] + "..." if len(entry.get(
                "overview", "")) > 150 else entry.get("overview", ""),
                "Investment Impact": entry.get("investment_action_importance", ""),
                "Personal Impact": entry.get("personal_impact_importance", ""),
                "Recommended Periods": ", ".join(entry.get("recommended_time_periods", [])),
            })
        membership_df = pd.DataFrame(member_data)

        st.markdown("##### 🔎 Filter Membership Table")
        col1, col2, col3 = st.columns(3)
        use_case_filter = col1.multiselect("🧠 Use Case",
        sorted(membership_df["Use Case"].dropna().unique()), key="membership_use_case")
        invest_impact_filter = col2.multiselect("📊 Investment Impact",
        sorted(membership_df["Investment Impact"].dropna().unique()), key="membership_investment")
        personal_impact_filter = col3.multiselect("👤 Personal Impact",
        sorted(membership_df["Personal Impact"].dropna().unique()), key="membership_personal")

        filtered_membership_df = membership_df.copy()
        if use_case_filter:
            filtered_membership_df = filtered_membership_df[filtered_membership_df[
            "Use Case"].isin(use_case_filter)]
        if invest_impact_filter:
            filtered_membership_df = filtered_membership_df[filtered_membership_df[
            "Investment Impact"].isin(invest_impact_filter)]
        if personal_impact_filter:
            filtered_membership_df = filtered_membership_df[filtered_membership_df[
            "Personal Impact"].isin(personal_impact_filter)]

        gb = GridOptionsBuilder.from_dataframe(filtered_membership_df)
        gb.configure_default_column(wrapText=True, autoHeight=True, filter=True,
        sortable=True, resizable=True)
        gb.configure_column("Indicator Code", pinned="left", width=120)
        gb.configure_column("Use Case", width=160)
        gb.configure_column("Title", width=200)
        gb.configure_column("Overview", width=300)
        gb.configure_column("Investment Impact", width=100)
        gb.configure_column("Personal Impact", width=100)
        gb.configure_column("Recommended Periods", width=160)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()

        AgGrid(filtered_membership_df, gridOptions=grid_options, height=400,
        fit_columns_on_grid_load=True, columns_auto_size_mode='FIT_CONTENTS')

    # --- Sub-tab 1: Indicator Map ---
    with sub_tabs[1]:
        st.subheader("📊 Indicator Map Explorer")
        st.markdown("*Query indicators by country, theme, template, or source.*")

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
                            "Use Case": entry.get("Use Case", ""),
                            "Display Name": entry.get("ui_display_name", entry.get("name", "")),
                            "Unit": entry.get("unit_type", ""),
                            "Frequency": entry.get("frequency", ""),
                            "Seasonal Adj.": entry.get("seasonal_adjustment", ""),
                            "Value Type": entry.get("value_type", ""),
                            "Source": entry.get("source", ""),
                            "Source URL": entry.get("source_url", ""),
                            "Release (Prelim)": entry.get("release_schedule: preliminary", ""),
                            "Release (Second)": entry.get("release_schedule: second", ""),
                            "Release (Final)": entry.get("release_schedule: final", ""),
                            "Note": entry.get("note", "")
                        })

        indicator_df = pd.DataFrame(indicator_records)

        st.markdown("##### 🔎 Filter Options")
        col1, col2, col3 = st.columns(3)
        country_filter = col1.multiselect("🌍 Country", sorted(indicator_df["Country"].unique()),
        key="indmap_country")
        theme_filter = col2.multiselect("🧩 Theme", sorted(indicator_df["Theme"].unique()),
        key="indmap_theme")
        use_case_filter = col3.multiselect("🧠 Use Case",
        sorted(indicator_df["Use Case"].dropna().unique()), key="indmap_use_case")
        source_filter = st.text_input("📡 Source Contains (e.g., FRED, ECB)", "",
        key="indmap_source")

        filtered_df = indicator_df.copy()
        if country_filter:
            filtered_df = filtered_df[filtered_df["Country"].isin(country_filter)]
        if theme_filter:
            filtered_df = filtered_df[filtered_df["Theme"].isin(theme_filter)]
        if use_case_filter:
            filtered_df = filtered_df[filtered_df["Use Case"].isin(use_case_filter)]
        if source_filter:
            filtered_df = filtered_df[filtered_df["Source"].str.contains(
            source_filter, case=False, na=False)]

        st.markdown("#### 📋 Filtered Indicator Table")
        col_toggle, release_toggle = st.columns(2)
        show_all = col_toggle.toggle("🔁 Show All Columns", value=False, key="indmap_toggle_all")
        show_schedule = release_toggle.toggle("📅 Include Release Schedule",
        value=False, key="indmap_toggle_release")

        display_cols = ["Country", "Theme", "Use Case", "Source", "Source URL", "Note"]
        if show_schedule:
            display_cols += ["Release (Prelim)", "Release (Second)", "Release (Final)"]

        table_df = filtered_df if show_all else filtered_df[display_cols].copy()

        gb = GridOptionsBuilder.from_dataframe(table_df)
        gb.configure_default_column(wrapText=True, autoHeight=True, filter=True,
        sortable=True, resizable=True)

        if "Country" in table_df.columns:
            gb.configure_column("Country", pinned="left", width=100)
        if "Theme" in table_df.columns:
            gb.configure_column("Theme", width=160)
        if "Template" in table_df.columns:
            gb.configure_column("Template", width=160)
        if "Use Case" in table_df.columns:
            gb.configure_column("Use Case", width=180)
        if "Source" in table_df.columns:
            gb.configure_column("Source", width=200)

        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()

        AgGrid(table_df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True,
        columns_auto_size_mode='FIT_CONTENTS')

    # --- Sub-tab 2: Audit Panel ---
    with sub_tabs[2]:
        st.subheader("🧪 Thematic Audit Panel")
        st.markdown("This audit validates the consistency and structural integrity of defined "
        "theme groupings and mapped indicators across the system.")

        st.markdown("#### 1️⃣ Duplicate Indicator Codes")
        indicator_seen = set()
        indicator_duplicates = set()
        for country, themes in ECONOMIC_SERIES_MAP.items():
            for theme, templates in themes.items():
                for template, indicators in templates.items():
                    for code in indicators.keys():
                        if code in indicator_seen:
                            indicator_duplicates.add(code)
                        indicator_seen.add(code)

        if indicator_duplicates:
            st.warning(
            f"Duplicate indicator codes found: `{', '.join(sorted(indicator_duplicates))}`")
        else:
            st.success("✅ No duplicate indicator codes found across countries.")

        st.markdown("#### 2️⃣ Unused or Orphaned Themes")
        all_used_themes = set()
        for country_data in ECONOMIC_SERIES_MAP.values():
            all_used_themes.update(country_data.keys())

        all_defined_themes = set(THEMATIC_GROUPS.keys())
        unused_themes = sorted(all_defined_themes - all_used_themes)

        if unused_themes:
            st.warning(f"Themes defined but not used in any country: `{', '.join(unused_themes)}`")
            st.caption("Note: Not all themes are expected to be implemented across all countries.")
        else:
            st.success("✅ All defined themes are currently in use.")

        st.markdown("#### 3️⃣ Templates Used but Not Declared in Theme Groupings")
        undeclared_templates = []
        for country, themes in ECONOMIC_SERIES_MAP.items():
            for theme_id, templates in themes.items():
                declared_templates = set(THEMATIC_GROUPS.get(theme_id, {}).get("template",
                {}).keys())
                for template_id in templates.keys():
                    if template_id not in declared_templates:
                        undeclared_templates.append({
                            "Country": country,
                            "Theme ID": theme_id,
                            "Template": template_id
                        })

        if undeclared_templates:
            st.warning("Templates found in the indicator map that are not declared in the \
            thematic groupings.")
            AgGrid(pd.DataFrame(undeclared_templates), height=300)
        else:
            st.success("✅ All templates used in the indicator map are properly declared.")

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()
st.caption("© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — "
            "No trading, investment, or policy advice provided.")
