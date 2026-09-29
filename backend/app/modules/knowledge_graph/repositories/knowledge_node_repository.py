"""
Repository for knowledge graph node persistence.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNode,
    KnowledgeNodeType,
)


class KnowledgeNodeRepository:
    """
    Handles database operations for knowledge graph nodes.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        node_type: KnowledgeNodeType,
        label: str,
        entity_id: uuid.UUID | None = None,
        properties: dict | None = None,
    ) -> KnowledgeNode:
        """
        Create and persist a knowledge graph node.
        """

        node = KnowledgeNode(
            node_type=node_type,
            entity_id=entity_id,
            label=label,
            properties=properties or {},
        )

        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)

        return node

    def get_by_id(
        self,
        node_id: uuid.UUID,
    ) -> KnowledgeNode | None:
        """
        Retrieve a knowledge graph node by its ID.
        """

        statement = select(KnowledgeNode).where(
            KnowledgeNode.id == node_id
        )

        return self.db.scalar(statement)

    def get_by_entity(
        self,
        node_type: KnowledgeNodeType,
        entity_id: uuid.UUID,
    ) -> KnowledgeNode | None:
        """
        Retrieve a graph node linked to an existing MRIP entity.
        """

        statement = select(KnowledgeNode).where(
            KnowledgeNode.node_type == node_type,
            KnowledgeNode.entity_id == entity_id,
        )

        return self.db.scalar(statement)

    def get_by_label(
        self,
        node_type: KnowledgeNodeType,
        label: str,
    ) -> KnowledgeNode | None:
        """
        Retrieve a graph node by type and label.
        """

        statement = select(KnowledgeNode).where(
            KnowledgeNode.node_type == node_type,
            KnowledgeNode.label == label,
        )

        return self.db.scalar(statement)