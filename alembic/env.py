from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models.base import Base

from app.models.user import User
from app.models.employee_info import EmployeeInfo
from app.models.training import Training
from app.models.statistics import Statistics
from app.models.admin import Admin
from app.models.observer import Observer
from app.models.department import Department
from app.models.association import observer_department, employee_department






config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),
                      target_metadata=target_metadata,
                      literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section),
                                     prefix='sqlalchemy.',
                                     poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()