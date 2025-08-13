from typing import Literal, Optional, Union
from pydantic import BaseModel, EmailStr

ROLE = Literal["admin", "observer", "participant", "employee"]


class LoginForm(BaseModel):
    username: EmailStr
    password: str


class TokenPayload(BaseModel):
    sub: Union[str, int]
    email: str
    role: ROLE
    exp: int
    iat: Optional[int] = None
    iss: Optional[str] = None
    aud: Optional[Union[str, list[str]]] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None
    scope: str | None = None
