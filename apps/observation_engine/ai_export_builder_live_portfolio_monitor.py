# -------------------------------------------------------------------------------------------------
# AI Export Snapshot Builder — Live Portfolio Monitor
# -------------------------------------------------------------------------------------------------

from datetime import datetime, UTC
import pandas as pd


def _safe_records(df):
    """Return JSON-safe record dictionaries from a DataFrame."""
    if df is None or df.empty:
        return []

    clean_df = df.copy()

    for column in clean_df.columns:
        if pd.api.types.is_datetime64_any_dtype(clean_df[column]):
            clean_df[column] = clean_df[column].dt.strftime("%Y-%m-%d")

    clean_df = clean_df.astype(object).where(pd.notna(clean_df), None)
    return clean_df.to_dict(orient="records")


def _safe_mapping(value):
    """Return a mapping or an empty mapping when no structured value is supplied."""
    return value if isinstance(value, dict) else {}


def build_macro_insight_snapshot_live_portfolio_monitor(
    theme_code: str,
    theme_title: str,
    portfolio_df,
    filtered_portfolio_df,
    portfolio_summary: dict,
    exposure_summary: dict,
    diagnostic_summary: dict,
    validation: dict | None,
    capital: float,
    base_currency: str,
    global_leverage: float,
    source_label: str,
) -> dict:
    """
    Build an AI-ready snapshot for Live Portfolio Monitor.

    The export preserves the current portfolio state, deterministic exposure calculations,
    structural diagnostics, validation findings, and position context. AI is asked to interpret
    relationships and vulnerabilities rather than recalculate broker or portfolio figures.
    """

    validation = validation or {}
    portfolio_summary = _safe_mapping(portfolio_summary)
    exposure_summary = _safe_mapping(exposure_summary)
    diagnostic_summary = _safe_mapping(diagnostic_summary)

    base_currency = str(base_currency or "USD").strip().upper()
    source_label = str(source_label or "Portfolio Snapshot").strip()

    all_symbols: list[str] = []
    selected_symbols: list[str] = []

    if (
        portfolio_df is not None
        and not portfolio_df.empty
        and "Symbol" in portfolio_df.columns
    ):
        all_symbols = (
            portfolio_df["Symbol"]
            .dropna()
            .astype(str)
            .str.strip()
            .loc[lambda values: values.ne("")]
            .tolist()
        )

    if (
        filtered_portfolio_df is not None
        and not filtered_portfolio_df.empty
        and "Symbol" in filtered_portfolio_df.columns
    ):
        selected_symbols = (
            filtered_portfolio_df["Symbol"]
            .dropna()
            .astype(str)
            .str.strip()
            .loc[lambda values: values.ne("")]
            .tolist()
        )

    portfolio_positions = (
        int(len(portfolio_df))
        if portfolio_df is not None
        else 0
    )

    selected_positions = (
        int(len(filtered_portfolio_df))
        if filtered_portfolio_df is not None
        else 0
    )

    return {
        "snapshot_metadata": {
            "base_asset": source_label,
            "theme": {
                "code": theme_code,
                "title": theme_title,
            },
            "snapshot_timestamp": datetime.now(UTC).isoformat(),
            "asset_type": theme_title,
            "dataset": source_label,
            "module_type": "live_portfolio_monitor",
            "portfolio_scope": {
                "all_symbols": all_symbols,
                "selected_symbols": selected_symbols,
                "portfolio_positions": portfolio_positions,
                "selected_positions": selected_positions,
            },
        },
        "analysis_summary": {
            "account_configuration": {
                "account_capital": float(capital),
                "base_currency": base_currency,
                "global_leverage_default": float(global_leverage),
                "source": source_label,
                "calculation_basis": (
                    "FIT leverage-adjusted structural interpretation. Monetary values are "
                    "expressed in the configured portfolio base currency. Values may differ "
                    "from broker accounting, margin, buying-power, financing, currency-conversion, "
                    "or execution views."
                ),
            },
            "portfolio_summary": portfolio_summary,
            "position_records": _safe_records(filtered_portfolio_df),
            "exposure_summary": exposure_summary,
            "structural_diagnostics": diagnostic_summary,
            "validation": {
                "valid": validation.get("valid"),
                "errors": validation.get("errors", []),
                "warnings": validation.get("warnings", []),
            },
        },
        "metadata": {
            "snapshot_notes": (
                "Generated from Live Portfolio Monitor. Figures are FIT portfolio diagnostics "
                "derived from the supplied snapshot, configured base currency, and capital "
                "assumptions. They do not replace broker records, statements, margin calculations, "
                "currency-conversion records, or account analytics."
            ),
            "ai_review_instruction": (
                "Review this Live Portfolio Monitor snapshot as a structural interpretation of the "
                "current portfolio. Use the supplied calculations and validation outputs as given; "
                "do not recalculate P&L, exposure, leverage, margin, buying power, or broker account "
                "figures. Examine visible concentration across positions, sectors, countries, "
                "strategies, direction, and leverage. Identify overlapping exposures, shared "
                "assumptions, potential hidden concentration, and structural vulnerabilities that "
                "may affect several positions together. Distinguish confirmed portfolio facts from "
                "inferences. Note missing context and areas that warrant further investigation. "
                "Do not recommend trades, position changes, investment actions, or performance "
                "predictions."
            ),
        },
    }
