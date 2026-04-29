from __future__ import annotations

import pandas as pd

from src.config import RANKING_CONFIG


def _compute_price_score(prices: pd.Series) -> pd.Series:
    numeric_prices = prices.astype(float)
    min_price = float(numeric_prices.min())
    max_price = float(numeric_prices.max())
    if max_price == min_price:
        return pd.Series(1.0, index=prices.index, dtype="float64")
    return (max_price - numeric_prices) / (max_price - min_price)


def rank_suppliers(scored_items: pd.DataFrame) -> pd.DataFrame:
    """Aggregate scored items by supplier and return ranked top-k."""
    if scored_items.empty:
        return pd.DataFrame(
            columns=[
                "supplier",
                "matched_items_count",
                "avg_semantic_score",
                "min_price",
                "final_score",
                "match_explanation",
            ]
        )

    aggregation = (
        scored_items.groupby("supplier", as_index=False)
        .agg(
            matched_items_count=("item_name", "count"),
            avg_semantic_score=("semantic_score", "mean"),
            min_price=("price", "min"),
        )
        .reset_index(drop=True)
    )

    aggregation["price_score"] = _compute_price_score(aggregation["min_price"])
    aggregation["final_score"] = (
        aggregation["avg_semantic_score"] * RANKING_CONFIG.semantic_weight
        + aggregation["price_score"] * RANKING_CONFIG.price_weight
    )
    aggregation["match_explanation"] = (
        "semantic="
        + aggregation["avg_semantic_score"].round(3).astype(str)
        + "; min_price="
        + aggregation["min_price"].round(2).astype(str)
    )

    ranked = aggregation.sort_values(
        by=["final_score", "avg_semantic_score", "min_price"],
        ascending=[False, False, True],
    )

    return ranked.head(RANKING_CONFIG.top_k)[
        [
            "supplier",
            "matched_items_count",
            "avg_semantic_score",
            "min_price",
            "final_score",
            "match_explanation",
        ]
    ].reset_index(drop=True)
