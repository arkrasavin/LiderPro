import os

os.environ["DATABASE_URL"] = "sqlite:///./test_employees.db"
os.environ["AUTH_PROVIDER"] = "keycloak"
os.environ["KEYCLOAK_ISSUER"] = "http://fake-keycloak/realms/liderpro"
os.environ["KEYCLOAK_JWKS_URL"] = "http://fake-keycloak/certs"
os.environ["KEYCLOAK_AUDIENCE"] = "account"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..app.main import app
from ..app.db.session import get_db
from ..app.models.base import Base
from ..app.core.deps import decode_token
from shared_schemas.security import TokenPayload

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_employees.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_admin(monkeypatch):
    def fake_decode_token(token: str):
        return TokenPayload(
            sub="1",
            email="admin@corp.example",
            role="admin",
            roles=["admin"],
        )

    monkeypatch.setattr("app.core.deps.decode_token", fake_decode_token)


@pytest.fixture
def mock_observer(monkeypatch):
    def fake_decode_token(token: str):
        return TokenPayload(
            sub="2",
            email="observer@corp.example",
            role="observer",
            roles=["observer"],
        )

    monkeypatch.setattr("app.core.deps.decode_token", fake_decode_token)


@pytest.fixture
def mock_participant(monkeypatch):
    def fake_decode_token(token: str):
        return TokenPayload(
            sub="3",
            email="user@corp.example",
            role="participant",
            roles=["participant"],
        )

    monkeypatch.setattr("app.core.deps.decode_token", fake_decode_token)
