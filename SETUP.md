# Invoice Service - Full Setup Guide

Complete instructions for running both frontend and backend locally.

## Architecture Overview

- **Frontend**: React + Vite + TypeScript (runs on port 8080)
- **Backend**: Python FastAPI (runs on port 8000)
- **Database**: Supabase PostgreSQL

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account

### Step 1: Setup Supabase

1. Create a Supabase project at https://supabase.com/dashboard
2. Go to SQL Editor and run `backend/database.sql`
3. Copy your Project URL and anon key from Settings → API

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase credentials

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Step 3: Setup Frontend

```bash
# In a new terminal, navigate to project root
cd ..

# Install dependencies
npm install

# Configure environment (optional - defaults to localhost:8000)
cp .env.example .env

# Start the frontend
npm run dev
```

Frontend will be running at `http://localhost:8080`

## Testing the Application

1. Open `http://localhost:8080` in your browser
2. Try creating an invoice using the form
3. View the invoices list update automatically
4. Check the backend API at `http://localhost:8000/docs`

## Project Structure

```
invoice-service/
├── src/                    # React frontend source
│   ├── pages/
│   │   └── Index.tsx      # Main invoice page
│   ├── components/        # UI components (shadcn)
│   └── index.css         # Design system
├── backend/               # Python FastAPI backend
│   ├── main.py           # API routes and logic
│   ├── requirements.txt  # Python dependencies
│   ├── database.sql      # Database schema
│   └── README.md         # Backend-specific docs
├── .env.example          # Frontend env template
└── SETUP.md             # This file
```

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (backend/.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

## Common Issues

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/main.py`

### Connection Refused
- Verify backend is running: `curl http://localhost:8000/health`
- Check firewall settings

### Supabase Errors
- Verify credentials in `backend/.env`
- Ensure `invoices` table exists
- Check Supabase dashboard for errors

## Next Steps

- Add authentication with Supabase Auth
- Implement invoice editing and deletion
- Add filtering and search functionality
- Deploy backend (e.g., Railway, Render, Fly.io)
- Deploy frontend (Vercel, Netlify, or Lovable publish)
- Add comprehensive tests
- Generate OpenAPI/Swagger documentation

## Export Notes

This project is structured for easy export and extension:
- Backend can be deployed independently
- Frontend can be deployed independently
- Both communicate via REST API
- Database is hosted on Supabase (cloud-managed)
