# 📚 Reference Data & Trusted Sources

This module provides access to foundational tools for inspecting, validating, and navigating core reference components within the Financial Insight Tools system.

Rather than interacting with data directly, these tools offer institutional-grade scaffolding for **data sourcing, structural alignment, and metadata validation**.

---

## 📚 Institutional Reference Directory

A curated set of non-interactive external links to global financial regulators, economic agencies, classification standards, and market data providers.

**Purpose**:
- Validate economic or financial data origins
- Locate official market filings, datasets, or licensing frameworks
- Reference global standards, codes, and legal identifiers

**Scope Includes**:
- Market data platforms (e.g., Bloomberg, Reuters)
- Regulatory bodies (SEC, FCA, ESMA)
- Financial identifiers (ISIN, LEI, CIK)
- Statistical agencies and global institutions (BEA, IMF, OECD)

All entries are outbound links — no API usage, downloads, or in-app processing.

---

## 📚 Classification Schema Viewer

An internal tool for **viewing, filtering, and interpreting global economic classification systems**, including:

- **GICS** – Global Industry Classification Standard  
- **NAICS / SIC** – North American and legacy business classifications  
- **ISIC / NACE** – UN and Eurostat economic activity frameworks  
- **ICB** – Industry Classification Benchmark (FTSE)

**Use Cases**:
- Map economic sectors to indicators or ETFs
- Support intermarket dashboards or correlation tools
- Validate classification alignment when comparing cross-country economic metrics

---

## 📚 Thematic Registry Explorer

Interactive browser for inspecting:

- Thematic groupings (`thematic_groupings.json`)
- Indicator and use case metadata (`economic_series_map.json`)
- Membership validation across system modules

**Capabilities**:
- Filter by country, theme, indicator ID, or use case
- Identify gaps, mismatches, or orphaned entries
- Export listings for documentation or module setup

Essential for onboarding new economic themes, extending country coverage, or validating system coherence during updates.

---

## Developer Notes

- This module contains no real-time indicators or trading utilities
- All subpages are navigated via the main launcher
- Markdown assets and documentation are stored in `/docs/`
