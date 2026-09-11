"""
Paper database model.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String , Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database.mixins.timestamp import TimestampMixin

from app.core.database.base import Base
from app.modules.papers.models.upload_status import UploadStatus

if TYPE_CHECKING:
    from app.modules.projects.models.project import Project
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.paper_contents.models.paper_content import PaperContent



class Paper(TimestampMixin , Base):
    """
    Database model for uploaded research papers.
    """

    __tablename__ = "papers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    semantic_scholar_id: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    abstract: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    authors: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    publication_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    citation_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    pdf_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    upload_status: Mapped[UploadStatus] = mapped_column(
        Enum(UploadStatus),
        default=UploadStatus.UPLOADED,
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="papers",
    )

    content: Mapped["PaperContent"] = relationship(
        back_populates="paper",
        uselist=False,
        cascade="all, delete-orphan",
    )