from typing import Literal, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .config import get_settings
from .security import decode_payload
from shared_schemas.security import TokenPayload

_oauth = OAuth2PasswordBearer(tokenUrl=get_settings().oauth_token_url)


def get_current_token_payload(token: str = Depends(_oauth)) -> TokenPayload:
    """
    Извлекает и валидирует токен из Authorization: Bearer <token>.
    Возвращает TokenPayload.
    """
    payload = decode_payload(token)
    return payload


def require_role(*roles: Literal["admin", "observer", "participant"]) -> Callable:
    """
    Использование:
        @router.get("/secure", dependencies=[Depends(require_role("admin", "observer"))])
    или
        def endpoint(payload: TokenPayLoad = Depends(require_role("admin"))): ...
    """

    def _checker(
            payload: TokenPayload = Depends(get_current_token_payload)
    ) -> TokenPayload:
        if payload.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        return payload

    return _checker
