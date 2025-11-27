# Invoice Service Backend (FastAPI)

Python FastAPI backend for the Invoice Service application.

## Prerequisites

- Python 3.9+
- Supabase account with a project created
- pip or poetry for package management

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project or use existing one
3. Navigate to Settings → API
4. Copy your `Project URL` and `anon/public` key

### 3. Set Up Database

1. Go to SQL Editor in Supabase Dashboard
2. Run the SQL script from `database.sql`
3. Verify the `invoices` table was created

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual Supabase credentials
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key-here
```

### 5. Run the Backend

```bash
# From the backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```

### Get All Invoices
```http
GET /invoices
```

### Create Invoice
```http
POST /invoices
Content-Type: application/json

{
  "customer": "John Doe",
  "amount": 1500.00,
  "status": "pending"
}
```

## Testing the API

### Using curl:
```bash
# Health check
curl http://localhost:8000/health

# Get all invoices
curl http://localhost:8000/invoices

# Create an invoice
curl -X POST http://localhost:8000/invoices \
  -H "Content-Type: application/json" \
  -d '{"customer":"Test Customer","amount":100.00,"status":"pending"}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── requirements.txt     # Python dependencies
├── database.sql         # Supabase table schema
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Development Notes

- The API uses CORS middleware to allow requests from the frontend (localhost:8080, 5173, 3000)
- All invoice data is stored in Supabase PostgreSQL
- Input validation is handled by Pydantic models
- The API follows RESTful conventions

## Next Steps

- Add authentication/authorization
- Implement invoice updates and deletions
- Add pagination for large datasets
- Include invoice PDF generation
- Add comprehensive test suite
