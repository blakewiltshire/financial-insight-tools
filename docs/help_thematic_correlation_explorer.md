## 🔗 Thematic Correlation Explorer — ℹ️ Help: How to Read These Summaries

This module surfaces structural relationships across macroeconomic indicators, enabling multi-theme, multi-country correlation analysis across diverse combinations of signals.

### 🧮 What is being calculated?

- **Z-score Standardisation:**  
  All indicators are internally normalised, removing original units, levels, and scales. Each series reflects its standard deviation movement around its own historical mean.

- **Correlation Matrix:**  
  Pairwise Pearson correlation coefficients are calculated between all selected indicators. Correlation strength ranges from `-1.0` (perfect inverse) to `+1.0` (perfect direct alignment).

- **Rolling Timeline Slicing:**  
  - 📉 *Short-Term (50 periods)* — most recent dynamics  
  - 📊 *Medium-Term (200 periods)* — broader structural trends  
  - 🕰 *Full History* — full available dataset range

📊 Interpreting the Correlation Outputs

- **Heatmaps:**  

  - Color-coded matrices display the correlation coefficient between all selected indicators.
  - Dark red indicates strong positive relationships (direct correlation).
  - Dark blue indicates strong inverse relationships (negative correlation).

- **Summary Statistics**

  - Each time horizon includes aggregate correlation summaries:

    - **Mean Correlation:** Average across all indicators.
    - **Standard Deviation of Correlations:** Dispersion of observed relationships.
    - **Max / Min:** Strongest positive and negative correlations within the selection.

- **Standardised Overlay**

    - Visual representation of all selected indicators over time, Z-score normalised.
    - Allows intuitive visual comparison of how indicators move relative to each other.

- **Structural Directionality Summary**

  - **Direct Relationships (r > +0.3):** Signals showing consistent positive co-movement.
  - **Inverse Relationships (r < -0.3):** Signals exhibiting consistent opposite behaviour.

These directional markers are not thresholds of significance, but reference anchors for structural context.

---

### 💡 Practical Example: GDP vs S&P500

As illustration:

- A user selects *Real GDP Level (United States)* and *S&P500 Index*.
- After harmonisation, the system aligns both series to monthly periodicity for correlation evaluation.
- Across available history, structural correlations may surface high positive alignment (e.g. `r = 0.91` full history), reflecting long-term economic expansion supporting broad equity markets.
- In short-term slicing, these relationships may vary as markets discount expectations, shift forward-looking, or react to sentiment and monetary conditions.

Such alignment can inform:

- Observation-driven macro framing
- Contextual evaluation of trading or investment scenarios
- Scenario-building for AI persona analysis within broader workflows

This approach supports **multi-dimensional reflection** rather than prediction. It allows users to structurally assess where selected indicators have historically aligned or diverged, without asserting causality or predictive validity.

---

### 🔄 Time Alignment and Lagged Relationships

The module aligns all series on the same time axis after resampling. This means all comparisons are performed contemporaneously — indicator values for a given month are evaluated side-by-side.

However, true economic causality often unfolds with time lags, where one indicator’s movement precedes another. For example:

- **GDP Growth → Labour Market**
GDP expansions often precede employment gains.
- **PMI Declines → Industrial Output Slowdown**
Sentiment deterioration frequently leads physical production changes.
- **Policy Rates → Credit and Equity Markets**
Monetary policy shifts may influence financial markets after several months.

**Thematic Correlation Explorer does not automatically apply lag adjustments.** Users must interpret whether observed contemporaneous correlations reflect leading, coincident, or lagging dynamics based on domain knowledge.

### 🔎 Advanced Lag and Event-Based Exploration

For users seeking to investigate time-shifted relationships or event-based sequencing:

- **🔎 Market & Volatility Scanner**
Includes Event-Based Analysis Filtering, enabling targeted analysis of asset behaviour (e.g. SP500) around key macroeconomic releases (e.g. GDP reports, CPI prints, central bank decisions). This supports practical event-driven timing assessments.
- **🧠 Observation & AI Export**
Users can construct observation bundles reflecting hypothesised lead-lag sequences for AI-supported scenario evaluation and portfolio framing.

---

### ⚠ Framing

This module supports:

- Observational signal structuring  
- User-generated scenario stress testing  
- AI-enhanced personal development or investment context evaluation

**It does not offer forecasts, recommendations, or prescriptive outputs. All interpretation remains with the user.**
