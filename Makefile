.PHONY: install test run

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest tests

run:
	python -m src.cli --input data/cp_archive_sample.csv --query "$(QUERY)" --out outputs
