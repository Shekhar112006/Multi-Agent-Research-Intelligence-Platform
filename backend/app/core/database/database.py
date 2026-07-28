"""
Database configuration.

This module creates the SQLAlchemy Engine,
Session factory, and Declarative Base.

Every database operation in the application
will use the SessionLocal factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config.settings import settings


engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """

    pass