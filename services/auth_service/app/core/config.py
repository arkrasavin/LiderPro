import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:pass@db:5432/liderdb"
    )
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8001",
    ]
    auth_provider: str = "keycloak"  # 'local' | 'keycloak'
    keycloak_realm: str = "liderpro"
    keycloak_base: str = "http://keycloak:8080"
    keycloak_token_url: str = "http://keycloak:8080/realms/liderpro/protocol/openid-connect/token"
    keycloak_client_id: str = "backend"
    keycloak_client_secret: str = "CHANGE_ME_DEV_ONLY"
    keycloak_admin_client_id: str = "backend"
    keycloak_admin_client_secret: str = "CHANGE_ME_DEV_ONLY"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
