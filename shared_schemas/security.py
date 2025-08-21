from typing import Literal, Optional, Union
from pydantic import BaseModel, EmailStr

ROLE = Literal["admin", "observer", "participant"]


class LoginForm(BaseModel):
    username: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None
    scope: str | None = None


class TokenPayload(BaseModel):
    sub: str | None = None
    email: EmailStr | None = None
    role: ROLE | None = None
    exp: int | None = None
    iat: int | None = None
    iss: str | None = None
    aud: Union[str, list[str], None] = None
