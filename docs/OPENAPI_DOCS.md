# API Documentation

## Interactive Documentation

FastAPI automatically generates OpenAPI/Swagger documentation:

- **Swagger UI**: http://localhost:8000/docs (interactive testing)
- **ReDoc**: http://localhost:8000/redoc (clean view)
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Quick Start

1. Start backend: `docker-compose up backend`
2. Visit http://localhost:8000/docs
3. Click "Try it out" on any endpoint to test

## Endpoints

### Health Check
```http
GET /api/v1/health
```

### List Invoices
```http
GET /api/v1/invoices/
```

### Create Invoice
```http
POST /api/v1/invoices/
Content-Type: application/json

{
  "customer": "John Doe",
  "amount": 1500.00,
  "status": "pending"
}
```

## Using the OpenAPI Spec

**Import to Postman/Insomnia**:
```bash
http://localhost:8000/openapi.json
```

**Generate TypeScript client**:
```bash
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-fetch \
  -o ./src/api-client
```

**Download spec**:
```bash
curl http://localhost:8000/openapi.json > docs/openapi.json
```

## Data Models

**InvoiceCreate**:
- `customer` (string, required): 1-255 chars
- `amount` (number, required): > 0
- `status` (string, optional): `pending` | `paid` | `cancelled` | `overdue`

**InvoiceResponse**:
- All fields from InvoiceCreate plus:
- `id` (integer)
- `created_at` (datetime)
- `updated_at` (datetime)