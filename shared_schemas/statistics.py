from pydantic import BaseModel, conint


class StatisticsRead(BaseModel):
    employee_id: int
    rating__overall: conint(ge=0) | None = None
    points_sum: conint(ge=0) | None = None
    rating__efficiency: int | None = None
    points_efficiency: int | None = None
    rating__proactive: int | None = None
    points_proactive: int | None = None


class TopQuery(BaseModel):
    metric: str = "points_sum"  # Поле для сортировки
    limit: conint(le=100) = 10


class OverallStats(BaseModel):
    year: int
    curators_count: int
    mentees_count: int
    conferences_presence_rate: float | None = None
    certification_rate: float | None = None
    wallet_balance_sum: int
    total_writeoff_points: int


class DemographicsStats(BaseModel):
    year: int
    age_groups: dict[str, int]
    cities: dict[str, int]


class TopRow(StatisticsRead):
    ...
