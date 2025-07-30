from enum import Enum

from sqlalchemy import Column, Integer, String, Date, Boolean, CheckConstraint
from sqlalchemy.orm import validates
from .base import Base


class WorkFormat(str, Enum):
    office = "Офис"
    remote = "Удалено"
    hybrid = "Гибрид"


class Employee(Base):
    __tablename__ = "employ_info"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    emp_ind = Column(Integer, unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    position = Column(String(255))
    company = Column(String(255))
    department = Column(String(255))
    city = Column(String(255))
    work_format = Column(Enum(WorkFormat))
    remote_city = Column(String(255))
    hire_date = Column("emp_date", Date)
    birthday = Column(Date)
    fired = Column(Boolean, default=False)
    long_leave = Column(Boolean, default=False)

    __table_args__ = (CheckConstraint("emp_ind > 0", name="ck_emp_ind_positive"),)

    @validates("email")
    def _lower(self, _, value):
        return value.lower()
