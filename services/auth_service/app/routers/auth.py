from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
import httpx

from shared_schemas.security import TokenResponse, LoginForm
from ..core.config import get_settings

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(form: LoginForm):
    """
    Проксируем логин в Keycloak через Direct Access Grants (grant_type=password).
    ТЗ: вход по корпоративной почте + пароль.
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
                "application/json") else resp.text
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"keycloak_error": detail}
            )

        tok = resp.json()
        return TokenResponse(
            access_token=tok.get("access_token"),
            refresh_token=tok.get("refresh_token"),
            token_type=tok.get("token_type", "bearer"),
            expires_in=tok.get("expires_in"),
            scope=tok.get("scope")
        )


class ForgotPasswordIn(BaseModel):
    email: EmailStr


async def _get_admin_token() -> str:
    settings = get_settings()
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.keycloak_admin_client_id,
        "client_secret": settings.keycloak_admin_client_secret,
    }
    token_url = f"{settings.keycloak_base}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(token_url, data=data)
        resp.raise_for_status()

        return resp.json()["access_token"]


@router.post("/password/forgot", status_code=204)
async def forgot_password(payload: ForgotPasswordIn):
    """
    Отправляем письмо на корпоративную почту через Keycloak Admin API.
    Требуется: у сервис-аккаунта клиента 'backend' права на пользователей
    (например, roles: manage-users, view-users).
    """
    settings = get_settings()
    admin_token = await _get_admin_token()

    search_url = f"{settings.keycloak_base}/admin/realms/{settings.keycloak_realm}/users"
    params = {"email": payload.email}
    headers = {"Authorization": f"Bearer {admin_token}"}
    async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
        r = await client.get(search_url, params=params)
        r.raise_for_status()
        users = r.json()
        if not users:
            return
        user_id = users[0]["id"]

        exec_url = f"{settings.keycloak_base}/admin/realms/{settings.keycloak_realm}/users/{user_id}/execute-actions-email"
        r2 = await client.put(exec_url, json=["UPDATE_PASSWORD"])
        r2.raise_for_status()

    return
