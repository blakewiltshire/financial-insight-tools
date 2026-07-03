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

Modular planning calculators for structuring trade scenarios across Shares (No Leverage),
CFDs/Spread Betting (Leverage Applied), and Pairs/Multi-Leg Spread strategies.

The calculators are designed as planning worksheets rather than execution tools. They preserve
position assumptions, risk boundaries, reward targets, cost estimates, and notes for downstream
review in the structured trade dashboard.
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
# Shared Helpers
# -------------------------------------------------------------------------------------------------
def _safe_ratio(numerator: float, denominator: float) -> float:
    """Return a safe numeric ratio."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _date_label(last_close_date) -> str:
    """Format date-like objects safely for display."""
    if hasattr(last_close_date, "strftime"):
        return last_close_date.strftime("%Y-%m-%d")
    return str(last_close_date)


def _summary_lines(title: str, rows: list[tuple[str, str]]) -> None:
    """Render a compact planning summary using FIT's restrained text style."""
    st.markdown(f"### {title}")
    for label, value in rows:
        st.write(f"**{label}:** {value}")


def _price_precision(asset_type) -> int:
    """Return display precision based on the underlying asset type."""
    asset = (asset_type or "").lower()

    if any(term in asset for term in ["currenc", "forex", "fx"]):
        return 4
    if "crypto" in asset:
        return 4

    return 2


def _price_step(precision: int) -> float:
    """Return a sensible Streamlit step for the selected price precision."""
    return 1 / (10 ** precision)


def _fmt_price(value: float, precision: int) -> str:
    """Format a price or price distance using asset-specific precision."""
    return f"{value:,.{precision}f}"


def _fmt_money(value: float) -> str:
    """Format money/exposure values using two decimal places."""
    return f"{value:,.2f}"


def _fmt_ratio(value: float) -> str:
    """Format reward-to-risk ratios using compact trading notation."""
    return f"{value:.2f}"


