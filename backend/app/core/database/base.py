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


# Import models ONLY AFTER Base exists.
from app.modules.users.models.users import User
from app.modules.projects.models.project import Project
from app.modules.papers.models.paper import Paper
from app.modules.paper_contents.models.paper_content import PaperContent
