"""
User database model.

This module defines the User ORM model that maps
to the users table in PostgreSQL.
"""

from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import relationship

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.modules.users.models.enums import UserRole

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.projects.models.project import Project
"""
User database model.

This module defines the User ORM model that maps
to the users table in PostgreSQL.
"""

from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.modules.users.models.enums import UserRole


from app.core.database.mixins.timestamp import TimestampMixin


class User(TimestampMixin, Base):
    """
    User database model.

    Represents an application user and stores
    authentication and authorization information.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            create_type=True,
        ),
        default=UserRole.RESEARCHER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    projects: Mapped[list["Project"]] = relationship(
    back_populates="owner",
    cascade="all, delete-orphan",
)