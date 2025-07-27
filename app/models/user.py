from sqlalchemy import Column, Integer, String, Enum, Boolean, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

import enum

from app.models.base import Base

class UserRole(str, enum.Enum):
    employee = "employee"
    observer = "observer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    emp_ind = Column(Integer, unique=True, nullable=True, index=True, comment="Foreign key for table employees_info")
    login = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.employee)
    is_active = Column(Boolean, default=True, server_default='true')

    admin = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    observer = relationship("Observer", back_populates="user", uselist=False, cascade="all, delete-orphan")

    employee_info = relationship("EmployeeInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def is_admin(self):
        return self.role == UserRole.admin
