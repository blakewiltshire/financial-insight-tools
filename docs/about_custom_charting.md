
# 📖 About Custom Charting

The charting system used across the Financial Insight Tools suite supports **modular extension** by design. Each module—such as *Price Action & Confirmation*—includes a dedicated charting file where custom visualisations can be added using a consistent, platinum-grade structure.

---

## 🧱 Charting Architecture

Each charting function:
- Is stored in a shared file (e.g. `charting_price_action.py`)
- Includes a structured docstring and header:
  - `Function:` Name of the chart function
  - `Purpose:` What the chart shows
  - `Use Case:` Thematically linked decision-support objective
- Can be referenced conditionally in the main Streamlit dashboard (e.g. `04_📊_Price_Action_and_Trend_Confirmation.py`)

---

## 🛠 How to Add a Custom Chart

1. **Identify the Use Case:**
   - What decision or pattern are you supporting?
   - Examples: "Volatility Swing Bands", "Liquidity Zones", "Impulse Reversals"

2. **Add Indicators (if needed):**
   - Extend the appropriate indicator map in `indicators_price_action.py`

3. **Create the Chart Function:**
   - Use the charting template (available in `template_charting_function.py`)
   - Define inputs, logic, and visual layout
   - Place the function inside `charting_price_action.py`

4. **Link to Dashboard:**
   - Reference the new chart in the corresponding module's page logic using `st.plotly_chart(...)`

---

## ✅ Best Practice

- Keep all chart logic modular and self-contained
- Use descriptive names and clear axis titles
- Avoid duplicating logic—reuse helper functions like `get_y_axis_scale()`
- Stick to the colour and layout conventions (e.g. `plotly_white`, dual axes)

---

## 🧩 Related Files

- `charting_price_action.py` — Custom visualisation logic
- `indicators_price_action.py` — Toggle options for charts
- `definitions_price_action.py` — Use case descriptors
- `04_📊_Price_Action_and_Trend_Confirmation.py` — Dashboard logic

---

This system empowers you to extend insight generation visually—whether you're enhancing a strategy, validating signals, or preparing export-ready views.
