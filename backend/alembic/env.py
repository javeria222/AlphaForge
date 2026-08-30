"""Alembic configuration and initialization"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    pass

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    pass

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
