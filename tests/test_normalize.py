import math

from src.normalize import normalize_text


def test_normalize_text_maps_units_and_noise() -> None:
    source = "  Труба 20 миллиметр!!!  "

    result = normalize_text(source)

    assert result == "труба 20 мм"


def test_normalize_text_supports_mm_alias() -> None:
    source = "Кабель 10 mm"

    result = normalize_text(source)

    assert result == "кабель 10 мм"


def test_normalize_text_handles_none_and_nan() -> None:
    assert normalize_text(None) == ""
    assert normalize_text(float("nan")) == ""
    assert normalize_text(math.nan) == ""
