from pydantic import BaseModel, EmailStr, Field, constr

_role = constr(pattern=r"^(admin|observer|participant)$")


class UserBase(BaseModel):
    name: constr(max_length=255)
    email: EmailStr
    role: _role = "observer"


class UserCreate(UserBase):
    password: constr(min_length=8) #  Есть только во входном DTO. Внутри сервиса хранится только хэш.


class UserRead(UserBase):
    id: int

    class Config: from_attributes = True
