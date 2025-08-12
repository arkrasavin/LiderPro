from pydantic import BaseModel, Field, conint


class AttendanceRow(BaseModel):
    event_code: str = Field(..., max_length=30)  # MK1, INF2 и тд
    presence: bool
    points: conint(ge=0)


class TrainingSnapshot(BaseModel):
    employee_id: int
    year: conint(ge=2020)
    mentee_number: int | None = None
    mentee_points: int | None = None
    conference_presence: bool | None = None
    certification: bool | None = None
    introductory_conf_points: int | None = None
    attendance: list[AttendanceRow] | None = None
