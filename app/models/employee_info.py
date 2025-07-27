from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.association import employee_department

class EmployeeInfo(Base):
    __tablename__ = "employees_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    position = Column(String(255), nullable=True, index=True)
    company = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    work_format = Column(String(255), nullable=True)
    remote_city = Column(String(255), nullable=True)
    emp_date = Column(Date, nullable=True)
    birthday = Column(Date, nullable=True)

    departments = relationship(
        "Department",
        secondary=employee_department,
        back_populates="employees"
    )

    emp_ind = Column(
        Integer,
        ForeignKey("users.emp_ind", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment = "Foreign key for table users",
    )

    user = relationship("User", back_populates="employee_info")
    training = relationship("Training", back_populates="employee", uselist=False, cascade="all, delete-orphan")
    statistics = relationship("Statistics", back_populates="employee", uselist=False, cascade="all, delete-orphan")
