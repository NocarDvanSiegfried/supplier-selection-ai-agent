import pandas as pd

from src.pipeline import find_top5_suppliers


def test_find_top5_suppliers_returns_expected_columns() -> None:
    frame = pd.DataFrame(
        {
            "supplier": ["A", "B", "C"],
            "item_name": ["труба стальная", "кабель силовой", "бумага офисная"],
            "price": [120.0, 100.0, 80.0],
            "attributes": ["20 мм", "медь", "а4"],
        }
    )

    result = find_top5_suppliers("нужна стальная труба 20 мм", frame)

    assert list(result.columns) == [
        "supplier",
        "matched_items_count",
        "avg_semantic_score",
        "min_price",
        "final_score",
        "match_explanation",
    ]
    assert len(result) <= 5
    assert result.iloc[0]["supplier"] == "A"
