"""
Request schema for creating knowledge graph nodes.
"""

import uuid

from pydantic import BaseModel, Field

from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNodeType,
)


class KnowledgeNodeCreateRequest(BaseModel):
    """
    Defines the data required to create a knowledge graph node.
    """

    node_type: KnowledgeNodeType = Field(
        ...,
        description="Type of entity represented by the graph node.",
    )

    label: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable label for the graph node.",
    )

    entity_id: uuid.UUID | None = Field(
        default=None,
        description="ID of the existing MRIP entity represented by this node.",
    )

    properties: dict = Field(
        default_factory=dict,
        description="Additional structured metadata for the node.",
    )