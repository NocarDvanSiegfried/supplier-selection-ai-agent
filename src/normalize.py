from __future__ import annotations

import math
import re
from typing import Any

_PUNCTUATION_PATTERN = re.compile(r"[^\w\s]", flags=re.UNICODE)
_MULTISPACE_PATTERN = re.compile(r"\s+")
_UNIT_ALIASES: dict[str, str] = {
    "миллиметр": "мм",
    "миллиметров": "мм",
    "millimeter": "мм",
    "mm": "мм",
}


def _is_nan(value: Any) -> bool:
    if isinstance(value, float):
        return math.isnan(value)
    return False


def normalize_text(value: Any) -> str:
    """Normalize raw text for deterministic matching."""
    if value is None or _is_nan(value):
        return ""

    normalized = str(value).strip().lower()
    normalized = _PUNCTUATION_PATTERN.sub(" ", normalized)
    normalized = _MULTISPACE_PATTERN.sub(" ", normalized).strip()

    if not normalized:
        return ""

    tokens = normalized.split(" ")
    replaced = [_UNIT_ALIASES.get(token, token) for token in tokens]
    return " ".join(replaced)
