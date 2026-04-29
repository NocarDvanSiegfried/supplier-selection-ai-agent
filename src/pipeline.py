from __future__ import annotations

import pandas as pd

from src.extract import extract_supplier_items
from src.match import compute_semantic_similarity
from src.metrics import calculate_metrics
from src.rank import rank_suppliers


def find_top5_suppliers(request_text: str, cp_database: pd.DataFrame) -> pd.DataFrame:
    """Find top-5 suppliers by semantic relevance and price competitiveness."""
    extracted_items = extract_supplier_items(cp_database)
    scored_items = compute_semantic_similarity(request_text=request_text, items_frame=extracted_items)
    ranked_suppliers = rank_suppliers(scored_items)
    return ranked_suppliers


def run_pipeline(request_text: str, cp_database: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float | int]]:
    """Run extraction, matching, ranking and return metrics."""
    extracted_items = extract_supplier_items(cp_database)
    scored_items = compute_semantic_similarity(request_text=request_text, items_frame=extracted_items)
    ranked_suppliers = rank_suppliers(scored_items)
    metrics = calculate_metrics(
        extracted_items=extracted_items,
        ranked_suppliers=ranked_suppliers,
        scored_items=scored_items,
    )
    return ranked_suppliers, metrics
