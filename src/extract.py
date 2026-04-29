from __future__ import annotations

import re
from typing import Any

import pandas as pd

from src.config import EXTRACTION_CONFIG
from src.schemas import OPTIONAL_CP_COLUMNS, validate_cp_dataframe_schema

_INVALID_PRICE_MARKERS = {"", "none", "null", "nan", "не указано", "-", "n/a"}
_NUMERIC_PATTERN = re.compile(r"[^\d,.\-]")


def parse_price(raw_value: Any) -> float | None:
    """Parse arbitrary price values into float."""
    if raw_value is None:
        return None

    if isinstance(raw_value, (int, float)) and not pd.isna(raw_value):
        return float(raw_value)

    normalized = str(raw_value).strip().lower()
    if normalized in _INVALID_PRICE_MARKERS:
        return None

    cleaned = _NUMERIC_PATTERN.sub("", normalized).replace(" ", "")
    if not cleaned:
        return None

    has_comma = "," in cleaned
    has_dot = "." in cleaned

    if has_comma and has_dot:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif has_comma:
        cleaned = cleaned.replace(",", ".")

    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_supplier_items(raw_frame: pd.DataFrame) -> pd.DataFrame:
    """Extract typed supplier items table from raw commercial proposals."""
    schema_check = validate_cp_dataframe_schema(raw_frame)
    if not schema_check.is_valid:
        missing = ", ".join(schema_check.missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    if "item_name" in raw_frame.columns:
        position_source = raw_frame["item_name"]
    else:
        position_source = raw_frame["position"]

    extracted = pd.DataFrame(
        {
            "supplier": raw_frame["supplier"],
            "position": position_source,
            "item_name": position_source,
            "price": raw_frame["price"],
            "attributes": raw_frame["attributes"] if "attributes" in raw_frame.columns else "",
        }
    ).reindex(columns=["supplier", "position", "item_name", "price", *OPTIONAL_CP_COLUMNS])

    extracted["supplier"] = (
        extracted["supplier"].astype("string").fillna("").str.strip().replace("", EXTRACTION_CONFIG.unknown_supplier)
    )
    extracted["item_name"] = extracted["item_name"].astype("string").fillna("").str.strip()
    extracted["position"] = extracted["position"].astype("string").fillna("").str.strip()
    extracted["attributes"] = extracted["attributes"].astype("string").fillna("").str.strip()
    extracted["price"] = extracted["price"].map(parse_price).astype("Float64")

    return extracted
