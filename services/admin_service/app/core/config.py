from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8001",
    ]
    auth_secret_key: str = "CHANGE_ME"
    auth_algorithm: str = "HS256"
    oauth_token_url: str = "/auth/login"
    database_url: PostgresDsn = "postgresql+psycopg2://user:pass@db:5432/liderdb"
    auth_provider: str = "local"  # local | keycloak
    keycloak_issuer: str = "http://keycloak:8080/realms/liderpro"
    keycloak_audience: str = "backend"
    keycloak_jwks_url: str = "http://keycloak:8080/realms/liderpro/protocol/openid-connect/certs"


@lru_cache
def get_settings() -> Settings:
    return Settings()
