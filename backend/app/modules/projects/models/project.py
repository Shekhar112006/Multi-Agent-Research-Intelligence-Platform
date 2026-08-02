"""
Project database model.
"""

import uuid
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database.mixins.timestamp import TimestampMixin
from app.core.database.base import Base
from app.modules.projects.models.project_status import ProjectStatus
from typing import TYPE_CHECKING


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.papers.models.paper import Paper

if TYPE_CHECKING:
    from app.modules.users.models.users import User

class Project(TimestampMixin,Base):
    """
    Database model for research projects.
    """

    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
)

    owner_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id"),
    nullable=False,
)

    name: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
)

    description: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
)

    status: Mapped[ProjectStatus] = mapped_column(
    Enum(
        ProjectStatus,
        name="project_status",
    ),
    default=ProjectStatus.ACTIVE,
    nullable=False,
)

    owner: Mapped["User"] = relationship(
    back_populates="projects",
)

    papers: Mapped[list["Paper"]] = relationship(
    back_populates="project",
    cascade="all, delete-orphan",
)