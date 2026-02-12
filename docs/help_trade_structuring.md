
# 🛠️ Trade Structuring & Risk Planning — Help

This module allows users to construct structured trade setups — from single-leg instruments like shares or CFDs to more complex multi-leg spreads or mean-reversion pairs. It draws together diagnostic insights from other modules (volatility, timing, trends) into a final planning layer.

---

## ℹ️ What Does This App Do?

The Trade Structuring & Risk Planning module provides a hands-on interface to configure trades using real asset data. Users define trade type, select assets, determine direction, set price targets and stops, and review structural sizing logic. Outputs are added to a session-based dashboard for download or future evaluation.

---

## 💡 Use Case Walkthrough

**Example:** You’ve uploaded a trade journal and wish to structure a new **Pairs Trade** using user-defined preloaded assets.

1. **Step 1:** Select `Pairs Trading (Mean Reversion)` from the trade type menu.
2. **Step 2:** Choose your **Long** and **Short** legs from your user-preloaded categories.
3. **Step 3:** Pull insights from other modules (e.g. price divergence from Spread Analysis or timing alignment from Technical Indicators).
4. **Step 4:** Enter stop-loss, take-profit, capital allocation, and leverage assumptions.
5. **Step 5:** Add trade to the dashboard for further review or export.

This structured flow enables real-world preparation for execution — aligning trade logic with risk limits and sizing principles.

---

## 🧭 Key Concepts

- **Trade Type:** Affects available calculators and structuring logic (e.g., leverage vs non-leverage).
- **Long / Short Legs:** Required for Pairs or Multi-Leg strategies.
- **Reward-to-Risk Ratio:** Used to calculate target distance if not manually specified.
- **Allocated Capital & Risk %:** Determines position size and risk tiering.
- **Dashboard:** Aggregates all configured trades for download, review, or export to broker systems.

---

## ⚠️ Advisory Framing

This module is **non-advisory and structural only**. It does not estimate fees, execution costs, or margin rates specific to your broker. Outputs should be validated using your platform’s execution parameters.

- Supports decision planning
- Does not replace live pricing or broker systems
- Reflects user inputs only

---

## ✅ Output Options

- Real-time trade preview with calculator feedback
- Editable trade dashboard (session state)
- CSV download of structured trades for record keeping or onward processing
