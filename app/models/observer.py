from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.association import observer_department

class Observer(Base):
    __tablename__ = "observers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
        comment = "Foreign key for table users",
    )

    user = relationship("User", back_populates="observer")

    departments = relationship(
        "Department",
        secondary=observer_department,
        back_populates="observers"
    )