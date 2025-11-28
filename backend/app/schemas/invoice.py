from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    """Schema for creating a new invoice"""

    customer: str = Field(..., min_length=1, max_length=255, description="Customer name")
    amount: Decimal = Field(..., gt=0, description="Invoice amount")
    status: str = Field(
        default="pending", pattern="^(pending|paid|cancelled|overdue)$", description="Invoice status"
    )


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer: str
    amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
