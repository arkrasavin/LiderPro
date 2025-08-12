from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared_schemas import EmployeeRead
from ..db.session import get_db
from ..models.employee import Employee

router = APIRouter(prefix="/api/employees_info", tags=["employees"])


@router.get("", response_model=List[EmployeeRead])
def list_employees(db: Session = Depends(get_db)):
    rows = db.execute(select(Employee)).scalars().all()
    return [
        Employee.model_validate(r)
        for r in rows
    ]
