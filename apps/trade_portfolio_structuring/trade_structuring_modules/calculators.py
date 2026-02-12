# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=unused-variable, invalid-name, non-ascii-file-name
# pylint: disable=too-many-locals, too-many-arguments, too-many-statements

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Trade Calculators

Modular calculators for structuring trade setups across Shares (No Leverage),
CFDs/Spread Betting (Leverage Applied), and Pairs/Multi-Leg Spread strategies.
Includes universal input fields for tax, slippage, and currency conversions.
Integrated with the trade dashboard module to enable interactive position planning.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Import Your Module Logic Below
# -------------------------------------------------------------------------------------------------
from trade_structuring_modules.trade_dashboard import add_trade_to_dashboard

# -------------------------------------------------------------------------------------------------
# Universal Trade Field Inputs
# -------------------------------------------------------------------------------------------------
def universal_trade_fields():
    """
    Collects universal trading fields for slippage, tax, transaction costs, etc.
    """
    with st.expander("🧾 Cost & Currency Considerations"):
        st.markdown("""
        These fields apply to **all trade types** and model real-world frictions:

        - **Slippage (%)**: Estimated execution friction
        - **Transaction Costs**: Flat fees from broker/platform
        - **Capital Gains Tax (%)**: For post-tax return estimation
        - **Dividend Yield (%)**: Applies to equity holdings if relevant
        - **Currency Conversion Rate**: Simulate FX adjustment (e.g., GBP to USD)
        - **Exchange Rate (Preview Only)**: View or compare exchange environment

        ⚠️ Mixing assets across currencies without explicit conversion may distort
        exposure or margin.
        """)

        slippage_pct = st.number_input("Estimated Slippage (%)", min_value=0.0, value=0.05,
        step=0.01)
        transaction_costs = st.number_input("Transaction Costs", min_value=0.0, value=0.0,
        step=0.01)
        capital_gains_tax_pct = st.number_input("Capital Gains Tax Rate (%)", min_value=0.0,
        value=0.0, step=0.1)
        dividend_yield_pct = st.number_input("Dividend Yield (%) (if applicable)", min_value=0.0,
        value=0.0, step=0.1)
        currency_conversion_rate = st.number_input("Currency Conversion Rate (if applicable)",
                                                   min_value=0.0, value=1.0, step=0.0001,
                                                   format="%.4f")
        exchange_rate = st.number_input("Exchange Rate (if applicable)",
                                        min_value=0.0, value=1.0, step=0.0001, format="%.4f")

        return {
            "Slippage (%)": slippage_pct,
            "Transaction Costs": transaction_costs,
            "Capital Gains Tax (%)": capital_gains_tax_pct,
            "Dividend Yield (%)": dividend_yield_pct,
            "Currency Conversion Rate": currency_conversion_rate,
            "Exchange Rate (if applicable)": exchange_rate,
        }

