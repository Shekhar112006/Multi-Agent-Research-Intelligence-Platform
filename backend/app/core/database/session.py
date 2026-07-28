"""
Database session management.

This module creates SQLAlchemy database sessions and provides
a FastAPI dependency for safely accessing the database.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.core.database.database import engine


# Create a factory for database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for a single request.

    A new session is created for every request and
    automatically closed after the request finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()