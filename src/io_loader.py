from __future__ import annotations

import pandas as pd


def load_cp_archive(path: str) -> pd.DataFrame:
    """Load CSV archive with conservative NA parsing."""
    return pd.read_csv(
        path,
        keep_default_na=True,
        na_filter=True,
        skip_blank_lines=True,
    )
