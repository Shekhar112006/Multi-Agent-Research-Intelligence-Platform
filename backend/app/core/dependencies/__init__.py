"""
Database dependencies.

This module contains reusable FastAPI dependencies.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for each request.

    The session is automatically closed after
    the request finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()