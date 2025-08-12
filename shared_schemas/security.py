from typing import Literal, Optional

from pydantic import BaseModel

ROLE = Literal["admin", "observer", "participant"]


class TokenPayload(BaseModel):
    sub: int  # user_id
    email: str
    role: ROLE
    exp: int
    iat: Optional[int] = None
    iss: Optional[str] = None
    aud: Optional[str] = None
