## Historical Data Currency Converter

This utility applies a **manual currency conversion** to uploaded historical
OHLC data (Open, High, Low, Close).

**Primary Use Case:** Unifying currency for correlation or spread analysis

**Use With:** Market & Volatility Scanner, Intermarket Correlation, and related modules  

**Supported Format:** Tested with Investing.com historical data files only  

**Do Not Use:** With mixed-currency comparisons — always align base currencies  

**Saved Location:**
  ```plaintext
  /financial_data/asset_currency_converted/
  ```

  ---
**Why this matters**

Most financial comparisons — including correlation matrices, spread charts, and volatility diagnostics —  assume all assets are priced in a **common base currency**.

Mixing currencies (e.g. comparing Tesla `[USD]` with Volkswagen `[EUR]`) will distort calculations.

This tool ensures **unified pricing** so that analysis across geographies remains
structurally valid.


---
⚠️ **Important Note**

Currency conversion in this module is a **manual, point-in-time operation**.
It is designed for **data normalisation**, not for live trading or price forecasting.
Rates should be verified externally and reflect your intended analysis timeframe.
