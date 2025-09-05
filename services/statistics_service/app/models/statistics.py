# !!! модель недоделана, обозначены лишь названия колонок в db.
from sqlalchemy import Column

from .base import Base


class Statistics(Base):
    __tablename__ = "statistics"
    __table_args__ = {"engine": "MergeTree ORDER BY employee_id"}

    employee_id = Column(primary_key=True)
    raiting_overall = Column()
    points_sum = Column()
    raiting_efficiency = Column()
    points_efficiency = Column()
    raiting_proactive = Column()
    points_proactive = Column()
