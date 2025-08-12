from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    auth_secret_key: str = "CHANGE_ME"
    auth_algorithm: str = "HS256"
    oauth_token_url: str = "/auth/login"
    database_url: PostgresDsn = "postgresql+psycopg2://user:pass@db:5432/liderdb"
    # access_token_expire_minutes: int = 60       # время "жизни" токена
    cors_origins: list[str] = [
        "http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"
    ]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
