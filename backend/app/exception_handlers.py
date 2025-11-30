from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError
from app.logging_config import get_logger

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    Handler catches all exceptions that inherit from AppError
    and converts them into proper HTTP JSON responses.

    Args:
        request: The incoming request
        exc: The custom exception

    Returns:
        JSON response with error details and appropriate status code
    """

    logger.error(
        f"AppError: {exc.message} | "
        f"Status: {exc.status_code} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Details: {exc.details}"
    )

    response_content: dict[str, Any] = {"error": exc.message}

    if exc.details:
        response_content["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Safety net for any exceptions that slip through.
    It ensures we never leak stack traces or internal details to clients.

    Args:
        request: The incoming request
        exc: The unhandled exception

    Returns:
        JSON response with generic error message
    """
    # Log full error details server-side (including stack trace)
    logger.error(
        f"Unhandled exception: {str(exc)} | "
        f"Type: {type(exc).__name__} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}",
        exc_info=True,  # Include full stack trace in logs
    )

    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
