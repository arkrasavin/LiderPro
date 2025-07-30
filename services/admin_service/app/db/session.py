from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import get_settings

engine = create_engine(str(get_settings().database_url), echo=False, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)
