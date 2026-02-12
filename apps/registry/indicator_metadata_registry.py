# -------------------------------------------------------------------------------------------------
# 📚 Indicator Metadata Registry
#  Trade Timing & Confirmation
#  Price Action
# -------------------------------------------------------------------------------------------------
# Structured per locked metadata_indicators and AI export requirements.
# -------------------------------------------------------------------------------------------------

TRADE_TIMING_METADATA = {

    "Naked Charts": {
        "overview": "Discretionary visual inspection of raw price charts without indicators.",
        "why_it_matters": "Helps maintain objectivity and reduce overreliance on signals.",
        "Categories": [],
        "Description": "Pure price-action scanning without overlays or technical tools.",
        "indicators": {}
    },

    "General Market Overview": {
        "overview": "Provides a basic overview of current market technicals without predefined directional bias.",
        "why_it_matters": "Helps orient traders to the current technical state before taking a stance.",
        "Categories": ["Trend Confirmation", "Volatility & Risk"],
        "Description": "Initial scan using broad indicators to frame market structure and volatility.",
        "indicators": {
            "Simple Moving Average": {
                "overview": "A trend-following indicator that calculates the average price over a fixed number of periods.",
                "why_it_matters": "Helps smooth out short-term fluctuations and highlights overall trend direction.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Entry confirmation and trend continuation alignment."
            },
            "Bollinger Bands": {
                "overview": "Price envelope plotted at standard deviation levels above/below a moving average.",
                "why_it_matters": "Used to identify breakout setups and gauge volatility compression.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Core tool for mean reversion and volatility playbooks."
            }
        }
    },

    "Trend Strength & Direction": {
        "overview": "Evaluates the strength and direction of the prevailing market trend using trend-following indicators.",
        "why_it_matters": "Understanding the dominant trend helps align trades with momentum and avoid counter-trend setups.",
        "Categories": ["Trend Confirmation"],
        "Description": "Confirms trend strength and directionality using key moving averages.",
        "indicators": {
            "Average Directional Index": {
                "overview": "Measures trend strength without regard to direction.",
                "why_it_matters": "High ADX values indicate strong trends, useful for filtering entries.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟🌟 – Filters entries based on trending vs ranging conditions."
            },
            "Simple Moving Average": {
                "overview": "Basic trend confirmation via smoothing.",
                "why_it_matters": "Clarifies directional bias over a defined period.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Entry timing and bias alignment."
            },
            "Exponential Moving Average": {
                "overview": "A weighted moving average that gives more importance to recent prices.",
                "why_it_matters": "Responds faster to price changes than SMA, helping with timely entries.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Often used for entry triggers and dynamic support/resistance."
            }
        }
    },

    "Reversal Identification": {
        "overview": "Detects when current trends may be weakening or reversing using key signal indicators.",
        "why_it_matters": "Supports traders in identifying early inflection points.",
        "Categories": ["Trend Reversal", "Setup Triggers"],
        "Description": "Tools used to identify potential trend exhaustion or reversals.",
        "indicators": {
            "Average Directional Index": {
                "overview": "Measures trend strength without regard to direction.",
                "why_it_matters": "A declining ADX during a strong trend may signal weakening momentum.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟 – Assists in detecting fading trends."
            },
            "Super Trend": {
                "overview": "Trend-following overlay that adjusts with volatility and direction.",
                "why_it_matters": "Useful for highlighting shifts in market direction.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Confirms reversals and stop-loss placement."
            },
            "Parabolic SAR": {
                "overview": "Time/price-based indicator showing potential trend reversals.",
                "why_it_matters": "Signals exits or reversals when dots flip sides.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Tight trailing exit and reversal marker."
            }
        }
    },

    "Momentum Reversal Signals": {
        "overview": "Momentum oscillators identifying oversold/overbought and divergence setups.",
        "why_it_matters": "Highlights potential exhaustion points for trend reversals.",
        "Categories": ["Momentum", "Mean Reversion"],
        "Description": "Oscillators used to detect extremes and signal reversals.",
        "indicators": {
            "Moving Average Convergence Divergence": {
                "overview": "Measures the relationship between two EMAs.",
                "why_it_matters": "MACD crossovers and divergence signal shifts in momentum.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Core tool for momentum reversal confirmation."
            },
            "Relative Strength Index": {
                "overview": "Compares magnitude of recent gains to losses.",
                "why_it_matters": "Overbought/oversold levels and divergences signal potential reversals.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Widely used for swing entries and exits."
            },
            "Chande Momentum Oscillator": {
                "overview": "Combines up and down days to assess momentum.",
                "why_it_matters": "Offers a smoothed alternative to RSI for trend reversal anticipation.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Alternate oscillator for secondary confirmation."
            }
        }
    },

    "Institutional Activity & Trend Validity": {
        "overview": "Assesses whether price moves are supported by institutional volume.",
        "why_it_matters": "Validates trend quality and uncovers smart money participation.",
        "Categories": ["Volume Analysis"],
        "Description": "Volume-derived indicators for trend strength and conviction.",
        "indicators": {
            "On Balance Volume": {
                "overview": "Cumulative volume-based indicator aligning with price direction.",
                "why_it_matters": "Rising OBV confirms accumulation; divergences flag warnings.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟 – Institutional volume confirmation and divergence spotting."
            },
            "Accumulation/Distribution Line": {
                "overview": "Price-volume indicator that distinguishes between buying and selling pressure.",
                "why_it_matters": "Tracks institutional support or distribution below the surface.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟 – Smart money flow identification."
            }
        }
    },

    "Risk & Expected Price Swings": {
        "overview": "Measures expected volatility and defines stop/target zones.",
        "why_it_matters": "Essential for position sizing and tactical trade design.",
        "Categories": ["Risk Management"],
        "Description": "Indicators measuring volatility and swing potential.",
        "indicators": {
            "Average True Range": {
                "overview": "Measures average range of price over a lookback period.",
                "why_it_matters": "Defines stop loss buffer and trade volatility profile.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Volatility-informed risk calibration."
            },
            "Bollinger Bands": {
                "overview": "Price envelope plotted at standard deviation levels.",
                "why_it_matters": "Visualises expected range and breakout potential.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Supplementary volatility framing."
            },
            "Standard Deviation": {
                "overview": "Statistical measure of dispersion from mean price.",
                "why_it_matters": "Quantifies variability to support range-bound or breakout assumptions.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Auxiliary volatility estimator."
            }
        }
    },

    "Reversal & Continuation Patterns": {
        "overview": "Visual price formations signalling potential reversals or continuations.",
        "why_it_matters": "Adds contextual confirmation based on price action psychology.",
        "Categories": ["Pattern Recognition"],
        "Description": "Patterns formed by price movements providing narrative signals.",
        "indicators": {
            "Candlestick Patterns": {
                "overview": "Sequences of price bars with predictive historical tendencies.",
                "why_it_matters": "Provides early signals based on trader sentiment shifts.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Crucial for discretionary confirmation setups."
            },
            "Head & Shoulders": {
                "overview": "Reversal pattern indicating trend exhaustion and potential reversal.",
                "why_it_matters": "Used for identifying exhaustion zones and breakout thresholds.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟 – Pattern-based swing trade framing."
            },
            "Flags & Pennants": {
                "overview": "Continuation patterns suggesting trend resumption after consolidation.",
                "why_it_matters": "Supports trend continuation bias with measured move targets.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Trend-following re-entry signals."
            },
            "Double Tops/Bottoms": {
                "overview": "Reversal formations marking failed trend continuation.",
                "why_it_matters": "Common signal for trade exits or trend change confirmation.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟 – Confirmation for reversal bias."
            }
        }
    }
}


