from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from shared_schemas import StatisticsRead
from ..core.deps import require_roles
from ..db.session import get_db

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("/{employee_id}", response_model=StatisticsRead)
def stats_by_employee(
        employee_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    row = db.execute(text(
        """
        SELECT id               as employee_id,
               total_points     as points_sum,
               effective_points as points_efficiency,
               proactive_points as points_proactive
        FROM employees_info
        WHERE id = :eid
        """
    ), {"eid": employee_id}).mappings().first()

    if not row:
        raise HTTPException(404, "Employee not found")

    # рейтинг в этом MVP пока не считаем (None),
    # points_* возвращаем как есть
    return StatisticsRead(
        employee_id=row["employee_id"],
        points_sum=row["points_sum"] or 0,
        rating__overall=None,
        rating__efficiency=None,
        rating__proactive=None,
        points_efficiency=row["points_efficiency"] or 0,
        points_proactive=row["points_proactive"] or 0,
    )


@router.get("/top", response_model=list[StatisticsRead])
def top_employees(
        metric: str = Query(
            "points_sum",
            pattern="^(points_sum|points_efficiency|points_proactive)S"
        ),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    field_map = {
        "points_sum": "total_points",
        "points_efficiency": "effective_points",
        "points_proactive": "proactive_points",
    }
    col = field_map[metric]
    rows = db.execute(
        text(
            f"""
        SELECT id as employee_id, total_points, effective_points, proactive_points
        FROM employees_info
        ORDER BY {col} DESC 
        LIMIT :lim
    """
        ), {"lim": limit}.mappings().all()
    )

    return [
        StatisticsRead(
            employee_id=r["employee_id"],
            points_sum=r["total_points"] or 0,
            rating__overall=None,
            rating__efficiency=None,
            rating__proactive=None,
            points_efficiency=r["effective_points"] or 0,
            points_proactive=r["proactive_points"] or 0,
        )
        for r in rows
    ]
