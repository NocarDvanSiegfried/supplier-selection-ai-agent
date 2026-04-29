import json

import pandas as pd

from src.cli import main


def test_cli_main_generates_artifacts(tmp_path) -> None:
    input_path = tmp_path / "cp_archive_sample.csv"
    source = pd.DataFrame(
        {
            "supplier": ["A", "B", "C"],
            "item_name": ["стальная труба 20 мм", "медный кабель", "бумага офисная"],
            "price": [120.0, 80.0, 50.0],
            "attributes": ["оцинкованная", "силовой", "а4"],
        }
    )
    source.to_csv(input_path, index=False)

    output_dir = tmp_path / "outputs"
    exit_code = main(
        [
            "--input",
            str(input_path),
            "--query",
            "нужна стальная труба",
            "--out",
            str(output_dir),
        ]
    )

    assert exit_code == 0
    assert (output_dir / "top5_suppliers.csv").exists()
    assert (output_dir / "metrics.json").exists()
    assert (output_dir / "extraction_report.md").exists()

    metrics = json.loads((output_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["top5_suppliers_count"] >= 1
