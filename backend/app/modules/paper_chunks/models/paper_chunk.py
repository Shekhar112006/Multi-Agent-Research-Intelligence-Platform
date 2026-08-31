"""
Paper chunk model.
"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base
from app.core.database.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.modules.papers.models.paper import Paper


class PaperChunk(Base, TimestampMixin):
    """
    Stores one chunk of a paper.
    """

    __tablename__ = "paper_chunks"

    __table_args__ = (
        UniqueConstraint(
            "paper_id",
            "chunk_index",
            name="uq_paper_chunks_paper_id_chunk_index",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    paper_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id"),
        nullable=False,
    )

    paper: Mapped["Paper"] = relationship()

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )