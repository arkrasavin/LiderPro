from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.deps import require_roles
from shared_schemas import EmployeeOut, EmployeeUpdate
from ..db.session import get_db
from ..models.employee import Employee

router = APIRouter(prefix="/api/employees_info", tags=["employees_info"])


@router.get("", response_model=dict)
def list_employees(
        id: int | None = None,
        name: str | None = None,
        email: str | None = None,
        position: str | None = None,
        company: str | None = None,
        department: str | None = None,
        city: str | None = None,
        remote_city: str | None = None,
        emp_date: str | None = None,
        birthday: str | None = None,
        emp_ind: int | None = None,
        sort: str | None = None,
        limit: int = Query(20, ge=1, le=200),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    query_empl = select(Employee)
    if id is not None: query_empl = query_empl.where(Employee.id == id)
    if name: query_empl = query_empl.where(Employee.name.ilike(f"%{name}%"))
    if email: query_empl = query_empl.where(Employee.email == email)
    if position: query_empl = query_empl.where(Employee.position == position)
    if company: query_empl = query_empl.where(Employee.company == company)
    if department: query_empl = query_empl.where(Employee.department == department)
    if city: query_empl = query_empl.where(Employee.city == city)
    if remote_city: query_empl = query_empl.where(Employee.remote_city == remote_city)
    if emp_ind is not None: query_empl = query_empl.where(Employee.emp_ind == emp_ind)

    if sort in {"name", "position", "company", "department", "city"}:
        query_empl = query_empl.order_by(getattr(Employee, sort))
    total = db.execute(query_empl).scalars().all()
    data = [
        EmployeeOut.model_validate(elem)
        for elem in total[offset:offset + limit]
    ]

    answer = {
        "data": data,
        "meta": {"total_count": len(total)},
        "limit": limit,
        "offset": offset,
        "filters": {
            key: value
            for key, value in dict(
                id=id,
                name=name,
                email=email,
                position=position,
                company=company,
                department=department,
                city=city,
                remote_city=remote_city,
                emp_ind=emp_ind,
            ).items() if value is not None
        }
    }

    return answer


@router.get("/{emp_id}", response_model=EmployeeOut)
def get_employee(
        emp_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    empl = db.get(Employee, emp_id)
    if not empl:
        raise HTTPException(404, "Employee not found")
    return EmployeeOut.model_validate(empl)


@router.put("/{emp_id}", response_model=EmployeeOut)
def update_employee(
        emp_id: int,
        payload: EmployeeUpdate,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    empl = db.get(Employee, emp_id)
    if not empl:
        raise HTTPException(404, "Employee not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(empl, key, value)
    db.add(empl)
    db.commit()
    db.refresh(empl)

    return EmployeeOut.model_validate(empl)


@router.post("", response_model=EmployeeOut, status_code=201)
def create_employee(
        payload: EmployeeUpdate,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    obj = Employee(**payload.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return EmployeeOut.model_validate(obj)


@router.patch("/{emp_id}", response_model=EmployeeOut)
def path_employee(
        emp_id: int,
        payload: EmployeeUpdate,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    obj = db.get(Employee, emp_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return EmployeeOut.model_validate(obj)


@router.delete("/{emp_id}", status_code=204)
def delete_employee(
        emp_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    obj = db.get(Employee, emp_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(obj)
    db.commit()
