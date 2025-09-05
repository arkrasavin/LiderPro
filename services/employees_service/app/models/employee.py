from sqlalchemy import Integer, String, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Employee(Base):
    __tablename__ = "employees_info"
    __table_args__ = (
        CheckConstraint("writeoff_points >= 0", name="ck_writeoff_points_nonneg"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    department: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    work_format: Mapped[str] = mapped_column(String(255), nullable=True)
    remote_city: Mapped[str] = mapped_column(String(255), nullable=True)
    emp_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    birthday: Mapped[Date | None] = mapped_column(Date, nullable=True)
    emp_ind: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # поля под минимальную аналитику
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    proactive_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    effective_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wallet_balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    writeoff_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
