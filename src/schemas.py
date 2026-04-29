from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import pandas as pd

REQUIRED_BASE_COLUMNS: Final[tuple[str, ...]] = ("supplier", "price")
POSITION_ALIASES: Final[tuple[str, ...]] = ("item_name", "position")
OPTIONAL_CP_COLUMNS: Final[tuple[str, ...]] = ("attributes",)
CP_TABLE_COLUMNS: Final[tuple[str, ...]] = ("supplier", "position", "item_name", "price", "attributes")


@dataclass(frozen=True)
class SchemaValidationResult:
    is_valid: bool
    missing_columns: tuple[str, ...]


def validate_cp_dataframe_schema(frame: pd.DataFrame) -> SchemaValidationResult:
    missing_base = [column for column in REQUIRED_BASE_COLUMNS if column not in frame.columns]
    has_position_alias = any(column in frame.columns for column in POSITION_ALIASES)
    missing = tuple(missing_base + ([] if has_position_alias else ["item_name|position"]))
    return SchemaValidationResult(is_valid=len(missing) == 0, missing_columns=missing)


def build_empty_cp_dataframe() -> pd.DataFrame:
    return pd.DataFrame(columns=CP_TABLE_COLUMNS)