# -------------------------------------------------------------------------------------------------
# Universal Trade Field Inputs
# -------------------------------------------------------------------------------------------------
def universal_trade_fields():
    """
    Collects universal planning fields for slippage, tax, transaction costs, and FX context.

    Returns:
        dict: User-defined cost and currency assumptions used by trade planning calculators.
    """
    with st.expander("Cost & Currency Considerations"):
        st.markdown("""
        These fields apply to **all trade types** and model real-world planning assumptions:

        - **Slippage (%)**: Estimated execution friction
        - **Transaction Costs**: Additional flat costs not captured by broker fees
        - **Capital Gains Tax (%)**: Optional post-tax return context
        - **Dividend Yield (%)**: Optional equity income context
        - **Currency Conversion Rate**: Planning conversion factor where applicable
        - **Exchange Rate (Preview Only)**: Reference exchange environment

        ⚠️ Mixing assets across currencies without explicit conversion may distort
        exposure, margin, and return calculations.
        """)

        slippage_pct = st.number_input(
            "Estimated Slippage (%)", min_value=0.0, value=0.05, step=0.01
        )
        transaction_costs = st.number_input(
            "Transaction Costs", min_value=0.0, value=0.0, step=0.01
        )
        capital_gains_tax_pct = st.number_input(
            "Capital Gains Tax Rate (%)", min_value=0.0, value=0.0, step=0.1
        )
        dividend_yield_pct = st.number_input(
            "Dividend Yield (%) (if applicable)", min_value=0.0, value=0.0, step=0.1
        )
        currency_conversion_rate = st.number_input(
            "Currency Conversion Rate (if applicable)",
            min_value=0.0, value=1.0, step=0.0001, format="%.4f"
        )
        exchange_rate = st.number_input(
            "Exchange Rate (if applicable)",
            min_value=0.0, value=1.0, step=0.0001, format="%.4f"
        )

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
    Streamlit-based calculator for structuring non-leveraged equity trade scenarios.

    The worksheet captures position size, stop-loss distance, target distance, estimated costs,
    break-even exit price, and planning notes. It is designed for non-leveraged long equity
    exposure and exports the structured scenario to the trade dashboard.
    """
    st.subheader(f"Shares (No Leverage) Planning Worksheet for **{asset_name}**")
    st.caption(
        "Structure a non-leveraged equity scenario. Override stop-loss or target distance "
        "where custom levels are being reviewed."
    )
    st.caption(f"Last Close Date: {_date_label(last_close_date)}")

    st.markdown("### Position Setup")
    share_price = st.number_input(
        "Entry / Current Asset Price",
        min_value=0.01, value=round(float(last_close_price), 2), step=0.01,
        key=f"{asset_name}_share_price"
    )
    num_shares = st.number_input(
        "Number of Shares", min_value=1, value=10, step=1,
        key=f"{asset_name}_shares_qty"
    )
    entry_fees = st.number_input(
        "Estimated Entry Broker Fees", min_value=0.0, value=5.0, step=0.01,
        key=f"{asset_name}_entry_fees"
    )
    exit_fees = st.number_input(
        "Estimated Exit Broker Fees", min_value=0.0, value=5.0, step=0.01,
        key=f"{asset_name}_exit_fees"
    )

    st.markdown("### Risk & Reward Setup")
    reward_to_risk_ratio = st.slider(
        "Target Multiplier (Reward-to-Risk)",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1,
        key=f"{asset_name}_shares_rrr_slider"
    )
    stop_loss_pct = st.slider(
        "Stop Loss Distance (%)",
        min_value=0.5, max_value=10.0, value=1.0, step=0.1,
        key=f"{asset_name}_stop_loss_pct"
    )

    stop_loss_distance = (stop_loss_pct / 100) * share_price
    soft_target_distance = stop_loss_distance * reward_to_risk_ratio

    override_sl = st.number_input(
        "Override Stop Loss Distance (Optional)",
        min_value=0.0, value=0.0, step=0.01,
        key=f"{asset_name}_shares_sl_override"
    )
    override_target = st.number_input(
        "Override Target Distance (Optional)",
        min_value=0.0, value=0.0, step=0.01,
        key=f"{asset_name}_shares_target_override"
    )

    final_stop_loss = override_sl if override_sl > 0 else stop_loss_distance
    final_target = override_target if override_target > 0 else soft_target_distance

    universal_fields = universal_trade_fields()

    position_value = share_price * num_shares
    estimated_slippage_cost = position_value * (universal_fields["Slippage (%)"] / 100)
    transaction_costs = universal_fields["Transaction Costs"]
    known_costs = entry_fees + exit_fees + transaction_costs
    estimated_total_costs = known_costs + estimated_slippage_cost
    capital_required = position_value + entry_fees + transaction_costs + estimated_slippage_cost

    stop_loss_price = share_price - final_stop_loss
    target_price = share_price + final_target
    capital_at_risk = final_stop_loss * num_shares
    potential_reward = final_target * num_shares
    actual_reward_to_risk = _safe_ratio(final_target, final_stop_loss)
    risk_pct_actual = _safe_ratio(final_stop_loss, share_price) * 100
    target_pct_actual = _safe_ratio(final_target, share_price) * 100
    break_even_known_price = share_price + _safe_ratio(known_costs, num_shares)
    estimated_break_even_price = share_price + _safe_ratio(estimated_total_costs, num_shares)

    _summary_lines("Planning Summary", [
        ("Position Value", _fmt_money(position_value)),
        ("Capital Required", _fmt_money(capital_required)),
        ("Capital at Risk", _fmt_money(capital_at_risk)),
        ("Potential Reward", _fmt_money(potential_reward)),
        ("Target Multiplier", f"{actual_reward_to_risk:.2f}×"),
    ])

    _summary_lines("Execution Reference", [
        ("Stop Price", _fmt_price(stop_loss_price, 2)),
        ("Target Price", _fmt_price(target_price, 2)),
        ("Break-even Price (Known Costs)", _fmt_price(break_even_known_price, 2)),
        ("Estimated Break-even Price", _fmt_price(estimated_break_even_price, 2)),
        ("Risk Distance", f"{_fmt_price(final_stop_loss, 2)} ({risk_pct_actual:.2f}%)"),
        ("Target Distance", f"{_fmt_price(final_target, 2)} ({target_pct_actual:.2f}%)"),
        ("Known Costs", _fmt_money(known_costs)),
        ("Estimated Slippage", _fmt_money(estimated_slippage_cost)),
    ])

    st.caption(
        "Known break-even uses entry fees, exit fees, and transaction costs. "
        "Estimated break-even also includes slippage as a planning assumption. Tax effects are excluded."
    )

    notes = st.text_area("Planning Notes (Optional)", key=f"{asset_name}_shares_notes")

    if st.button("➕ Add Planning Scenario to Dashboard", key=f"add_shares_trade_{asset_name}"):
        trade_data = {
            "Planning Status": "Planned",
            "Asset (Primary)": asset_name,
            "Trade Type": "Shares (No Leverage)",
            "Trade Direction": "Long",
            "Long Entry Price (Planned)": share_price,
            "Stop Loss (Planned)": stop_loss_price,
            "Take Profit (Planned)": target_price,
            "Long Position Size (Units)": num_shares,
            "Position Value": round(position_value, 2),
            "Allocated Capital": round(position_value, 2),
            "Estimated Entry Costs": round(entry_fees + transaction_costs + estimated_slippage_cost, 2),
            "Estimated Exit Costs": round(exit_fees, 2),
            "Known Costs": round(known_costs, 2),
            "Estimated Total Costs": round(estimated_total_costs, 2),
            "Break-even Price": round(break_even_known_price, 4),
            "Estimated Break-even Price": round(estimated_break_even_price, 4),
            "Capital at Risk": round(capital_at_risk, 2),
            "Potential Reward": round(potential_reward, 2),
            "Risk %": f"{risk_pct_actual:.2f}%",
            "Target %": f"{target_pct_actual:.2f}%",
            "Reward-to-Risk Ratio": round(actual_reward_to_risk, 2),
            "Execution Price Override": "",
            "Broker Fees": round(entry_fees + exit_fees, 2),
            "Carry/Rollover Cost": "",
            **universal_fields,
            "Notes": (
                notes +
                f" | Stop distance: {final_stop_loss:.2f}; Target distance: {final_target:.2f}; "
                f"Known break-even: {break_even_known_price:.2f}; "
                f"Estimated break-even: {estimated_break_even_price:.2f}"
            ).strip()
        }
        add_trade_to_dashboard(trade_data)


# -------------------------------------------------------------------------------------------------
# --- CFD / Spread Betting Calculator with full universal fields and contextual panels ---
# -------------------------------------------------------------------------------------------------
def cfd_calculator(asset_name, last_close_price, last_close_date,
                   asset_type="Equities", lot_size=100000, decimal_places=None):
    """
    Streamlit-based calculator for structuring leveraged CFD and spread betting scenarios.

    Direction-aware stop, target, break-even, margin, notional exposure, and cost estimates are
    calculated for planning purposes. No execution, signal generation, or recommendation is made.
    """
    price_dp = _price_precision(asset_type) if decimal_places is None else int(decimal_places)
    step = _price_step(price_dp)

    st.subheader(f"CFD / Spread Betting Planning Worksheet for **{asset_name}**")
    st.caption(
        "Structure leveraged scenarios with direction-aware stops, targets, margin planning, "
        "stake-per-point, and estimated execution costs."
    )
    st.caption(f"Last Close Date: {_date_label(last_close_date)}")

    st.markdown("### Position Setup")
    price = st.number_input(
        "Entry / Current Asset Price",
        min_value=0.00001,
        value=round(float(last_close_price), price_dp),
        step=step,
        key=f"{asset_name}_cfd_price"
    )
    trade_direction = st.selectbox(
        "Trade Direction", ["Long", "Short"], key=f"{asset_name}_cfd_direction"
    )

    if _price_precision(asset_type) == 4:
        pip_size = 1 / (10 ** 4)
        pip_value = pip_size * lot_size
        st.write(f"**Pip Value:** {pip_value:.2f}")

    fees = st.number_input(
        "Estimated Broker Fees & Carry Costs",
        min_value=0.0, value=5.0, step=0.01, key=f"{asset_name}_fees"
    )
    margin_pct = st.slider(
        "Broker Margin Requirement (%)",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name}_margin_pct"
    )
    effective_leverage = _safe_ratio(100, margin_pct)
    st.caption(f"Implied leverage from margin requirement: **{effective_leverage:.2f}x**")

    st.markdown("### Risk & Reward Setup")
    reward_to_risk_ratio = st.slider(
        "Target Multiplier (Reward-to-Risk)",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name}_rrr"
    )
    stop_loss_pct = st.slider(
        "Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1, key=f"{asset_name}_sl_pct"
    )

    stop_loss_distance = (stop_loss_pct / 100) * price
    target_distance = stop_loss_distance * reward_to_risk_ratio

    override_sl = st.number_input(
        "Override Stop Loss Distance (optional)",
        min_value=0.0, value=0.0, step=0.0001, key=f"{asset_name}_override_sl"
    )
    override_target = st.number_input(
        "Override Target Distance (optional)",
        min_value=0.0, value=0.0, step=0.0001, key=f"{asset_name}_override_target"
    )

    final_stop_loss = override_sl if override_sl > 0 else stop_loss_distance
    final_target = override_target if override_target > 0 else target_distance

    stake_per_point = st.number_input(
        "Stake-per-Point", min_value=0.01, value=1.0, step=0.01,
        key=f"{asset_name}_stake"
    )

    if _price_precision(asset_type) == 4:
        notional_exposure = stake_per_point * lot_size
    else:
        notional_exposure = stake_per_point * price

    margin_required = notional_exposure * (margin_pct / 100)
    capital_at_risk = stake_per_point * final_stop_loss
    potential_reward = stake_per_point * final_target
    actual_reward_to_risk = _safe_ratio(final_target, final_stop_loss)

    spread_points = st.number_input(
        "Estimated Broker Spread (Points)",
        min_value=0.0, value=1.0, step=0.1, key=f"{asset_name}_spread_points"
    )
    estimated_spread_cost = spread_points * stake_per_point

    universal_data = universal_trade_fields()
    transaction_costs = universal_data["Transaction Costs"]
    estimated_slippage_cost = notional_exposure * (universal_data["Slippage (%)"] / 100)
    known_costs = fees + estimated_spread_cost + transaction_costs
    estimated_total_costs = known_costs + estimated_slippage_cost
    known_break_even_points = _safe_ratio(known_costs, stake_per_point)
    estimated_break_even_points = _safe_ratio(estimated_total_costs, stake_per_point)

    if trade_direction == "Long":
        stop_price = price - final_stop_loss
        target_price = price + final_target
        break_even_price = price + known_break_even_points
        estimated_break_even_price = price + estimated_break_even_points
    else:
        stop_price = price + final_stop_loss
        target_price = price - final_target
        break_even_price = price - known_break_even_points
        estimated_break_even_price = price - estimated_break_even_points

    risk_pct_actual = _safe_ratio(final_stop_loss, price) * 100
    target_pct_actual = _safe_ratio(final_target, price) * 100

    _summary_lines("Planning Summary", [
        ("Underlying Exposure", _fmt_money(notional_exposure)),
        ("Margin Required", _fmt_money(margin_required)),
        ("Capital at Risk", _fmt_money(capital_at_risk)),
        ("Potential Reward", _fmt_money(potential_reward)),
        ("Target Multiplier", f"{actual_reward_to_risk:.2f}×"),
    ])

    _summary_lines("Execution Reference", [
        ("Stop Price", _fmt_price(stop_price, price_dp)),
        ("Target Price", _fmt_price(target_price, price_dp)),
        ("Break-even Price (Known Costs)", _fmt_price(break_even_price, price_dp)),
        ("Estimated Break-even Price", _fmt_price(estimated_break_even_price, price_dp)),
        ("Risk Distance", f"{_fmt_price(final_stop_loss, price_dp)} ({risk_pct_actual:.2f}%)"),
        ("Target Distance", f"{_fmt_price(final_target, price_dp)} ({target_pct_actual:.2f}%)"),
        ("Known Costs", _fmt_money(known_costs)),
        ("Estimated Slippage", _fmt_money(estimated_slippage_cost)),
    ])

    st.caption(
        "Known break-even includes broker fees, spread cost, and transaction costs. "
        "Estimated break-even also includes slippage as a planning assumption."
    )

    notes = st.text_area("Planning Notes (Optional)", key=f"{asset_name}_notes")

    if st.button("➕ Add Planning Scenario to Dashboard", key=f"add_cfd_trade_{asset_name}"):
        trade_data = {
            "Planning Status": "Planned",
            "Asset (Primary)": asset_name,
            "Trade Type": "CFDs / Spread Betting",
            "Trade Direction": trade_direction,
            "Long Entry Price (Planned)": price if trade_direction == "Long" else "",
            "Short Entry Price (Planned)": price if trade_direction == "Short" else "",
            "Stop Loss (Planned)": round(stop_price, price_dp),
            "Take Profit (Planned)": round(target_price, price_dp),
            "Stake per Point": stake_per_point,
            "Notional Exposure": round(notional_exposure, 2),
            "Margin Required": round(margin_required, 2),
            "Capital at Risk": round(capital_at_risk, 2),
            "Potential Reward": round(potential_reward, 2),
            "Risk %": f"{risk_pct_actual:.2f}%",
            "Target %": f"{target_pct_actual:.2f}%",
            "Reward-to-Risk Ratio": round(actual_reward_to_risk, 2),
            "Leverage": round(effective_leverage, 2),
            "Estimated Spread Cost": round(estimated_spread_cost, 2),
            "Known Costs": round(known_costs, 2),
            "Estimated Total Costs": round(estimated_total_costs, 2),
            "Break-even Price": round(break_even_price, price_dp),
            "Estimated Break-even Price": round(estimated_break_even_price, price_dp),
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
    Streamlit-based calculator for designing pairs or multi-leg spread planning scenarios.

    The worksheet records both legs, independent margin settings, stop-loss distances,
    reward-to-risk assumptions, combined risk/reward, and spread context such as ratio,
    volatility, correlation, and z-score.
    """
    st.subheader(f"Pairs / Multi-Leg Spread Planning Worksheet for {asset_name_long} / {asset_name_short}")
    st.caption(
        "Structure long and short legs with independent risk assumptions, margin planning, "
        "historical context, and ratio observations."
    )

    long_dp = _price_precision(long_asset_type)
    short_dp = _price_precision(short_asset_type)

    # --- Long Leg ---
    st.markdown("### Long Leg Setup")
    st.write(f"**{asset_name_long} Price:** {_fmt_price(long_price, long_dp)} | Type: {long_asset_type}")
    stake_long = st.number_input(
        f"Stake-per-Point for {asset_name_long}",
        min_value=0.1, value=1.0, step=0.1, key=f"{asset_name_long}_stake_long"
    )
    long_margin_pct = st.slider(
        f"Broker Margin Requirement (%) for {asset_name_long}",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name_long}_margin_pct_long"
    )
    long_stop_pct = st.slider(
        f"{asset_name_long} Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1,
        key=f"{asset_name_long}_stop_pct_long"
    )
    long_sl_default = (long_stop_pct / 100) * long_price
    override_long_sl = st.number_input(
        f"Override Stop Loss Distance for {asset_name_long} (optional)",
        min_value=0.0, value=0.0, step=_price_step(long_dp), key=f"{asset_name_long}_sl_override_long"
    )
    long_stop_loss = override_long_sl if override_long_sl > 0 else long_sl_default
    long_rrr = st.slider(
        f"Reward-to-Risk Ratio for {asset_name_long}",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name_long}_rrr_long"
    )
    long_target = long_stop_loss * long_rrr
    long_notional = stake_long * long_price
    long_margin = long_notional * (long_margin_pct / 100)
    long_stop_price = long_price - long_stop_loss
    long_target_price = long_price + long_target

    # --- Short Leg ---
    st.markdown("### Short Leg Setup")
    st.write(f"**{asset_name_short} Price:** {_fmt_price(short_price, short_dp)} | Type: {short_asset_type}")
    stake_short = st.number_input(
        f"Stake-per-Point for {asset_name_short}",
        min_value=0.1, value=1.0, step=0.1, key=f"{asset_name_short}_stake_short"
    )
    short_margin_pct = st.slider(
        f"Broker Margin Requirement (%) for {asset_name_short}",
        min_value=3, max_value=50, value=20, step=1, key=f"{asset_name_short}_margin_pct_short"
    )
    short_stop_pct = st.slider(
        f"{asset_name_short} Stop Loss Distance (%)",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1,
        key=f"{asset_name_short}_stop_pct_short"
    )
    short_sl_default = (short_stop_pct / 100) * short_price
    override_short_sl = st.number_input(
        f"Override Stop Loss Distance for {asset_name_short} (optional)",
        min_value=0.0, value=0.0, step=_price_step(short_dp), key=f"{asset_name_short}_sl_override_short"
    )
    short_stop_loss = override_short_sl if override_short_sl > 0 else short_sl_default
    short_rrr = st.slider(
        f"Reward-to-Risk Ratio for {asset_name_short}",
        min_value=1.0, max_value=5.0, value=3.0, step=0.1, key=f"{asset_name_short}_rrr_short"
    )
    short_target = short_stop_loss * short_rrr
    short_notional = stake_short * short_price
    short_margin = short_notional * (short_margin_pct / 100)
    short_stop_price = short_price + short_stop_loss
    short_target_price = short_price - short_target

    # --- Combined Metrics ---
    combined_risk = (stake_long * long_stop_loss) + (stake_short * short_stop_loss)
    combined_reward = (stake_long * long_target) + (stake_short * short_target)
    combined_rrr = _safe_ratio(combined_reward, combined_risk)
    combined_margin = long_margin + short_margin
    combined_notional = long_notional + short_notional

    st.markdown("### Historical Spread Reference & Observations")
    historical_summary = st.text_area(
        "Historical spread context, Z-score levels, or observations (optional)",
        key="pairs_historical_context"
    )
    avg_spread_ratio = st.number_input(
        "Average Spread Ratio (manual entry)",
        min_value=0.0, value=0.0, step=0.0001, key="avg_spread_ratio_manual"
    )
    spread_volatility = st.number_input(
        "Volatility (Std Dev) of spread (manual entry)",
        min_value=0.0, value=0.0, step=0.0001, key="spread_volatility_manual"
    )
    correlation = st.number_input(
        "Correlation (manual entry)",
        min_value=-1.0, max_value=1.0, value=0.0, step=0.01, key="correlation_manual"
    )
    z_score = st.number_input(
        "Z-Score (Deviation from Mean, manual entry)",
        min_value=-5.0, max_value=5.0, value=0.0, step=0.01, key="z_score_manual"
    )
    support_levels = st.text_area(
        "Support Levels (comma-separated, manual entry)", key="support_levels_manual"
    )
    resistance_levels = st.text_area(
        "Resistance Levels (comma-separated, manual entry)", key="resistance_levels_manual"
    )
    drift_notes = st.text_area(
        "Observed drift or additional notes (optional)", key="drift_notes_manual"
    )

    _summary_lines("Combined Planning Summary", [
        ("Gross Exposure", _fmt_money(combined_notional)),
        ("Required Margin", _fmt_money(combined_margin)),
        ("Capital at Risk", _fmt_money(combined_risk)),
        ("Potential Reward", _fmt_money(combined_reward)),
        ("Target Multiplier", f"{combined_rrr:.2f}×"),
    ])

    _summary_lines("Reference Prices", [
        (f"Long {asset_name_long}", f"stop {_fmt_price(long_stop_price, long_dp)}, target {_fmt_price(long_target_price, long_dp)}"),
        (f"Short {asset_name_short}", f"stop {_fmt_price(short_stop_price, short_dp)}, target {_fmt_price(short_target_price, short_dp)}"),
    ])

    universal_fields = universal_trade_fields()
    ref_only = st.checkbox(
        "Mark this trade as reference only (stops not auto-placed)",
        key="ref_only_checkbox"
    )
    notes = st.text_area("Additional Notes (optional)", key="pairs_notes")

    if st.button("➕ Add Spread Planning Scenario to Dashboard", key="add_pairs_trade_btn"):
        trade_data = {
            "Planning Status": "Planned",
            "Asset (Primary)": asset_name_long,
            "Long Asset Type": long_asset_type,
            "Asset (Short Leg)": asset_name_short,
            "Short Asset Type": short_asset_type,
            "Trade Type": "Pairs / Multi-Leg Spread",
            "Trade Direction": "Spread",
            "Long Entry Price (Planned)": long_price,
            "Short Entry Price (Planned)": short_price,
            "Long Position Size (Units)": stake_long,
            "Short Position Size (Units)": stake_short,
            "Long Stake-per-Point": stake_long,
            "Short Stake-per-Point": stake_short,
            "Stop Loss (Planned)": f"Long: {_fmt_price(long_stop_price, long_dp)} | Short: {_fmt_price(short_stop_price, short_dp)}",
            "Take Profit (Planned)": f"Long: {_fmt_price(long_target_price, long_dp)} | Short: {_fmt_price(short_target_price, short_dp)}",
            "Long Margin Required": round(long_margin, 2),
            "Short Margin Required": round(short_margin, 2),
            "Margin Required": round(combined_margin, 2),
            "Notional Exposure": round(combined_notional, 2),
            "Long Stop Loss (pts)": round(long_stop_loss, long_dp),
            "Short Stop Loss (pts)": round(short_stop_loss, short_dp),
            "Long Target (pts)": round(long_target, long_dp),
            "Short Target (pts)": round(short_target, short_dp),
            "Capital at Risk": round(combined_risk, 2),
            "Potential Reward": round(combined_reward, 2),
            "Risk (Combined)": round(combined_risk, 2),
            "Potential Reward (Combined)": round(combined_reward, 2),
            "Reward-to-Risk Ratio": round(combined_rrr, 2),
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
