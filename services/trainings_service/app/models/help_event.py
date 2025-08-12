# помощь в мероприятии
from datetime import date

from sqlalchemy import Column, Integer, Date, String

from .base import Base


class HelpEvent(Base):
    __tablename__ = "help_event"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, index=True)
    event_date = Column(Date, default=date.today)
    description = Column(String(255))
