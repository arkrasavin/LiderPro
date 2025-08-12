from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from ..core.config import get_settings

ALGORITHM = "HS256"
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return _pwd.hash(password)


def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return _pwd.verify(plain_pass, hashed_pass)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().auth_secret_key,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def create_reset_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, get_settings().auth_secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None
