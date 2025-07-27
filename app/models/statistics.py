from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    raiting_overall = Column(Integer, nullable=True)
    points_sum = Column(Integer, nullable=True)
    raiting_efficiency = Column(Integer, nullable=True)
    points_efficiency = Column(Integer, nullable=True)
    raiting_proactive = Column(Integer, nullable=True)
    points_proactive = Column(Integer, nullable=True)
    ewallet = Column(Integer, nullable=True)
    lavka_exchange = Column(Integer, nullable=True)
    lavka_exchange_name = Column(Integer, nullable=True)
    lavka_exchange_points = Column(Integer, nullable=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees_info.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment = "Foreign key for table employees_info",
    )

    employee = relationship("EmployeeInfo", back_populates="statistics")
