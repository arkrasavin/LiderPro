from datetime import date
from typing import Literal
from pydantic import BaseModel, conint


class WalletEvent(BaseModel):
    employee_id: int
    event_date: date
    item_name: str
    amount: conint(ge=0)
    kind: Literal["accrual", "writeoff"]
    # points_delta: int


class Balance(BaseModel):
    employee_id: int
    points: conint(ge=0)
