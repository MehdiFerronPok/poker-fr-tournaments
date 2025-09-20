PYTHON=python3
POETRY=poetry

.PHONY: help init install test lint format ingest normalize api web

help:
	@echo "Useful targets:"
	@echo "  init      – install Python and Node dependencies via Poetry & npm"
	@echo "  test      – run unit tests for Python and frontend"
	@echo "  lint      – run linters (ruff, black, mypy, eslint, prettier)"
	@echo "  format    – format code (black, prettier)"
	@echo "  ingest    – run all ingestion connectors"
	@echo "  normalize – normalize ingested events"
	@echo "  api       – start the API locally"
	@echo "  web       – start the frontend locally"

init:
	$(POETRY) install --no-root
	cd web && npm install

test:
	$(POETRY) run pytest -q
	cd web && npm run test

lint:
	$(POETRY) run ruff .
	$(POETRY) run black --check .
	$(POETRY) run mypy api ingestion normalize
	cd web && npm run lint

format:
	$(POETRY) run black .
	cd web && npm run format

ingest:
	$(POETRY) run python ingestion/run_all.py

normalize:
	$(POETRY) run python normalize/normalizer.py

api:
	$(POETRY) run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd web && npm run dev
