from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError

from ..core.config import get_settings
from shared_schemas.security import TokenPayload


def decode_payload(token: str) -> TokenPayload:
    """
    Декодирует и валидирует токен JWT. Бросает 401 при ошибках
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.auth_secret_key,
            algorithms=[settings.auth_algorithm]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    try:
        return TokenPayload.model_validate(payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
