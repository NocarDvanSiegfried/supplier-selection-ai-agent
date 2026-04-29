import json

import pandas as pd

from src.report import generate_outputs


def test_generate_outputs_creates_expected_files(tmp_path) -> None:
    ranked = pd.DataFrame(
        {
            "supplier": ["A"],
            "matched_items_count": [1],
            "avg_semantic_score": [0.8],
            "min_price": [100.0],
            "final_score": [0.9],
            "match_explanation": ["semantic=0.8; min_price=100"],
        }
    )
    metrics = {
        "extraction_field_coverage": 0.75,
        "price_parse_success_rate": 1.0,
        "mean_semantic_score_top5": 0.8,
        "top5_suppliers_count": 1,
        "match_precision_at_5": 1.0,
        "match_recall_at_5": 1.0,
    }

    generate_outputs(ranked_suppliers=ranked, metrics=metrics, output_dir=tmp_path)

    assert (tmp_path / "top5_suppliers.csv").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "extraction_report.md").exists()
    assert (tmp_path / "top5_scores.png").exists()

    saved_metrics = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert saved_metrics["top5_suppliers_count"] == 1
