import pandas as pd

from src.metrics import calculate_metrics


def test_calculate_metrics_returns_expected_keys() -> None:
    extracted = pd.DataFrame(
        {
            "supplier": ["A", "B", "UNKNOWN_SUPPLIER"],
            "item_name": ["труба", "кабель", ""],
            "price": pd.Series([100.0, None, 50.0], dtype="Float64"),
            "attributes": ["20 мм", "", ""],
        }
    )
    ranked = pd.DataFrame(
        {
            "supplier": ["A", "B"],
            "matched_items_count": [1, 1],
            "avg_semantic_score": [0.8, 0.6],
            "min_price": [100.0, 120.0],
            "final_score": [0.86, 0.65],
            "match_explanation": ["x", "y"],
        }
    )

    metrics = calculate_metrics(extracted_items=extracted, ranked_suppliers=ranked)

    assert "extraction_field_coverage" in metrics
    assert "price_parse_success_rate" in metrics
    assert "mean_semantic_score_top5" in metrics
    assert "top5_suppliers_count" in metrics
    assert "match_precision_at_5" in metrics
    assert "match_recall_at_5" in metrics
