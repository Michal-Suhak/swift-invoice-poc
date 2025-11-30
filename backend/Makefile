install:
	uv pip install --system -e .

install-dev:
	uv pip install --system -e ".[dev]"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest -v --cov=app --cov-report=html --cov-report=term

lint:
	ruff check app tests
	mypy app

format:
	black app tests
	ruff check --fix app tests

check: lint test

supercode: format lint

db-up:
	cd .. && docker-compose up -d postgres
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3

db-down:
	cd .. && docker-compose down

db-migrate:
	alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-revision:
	alembic revision -m "$(msg)"

docker-build:
	cd .. && docker-compose build
docker-up:
	cd .. && docker-compose up -d

docker-down:
	cd .. && docker-compose down

docker-restart:
	cd .. && docker-compose restart backend
