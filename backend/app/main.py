from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.exception_handlers import app_exception_handler, general_exception_handler
from app.exceptions import AppError
from app.logging_config import get_logger, setup_logging
from app.middleware.logging import RequestLoggingMiddleware

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Invoice Service API",
    description="Backend API for managing invoices",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Register global exception handlers (must be before middleware)
app.add_exception_handler(AppError, app_exception_handler)  # type: ignore[arg-type]
# Safety net for any unhandled exceptions
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(RequestLoggingMiddleware)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Invoice Service API v{app.version}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(
        f"Database: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Invoice Service API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
