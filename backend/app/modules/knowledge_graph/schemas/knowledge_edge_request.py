"""
Request schema for creating knowledge graph relationships.
"""

import uuid

from pydantic import BaseModel, Field

from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeRelationshipType,
)


class KnowledgeEdgeCreateRequest(BaseModel):
    """
    Defines the data required to create a knowledge graph relationship.
    """

    source_node_id: uuid.UUID = Field(
        ...,
        description="ID of the source knowledge graph node.",
    )

    target_node_id: uuid.UUID = Field(
        ...,
        description="ID of the target knowledge graph node.",
    )

    relationship_type: KnowledgeRelationshipType = Field(
        ...,
        description="Type of relationship between the two nodes.",
    )

    evidence: str | None = Field(
        default=None,
        description="Evidence supporting the relationship.",
    )

    confidence: str | None = Field(
        default=None,
        max_length=20,
        description="Confidence level of the relationship.",
    )

    source_paper_id: uuid.UUID | None = Field(
        default=None,
        description="Paper that provides provenance for the relationship.",
    )

    properties: dict = Field(
        default_factory=dict,
        description="Additional structured metadata for the relationship.",
    )