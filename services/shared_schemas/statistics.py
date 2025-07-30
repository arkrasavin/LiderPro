from pydantic import BaseModel, conint


class StatisticsRead(BaseModel):
    employee_id: int
    raiting_overall: conint(ge=0) | None = None
    points_sum: conint(ge=0) | None = None
    raiting_efficiency: int | None = None
    points_efficiency: int | None = None
    raiting_proactive: int | None = None
    points_proactive: int | None = None


class TopQuery(BaseModel):
    metric: str = "points_sum"  # Поле для сортировки
    limit: conint(le=100) = 10
