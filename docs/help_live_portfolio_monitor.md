# ℹ️ Help: How to Interpret Live Portfolio Monitoring

This module evaluates the structure and risk composition of your **currently active positions**, offering real-time diagnostics for exposure, leverage, and return asymmetry.

It does not assess future strategy or offer performance forecasts. Instead, it applies rule-based calculations to surface key insights about your **present portfolio state**.

---

**Key Concepts:**

- **Leverage-Adjusted Value:** Actual position size multiplied by leverage — reflects true capital exposure.
- **Unrealised P&L:** The floating profit or loss on each trade, not yet locked in.
- **Percent of Portfolio:** Share of account capital allocated to each position, adjusted for leverage.
- **Risk Tiering:** Classifies positions by relative size and risk-weight to highlight concentration.

---

**Example:**
You upload a portfolio of 12 active positions.  
With capital set at $100,000 and leverage applied:

- 2 positions exceed 25% exposure threshold (flagged)
- 4 are classified as “Moderate Risk” (10–15% of capital)
- Sector exposure shows 40% in Technology

**You receive:**
- Exposure tables (Sector, Country, Strategy)
- Risk diagnostics (flags, tier classifications)
- Position table (sortable, colour-coded)
- Validator feedback for structural issues (e.g., fallback leverage, missing data)

---

**Use Case:**
This module is best used to:

- Monitor current portfolio balance, leverage usage, and sector tilt
- Identify risky concentrations or oversized trades before making adjustments
- Validate trade snapshot before transitioning positions to historical review (e.g., when closed)
- Support downstream diagnostics such as:
  - Trade Structuring & Risk Planning
  - Portfolio & Trade Performance Review

---

⚠️ Interpretation Caution:
- Outputs reflect **open trades only**, based on uploaded values.
- No forecast, signal, or valuation model is applied.
- Risk tiering is structural, not advisory — it helps flag exposure concentration, not performance quality.
