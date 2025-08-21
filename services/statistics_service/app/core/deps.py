from typing import Callable, Optional, Iterable
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer

from .config import get_settings
from .security import decode_token
from shared_schemas.security import TokenPayload
from shared_schemas.security import ROLE

_oauth = OAuth2PasswordBearer(
    tokenUrl=get_settings().keycloak_issuer.replace(
        "/realms/", "/protocol/openid-connect/token"
    )
)

ALLOWED_ACT_AS: set[ROLE] = {"observer", "participant"}


def get_current_user(token: str = Depends(_oauth)) -> TokenPayload:
    """
    Извлекает и валидирует токен из Authorization: Bearer <token>.
    Возвращает TokenPayLoad.
    """
    return decode_token(token)


def get_effective_user(
        user: TokenPayload = Depends(get_current_user),
        x_act_as: Optional[str] = Header(default=None, alias="X-Act-As")
) -> TokenPayload:
    if not x_act_as:
        return user

    requested = (x_act_as or "").strip().lower()
    role = (user.role or "").lower()
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Forbidden",
                "message": "Impersonation allowed for admin only"
            },
        )

    if requested not in ALLOWED_ACT_AS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Bad request",
                "message": f"Invalid X-Act_As value '{requested}'. "
                           f"Allowed:  {sorted(ALLOWED_ACT_AS)}",
            },
        )

    output = user.model_copy(update={"role": requested})

    return output


def require_roles(
        allowed: Iterable[ROLE],
        *,
        admin_always_ok: bool = True
) -> Callable[[TokenPayload], TokenPayload]:
    allowed_set = {
        str(role).lower()
        for role in allowed
    }

    def _checker(user: TokenPayload = Depends(get_effective_user)) -> TokenPayload:
        role = (user.role or "").lower()
        if role == "employee":
            role = "participant"
        if admin_always_ok and role == "admin":
            return user

        if role not in allowed_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Forbidden",
                    "message": f"Role '{role}' is not allowed. "
                               f"Required: {sorted(allowed_set)}",
                },
            )

        return user

    return _checker
