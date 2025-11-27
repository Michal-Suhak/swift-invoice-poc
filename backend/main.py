"""
FastAPI backend for Invoice Service
Run with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import os
from supabase import create_client, Client

# Initialize FastAPI app
app = FastAPI(
    title="Invoice Service API",
    description="Backend API for managing invoices",
    version="1.0.0"
)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic Models
class InvoiceCreate(BaseModel):
    """Schema for creating a new invoice"""
    customer: str = Field(..., min_length=1, max_length=255, description="Customer name")
    amount: float = Field(..., gt=0, description="Invoice amount in USD")
    status: str = Field(default="pending", pattern="^(pending|paid|cancelled)$", description="Invoice status")

class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: str
    customer: str
    amount: float
    status: str
    created_at: str

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str

# API Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices():
    """
    Retrieve all invoices from the database
    """
    try:
        response = supabase.table("invoices").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch invoices: {str(e)}")

@app.post("/invoices", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate):
    """
    Create a new invoice
    """
    try:
        invoice_data = {
            "customer": invoice.customer,
            "amount": invoice.amount,
            "status": invoice.status,
        }
        
        response = supabase.table("invoices").insert(invoice_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create invoice")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
