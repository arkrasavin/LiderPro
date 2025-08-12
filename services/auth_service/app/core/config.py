import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_secret_key: str = os.getenv("AUTH_SECRET_KEY", "CHANGE_ME")
    smtp_host: str | None = os.getenv("SMTP_HOST")
    smtp_port: int | None = int(os.getenv("SMTP_PORT", "0") or 0)
    smtp_user: str | None = os.getenv("SMTP_USER")
    smtp_pass: str | None = os.getenv("SMTP_PASS")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:pass@db:5432/liderdb"
    )
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config: env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
