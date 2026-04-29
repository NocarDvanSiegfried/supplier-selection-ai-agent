# supplier-selection-ai-agent

AI-пайплайн подбора поставщиков по архиву коммерческих предложений.

## Запуск

```bash
python -m pip install -r requirements.txt
python -m src.cli --input data/cp_archive_sample.csv --query "нужна стальная труба 20 мм" --out outputs
```

Через `Makefile`:

```bash
make install
make test
make run QUERY="нужна стальная труба 20 мм"
```

## Используемые технологии

- `pandas`, `numpy` - табличная обработка и численные операции.
- `scikit-learn` - TF-IDF и cosine similarity для семантического матчинга.
- `pytest` - unit-тесты бизнес-логики.

## Архитектура

- `src/io_loader.py` - загрузка CSV.
- `src/extract.py` - извлечение и типизация сущностей (supplier/item/price/attributes).
- `src/normalize.py` - нормализация текстов.
- `src/match.py` - расчет `semantic_score`.
- `src/rank.py` - агрегация по поставщику и финальный скоринг.
- `src/metrics.py` - расчет KPI качества.
- `src/report.py` - экспорт `top5_suppliers.csv`, `metrics.json`, `extraction_report.md`.
- `src/pipeline.py` - orchestration (`find_top5_suppliers`, `run_pipeline`).
- `src/cli.py` - CLI-интерфейс.

## Компромиссы

- Для MVP использован TF-IDF baseline вместо эмбеддинговых моделей: быстрее и проще в офлайн запуске.
- Метрики extraction/matching реализованы proxy-уровня без внешнего эталонного датасета.
- Ранжирование использует фиксированные веса (`semantic=0.7`, `price=0.3`) из конфига.

## Проверка работы

```bash
python -m pytest tests
```

Ожидаемые артефакты после запуска CLI:

- `outputs/top5_suppliers.csv`
- `outputs/metrics.json`
- `outputs/extraction_report.md`
- `outputs/top5_scores.png`

В `metrics.json` дополнительно считаются метрики сопоставления:
- `match_precision_at_5`
- `match_recall_at_5`

## Пример вызова функции

```python
import pandas as pd
from src.pipeline import find_top5_suppliers

frame = pd.read_csv("data/cp_archive_sample.csv")
top5 = find_top5_suppliers("нужна стальная труба 20 мм", frame)
print(top5)
```

CLI пример:

```bash
python -m src.cli --input data/cp_archive_sample.csv --query "нужна стальная труба 20 мм" --out outputs
```

## Скриншот графика

После запуска пайплайна график сохраняется в `outputs/top5_scores.png`.

## Мотивация участия

1) Проект интересен тем, что сочетает NLP и прикладную закупочную аналитику с измеримым бизнес-эффектом.  
2) Моя роль в команде: разработка ядра data-пайплайна, метрик качества и reproducible ML/analytics workflow.  
3) Готов уделять 15-20 часов в неделю в течение 2-3 месяцев на запуск production-ready MVP.


# Мотивационное письмо

Почему мне интересен проект
Мне интересен этот проект, потому что в нём данные решают бизнес-задачу: помогают быстрее выбрать поставщика и не тратить время на ручной просмотр старых КП. Мне нравится, что такой проект можно быстро довести до полезного рабочего прототипа.

Моя роль в команде
Я вижу себя в роли человека, который отвечает за обработку данных и логику подбора. Также мне интересно участвовать в продуктовой части: какие метрики показывать пользователю и как объяснять выбор поставщика ”.

Сколько времени готов уделять
Готов уделять проекту около 40 часов в неделю в течение ближайших 3–6 месяцев. На активных этапах разработки могу выделять больше времени.