# -------------------------------------------------------------------------------------------------
# --- Share Calculator Integration ---
# -------------------------------------------------------------------------------------------------
def shares_calculator_intuitive(asset_name, last_close_price, last_close_date):
    """
    Streamlit-based calculator for structuring non-leveraged equity trades (shares).

    Allows users to plan equity positions by defining stop-loss and target levels
    (based on reward-to-risk ratios), position size, fees, and optional overrides.
    Results are summarised and optionally added to the structured trade dashboard.

    Parameters:
        asset_name (str): Name of the selected equity asset.
        last_close_price (float): Latest available closing price.
        last_close_date (str or datetime): Most recent date for available pricing data.

    Returns:
        None. Outputs results to Streamlit interface and optionally appends
        structured trade to the session dashboard.
    """
    st.subheader(f"Shares (No Leverage) Calculator for **{asset_name}**")
    st.caption("Plan your equity trade structure. Override stop-loss or soft target if \
    using custom levels.")
    st.caption(f"📅 Last Close Date: {last_close_date.strftime('%Y-%m-%d')}")

    share_price = st.number_input("Current Asset Price",
                                  min_value=0.01, value=round(last_close_price, 2), step=0.01,
                                  key=f"{asset_name}_share_price")
    num_shares = st.number_input("Number of Shares to Buy",
                                 min_value=1, value=10, step=1,
                                 key=f"{asset_name}_shares_qty")
    fees = st.number_input("Broker Fees",
                           min_value=0.0, value=5.0, step=0.01,
                           key=f"{asset_name}_fees")

    reward_to_risk_ratio = st.slider("Soft Target Multiplier (based on Reward-to-Risk Ratio)",
                                     min_value=1.0, max_value=5.0, value=3.0, step=0.1,
                                     key=f"{asset_name}_shares_rrr_slider")
    stop_loss_pct = st.slider("Stop Loss Distance (%)",
                               min_value=0.5, max_value=10.0, value=1.0, step=0.1,
                               key=f"{asset_name}_stop_loss_pct")

    stop_loss_distance = (stop_loss_pct / 100) * share_price
    soft_target_distance = stop_loss_distance * reward_to_risk_ratio

    override_sl = st.number_input("Override Stop Loss Distance (Optional)",
                                  min_value=0.0, value=0.0, step=0.01,
                                  key=f"{asset_name}_shares_sl_override")
    override_target = st.number_input("Override Soft Target Distance (Optional)",
                                      min_value=0.0, value=0.0, step=0.01,
                                      key=f"{asset_name}_shares_target_override")

    final_stop_loss = override_sl if override_sl > 0 else stop_loss_distance
    final_soft_target = override_target if override_target > 0 else soft_target_distance

    capital_at_risk = final_stop_loss * num_shares
    potential_reward = final_soft_target * num_shares
    break_even = share_price + (capital_at_risk / num_shares) / 2 + (fees / num_shares)

    total_cost = (share_price * num_shares) + fees

    st.markdown("### Planning Summary")
    st.write(f"**Capital at Risk:** {capital_at_risk:,.2f}")
    st.write(f"**Potential Reward:** {potential_reward:,.2f}")
    st.write(f"**Break-even Price (Including Fees):** {break_even:,.2f}")
    st.write(f"**Reward-to-Risk Ratio:** {reward_to_risk_ratio:.2f}")

    st.markdown("### Execution Panel")
    st.write(f"**Calculated Stop Loss Distance:** {final_stop_loss:,.2f}")
    st.write(f"**Calculated Soft Target Distance:** {final_soft_target:,.2f}")
    st.write(f"**Total Cost to Buy Shares (Including Fees):** {total_cost:,.2f}")

    # --- Cost and Currency Panel ---
    universal_fields = universal_trade_fields()

    notes = st.text_area("Notes (Optional)", key=f"{asset_name}_shares_notes")

    if st.button("➕ Add Trade to Dashboard", key=f"add_shares_trade_{asset_name}"):
        trade_data = {
            "Asset (Primary)": asset_name,
            "Trade Type": "Shares (No Leverage)",
            "Trade Direction": "Long",
            "Long Entry Price (Planned)": share_price,
            "Stop Loss (Planned)": share_price - final_stop_loss,
            "Take Profit (Planned)": share_price + final_soft_target,
            "Long Position Size (Units)": num_shares,
            "Allocated Capital": share_price * num_shares,
            "Risk %": f"{stop_loss_pct}%",
            "Reward-to-Risk Ratio": round(reward_to_risk_ratio, 2),
            "Execution Price Override": "",
            "Broker Fees": fees,
            "Carry/Rollover Cost": "",
            **universal_fields,
            "Notes": notes + f" | SL: {final_stop_loss}, Target: {final_soft_target}"
        }
        add_trade_to_dashboard(trade_data)

