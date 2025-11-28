install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

lint:
	uv run ruff check app tests
	uv run mypy app

format:
	uv run black app tests
	uv run ruff check --fix app tests

check: lint test

supercode: format lint

db-up:
	cd .. && docker-compose up -d postgres
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3

db-migrate:
	uv run alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	uv run alembic upgrade head

db-downgrade:
	uv run alembic downgrade -1

db-revision:
	uv run alembic revision -m "$(msg)"
