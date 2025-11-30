from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.exceptions import DatabaseError, InvoiceDuplicateError
from app.logging_config import get_logger
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceResponse

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=list[InvoiceResponse])
async def get_invoices(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all invoices from the database.

    Returns:
        List of invoices ordered by creation date (newest first)

    Raises:
        DatabaseError: If database operation fails
    """
    try:
        logger.info("Fetching all invoices")
        result = await db.execute(select(Invoice).order_by(Invoice.created_at.desc()))
        invoices = result.scalars().all()
        logger.info(f"Successfully fetched {len(invoices)} invoices")
        return invoices
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching invoices: {str(e)}", exc_info=True)
        raise DatabaseError("Failed to fetch invoices")
    except Exception as e:
        logger.error(f"Unexpected error while fetching invoices: {str(e)}", exc_info=True)
        raise DatabaseError("Internal server error")


@router.post("/", response_model=InvoiceResponse, status_code=201)
async def create_invoice(invoice: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new invoice.

    Args:
        invoice: Invoice data to create

    Returns:
        Created invoice with generated ID and timestamps

    Raises:
        InvoiceDuplicateError: If invoice already exists
        DatabaseError: If database operation fails
    """
    try:
        logger.info(f"Creating invoice for customer: {invoice.customer}")

        db_invoice = Invoice(
            customer=invoice.customer,
            amount=invoice.amount,
            status=invoice.status,
        )
        db.add(db_invoice)
        await db.commit()
        await db.refresh(db_invoice)

        logger.info(f"Successfully created invoice with ID: {db_invoice.id}")
        return db_invoice

    except IntegrityError as e:
        await db.rollback()
        logger.warning(f"Integrity error while creating invoice: {str(e)}")
        raise InvoiceDuplicateError(details={"customer": invoice.customer})
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while creating invoice: {str(e)}", exc_info=True)
        raise DatabaseError("Failed to create invoice")
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error while creating invoice: {str(e)}", exc_info=True)
        raise DatabaseError("Internal server error")
