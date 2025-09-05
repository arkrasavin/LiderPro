# emp_ind переедет в мкр-сервис employees_service.
# Связи is_active, login, emp_ind будут через REST,
# а не через ORM, поэтому убрал их из модели.
# Поля логин и email в модели избыточны, тк email и есть логин.
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(30), default="observer")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
