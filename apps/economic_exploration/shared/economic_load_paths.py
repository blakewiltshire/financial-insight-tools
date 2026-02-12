"""
System path loader for thematic country modules.

Ensures all shared and universal components are accessible,
without polluting sys.path with unnecessary local paths.
"""

import os
import sys


def load_project_paths(current_file: str) -> dict:
    """
    Resolves standard project path levels based on current file location.

    Args:
        current_file (str): Typically __file__ from the caller module.

    Returns:
        dict: Dictionary with named path levels.
    """
    level_up_1 = os.path.abspath(os.path.join(current_file, ".."))
    level_up_2 = os.path.abspath(os.path.join(current_file, "..", ".."))
    level_up_3 = os.path.abspath(os.path.join(current_file, "..", "..", ".."))
    level_up_4 = os.path.abspath(os.path.join(current_file, "..", "..", "..", ".."))

    return {
        "level_up_1": level_up_1,
        "level_up_2": level_up_2,
        "level_up_3": level_up_3,
        "level_up_4": level_up_4,
    }


def append_standard_paths(paths: dict) -> None:
    """
    Appends shared and universal paths to sys.path using resolved project levels.

    Args:
        paths (dict): Output from load_project_paths
    """
    app_path = paths["level_up_2"]
    apps_path = paths["level_up_3"]
    root_path = paths["level_up_4"]

    include_paths = [
        os.path.join(apps_path, "constants"),
        os.path.join(apps_path, "macro_tools"),
        os.path.join(app_path, "shared"),
        os.path.join(app_path, "universal_insight_generator"),
        os.path.join(app_path, "universal_thematic_membership"),
        os.path.join(app_path, "universal_use_cases"),
        os.path.join(app_path, "universal_visuals"),
        os.path.join(app_path, "universal_weightings"),
    ]

    for path in include_paths:
        if path not in sys.path:
            sys.path.append(path)
