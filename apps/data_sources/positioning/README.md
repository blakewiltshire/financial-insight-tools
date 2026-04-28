# Positioning & Crowding — Adding New Assets

This module supports optional expansion through user-supplied positioning datasets.

Assets are based on:

- Weekly CFTC Commitment of Traders (COT) data
- Supplementary market price data

This module is optional and does not affect core Financial Insight Tools functionality.

---

### Step 1 — Create Asset File

Add a new CSV inside:

apps/data_sources/positioning/

Example:

cad_positioning.csv

---

### Step 2 — Required Columns

Your dataset must follow this structure:

date,market_name,leveraged_long,leveraged_short,change_long,change_short,open_interest_long_pct,open_interest_short_pct

---

### Step 3 — Source COT Data

Download from:

U.S. Commodity Futures Trading Commission
→ Commitment of Traders → Historical Compressed

Use:

- Traders in Financial Futures (TFF)
- Disaggregated Futures Reports

---

### Step 4 — Transform Columns

Map raw fields:

Traders in Financial Futures (TFF)

Report_Date_as_MM_DD_YYYY → date
Market_and_Exchange_Names → market_name
Lev_Money_Positions_Long_All → leveraged_long
Lev_Money_Positions_Short_All → leveraged_short
Change_in_Lev_Money_Long_All → change_long
Change_in_Lev_Money_Short_All → change_short
Pct_of_OI_Lev_Money_Long_All → open_interest_long_pct
Pct_of_OI_Lev_Money_Short_All → open_interest_short_pct

Disaggregated Futures Only Reports

Report_Date_as_MM_DD_YYYY → date
Market_and_Exchange_Names → market_name
M_Money_Positions_Long_All → leveraged_long
M_Money_Positions_Short_All → leveraged_short
Change_in_M_Money_Long_All → change_long
Change_in_M_Money_Short_All → change_short
Pct_of_OI_M_Money_Long_All → open_interest_long_pct
Pct_of_OI_M_Money_Short_All → open_interest_short_pct

---

### Step 5 — Clean Naming

Standardise:

AUSTRALIAN DOLLAR → Australian Dollar
USD INDEX → USD DXY
UST 10Y NOTE → US 10Y Note

---

### Step 6 — Add Weekly Market Price Data

Download weekly historical price data for the asset.

Suggested workflow:

1. Go to Investing.com
2. Find the relevant asset, currency pair, commodity, yield, index, or futures market
3. Open Historical Data
4. Set frequency to Weekly
5. Set start date to 2020-01-01
6. Sort oldest first
7. Download the dataset
8. Add the weekly price series to:

cots_assets_default.csv

The column name used here must match the asset_column value in processing_positioning.py.

All dates must be formatted using the standard international format: YYYY-MM-DD

This avoids regional formatting conflicts (for example DD/MM/YYYY vs MM/DD/YYYY)
and ensures charts, overlays, and positioning calculations render correctly.

---

### Step 7 — Register the Asset in processing_positioning.py

Add the new market to POSITIONING_MARKET_MAP.

Example:

"cad_positioning": {
    "label": "CAD Positioning",
    "positioning_file": "cad_positioning.csv",
    "asset_column": "cad_usd",
    "market_price_label": "CAD/USD",
},

The asset_column must match the column added to cots_assets_default.csv.

Both files must align:

- cots_assets_default.csv
- processing_positioning.py

---

### Step 8 — Validate

Confirm:

- the positioning CSV exists
- the asset column exists in cots_assets_default.csv
- the slug exists in POSITIONING_MARKET_MAP
- the market appears in the Positioning & Crowding dropdown
- the positioning chart and market overlay both render

If data is incomplete, the module may still run but some visuals may be hidden.

---

Financial Insight Tools by Blake Wiltshire
© Blake Media Ltd.
