from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table, UniqueConstraint

from app.models.base import Base


employee_department = Table(
    'employee_department',
    Base.metadata,
    Column('employee_id', Integer, ForeignKey('employees_info.id'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id'), primary_key=True),
)

observer_department = Table(
    'observer_department',
    Base.metadata,
    Column('observer_id', Integer, ForeignKey('observers.id'), primary_key=True),
    Column('department_id', Integer, ForeignKey('departments.id'), primary_key=True),
)