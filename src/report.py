from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _build_markdown_report(metrics: dict[str, Any]) -> str:
    lines = [
        "# Extraction Report",
        "",
        "## Quality summary",
        "",
        f"- extraction_field_coverage: {metrics.get('extraction_field_coverage', 0.0)}",
        f"- price_parse_success_rate: {metrics.get('price_parse_success_rate', 0.0)}",
        f"- mean_semantic_score_top5: {metrics.get('mean_semantic_score_top5', 0.0)}",
        f"- top5_suppliers_count: {metrics.get('top5_suppliers_count', 0)}",
        f"- price_advantage_vs_median: {metrics.get('price_advantage_vs_median', 0.0)}",
        f"- match_precision_at_5: {metrics.get('match_precision_at_5', 0.0)}",
        f"- match_recall_at_5: {metrics.get('match_recall_at_5', 0.0)}",
        "",
        "## Analyst notes",
        "",
        "- Coverage shows how many required fields were parsed.",
        "- Price parse success captures robustness of price extraction.",
        "- Mean semantic score reflects relevance quality of top-5 output.",
    ]
    return "\n".join(lines) + "\n"


def generate_outputs(ranked_suppliers: pd.DataFrame, metrics: dict[str, Any], output_dir: str | Path) -> None:
    """Export ranked suppliers, metrics, and markdown report."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    ranked_suppliers.to_csv(destination / "top5_suppliers.csv", index=False)
    (destination / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (destination / "extraction_report.md").write_text(
        _build_markdown_report(metrics),
        encoding="utf-8",
    )
    _save_scores_chart(ranked_suppliers, destination / "top5_scores.png")


def _save_scores_chart(ranked_suppliers: pd.DataFrame, output_path: Path) -> None:
    plot_frame = ranked_suppliers.copy()
    if plot_frame.empty:
        plot_frame = pd.DataFrame({"supplier": ["no-data"], "final_score": [0.0]})

    figure, axis = plt.subplots(figsize=(8, 4))
    axis.bar(plot_frame["supplier"], plot_frame["final_score"])
    axis.set_title("Top suppliers by final score")
    axis.set_xlabel("Supplier")
    axis.set_ylabel("Final score")
    axis.tick_params(axis="x", rotation=30)
    figure.tight_layout()
    figure.savefig(output_path)
    plt.close(figure)
