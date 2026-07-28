"""
Base class for all SQLAlchemy ORM models.

Every database model in the application must inherit from
this Base class so SQLAlchemy and Alembic can discover them.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """

    pass