from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.association import employee_department, observer_department


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, default="Name")

    employees = relationship(
        "EmployeeInfo",
        secondary=employee_department,
        back_populates="departments"
    )

    observers = relationship(
        "Observer",
        secondary=observer_department,
        back_populates="departments"
    )