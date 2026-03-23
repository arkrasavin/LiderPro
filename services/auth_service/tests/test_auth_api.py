import httpx


class DummyResponse:
    def __init__(self, status_code: int, payload=None, text: str = ""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text
        self.headers = {
            "content-type": "application/json"
        }

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            request = httpx.Request("GET", "http://test")
            response = httpx.Response(status_code=self.status_code, request=request)
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=request,
                response=response,
            )


def test_login_success(client, monkeypatch):
    async def fake_post(self, url, data=None, **kwargs):
        assert url.endswith("/token")
        assert data["grant_type"] == "password"
        assert data["username"] == "admin@corp.example"
        return DummyResponse(
            200,
            {
                "access_token": "access-123",
                "refresh_token": "refresh-123",
                "token_type": "bearer",
                "expires_in": 300,
                "scope": "openid profile",
            },
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    response = client.post(
        "/auth/login",
        json={
            "username": "admin@corp.example",
            "password": "secret123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] == "access-123"
    assert body["refresh_token"] == "refresh-123"
    assert body["token_type"] == "bearer"


def test_login_invalid_credentials_returns_401(client, monkeypatch):
    async def fake_post(self, url, data=None, **kwargs):
        return DummyResponse(
            400,
            {"error": "invalid_grant", "error_description": "Bad credentials"},
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    response = client.post(
        "/auth/login",
        json={
            "username": "admin@corp.example",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    body = response.json()
    assert body["detail"]["keycloak_error"]["error"] == "invalid_grant"


def test_refresh_success(client, monkeypatch):
    async def fake_post(self, url, data=None, **kwargs):
        assert data["grant_type"] == "refresh_token"
        assert data["refresh_token"] == "refresh-123"
        return DummyResponse(
            200,
            {
                "access_token": "new-access-123",
                "refresh_token": "new-refresh-123",
                "token_type": "bearer",
                "expires_in": 300,
            },
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "refresh-123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] == "new-access-123"
    assert body["refresh_token"] == "new-refresh-123"


def test_logout_success_returns_204(client, monkeypatch):
    async def fake_post(self, url, data=None, **kwargs):
        assert url.endswith("/logout")
        assert data["refresh_token"] == "refresh-123"
        return DummyResponse(204)

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    response = client.post(
        "/auth/logout",
        json={"refresh_token": "refresh-123"},
    )

    assert response.status_code == 204
    assert response.text == ""


def test_forgot_password_unknown_email_returns_204(client, monkeypatch):
    async def fake_post(self, url, data=None, **kwargs):
        return DummyResponse(200, {"access_token": "admin-token"})

    async def fake_get(self, url, params=None, headers=None, **kwargs):
        assert params["email"] == "nobody@corp.example"
        return DummyResponse(200, [])

    async def fake_put(self, url, json=None, headers=None, **kwargs):
        raise AssertionError("PUT не должен вызываться, если пользователь не найден")

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    monkeypatch.setattr(httpx.AsyncClient, "put", fake_put)

    response = client.post(
        "/auth/forgot-password",
        json={"email": "nobody@corp.example"},
    )

    assert response.status_code == 204
