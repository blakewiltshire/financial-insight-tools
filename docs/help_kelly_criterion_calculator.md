# ℹ️ Help: How to interpret Kelly Criterion analysis

The Kelly Criterion offers a structural way to estimate how much capital to allocate to a single trade, based on your probability of success and reward-to-risk profile.

It calculates the optimal fraction of your capital to risk in order to maximise long-term growth under repeatable edge-driven conditions.

---

**Key Terms:**

- **Win Probability (W):** Your estimated or historical chance of winning.
- **Reward-to-Risk Ratio (R):** How much you typically gain relative to what you risk.
- **Kelly Fraction:** The theoretical capital percentage to allocate per trade to maximise compounded return, assuming probabilities are accurate.

---

**Example (From Historical Trade Data):**

You’ve executed 61 trades:
- 30 were wins, 31 were losses.
- Your average win: \$X; your average loss: \$Y.
- This results in:
  - **Win Probability:** 49.2%
  - **Reward-to-Risk Ratio:** 1.80

The Kelly Criterion returns:

- **Full Kelly Fraction:** 20.94%
- **Applied Fraction (e.g., 10% Kelly):** 2.09%

This means:  
If your past performance remains statistically consistent, risking **20.94% of capital** per trade would — in theory — maximise long-term growth.  
Reducing this (e.g., to 10% Kelly) moderates exposure while retaining the informational value of the signal.

---

**Use Case:**

This value can inform stop-loss placement or capital sizing logic inside your **Trade Structuring & Risk Planning** workflow.

For example, when targeting a 4% directional move on an asset like Tesla, your ATR-based stop and Kelly-based position sizing can be combined to balance exposure and probability-weighted growth.

---

⚠️ Interpretation Caution:

- Kelly is designed for **repeated, probabilistic events**.
- It **does not** reduce drawdowns — it **maximises geometric growth** under theoretical consistency.
- Many professional traders apply **fractional Kelly** to manage volatility exposure.