PRICE_ACTION_METADATA = {

    "Naked Charts": {
        "overview": "Discretionary visual inspection of raw price charts without indicators.",
        "why_it_matters": "Helps maintain objectivity and reduce overreliance on signals.",
        "Categories": [],
        "Description": "Pure price-action scanning without overlays or technical tools.",
        "indicators": {}
    },

    "Performance": {
        "overview": "Assesses historical trade outcomes and net directional progress.",
        "why_it_matters": "Understanding return consistency and volatility helps evaluate price reliability.",
        "Categories": ["Performance"],
        "Description": "Evaluates directional consistency, return volatility, and net price movement.",
        "indicators": {
            "Winning vs. Losing": {
                "overview": "Tracks frequency and magnitude of positive vs. negative price periods.",
                "why_it_matters": "Aids in recognising directional persistence and downside risk.",
                "temporal_categorisation": "Multi-Timeframe",
                "investment_action_importance": "🌟 – Core for trend-following conviction."
            },
            "Rolling Returns": {
                "overview": "Measures returns across shifting time windows.",
                "why_it_matters": "Identifies smoothing effects and performance decay or acceleration.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟 – Important for tactical entry refinement."
            },
            "Volatility-Adjusted Returns": {
                "overview": "Normalises returns by volatility to assess risk efficiency.",
                "why_it_matters": "Separates high-return but erratic assets from stable outperformers.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟 – Filters for tradable quality."
            },
            "Momentum Score": {
                "overview": "Quantifies directional strength over a set lookback window.",
                "why_it_matters": "Detects early continuation or potential stalling patterns.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Initial signal for trade review."
            },
            "Net Price Movement": {
                "overview": "Captures absolute directional movement between start and end points.",
                "why_it_matters": "Useful for visual trend confirmation and noise filtering.",
                "temporal_categorisation": "Short to Long-Term",
                "investment_action_importance": "🌟 – Contextual visual reinforcement."
            }
        }
    },

    "Trend & Momentum": {
        "overview": "Assesses directional strength, trend sustainability, and momentum quality.",
        "why_it_matters": "Trend persistence and quality can influence entry precision and stop placement.",
        "Categories": ["Trend & Momentum"],
        "Description": "Assesses directional strength, trend sustainability, and momentum quality.",
        "indicators": {
            "Price Rate of Change": {
                "overview": "Measures the velocity of price change over time.",
                "why_it_matters": "Highlights acceleration or deceleration in price trends.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Useful for early trend confirmation."
            },
            "Price Action Momentum": {
                "overview": "Evaluates strength of directional moves using raw price structures.",
                "why_it_matters": "Captures clean momentum without indicator smoothing.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Favoured in discretionary price-action models."
            },
            "Trend Confirmation (Higher Highs / Lower Lows)": {
                "overview": "Detects consistent breakouts above or below prior price swings.",
                "why_it_matters": "Fundamental building block for structural trend confirmation.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟🌟 – Foundational trend-following trigger."
            },
            "Momentum Strength": {
                "overview": "Ranks directional conviction based on magnitude and consistency.",
                "why_it_matters": "Separates strong impulse moves from weak drift.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Secondary signal layer for tactical entry."
            },
            "Price Acceleration": {
                "overview": "Captures curvature or slope change in price trend.",
                "why_it_matters": "Helps detect inflection points and trend exhaustion.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Often used as precursor to reversal scanning."
            },
            "Volume-Based Confirmation": {
                "overview": "Validates trend or momentum with supporting volume patterns.",
                "why_it_matters": "Volume underpins commitment; lack of it weakens conviction.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Confirmation layer for conviction."
            },
            "Support/Resistance Validation": {
                "overview": "Tests whether price breaks or holds key historical zones.",
                "why_it_matters": "Confirms directional strength or identifies rejection zones.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟 – Reinforces structural conviction."
            }
        }
    },

    "Breakout & Mean Reversion": {
        "overview": "Detects breakout signals, compression setups, and volatility expansions.",
        "why_it_matters": "Key to identifying explosive setups or reversion risk.",
        "Categories": ["Breakout & Mean Reversion"],
        "Description": "Detects breakout signals, compression setups, and volatility expansions.",
        "indicators": {
            "Bollinger Band Expansion": {
                "overview": "Tracks volatility widening to confirm breakout potential.",
                "why_it_matters": "Breakouts often follow periods of band contraction.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Early alert for volatility expansion."
            },
            "Price Breakout vs. Mean Reversion": {
                "overview": "Assesses whether price is extending or returning to norm.",
                "why_it_matters": "Distinguishes continuation from exhaustion patterns.",
                "temporal_categorisation": "Short to Medium-Term",
                "investment_action_importance": "🌟🌟 – Core trigger for strategy selection."
            },
            "ATR Volatility Trends": {
                "overview": "Tracks average true range dynamics over time.",
                "why_it_matters": "Provides insight into breakout fuel or fading risk.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟 – Secondary confirmation tool."
            },
            "Standard Deviation of Price Swings": {
                "overview": "Measures dispersion of price movements around the mean.",
                "why_it_matters": "Elevated deviation can indicate regime shift or instability.",
                "temporal_categorisation": "Medium-Term",
                "investment_action_importance": "🌟 – Volatility insight for breakout context."
            },
            "Volume vs. Price Range Compression": {
                "overview": "Compares range narrowing to volume behaviour.",
                "why_it_matters": "Tight range with high volume often precedes breakout.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "🌟🌟 – Compression detector for entry planning."
            }
        }
    }
}

# -------------------------------------------------------------------------------------------------
# ✅ END — Canonical Metadata Registry (Platinum Grade)
# -------------------------------------------------------------------------------------------------