# -------------------------------------------------------------------------------------------------
# --- CFD / Spread Betting Calculator with full universal fields and contextual panels ---
# -------------------------------------------------------------------------------------------------
def cfd_calculator(asset_name, last_close_price, last_close_date,
                   asset_type="Equity", lot_size=100000, decimal_places=4):
    """
    Streamlit-based calculator for structuring leveraged CFD and spread betting trades.

    Provides a dynamic interface to define position parameters such as stake-per-point,
    margin requirements, leverage, stop-loss distance, and soft target multipliers.
    Supports both currency and non-currency asset types, with override fields
    and universal cost inputs. Results can be exported to the structured trade dashboard.

    Parameters:
        asset_name (str): Name of the asset being evaluated.
        last_close_price (float): Most recent closing price for the asset.
        last_close_date (str or datetime): Most recent available date.
        asset_type (str): Type of asset (e.g., "Equity", "Currencies").
        lot_size (int): Standard lot size (only relevant for currencies).
        decimal_places (int): Number of decimals to use in price formatting.

    Returns:
        None. Outputs calculations to the Streamlit interface and optionally
        appends the structured trade to the session dashboard.
    """
    st.subheader(f"CFD / Spread Betting Calculator for **{asset_name}**")
    st.caption("Structuring CFD or spread betting positions with proper Forex handling, \
    margin planning, and universal fields.")
    st.caption(f"📅 Last Close Date: {last_close_date.strftime('%Y-%m-%d')}")

    share_price = st.number_input("Current Asset Price",
        min_value=0.00001,
        value=round(last_close_price, decimal_places),
        step=0.00001,
        key=f"{asset_name}_cfd_price"
    )

    if asset_type == "Currencies":
        pip_size = 1 / (10 ** 4)
        pip_value = pip_size * lot_size
        st.write(f"**Pip Value:** {pip_value:.2f}")

    fees = st.number_input("Estimated Broker Fees & Carry Costs",
        min_value=0.0, value=5.0, step=0.01, key=f"{asset_name}_fees")
    margin_pct = st.slider("Broker Margin Requirement (%)",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name}_margin_pct")
    leverage = st.slider("Leverage",
        min_value=1, max_value=100, value=30, step=1, key=f"{asset_name}_leverage")

    reward_to_risk_ratio = st.slider("Reward-to-Risk Ratio Multiplier",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name}_rrr")
    stop_loss_pct = st.slider("Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1, key=f"{asset_name}_sl_pct")

    stop_loss_distance = (stop_loss_pct / 100) * share_price
    soft_target_distance = stop_loss_distance * reward_to_risk_ratio

    override_sl = st.number_input("Override Stop Loss (optional)",
        min_value=0.0, value=0.0, step=0.0001, key=f"{asset_name}_override_sl")
    override_target = st.number_input("Override Soft Target (optional)",
        min_value=0.0, value=0.0, step=0.0001, key=f"{asset_name}_override_target")

    final_stop_loss = override_sl if override_sl > 0 else stop_loss_distance
    final_soft_target = override_target if override_target > 0 else soft_target_distance

    stake_per_point = st.number_input("Stake-per-Point",
        min_value=0.01, value=1.0, step=0.01, key=f"{asset_name}_stake")

    if asset_type == "Currencies":
        notional_exposure = stake_per_point * lot_size
    else:
        notional_exposure = stake_per_point * share_price

    margin_required = notional_exposure * (margin_pct / 100)
    capital_at_risk = stake_per_point * final_stop_loss

    spread_points = st.number_input("Estimated Broker Spread (Points)",
        min_value=0.0, value=1.0, step=0.1, key=f"{asset_name}_spread_points")
    estimated_spread_cost = spread_points * stake_per_point

    break_even_price = share_price + (
    fees / stake_per_point) + (estimated_spread_cost / stake_per_point
    )

    st.markdown("### Planning Summary")
    st.write(f"**Capital at Risk:** {capital_at_risk:,.2f}")
    st.write(f"**Notional Exposure:** {notional_exposure:,.2f}")
    st.write(f"**Margin Required:** {margin_required:,.2f}")
    st.write(f"**Estimated Spread Cost:** {estimated_spread_cost:,.2f}")
    st.write(f"**Leverage:** {leverage}x")

    st.markdown("### Execution Panel")
    st.write(f"**Calculated Stop Loss:** {final_stop_loss:.5f} | {capital_at_risk:.2f} at risk")
    st.write(f"**Soft Target:** {final_soft_target:.5f} points")
    st.write(f"**Break-even Price:** {break_even_price:,.5f}")

    universal_data = universal_trade_fields()
    notes = st.text_area("Notes (Optional)", key=f"{asset_name}_notes")

    if st.button("➕ Add CFD Trade to Dashboard", key=f"add_cfd_trade_{asset_name}"):
        trade_data = {
            "Asset (Primary)": asset_name,
            "Trade Type": "CFDs / Spread Betting",
            "Trade Direction": "Long or Short",
            "Long Entry Price (Planned)": share_price,
            "Stop Loss (Planned)": share_price - final_stop_loss,
            "Take Profit (Planned)": share_price + final_soft_target,
            "Stake per Point": stake_per_point,
            "Notional Exposure": notional_exposure,
            "Reward-to-Risk Ratio": reward_to_risk_ratio,
            "Leverage": leverage,
            "Margin Required": margin_required,
            "Estimated Spread Cost": estimated_spread_cost,
            "Execution Price Override": "",
            "Broker Fees": fees,
            "Carry/Rollover Cost": "",
            "Notes": notes,
            **universal_data
        }
        add_trade_to_dashboard(trade_data)

# -------------------------------------------------------------------------------------------------
# --- Pairs / Multi-Leg Spread Calculator (Updated with asset types) ---
# -------------------------------------------------------------------------------------------------
def pairs_spread_calculator(
    asset_name_long, asset_name_short, long_price, short_price,
    long_asset_type="Equities", short_asset_type="Equities"
):
    """
    Streamlit-based calculator for designing pairs or multi-leg spread trades.

    Allows users to configure both long and short legs of a spread strategy with
    independent margin settings, stop-loss distances, and reward-to-risk multipliers.
    Includes optional overrides, contextual notes, and spread analytics such as
    Z-score, correlation, and volatility. Designed to support intermarket, sector,
    or mean-reversion strategies across asset types.

    Parameters:
        asset_name_long (str): Name of the asset in the long leg.
        asset_name_short (str): Name of the asset in the short leg.
        long_price (float): Latest price of the long asset.
        short_price (float): Latest price of the short asset.
        long_asset_type (str): Asset category for the long leg (e.g., "Equities", "Currencies").
        short_asset_type (str): Asset category for the short leg.

    Returns:
        None. Outputs results to the Streamlit interface and updates the session trade dashboard
        if the user confirms the trade structure.
    """
    st.subheader(f"Pairs / Multi-Leg Spread Calculator for {asset_name_long} / {asset_name_short}")
    st.caption("Structure each leg with overrides, margin planning, historical context, \
    and ratio observations.")

    # --- Long Leg ---
    st.markdown("### Long Leg Setup")
    st.write(f"**{asset_name_long} Price:** {long_price:.2f} | Type: {long_asset_type}")
    stake_long = st.number_input(f"Stake-per-Point for {asset_name_long}",
        min_value=0.1, value=1.0, step=0.1, key=f"{asset_name_long}_stake_long")
    long_margin_pct = st.slider(f"Broker Margin Requirement (%) for {asset_name_long}",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name_long}_margin_pct_long")
    long_stop_pct = st.slider(f"{asset_name_long} Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1,
        key=f"{asset_name_long}_stop_pct_long")
    long_sl_default = (long_stop_pct / 100) * long_price
    override_long_sl = st.number_input(
        f"Override Stop Loss Distance for {asset_name_long} (optional)",
        min_value=0.0, value=0.0, step=0.01, key=f"{asset_name_long}_sl_override_long")
    long_stop_loss = override_long_sl if override_long_sl > 0 else long_sl_default
    long_rrr = st.slider(f"Reward-to-Risk Ratio for {asset_name_long}",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name_long}_rrr_long")
    long_target = long_stop_loss * long_rrr
    long_notional = stake_long * long_price
    long_margin = long_notional * (long_margin_pct / 100)

    # --- Short Leg ---
    st.markdown("### Short Leg Setup")
    st.write(f"**{asset_name_short} Price:** {short_price:.2f} | Type: {short_asset_type}")
    stake_short = st.number_input(f"Stake-per-Point for {asset_name_short}",
        min_value=0.1, value=1.0, step=0.1, key=f"{asset_name_short}_stake_short")
    short_margin_pct = st.slider(f"Broker Margin Requirement (%) for {asset_name_short}",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name_short}_margin_pct_short")
    short_stop_pct = st.slider(f"{asset_name_short} Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1,
        key=f"{asset_name_short}_stop_pct_short")
    short_sl_default = (short_stop_pct / 100) * short_price
    override_short_sl = st.number_input(
        f"Override Stop Loss Distance for {asset_name_short} (optional)",
        min_value=0.0, value=0.0, step=0.01, key=f"{asset_name_short}_sl_override_short")
    short_stop_loss = override_short_sl if override_short_sl > 0 else short_sl_default
    short_rrr = st.slider(f"Reward-to-Risk Ratio for {asset_name_short}",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name_short}_rrr_short")
    short_target = short_stop_loss * short_rrr
    short_notional = stake_short * short_price
    short_margin = short_notional * (short_margin_pct / 100)

    # --- Combined Metrics ---
    combined_risk = (stake_long * long_stop_loss) + (stake_short * short_stop_loss)
    combined_reward = (stake_long * long_target) + (stake_short * short_target)

    st.markdown("### Historical Spread Reference & Observations")
    historical_summary = st.text_area(
    "Historical spread context, Z-score levels, or observations (optional)",
        key="pairs_historical_context")
    avg_spread_ratio = st.number_input("Average Spread Ratio (manual entry)",
        min_value=0.0, value=0.0, step=0.0001, key="avg_spread_ratio_manual")
    spread_volatility = st.number_input("Volatility (Std Dev) of spread (manual entry)",
        min_value=0.0, value=0.0, step=0.0001, key="spread_volatility_manual")
    correlation = st.number_input("Correlation (manual entry)",
        min_value=-1.0, max_value=1.0, value=0.0, step=0.01, key="correlation_manual")
    z_score = st.number_input("Z-Score (Deviation from Mean, manual entry)",
        min_value=-5.0, max_value=5.0, value=0.0, step=0.01, key="z_score_manual")
    support_levels = st.text_area("Support Levels (comma-separated, manual entry)"
    , key="support_levels_manual")
    resistance_levels = st.text_area("Resistance Levels (comma-separated, manual entry)"
    , key="resistance_levels_manual")
    drift_notes = st.text_area("Observed drift or additional notes (optional)"
    , key="drift_notes_manual")

    st.markdown("### Combined Planning Summary")
    st.write(f"**Total Long Margin:** {long_margin:.2f}")
    st.write(f"**Total Short Margin:** {short_margin:.2f}")
    st.write(f"**Combined Margin Required:** {(long_margin + short_margin):.2f}")
    st.write(f"**Combined Risk:** {combined_risk:.2f}")
    st.write(f"**Combined Potential Reward:** {combined_reward:.2f}")

    universal_fields = universal_trade_fields()
    ref_only = st.checkbox("Mark this trade as reference only (stops not auto-placed)",
    key="ref_only_checkbox")
    notes = st.text_area("Additional Notes (optional)", key="pairs_notes")

    if st.button("➕ Add Spread Trade to Dashboard", key="add_pairs_trade_btn"):
        trade_data = {
            "Asset (Primary)": asset_name_long,
            "Long Asset Type": long_asset_type,
            "Asset (Short Leg)": asset_name_short,
            "Short Asset Type": short_asset_type,
            "Trade Type": "Pairs / Multi-Leg Spread",
            "Trade Direction": "Spread",
            "Long Entry Price (Planned)": long_price,
            "Short Entry Price (Planned)": short_price,
            "Long Stake-per-Point": stake_long,
            "Short Stake-per-Point": stake_short,
            "Long Margin Required": long_margin,
            "Short Margin Required": short_margin,
            "Long Stop Loss (pts)": long_stop_loss,
            "Short Stop Loss (pts)": short_stop_loss,
            "Long Target (pts)": long_target,
            "Short Target (pts)": short_target,
            "Risk (Combined)": combined_risk,
            "Potential Reward (Combined)": combined_reward,
            "Reference Only": ref_only,
            "Historical Context": historical_summary,
            "Average Spread Ratio": avg_spread_ratio,
            "Spread Volatility (Std Dev)": spread_volatility,
            "Correlation": correlation,
            "Z-Score": z_score,
            "Support Levels": support_levels,
            "Resistance Levels": resistance_levels,
            "Drift Notes": drift_notes,
            **universal_fields,
            "Notes": notes
        }
        add_trade_to_dashboard(trade_data)
