from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn = "postgresql+psycopg://user:pass@db:5432/hrm"
    secret_key: str = "CHANGE_ME"
    access_token_expire_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
