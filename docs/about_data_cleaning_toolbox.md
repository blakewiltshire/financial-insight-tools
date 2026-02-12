📊 Data Cleaning & Inspection Toolbox — README & Help Guide

✅ About This App

The Data Cleaning & Inspection Toolbox is designed to help users quickly and effectively clean, inspect, and prepare both securities data and economic indicator datasets before analysis.

This standalone tool allows users to:

Upload CSV files.

Automatically clean and standardise data fields.

Detect and visually highlight outliers.

Review missing values.

Manually edit data using an intuitive table editor.

Download the cleaned and manually updated data with dynamic, descriptive filenames.

This app supports integration into larger data analysis workflows or can be used independently.

🛠 Features Overview

1️⃣ Upload Data

Upload CSV files via the sidebar.

Supports both Securities data (OHLC + Volume) and Economic Indicators.

2️⃣ Select Data Type

Choose between Securities or Economic Indicators.

The app will reset (via st.rerun()) to avoid confusion when switching data types.

3️⃣ Auto Cleaning Includes:

Column renaming for consistency (Date → date, Price → close, Vol. → volume, etc.).

Date column conversion to US format.

Automatic volume parsing (e.g., converting K, M, B notations).

Sorting by date and removal of duplicates.

Basic numeric type enforcement.

4️⃣ Missing Values Summary

Option to show and review missing values across all columns.

5️⃣ Outlier Highlighting

Visual highlight of statistical outliers using IQR detection on relevant numeric fields.

Outliers flagged in yellow for easy identification.

6️⃣ Auto Cleaned Data View

Display the fully cleaned dataset.

7️⃣ Manual Editing Panel

Fully editable table with the ability to make final adjustments.

Edits are captured in the export.

8️⃣ Download Cleaned Data

Download button automatically names the file in the format:

cleaned_<original_file_name>.csv

This ensures traceability and professional output.

📂 Supported Data Columns

Securities Data

date, open, high, low, close, volume

Economic Indicators

date, value columns (flexible; only date and numeric consistency enforced)

✅ Best Practices & Recommendations

Always review missing values and correct them where applicable.

Outliers may be valid (e.g., price spikes) or data errors — cross-check with source.

Use manual editing for final refinements, especially if large or nonsensical outliers are detected.

Download the cleaned file and store versioned backups.

🚀 Deployment Notes

Fully compatible with Streamlit Cloud.

No external dependencies beyond pandas, numpy, and streamlit.

Dynamic reruns and session clearing ensure users start fresh when switching data types.

📚 Help & Future Enhancements

Tooltips to explain each field (planned).

Automated suggested corrections for common anomalies (future version).

Integration hooks for export into other Streamlit apps (optional add-on).

✅ Contact / Feedback

For issues, feedback, or suggestions, please contact the development team or raise a ticket in the associated GitHub repository.
