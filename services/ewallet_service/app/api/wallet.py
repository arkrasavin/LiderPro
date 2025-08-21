from datetime import date
from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from shared_schemas import WalletEvent, Balance
from ..db.session import get_db
from ..core.deps import require_roles
from ..models.ewallet import WalletEventModel

router = APIRouter(prefix="/api/ewallet", tags=["ewallet"])


@router.get("", response_model=List[WalletEvent])
def list_events(
        employee_id: int = Query(..., ge=1),
        date_from: date | None = Query(None, alias="from"),
        date_to: date | None = Query(None, alias="to"),
        limit: int = Query(50, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    stmt = select(WalletEventModel).where(WalletEventModel.employee_id == employee_id)
    if date_from:
        stmt = stmt.where(WalletEventModel.event_date >= date_from)
    if date_to:
        stmt = stmt.where(WalletEventModel.event_date <= date_to)
    stmt = stmt.order_by(WalletEventModel.event_date.desc()).offset(offset).limit(limit)

    rows = db.execute(stmt).scalars().all()

    return [
        WalletEvent(
            **{
                "employee_id": row.employee_id,
                "event_date": row.event_date,
                "item_name": row.item_name,
                "points_delta": row.points_delta,
            }
        )
        for row in rows
    ]


@router.get("/balance/{employee_id}", response_model=Balance)
def get_balance(
        employee_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer", "participant"]))
):
    total = db.execute(
        text("""
             SELECT wallet_balance
             FROM employee
             WHERE id = :eid
             """
             ), {"eid": employee_id}).first()
    if not total:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"employee_id": employee_id, "points": total[0] or 0}


@router.post("", status_code=HTTP_201_CREATED)
def add_event(
        payload: WalletEvent,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin"]))
):
    exists = db.execute(
        text(
            """
            SELECT 1
            FROM employees_info
            WHERE id = :eid
            """
        ),
        {"eid": payload.employee_id}
    ).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Employee not found")

    evt = WalletEventModel(
        employee_id=payload.employee_id,
        event_date=payload.event_date,
        item_name=payload.item_name,
        points_delta=payload.amount if payload.kind == "accrual" else -payload.amount
    )
    db.add(evt)

    sql = text("""
               UPDATE employees_info
               SET wallet_balance  = GREATEST(0, wallet_balance + :delta),
                   writeoff_points = writeoff_points + :writeoff_inc
               WHERE id = :eid
               """)
    db.execute(
        sql, {
            "eid": payload.employee_id,
            "delta": payload.amount if payload.kind == "accrual" else -payload.amount,
            "writeoff_inc": payload.amount if payload.kind == "writeoff" else 0,
        }
    )
    db.commit()

    return {"status": "created"}
