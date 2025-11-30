"""Custom exception classes for the application."""

from typing import Any


class AppError(Exception):
    """Base exception class for application errors."""

    def __init__(self, message: str, status_code: int = 500, details: dict[str, Any] | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class InvoiceNotFoundError(AppError):
    def __init__(self, invoice_id: int):
        super().__init__(
            message="Invoice not found",
            status_code=404,
            details={"invoice_id": invoice_id},
        )


class InvoiceDuplicateError(AppError):
    def __init__(self, details: dict[str, Any] | None = None):
        super().__init__(
            message="Invoice already exists",
            status_code=409,
            details=details,
        )


class InvoiceValidationError(AppError):
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(
            message=message,
            status_code=400,
            details=details,
        )


class DatabaseError(AppError):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            status_code=500,
        )
