# -------------------------------------------------------------------------------------------------
# Positioning Data Processing
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
processing_positioning.py

Utilities for the Positioning & Crowding module.

Purpose:
- discover available positioning markets from cleaned CSV files
- load weekly positioning data and matching weekly market overlay data
- derive positioning metrics such as net positioning, net % OI, percentile, and flip
- return a compact summary payload for the page layer
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------------------------------
POSITIONING_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__))
)

DEFAULT_ASSET_FILE = os.path.join(POSITIONING_PATH, "cots_assets_default.csv")

# -------------------------------------------------------------------------------------------------
# Market Config
# -------------------------------------------------------------------------------------------------
POSITIONING_MARKET_MAP = {
    "aud_positioning": {
        "label": "AUD Positioning",
        "positioning_file": "aud_positioning.csv",
        "asset_column": "aud_usd",
        "market_price_label": "AUD/USD",
    },
    "eur_positioning": {
        "label": "EUR Positioning",
        "positioning_file": "eur_positioning.csv",
        "asset_column": "eur_usd",
        "market_price_label": "EUR/USD",
    },
    "gbp_positioning": {
        "label": "GBP Positioning",
        "positioning_file": "gbp_positioning.csv",
        "asset_column": "gbp_usd",
        "market_price_label": "GBP/USD",
    },
    "jpy_positioning": {
        "label": "JPY Positioning",
        "positioning_file": "jpy_positioning.csv",
        "asset_column": "usd_jpy",
        "market_price_label": "USD/JPY",
    },
    "usd_index_positioning": {
        "label": "USD Index Positioning",
        "positioning_file": "usd_index_positioning.csv",
        "asset_column": "dxy",
        "market_price_label": "DXY",
    },
    "ust_2y_positioning": {
        "label": "UST 2Y Positioning",
        "positioning_file": "ust_2y_positioning.csv",
        "asset_column": "us2y",
        "market_price_label": "US 2Y",
    },
    "ust_10y_positioning": {
        "label": "UST 10Y Positioning",
        "positioning_file": "ust_10y_positioning.csv",
        "asset_column": "us10y",
        "market_price_label": "US 10Y",
    },
    "russell2000_positioning": {
        "label": "Russell 2000 Positioning",
        "positioning_file": "russell2000_positioning.csv",
        "asset_column": "russell2000",
        "market_price_label": "Russell 2000",
    },
    "sp500_positioning": {
        "label": "S&P 500 Positioning",
        "positioning_file": "sp500_positioning.csv",
        "asset_column": "sp500",
        "market_price_label": "S&P 500",
    },
    "vix_positioning": {
        "label": "VIX Positioning",
        "positioning_file": "vix_positioning.csv",
        "asset_column": "vix",
        "market_price_label": "VIX",
    },
    "silver_positioning": {
        "label": "Silver Positioning",
        "positioning_file": "silver_positioning.csv",
        "asset_column": "silver",
        "market_price_label": "Silver",
    },
    "gold_positioning": {
        "label": "Gold Positioning",
        "positioning_file": "gold_positioning.csv",
        "asset_column": "gold",
        "market_price_label": "Gold",
    },
}

# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
def _safe_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def _load_positioning_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = [
        "leveraged_long",
        "leveraged_short",
        "change_long",
        "change_short",
        "open_interest_long_pct",
        "open_interest_short_pct",
    ]
    for col in numeric_cols:
        df[col] = _safe_numeric(df[col])

    df = df.dropna(subset=["date"]).copy()
    df = df.sort_values("date").drop_duplicates(subset=["date"])

    df["net_position"] = df["leveraged_long"] - df["leveraged_short"]
    df["net_position_change"] = df["net_position"].diff()
    df["net_open_interest_pct"] = df["open_interest_long_pct"] - df["open_interest_short_pct"]
    df["abs_net_open_interest_pct"] = df["net_open_interest_pct"].abs()

    return df


def _load_default_assets() -> pd.DataFrame:
    df = pd.read_csv(DEFAULT_ASSET_FILE)
    df.columns = df.columns.str.strip()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in df.columns:
        if col != "date":
            df[col] = _safe_numeric(df[col])

    df = df.dropna(subset=["date"]).copy()
    df = df.sort_values("date").drop_duplicates(subset=["date"])
    return df


def _compute_percentile(series: pd.Series) -> float:
    clean = series.dropna()
    if clean.empty:
        return np.nan

    current = clean.iloc[-1]
    return float((clean <= current).mean() * 100)


def _compute_positioning_turn(net_series: pd.Series) -> str:
    clean = net_series.dropna()
    if len(clean) < 2:
        return "No Recent Regime Turn"

    prev_val = clean.iloc[-2]
    curr_val = clean.iloc[-1]

    if prev_val <= 0 < curr_val:
        return "Shift Towards Net Long Positioning"
    if prev_val >= 0 > curr_val:
        return "Shift Towards Net Short Positioning"
    return "No Recent Regime Turn"


def _compute_structural_state(percentile: float, net_value: float) -> str:
    if pd.isna(percentile) or pd.isna(net_value):
        return "N/A"

    if percentile >= 90:
        return "Crowded Long" if net_value > 0 else "Crowded Short"
    if percentile <= 10:
        return "Crowded Short" if net_value < 0 else "Crowded Long"
    if percentile >= 75 or percentile <= 25:
        return "Moving Towards Extreme"
    return "Within Historical Range"


