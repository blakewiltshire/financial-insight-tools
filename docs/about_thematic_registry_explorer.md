# 📘 What is this app about?

Thematic Registry Explorer

This module allows structured inspection of all thematic groupings and economic indicator mappings within the Financial Insight Tools ecosystem. It is designed for internal governance, ensuring that all data sources, themes, and indicator references remain consistent, validated, and system-aligned.

---

### Purpose

- View all thematic groupings, their associated templates, and linked use cases
- Explore country-level and global indicators across themes
- Support structural audits of indicator metadata, template alignment, and release schedule coverage

---

### Structure

- Loads from `/constants/thematic_groupings.py` and `/constants/economic_series_map.py`
- Includes tabbed interface:
  - **Themes** — Review structure and memberships of each economic theme
  - **Indicators** — Explore indicator metadata across countries and use cases
  - **Audit** — Validate consistency, highlight orphans, mismatches, and duplicates
- Built for development, data alignment, and structural insight — not for end-user interaction or analysis

---

© 2025 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire  
No trading, investment, or policy advice provided.
