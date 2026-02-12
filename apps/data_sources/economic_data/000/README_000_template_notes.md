# 📄 Template Notes — Economic Data CSV Inputs

Folder 000 contains **template CSV files** used to structure economic indicator inputs
for each country and thematic grouping within the Economic Exploration module of
the Financial Insight Tools system.

---

## 🎯 Purpose

These templates serve as **scaffolded inputs** for users who are adding new themes or indicators
to a country module. They ensure consistent formatting, reliable charting, and accurate
integration with the decision-support system and AI augmentation workflows.

---

## 📂 Files Included

| File Name            | Purpose                                                                          |
|---------------------|-----------------------------------------------------------------------------------|
| `country-2digit-code_q_100_structural.csv` | Quarterly CSV data input template for Theme 100 – *Economic Growth & Stability*  |
| `country-2digit-code_m_200_structural.csv` | Monthly CSV data input template for Theme 200 – *Labour Market Dynamics*         |

---

## 🛠 Required Formatting

To ensure system compatibility and avoid downstream errors, the following requirements must be met:

### 🔹 Column Headers

All CSVs must include the following structure:

- `date` — ISO format `YYYY-MM-DD` (Quarter-end for quarterly data; Month-end for monthly)
- One column per indicator, with exact title matching the **`"name":`** field in `economic_series_map.py`.

Example:

```csv
date,Real GDP (Level),Nominal GDP,Real Personal Consumption
2018-03-31,19500.2,21003.1,13312.4
2018-06-30,19675.4,21245.0,13422.6
...
