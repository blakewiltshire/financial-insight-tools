## External Market Data Sources

To prepare your own user-uploaded asset sets, we recommend using the following historical data providers. Ensure you download **daily historical data in CSV format**, with standard columns: `date, open, high, low, close, volume`.

---

### [Investing.com](https://www.investing.com/)
- Offers free historical data for equities, ETFs, indices, commodities, bonds, and forex.
- Steps:
  1. Navigate to the desired asset page (e.g. Tesla, Gold, S&P 500).
  2. Select **Historical Data** tab.
  3. Choose **daily frequency**, and export to CSV.
  4. Save the file into the relevant folder under `/financial_data/` — e.g., `equities_mag7_user/`.

---

### Other Compatible Providers
These platforms also allow manual CSV downloads compatible with the Insight Tools system:

- [TradingView](https://www.tradingview.com/) – Charts and historical data for major assets.
- [MarketWatch](https://www.marketwatch.com/) – Equities and ETF performance history.
- [Barchart](https://www.barchart.com/) – Commodities and futures.
- [Stooq](https://stooq.com/) – Broad asset coverage with flexible download formats.

---

### Currency & Format Reminders
- Ensure all assets for spread analysis are **in the same currency** (e.g., all in USD).
- If needed, use the **Historical Data Currency Converter** module before building your snapshot.
- Remove any non-numeric columns (e.g., dividend flags, adjusted closes).
- Use consistent formatting for headers and dates (e.g., YYYY-MM-DD).
