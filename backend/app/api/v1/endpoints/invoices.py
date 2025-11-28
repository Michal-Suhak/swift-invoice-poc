from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceResponse

router = APIRouter()


@router.get("/", response_model=list[InvoiceResponse])
async def get_invoices(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all invoices from the database
    """
    try:
        result = await db.execute(select(Invoice).order_by(Invoice.created_at.desc()))
        invoices = result.scalars().all()
        return invoices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch invoices: {str(e)}")


@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new invoice
    """
    try:
        db_invoice = Invoice(
            customer=invoice.customer,
            amount=invoice.amount,
            status=invoice.status,
        )
        db.add(db_invoice)
        await db.commit()
        await db.refresh(db_invoice)
        return db_invoice
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")
