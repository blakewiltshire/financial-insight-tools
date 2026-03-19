# thematic_groupings.py

THEMATIC_GROUPS = {
    "000_template": {
        "theme_title": "🧩 Thematic Grouping Template",
        "theme_introduction": "This entry provides a structural reference for building "
        "new thematic groupings within the Economic Exploration system. It is not linked "
        "to live data but defines the metadata layout and schema used across all themes.",
        "temporal_categorisation": {
            "coincident_indicators": "",
            "leading_indicators": "",
            "lagging_indicators": ""
        },
        "template": {
            "blank_template": "."
        },
        "data_points": [
            "Historical Trends: ",
            "Comparative Analysis: ",
            "Policy Impact Assessment: "
        ],
        "navigating_the_theme": "This theme acts as a deployment scaffold only. Replace all "
        "placeholder values when implementing a live country-theme module.",
        "memberships": {
            "001_signal_a": {
                "Use Case": "Placeholder Use Case A",
                "title": "Signal A Group",
                "overview": "This placeholder group contains Signal A.",
                "why_it_matters": "Demonstrates structure for an early-stage insight group.",
                "temporal_categorisation": "Leading Indicator",
                "investment_action_importance": "Placeholder rating",
                "personal_impact_importance": "Placeholder rating",
                "current_vs_previous": "No real data – placeholder only.",
                "points_percentage_changes": "N/A",
                "min_max_12months": "N/A",
                "averages": "N/A",
                "year_over_year": "N/A",
                "recommended_time_periods": [],
                "path": "default_template/pages/000_🧩_template.py"
            },
            "002_signal_b": {
                "Use Case": "Placeholder Use Case A",
                "title": "Signal B Group",
                "overview": "This group includes placeholder signal B for testing.",
                "why_it_matters": "Used to validate UI structure and insight group logic.",
                "temporal_categorisation": "Coincident Indicator",
                "investment_action_importance": "Placeholder rating",
                "personal_impact_importance": "Placeholder rating",
                "current_vs_previous": "No real data – placeholder only.",
                "points_percentage_changes": "N/A",
                "min_max_12months": "N/A",
                "averages": "N/A",
                "year_over_year": "N/A",
                "recommended_time_periods": [],
                "path": "default_template/pages/000_🧩_template.py"
            },
            "003_signal_c": {
                "Use Case": "Placeholder Use Case B",
                "title": "Signal C Group",
                "overview": "Standalone signal group under Use Case B.",
                "why_it_matters": "Final example group for template scaffolding.",
                "temporal_categorisation": "Lagging Indicator",
                "investment_action_importance": "Placeholder rating",
                "personal_impact_importance": "Placeholder rating",
                "current_vs_previous": "No real data – placeholder only.",
                "points_percentage_changes": "N/A",
                "min_max_12months": "N/A",
                "averages": "N/A",
                "year_over_year": "N/A",
                "recommended_time_periods": [],
                "path": "default_template/pages/000_🧩_template.py"
            },
        }
    },

    "100_economic_growth_stability": {
        "theme_title": "Economic Growth and Stability",
        "theme_introduction": "Economic growth and stability represent core system-level metrics for evaluating national economic dynamics, resilience, and expansion capacity.",
        "temporal_categorisation": {
            "coincident_indicators": "Indicators that reflect the current state of the economy.",
            "leading_indicators": "Indicators that signal future economic trends, useful for anticipating shifts in market dynamics.",
            "lagging_indicators": "Indicators that confirm long-term economic trends, used to validate earlier movements."
        },
        "template": {
            "gdp_template": "GDP Template – For GDP growth rate, nominal GDP, and breakdown components.",
            "gdp_macro_composite_template": "Composite & Leading Macro Indicators Template – For aggregate or forward-looking macro indices."
        },
        "data_points": [
            "Historical Trends: Review past performance to understand economic cycles and volatility.",
            "Comparative Analysis: Compare economic indicators across countries and time periods.",
            "Policy Impact Assessment: Evaluate the effects of monetary and fiscal policy on growth trends."
        ],
        "navigating_the_theme": "This theme structures GDP indicators and composite macro signals as aligned frameworks to observe expansion velocity, output composition, and policy interaction layers.",
        "conclusion_and_further_exploration": "GDP-related and leading macro indicators serve as composite signals reflecting expansion dynamics, volatility bands, and regime transitions across economic cycles.",
        "memberships": {
            "101_real_gdp": {
                "Use Case": "GDP Signals",
                "title": "Real GDP",
                "template": "gdp_template",
                "overview": "Real GDP measures the inflation-adjusted value of economic output, reflecting the pace of expansion or contraction in an economy.",
                "why_it_matters": "A foundational metric for assessing the health of an economy. Real GDP is used to track business cycles, anticipate shifts in macro conditions, and evaluate momentum in growth. Often referenced in market and policy commentary.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 – Provides insight into economic momentum, sector sensitivity, and cyclical positioning, supporting top-down portfolio context.",
                "personal_impact_importance": "🌟🌟🌟 – Influences employment stability, wage trends, and cost-of-living dynamics—key factors in household planning.",
                "current_vs_previous": "Compares the latest GDP figures to previous quarters to assess acceleration or deceleration in economic activity.",
                "points_percentage_changes": "Tracks both absolute GDP changes and percentage growth rates to gauge scale and intensity.",
                "min_max_12months": "Highlights the highest and lowest GDP readings over the past year for volatility context.",
                "averages": "Calculates running averages to help identify sustained growth or contraction trends.",
                "year_over_year": "Compares GDP values with the same period last year to provide a broader historical perspective.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },
            "102_nominal_gdp": {
                "Use Case": "GDP Signals",
                "title": "Nominal GDP",
                "template": "gdp_template",
                "overview": "Nominal GDP captures the value of economic output using current market prices, without inflation adjustment.",
                "why_it_matters": "Useful for understanding market size and pricing trends. Supports comparison of economic scale across countries.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Offers insight into scale and nominal growth trends that may impact equity markets or sector strength.",
                "personal_impact_importance": "🌟 - Reflects the nominal economic size influencing household confidence and fiscal outlooks.",
                "current_vs_previous": "Evaluates current nominal output against previous data.",
                "points_percentage_changes": "Measures nominal fluctuations, helpful for pricing and tax-related assessments.",
                "min_max_12months": "Shows highest and lowest values over the past year.",
                "averages": "Smooths out noise to display ongoing trendlines.",
                "year_over_year": "Supports broader trend analysis.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },
            "103_gdp_components_breakdown": {
                "Use Case": "GDP Signals",
                "title": "GDP Components Breakdown",
                "template": "gdp_template",
                "overview": "GDP component analysis breaks down economic output into key sectors such as consumption, investment, government spending, and net exports.",
                "why_it_matters": "The contributions of each GDP component can help identify the drivers behind economic growth or contraction, aiding in macroeconomic and sector analysis.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Highlights which sectors are contributing to growth dynamics, supporting top-down contextual understanding.",
                "personal_impact_importance": "🌟🌟 - Reveals shifts in consumption, investment, and trade that affect household and employment trends.",
                "current_vs_previous": "Examines the recent shifts in component contributions versus prior data.",
                "points_percentage_changes": "Shows percentage weight changes in each GDP category.",
                "min_max_12months": "Highlights peak and trough contribution from major GDP drivers.",
                "averages": "Smooths volatility across components for trend awareness.",
                "year_over_year": "Compares current GDP composition to the same period last year for structural insights.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },
            "104_conference_board_leading_index": {
                "Use Case": "Macro Composite Signals",
                "title": "Leading Growth Index (Conference Board)",
                "template": "gdp_macro_composite_template",
                "overview": "Composite index blending present situation and expectations. Broader gauge of household sentiment.",
                "why_it_matters": "Used widely as a policy and market sentiment reference.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Broad directional consumer signal.",
                "personal_impact_importance": "🌟🌟 - Tracks confidence that may influence discretionary spending.",
                "current_vs_previous": "Compares change in overall sentiment.",
                "points_percentage_changes": "Measures magnitude of movement.",
                "min_max_12months": "Frames extreme readings.",
                "averages": "Benchmarks expectations.",
                "year_over_year": "Adds context for long-cycle patterns.",
                "recommended_time_periods": ["MM", "3M", "6M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },

            "105_weekly_economic_index": {
                "Use Case": "Macro Composite Signals",
                "title": "Weekly Economic Index (NY Fed)",
                "template": "gdp_macro_composite_template",
                "overview": "High-frequency index combining multiple real-time indicators to monitor economic activity.",
                "why_it_matters": "Provides early insight into output shifts, helping assess momentum in fast-moving macro environments.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Supports rapid assessment of macro turning points or shocks.",
                "personal_impact_importance": "🌟 - Reflects near-term shifts that may affect employment, income, or confidence.",
                "current_vs_previous": "Evaluates weekly directional change.",
                "points_percentage_changes": "Tracks momentum and inflection signals.",
                "min_max_12months": "Identifies high-frequency peaks or troughs.",
                "averages": "Smooths volatile readings for pattern recognition.",
                "year_over_year": "Useful for comparing current conditions to prior cycles.",
                "recommended_time_periods": ["1W", "1M", "3M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },

            "106_economic_uncertainty_index": {
                "Use Case": "Macro Composite Signals",
                "title": "Economic Uncertainty Index",
                "template": "gdp_macro_composite_template",
                "overview": "Text-based index capturing macro and policy uncertainty from media, announcements, and institutional signals.",
                "why_it_matters": "Used to monitor systemic uncertainty and prepare for volatility regimes.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - May pre-empt regime changes or defensive allocation needs.",
                "personal_impact_importance": "🌟 - Can influence hiring expectations, confidence, and sentiment shifts.",
                "current_vs_previous": "Identifies major uncertainty shocks or reversals.",
                "points_percentage_changes": "Measures narrative acceleration or decline.",
                "min_max_12months": "Highlights key inflection periods.",
                "averages": "Distills average noise levels.",
                "year_over_year": "Benchmarks systemic risk climate shifts.",
                "recommended_time_periods": ["1M", "3M", "6M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },

            "107_chicago_fed_national_activity_index": {
                "Use Case": "Macro Composite Signals",
                "title": "National Activity Composite (Chicago Fed)",
                "template": "gdp_macro_composite_template",
                "overview": "A weighted index of 85 indicators covering income, employment, consumption, production, and housing.",
                "why_it_matters": "Assesses economic activity relative to trend and identifies broad pressures across macro drivers.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Helps validate or question economic narratives with composite evidence.",
                "personal_impact_importance": "🌟 - Reflects general macroeconomic health and resilience.",
                "current_vs_previous": "Reveals broad macro shifts.",
                "points_percentage_changes": "Captures composite directional movement.",
                "min_max_12months": "Contextualises cycles of acceleration or deceleration.",
                "averages": "Smooths aggregate deviations from trend.",
                "year_over_year": "Assesses medium-term structural direction.",
                "recommended_time_periods": ["MM", "3M", "6M"],
                "path": "{country}/pages/100_📈_economic_growth_stability.py"
            },

        }
    },

    "200_labour_market_dynamics": {
        "theme_title": "Labour Market Dynamics",
        "theme_introduction": "Labour market dynamics reflect employment capacity, wage formation, workforce participation, and cyclical adjustments tied to business cycle evolution.",
        "temporal_categorisation": {
            "coincident_indicators": "Indicators that reflect current labour market conditions, such as payroll growth and the unemployment rate.",
            "leading_indicators": "Indicators that may signal future employment shifts, such as job openings or weekly claims.",
            "lagging_indicators": "Indicators that confirm established employment trends, including average hourly earnings or participation shifts."
        },
        "template": {
            "employment_template": "Employment Template – For jobless claims, unemployment, participation, non-farm payrolls, etc.",
            "employment_composite_template": "Composite Labour Indicators Template – For wage pressure, layoffs, diffusion indices, or early labour signals."

        },
        "data_points": [
            "Labour Force Structure: Track employment, unemployment, participation, and job vacancy shifts.",
            "Wage Trends: Monitor earnings growth and its implications on consumer behaviour and policy.",
            "Cyclical Timing: Observe weekly and monthly labour market signals as they respond to broader economic momentum."
        ],
        "navigating_the_theme": "Indicators across employment, participation, wage pressure, and claims activity provide a multi-dimensional frame to observe hiring trends, absorption capacity, and cyclical stress formation.",
        "conclusion_and_further_exploration": "Employment-based indicators act as coincident and leading markers for productivity cycles, sector resilience, and systemic employment adjustments without directional forecasting.",
        "memberships": {
            "201_total_employment": {
                "Use Case": "Employment Template",
                "title": "Number of People in Employment",
                "overview": "Measures total employment. Tracks macro-level hiring trends and is a core signal of business cycle strength.",
                "why_it_matters": "A key employment indicator used in policy and market discussions. Tracks the pace of hiring and sectoral growth or contraction.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Central to assessing the health of the real economy and business cycle alignment.",
                "personal_impact_importance": "🌟🌟🌟 - Closely linked to employment availability and job security.",
                "current_vs_previous": "Compares monthly job additions or losses to previous figures.",
                "points_percentage_changes": "Tracks absolute change in jobs and percentage impact where relevant.",
                "min_max_12months": "Identifies most and least active hiring periods.",
                "averages": "Smooths monthly hiring noise for a trend-based view.",
                "year_over_year": "Used for structural comparisons in labour expansion or contraction.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "202_unemployment_rate": {
                "Use Case": "Employment Template",
                "title": "Unemployment Rate",
                "overview": "Percentage of the total labour force currently without a job but actively seeking work. Used to assess slack or tightness in the labour market and potential policy sensitivity.",
                "why_it_matters": "It serves as a key indicator of economic slack, labour demand, and consumer sentiment.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Reflects labour market tightness and potential wage pressure.",
                "personal_impact_importance": "🌟🌟🌟 - Directly affects job security, earnings potential, and household planning.",
                "current_vs_previous": "Month-to-month comparisons for directionality.",
                "points_percentage_changes": "Focuses on point moves (e.g., from 4.2% to 4.4%).",
                "min_max_12months": "Useful for contextualising job market shifts.",
                "averages": "Smoothed values for economic cycle awareness.",
                "year_over_year": "Shows broader structural changes in unemployment.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "203_labour_participation_rate": {
                "Use Case": "Employment Template",
                "title": "Labour Participation Rate",
                "overview": "Share of the working-age population either employed or actively seeking employment. Can reflect demographic trends, inclusion, and structural labour engagement.",
                "why_it_matters": "Provides insight into workforce engagement and demographic labor shifts.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟 - Contextual rather than directional—reflects structural trends.",
                "personal_impact_importance": "🌟🌟 - Tied to job availability, retirement trends, and gender/youth inclusion.",
                "current_vs_previous": "Month-to-month view of participation.",
                "points_percentage_changes": "Helps spot subtle participation shifts.",
                "min_max_12months": "Tracks broader behavioural changes.",
                "averages": "Shows underlying trendlines in workforce engagement.",
                "year_over_year": "Best for understanding structural change.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "204_business_sector_employment": {
                "Use Case": "Employment Composite",
                "title": "Business Sector Employment Breakdown",
                "overview": "Disaggregates employment across goods, services, and public sectors, capturing structural momentum and cyclical dispersion.",
                "why_it_matters": "Tracks employment shifts by sector — critical for sectoral rotation, policy targeting, and understanding cyclical exposure.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Useful for macro-sector positioning and growth dispersion insights.",
                "personal_impact_importance": "🌟🌟 - Signals which industries are hiring or contracting over time.",
                "current_vs_previous": "Detects acceleration or deceleration in sector hiring.",
                "points_percentage_changes": "Flags magnitude of hiring expansion or loss.",
                "min_max_12months": "Reveals most/least resilient sectors over time.",
                "averages": "Highlights sectoral momentum trends.",
                "year_over_year": "Enables structural comparisons across business cycles.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "205_full_part_time_employment": {
                "Use Case": "Employment Composite",
                "title": "Full-Time vs Part-Time Employment",
                "overview": "Contrasts stable full-time roles with flexible or underemployed part-time positions — a signal of labour market quality and resilience.",
                "why_it_matters": "A shift toward part-time work may indicate hidden slack, cost pressures, or structural changes in job stability.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Reveals resilience vs. fragility in job creation.",
                "personal_impact_importance": "🌟🌟 - Influences wage stability, benefits access, and personal financial planning.",
                "current_vs_previous": "Watches transitions between full and part-time employment.",
                "points_percentage_changes": "Indicates rebalancing in labour quality.",
                "min_max_12months": "Exposes peak employment quality shifts.",
                "averages": "Smooths volatility in part-time work trends.",
                "year_over_year": "Detects structural erosion or restoration of job quality.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "206_average_hourly_earnings": {
                "Use Case": "Employment Composite",
                "title": "Average Hourly Earnings",
                "overview": "Measures the average hourly compensation for employees across sectors — a key input for inflation and policy decisions.",
                "why_it_matters": "Wages link employment to consumption, inflation, and monetary policy positioning.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟🌟 - Affects inflation outlooks and earnings forecasts.",
                "personal_impact_importance": "🌟🌟🌟 - Reflects household earning power and planning capability.",
                "current_vs_previous": "Spots pay acceleration or stagnation.",
                "points_percentage_changes": "Used to assess cost-push inflation risks.",
                "min_max_12months": "Signals volatility or momentum in pay structures.",
                "averages": "Filters noise in wage progression.",
                "year_over_year": "Key for macro-monetary calibration.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "207_initial_jobless_claims": {
                "Use Case": "Employment Composite",
                "title": "Initial Jobless Claims",
                "overview": "Measures the number of new claims for unemployment insurance — a high-frequency signal of stress or recovery.",
                "why_it_matters": "Functions as a directional risk marker — rising claims often precede employment deterioration or policy response.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Often used in early recession detection and equity volatility anticipation.",
                "personal_impact_importance": "🌟🌟 - Can pre-empt personal or regional job security challenges.",
                "current_vs_previous": "Tracks week-on-week directional shifts.",
                "points_percentage_changes": "Reveals acceleration or relief trends.",
                "min_max_12months": "Highlights stress episodes.",
                "averages": "Smooths volatility with short-term MA overlays.",
                "year_over_year": "Benchmarks current conditions against prior stress periods.",
                "recommended_time_periods": ["1W", "4W", "12W", "52W"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
            "208_continued_jobless_claims": {
                "Use Case": "Employment Composite",
                "title": "Continued Jobless Claims",
                "overview": "Tracks those who remain on unemployment benefits, suggesting persistent dislocation or policy frictions.",
                "why_it_matters": "A stickiness signal — shows whether people are finding jobs or remaining structurally unemployed.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟🌟 - Reflects medium-term strain on labour absorption and consumer resilience.",
                "personal_impact_importance": "🌟🌟🌟 - Critical for understanding regional job market friction.",
                "current_vs_previous": "Watches exit/entry pressure trends.",
                "points_percentage_changes": "Signals resolution or buildup of dislocation.",
                "min_max_12months": "Identifies relief periods or entrenchment.",
                "averages": "Useful for medium-term trend evaluation.",
                "year_over_year": "Supports comparative recovery analysis.",
                "recommended_time_periods": ["1W", "4W", "12W", "52W"],
                "path": "{country}/pages/200_💼_labour_market_dynamics.py"
            },
        }
    },
    "300_consumer_behaviour_confidence": {
        "theme_title": "Consumer Behaviour and Confidence",
        "theme_introduction": "Consumer behaviour and confidence capture aggregate demand shifts, sentiment positioning, and consumption adaptation patterns tied to macro resilience.",
        "temporal_categorisation": {
            "coincident_indicators": "Reflect current consumption levels and spending behaviour (e.g., monthly retail sales).",
            "leading_indicators": "Anticipate changes in consumer behaviour or economic turning points (e.g., sentiment indices).",
            "lagging_indicators": "Confirm prior consumption trends or behavioural shifts that follow other macro developments."
        },
        "template": {
            "retail_template": "Retail Template – For headline and core retail sales.",
            "sentiment_template": "Sentiment Template – For confidence indices, market positioning metrics, and speculative behaviour."
        },
        "data_points": [
            "Spending Trends: Monitor consumption momentum and goods/services demand.",
            "behavioural Indicators: Evaluate confidence, positioning, and speculative shifts.",
            "Cross-Market Signals: Retail and sentiment can signal turning points across markets."
        ],
        "navigating_the_theme": "Retail sales and sentiment indices reflect both real-time consumption momentum and forward behavioural tendencies influencing cyclical demand configurations.",
        "conclusion_and_further_exploration": "Consumption and sentiment indicators provide structural demand signals tied to aggregate economic balance, policy sensitivity, and household confidence trends.",
        "memberships": {
            "301_retail_sales_mom": {
                "overview": "Measures month-over-month change in total retail sales, reflecting near-term demand activity.",
                "why_it_matters": "Retail sales are a critical gauge of consumer strength, closely watched for economic turning points.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Signals short-term demand strength and sectoral exposure.",
                "personal_impact_importance": "🌟🌟 - Indicates household spending behaviour and confidence.",
                "current_vs_previous": "Highlights month-on-month change in consumer spending.",
                "points_percentage_changes": "Tracks % change in total retail activity.",
                "min_max_12months": "Shows volatility in consumer demand.",
                "averages": "Smooths trend to see sustained consumer cycles.",
                "year_over_year": "Evaluates broader consumption shifts.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "pages/301_retail_sales_mom.py"
            },
            "302_core_retail_sales": {
                "overview": "Retail sales excluding autos, fuel, and/or volatile categories. A more stable view of core demand.",
                "why_it_matters": "Provides clarity on underlying consumption trends by filtering noise from volatile items.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Reflects stable demand signals, important for macro and sector screening.",
                "personal_impact_importance": "🌟🌟 - Closer link to broad household consumption capacity.",
                "current_vs_previous": "Month-on-month baseline consumer activity.",
                "points_percentage_changes": "Highlights relative strength.",
                "min_max_12months": "Indicates strength or weakness in spending patterns.",
                "averages": "Tracks consistent underlying demand.",
                "year_over_year": "Shows annualised consumer behaviour trends.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "pages/302_core_retail_sales.py"
            },
            "303_consumer_sentiment_index": {
                "overview": "A measure of how optimistic or pessimistic consumers are regarding their expected financial situation.",
                "why_it_matters": "Often leads actual consumption and investment behaviour. Used to gauge confidence and economic mood.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Reflects future spending potential and economic resilience.",
                "personal_impact_importance": "🌟🌟🌟 - Impacts job expectations, purchases, and personal finance choices.",
                "current_vs_previous": "Assesses sentiment change from prior month.",
                "points_percentage_changes": "Evaluates confidence swings.",
                "min_max_12months": "Captures emotional highs and lows across the year.",
                "averages": "Shows mean confidence over time.",
                "year_over_year": "Provides long-term attitude trendlines.",
                "recommended_time_periods": ["MM", "3M", "6M"],
                "path": "pages/303_consumer_sentiment_index.py"
            },
            "304_consumer_expectations_index": {
                "overview": "Forward-looking component of consumer sentiment focused on expectations for income, jobs, and economy.",
                "why_it_matters": "Can shift prior to actual changes in behaviour or spending patterns.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Valuable for anticipating economic and behavioural changes.",
                "personal_impact_importance": "🌟🌟 - Reflects optimism or concern around household finances.",
                "current_vs_previous": "Compares outlook vs prior month.",
                "points_percentage_changes": "Assesses directional change.",
                "min_max_12months": "Helps map confidence swings.",
                "averages": "Useful for smoothing volatile readings.",
                "year_over_year": "Highlights long-term outlook shifts.",
                "recommended_time_periods": ["MM", "3M"],
                "path": "pages/304_consumer_expectations_index.py"
            },
            "305_conference_board_index": {
                "overview": "Composite index blending present situation and expectations. Broader gauge of household sentiment.",
                "why_it_matters": "Used widely as a policy and market sentiment reference.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Broad directional consumer signal.",
                "personal_impact_importance": "🌟🌟 - Tracks confidence that may influence discretionary spending.",
                "current_vs_previous": "Compares change in overall sentiment.",
                "points_percentage_changes": "Measures magnitude of movement.",
                "min_max_12months": "Frames extreme readings.",
                "averages": "Benchmarks expectations.",
                "year_over_year": "Adds context for long-cycle patterns.",
                "recommended_time_periods": ["MM", "3M", "6M"],
                "path": "pages/305_conference_board_index.py"
            },
            "306_bull_bear_index": {
                "overview": "A sentiment survey tracking the proportion of bullish vs bearish outlooks among market participants.",
                "why_it_matters": "Useful for gauging crowd psychology. Often used as a contrarian signal or to contextualise extremes in market sentiment.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Tracks speculative extremes, which may signal caution or momentum.",
                "personal_impact_importance": "🌟 - Reflects investor mood, which can influence media sentiment and retail behaviour.",
                "current_vs_previous": "Change in bullish/bearish split vs previous period.",
                "points_percentage_changes": "Degree of sentiment skew.",
                "min_max_12months": "Frames historical extremes.",
                "averages": "Smoothing of directional sentiment.",
                "year_over_year": "Contextualizing trend consistency.",
                "recommended_time_periods": ["3M", "6M"],
                "path": "pages/306_bull_bear_index.py"
            },
            "307_speculation_index": {
                "overview": "Captures speculative appetite across retail or derivatives activity.",
                "why_it_matters": "May reflect risk-taking appetite or complacency during market runs.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Contextualises excess optimism or fear.",
                "personal_impact_importance": "🌟 - Sentiment shifts often reflect emotional extremes in public discourse.",
                "current_vs_previous": "Compares current risk appetite to previous benchmarks.",
                "points_percentage_changes": "Highlights overextended sentiment.",
                "min_max_12months": "Detects speculative peaks.",
                "averages": "Helps smooth behavioural impulses.",
                "year_over_year": "Broadens speculative trends.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/307_speculation_index.py"
            },
            "308_cot_positioning": {
                "overview": "Tracks trader positioning across futures contracts, segmented by commercial, non-commercial, and retail traders.",
                "why_it_matters": "Highlights commitment of large institutions and speculators, offering positioning clues.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟🌟 - Reveals crowded trades or shifts in institutional bias.",
                "personal_impact_importance": "🌟 - Positioning signals may reflect institutional conviction or hedging behaviour.",
                "current_vs_previous": "Net long/short changes versus prior week.",
                "points_percentage_changes": "Captures shifts in positioning concentration.",
                "min_max_12months": "Detects positioning extremes.",
                "averages": "Smooths weekly data to identify regime change.",
                "year_over_year": "Compares positioning evolution over time.",
                "recommended_time_periods": ["1W", "3M", "6M"],
                "path": "pages/308_cot_positioning.py"
            },
            "309_put_call_ratio": {
                "overview": "Ratio of put options to call options traded. Used to gauge sentiment and hedging demand.",
                "why_it_matters": "Higher readings suggest fear or hedging, while lower may imply complacency or bullishness.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Monitors market protection demand and speculative risk-on behaviour.",
                "personal_impact_importance": "🌟 - May reflect caution in investor outlook.",
                "current_vs_previous": "Week-on-week ratio change.",
                "points_percentage_changes": "Measuring hedging demand spikes.",
                "min_max_12months": "Highlights panic or complacency extremes.",
                "averages": "Trend-based smoothing.",
                "year_over_year": "Evaluates broader sentiment cycles.",
                "recommended_time_periods": ["1W", "3M"],
                "path": "pages/309_put_call_ratio.py"
            },
            "310_rsi_14_day": {
                "overview": "Relative Strength Index (14-day) is a momentum oscillator indicating overbought or oversold conditions.",
                "why_it_matters": "Popular tool for gauging short-term price exhaustion. Used across asset classes.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟 - Supports short-term positioning review, especially at extremes.",
                "personal_impact_importance": "🌟 - Often featured in financial media and commentary.",
                "current_vs_previous": "Compares RSI level to recent periods.",
                "points_percentage_changes": "Measures swing strength.",
                "min_max_12months": "Signals peak technical exuberance.",
                "averages": "Smooths oscillations.",
                "year_over_year": "Supports comparative asset behaviour analysis.",
                "recommended_time_periods": ["1W", "1M"],
                "path": "pages/310_rsi_14_day.py"
            },
        }
    },
    "400_inflation_price_dynamics": {
        "theme_title": "Price Levels and Inflation Trends",
        "theme_introduction": "Price level dynamics reflect cost pressures across producers and consumers, interacting with monetary stability, purchasing power, and policy response cycles.",
        "temporal_categorisation": {
            "coincident_indicators": "Reflect current inflation conditions impacting consumers and producers in real-time.",
            "leading_indicators": "Expectations-based price surveys (not included here but referenced in correlation analysis).",
            "lagging_indicators": "Some inflation data may lag economic movements due to data collection timelines or smoothing effects."
        },
        "template": {
            "inflation_template": "Inflation Template – Includes CPI, PPI, and PCE-related metrics for consumer and producer inflation assessment."
        },
        "data_points": [
            "Headline vs Core: Understand the role of volatile components like food and energy.",
            "Goods vs Services Inflation: Assess pressures by category.",
            "Trend Decomposition: Track persistent vs transitory effects using time-based comparisons.",
            "Policy Context: Used by central banks to set interest rates and adjust guidance."
        ],
        "navigating_the_theme": "Consumer price indices, producer input costs, and inflation components offer comparative benchmarks to assess cost expansion, input sensitivity, and real economic strain.",
        "conclusion_and_further_exploration": "Inflation-linked measures serve as anchor variables across monetary policy regimes, household purchasing stability, and systemic price volatility assessment.",
        "memberships": {
            "401_core_cpi": {
                "overview": "Core Consumer Price Index excludes volatile food and energy prices, providing a clearer view of underlying inflation.",
                "why_it_matters": "A preferred gauge for central banks, it helps in determining longer-term inflation trends.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Widely used for assessing monetary policy trajectory and long-term real returns.",
                "personal_impact_importance": "🌟🌟 - Affects wages, rent, healthcare costs, and planning for future inflation.",
                "current_vs_previous": "Highlights month-to-month underlying changes.",
                "points_percentage_changes": "Tracks price growth trends excluding energy and food.",
                "min_max_12months": "Shows inflation stability over the year.",
                "averages": "Smooths short-term volatility.",
                "year_over_year": "Used to assess persistent price changes.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "pages/401_core_cpi.py"
            },
            "402_headline_cpi": {
                "overview": "Headline CPI reflects the total change in consumer prices, including food and energy.",
                "why_it_matters": "Captures the full inflationary experience for households.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Reflects pressures on consumption and short-term policy reaction.",
                "personal_impact_importance": "🌟🌟🌟 - Strongly tied to cost of living and real wage growth.",
                "current_vs_previous": "Measures total monthly inflation swing.",
                "points_percentage_changes": "Tracks absolute and relative inflationary movements.",
                "min_max_12months": "Assesses price spikes and slowdowns.",
                "averages": "Supports smoothing of high-volatility months.",
                "year_over_year": "Long-run CPI trend monitoring.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "pages/402_headline_cpi.py"
            },
            "403_core_pce": {
                "overview": "The Core Personal Consumption Expenditures Price Index is the Federal Reserve’s preferred inflation metric, removing food and energy.",
                "why_it_matters": "Often cited in Fed forecasts and rate decision commentary.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Highly relevant to policy outlook and long-term yield adjustments.",
                "personal_impact_importance": "🌟 - Less directly felt by households, but critical for market expectations.",
                "current_vs_previous": "Analyzes month-to-month price movement.",
                "points_percentage_changes": "Focuses on structural inflation trajectory.",
                "min_max_12months": "Helps identify stabilization zones.",
                "averages": "Smoothed to remove noise from volatile categories.",
                "year_over_year": "Used for long-term target comparisons.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/403_core_pce.py"
            },
            "404_headline_pce": {
                "overview": "Headline PCE includes food and energy prices and reflects broad consumption-based inflation.",
                "why_it_matters": "Used for broader macroeconomic consumption-based inflation evaluation.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Used alongside CPI to cross-check price trends.",
                "personal_impact_importance": "🌟🌟 - Reflects the total cost pressure on spending.",
                "current_vs_previous": "Highlights recent consumption inflation changes.",
                "points_percentage_changes": "Captures short- and medium-term trend shifts.",
                "min_max_12months": "Visualises inflationary extremes.",
                "averages": "Used to confirm longer cycles.",
                "year_over_year": "Benchmarks annual inflation expectations.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/404_headline_pce.py"
            },
            "405_ppi_all_commodities": {
                "overview": "Producer Price Index (PPI) for All Commodities reflects changes in input prices across sectors.",
                "why_it_matters": "Used to assess upstream price pressures that may pass through to consumers.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Valuable for anticipating margin pressures and sector rotation.",
                "personal_impact_importance": "🌟 - Indirect but felt through cost pass-through in goods and services.",
                "current_vs_previous": "Shows shifts in wholesale pricing power.",
                "points_percentage_changes": "Tracks rate and speed of change.",
                "min_max_12months": "Assesses commodity-driven inflation risk.",
                "averages": "Smooths out seasonal effects.",
                "year_over_year": "Highlights cyclical pressure trends.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/405_ppi_all_commodities.py"
            },
            "406_core_ppi": {
                "overview": "Core PPI strips out food and energy to focus on stable wholesale price trends.",
                "why_it_matters": "Often more predictive of long-run cost structures and pricing pass-through.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Supports inflation forecasting and corporate cost analysis.",
                "personal_impact_importance": "🌟 - Reflected in goods/services prices over time.",
                "current_vs_previous": "Highlights consistent pricing patterns.",
                "points_percentage_changes": "Tracks stable price movement trends.",
                "min_max_12months": "Pinpoints pressure points.",
                "averages": "Gives longer-term view without shocks.",
                "year_over_year": "Provides basis for structural inflation assessment.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/406_core_ppi.py"
            },
        }
    },
    "500_monetary_indicators_policy_effects": {
        "theme_title": "Monetary Indicators and Policy Effects",
        "temporal_categorisation": {
        "theme_introduction": "Monetary policy frameworks capture the institutional response mechanisms via interest rates, liquidity tools, and macro-prudential interventions applied across business cycles.",
            "coincident_indicators": "Interest rates and monetary aggregates that reflect current credit conditions and central bank stance.",
            "leading_indicators": "Yield curve spreads and money velocity trends that anticipate shifts in economic growth or financial risk-taking.",
            "lagging_indicators": "Some monetary aggregates and rates may lag broader business cycle changes."
        },
        "template": {
            "interest_rate_template": "Interest Rate Template – For policy rates, government bond yields, and yield curve spreads.",
            "money_supply_template": "Money Supply Template – For monetary aggregates and their velocity across the economy."
        },
        "data_points": [
            "Policy Rate Signals: Fed Funds Rate and similar benchmarks to assess tightening or easing.",
            "Yield Curve Structure: Shape and slope of government bond curves signalling macro expectations, financial conditions, and recession risk.",
            "Monetary Aggregates: M1/M2 to understand liquidity and credit availability.",
            "Velocity Metrics: Insights into how fast money circulates and supports demand."
        ],
        "navigating_the_theme": "Policy rate adjustments, balance sheet movements, and liquidity operations reflect official calibrations intended to balance growth support with inflation management objectives.",
        "conclusion_and_further_exploration": "Monetary policy indicators form part of forward reaction functions observed for systemic risk containment, growth modulation, and currency stability maintenance.",
        "memberships": {
            "501_fed_funds_rate": {
                "overview": "The Federal Funds Rate is the primary tool used by the U.S. Federal Reserve to influence short-term interest rates and liquidity.",
                "why_it_matters": "It signals central bank stance and influences all downstream borrowing costs.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Directly affects valuation models, funding costs, and currency strength.",
                "personal_impact_importance": "🌟🌟 - Tied to mortgage rates, credit card rates, and bank lending conditions.",
                "current_vs_previous": "Tracks rate hikes or cuts.",
                "points_percentage_changes": "Assesses magnitude of change.",
                "min_max_12months": "Shows extremes in central bank stance.",
                "averages": "Useful to measure neutral or tight conditions.",
                "year_over_year": "Contextualises current policy.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/501_fed_funds_rate.py"
            },
            "502_treasury_yields": {
                "overview": "Treasury yields represent benchmark borrowing costs across maturities, used globally to assess risk-free rates.",
                "why_it_matters": "Signals market expectations of inflation, growth, and policy path.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Drives asset discounting, DCF models, and relative valuations.",
                "personal_impact_importance": "🌟 - Indirectly affects long-term debt and savings vehicles.",
                "current_vs_previous": "Tracks shifts across maturity curve.",
                "points_percentage_changes": "Measures direction and intensity.",
                "min_max_12months": "Assesses market highs/lows.",
                "averages": "Establishes benchmark trend.",
                "year_over_year": "Used for positioning outlooks.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/502_treasury_yields.py"
            },
            "503_yield_curve_spread": {
                "overview": "This spread measures the difference between long-term and short-term Treasury yields, often used to signal recession risk.",
                "why_it_matters": "A widely followed indicator of investor sentiment, policy outlook, and economic momentum.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Used in asset allocation models to anticipate downturns or recovery phases.",
                "personal_impact_importance": "🌟 - Indicates shifts in confidence and credit cycles.",
                "current_vs_previous": "Tracks inversion or steepening.",
                "points_percentage_changes": "Shows movement in curve shape.",
                "min_max_12months": "Reveals compression or expansions.",
                "averages": "Used to calculate expected slope.",
                "year_over_year": "Highlights regime changes.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/503_yield_curve_spread.py"
            },
            "504_eurodollar_futures": {
                "overview": "Eurodollar futures reflect market expectations for future interest rates and are used to price rate risk.",
                "why_it_matters": "Useful for forward guidance and policy pricing by traders and institutions.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Helpful in gauging interest rate expectations.",
                "personal_impact_importance": "🌟 - Limited direct impact but relevant to funding costs.",
                "current_vs_previous": "Tracks repricing of interest rate paths.",
                "points_percentage_changes": "Measures forward rate volatility.",
                "min_max_12months": "Highlights market shifts.",
                "averages": "Establishes expected path.",
                "year_over_year": "Shows policy divergence.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/504_eurodollar_futures.py"
            },
            "505_money_supply_m1": {
                "overview": "M1 includes the most liquid forms of money like cash and checking deposits.",
                "why_it_matters": "Reflects liquidity directly available for spending and transaction.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Useful to assess immediate liquidity shifts.",
                "personal_impact_importance": "🌟 - Influences short-term economic confidence.",
                "current_vs_previous": "Shows real-time shifts in monetary base.",
                "points_percentage_changes": "Measures liquidity injections or contractions.",
                "min_max_12months": "Highlights surges or pullbacks.",
                "averages": "Reveals trendline support.",
                "year_over_year": "Key for long-run money conditions.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/505_money_supply_m1.py"
            },
            "506_money_supply_m2": {
                "overview": "M2 includes M1 plus savings deposits and money market funds.",
                "why_it_matters": "More expansive view of liquidity and savings behaviour.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Reflects broader monetary expansion/contraction.",
                "personal_impact_importance": "🌟 - Relates to household wealth and saving.",
                "current_vs_previous": "Tracks monetary accumulation.",
                "points_percentage_changes": "Shows growth momentum.",
                "min_max_12months": "Assesses monetary trends.",
                "averages": "Provides macro context.",
                "year_over_year": "Used for historical benchmark.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/506_money_supply_m2.py"
            },
            "507_velocity_m1": {
                "overview": "Velocity of M1 measures how frequently money is used in economic transactions.",
                "why_it_matters": "Higher velocity indicates stronger demand and consumption.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟 - Supports credit and inflation modeling.",
                "personal_impact_importance": "🌟 - Indirectly reflects spending behaviour.",
                "current_vs_previous": "Evaluates speed of money circulation.",
                "points_percentage_changes": "Assesses velocity changes.",
                "min_max_12months": "Contextualises momentum.",
                "averages": "Highlights sustained shifts.",
                "year_over_year": "Macro-level behavioural shifts.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/507_velocity_m1.py"
            },
            "508_velocity_m2": {
                "overview": "Velocity of M2 examines broader money use across savings and investment layers.",
                "why_it_matters": "Low velocity often coincides with deleveraging or low confidence.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟 - Interpreted for long-run demand dynamics.",
                "personal_impact_importance": "🌟 - Reflects macroeconomic engagement.",
                "current_vs_previous": "Monitors long-term flow slowdowns or spikes.",
                "points_percentage_changes": "Quantifies flow speed.",
                "min_max_12months": "Highlights abnormal behaviour.",
                "averages": "Smooths year-end noise.",
                "year_over_year": "Macro liquidity pacing.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/508_velocity_m2.py"
            },
        }
    },
    "600_financial_conditions_risk_analysis": {
        "theme_title": "Financial Conditions and Risk Analysis",
        "theme_introduction": "Financial conditions reflect systemic liquidity levels, credit expansion dynamics, banking system resilience, and financial market stress regimes that influence capital allocation, leverage cycles, and systemic fragility risk.",
        "temporal_categorisation": {
            "coincident_indicators": "Current financial health indicators such as bank credit and financial conditions indices.",
            "leading_indicators": "Metrics like credit growth and banking stress that can signal upcoming shifts in risk appetite or liquidity availability.",
            "lagging_indicators": "Historical data that reveal long-term financial stability or the delayed impact of policy measures."
        },
        "template": {
            "financial_conditions_template": "Financial Conditions Template – For stress indicators, credit growth, and broad financial market conditions.",
            "credit_cycle_default_template": "Credit Cycle & Default Risk Template – For credit tightening, default trends, and high-yield spread monitoring.",
            "housing_cycle_template": "Housing Construction Cycle Template – For financing conditions, permits, starts, and completions tracking across housing demand, credit sensitivity, and construction supply flow stages."
        },
        "data_points": [
            "Liquidity Flows: Assess levels of available capital in financial markets.",
            "Credit Expansion Trends: Understand the pace and breadth of lending and borrowing.",
            "Banking Sector Health: Evaluate stress metrics and resilience levels across the financial system.",
            "Housing Construction Pipeline: Observe authorization, build activity, and completion flow as credit-sensitive signals shaping supply, industry activity, and broader economic interpretation.",
            "Mortgage Financing Conditions: Monitor long-term mortgage borrowing costs influencing housing affordability and construction demand.",
            "Yield Curve Structure: Observe long- versus short-term interest rate dynamics signalling liquidity conditions and macroeconomic expectations."
        ],
        "navigating_the_theme": "Credit growth, financial conditions indices, banking stress markers, and liquidity flow measures provide system-level signals monitoring leverage expansion, funding constraints, and structural market stress evolution across macroeconomic cycles.",
        "conclusion_and_further_exploration": "Financial conditions and credit indicators serve as composite signals reflecting systemic liquidity regimes, leverage sensitivity, credit tightening phases, and evolving systemic stress states across policy cycles.",
        "memberships": {
            "601_bank_stress_index": {
                "overview": "Tracks banking system stress using composite indicators or credit default spread proxies.",
                "why_it_matters": "Early signal of instability in the banking sector. Useful for identifying systemic risk or financial fragility.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Helps flag credit events and financial shocks that may affect liquidity or valuation models.",
                "personal_impact_importance": "🌟🌟 - Tighter lending and instability can influence personal credit access and confidence.",
                "current_vs_previous": "Changes in stress level vs prior readings.",
                "points_percentage_changes": "Evaluates the scale of financial tightening.",
                "min_max_12months": "Identifies episodes of significant systemic strain.",
                "averages": "Helps assess if conditions are unusually tight or loose.",
                "year_over_year": "Compares structural shifts in the financial system.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/601_bank_stress_index.py"
            },
            "602_credit_growth": {
                "overview": "Measures the rate at which new credit is expanding across the economy.",
                "why_it_matters": "Credit growth often precedes economic momentum or overextension. Useful for policy analysis and cyclical shifts.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Helps assess liquidity regimes, macro credit cycles, and risk-on/off behaviour.",
                "personal_impact_importance": "🌟 - Influences access to mortgages, consumer loans, and general borrowing conditions.",
                "current_vs_previous": "Highlights acceleration or deceleration in lending.",
                "points_percentage_changes": "Tracks quarterly and annual lending shifts.",
                "min_max_12months": "Identifies credit booms or contractions.",
                "averages": "Establishes baseline credit conditions.",
                "year_over_year": "Used for structural credit growth assessment.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/602_credit_growth.py"
            },
            "603_bank_credit": {
                "overview": "Total bank credit extended, encompassing business and household lending.",
                "why_it_matters": "Reflects overall credit supply conditions. Serves as a proxy for financial activity and willingness to lend.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟 - Highlights prevailing risk sentiment and financial intermediation.",
                "personal_impact_importance": "🌟 - Associated with consumer credit, small business loans, and banking accessibility.",
                "current_vs_previous": "Comparison of recent vs earlier bank credit figures.",
                "points_percentage_changes": "Shows absolute or relative lending shifts.",
                "min_max_12months": "Provides a volatility profile of credit creation.",
                "averages": "Baseline lending levels.",
                "year_over_year": "Assess structural changes in bank behaviour.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/603_bank_credit.py"
            },
            "604_financial_conditions_index": {
                "overview": "An aggregate index capturing interest rates, spreads, equity valuations, and volatility.",
                "why_it_matters": "Tracks overall tightness or looseness in financial markets. Useful for gauging policy effectiveness or risk appetite shifts.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Widely used to assess if conditions are supporting or hindering asset price performance.",
                "personal_impact_importance": "🌟 - May reflect policy-driven changes in loan availability or volatility in asset prices.",
                "current_vs_previous": "Monitors tightening or easing in the financial environment.",
                "points_percentage_changes": "Tracks swings in composite risk tolerance.",
                "min_max_12months": "Detects extremes in financial tightness or exuberance.",
                "averages": "Smooths noise across multiple indicators.",
                "year_over_year": "Captures high-level liquidity and sentiment shifts.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/604_financial_conditions_index.py"
            },
            "605_loan_officer_survey": {
                "overview": "Survey of senior loan officers regarding changes in credit standards and demand for loans.",
                "why_it_matters": "Acts as a forward-looking view of tightening or loosening credit availability.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Indicates business and consumer credit constraints before hard data appears.",
                "personal_impact_importance": "🌟🌟 - Reflects how easily households or businesses can obtain credit.",
                "current_vs_previous": "Tracks recent tightening or easing behaviour.",
                "points_percentage_changes": "Assesses pace of change in credit terms.",
                "min_max_12months": "Identifies sharp pivots in lending trends.",
                "averages": "Smooths signals across quarters.",
                "year_over_year": "Evaluates long-term shifts in credit market stance.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/605_loan_officer_survey.py"
            },
            "606_high_yield_spread": {
                "overview": "Spread between high-yield (junk) bond yields and safer government bonds.",
                "why_it_matters": "Acts as a stress barometer in credit markets—wider spreads imply more fear or default risk.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Strong signal of market tension or relative optimism across corporate credit.",
                "personal_impact_importance": "🌟 - May correlate with volatility or tightening lending standards.",
                "current_vs_previous": "Compares spread movements over time.",
                "points_percentage_changes": "Analyzes spread magnitude and shifts.",
                "min_max_12months": "Identifies historic stress periods.",
                "averages": "Provides cyclical norm reference.",
                "year_over_year": "Shows broader market regime shifts.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "pages/606_high_yield_spread.py"
            },
            "607_default_rate_index": {
                "overview": "Measures corporate or consumer loan default rates over time.",
                "why_it_matters": "Elevated defaults often reflect deeper economic or financial stress, trailing tightening periods.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟🌟 - Confirms deterioration in financial conditions.",
                "personal_impact_importance": "🌟🌟 - Affects credit access, insurance, and systemic risk perception.",
                "current_vs_previous": "Compares change in default volumes.",
                "points_percentage_changes": "Tracks % change in default rates.",
                "min_max_12months": "Highlights most stressed periods.",
                "averages": "Reveals baseline financial health.",
                "year_over_year": "Used to confirm trend reversals.",
                "recommended_time_periods": ["6M", "12M"],
                "path": "pages/607_default_rate_index.py"
            },
            "608_leveraged_loan_index": {
                "overview": "Captures pricing and volume trends in the leveraged loan market.",
                "why_it_matters": "Reflects credit appetite in higher-risk lending markets and liquidity pressure.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Used to identify shifts in risk appetite or excess.",
                "personal_impact_importance": "🌟 - May tie to credit spreads and refinancing dynamics.",
                "current_vs_previous": "Shows price trend or issuance strength.",
                "points_percentage_changes": "Measures risk tolerance via spreads or performance.",
                "min_max_12months": "Assesses fragility or demand for risk assets.",
                "averages": "Benchmark levels of issuance.",
                "year_over_year": "Highlights major cyclical shifts.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/608_leveraged_loan_index.py"
            },
            "609_housing_units_authorized": {
                "Use Case": "Housing Construction Cycle",
                "title": "Housing Units Authorized",
                "template": "housing_cycle_template",
                "overview": "Measures the number of housing units authorized for future construction, capturing the earliest stage of the residential building pipeline.",
                "why_it_matters": "Housing authorizations act as a forward-looking signal for construction activity, financing demand, supply pipeline formation, and broader credit-sensitive economic momentum.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Helps frame early housing-cycle momentum, construction sensitivity, and downstream industry or market implications tied to financial conditions.",
                "personal_impact_importance": "🌟🌟 - Signals potential changes in future housing supply, build activity, and the broader affordability and employment backdrop.",
                "current_vs_previous": "Compares the latest authorizations to prior periods to detect acceleration or slowing in pipeline formation.",
                "points_percentage_changes": "Tracks absolute and percentage changes to assess the strength and direction of future construction intent.",
                "min_max_12months": "Highlights the highest and lowest authorization levels over the past year to place current readings in cycle context.",
                "averages": "Uses average levels to identify whether authorization activity is running above or below recent housing-cycle norms.",
                "year_over_year": "Compares current authorizations with the same period last year to surface broader directional shifts in the housing pipeline.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/600_🔍_financial_conditions_risk_analysis.py"
            },
            "610_housing_units_started": {
                "Use Case": "Housing Construction Cycle",
                "title": "Housing Units Started",
                "template": "housing_cycle_template",
                "overview": "Measures the number of housing units on which construction has begun, reflecting active build execution within the residential pipeline.",
                "why_it_matters": "Housing starts provide a live read on construction activity, financing follow-through, developer confidence, and the conversion of approvals into real-economy building momentum.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Useful for tracking active cycle conditions across construction-linked industries, materials demand, and market sensitivity to shifting financial conditions.",
                "personal_impact_importance": "🌟🌟 - Connects to employment conditions, local building activity, and the pace at which future housing supply is being advanced.",
                "current_vs_previous": "Compares current starts with previous readings to show whether active construction is expanding or cooling.",
                "points_percentage_changes": "Measures absolute and percentage changes to assess the pace of execution within the housing pipeline.",
                "min_max_12months": "Shows the range of start activity over the past year to help place current construction intensity in context.",
                "averages": "Calculates average start levels to reveal whether current activity is above or below recent construction norms.",
                "year_over_year": "Compares starts with the same period last year to surface broader changes in construction momentum.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/600_🔍_financial_conditions_risk_analysis.py"
            },
            "611_housing_units_completed": {
                "Use Case": "Housing Construction Cycle",
                "title": "Housing Units Completed",
                "template": "housing_cycle_template",
                "overview": "Measures the number of housing units completed and ready to enter available supply, reflecting the delivery stage of the construction cycle.",
                "why_it_matters": "Housing completions help reveal when pipeline activity is converting into delivered supply, with implications for housing availability, construction follow-through, and broader system interpretation.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟🌟 - Helps confirm whether earlier construction momentum is translating into delivered supply and downstream sector effects.",
                "personal_impact_importance": "🌟🌟🌟 - Most closely tied to housing availability, local supply conditions, and the pace at which pipeline activity reaches households and communities.",
                "current_vs_previous": "Compares current completions with prior readings to show whether supply delivery is accelerating or normalizing.",
                "points_percentage_changes": "Tracks absolute and percentage changes to assess how quickly completed supply is entering the market.",
                "min_max_12months": "Highlights the highest and lowest completion levels over the past year for supply-cycle context.",
                "averages": "Uses average completion levels to show whether delivered supply is running above or below recent norms.",
                "year_over_year": "Compares completions with the same period last year to confirm broader shifts in delivered housing supply.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/600_🔍_financial_conditions_risk_analysis.py"
            },
            "612_30_year_mortgage_rate": {
                "Use Case": "Housing Construction Cycle",
                "title": "30-Year Mortgage Rate",
                "template": "housing_cycle_template",
                "overview": "Represents the average interest rate charged on standard 30-year fixed-rate mortgages, reflecting prevailing long-term borrowing costs in residential housing finance.",
                "why_it_matters": "Mortgage rates influence housing affordability, borrowing demand, refinancing activity, and the willingness of households and developers to enter the housing market.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Provides insight into financing conditions that shape housing demand, credit sensitivity, and broader construction-cycle momentum.",
                "personal_impact_importance": "🌟🌟🌟 - Directly affects mortgage affordability, household borrowing capacity, and the cost of home ownership or refinancing decisions.",
                "current_vs_previous": "Compares the latest mortgage rate with prior readings to highlight whether borrowing costs are rising, stabilising, or easing.",
                "points_percentage_changes": "Tracks both point movements and percentage changes to show shifts in financing conditions affecting housing demand.",
                "min_max_12months": "Identifies the highest and lowest mortgage rate levels observed over the past year to contextualise current financing conditions.",
                "averages": "Uses average rate levels to reveal whether current mortgage costs sit above or below recent borrowing cost norms.",
                "year_over_year": "Compares current mortgage rates with the same period last year to surface broader shifts in long-term housing financing conditions.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/600_🔍_financial_conditions_risk_analysis.py"
            },
            "613_yield_curve_spread": {
                "Use Case": "Housing Construction Cycle",
                "title": "Yield Curve Spread",
                "template": "housing_cycle_template",
                "overview": "Measures the difference between long-term and short-term government bond yields, commonly represented by the spread between 10-year and 2-year Treasury rates.",
                "why_it_matters": "Yield curve structure reflects expectations around economic growth, inflation, and monetary policy direction, often signalling shifts in financial conditions and macroeconomic momentum.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟🌟 - Widely observed as a macro signal reflecting liquidity conditions, economic expectations, and potential turning points across financial cycles.",
                "personal_impact_importance": "🌟 - Indirectly influences borrowing costs, credit availability, and broader economic conditions affecting employment and financial stability.",
                "current_vs_previous": "Compares the current spread with previous readings to reveal whether the curve is steepening, flattening, or inverting.",
                "points_percentage_changes": "Tracks changes in the spread to detect shifts in macro expectations and financial market positioning.",
                "min_max_12months": "Highlights the highest and lowest spread levels observed over the past year to place the current curve structure in context.",
                "averages": "Uses average spread levels to show whether the current curve structure is above or below recent macro cycle norms.",
                "year_over_year": "Compares the current spread with the same period last year to surface structural shifts in the yield curve environment.",
                "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                "path": "{country}/pages/600_🔍_financial_conditions_risk_analysis.py"
            }
        }
    },

     "700_global_trade_economic_relations": {
        "theme_title": "Global Trade and Economic Relations",
        "theme_introduction": "Global trade dynamics capture external sector interactions, cross-border demand flows, competitiveness positioning, and systemic trade balances tied to macroeconomic cycle transitions.",
        "temporal_categorisation": {
            "coincident_indicators": "Provide a real-time snapshot of a country's trade position and external demand.",
            "leading_indicators": "Help forecast future economic momentum through shifts in exports, imports, and global supply chains.",
            "lagging_indicators": "Confirm structural trade trends and long-term trade competitiveness."
         },
         "template": {
            "trade_activity_template": "Trade Activity Template – For imports, exports, trade balance, and trade-to-GDP ratios."
         },
         "data_points": [
            "Historical Trends: Analyze how trade flows have evolved in response to currency changes, geopolitical developments, or trade policies.",
            "Comparative Analysis: Compare trade dynamics across countries or regions to assess global competitiveness.",
            "Policy Impact Assessment: Evaluate the effects of tariffs, trade agreements, or sanctions on export/import flows.",
         ],
         "navigating_the_theme": "Trade flow data including imports, exports, trade balances, and trade-to-GDP ratios provide system-level signals on competitiveness shifts, demand composition, currency alignment sensitivity, and structural exposure to global markets.",
         "conclusion_and_further_exploration": "Trade indicators serve as composite signals reflecting external sector stability, capital allocation dependencies, and cyclical positioning of cross-border flows within global economic regimes.",
         "memberships": {
            "701_trade_balance": {
                "overview": "Trade Balance measures the difference between exports and imports of goods and services.",
                "why_it_matters": "A persistent surplus or deficit can influence currency strength, external stability, and macro risk exposure.",
                 "temporal_categorisation": "Coincident indicator",
                 "investment_action_importance": "🌟🌟 - Supports currency, export-driven sector, and fiscal policy context.",
                 "personal_impact_importance": "🌟 - Trade balances can influence inflation, job security in exposed sectors, and currency-driven purchasing power.",
                 "current_vs_previous": "Compare net exports over time to track trends.",
                 "points_percentage_changes": "Track surplus/deficit shifts as percent of GDP or nominal flow.",
                 "min_max_12months": "Detect volatility, structural improvements, or sudden shocks.",
                 "averages": "Assess trend direction across quarters.",
                 "year_over_year": "Understand cyclical vs structural shifts.",
                 "recommended_time_periods": ["3M", "6M", "12M"],
                 "path": "pages/701_trade_balance.py"
           },
           "702_import_growth": {
                 "overview": "Import Growth tracks the change in the volume or value of goods and services brought into a country.",
                 "why_it_matters": "Signals domestic demand and potential exposure to foreign supply chain risks.",
                 "temporal_categorisation": "Coincident indicator",
                 "investment_action_importance": "🌟 - Helps understand consumption trends and currency pressure.",
                 "personal_impact_importance": "🌟 - Affects product availability and pricing for consumers.",
                 "current_vs_previous": "Track month-over-month shifts in import levels.",
                 "points_percentage_changes": "Gauge consumption strength and exchange rate sensitivity.",
                 "min_max_12months": "Shows volatility in supply-driven trends.",
                 "averages": "Contextualise sharp moves in seasonal activity.",
                 "year_over_year": "Capture annual demand trends and currency impacts.",
                 "recommended_time_periods": ["MM", "3M", "6M"],
                 "path": "pages/702_import_growth.py"
           },
           "703_export_growth": {
                 "overview": "Export Growth tracks outbound trade, often seen as a signal of competitiveness and global demand for domestic goods.",
                 "why_it_matters": "Informs positioning in export-linked sectors and macro trade resilience.",
                 "temporal_categorisation": "Leading indicator",
                 "investment_action_importance": "🌟🌟 - Tied to manufacturing, commodities, and FX strength.",
                 "personal_impact_importance": "🌟 - Impacts job creation and wage growth in export-heavy industries.",
                 "current_vs_previous": "Tracks export fluctuations across reporting cycles.",
                 "points_percentage_changes": "Shows demand growth trends from external partners.",
                 "min_max_12months": "Captures recovery patterns after trade shocks.",
                 "averages": "Helps normalise cyclical moves in external demand.",
                 "year_over_year": "Highlights durable trade growth or structural erosion.",
                 "recommended_time_periods": ["3M", "6M", "12M"],
                 "path": "pages/703_export_growth.py"
           },
           "704_net_exports_gdp": {
                 "overview": "Net Exports as a % of GDP provides a sense of trade dependency and external leverage.",
                 "why_it_matters": "Frames how much GDP is driven by trade surplus or deficit.",
                 "temporal_categorisation": "Lagging indicator",
                 "investment_action_importance": "🌟 - Useful for sovereign risk analysis and current account context.",
                 "personal_impact_importance": "🌟 - Long-term deficits may pressure taxes or subsidies.",
                 "current_vs_previous": "Evaluate quarterly shifts in trade-to-GDP dynamics.",
                 "points_percentage_changes": "Highlight changing trade reliance.",
                 "min_max_12months": "Surface long-term imbalances or rebalancing.",
                 "averages": "Contextualises trade role across cycles.",
                 "year_over_year": "Detect longer-run movement in export/import contribution to GDP.",
                 "recommended_time_periods": ["Q", "12M"],
                 "path": "pages/704_net_exports_gdp.py"
           },
           "705_trade_percent_gdp": {
                 "overview": "Total trade (imports + exports) as a % of GDP reflects an economy’s openness and exposure to global markets.",
                 "why_it_matters": "Higher ratios suggest integration with the global economy; lower ones may indicate autarky or internal demand focus.",
                 "temporal_categorisation": "Lagging indicator",
                 "investment_action_importance": "🌟 - Helps frame global risk sensitivity and foreign demand reliance.",
                 "personal_impact_importance": "🌟 - High trade exposure may influence inflation, jobs, and FX sensitivity.",
                 "current_vs_previous": "Review shifts in total trade activity relative to output.",
                 "points_percentage_changes": "Indicates growing or shrinking global exposure.",
                 "min_max_12months": "Visualises trade dependency stability.",
                 "averages": "Normalises trade role for structural assessment.",
                 "year_over_year": "Highlight trade integration or decoupling trends.",
                 "recommended_time_periods": ["6M", "12M"],
                 "path": "pages/705_trade_percent_gdp.py"
             },
         }
     },
 "800_supply_chains_logistics": {
         "theme_title": "Supply Chains and Global Logistics",
         "theme_introduction": "Supply chain and logistics indicators reflect transportation capacity, bottleneck formation, global freight dynamics, and systemic logistical stress conditions influencing production stability and cost structures.",
         "temporal_categorisation": {
             "coincident_indicators": "Show the current state of shipping and freight activity.",
             "leading_indicators": "Signal upcoming disruptions or easing in logistics pressures.",
             "lagging_indicators": "Help assess the downstream effects of past supply shocks."
         },
         "template": {
             "supply_chain_template": "Supply Chain Template – For freight indices, pressure metrics, and logistics stress indicators."
         },
         "data_points": [
             "Shipping Costs: Track changes in global freight rates and transportation costs.",
             "Bottleneck Indicators: Assess congestion, delays, and logistical friction across ports and routes.",
             "Macro Linkages: Understand how supply chain constraints feed into inflation, production delays, and equity margins."
         ],
         "navigating_the_theme": "Freight indices, supply chain pressure composites, and logistics congestion measures structure system-level signals capturing operational stress, input flow volatility, and upstream cost friction feeding into broader macroeconomic cycles.",
         "conclusion_and_further_exploration": "Supply chain indicators serve as composite signals quantifying logistics-driven cost pressure, production volatility sensitivity, and frictional input constraints across manufacturing and distribution cycles.",
         "memberships": {
             "801_baltic_dry_index": {
                 "overview": "Tracks the cost of shipping raw materials like coal, iron ore, and grain across major global routes.",
                 "why_it_matters": "Serves as a proxy for global trade activity and industrial demand.",
                 "temporal_categorisation": "Leading indicator",
                 "investment_action_importance": "🌟🌟 - Useful in macro framing, particularly for commodity markets and industrial trends.",
                 "personal_impact_importance": "🌟 - Affects global supply chain costs that may feed into consumer goods pricing.",
                 "current_vs_previous": "Shows rate changes in dry bulk shipping.",
                 "points_percentage_changes": "Monitors volatility and demand sensitivity.",
                 "min_max_12months": "Frames highest/lowest freight costs for reference.",
                 "averages": "Identifies sustained pressures or relief in trade lanes.",
                 "year_over_year": "Provides historical perspective on trade flows.",
                 "recommended_time_periods": ["MM", "3M", "6M"],
                 "path": "pages/801_baltic_dry_index.py"
             },
             "802_global_container_shipping_index": {
                 "overview": "Aggregates global container rates across key ports and shipping routes.",
                 "why_it_matters": "Reflects logistics congestion and cost spikes that can ripple through supply chains.",
                 "temporal_categorisation": "Coincident indicator",
                 "investment_action_importance": "🌟🌟 - Supports assessment of goods inflation and corporate margin risks.",
                 "personal_impact_importance": "🌟 - Impacts cost of goods and delivery timelines.",
                 "current_vs_previous": "Compares global shipping price shifts.",
                 "points_percentage_changes": "Tracks container rate dynamics.",
                 "min_max_12months": "Highlights supply chain stress windows.",
                 "averages": "Smooths short-term spikes to reveal trend.",
                 "year_over_year": "Highlights major supply/demand imbalances.",
                 "recommended_time_periods": ["MM", "3M", "6M", "12M"],
                 "path": "pages/802_global_container_shipping_index.py"
             },
             "803_supply_chain_pressure_index": {
                 "overview": "Composite index measuring global transportation, inventory, and delivery delays.",
                 "why_it_matters": "A broader gauge of supply-side friction across economies.",
                 "temporal_categorisation": "Coincident to leading",
                 "investment_action_importance": "🌟🌟 - Provides regime context for inflation, manufacturing, and cost-push narratives.",
                 "personal_impact_importance": "🌟 - Linked to cost of living and availability of goods.",
                 "current_vs_previous": "Measures month-over-month easing or tightening.",
                 "points_percentage_changes": "Tracks multi-variable change across supply stressors.",
                 "min_max_12months": "Identifies peak pressure periods.",
                 "averages": "Highlights average stress trend.",
                 "year_over_year": "Maps relief or escalation from prior year.",
                 "recommended_time_periods": ["3M", "6M", "12M"],
                 "path": "pages/803_supply_chain_pressure_index.py"
             },
         }
     },
     "900_commodity_markets_pricing": {
     "theme_title": "Commodity Markets and Resource Pricing",
     "theme_introduction": "Commodity markets reflect input cost regimes, global production capacity, resource scarcity dynamics, and inflationary transmission mechanisms across energy, agriculture, and metals sectors.",
     "temporal_categorisation": {
         "coincident_indicators": "Spot and futures prices reflect current market conditions and supply-demand balance.",
         "leading_indicators": "Trends in futures curves, volatility, and inventory levels can signal future inflationary pressures or economic turning points.",
         "lagging_indicators": "Commodity indices and long-run price trends provide insight into structural shifts and global resource cycles."
     },
     "template": {
         "commodity_template": "Commodity Template – For energy, metals, agricultural futures, and commodity indices."
     },
     "data_points": [
         "Volatility and Spikes: Track extreme price behaviour due to geopolitical risk, weather, or policy shifts.",
         "Correlation Insights: Understand linkages between commodities and inflation, interest rates, or equities.",
         "Cycle Positioning: Identify where individual commodities are in their boom-bust cycles."
     ],
     "navigating_the_theme": "Futures curves, spot pricing, volatility regimes, and inventory levels provide system-level signals capturing supply-demand imbalances, cost pressure channels, and macroeconomic sensitivity tied to resource cycles.",
     "conclusion_and_further_exploration": "Commodity price signals serve as structural markers of inflation transmission, resource scarcity dynamics, geopolitical friction exposure, and cyclical positioning across global production regimes.",
     "memberships": {
         "901_wti_crude_future": {
             "overview": "West Texas Intermediate (WTI) is a benchmark for US crude oil prices, reflecting supply/demand in North America.",
             "why_it_matters": "Crucial for energy cost trends, inflation expectations, and geopolitical sensitivity.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟🌟 - Influences equity sectors, inflation hedges, and macro sentiment.",
             "personal_impact_importance": "🌟🌟 - Affects fuel prices and household costs.",
             "current_vs_previous": "Track price changes over short periods.",
             "points_percentage_changes": "Assess volatility and momentum.",
             "min_max_12months": "Highlight supply shocks or demand surges.",
             "averages": "Identify fair value zones.",
             "year_over_year": "Analyze oil price cycles and geopolitical episodes.",
             "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
             "path": "pages/901_wti_crude_future.py"
         },
         "902_brent_crude_future": {
             "overview": "Brent is the global benchmark for crude oil, reflecting international supply-demand conditions.",
             "why_it_matters": "Used for global pricing and trade contracts, especially outside North America.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟🌟 - Impacts inflation, EM economies, and global capital flows.",
             "personal_impact_importance": "🌟 - Reflects broad energy trends affecting household fuel prices.",
             "current_vs_previous": "Week/month comparisons to spot global energy trends.",
             "points_percentage_changes": "Capture sharp dislocations in pricing.",
             "min_max_12months": "Reveal extreme geopolitical or demand-driven moves.",
             "averages": "Gauge medium-term trendlines.",
             "year_over_year": "Track price recovery or decline across economic cycles.",
             "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
             "path": "pages/902_brent_crude_future.py"
         },
         "903_natural_gas_future": {
             "overview": "Natural gas futures reflect energy market dynamics in power generation and industrial usage.",
             "why_it_matters": "Highly sensitive to weather and energy substitution trends.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Indicates seasonal stress and energy market tightness.",
             "personal_impact_importance": "🌟 - Influences heating costs and energy affordability.",
             "current_vs_previous": "Track seasonal demand swings.",
             "points_percentage_changes": "Detect shocks tied to weather or supply.",
             "min_max_12months": "Reveal volatility during demand surges or storage issues.",
             "averages": "Smooth pricing patterns for insight.",
             "year_over_year": "Compare across seasonal heating cycles.",
             "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
             "path": "pages/903_natural_gas_future.py"
         },
         "904_soybean_future": {
             "overview": "Soybeans are a key agricultural commodity used in food, biofuel, and livestock feed.",
             "why_it_matters": "Prices reflect global food supply, weather impacts, and trade policies.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Tracks agri-inflation and supply disruptions.",
             "personal_impact_importance": "🌟 - Affects food prices and livestock feed costs.",
             "current_vs_previous": "Assess short-term crop expectations.",
             "points_percentage_changes": "Understand agri volatility.",
             "min_max_12months": "Monitor yield uncertainty.",
             "averages": "Evaluate mean reversion or pricing trends.",
             "year_over_year": "Supports broader inflation analysis.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/904_soybean_future.py"
         },
         "905_corn_future": {
             "overview": "Corn is a staple crop with uses in food, fuel, and animal feed.",
             "why_it_matters": "Reflects agricultural cycles and trade conditions.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟 - Tracks agri-economic pressures and food input costs.",
             "personal_impact_importance": "🌟 - Influences food and energy expenses.",
             "current_vs_previous": "Seasonal yield and demand variation.",
             "points_percentage_changes": "Signal short-term stress or relief.",
             "min_max_12months": "Spot peak seasonal supply/demand cycles.",
             "averages": "Highlight production baselines.",
             "year_over_year": "Use in food inflation tracking.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/905_corn_future.py"
         },
         "906_wheat_future": {
             "overview": "Wheat futures track global staple grain markets and geopolitical impacts on food trade.",
             "why_it_matters": "High relevance during global shocks or sanctions.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟 - A proxy for food security concerns.",
             "personal_impact_importance": "🌟 - Directly impacts household food cost volatility.",
             "current_vs_previous": "Follow harvest patterns and policy decisions.",
             "points_percentage_changes": "Capture acute food price changes.",
             "min_max_12months": "Review supply-side shocks or bumper harvests.",
             "averages": "Assess pricing floors or ceilings.",
             "year_over_year": "Reveal trend shifts across economic phases.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/906_wheat_future.py"
         },
         "907_gold_spot": {
             "overview": "Gold is a traditional store of value, widely viewed as a hedge against inflation and systemic risk.",
             "why_it_matters": "Responds to real yields, USD strength, and risk sentiment.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟🌟 - Important for hedging, sentiment, and intermarket analysis.",
             "personal_impact_importance": "🌟 - Reflects broader confidence in financial systems.",
             "current_vs_previous": "Gauge movement linked to macro uncertainty.",
             "points_percentage_changes": "Track shifts in investor demand or real yield impact.",
             "min_max_12months": "Highlight safe-haven flows during crises.",
             "averages": "Identify mean-reverting behaviour.",
             "year_over_year": "Useful for real return tracking.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/907_gold_spot.py"
         },
         "908_silver_spot": {
             "overview": "Silver combines industrial and precious metal characteristics, making it sensitive to growth and sentiment.",
             "why_it_matters": "Acts as a hybrid commodity linked to both macro and industrial cycles.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Provides signals on economic activity and investor positioning.",
             "personal_impact_importance": "🌟 - Tracks metal-linked inflation and supply chains.",
             "current_vs_previous": "Follow shifts in demand.",
             "points_percentage_changes": "Measure volatility.",
             "min_max_12months": "Detect cyclical reversals.",
             "averages": "Support macro regime awareness.",
             "year_over_year": "Useful for trend analysis.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/908_silver_spot.py"
         },
         "909_platinum_spot": {
             "overview": "Platinum is a rare industrial and precious metal with use in catalysts and jewelry.",
             "why_it_matters": "Tightly tied to automotive and industrial demand.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟 - Tracks growth-linked industrial momentum.",
             "personal_impact_importance": "🌟 - Monitors inflation and industry sentiment indirectly.",
             "current_vs_previous": "Check for short-term directional change.",
             "points_percentage_changes": "Volatility signals linked to supply shocks.",
             "min_max_12months": "Extremes reveal cyclical importance.",
             "averages": "Smoothed behaviour across time.",
             "year_over_year": "Supports cyclical interpretation.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/909_platinum_spot.py"
         },
         "910_palladium_spot": {
             "overview": "Palladium is heavily used in automotive catalytic converters and is considered a tight-supply metal.",
             "why_it_matters": "Highly sensitive to industry cycles and regulation.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟 - Cyclical indicator of industrial intensity.",
             "personal_impact_importance": "🌟 - Minor, but reflects industrial health.",
             "current_vs_previous": "Follow price spikes tied to supply chain stress.",
             "points_percentage_changes": "Evaluate sharp fluctuations.",
             "min_max_12months": "Spot range extremes.",
             "averages": "Support broader materials sentiment.",
             "year_over_year": "Highlight recovery or collapse periods.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/910_palladium_spot.py"
         },
         "911_copper_future": {
             "overview": "Copper is a global bellwether for construction, electronics, and industrial growth trends.",
             "why_it_matters": "Closely watched for insights into manufacturing cycles and China demand.",
             "temporal_categorisation": "Leading indicator",
             "investment_action_importance": "🌟🌟🌟 - Often called 'Dr. Copper' for its forecasting ability.",
             "personal_impact_importance": "🌟 - Linked to housing and infrastructure cost cycles.",
             "current_vs_previous": "Spot shifts in real-time demand.",
             "points_percentage_changes": "Capture price sensitivity to data surprises.",
             "min_max_12months": "Track industrial booms/busts.",
             "averages": "Show structural trend shifts.",
             "year_over_year": "Anchor analysis around global growth.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/911_copper_future.py"
         },
         "912_lme_metals": {
             "overview": "LME Metals Index represents a basket of base metals traded on the London Metal Exchange.",
             "why_it_matters": "Serves as a benchmark for global industrial commodity demand and cost pressures.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Reflects global demand for raw materials.",
             "personal_impact_importance": "🌟 - Affects construction and electronics prices.",
             "current_vs_previous": "Track composite pricing behaviour.",
             "points_percentage_changes": "Spot large shifts in base metals trend.",
             "min_max_12months": "Detect macro inflection points.",
             "averages": "Smooth intermetallic noise.",
             "year_over_year": "Anchor base metal macro thesis.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/912_lme_metals.py"
         },
         "913_bloomberg_commodity_index": {
             "overview": "The Bloomberg Commodity Index (BCOM) tracks a diversified basket of commodity futures.",
             "why_it_matters": "Used to evaluate broad commodity trends and inflation sensitivity.",
             "temporal_categorisation": "Lagging indicator",
             "investment_action_importance": "🌟🌟 - Acts as a barometer for overall resource pricing.",
             "personal_impact_importance": "🌟 - Reflects household inflation pressures.",
             "current_vs_previous": "Spot cycle turns across commodities.",
             "points_percentage_changes": "Track shifts in sector-level movements.",
             "min_max_12months": "Benchmark commodities bull/bear phases.",
             "averages": "Review macro balance conditions.",
             "year_over_year": "Anchor multi-commodity analysis.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/913_bloomberg_commodity_index.py"
             },
         }
     },
     "1000_currency_exchange_movements": {
     "theme_title": "Currency and Exchange Rate Movements",
     "theme_introduction": "Currency markets reflect capital flow positioning, trade competitiveness dynamics, policy divergence regimes, and inflation transmission channels embedded within cross-border financial systems.",
     "temporal_categorisation": {
         "coincident_indicators": "Spot values and index levels provide real-time information about currency strength and market perception.",
         "leading_indicators": "Changes in FX volatility or relative value shifts often precede monetary policy adjustments and trade responses.",
         "lagging_indicators": "Structural currency trends can reflect the cumulative effect of trade balances, capital flows, and inflation differentials."
     },
     "template": {
         "currency_template": "Currency Template – For DXY, major cross pairs, NEER, REER, and FX volatility."
     },
     "data_points": [
         "Relative Strength: Tracking how a currency performs versus others or a basket.",
         "Competitiveness: Assessing overvaluation or undervaluation using real exchange rate indices.",
         "Volatility Trends: Understanding stability and stress periods in FX markets."
     ],
     "navigating_the_theme": "Spot rates, exchange rate indices, cross-pair movements, and FX volatility metrics structure system-level signals capturing capital allocation shifts, trade imbalances, monetary policy divergence, and systemic currency stress regimes.",
     "conclusion_and_further_exploration": "Currency indicators serve as composite signals reflecting trade competitiveness, policy alignment gradients, external balance stress points, and capital flow sensitivity across macroeconomic cycles.",
     "memberships": {
         "1001_dxy_index": {
             "overview": "The US Dollar Index (DXY) measures the value of the USD against a basket of major world currencies.",
             "why_it_matters": "Widely referenced as a gauge of global USD strength, often inversely correlated with commodities and risk appetite.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟🌟 - Changes in DXY can ripple through commodities, EM assets, and global equities.",
             "personal_impact_importance": "🌟🌟 - Currency strength influences import costs, travel, and inflation transmission.",
             "current_vs_previous": "Track week-to-week or month-to-month USD strength changes.",
             "points_percentage_changes": "Shows USD appreciation or depreciation trend magnitude.",
             "min_max_12months": "Identify dollar strength/weakness extremes over the past year.",
             "averages": "Smooth dollar index fluctuations over time.",
             "year_over_year": "Assess broader cyclical shifts in dollar strength.",
             "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
             "path": "pages/1001_dxy_index.py"
         },
         "1002_usd_fx_crosses": {
             "overview": "Tracks the USD's performance against individual currencies (e.g., EUR/USD, USD/JPY, GBP/USD).",
             "why_it_matters": "Helps assess bilateral trade dynamics, monetary divergence, and capital flow shifts.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Useful for interpreting regional currency strength and relative momentum.",
             "personal_impact_importance": "🌟 - FX rates affect import/export pricing, remittances, and foreign spending power.",
             "current_vs_previous": "Compare weekly or monthly FX cross changes.",
             "points_percentage_changes": "Capture fluctuations in bilateral exchange rates.",
             "min_max_12months": "Identify performance extremes for each pair.",
             "averages": "Evaluate relative value trends.",
             "year_over_year": "Track longer-term currency cycles.",
             "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
             "path": "pages/1002_usd_fx_crosses.py"
         },
         "1003_neer_index": {
             "overview": "Nominal Effective Exchange Rate (NEER) shows a country's average currency value relative to a basket of other currencies, unadjusted for inflation.",
             "why_it_matters": "Used to evaluate trade competitiveness and nominal relative strength.",
             "temporal_categorisation": "Coincident indicator",
             "investment_action_importance": "🌟🌟 - Key for gauging relative FX movements vs trade partners.",
             "personal_impact_importance": "🌟 - Impacts trade competitiveness and import prices.",
             "current_vs_previous": "Track nominal relative strength shifts.",
             "points_percentage_changes": "Assess short-term currency appreciation/depreciation.",
             "min_max_12months": "Detect cyclical nominal extremes.",
             "averages": "Smooth fluctuations for better macro insight.",
             "year_over_year": "Useful for inflation pass-through and trade trend context.",
             "recommended_time_periods": ["1M", "3M", "6M", "12M"],
             "path": "pages/1003_neer_index.py"
         },
         "1004_reer_index": {
             "overview": "The Real Effective Exchange Rate (REER) adjusts NEER for relative inflation differences, offering a truer measure of currency value.",
             "why_it_matters": "Critical for evaluating actual trade competitiveness over time.",
             "temporal_categorisation": "Lagging indicator",
             "investment_action_importance": "🌟🌟🌟 - Helps identify currency misalignments and pricing power shifts.",
             "personal_impact_importance": "🌟 - Affects purchasing power and longer-term import/export dynamics.",
             "current_vs_previous": "Track changes in real currency strength.",
             "points_percentage_changes": "Capture valuation swings adjusted for inflation.",
             "min_max_12months": "Highlight over- or undervaluation extremes.",
             "averages": "Reveal fair value trends over time.",
             "year_over_year": "Support structural competitiveness evaluation.",
             "recommended_time_periods": ["3M", "6M", "12M"],
             "path": "pages/1004_reer_index.py"
         },
         "1005_fx_volatility_index": {
             "overview": "Measures expected volatility in foreign exchange markets (e.g., JPM VXY or similar indices).",
             "why_it_matters": "Used to assess risk appetite and stress across currency markets.",
             "temporal_categorisation": "Leading indicator",
             "investment_action_importance": "🌟🌟🌟 - Volatility spikes often signal cross-asset risk-on/risk-off rotations.",
             "personal_impact_importance": "🌟 - FX volatility may impact hedging costs and currency-linked pricing.",
             "current_vs_previous": "Compare recent volatility changes vs baseline.",
             "points_percentage_changes": "Identify intensity of short-term swings.",
             "min_max_12months": "Find volatility spikes and calm periods.",
             "averages": "Gauge typical volatility levels for reference.",
             "year_over_year": "Understand structural shifts in FX market behaviour.",
             "recommended_time_periods": ["1W", "1M", "3M", "12M"],
             "path": "pages/1005_fx_volatility_index.py"
             },
         }
     },
    "1100_market_trends_financial_health": {
        "theme_title": "Market Trends and Financial Health",
        "theme_introduction": "Market trend indicators capture equity market performance dynamics, macroeconomic shock absorption, investor positioning shifts, and system-level risk rotations tied to financial market health and macro regime alignment.",
        "temporal_categorisation": {
            "coincident_indicators": "Metrics that reflect the current performance of equity markets and asset class behaviour.",
            "leading_indicators": "Indices and trends that anticipate future market direction or investor sentiment.",
            "lagging_indicators": "Confirmatory data that validates existing trends and conditions in financial markets."
        },
        "template": {
            "equity_index_template": "Equity Index Template – For broad, sectoral, regional, and thematic equity market trends.",
            "surprise_index_template": "Surprise Index Template – For tracking economic surprises across regions like the US and EU."
        },
        "data_points": [
            "Historical Trends: Analyze past equity index behaviour to understand macro-financial cycles.",
            "Relative Strength: Track how various equity categories (value vs growth, small vs large cap) behave under different regimes.",
            "Macro Shock Response: Assess how markets have reacted to positive or negative economic surprises."
        ],
        "navigating_the_theme": "Equity indices, sector dispersion metrics, surprise indices, and relative strength rotations provide system-level signals tracking capital allocation shifts, leadership transitions, and sentiment adjustment processes aligned to cyclical macroeconomic narratives.",
        "conclusion_and_further_exploration": "Market trend signals serve as composite markers reflecting cyclical leadership shifts, systemic volatility transitions, regional capital allocation gradients, and macroeconomic news sensitivity across evolving financial regimes.",
        "memberships": {
            "1101_broad_equity_index": {
                "overview": "Tracks headline equity market performance for large, diversified indices (e.g., S&P 500, MSCI World).",
                "why_it_matters": "Serves as a benchmark for assessing broad equity performance and macroeconomic health.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Widely used reference for risk-on/risk-off dynamics, asset allocation posture, and volatility trends.",
                "personal_impact_importance": "🌟🌟 - Often tied to retirement accounts and broader financial well-being.",
                "current_vs_previous": "Tracks index movement across recent periods.",
                "points_percentage_changes": "Captures magnitude of returns in absolute and relative terms.",
                "min_max_12months": "Displays annual volatility and return range.",
                "averages": "Reveals trend strength via moving averages.",
                "year_over_year": "Highlights longer-term performance.",
                "recommended_time_periods": ["1W", "1M", "3M", "6M", "12M"],
                "path": "pages/1101_broad_equity_index.py"
            },
            "1102_sector_equity_index": {
                "overview": "Tracks performance of specific economic sectors such as technology, energy, or financials.",
                "why_it_matters": "Reveals sectoral leadership during various macro phases (inflation, growth, recession, etc.).",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Useful for top-down positioning and thematic monitoring.",
                "personal_impact_importance": "🌟 - May correlate with employment or regional economic trends.",
                "current_vs_previous": "Compares recent sector performance.",
                "points_percentage_changes": "Tracks sector gains/losses over time.",
                "min_max_12months": "Sector highs/lows used in rotation models.",
                "averages": "Supports trend durability analysis.",
                "year_over_year": "Evaluates relative strength over long cycles.",
                "recommended_time_periods": ["1M", "3M", "6M", "12M"],
                "path": "pages/1102_sector_equity_index.py"
            },
            "1103_emerging_market_equity_index": {
                "overview": "Reflects equity market activity in developing economies.",
                "why_it_matters": "Useful for global diversification context and understanding capital flow risk.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Emerging markets often experience outsized volatility and are sensitive to global liquidity.",
                "personal_impact_importance": "🌟 - May affect commodity-linked markets and multinational company revenues.",
                "current_vs_previous": "Evaluates relative strength and stability of EM vs DM.",
                "points_percentage_changes": "Supports return comparison and exposure calibration.",
                "min_max_12months": "Shows volatility of EM indices.",
                "averages": "Evaluates sustained under/overperformance.",
                "year_over_year": "Captures long-cycle shifts and capital reallocation patterns.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/1103_emerging_market_equity_index.py"
            },
            "1104_value_vs_growth_index": {
                "overview": "Tracks relative performance between value-oriented and growth-oriented equities.",
                "why_it_matters": "Captures macro rotation themes influenced by rates, inflation, and liquidity.",
                "temporal_categorisation": "Leading/Rotational indicator",
                "investment_action_importance": "🌟🌟 - Reflects underlying equity risk sentiment and macro bias.",
                "personal_impact_importance": "🌟 - May be tied to ETF or retirement account structure.",
                "current_vs_previous": "Monitors performance reversals and inflection points.",
                "points_percentage_changes": "Shows the magnitude of leadership transitions.",
                "min_max_12months": "Displays peaks and troughs in style dominance.",
                "averages": "Smooths relative performance trendlines.",
                "year_over_year": "Signals prolonged market regime shifts.",
                "recommended_time_periods": ["1M", "3M", "6M", "12M"],
                "path": "pages/1104_value_vs_growth_index.py"
            },
            "1105_cyclical_vs_defensive_index": {
                "overview": "Monitors performance between economically sensitive and defensive sectors.",
                "why_it_matters": "Indicates economic confidence or caution, especially during policy or earnings shifts.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Used to evaluate market breadth and momentum strength.",
                "personal_impact_importance": "🌟 - Tied to shifts in consumer/business confidence.",
                "current_vs_previous": "Tracks spread directionality.",
                "points_percentage_changes": "Helps calibrate equity exposure risk.",
                "min_max_12months": "Used to monitor regime durability.",
                "averages": "Evaluates rotation timing.",
                "year_over_year": "Highlights performance gaps between sectors.",
                "recommended_time_periods": ["1M", "3M", "6M"],
                "path": "pages/1105_cyclical_vs_defensive_index.py"
            },
            "1106_small_cap_vs_large_cap_index": {
                "overview": "Compares the performance of small-cap and large-cap equities.",
                "why_it_matters": "Reflects risk appetite and credit sensitivity in equity markets.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Helps gauge market risk tolerance and growth expectations.",
                "personal_impact_importance": "🌟 - Smaller company trends often reflect entrepreneurial sentiment and funding flows.",
                "current_vs_previous": "Identifies shifts in capital allocation.",
                "points_percentage_changes": "Assesses outperformance magnitude.",
                "min_max_12months": "Signals rotation or extended trend fatigue.",
                "averages": "Measures leadership consistency.",
                "year_over_year": "Evaluates relative resilience across business cycles.",
                "recommended_time_periods": ["1M", "3M", "6M"],
                "path": "pages/1106_small_cap_vs_large_cap_index.py"
            },
            "1107_economic_surprise_index_us": {
                "overview": "Tracks whether US economic data releases exceed or fall short of expectations.",
                "why_it_matters": "Useful for assessing sentiment, volatility risk, and macroeconomic adjustment pressure.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - High surprises can cause bond yield moves, FX strength, or equity rallies.",
                "personal_impact_importance": "🌟 - Reflects economic momentum that may filter into employment or inflation shifts.",
                "current_vs_previous": "Tracks change in data surprise level week-over-week.",
                "points_percentage_changes": "Highlights directionality and magnitude of surprise momentum.",
                "min_max_12months": "Shows volatility in economic newsflow.",
                "averages": "Smooths noise for policy signal tracking.",
                "year_over_year": "Contextual comparison of current vs prior regime surprises.",
                "recommended_time_periods": ["1W", "1M", "3M"],
                "path": "pages/1107_economic_surprise_index_us.py"
            },
            "1108_economic_surprise_index_eu": {
                "overview": "Monitors surprise dynamics across Eurozone economic data releases.",
                "why_it_matters": "Helps interpret policy surprise risk in ECB settings and euro area growth signals.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Signals market misalignment with macro data.",
                "personal_impact_importance": "🌟 - Surprise swings may foreshadow currency moves or regional shifts.",
                "current_vs_previous": "Weekly shift tracking in surprise metrics.",
                "points_percentage_changes": "Captures sharp revisions or volatility in Eurozone data.",
                "min_max_12months": "Highlights historic sentiment regime reversals.",
                "averages": "Assesses policy signal stability.",
                "year_over_year": "Annual sentiment comparison vs macro backdrop.",
                "recommended_time_periods": ["1W", "1M", "3M"],
                "path": "pages/1108_economic_surprise_index_eu.py"
            },
        }
    },
    "1200_industry_performance_production": {
    "theme_title": "Industry Performance and Production",
    "theme_introduction": "ndustry performance indicators capture manufacturing output cycles, capacity utilization dynamics, sector momentum trends, and operational efficiency regimes tied to business cycle amplitude and production stability.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect current production trends and utilization, providing real-time insights into industrial activity.",
        "leading_indicators": "Offer early signals of business cycle shifts based on order flow and service sentiment.",
        "lagging_indicators": "Support validation of long-term output patterns and structural efficiency."
    },
    "template": {
        "pmi_template": "PMI Template – For ISM/S&P PMIs, new orders, business activity.",
        "industrial_production_template": "Industrial Production Template – For output, capacity utilization, steel usage."
    },
    "data_points": [
        "Production Cycles: Analysis of contraction/expansion phases in manufacturing.",
        "Sectoral Activity: Review of output trends and capacity indicators.",
        "Business Conditions: Forward-looking assessments of order flows and sentiment."
    ],
    "navigating_the_theme": "Purchasing manager indices, industrial production measures, capacity utilization levels, and sectoral order flows structure system-level signals reflecting production resilience, cyclical momentum transitions, and manufacturing-driven macroeconomic positioning.",
    "conclusion_and_further_exploration": "Industry and production indicators serve as composite signals framing business cycle amplitude, sector expansion durability, and systemic production capacity alignment across evolving macro regimes.",
    "memberships": {
        "1201_manufacturing_pmi": {
            "overview": "Tracks sentiment in manufacturing, capturing output, orders, and inventories across firms.",
            "why_it_matters": "Used globally to assess business sentiment and potential inflection points in economic activity.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟🌟 - Highlights early-cycle trends, influencing top-down allocation.",
            "personal_impact_importance": "🌟 - May reflect employment or wage expectations in industrial sectors.",
            "current_vs_previous": "Highlights changes in headline PMI sentiment.",
            "points_percentage_changes": "Tracks directional shifts from expansion (>50) or contraction (<50).",
            "min_max_12months": "Shows PMI sentiment ranges over the past year.",
            "averages": "Contextualises normal levels of optimism or caution.",
            "year_over_year": "Not always applicable due to short-term sentiment nature.",
            "recommended_time_periods": ["MM", "3M", "6M"],
            "path": "pages/1201_manufacturing_pmi.py"
        },
        "1202_services_pmi": {
            "overview": "Captures service sector sentiment across employment, orders, and pricing.",
            "why_it_matters": "Complements manufacturing PMI to gauge broader economic activity, especially in service-led economies.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Helps identify consumption-related demand shifts.",
            "personal_impact_importance": "🌟 - Service-sector changes can affect employment conditions.",
            "current_vs_previous": "Reviews service sentiment momentum.",
            "points_percentage_changes": "Evaluates strength or softening in reported business activity.",
            "min_max_12months": "Identifies cyclical extremes in sentiment.",
            "averages": "Provides trend-level outlook.",
            "year_over_year": "Limited value due to month-to-month focus.",
            "recommended_time_periods": ["MM", "3M"],
            "path": "pages/1202_services_pmi.py"
        },
        "1203_new_orders_pmi": {
            "overview": "Measures new order flow in manufacturing and services.",
            "why_it_matters": "Leads output and hiring decisions; a powerful forward-looking signal.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟🌟 - Often cited as an early demand signal.",
            "personal_impact_importance": "🌟 - Shifts in new orders may impact future job stability.",
            "current_vs_previous": "Compares latest sentiment in order flow.",
            "points_percentage_changes": "Tracks marginal order improvements or declines.",
            "min_max_12months": "Detects order cycle extremes.",
            "averages": "Contextualises structural order demand.",
            "year_over_year": "Used to benchmark annual trend sentiment.",
            "recommended_time_periods": ["MM", "3M", "6M"],
            "path": "pages/1203_new_orders_pmi.py"
        },
        "1204_business_activity_pmi": {
            "overview": "Focuses on real-time business output expectations and performance.",
            "why_it_matters": "Tracks expansion/contraction phases and business performance signals.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - May inform sector-based cyclical views.",
            "personal_impact_importance": "🌟 - Activity data may affect hiring or wage sentiment.",
            "current_vs_previous": "Shows direction of activity momentum.",
            "points_percentage_changes": "Signals sentiment shifts in workload.",
            "min_max_12months": "Identifies historic confidence swings.",
            "averages": "Frames longer-term trend range.",
            "year_over_year": "Limited in value due to short survey cycles.",
            "recommended_time_periods": ["MM", "3M"],
            "path": "pages/1204_business_activity_pmi.py"
        },
        "1205_industrial_production_index": {
            "overview": "Tracks real output in industrial sectors like manufacturing, utilities, and mining.",
            "why_it_matters": "Key measure of physical economic production, relevant to energy, capital goods, and logistics.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Used to validate cyclical strength or capacity strain.",
            "personal_impact_importance": "🌟 - Can affect employment in manufacturing-heavy regions.",
            "current_vs_previous": "Tracks short-run changes in real output.",
            "points_percentage_changes": "Measures production shifts across goods.",
            "min_max_12months": "Shows production cycle highs and lows.",
            "averages": "Sheds light on trend persistence.",
            "year_over_year": "Supports economic benchmarking.",
            "recommended_time_periods": ["MM", "3M", "6M", "12M"],
            "path": "pages/1205_industrial_production_index.py"
        },
        "1206_capacity_utilization_rate": {
            "overview": "Measures the extent to which productive capacity is being used.",
            "why_it_matters": "Higher utilization may precede inflationary pressures or capital investment.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Signals operational efficiency or slack.",
            "personal_impact_importance": "🌟 - May affect job creation or wage trends.",
            "current_vs_previous": "Compares recent capacity changes.",
            "points_percentage_changes": "Reveals stress or slack in the system.",
            "min_max_12months": "Benchmarks operational extremes.",
            "averages": "Shows normal production intensity.",
            "year_over_year": "Used in capacity trend analysis.",
            "recommended_time_periods": ["MM", "3M", "6M"],
            "path": "pages/1206_capacity_utilization_rate.py"
        },
        "1207_steel_utilization_index": {
            "overview": "Tracks production and use of steel as a proxy for industrial health.",
            "why_it_matters": "Heavily used in construction, manufacturing, and infrastructure—often an early signal of hard demand.",
            "temporal_categorisation": "Coincident to leading indicator",
            "investment_action_importance": "🌟 - Niche signal, especially for commodity or construction-related trades.",
            "personal_impact_importance": "🌟 - Reflects demand-side industrial resilience.",
            "current_vs_previous": "Tracks steel production changes.",
            "points_percentage_changes": "Reveals shifts in heavy industry usage.",
            "min_max_12months": "Useful for cyclical sentiment.",
            "averages": "Frames steady-state usage.",
            "year_over_year": "Benchmarks broad activity swings.",
            "recommended_time_periods": ["MM", "3M", "6M"],
            "path": "pages/1207_steel_utilization_index.py"
            },
        }
    },
    "1300_sustainability_green_economy": {
    "theme_title": "Sustainability and Green Economy",
    "theme_introduction": "Sustainability indicators reflect the structural transition toward low-carbon economic models, green energy capacity scaling, regulatory alignment regimes, and long-horizon capital allocation shifts tied to decarbonisation objectives.",
    "temporal_categorisation": {
        "coincident_indicators": "Track real-time production and emissions data tied to economic output and energy use.",
        "leading_indicators": "Early signals of green investment trends, policy support, and infrastructure development.",
        "lagging_indicators": "Structural changes in emissions intensity or green adoption post major reforms."
    },
    "template": {
        "sustainability_template": "Sustainability Template – For green energy production, carbon emissions intensity, and sustainable investment flows."
    },
    "data_points": [
        "Emissions Intensity Trends: Gauge economic activity versus environmental cost.",
        "Investment Shifts: Track capital movement into renewable sectors and technologies.",
        "Policy Alignment: Assess how green efforts align with regulatory and global initiatives (e.g., Paris Agreement)."
    ],
    "navigating_the_theme": "Emissions intensity metrics, renewable capacity growth, green investment flows, and policy alignment indices structure system-level signals capturing resource transition depth, sector rotation gradients, and macroeconomic realignment under sustainability mandates.",
    "conclusion_and_further_exploration": "Sustainability signals serve as composite markers reflecting structural capital reallocation, long-cycle energy transition processes, policy-aligned investment flows, and decarbonisation trajectory alignment across national and sectoral systems.",
    "memberships": {
        "1301_carbon_emissions_gdp": {
            "overview": "This indicator measures carbon dioxide emissions per unit of GDP, capturing the environmental intensity of economic activity.",
            "why_it_matters": "Used to evaluate decarbonization progress and the efficiency of economic growth in lowering emissions.",
            "temporal_categorisation": "Lagging indicator",
            "investment_action_importance": "🌟🌟 - Useful for assessing the long-term transition risk of economies and sectors tied to fossil fuels.",
            "personal_impact_importance": "🌟 - Reflects alignment with climate goals and the broader sustainability narrative.",
            "current_vs_previous": "Track progress in emissions efficiency over time.",
            "points_percentage_changes": "Assess shifts in emissions per economic unit.",
            "min_max_12months": "Spot annual highs and lows in environmental intensity.",
            "averages": "Identify consistent improvement or setbacks.",
            "year_over_year": "Reveal structural change or stalling.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1301_carbon_emissions_gdp.py"
        },
        "1302_renewable_energy_production": {
            "overview": "Tracks the share or total volume of energy derived from renewable sources like solar, wind, hydro, and geothermal.",
            "why_it_matters": "A leading signal of energy transition, investment opportunity, and policy-driven infrastructure evolution.",
            "temporal_categorisation": "Coincident to leading indicator",
            "investment_action_importance": "🌟🌟🌟 - Critical for understanding trends in energy markets, technology adoption, and resource shift.",
            "personal_impact_importance": "🌟🌟 - Affects household energy policies, pricing, and sustainability awareness.",
            "current_vs_previous": "Compare recent renewable output versus prior months or years.",
            "points_percentage_changes": "Monitor the pace of adoption and grid integration.",
            "min_max_12months": "Spot records and seasonal performance.",
            "averages": "Reveal sustainable trajectory trends.",
            "year_over_year": "Gauge broader success of energy transition.",
            "recommended_time_periods": ["1M", "6M", "1Y", "3Y"],
            "path": "pages/1302_renewable_energy_production.py"
        },
        "1303_green_investment_trends": {
            "overview": "Measures capital flows into green sectors, ESG-focused funds, and renewable infrastructure.",
            "why_it_matters": "Indicates market sentiment toward sustainability and regulatory traction around ESG mandates.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Signals where institutional and policy capital is being deployed.",
            "personal_impact_importance": "🌟 - Reflects growing access to green financial products and long-term planning.",
            "current_vs_previous": "Evaluate monthly or quarterly investment flows.",
            "points_percentage_changes": "Track upticks or slowdowns in ESG momentum.",
            "min_max_12months": "Spot surges linked to regulation or policy shifts.",
            "averages": "Assess baseline participation growth.",
            "year_over_year": "Anchor long-term green capital trends.",
            "recommended_time_periods": ["3M", "6M", "1Y"],
            "path": "pages/1303_green_investment_trends.py"
            },
        }
    },
    "1400_digital_economy_ecommerce": {
    "theme_title": "Digital Economy and E-Commerce",
    "theme_introduction": "Digital economy indicators reflect structural transformation across economic activities driven by digital infrastructure deployment, platform penetration rates, online consumption expansion, and technology-driven productivity regimes.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect the current adoption and output levels of digital services within the broader economy.",
        "leading_indicators": "Signal shifts toward digital transformation, consumer behaviour changes, and technological integration.",
        "lagging_indicators": "Highlight long-term changes in economic composition and workforce due to digitization."
    },
    "template": {
        "digital_economy_template": "Digital Economy Template – For internet access, e-commerce penetration, and growth in digital transactions."
    },
    "data_points": [
        "Digital Infrastructure: The foundational role of internet access in enabling growth.",
        "Consumption Shifts: How spending behaviour adapts to digital retail formats.",
        "Structural Adoption: The role of digital in employment, supply chains, and macro resilience."
    ],
    "navigating_the_theme": "Internet access rates, e-commerce penetration levels, digital transaction volumes, and structural platform integration measures provide system-level signals capturing consumption transitions, sectoral substitution patterns, and digital productivity leverage across economies.",
    "conclusion_and_further_exploration": "Digital economy signals serve as composite markers reflecting technological absorption depth, structural consumption reallocation, cross-sector platform scaling dynamics, and macroeconomic competitiveness positioning under digitalisation transitions.",
    "memberships": {
        "1401_internet_penetration_rate": {
            "overview": "Measures the percentage of the population with access to the internet, serving as a foundational enabler of the digital economy.",
            "why_it_matters": "High penetration supports scalability of e-commerce, digital services, and remote work ecosystems.",
            "temporal_categorisation": "Coincident to leading indicator",
            "investment_action_importance": "🌟🌟 - Indicates market readiness for digital services, platforms, and infrastructure deployment.",
            "personal_impact_importance": "🌟🌟 - Enhances access to jobs, education, healthcare, and e-commerce opportunities.",
            "current_vs_previous": "Track improvements in population coverage.",
            "points_percentage_changes": "Assess expansion velocity and access gaps.",
            "min_max_12months": "Spot coverage milestones or plateauing.",
            "averages": "Gauge long-run access trends.",
            "year_over_year": "Monitor long-term infrastructure and policy effects.",
            "recommended_time_periods": ["6M", "1Y", "3Y"],
            "path": "pages/1401_internet_penetration_rate.py"
        },
        "1402_ecommerce_gdp_contribution": {
            "overview": "Represents the share of GDP generated by digital commerce activities, including online retail, marketplaces, and digital service platforms.",
            "why_it_matters": "A proxy for economic digitization, e-commerce reflects consumption shifts, business model changes, and platform-led growth.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟🌟 - Highlights where digital sectors may be expanding their economic footprint and influencing consumption.",
            "personal_impact_importance": "🌟🌟 - Demonstrates increasing household engagement with digital services and pricing ecosystems.",
            "current_vs_previous": "Assess growing or contracting GDP share.",
            "points_percentage_changes": "Track major accelerations linked to policy or technology.",
            "min_max_12months": "Spot e-commerce peaks and seasonal troughs.",
            "averages": "Understand structural composition over time.",
            "year_over_year": "Frame longer-term digital substitution trends.",
            "recommended_time_periods": ["1Q", "1Y", "3Y"],
            "path": "pages/1402_ecommerce_gdp_contribution.py"
        },
        "1403_digital_sales_growth": {
            "overview": "Tracks the rate of change in digital or online sales across sectors, often expressed as a monthly or annual growth percentage.",
            "why_it_matters": "Signals adoption momentum and the strength of the digital retail ecosystem.",
            "temporal_categorisation": "Leading to coincident indicator",
            "investment_action_importance": "🌟🌟 - Provides context on demand shifts, platform penetration, and consumer confidence.",
            "personal_impact_importance": "🌟 - Reflects access, preference, and price sensitivity in household spending.",
            "current_vs_previous": "Monthly trend tracking.",
            "points_percentage_changes": "Capture growth surges or slowdowns.",
            "min_max_12months": "Spot e-commerce volatility or resilience.",
            "averages": "Compare normalised periods (e.g., post-COVID or regulatory shifts).",
            "year_over_year": "Anchor long-run adoption insights.",
            "recommended_time_periods": ["1M", "3M", "6M", "1Y"],
            "path": "pages/1403_digital_sales_growth.py"
            },
        }
    },
    "1500_innovation_rd_investment": {
    "theme_title": "Innovation and R&D Investment",
    "theme_introduction": "Innovation and R&D indicators reflect structural knowledge capital formation, intellectual property expansion, technological leadership gradients, and long-horizon productivity growth trajectories across economies and sectors.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect current national and sector-level innovation output or spending.",
        "leading_indicators": "Signal future growth potential based on knowledge creation and R&D intensity.",
        "lagging_indicators": "Confirm sustained investment in innovation and its economic returns over time."
    },
    "template": {
        "innovation_template": "Innovation Template – For innovation rankings, patent applications, and R&D expenditure trends."
    },
    "data_points": [
        "Knowledge Capital: Assess the foundations for productivity and future growth.",
        "Technological Output: Examine the rate and scope of patentable or proprietary technologies.",
        "Public/Private Investment Trends: Track how capital is allocated toward forward-looking innovation."
    ],
    "navigating_the_theme": "Patent output volumes, R&D expenditure ratios, innovation rankings, and technological development composites structure system-level signals capturing frontier positioning, intellectual capital scaling, and innovation-driven productivity leverage.",
    "conclusion_and_further_exploration": "Innovation and R&D signals serve as composite markers reflecting long-cycle growth differentials, competitive productivity asymmetries, and sectoral leadership positioning across evolving technological adoption regimes.",
    "memberships": {
        "1501_innovation_index": {
            "overview": "Captures a country's relative innovation capacity using composite metrics including education, infrastructure, R&D investment, and patent output.",
            "why_it_matters": "Useful for comparing innovation ecosystems and forecasting long-term growth environments.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Offers context for identifying economies or sectors with forward-looking capacity.",
            "personal_impact_importance": "🌟 - Linked to job creation, technological access, and long-term wage dynamics.",
            "current_vs_previous": "Track year-to-year movement in rankings or scores.",
            "points_percentage_changes": "Compare index changes across countries or over time.",
            "min_max_12months": "Identify peaks or troughs in composite scores.",
            "averages": "Smooth cyclical volatility for trend clarity.",
            "year_over_year": "Assess sustained innovation performance.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1501_innovation_index.py"
        },
        "1502_patent_applications": {
            "overview": "Measures the volume of patents filed within a country or sector over a given time period.",
            "why_it_matters": "Patents represent tangible innovation output and intellectual property creation.",
            "temporal_categorisation": "Coincident to leading indicator",
            "investment_action_importance": "🌟🌟 - Tracks technological leadership and commercialization potential.",
            "personal_impact_importance": "🌟 - Reflects national innovation and potential job creation in high-tech sectors.",
            "current_vs_previous": "Month-to-month or annual filing comparisons.",
            "points_percentage_changes": "Measure spikes in innovation cycles.",
            "min_max_12months": "Spot high-activity periods.",
            "averages": "Analyze underlying innovation pace.",
            "year_over_year": "Assess structural growth in IP creation.",
            "recommended_time_periods": ["6M", "1Y", "3Y"],
            "path": "pages/1502_patent_applications.py"
        },
        "1503_rd_spending_gdp": {
            "overview": "Tracks gross domestic expenditure on research and development as a percentage of GDP.",
            "why_it_matters": "A key proxy for innovation intensity and future growth potential.",
            "temporal_categorisation": "Lagging to coincident indicator",
            "investment_action_importance": "🌟🌟🌟 - Long-term signal of national or sectoral commitment to innovation.",
            "personal_impact_importance": "🌟🌟 - Affects job creation and innovation-driven consumption trends.",
            "current_vs_previous": "Review yearly updates in budgetary commitment.",
            "points_percentage_changes": "Track increases or cuts in R&D budgets.",
            "min_max_12months": "Evaluate long-term high/low spending periods.",
            "averages": "Understand persistent trends in innovation allocation.",
            "year_over_year": "Review structural commitment to research.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1503_rd_spending_gdp.py"
            },
        }
    },
    "1600_urbanisation_and_smart_cities": {
    "theme_title": "Urbanisation and Smart Cities",
    "theme_introduction": "Urbanisation and smart infrastructure indicators reflect spatial growth dynamics, population agglomeration effects, infrastructure scalability regimes, and adaptive technology deployment across evolving city systems.",
    "temporal_categorisation": {
        "coincident_indicators": "Show the present scale and distribution of urban population and infrastructure usage.",
        "leading_indicators": "Signal future capacity needs, real estate dynamics, and urban policy developments.",
        "lagging_indicators": "Confirm the long-term impact of infrastructure investments and demographic migration trends."
    },
    "template": {
        "urbanisation_template": "Urbanisation Template – Tracks urban population dynamics, infrastructure deployment, and smart city investment."
    },
    "data_points": [
        "Urban Expansion Patterns: Growth of metropolitan areas and shifts in population density.",
        "Infrastructure Modernisation: Deployment of intelligent systems, transportation, and energy efficiency.",
        "Service Access: Equity and scalability of essential services within dense urban environments."
    ],
    "navigating_the_theme": "Urban population expansion rates, infrastructure deployment metrics, smart city investment flows, and service delivery indices structure system-level signals capturing spatial economic stress, urban resilience capacity, and infrastructure modernization gradients.",
    "conclusion_and_further_exploration": "Urbanisation and smart city signals serve as composite markers reflecting demographic pressure gradients, infrastructure capital allocation cycles, service delivery efficiency, and spatial growth alignment across evolving macroeconomic systems.",
    "memberships": {
        "1601_urban_population_growth": {
            "overview": "Tracks the rate of population growth in urban areas relative to rural or national growth.",
            "why_it_matters": "Higher urbanisation often correlates with rising infrastructure needs, real estate demand, and service delivery challenges.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Offers context for construction trends and regional growth stories.",
            "personal_impact_importance": "🌟🌟 - Reflects evolving housing, transportation, and employment dynamics.",
            "current_vs_previous": "Measures change in urban population share over recent periods.",
            "points_percentage_changes": "Highlights absolute and relative shifts in population trends.",
            "min_max_12months": "Identifies the range of urban growth experienced within a year.",
            "averages": "Smooths temporary spikes in migration or reclassification.",
            "year_over_year": "Assesses broader shifts toward urbanisation over time.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1601_urban_population_growth.py"
        },
        "1602_urban_density_services_index": {
            "overview": "Measures the relationship between population density and service delivery (e.g., healthcare, transport, utilities).",
            "why_it_matters": "Essential for evaluating the resilience, accessibility, and quality of urban services.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟 - Reflects the efficiency and scalability of infrastructure.",
            "personal_impact_importance": "🌟🌟 - Affects quality of life, commute times, and access to essential services.",
            "current_vs_previous": "Tracks changes in density relative to service capacity.",
            "points_percentage_changes": "Identifies improvements or deterioration in service availability per capita.",
            "min_max_12months": "Shows strain or improvement across key urban metrics.",
            "averages": "Highlights service adequacy across different cities or regions.",
            "year_over_year": "Compares systemic change over a longer period.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1602_urban_density_services_index.py"
        },
        "1603_smart_infrastructure_investment": {
            "overview": "Tracks public and private investment into smart infrastructure, such as transport tech, digital grids, and intelligent systems.",
            "why_it_matters": "Smart infrastructure signals a shift toward sustainable urban living and efficient city management.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Helps contextualise technology deployment in real estate, utilities, and mobility.",
            "personal_impact_importance": "🌟🌟 - Reflects shifts in urban experience, from traffic patterns to green energy solutions.",
            "current_vs_previous": "Monitors changes in smart infrastructure capital allocation.",
            "points_percentage_changes": "Captures rising or falling investment commitments.",
            "min_max_12months": "Highlights periods of intense infrastructure focus.",
            "averages": "Normalises data for trend tracking and regional comparison.",
            "year_over_year": "Evaluates commitment to long-term digital transformation.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1603_smart_infrastructure_investment.py"
            },
        }
    },
    "1700_healthcare_economics": {
    "theme_title": "Healthcare Economics",
    "theme_introduction": "Healthcare economics indicators reflect resource allocation structures, access differentials, expenditure regimes, system efficiency gradients, and demographic demand dynamics embedded within national health delivery frameworks.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect the current status of health system coverage and expenditure.",
        "leading_indicators": "May point to evolving access or spending priorities that will shape future healthcare delivery.",
        "lagging_indicators": "Confirm long-term health system trends and historical policy impacts."
    },
    "template": {
        "healthcare_template": "Healthcare Template – For access indices, public vs private healthcare trends, and spending patterns."
    },
    "data_points": [
        "Access & Equity: Who receives care, and how evenly is it distributed?",
        "Cost Allocation: How healthcare costs are funded—public vs private systems.",
        "Expenditure Monitoring: Trends in total and per capita healthcare outlays over time."
    ],
    "navigating_the_theme": "Healthcare access indices, public-private cost distribution metrics, expenditure scaling trends, and per capita spending trajectories structure system-level signals capturing policy alignment, demographic stress gradients, and long-term healthcare system sustainability positioning.",
    "conclusion_and_further_exploration": "Healthcare economics signals serve as composite markers reflecting fiscal sustainability regimes, service delivery efficiency, policy-induced allocation gradients, and structural demographic pressures across evolving healthcare systems.",
    "memberships": {
        "1701_access_to_care_index": {
            "overview": "Evaluates the availability, quality, and equity of healthcare services across populations.",
            "why_it_matters": "A core proxy for social stability, inclusion, and health sector reach. It reflects access gaps and potential stress points in systems.",
            "temporal_categorisation": "Coincident to lagging indicator",
            "investment_action_importance": "🌟 - Provides social context; less directly actionable but may inform long-term healthcare system trends.",
            "personal_impact_importance": "🌟🌟🌟 - Strong implications for personal outcomes, longevity, and national wellness.",
            "current_vs_previous": "Monitor improvements or regressions in healthcare delivery.",
            "points_percentage_changes": "Track scale of change in care accessibility.",
            "min_max_12months": "Observe best/worst performance periods.",
            "averages": "Helps benchmark healthcare access levels over time.",
            "year_over_year": "Supports structural review of national systems.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1701_access_to_care_index.py"
        },
        "1702_healthcare_spending_gdp": {
            "overview": "Measures healthcare expenditures as a percentage of gross domestic product.",
            "why_it_matters": "Signals national prioritization of healthcare and structural cost pressures on the economy.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Highlights shifts in fiscal priorities and may influence broader macro or policy outlooks.",
            "personal_impact_importance": "🌟🌟 - Informs expectations around cost of care, insurance burden, and system access.",
            "current_vs_previous": "Compares recent spending levels to historical baselines.",
            "points_percentage_changes": "Track budgetary changes as a portion of GDP.",
            "min_max_12months": "Highlights high/low expenditure years.",
            "averages": "Helps reveal systemic healthcare allocation trends.",
            "year_over_year": "Supports broader fiscal context and health prioritization.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1702_healthcare_spending_gdp.py"
        },
        "1703_public_vs_private_spending": {
            "overview": "Compares the share of healthcare expenditures funded publicly versus privately (e.g., out-of-pocket, insurance).",
            "why_it_matters": "Reveals structural dynamics in health funding and potential burdens on individuals or public systems.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟 - Useful for understanding potential insurance market shifts or systemic strain.",
            "personal_impact_importance": "🌟🌟🌟 - Direct implications for out-of-pocket costs and access variability.",
            "current_vs_previous": "Evaluate the shift between public and private funding.",
            "points_percentage_changes": "Track trends in cost-sharing responsibility.",
            "min_max_12months": "Highlight funding dominance shifts over time.",
            "averages": "Reveal baseline cost-sharing dynamics.",
            "year_over_year": "Assess multi-year changes in healthcare burden distribution.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1703_public_vs_private_spending.py"
            },
        }
    },
    "1800_education_and_human_capital": {
    "theme_title": "Education and Human Capital",
    "theme_introduction": "Education and human capital indicators reflect long-horizon productivity capacity formation, workforce skill alignment gradients, demographic competitiveness positioning, and systemic innovation leverage potential embedded in labor market structures.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect the current state of educational access and workforce development.",
        "leading_indicators": "Signal future productivity potential, labor market capacity, and innovation readiness.",
        "lagging_indicators": "Confirm the effectiveness of long-term educational investment and policy reforms."
    },
    "template": {
        "education_template": "Education Template – For education expenditure, enrollment trends, and workforce readiness."
    },
    "data_points": [
        "Long-Term Investment Trends: Education spending as a percentage of GDP.",
        "Access and Attainment: Enrollment trends and gaps in post-secondary education.",
        "Workforce Alignment: Gaps between skills provided and labor market demand."
    ],
    "navigating_the_theme": "Education expenditure ratios, enrollment penetration levels, workforce readiness indices, and skill-demand alignment metrics structure system-level signals capturing knowledge capital development trajectories, labor force flexibility, and demographic productivity leverage across economies.",
    "conclusion_and_further_exploration": "Education and human capital signals serve as composite markers reflecting long-cycle growth capacity, structural workforce competitiveness, productivity asymmetries, and national innovation leverage under evolving economic regimes.",
    "memberships": {
        "1801_education_spending_gdp": {
            "overview": "Tracks public and private education expenditures as a percentage of GDP.",
            "why_it_matters": "A high share signals long-term investment in human capital and may reflect policy prioritization.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟 - Useful for identifying structural emphasis on human capital formation.",
            "personal_impact_importance": "🌟🌟 - Affects the quality of educational infrastructure, impacting lifetime earnings and societal mobility.",
            "current_vs_previous": "Compares current education funding to prior benchmarks.",
            "points_percentage_changes": "Measures relative changes in fiscal allocation.",
            "min_max_12months": "Shows highest and lowest levels of educational investment.",
            "averages": "Provides baseline context for educational prioritization.",
            "year_over_year": "Highlights long-term commitment trends.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1801_education_spending_gdp.py"
        },
        "1802_tertiary_enrollment": {
            "overview": "Measures enrollment in higher education institutions (e.g., universities, colleges) as a percentage of the eligible population.",
            "why_it_matters": "A key signal of future workforce qualification and knowledge-based economy readiness.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟 - Indicates human capital scalability and potential for innovation.",
            "personal_impact_importance": "🌟🌟🌟 - Directly relates to personal opportunity and employment competitiveness.",
            "current_vs_previous": "Tracks changes in access to post-secondary education.",
            "points_percentage_changes": "Highlights enrollment trends over time.",
            "min_max_12months": "Reveals historic highs/lows in participation.",
            "averages": "Smooths cyclical fluctuations.",
            "year_over_year": "Shows year-over-year educational access progress.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1802_tertiary_enrollment.py"
        },
        "1803_skills_gap_metrics": {
            "overview": "Assesses the mismatch between workforce skills and labor market demands.",
            "why_it_matters": "A rising skills gap can limit growth and productivity. Closing it enhances employment quality and competitiveness.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Critical for understanding labor market friction and automation exposure.",
            "personal_impact_importance": "🌟🌟🌟 - Influences employability, wage trends, and lifelong training needs.",
            "current_vs_previous": "Monitors widening or closing of skill mismatches.",
            "points_percentage_changes": "Measures shifts in education-to-employment alignment.",
            "min_max_12months": "Highlights periods of maximum mismatch or progress.",
            "averages": "Provides long-term perspective on structural misalignment.",
            "year_over_year": "Supports planning around talent pipeline reforms.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1803_skills_gap_metrics.py"
            },
        }
    },
    "1900_social_impact_and_inequality": {
    "theme_title": "Social Impact and Inequality",
    "theme_introduction": "Social impact and inequality indicators reflect systemic distribution gradients, resource allocation asymmetries, opportunity access differentials, and structural demographic divides embedded within long-cycle economic development trajectories.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect present levels of inequality or resource allocation.",
        "leading_indicators": "May suggest emerging stress points in social mobility, public sentiment, or policy demand.",
        "lagging_indicators": "Confirm entrenched disparities and the cumulative impact of prior economic cycles or policies."
    },
    "template": {
        "social_inequality_template": "Social Inequality Template – Focuses on distributional metrics such as income inequality, poverty levels, and social support structures."
    },
    "data_points": [
        "Distributional Trends: How economic gains are shared across populations and income brackets.",
        "Welfare Commitments: Levels of social safety nets, subsidies, and transfers.",
        "Structural Gaps: Persistent divergences in opportunity, education, or healthcare tied to inequality."
    ],
    "navigating_the_theme": "Income inequality indices, poverty distribution metrics, social support coverage ratios, and opportunity gap composites structure system-level signals capturing economic resilience gradients, latent social pressure buildup, and consumption stability asymmetries across macroeconomic cycles.",
    "conclusion_and_further_exploration": "Social inequality signals serve as composite markers reflecting resource distribution asymmetries, demographic participation gradients, political economy stress points, and long-horizon systemic sustainability alignment across evolving economic regimes.",
    "memberships": {
        "1901_gini_coefficient": {
            "overview": "Measures income or wealth inequality within a country on a 0 to 1 scale, where 0 indicates perfect equality and 1 indicates perfect inequality.",
            "why_it_matters": "Serves as a benchmark for evaluating fairness in income distribution and its implications for long-term stability and social cohesion.",
            "temporal_categorisation": "Lagging indicator",
            "investment_action_importance": "🌟🌟 - Helps evaluate macro fragility or populist risk in countries with extreme inequality.",
            "personal_impact_importance": "🌟🌟🌟 - Directly affects social mobility, opportunity, and household outcomes.",
            "current_vs_previous": "Compares latest Gini score to prior measurements.",
            "points_percentage_changes": "Highlights shifts in distributional fairness.",
            "min_max_12months": "Tracks peaks or lows over time.",
            "averages": "Used to track persistent inequality trends.",
            "year_over_year": "Assesses annual shifts in economic equality.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1901_gini_coefficient.py"
        },
        "1902_poverty_rate": {
            "overview": "Represents the percentage of the population living below the poverty threshold, either nationally defined or relative to median income.",
            "why_it_matters": "Highlights economic exclusion and access challenges within society, often influencing consumption patterns, education outcomes, and healthcare usage.",
            "temporal_categorisation": "Lagging indicator",
            "investment_action_importance": "🌟 - Contextual macro signal for vulnerability or reform demand.",
            "personal_impact_importance": "🌟🌟🌟 - Impacts daily life, mobility, and access to basic needs.",
            "current_vs_previous": "Assesses improvements or setbacks in poverty alleviation.",
            "points_percentage_changes": "Highlights percentage point changes across timeframes.",
            "min_max_12months": "Shows poverty fluctuations through the cycle.",
            "averages": "Tracks long-term poverty persistence.",
            "year_over_year": "Annualised assessment of progress or decline.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1902_poverty_rate.py"
        },
        "1903_social_spending_gdp": {
            "overview": "Tracks government spending on social programs as a share of GDP, including health, welfare, education, and pensions.",
            "why_it_matters": "Reflects the fiscal commitment to equity, redistribution, and societal stability. Also influences budgetary flexibility.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Indicates fiscal posture and potential redistribution dynamics that may affect sector exposure.",
            "personal_impact_importance": "🌟🌟 - Signals state support for welfare, healthcare, and social safety nets.",
            "current_vs_previous": "Compares social spending shifts period-over-period.",
            "points_percentage_changes": "Shows realignment in fiscal priorities.",
            "min_max_12months": "Highlights high or low commitment windows.",
            "averages": "Supports longer-term welfare analysis.",
            "year_over_year": "Assesses yearly shifts in state-backed support.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/1903_social_spending_gdp.py"
            },
        }
    },
    "2000_geopolitical_risks_and_global_stability": {
        "theme_title": "Geopolitical Risks and Global Stability",
        "theme_introduction": "Geopolitical risk indicators reflect sovereign stability gradients, conflict escalation dynamics, political regime stress regimes, and systemic cross-border volatility exposure embedded within global capital flow structures.",
        "temporal_categorisation": {
            "coincident_indicators": "Reflect current levels of risk and geopolitical instability.",
            "leading_indicators": "Signal potential areas of conflict or shifts in international policy affecting markets and global supply chains.",
            "lagging_indicators": "Confirm broader economic and market effects following sustained periods of geopolitical stress."
        },
        "template": {
            "geopolitical_risk_template": "Geopolitical Risk Template – Covers military activity, political risk metrics, and sovereign credit indicators."
        },
        "data_points": [
            "Conflict Trends: Evolution of geopolitical tensions and regional conflicts.",
            "Sovereign Risk Metrics: Default spreads, credit ratings, and political risk rankings.",
            "Defense and Policy Commitments: Military spending trends and their economic footprint."
        ],
        "navigating_the_theme": "Military activity metrics, sovereign credit spreads, political risk indices, and defense expenditure trajectories structure system-level signals capturing cross-border stability alignment, geopolitical friction channels, and systemic macro-financial vulnerability gradients.",
        "conclusion_and_further_exploration": "Geopolitical risk signals serve as composite markers reflecting sovereign credit stress asymmetries, defense-capital allocation cycles, political economy fragility gradients, and volatility transmission channels across global macroeconomic systems.",
        "memberships": {
            "2001_conflict_impact_score": {
                "overview": "Quantifies the economic and market impact of geopolitical conflicts based on proximity, intensity, and persistence.",
                "why_it_matters": "Conflict can disrupt trade, increase risk premiums, and shift regional capital allocations.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟 - Important for tracking market instability drivers across sectors and regions.",
                "personal_impact_importance": "🌟 - Can affect commodity prices, regional inflation, and investor sentiment.",
                "current_vs_previous": "Shows changes in conflict exposure over time.",
                "points_percentage_changes": "Measures relative risk intensification or decline.",
                "min_max_12months": "Highlights historical stress periods for comparison.",
                "averages": "Normalises recent conflict data for trend recognition.",
                "year_over_year": "Provides context on rising or abating conflict effects.",
                "recommended_time_periods": ["6M", "12M", "3Y"],
                "path": "pages/2001_conflict_impact_score.py"
            },
            "2002_military_spending": {
                "overview": "Tracks national and global defense spending as a percentage of GDP or in absolute terms.",
                "why_it_matters": "Sustained or rising military expenditure often signals geopolitical shifts, policy redirection, or fiscal reprioritization.",
                "temporal_categorisation": "Lagging indicator",
                "investment_action_importance": "🌟 - Indicates structural policy changes or regional risk appetite.",
                "personal_impact_importance": "🌟 - Linked to government spending priorities and potential trade-offs in social investment.",
                "current_vs_previous": "Assesses fiscal adjustments in military allocations.",
                "points_percentage_changes": "Highlights ramp-ups or drawdowns.",
                "min_max_12months": "Establishes recent spending volatility.",
                "averages": "Tracks normalised expenditure trends over time.",
                "year_over_year": "Shows policy direction over longer periods.",
                "recommended_time_periods": ["1Y", "3Y", "5Y"],
                "path": "pages/2002_military_spending.py"
            },
            "2003_political_risk_indexpolitical_risk_index": {
                "overview": "Combines indicators of political stability, governance effectiveness, civil unrest, and rule of law.",
                "why_it_matters": "Political risk affects investor confidence, capital flight potential, and sovereign funding costs.",
                "temporal_categorisation": "Leading indicator",
                "investment_action_importance": "🌟🌟 - Flags early-stage risk exposure in emerging and developed markets alike.",
                "personal_impact_importance": "🌟 - Reflects institutional resilience and civic conditions.",
                "current_vs_previous": "Measures deterioration or improvement in political environment.",
                "points_percentage_changes": "Highlights trend shifts in risk rankings.",
                "min_max_12months": "Evaluates peaks in instability or improvements.",
                "averages": "Smooths volatility across cycles.",
                "year_over_year": "Compares recent data with long-term governance norms.",
                "recommended_time_periods": ["1Y", "3Y", "5Y"],
                "path": "pages/2003_political_risk_index.py"
            },
            "2004_sovereign_risk_spreads": {
                "overview": "Reflects the credit spread between sovereign bonds and benchmark rates, signaling perceived default risk.",
                "why_it_matters": "Used by markets to assess a country’s creditworthiness and risk of fiscal instability.",
                "temporal_categorisation": "Coincident indicator",
                "investment_action_importance": "🌟🌟🌟 - Highly relevant for credit, FX, and capital market positioning.",
                "personal_impact_importance": "🌟 - Linked to borrowing costs, inflation, and fiscal policy flexibility.",
                "current_vs_previous": "Evaluates spread widening or narrowing.",
                "points_percentage_changes": "Highlights risk repricing and investor sentiment shifts.",
                "min_max_12months": "Tracks pressure periods in sovereign markets.",
                "averages": "Provides context on sustained stress or improvement.",
                "year_over_year": "Confirms long-term shifts in credit risk perception.",
                "recommended_time_periods": ["3M", "6M", "12M"],
                "path": "pages/2004_sovereign_risk_spreads.py"
            },
        }
    },
    "2100_frontier_sectors": {
    "theme_title": "Frontier Sectors and Emerging Innovation",
    "theme_introduction": "Frontier sector indicators reflect long-horizon technological disruption trajectories, speculative capital allocation regimes, advanced research scaling, and transformative innovation gradients embedded in emerging productivity cycles.",
    "temporal_categorisation": {
        "coincident_indicators": "Reflect present investment flows or R&D activity in emerging sectors.",
        "leading_indicators": "Signal future growth potential and the trajectory of disruptive innovation.",
        "lagging_indicators": "Capture the maturation or scaling effects of technologies already adopted in the mainstream."
    },
    "template": {
        "frontier_sectors_template": "Frontier Sectors Template – Covers AI investment trends, biotech R&D, and venture capital activity in transformative sectors."
    },
    "data_points": [
        "Capital Allocation: Tracks where innovation-focused capital is being deployed.",
        "Sector Breakout Trends: Identifies which frontier areas are gaining traction.",
        "Technological Maturity: Considers adoption cycles and scale-readiness."
    ],
    "navigating_the_theme": "Venture capital allocation trends, sector-specific R&D intensity metrics, adoption readiness signals, and early-stage scaling indicators structure system-level signals capturing innovation breakout positioning, capital deployment asymmetries, and disruptive cycle emergence across global sectors.",
    "conclusion_and_further_exploration": "Frontier sector signals serve as composite markers reflecting speculative innovation capital flows, early adoption dynamics, transformative technology scale gradients, and long-cycle disruptive leverage potential across evolving economic architectures.",
    "memberships": {
        "2101_ai_investment_trends": {
            "overview": "Tracks investment activity into artificial intelligence across public markets, startups, and institutional funding.",
            "why_it_matters": "Signals the rise of automation and intelligence-driven disruption across industries. AI investment serves as a bellwether for digital transformation.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟 - Offers directional insight into capital interest and future competitive dynamics.",
            "personal_impact_importance": "🌟 - Suggests future shifts in employment, productivity, and consumer interfaces.",
            "current_vs_previous": "Compares current funding levels to historical norms.",
            "points_percentage_changes": "Highlights growth momentum or capital retraction.",
            "min_max_12months": "Reveals sentiment extremes in innovation appetite.",
            "averages": "Smooths volatility in quarterly or annual investment data.",
            "year_over_year": "Tracks annual growth or cooling periods.",
            "recommended_time_periods": ["6M", "12M", "3Y"],
            "path": "pages/2101_ai_investment_trends.py"
        },
        "2102_biotech_rd_growth": {
            "overview": "Measures the expansion of R&D spending in the biotechnology sector, across both public and private institutions.",
            "why_it_matters": "Reflects innovation in healthcare, gene editing, drug development, and life sciences—sectors with high barriers but transformative potential.",
            "temporal_categorisation": "Coincident indicator",
            "investment_action_importance": "🌟🌟 - Informs long-cycle strategic thinking around healthcare innovation.",
            "personal_impact_importance": "🌟🌟 - Potential future breakthroughs can reshape healthcare affordability and outcomes.",
            "current_vs_previous": "Examines quarterly shifts in biotech R&D intensity.",
            "points_percentage_changes": "Tracks magnitude of reinvestment or cutbacks.",
            "min_max_12months": "Provides high/low insight for innovation cycles.",
            "averages": "Tracks smoothed investment and focus levels.",
            "year_over_year": "Analyzes longer-term funding momentum.",
            "recommended_time_periods": ["1Y", "3Y", "5Y"],
            "path": "pages/2102_biotech_rd_growth.py"
        },
        "2103_venture_capital_activity": {
            "overview": "Captures VC activity across emerging sectors, including deal count, funding size, and thematic focus areas.",
            "why_it_matters": "Acts as a proxy for private market confidence in new technologies or business models. Often precedes public market attention.",
            "temporal_categorisation": "Leading indicator",
            "investment_action_importance": "🌟🌟🌟 - Offers early insight into disruptive sector emergence and potential IPO pipelines.",
            "personal_impact_importance": "🌟 - Reveals future employment or tech exposure areas shaping the economic landscape.",
            "current_vs_previous": "Compares current VC cycles to prior quarters or years.",
            "points_percentage_changes": "Shows momentum across deal size or theme shifts.",
            "min_max_12months": "Illustrates boom/bust patterns in early-stage capital.",
            "averages": "Smooths cyclical peaks and troughs in VC flow.",
            "year_over_year": "Assesses structural capital shifts.",
            "recommended_time_periods": ["6M", "12M", "3Y"],
            "path": "pages/2103_venture_capital_activity.py"
            },
        }
    },
}
