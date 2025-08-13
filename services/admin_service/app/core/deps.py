from typing import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .config import get_settings
from .security import decode_token
from shared_schemas.security import TokenPayload

_oauth = OAuth2PasswordBearer(tokenUrl=get_settings().oauth_token_url)


def get_current_token_payload(token: str = Depends(_oauth)) -> TokenPayload:
    return decode_token(token)


def require_roles(*roles: str) -> Callable[[TokenPayload], TokenPayload]:
    allowed = set(r.lower() for r in roles)

    def _checker(
            payload: TokenPayload = Depends(get_current_token_payload)
    ) -> TokenPayload:
        role = payload.role.lower()
        if role == "employee":
            role = "participant"
        if role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return payload

    return _checker
