from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.normalize import normalize_text


def _compose_item_text(row: pd.Series) -> str:
    item_name = normalize_text(row.get("item_name", ""))
    attributes = normalize_text(row.get("attributes", ""))
    return f"{item_name} {attributes}".strip()


def compute_semantic_similarity(request_text: str, items_frame: pd.DataFrame) -> pd.DataFrame:
    """Attach semantic similarity scores to each catalog row."""
    scored = items_frame.copy()
    query = normalize_text(request_text)

    if scored.empty:
        scored["semantic_score"] = pd.Series(dtype="float64")
        return scored

    if not query:
        scored["semantic_score"] = 0.0
        return scored

    documents = scored.apply(_compose_item_text, axis=1).tolist()
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    similarity_values = cosine_similarity(query_vector, tfidf_matrix).flatten()
    scored["semantic_score"] = similarity_values.astype(float)
    return scored
