"""
Database model for knowledge graph edges.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base


class KnowledgeRelationshipType(str, enum.Enum):
    """
    Supported relationships between knowledge graph nodes.
    """

    USES = "uses"
    STUDIES = "studies"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    EVALUATES_WITH = "evaluates_with"
    RELATED_TO = "related_to"


class KnowledgeEdge(Base):
    """
    Represents a relationship between two knowledge graph nodes.
    """

    __tablename__ = "knowledge_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    source_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_nodes.id", ondelete="CASCADE"),
        nullable=False,
    )

    target_node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_nodes.id", ondelete="CASCADE"),
        nullable=False,
    )

    relationship_type: Mapped[KnowledgeRelationshipType] = mapped_column(
        Enum(KnowledgeRelationshipType),
        nullable=False,
    )

    evidence: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    confidence: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    source_paper_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("papers.id", ondelete="SET NULL"),
        nullable=True,
    )

    properties: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_knowledge_edges_source_node_id",
            "source_node_id",
        ),
        Index(
            "ix_knowledge_edges_target_node_id",
            "target_node_id",
        ),
        Index(
            "ix_knowledge_edges_relationship_type",
            "relationship_type",
        ),
        Index(
            "ix_knowledge_edges_source_paper_id",
            "source_paper_id",
        ),
    )