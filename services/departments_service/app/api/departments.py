from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db.session import get_db
from shared_schemas.department import DepartmentOut, DepartmentPatch
from ..core.deps import require_roles
from ..models.department import Department

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("", response_model=dict)
def list_departments(
        id: int | None = None,
        name: str | None = None,
        sort: str | None = None,
        limit: int = Query(20, ge=1, le=200),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    stmt = select(Department)
    if id is not None:
        stmt = stmt.where(Department.id == id)
    if name:
        stmt = stmt.where(Department.name.ilike(f"%{name}%"))

    if sort == "name":
        stmt = stmt.order_by(Department.name.asc())
    elif sort == "-name":
        stmt = stmt.order_by(Department.name.desc())

    total = db.execute(select(Department).count()).scalar()
    rows = db.execute(stmt.offset(offset).limit(limit)).scalars().all()

    return {
        "items": [DepartmentOut.model_validate(x) for x in rows],
        "limit": limit,
        "offset": offset,
        "total": total,
    }


@router.get("/{dep_id}", response_model=DepartmentOut)
def get_department(
        dep_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    obj = db.get(Department, dep_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Department not found")

    return DepartmentOut.model_validate(obj)


@router.patch("/{dep_id}", response_model=DepartmentOut)
def patch_department(
        dep_id: int,
        payload: DepartmentPatch,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    empl = db.get(Department, dep_id)
    if not empl:
        raise HTTPException(status_code=404, detail="Department not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(empl, key, value)
    db.add(empl)
    db.commit()
    db.refresh(empl)

    return DepartmentOut.model_validate(empl)
