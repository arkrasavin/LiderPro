from pydantic import BaseModel, EmailStr


class ObserverOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ObserverPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
