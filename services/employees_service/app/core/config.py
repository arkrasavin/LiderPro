from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    database_url: str = "postgresql+psycopg2://user:pass@db:5432/liderdb"
    auth_provider: str = "keycloak"
    keycloak_issuer: str
    keycloak_audience: str = "account"
    keycloak_jwks_url: str
    cors_origins: str = "*"


def get_settings() -> Settings:
    return Settings()
