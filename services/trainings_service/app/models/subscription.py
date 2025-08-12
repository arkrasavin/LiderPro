# подписка на ленту
from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, index=True)
    channel = Column(String(100))
    subscribed = Column(Boolean, default=False)
