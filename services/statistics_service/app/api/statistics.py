from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import conint
from sqlalchemy import text
from sqlalchemy.orm import Session

from shared_schemas import StatisticsRead, TopRow, DemographicsStats, OverallStats
from ..core.deps import require_roles
from ..db.session import get_db

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


def _pick_year(db: Session, year: int | None) -> int:
    if year:
        return year
    res = db.execute(
        text(
            """
            SELECT COALESCE(MAX(year),
                            EXTRACT(YEAR FROM CURRENT_DATE) ::int) AS y
            FROM training
            """
        )
    )
    row = res.mappings().first()

    return int(row['y']) if row and row['y'] else date.today().year


@router.get("/{employee_id}", response_model=StatisticsRead)
def stats_by_employee(
        employee_id: int,
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer", "participant"]))
):
    row = db.execute(
        text(
            """
            SELECT e.id AS employee_id,
                   e.total_points,
                   e.effective_points,
                   e.proactive_points
            FROM employees_info e
            WHERE e.id = :employee_id
            """
        ), {"employee_id": employee_id},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")

    ranks = db.execute(
        text(
            """
            WITH r AS (SELECT id,
                              dense_rank()
                                  OVER (ORDER BY total_points DESC, id ASC) AS r_overall, dense_rank()
                    OVER (ORDER BY effective_points DESC, id ASC) AS r_eff, dense_rank()
                    OVER (ORDER BY proactive_points DESC, id ASC) AS r_pro
                       FROM employees_info)
            SELECT r_overall, r_eff, r_pro
            FROM r
            WHERE id = :employee_id
            """
        ), {"employee_id": employee_id},
    ).mappings().first()

    return StatisticsRead(
        employee_id=row["employee_id"],
        points_sum=row["total_points"] or 0,
        rating__overall=(ranks["r_overall"] if ranks else None),
        rating__efficiency=(ranks["r_eff"] if ranks else None),
        rating__proactive=(ranks["r_pro"] if ranks else None),
        points_efficiency=row["effective_points"] or 0,
        points_proactive=row["proactive_points"] or 0,
    )


@router.get("/top", response_model=list[TopRow])
def top_by_metric(
        metric: Annotated[
            Literal[
                "points_sum",
                "points_efficiency",
                "points_proactive"
            ], Query(alias="metric")
        ] = "points_sum",
        limit: Annotated[conint(gt=0, le=100), Query()] = 10,
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
                SELECT id AS employee_id,
                total_points, 
                effective_points, 
                proactive_points
                FROM employees_info
                ORDER BY {col} DESC, id ASC
                LIMIT :limit
            """
        ), {"limit": limit}
    ).mappings().all()

    ranks = db.execute(
        text(
            """
            SELECT id,
                   dense_rank()
                       OVER (ORDER BY total_points DESC, id ASC) AS r_overall, dense_rank()
                OVER (ORDER BY effective_points DESC, id ASC) AS r_eff, dense_rank()
                OVER (ORDER BY proactive_points DESC, id ASC) AS r_pro
            FROM employees_info
            """
        )
    ).mappings().all()
    ranks_map = {rank["id"] for rank in ranks}
    out: list[TopRow] = []
    for row in rows:
        rk = ranks_map.get(row["employee_id"], {})
        out.append(
            TopRow(
                employee_id=rk["employee_id"],
                points_sum=rk["total_points"] or 0,
                rating__overall=rk.get("r_overall"),
                rating__efficiency=rk.get("r_eff"),
                rating__proactive=rk.get("r_pro"),
                points_efficiency=rk["effective_points"] or 0,
                points_proactive=rk["proactive_points"] or 0,
            )
        )

    return out


@router.get("/demographics", response_model=DemographicsStats)
def demographics(
        year: int | None = Query(default=None, ge=2000, le=2100),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    city_rows = db.execute(text("""
                                SELECT city, COUNT(*) AS c
                                FROM employees_info
                                GROUP BY city
                                ORDER BY c DESC, city ASC
                                """)).mappings().all()
    cities = {
        row["city"] or "_": int(row["c"])
        for row in city_rows
    }
    age_rows = db.execute(
        text(
            """
            SELECT CASE
                       WHEN birthday IS NULL THEN 'unknown'
                       WHEN date_part('year', age(birthday)) BETWEEN 18 AND 25
                           THEN '18-25'
                       WHEN date_part('year', age(birthday)) BETWEEN 26 AND 35
                           THEN '26-35'
                       WHEN date_part('year', age(birthday)) BETWEEN 36 AND 45
                           THEN '36-45'
                       WHEN date_part('year', age(birthday)) BETWEEN 46 AND 55
                           THEN '46-55'
                       WHEN date_part('year', age(birthday)) BETWEEN 56 AND 65
                           THEN '56-65'
                       WHEN date_part('year', age(birthday)) BETWEEN 66 AND 75
                           THEN '66-75'
                       ELSE '76+'
                       END  AS bucket,
                   COUNT(*) AS c
            FROM employees_info
            GROUP BY bucket
            """
        )
    ).mappings().all()
    age_groups = {
        row["bucket"]: int(row["c"])
        for row in age_rows
    }

    return DemographicsStats(
        year=_pick_year(db, year),
        age_groups=age_groups,
        cities=cities,
    )


@router.get("", response_model=OverallStats)
def overall_stats(
        year: int | None = Query(default=None, ge=2000, le=2100),
        db: Session = Depends(get_db),
        _=Depends(require_roles(["admin", "observer"]))
):
    agg = db.execute(
        text(
            """
            SELECT COUNT(*)::int AS curators_count, COALESCE(SUM(wallet_balance), 0)::int AS wallet_balance_sum, COALESCE(SUM(writeoff_points), 0) ::int AS total_writeoff_points
            FROM emplouees_info
            """
        )
    ).mappings().first()
    if year is None:
        yr = db.execute(text(
            """
            SELECT COALESCE(MAX(year), EXTRACT(YEAR FROM NOW()) ::int) AS yr
            FROM training
            """
        )).mappings().first()
        year = int(yr["yr"]) if yr else date.today().year
    rates = db.execute(text(
        """
        SELECT COALESCE(SUM(CASE WHEN t.conference_presence THEN 1 ELSE 0 END), 0)::float
              / NULLIF(COUNT(e.id), 0) AS conferences_presence_rate, COALESCE(
                SUM(CASE WHEN t.certification THEN 1 ELSE 0 END), 0)::float
              / NULLIF(COUNT(e.id), 0) AS certification_rate, COALESCE(SUM(t.mentee_number), 0) ::int AS mentees_count
        FROM employees_info e
                 LEFT JOIN training t
                           ON t.employee_id = e.id AND t.year = :year
        """
    ), {"year": year}).mappings().first()

    return OverallStats(
        year=year,
        curators_count=int(agg["curators_count"]),
        mentees_count=int(rates["mentees_count"] or 0),
        conferences_presence_rate=float(rates["conferences_presence_rate"] or 0.0),
        certification_rate=float(rates["certification_rate"] or 0.0),
        wallet_balance_sum=int(agg["wallet_balance_sum"]),
        total_writeoff_points=int(agg["total_writeoff_points"]),
    )
