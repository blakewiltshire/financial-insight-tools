from datetime import datetime, date
import numpy as np
import pandas as pd


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]

    if isinstance(obj, tuple):
        return [make_json_safe(v) for v in obj]

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.bool_):
        return bool(obj)

    if isinstance(obj, (pd.Timestamp, datetime, date)):
        return obj.isoformat()

    if obj is None:
        return None

    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass

    return obj
