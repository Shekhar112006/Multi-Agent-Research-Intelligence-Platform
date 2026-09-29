
"""
Repository for knowledge graph edge persistence.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeEdge,
    KnowledgeRelationshipType,
)


class KnowledgeEdgeRepository:
    """
    Handles database operations for knowledge graph edges.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        source_node_id: uuid.UUID,
        target_node_id: uuid.UUID,
        relationship_type: KnowledgeRelationshipType,
        evidence: str | None = None,
        confidence: str | None = None,
        source_paper_id: uuid.UUID | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create and persist a knowledge graph relationship.
        """

        edge = KnowledgeEdge(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship_type=relationship_type,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=source_paper_id,
            properties=properties or {},
        )

        self.db.add(edge)
        self.db.commit()
        self.db.refresh(edge)

        return edge

    def get_by_id(
        self,
        edge_id: uuid.UUID,
    ) -> KnowledgeEdge | None:
        """
        Retrieve a knowledge graph edge by ID.
        """

        statement = select(KnowledgeEdge).where(
            KnowledgeEdge.id == edge_id
        )

        return self.db.scalar(statement)

    def get_existing(
        self,
        source_node_id: uuid.UUID,
        target_node_id: uuid.UUID,
        relationship_type: KnowledgeRelationshipType,
    ) -> KnowledgeEdge | None:
        """
        Find an existing relationship between two nodes.
        """

        statement = select(KnowledgeEdge).where(
            KnowledgeEdge.source_node_id == source_node_id,
            KnowledgeEdge.target_node_id == target_node_id,
            KnowledgeEdge.relationship_type == relationship_type,
        )

        return self.db.scalar(statement)

    def get_outgoing(
        self,
        source_node_id: uuid.UUID,
    ) -> list[KnowledgeEdge]:
        """
        Retrieve all relationships originating from a node.
        """

        statement = select(KnowledgeEdge).where(
            KnowledgeEdge.source_node_id == source_node_id
        )

        return list(self.db.scalars(statement).all())

    def get_incoming(
        self,
        target_node_id: uuid.UUID,
    ) -> list[KnowledgeEdge]:
        """
        Retrieve all relationships pointing to a node.
        """

        statement = select(KnowledgeEdge).where(
            KnowledgeEdge.target_node_id == target_node_id
        )

        return list(self.db.scalars(statement).all())
