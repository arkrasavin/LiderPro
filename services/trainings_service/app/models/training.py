# свободная строка на год
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint

from .base import Base


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, index=True, nullable=False)
    year = Column(Integer, nullable=False)

    mentee_number = Column(Integer)
    mentee_points = Column(Integer)
    conference_presence = Column(Boolean)
    certification = Column(Boolean)
    introductory_conf_points = Column(Integer)

    __table_args__ = (
        UniqueConstraint("employee_id", "year", name="uq_emp_year"),
    )
