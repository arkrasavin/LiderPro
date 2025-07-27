from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    mentee_number = Column(Integer, nullable=True)
    mentee_points = Column(Integer, nullable=True)
    curator_training_date = Column(Date, nullable=True)
    training_format = Column(String, nullable=True)
    conference_presence = Column(Boolean, nullable=True, default=False)
    certification = Column(Boolean, nullable=True, default=False)
    introductory_conf_points = Column(Integer, nullable=True)
    training_presence1_date = Column(Date, nullable=True)
    training_points1 = Column(Integer, nullable=True)
    training_presence2_date = Column(Date, nullable=True)
    training_points2 = Column(Integer, nullable=True)
    training_presence3_date = Column(Date, nullable=True)
    training_points3 = Column(Integer, nullable=True)
    training_presence4_date = Column(Date, nullable=True)
    training_points4 = Column(Integer, nullable=True)
    training_presence5_date = Column(Date, nullable=True)
    training_points5 = Column(Integer, nullable=True)
    training_presence6_date = Column(Date, nullable=True)
    training_points6 = Column(Integer, nullable=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees_info.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment = "Foreign key for table employees_info",
    )

    employee = relationship("EmployeeInfo", back_populates="training")
