# ℹ️ Help: Thematic Registry Explorer

This module enables structured querying and validation of key internal registries that govern the Financial Insight Tools ecosystem. It operates across two core files:

---

### 📁 What This App Queries

#### 1. `thematic_groupings.py`
Defines the architecture of all economic themes used across the system.

Each thematic grouping includes:
- A unique identifier (e.g., `100_economic_growth_stability`)
- Templates and data points relevant to that theme
- Categorisation of indicators (leading, coincident, lagging)
- A membership map linking use cases (e.g., "Real GDP") to unique indicator IDs

#### 2. `economic_series_map.py`
Maps all economic indicators to:
- Country of origin (e.g., United States, United Kingdom)
- Theme and template (e.g., `gdp_template`)
- Source and frequency (e.g., FRED, ONS, Quarterly)
- Display names, units, URLs, release schedules, and unique IDs

---

### 🧭 Why This Matters

This tool exists to:
- Surface the **structure** behind every economic module in the system
- Help verify what indicators are used, by which countries, and under which themes
- Allow developers, analysts, or tool designers to align datasets and workflows
- Audit release timing, metadata consistency, and structural integrity across components

It does **not**:
- Provide real-time data
- Perform any economic analysis or interpretation
- Offer financial advice or recommend policy positions

---

### 🛠 What You Can Do

Examples of supported queries:
- See which indicators are included under a thematic grouping (e.g., labour market dynamics)
- Filter by country to review available indicators and metadata (e.g., UK GDP vs US GDP)
- Check release schedules, units, or seasonal adjustments for operational planning
- Validate whether a given indicator ID appears in the right theme or template
- Prepare onboarding of new countries or modules by checking for missing mappings

---

### 🔐 Governance and Scope

This module is internal-facing — used to ensure the system operates on a consistent, validated base. It supports development, integration, and refinement of macroeconomic workflows across:

- 🌍 Economic Exploration
- 🔗 Intermarket & Correlation
- 🧠 Observation & AI Export

---

© 2025 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire  
No trading, investment, or policy advice provided.
