from __future__ import annotations

from typing import Any

import pandas as pd


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def calculate_metrics(
    extracted_items: pd.DataFrame,
    ranked_suppliers: pd.DataFrame,
    scored_items: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Calculate extraction and ranking quality metrics."""
    total_rows = float(len(extracted_items))
    if total_rows == 0:
        return {
            "extraction_field_coverage": 0.0,
            "price_parse_success_rate": 0.0,
            "mean_semantic_score_top5": 0.0,
            "top5_suppliers_count": 0,
            "price_advantage_vs_median": 0.0,
            "match_precision_at_5": 0.0,
            "match_recall_at_5": 0.0,
        }

    required_columns = ["supplier", "item_name", "price"]
    non_empty_count = 0
    for column in required_columns:
        if column == "price":
            non_empty_count += float(extracted_items[column].notna().sum())
        else:
            non_empty_count += float(extracted_items[column].astype("string").str.strip().ne("").sum())
    extraction_field_coverage = _safe_ratio(non_empty_count, total_rows * len(required_columns))

    parsed_price_rows = float(extracted_items["price"].notna().sum())
    price_parse_success_rate = _safe_ratio(parsed_price_rows, total_rows)

    if ranked_suppliers.empty:
        mean_semantic_score_top5 = 0.0
        top5_suppliers_count = 0
        price_advantage_vs_median = 0.0
        match_precision_at_5 = 0.0
        match_recall_at_5 = 0.0
    else:
        mean_semantic_score_top5 = float(ranked_suppliers["avg_semantic_score"].mean())
        top5_suppliers_count = int(len(ranked_suppliers))
        top_min_price = float(ranked_suppliers["min_price"].min())
        valid_source_prices = extracted_items["price"].dropna()
        if valid_source_prices.empty:
            price_advantage_vs_median = 0.0
        else:
            source_median = float(valid_source_prices.median())
            price_advantage_vs_median = _safe_ratio(source_median - top_min_price, source_median)
        match_precision_at_5, match_recall_at_5 = _calculate_match_proxy_metrics(
            ranked_suppliers=ranked_suppliers,
            scored_items=scored_items,
        )

    return {
        "extraction_field_coverage": round(extraction_field_coverage, 4),
        "price_parse_success_rate": round(price_parse_success_rate, 4),
        "mean_semantic_score_top5": round(mean_semantic_score_top5, 4),
        "top5_suppliers_count": top5_suppliers_count,
        "price_advantage_vs_median": round(price_advantage_vs_median, 4),
        "match_precision_at_5": round(match_precision_at_5, 4),
        "match_recall_at_5": round(match_recall_at_5, 4),
    }


def _calculate_match_proxy_metrics(ranked_suppliers: pd.DataFrame, scored_items: pd.DataFrame | None) -> tuple[float, float]:
    if scored_items is None or scored_items.empty:
        return 0.0, 0.0

    relevant_threshold = 0.3
    relevant_mask = scored_items["semantic_score"] >= relevant_threshold
    retrieved_mask = scored_items["supplier"].isin(ranked_suppliers["supplier"])
    true_positive_mask = relevant_mask & retrieved_mask

    retrieved_count = float(retrieved_mask.sum())
    relevant_count = float(relevant_mask.sum())
    true_positive_count = float(true_positive_mask.sum())

    precision = _safe_ratio(true_positive_count, retrieved_count)
    recall = _safe_ratio(true_positive_count, relevant_count)
    return precision, recall
