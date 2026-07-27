"""
Database engine configuration.

This module creates the SQLAlchemy Engine.
The engine manages the connection pool to PostgreSQL.
"""

from sqlalchemy import create_engine

from app.core.config.settings import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)