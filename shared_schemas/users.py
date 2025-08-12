from enum import Enum

from pydantic import BaseModel, EmailStr, constr, Field

role = constr(pattern=r"^(admin|observer|employee)$")


class Role(str, Enum):
    admin = "admin"
    employee = "employee"
    observer = "observer"


class UserCreate(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Role


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role
