# -------------------------------------------------------------------------------------------------
# 🧹 Snapshot Cleanup Utility — Validate and Remove Corrupted AI Exports
# -------------------------------------------------------------------------------------------------

import os
import json
from typing import List, Tuple

SNAPSHOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage", "ai_bundles"))


def find_invalid_snapshots() -> List[str]:
    """
    Recursively scan the ai_bundles folder for invalid or corrupted JSON snapshot files.

    A valid file must:
    - Load without JSONDecodeError
    - Contain both 'theme' and 'use_case' fields as strings

    Returns a list of relative paths to invalid files.
    """
    invalid_files = []

    for root, _, files in os.walk(SNAPSHOT_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                if not isinstance(content.get("theme"), str) or not isinstance(content.get("use_case"), str):
                    invalid_files.append(file_path)
            except (json.JSONDecodeError, UnicodeDecodeError):
                invalid_files.append(file_path)

    return sorted(invalid_files)


def delete_files(file_list: List[str]) -> Tuple[int, List[str]]:
    """
    Permanently deletes the given files from disk.
    Returns count and list of deleted file paths.
    """
    deleted = []
    for path in file_list:
        try:
            os.remove(path)
            deleted.append(path)
        except Exception:
            continue
    return len(deleted), deleted
