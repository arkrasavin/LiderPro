from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from ..core.config import get_settings

ALGORITHMS = "HS256"
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw: str) -> str:
    return _pwd.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return _pwd.verify(raw, hashed)


def create_access_token(sub: str) -> str:
    cfg = get_settings()
    return jwt.encode(
        {
            "subject": sub,
            "exp": datetime.now() + timedelta(munutes=cfg.access_token_expire_minutes)
        },
        cfg.secret_key,
        algorithm=ALGORITHMS,
    )


def decode_access_token(token: str) -> str | None:
    try:
        return jwt.secode(token, get_settings().secret_key, algorithm=[ALGORITHMS])["sub"]
    except JWTError:
        return None
