from fastapi import APIRouter, HTTPException, status
import httpx

from shared_schemas.security import TokenResponse, LoginForm, RefreshRequest, \
    ForgotPasswordRequest
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


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    settings = get_settings()
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "refresh_token": body.refresh_token,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(settings.keycloak_token_url, data=data)
        if resp.status_code != 200:
            try:
                detail = resp.json()
            except Exception:
                detail = {"error": resp.text}
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        tok = resp.json()

        return TokenResponse(
            access_token=tok.get("access_token"),
            refresh_token=tok.get("refresh_token"),
            token_type=tok.get("token_type", "bearer"),
            expires_in=tok.get("expires_in"),
            scope=tok.get("scope"),
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshRequest):
    settings = get_settings()
    logout_url = (
        f"{settings.keycloak_base}/realms/{settings.keycloak_realm}/protocol/openid-connect/logout"
        if hasattr(settings, "keycloak_base") and hasattr(settings, "keycloak_realm")
        else settings.keycloak_token_url.replace("/token", "/logout")
    )
    data = {
        "client_id": settings.keycloak_client_id,
        "client_secret": settings.keycloak_client_secret,
        "refresh_token": body.refresh_token,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(logout_url, data=data)
        if resp.status_code not in (200, 204):
            try:
                detail = resp.json()
            except Exception:
                detail = {"error": resp.text}
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    return


@router.post("/password/forgot", status_code=status.HTTP_204_NO_CONTENT)
async def password_forgot(body: ForgotPasswordRequest):
    settings = get_settings()
    token_data = {
        "grant_type": "client_credentials",
        "client_id": settings.keycloak_admin_client_id,
        "client_secret": settings.keycloak_admin_client_secret,
    }

    if hasattr(settings, "keycloak_base") and hasattr(settings, "keycloak_realm"):
        admin_users = f"{settings.keycloak_base}/admin/realms/{settings.keycloak_realm}/users"
    else:
        base = settings.keycloak_token_url.split("/realms/")[0]
        realm = settings.keycloak_token_url.split("/realms/")[1].split("/")[0]
        admin_users = f"{base}/admin/realms/{realm}/users"

    async with httpx.AsyncClient(timeout=10.0) as client:
        tok_resp = await client.post(settings.keycloak_token_url, data=token_data)
        if tok_resp.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail={"error": "Admin token request failed", "body": tok_resp.text}
            )
        admin_token = tok_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {admin_token}"}

        search = await client.get(
            admin_users,
            params={"email": body.email, "exact": "true"},
            headers=headers
        )
        search.raise_for_status()
        users = search.json()
        if not users:
            return

        user_id = users[0]["id"]
        exec_url = f"{admin_users}/{user_id}/execute-actions-email"
        resp = await client.put(exec_url, json=["UPDATE_PASSWORD"], headers=headers)
        resp.raise_for_status()

        return
