# -------------------------------------------------------------------------------------------------
# 🧹 Observation Log Cleanup Utility — Validate and Remove Corrupted CSVs
# -------------------------------------------------------------------------------------------------

import os
import pandas as pd
from typing import List, Tuple

OBSERVATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "user_observations"))

REQUIRED_COLUMNS = {"timestamp", "observation_text", "tags"}


def find_invalid_observation_files() -> List[str]:
    """
    Recursively find corrupted or invalid observation CSV files.
    A valid file must:
    - Be a readable CSV
    - Contain at least 'timestamp', 'observation_text', 'tags' columns

    Returns:
        List of invalid file paths.
    """
    invalid_files = []

    for root, _, files in os.walk(OBSERVATION_PATH):
        for file in files:
            if not file.endswith(".csv"):
                continue
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                if not REQUIRED_COLUMNS.issubset(df.columns):
                    invalid_files.append(file_path)
            except Exception:
                invalid_files.append(file_path)

    return sorted(invalid_files)


def delete_observation_files(file_list: List[str]) -> Tuple[int, List[str]]:
    """
    Deletes the specified observation log files.

    Returns:
        Tuple of (count deleted, list of deleted paths)
    """
    deleted = []
    for path in file_list:
        try:
            os.remove(path)
            deleted.append(path)
        except Exception:
            continue
    return len(deleted), deleted
