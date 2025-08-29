from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from shared_schemas import TrainingSnapshot
from ..core.deps import require_roles, only_self_or_supervisor
from ..db.session import get_db
from ..models.training import Training

router = APIRouter(prefix="/api/trainings", tags=["trainings"])


@router.get("/{employee_id}/{year}", response_model=TrainingSnapshot)
def read_snapshot(
        employee_id: int,
        year: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer", "participant"])),
        __=Depends(only_self_or_supervisor)
):
    obj = db.execute(
        select(Training).where(
            Training.employee_id == employee_id, Training.year == year
        )
    ).scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Training not found")

    return TrainingSnapshot(
        employee_id=obj.employee_id, year=obj.year,
        mentee_number=obj.mentee_number,
        mentee_points=obj.mentee_points,
        conference_presence=obj.conference_presence,
        certification=obj.certification,
        introductory_conf_points=obj.introductory_conf_points,
        attendance=None,  # В MVP посещения не храним
    )


@router.put("/{employee_id}/{year}", response_model=TrainingSnapshot)
def upsert_snapshot(
        employee_id: int,
        year: int,
        payload: TrainingSnapshot,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    obj = db.execute(
        select(Training).where(
            Training.employee_id == employee_id, Training.year == year
        )
    ).scalar_one_or_none()
    if not obj:
        obj = Training(employee_id=employee_id, year=year)
    obj.mentee_number = payload.mentee_number
    obj.mentee_points = payload.mentee_points
    obj.conference_presence = payload.conference_presence
    obj.certification = payload.certification
    obj.introductory_conf_points = payload.introductory_conf_points

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return TrainingSnapshot(
        employee_id=obj.employee_id, year=obj.year,
        mentee_number=obj.mentee_number,
        mentee_points=obj.mentee_points,
        conference_presence=obj.conference_presence,
        certification=obj.certification,
        introductory_conf_points=obj.introductory_conf_points,
        attendance=None,
    )
