from datetime import date

from pydantic import BaseModel, conint


class WalletEvent(BaseModel):
    employee_id: int
    event_date: date
    item_name: str
    points_delta: int  # >0 - начисление, <0 - списание


class Balance(BaseModel):
    employee_id: int
    points: conint(ge=0)
