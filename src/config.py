from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractionConfig:
    unknown_supplier: str = "UNKNOWN_SUPPLIER"


@dataclass(frozen=True)
class RankingConfig:
    semantic_weight: float = 0.7
    price_weight: float = 0.3
    top_k: int = 5


EXTRACTION_CONFIG = ExtractionConfig()
RANKING_CONFIG = RankingConfig()
