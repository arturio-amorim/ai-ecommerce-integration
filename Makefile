.PHONY: install sync search enrich test clean

install:
	pip install -e .
	pip install -r requirements.txt

sync:
	python scripts/sync.py

search:
	python scripts/search.py "$(Q)"

enrich:
	python scripts/enrich.py

test:
	pytest -q

clean:
	rm -rf .index __pycache__ src/shopai/__pycache__ .pytest_cache
