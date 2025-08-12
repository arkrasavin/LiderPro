# явка/баллы MK-N
from sqlalchemy import Integer, Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    training_id = Column(Integer, ForeignKey("training.id", ondelete="CASCADE"))
    event_code = Column(String(30))  # MK1, MK2 т тд
    presence = Column(Boolean)
    points = Column(Integer)

    training = relationship("Training", back_populates="events")
