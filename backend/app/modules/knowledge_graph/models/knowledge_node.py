"""
Database model for knowledge graph nodes.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Index, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base


class KnowledgeNodeType(str, enum.Enum):
    """
    Supported knowledge graph node types.
    """

    PAPER = "paper"
    CLAIM = "claim"
    METHOD = "method"
    DATASET = "dataset"
    METRIC = "metric"
    TOPIC = "topic"


class KnowledgeNode(Base):
    """
    Represents an entity inside the research knowledge graph.
    """

    __tablename__ = "knowledge_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    node_type: Mapped[KnowledgeNodeType] = mapped_column(
        Enum(KnowledgeNodeType),
        nullable=False,
    )

    entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    label: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
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
            "ix_knowledge_nodes_node_type",
            "node_type",
        ),
        Index(
            "ix_knowledge_nodes_entity_id",
            "entity_id",
        ),
    )