def _build_contextual_interpretation(
    market_label: str,
    structural_state: str,
    percentile: float,
    positioning_turn: str
) -> str:
    if structural_state == "Crowded Long":
        return (
            f"{market_label} remains skewed toward net long exposure, "
            f"with positioning concentrated near the upper end of its recent range."
        )

    if structural_state == "Crowded Short":
        return (
            f"{market_label} remains skewed toward net short exposure, "
            f"with positioning concentrated near the lower end of its recent range."
        )

    if structural_state == "Moving Towards Extreme":
        return (
            f"{market_label} is moving away from neutral positioning, "
            f"with exposure building toward a more concentrated regime."
        )

    return (
        f"{market_label} remains broadly within its recent historical range, "
        f"without a clear structural positioning extreme."
    )

# -------------------------------------------------------------------------------------------------
# Public Functions
# -------------------------------------------------------------------------------------------------
def get_available_positioning_markets() -> list[tuple[str, str]]:
    """
    Returns available positioning markets as:
    (slug, display_label)

    Example:
    [
        ("aud_positioning", "AUD Positioning"),
        ("gold_positioning", "Gold Positioning"),
    ]
    """
    available = []

    for slug, cfg in POSITIONING_MARKET_MAP.items():
        path = os.path.join(POSITIONING_PATH, cfg["positioning_file"])

        if os.path.exists(path):
            available.append(
                (
                    slug,
                    cfg.get("label", slug)
                )
            )

    return available


def load_positioning_market_bundle(
    market_slug: str,
    lookback_window: int,
    project_path: str | None = None  # kept for signature consistency
) -> dict:
    messages: list[str] = []

    cfg = POSITIONING_MARKET_MAP.get(market_slug)
    if cfg is None:
        return {
            "positioning_df": pd.DataFrame(),
            "overlay_df": pd.DataFrame(),
            "summary_payload": {},
            "messages": [f"Unknown positioning market: {market_slug}"],
        }

    positioning_path = os.path.join(POSITIONING_PATH, cfg["positioning_file"])
    if not os.path.exists(positioning_path):
        return {
            "positioning_df": pd.DataFrame(),
            "overlay_df": pd.DataFrame(),
            "summary_payload": {},
            "messages": [f"Positioning file not found: {cfg['positioning_file']}"],
        }

    if not os.path.exists(DEFAULT_ASSET_FILE):
        return {
            "positioning_df": pd.DataFrame(),
            "overlay_df": pd.DataFrame(),
            "summary_payload": {},
            "messages": ["Default positioning asset file not found: cots_assets_default.csv"],
        }

    positioning_df = _load_positioning_csv(positioning_path)
    assets_df = _load_default_assets()

    asset_column = cfg["asset_column"]
    if asset_column not in assets_df.columns:
        messages.append(f"Weekly asset column not found: {asset_column}")
        overlay_df = positioning_df.copy()
        overlay_df["market_price"] = np.nan
    else:
        overlay_asset = assets_df[["date", asset_column]].copy()
        overlay_asset = overlay_asset.rename(columns={
            "date": "asset_week_end",
            asset_column: "market_price"
        })

        positioning_merge = positioning_df.copy()
        positioning_merge["asset_week_end"] = positioning_merge["date"] + pd.offsets.Week(weekday=6)

        overlay_df = pd.merge(
            positioning_merge,
            overlay_asset,
            on="asset_week_end",
            how="left"
        )

    positioning_df = positioning_df.tail(lookback_window).copy()
    overlay_df = overlay_df.tail(lookback_window).copy()

    positioning_df["net_position_share_pct"] = positioning_df["net_open_interest_pct"]

    percentile = _compute_percentile(positioning_df["net_position_share_pct"])
    positioning_turn = _compute_positioning_turn(positioning_df["net_position_share_pct"])

    current_net_position = (
        positioning_df["net_position"].iloc[-1]
        if not positioning_df.empty else np.nan
    )
    current_net_pct = (
        positioning_df["net_open_interest_pct"].iloc[-1]
        if not positioning_df.empty else np.nan
    )

    structural_state = _compute_structural_state(percentile, current_net_position)

    summary_payload = {
        "market_slug": market_slug,
        "market_label": cfg["label"],
        "market_price_label": cfg["market_price_label"],
        "structural_state": structural_state,
        "current_net_position": current_net_position,
        "current_net_pct": current_net_pct,
        "positioning_percentile": percentile,
        "positioning_turn": positioning_turn,
        "contextual_interpretation": _build_contextual_interpretation(
            cfg["label"],
            structural_state,
            percentile,
            positioning_turn
        ),
    }

    return {
        "positioning_df": positioning_df,
        "overlay_df": overlay_df,
        "summary_payload": summary_payload,
        "messages": messages,
    }


def build_positioning_summary_table(positioning_df: pd.DataFrame) -> pd.DataFrame:
    if positioning_df.empty:
        return pd.DataFrame()

    table_df = positioning_df.copy()

    keep_cols = [
        "date",
        "market_name",
        "leveraged_long",
        "leveraged_short",
        "net_position",
        "change_long",
        "change_short",
        "net_position_change",
        "open_interest_long_pct",
        "open_interest_short_pct",
        "net_open_interest_pct",
    ]
    keep_cols = [col for col in keep_cols if col in table_df.columns]

    table_df = table_df[keep_cols].copy()
    table_df["date"] = pd.to_datetime(table_df["date"]).dt.date

    table_df.rename(columns={
        "market_name": "Market",
        "leveraged_long": "Leveraged Positions — Long",
        "leveraged_short": "Leveraged Positions — Short",
        "change_long": "Change in Long Positions",
        "change_short": "Change in Short Positions",
        "net_position": "Net Position",
        "net_position_change": "Net Position Change",
        "open_interest_long_pct": "Long Position Share (%)",
        "open_interest_short_pct": "Short Position Share (%)",
        "net_open_interest_pct": "Net Position Share (%)",
    }, inplace=True)

    return table_df.sort_values("date", ascending=False).reset_index(drop=True)
