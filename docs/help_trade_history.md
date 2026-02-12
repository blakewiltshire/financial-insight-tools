# ℹ️ Help: How to interpret Trade History Review

This module performs a structural review of your **closed historical trades**, enabling insight into realised performance, trade consistency, and outcome variance.

It validates file integrity and computes key outputs that can inform broader strategy evaluation, risk management, or optimisation planning.

---

**Key Concepts:**

- **Trade Status:** Trades are marked as `Closed` if exit price and date are both provided.
- **Realised P&L:** Profit or loss calculated based on direction (`Long`/`Short`), entry/exit price, and position size.
- **Position Sizing Consistency:** Variance in trade sizing can amplify volatility and distort performance metrics.

---

**Example:**
You upload a log of 40 trades.  
After validation:
- 35 are marked `Closed`
- 5 remain `Open` and are not analysed
- Realised P&L is computed for all closed trades

**You receive:**
- **Annualised Return:** Theoretical growth extrapolated from net profit, adjusted for days active
- **Volatility & Sharpe Ratio:** Metrics capturing reward-to-risk efficiency
- **Drawdown:** Largest cumulative loss during the observed trade sequence

---

**Use Case:**
This module is best used to:
- Identify performance patterns (e.g., consistent underperformance in a strategy tag)
- Assess outcome volatility relative to sizing logic
- Feed cleaned, verified results into other modules like:
  - Kelly Criterion Calculator
  - Trade Structuring & Risk Planning
  - Portfolio & Trade Performance Review

---

⚠️ Interpretation Caution:
- Outputs reflect **past trades only**. No predictive inference is made.
- **Open positions are excluded** from performance metrics.
- Metrics do not imply recommendation — they contextualise structural performance.
