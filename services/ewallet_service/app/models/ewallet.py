from sqlalchemy import Column, Integer, Date, String

from .base import Base


class WalletEventModel(Base):
    __tablename__ = "ewallet"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, index=True)
    event_date = Column(Date)
    item_name = Column(String(255))
    points_delta = Column(Integer) # + начисление / - дебит
