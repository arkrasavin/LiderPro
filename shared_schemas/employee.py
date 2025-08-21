from pydantic import BaseModel, EmailStr
from datetime import date

from typing import Optional


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    position: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    city: str
    work_format: Optional[str] = None
    remote_city: Optional[str] = None
    emp_date: Optional[date] | None = None
    birthday: Optional[date] = None
    emp_ind: Optional[int] = None
    total_points: int = 0
    proactive_points: int = 0
    effective_points: int = 0
    wallet_balance: int = 0
    writeoff_points: int = 0

    class Config:
        from_attributes = True


# Все поля являются обязательными, некоторые являются default = None только для MVP и тестирования
class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    position: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    city: str
    work_format: Optional[str] = None
    remote_city: Optional[str] = None
    emp_date: Optional[date] = None
    birthday: Optional[date] = None
    emp_ind: Optional[int] = None
