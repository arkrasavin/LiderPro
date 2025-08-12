from enum import Enum as SAEnum

from sqlalchemy import Column, Integer, String, Date, Boolean, CheckConstraint
from sqlalchemy.orm import validates
from .base import Base


class WorkFormat(str, SAEnum):
    office = "Офис"
    remote = "Удаленно"
    hybrid = "Гибрид"


class Employee(Base):
    __tablename__ = "employees_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    position = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    work_format = Column(SAEnum(WorkFormat), nullable=True)
    remote_city = Column(String(255), nullable=True)
    emp_date = Column(Date, nullable=True)
    birthday = Column(Date, nullable=True)
    emp_ind = Column(Integer, unique=True, index=True, nullable=False)
    fired = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("emp_ind > 0", name="ck_emp_ind_positive"),
    )

    @validates("email")
    def _lower(self, _, value):
        return value.lower()
