from fastapi import APIRouter, HTTPException, status
import httpx

from shared_schemas.security import TokenResponse, LoginForm
from ..core.config import get_settings

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(form: LoginForm):
    """
    Проксируем логин в Keycloak через Direct Access Grants (grant_type=password).
    """
    settings = get_settings()

    if settings.auth_provider != "keycloak":
        raise HTTPException(status_code=501,
                            detail="Local auth is disabled in this build")

    data = {
        "grant_type": "password",
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "username": form.username,
        "password": form.password,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(settings.keycloak_token_url, data=data)
        if resp.status_code != 200:
            detail = resp.json() if resp.headers.get("content-type", "").startswith(
                "application/json"
            ) else resp.text
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"keycloak_error": detail}
            )

        payload = resp.json()
        return TokenResponse(
            access_token=payload.get("access_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type", "bearer"),
            expires_in=payload.get("expires_in"),
            scope=payload.get("scope"),
        )


async def _get_admin_token() -> str:
    settings = get_settings()
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.keycloak_admin_client_id,
        "client_secret": settings.keycloak_admin_client_secret,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        token_resp = await client.post(settings.keycloak_token_url, data=data)
        token_resp.raise_for_status()
        admin_token = token_resp.json()["access_token"]

        return admin_token


@router.post("/password/reset", status_code=204)
async def reset_password(email: str):
    """
    Отправляем письмо на корпоративную почту через Keycloak admin API.
    Требуется: у сервис-аккаунта клиента 'backend' права на пользователей
    (например, roles: manage-users, view-users).
    """
    settings = get_settings()
    admin_token = await _get_admin_token()

    users_url = f"{settings.keycloak_base}/admin/realms/{settings.keycloak_realm}/users"
    params = {"email": email}
    headers = {"Authorization": f"Bearer {admin_token}"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        search = await client.get(users_url, params=params, headers=headers)
        search.raise_for_status()
        users = search.json()
        if not users:
            return

        user_id = users[0]["id"]

        exec_url = f"{settings.keycloak_base}/admin/realms/{settings.keycloak_realm}/users/{user_id}/execute-actions-email"
        resp = await client.put(exec_url, json=["UPDATE_PASSWORD"], headers=headers)
        resp.raise_for_status()

    return
