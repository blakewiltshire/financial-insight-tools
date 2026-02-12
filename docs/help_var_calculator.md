# ℹ️ Help: How to interpret VaR analysis

This app estimates how much an asset might lose, under typical historical conditions, with a specified statistical confidence.

---

## Key Terms

- **Value at Risk (VaR):** A statistical estimate of the potential loss over a defined period, with a given level of confidence.
- **Confidence Level:** Probability that actual loss will not exceed the VaR estimate. Common values: 90%, 95%, 99%.
- **Holding Period:** The number of days you plan to hold the asset — affects the potential exposure duration.
- **VaR Estimate:** The potential loss you might observe **or exceed** over the holding period with the inverse confidence probability (e.g. 5% for 95%).

---

## Example

For Tesla:

- **Confidence Level:** 95%
- **Holding Period:** 5 Days
- **Daily Return Distribution:** Based on last 250 periods
- **VaR:** −4.12%

**Interpretation:**  
There's a 95% chance that Tesla will not lose more than **4.12%** over the next 5 days under similar market conditions.  
Or inversely: there's a 5% chance it might lose more than that.

---

## Visuals

- **Histogram:** Shows full distribution of past daily returns.
- **Shaded Tail:** Highlights the portion representing the worst expected losses for the chosen confidence level.
- **Vertical Line (VaR):** Indicates threshold of potential downside under the current configuration.

---

## Use Case

The tool can help estimate appropriate **position sizes**, set expectations for drawdown scenarios, or inform broader **portfolio risk buffers** — especially when used in conjunction with trade logic such as:

- Stop-loss proximity
- Capital-at-risk models
- Scenario stress overlays

---

## Limitations

- This is a **historical VaR** tool — it does not account for future market regimes or tail risk dynamics.
- Does not imply probability of achieving returns — only estimates potential **loss** magnitude based on past data.
