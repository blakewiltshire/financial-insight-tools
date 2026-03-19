# 📦 Modules Template — Thematic Grouping Blueprint Repository

This directory contains pre-built template modules for each {country} **thematic grouping** within the Economic Exploration suite.

## 📁 Folder Structure

| Folder             | Description |
|--------------------|-------------|
| `indicator_modules/` | Template mappings of indicators to evaluation functions |
| `insights/`           | Generic insight logic per thematic grouping |
| `routing/`            | Dispatcher logic for country-specific df_dict inputs |
| `scoring_weights_labels/`    | Weighting and label assignment for alignment scoring |
| `use_cases/`          | Use case selector structure and default logic |
| `visual_config/`      | Generic visualisation logic for charts |

## 🛠 Usage

- Use these templates when building a new country module.
- Copy only the files corresponding to the desired **theme ID** (e.g., `100`, `200`) into your country folder.
- Do **not** modify these templates directly. They serve as a universal foundation for customisation.

## 🚫 Important

- These files are **not loaded at runtime**.
- Universal logic (shared across countries) lives in `/apps/economic_exploration/universal_*`.
- Country-specific modules must be copied to `apps/economic_exploration/{country}/{module_type}/`.

---
© 2026 Blake Media Ltd. All rights reserved.
