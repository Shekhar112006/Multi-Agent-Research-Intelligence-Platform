"""
Paper content model.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.modules.papers.models.paper import Paper


class PaperContent(Base, TimestampMixin):
    """
    Stores extracted text for a paper.
    """

    __tablename__ = "paper_contents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    paper_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id"),
        nullable=False,
        unique=True,
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    paper: Mapped["Paper"] = relationship(
        back_populates="content",
    )