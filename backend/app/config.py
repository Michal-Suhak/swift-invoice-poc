from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    POSTGRES_USER: str = "invoice_user"
    POSTGRES_PASSWORD: str = "invoice_password"
    POSTGRES_DB: str = "invoice_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def sync_database_url(self) -> str:
        """Sync database URL for Alembic migrations"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    CORS_ORIGINS: list[str] = ["http://localhost:8080", "http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = "../.env"  # Use root .env file
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
