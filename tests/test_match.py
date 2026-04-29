import pandas as pd

from src.match import compute_semantic_similarity


def test_compute_semantic_similarity_prefers_relevant_item() -> None:
    frame = pd.DataFrame(
        {
            "item_name": ["стальная труба 20 мм", "офисная бумага а4"],
            "attributes": ["оцинкованная", "белая"],
        }
    )

    result = compute_semantic_similarity("труба сталь 20 мм", frame)

    assert result.loc[0, "semantic_score"] > result.loc[1, "semantic_score"]


def test_compute_semantic_similarity_for_empty_query_returns_zeroes() -> None:
    frame = pd.DataFrame({"item_name": ["труба"], "attributes": ["сталь"]})

    result = compute_semantic_similarity("", frame)

    assert result.loc[0, "semantic_score"] == 0.0
