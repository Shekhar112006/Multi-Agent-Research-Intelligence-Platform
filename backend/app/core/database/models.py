"""
Registers all SQLAlchemy models.

Importing this module ensures every ORM model is
registered with Base.metadata.
"""

from app.modules.projects.models.project import Project
from app.modules.users.models.users import User

__all__ = [
    "User",
    "Project",
]