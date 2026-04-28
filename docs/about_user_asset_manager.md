## User Asset Manager

The **User Asset Manager** serves as a structured reference lens for managing user-defined assets across the Financial Insight Tools system.

It does not provide an upload interface — instead, it guides how to organise custom datasets within the _user asset folders located in the /data_sources/financial_data directory. Once correctly placed, these assets are automatically recognised and made available across all compatible tools.

### Key Functions

- **Directory Reference Viewer:** View available _user asset folders and understand their purpose
- **Category Guidance:** Access descriptions, examples, and formatting expectations for each folder type
- **Cross-Tool Compatibility:** Assets stored in valid folders are automatically integrated into scanners, structuring tools, and calculators
- **Preprocessing Expectations:** Files should be cleaned and structured consistently before placement

### File Handling, Currency Normalisation & Date Format

All files must be manually placed in the relevant `_user` folders — this app does not support drag-and-drop uploads.

Before using custom assets, ensure:

- files are saved in CSV format
- required columns are present
- dates use the standard international format: `YYYY-MM-DD`
- assets used together are aligned to the same currency
- unnecessary non-numeric columns are removed unless required by the module

Regional date formats such as `DD/MM/YYYY` or `MM/DD/YYYY` should not be used. They can be parsed incorrectly and may cause charts, overlays, joins, and calculations to render incorrectly.

Use the Historical Data Currency Converter module if currency alignment is required.

---

### ⚠️ No investment advice or recommendations are provided

This module supports structured planning and diagnostic exploration. Interpretive judgement, scenario assumptions, and execution decisions remain the responsibility of the end user. No trading signals or investment recommendations are produced by this system.
