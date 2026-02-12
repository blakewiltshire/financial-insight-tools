STATISTICAL_METADATA = {
    "descriptive_statistics": {
        "Measure of Central Tendency": {
            "overview": "Summarises the central value around which asset returns cluster, using mean, median, and mode.",
            "why_it_matters": "Provides baseline expectations for typical price behaviour and return anchoring.",
            "temporal_categorisation": "Medium-Term",
            "investment_action_importance": "🌟 – Useful for establishing trend bias and average return assumptions."
        },
        "Measures of Dispersion": {
            "overview": "Captures the spread and volatility of returns using standard deviation, variance, and range.",
            "why_it_matters": "Reveals the variability and potential risk associated with price movements.",
            "temporal_categorisation": "Short to Medium-Term",
            "investment_action_importance": "🌟🌟 – Central to risk estimation, stop placement, and portfolio stress testing."
        },
        "Measures of Shape": {
            "overview": "Describes asymmetry (skewness) and tail risk (kurtosis) of the return distribution.",
            "why_it_matters": "Helps assess whether returns exhibit unusual patterns or extremes beyond normal distributions.",
            "temporal_categorisation": "Short to Medium-Term",
            "investment_action_importance": "🌟 – Important for volatility targeting and risk-adjusted strategy design."
        },
        "Basic Statistics": {
            "overview": "Includes extreme values, return totals, and observation counts for general context.",
            "why_it_matters": "Provides foundational framing for all calculations, and helps validate sample robustness.",
            "temporal_categorisation": "Meta to Long-Term",
            "investment_action_importance": "⭐ – Informational context; critical when comparing multiple datasets."
        }
    },
    "risk_and_uncertainty_analysis": {
        "Risk-Adjusted Returns (Sharpe Ratio)": {
            "overview": "Evaluates how much return was generated per unit of total risk (volatility).",
            "why_it_matters": "Used as a benchmark for comparing investment efficiency across assets or strategies.",
            "temporal_categorisation": "Medium-Term",
            "investment_action_importance": "🌟🌟 – Core metric in portfolio construction, performance attribution, and fund comparison."
        },
        "Downside Risk Measure (Sortino Ratio)": {
            "overview": "Assesses return relative to downside deviation, focusing on negative volatility only.",
            "why_it_matters": "Prioritises capital preservation and penalises harmful volatility more heavily.",
            "temporal_categorisation": "Medium-Term",
            "investment_action_importance": "🌟🌟 – Preferred for conservative or risk-sensitive investment profiles."
        },
        "Probability of Hitting DPT": {
            "overview": "Estimates the likelihood of achieving a user-defined directional price target.",
            "why_it_matters": "Informs trade planning, profit-taking, and expectation alignment based on historical hit rates.",
            "temporal_categorisation": "Short-Term",
            "investment_action_importance": "🌟🌟 – Critical input for trade setup realism and reward calibration."
        }
    },
    "market_dynamics": {
        "Volatility Ratio": {
            "overview": "Assesses changes in volatility patterns using comparative ratio analysis.",
            "why_it_matters": "Highlights market regime shifts, ranging conditions, or elevated uncertainty.",
            "temporal_categorisation": "Short-Term",
            "investment_action_importance": "🌟 – Helps determine whether to apply trend-following or mean-reversion models."
        },
        "ATR (Average True Range)": {
            "overview": "Measures recent absolute price movement to determine real-time volatility.",
            "why_it_matters": "Used to set position size, stop-loss distances, and confirm volatility regime.",
            "temporal_categorisation": "Short-Term",
            "investment_action_importance": "🌟🌟 – Operationally essential in risk-based position sizing models."
        }
    },
    "performance_metrics": {
        "Annualised Return": {
            "overview": "Normalises total return to an annual rate for time-consistent comparison.",
            "why_it_matters": "Allows strategy evaluation across periods with different durations.",
            "temporal_categorisation": "Long-Term",
            "investment_action_importance": "🌟🌟 – Central to evaluating the sustainability and strength of returns."
        },
        "Maximum Drawdown": {
            "overview": "Measures the deepest historical capital loss from peak to trough.",
            "why_it_matters": "Sets expectations for worst-case scenarios and portfolio recovery needs.",
            "temporal_categorisation": "Long-Term",
            "investment_action_importance": "🌟🌟 – Core defensive metric in capital protection strategies."
        },
        "Volatility-Adjusted Return": {
            "overview": "Scales returns by volatility to assess efficiency of capital deployment.",
            "why_it_matters": "Reveals whether gains are commensurate with risk levels taken.",
            "temporal_categorisation": "Medium-Term",
            "investment_action_importance": "🌟 – Valuable when comparing strategies or asset classes."
        },
        "Return on Investment (ROI)": {
            "overview": "Simple gross return metric for a given period, expressed as a percentage.",
            "why_it_matters": "Quickly communicates headline performance, especially for discrete trades.",
            "temporal_categorisation": "Long-Term",
            "investment_action_importance": "🌟 – Commonly used for marketing, trade review, and benchmarking."
        },
        "Volume vs ATR Correlation": {
            "correlation": {
                "overview": "Tracks relationship between price volatility and trading activity.",
                "why_it_matters": "May signal regime shifts or validate trends when high volume aligns with volatility.",
                "temporal_categorisation": "Short-Term",
                "investment_action_importance": "⭐ – Useful diagnostic for confirming price action credibility."
            }
        }
    }
}
