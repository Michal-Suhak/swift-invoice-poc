# Swift Invoice POC

A modern full-stack invoice management system built with React, FastAPI, and PostgreSQL.

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite (build tool)
- shadcn/ui components
- TailwindCSS
- React Router
- TanStack Query (React Query)

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 (async)
- Alembic (database migrations)
- Pydantic v2 (validation)
- PostgreSQL (database)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (production)
- UV (Python package manager)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd swift-invoice-poc
```

### 2. Configure Environment Variables

Set up the environment variables in the `.env` file. Default values are listed in the env.example

```bash
# .env file (already configured with defaults)
POSTGRES_USER=invoice_user
POSTGRES_PASSWORD=invoice_password
POSTGRES_DB=invoice_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

DEBUG=False
HOST=0.0.0.0
PORT=8000

VITE_API_URL=http://localhost:8000
```

### 3. Start the Application

```bash
docker compose up -d
```

This command will:
- Pull required Docker images (first time only)
- Build the frontend and backend containers
- Start PostgreSQL, backend, and frontend services
- Run database migrations automatically
- Start all services in detached mode

### 4. Verify the Setup

Wait 10-15 seconds for services to initialize, then verify:

```bash
# Check all containers are running
docker compose ps

# Should show:
# - swift-invoice-postgres (healthy)
# - swift-invoice-backend  (running)
# - swift-invoice-frontend (running)
```

Test the backend health:
```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status":"ok"}
```

### 5. Access the Application

- **Frontend:** http://localhost:8080
- **Backend API Docs:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

### Stop the Application

```bash
docker compose down
```

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart backend
```

### Access the Database

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U invoice_user -d invoice_db

# Example queries:
# \dt                    -- List tables
# SELECT * FROM invoices; -- View invoices
# \q                     -- Quit
```

### Run Database Migrations

Migrations run automatically on container startup. To run manually:

```bash
docker compose exec backend alembic upgrade head
```

To create a new migration:

```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

## Testing

### Backend Tests

The backend includes a comprehensive test suite with pytest.

```bash
# Run all tests
docker compose exec backend pytest

# Run with coverage report
docker compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker compose exec backend pytest tests/test_invoices.py

# View coverage report (after running with --cov-report=html)
open backend/htmlcov/index.html
```

### Frontend Tests

```bash
# Run frontend tests (if implemented)
docker compose exec frontend npm test
```

## Production Deployment

For production deployment instructions, see:
- **AWS Deployment:** `docs/AWS_DEPLOYMENT.md`
- **Docker Production:** Use `Dockerfile` (not `Dockerfile.dev`)
- **Environment:** Set `DEBUG=False` and use strong passwords

## Code Quality

The project uses:
- **Backend:** Black, Ruff, MyPy
- **Frontend:** ESLint, TypeScript

```bash
# Backend linting
docker compose exec backend ruff check app tests
docker compose exec backend black --check app tests
docker compose exec backend mypy app

# Frontend linting
docker compose exec frontend npm run lint
```
