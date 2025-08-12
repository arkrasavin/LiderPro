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
