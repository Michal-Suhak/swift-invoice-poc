# Invoice Service Backend (FastAPI)

FastAPI backend for the Invoice Service application with PostgreSQL database, async SQLAlchemy 2.0, and Alembic migrations.

## Overview
- **FastAPI** for high-performance async API
- **SQLAlchemy 2.0** with async support for database operations
- **Alembic** for database migrations
- **PostgreSQL** for data persistence
- **Pydantic v2** for request/response validation
- **UV** for fast Python package management

## Prerequisites

For the recommended Docker setup (see main README.md):
- Docker Desktop or Docker Engine + Docker Compose
- That's it! Everything else runs in containers.

For local development without Docker:
- Python 3.11 or higher
- PostgreSQL 16+
- UV package manager (recommended) or pip

## Quick Start (Recommended: Docker)

The easiest way to run the backend is with Docker Compose from the project root:

```bash
# From project root directory
docker compose up -d

# Backend will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

**Or using Makefile (from backend directory):**
```bash
cd backend
make docker-up  # Starts all services (postgres, backend, frontend)
```

See the main `README.md` in the project root for complete Docker setup instructions.

## Using Makefile Commands

The backend includes a Makefile with convenient shortcuts for common tasks. Run all commands from the `backend/` directory:

### Docker Operations
```bash
make docker-up       # Start all services (postgres, backend, frontend)
make docker-down     # Stop all services
make docker-restart  # Restart backend service only
make docker-build    # Build Docker images
```

### Database Operations
```bash
make db-up           # Start PostgreSQL only
make db-down         # Stop all services
make db-upgrade      # Run database migrations
make db-migrate msg="description"  # Create new migration
make db-downgrade    # Rollback last migration
make db-revision msg="description" # Create empty migration
```

### Local Development (Without Docker)
```bash
make install         # Install dependencies
make install-dev     # Install development dependencies
make run             # Run backend server locally
```

### Testing
```bash
make test            # Run all tests
make test-cov        # Run tests with coverage report
```

### Code Quality
```bash
make lint            # Run linters (ruff + mypy)
make format          # Format code (black + ruff --fix)
make check           # Run lint + test
make supercode       # Format then lint
```

**View all commands:**
```bash
make  # or cat Makefile
```

## Testing

The backend includes a comprehensive test suite using pytest.

### Run Tests

**Using Docker:**
```bash
# From project root
docker compose exec backend pytest

# With coverage report
docker compose exec backend pytest --cov=app --cov-report=html

# View coverage report
open backend/htmlcov/index.html
```

**Using Makefile:**
```bash
cd backend
make test        # Run all tests
make test-cov    # Run with coverage report
```
## Database Migrations

This project uses Alembic for database schema migrations.

### Create a New Migration

**Using Docker:**
```bash
# Auto-generate migration from model changes
docker compose exec backend alembic revision --autogenerate -m "description of changes"
```

**Using Makefile:**
```bash
cd backend
make db-migrate msg="description of changes"
```

**Local (without Docker):**
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

**Using Docker:**
```bash
docker compose exec backend alembic upgrade head
```

**Using Makefile:**
```bash
cd backend
make db-upgrade
```

**Local:**
```bash
cd backend
alembic upgrade head
```

### Rollback Migration

**Using Docker:**
```bash
docker compose exec backend alembic downgrade -1
```

**Using Makefile:**
```bash
cd backend
make db-downgrade
```

## Code Quality

### Linting

**Using Docker:**
```bash
docker compose exec backend ruff check app tests
docker compose exec backend mypy app
```

**Using Makefile:**
```bash
cd backend
make lint  # Runs ruff + mypy
```

### Formatting

**Using Docker:**
```bash
# Check formatting
docker compose exec backend black --check app tests

# Auto-format
docker compose exec backend black app tests
docker compose exec backend ruff check --fix app tests
```

**Using Makefile:**
```bash
cd backend
make format  # Auto-format with black + ruff --fix
```

### Run All Quality Checks

**Using Docker:**
```bash
docker compose exec backend sh -c "ruff check app tests && black --check app tests && mypy app && pytest"
```

**Using Makefile:**
```bash
cd backend
make check      # Run lint + test
make supercode  # Format then lint
```

## Configuration

The backend is configured via environment variables (in `../.env`):

### Database Configuration
- `POSTGRES_USER` - Database username (default: invoice_user)
- `POSTGRES_PASSWORD` - Database password (default: invoice_password)
- `POSTGRES_DB` - Database name (default: invoice_db)
- `POSTGRES_HOST` - Database host (default: localhost, use "postgres" in Docker)
- `POSTGRES_PORT` - Database port (default: 5432 inside Docker, 5433 on host)

### Application Configuration
- `DEBUG` - Debug mode (default: False)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

### CORS Configuration
CORS origins are configured in `app/config.py`:
- Allows localhost:8080 (frontend)
- Add more origins as needed

### Database Session Management

The application uses FastAPI's dependency injection for database sessions:

```python
from app.db.session import get_db

@router.get("/")
async def get_invoices(db: AsyncSession = Depends(get_db)):
    # db session is automatically managed (commit/rollback/close)
    ...
```
