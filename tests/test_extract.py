import pandas as pd

from src.extract import extract_supplier_items, parse_price


def test_parse_price_from_string() -> None:
    assert parse_price("1 250,50 руб.") == 1250.5


def test_parse_price_from_numeric() -> None:
    assert parse_price(99) == 99.0


def test_parse_price_for_empty_or_invalid_returns_none() -> None:
    assert parse_price("") is None
    assert parse_price(None) is None
    assert parse_price("не указано") is None


def test_extract_supplier_items_keeps_required_columns_and_fallback_supplier() -> None:
    frame = pd.DataFrame(
        {
            "supplier": ["ООО Вектор", None],
            "item_name": ["Труба 20 мм", "Кабель силовой"],
            "price": ["100,00", ""],
            "attributes": ["сталь", None],
        }
    )

    result = extract_supplier_items(frame)

    assert list(result.columns) == ["supplier", "position", "item_name", "price", "attributes"]
    assert result.loc[0, "supplier"] == "ООО Вектор"
    assert result.loc[1, "supplier"] == "UNKNOWN_SUPPLIER"
    assert result.loc[0, "position"] == "Труба 20 мм"
    assert result.loc[0, "price"] == 100.0
    assert pd.isna(result.loc[1, "price"])


def test_extract_supplier_items_supports_position_column_as_source() -> None:
    frame = pd.DataFrame(
        {
            "supplier": ["ООО Север"],
            "position": ["Труба профильная 40x20"],
            "price": ["250"],
            "attributes": ["сталь"],
        }
    )

    result = extract_supplier_items(frame)

    assert result.loc[0, "position"] == "Труба профильная 40x20"
    assert result.loc[0, "item_name"] == "Труба профильная 40x20"
