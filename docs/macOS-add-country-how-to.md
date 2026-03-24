# HOW-TO: Add a New Country to Economic Exploration

This guide explains how to add a new country (e.g. **China**) to the Economic Exploration dashboard.

---

## 1️⃣ Prepare the Country Directory

Create the new directory under `economic_exploration/`:

```bash
mkdir economic_exploration/china

## 2️⃣ Copy the Streamlit Config
From /templates/, copy the .streamlit directory:

```bash
cp -r templates/.streamlit economic_exploration/china/

This clears the sidebar and enables custom navigation.

## 3️⃣ Configure config.toml
Ensure the .streamlit/config.toml file looks like this:

[theme]
base = "light"

[server]
headless = true

[client]
showSidebarNavigation = false

## 4️⃣ Update Shared Metadata
constants/regions.py
Add or uncomment:

"China": (35.8617, 104.1954),

constants/emoji.py
Ensure this exists:

"China": "🇨🇳",

## 5️⃣ Copy the App File
From templates/, copy the generic app.py:

```bash
cp templates/app.py economic_exploration/china/app.py


Update these values:

COUNTRY_NAME = "China"
THEME = "insight_launcher"

Replace any remaining "Template" text with "China".

## 6️⃣ Add Pages and Indicators
Copy thematic groupings and indicator files:

```bash
cp templates/pages/100_📈_economic_growth_stability.py economic_exploration/china/pages/
cp templates/pages/101_gdp_growth_rate.py economic_exploration/china/pages/

Update each file's COUNTRY = "China" value.

## 7️⃣ Review and Test
Run your app:

```bash
streamlit run economic_exploration/china/app.py

Verify:

- Sidebar works correctly
- Images and icons load
- Thematic pages link correctly
- No template placeholders remain

## 8️⃣ Repeat for New Countries
Follow the same steps for each new country you add.
