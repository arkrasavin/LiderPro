from typing import Optional

from pydantic import BaseModel, EmailStr

from .security import ROLE


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: ROLE

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: ROLE


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: ROLE | None = None
