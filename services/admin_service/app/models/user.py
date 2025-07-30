# emp_ind переедет в мкр-сервис employee_profile_service.
# Связи is_active, login, emp_ind будут через REST,
# а не через ORM, поэтому убрал их из модели.
# Поля логин и email в модели избыточны, тк email и есть логин.


from sqlalchemy import Column, Integer, String, Enum, Boolean, Table, ForeignKey, \
    DateTime, func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), default="observer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
