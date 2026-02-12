# 📖 What is this app about?

This module calculates and visualises stop-loss buffer zones using Average True Range (ATR) analysis across daily, weekly, and monthly timeframes.

It displays:

- **ATR Values**: A rolling measure of volatility calculated over a 14-period window.
- **Stop-Loss Zones**: Upper and lower reference bands based on the ATR added to or subtracted from the current price.
- **Historical Volatility Chart**: Visual overlays of price movement relative to suggested buffer zones.
- **Timeframe Views**: Evaluate full range (e.g., last 300 periods), 50-day short-term, and 200-day medium-term windows.

The tool helps contextualise how wide a stop might need to be to avoid volatility-triggered exits — and where compression or expansion may influence buffer design. It is **not a strategy engine** — it supports trade planning logic with volatility awareness.
