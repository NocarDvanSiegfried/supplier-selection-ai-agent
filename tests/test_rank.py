import pandas as pd

from src.rank import rank_suppliers


def test_rank_suppliers_returns_top_5_and_tie_breaks_by_price() -> None:
    frame = pd.DataFrame(
        {
            "supplier": ["A", "B", "C", "D", "E"],
            "item_name": ["x"] * 5,
            "attributes": [""] * 5,
            "price": [100, 90, 300, 350, 400],
            "semantic_score": [0.9, 0.9, 0.3, 0.2, 0.1],
        }
    )

    result = rank_suppliers(frame)

    assert len(result) == 5
    ranked_suppliers = result["supplier"].tolist()
    assert ranked_suppliers.index("B") < ranked_suppliers.index("A")
