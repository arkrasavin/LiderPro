from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class WorkFormat(str, Enum):
    office = "Офис"
    remote = "Удаленно"
    hybrid = "Гибрид"


class EmployeeBase(BaseModel):
    name: str = Field(..., max_length=255)
    emp_ind: int = Field(..., ge=1)
    email: EmailStr
    position: str | None = None
    company: str | None = None
    department: str | None = None
    city: str | None = None
    work_format: WorkFormat | None = None
    remote_city: str | None = None
    emp_date: date | None = None
    birthday: date | None = None


class EmployeeRead(EmployeeBase):
    id: int
    fired: bool | None = None

    class Config:
        from_attributes = True
