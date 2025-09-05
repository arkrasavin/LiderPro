from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Observer(Base):
    __tablename__ = "observers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
