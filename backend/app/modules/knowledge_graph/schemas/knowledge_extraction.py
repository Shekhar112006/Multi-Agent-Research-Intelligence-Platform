"""
Schemas for AI-driven knowledge graph extraction.
"""

import uuid

from pydantic import BaseModel, Field

from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeRelationshipType,
)
from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNodeType,
)


class ExtractedKnowledgeNode(BaseModel):
    """
    Represents a knowledge graph node extracted by the LLM.
    """

    node_type: KnowledgeNodeType = Field(
        ...,
        description="Type of knowledge graph entity.",
    )

    label: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable entity label.",
    )

    entity_id: uuid.UUID | None = Field(
        default=None,
        description="Existing MRIP entity ID when applicable.",
    )

    properties: dict = Field(
        default_factory=dict,
        description="Additional structured metadata.",
    )


class ExtractedKnowledgeRelationship(BaseModel):
    """
    Represents a relationship extracted by the LLM.
    """

    source_label: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Label of the source node.",
    )

    target_label: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Label of the target node.",
    )

    relationship_type: KnowledgeRelationshipType = Field(
        ...,
        description="Relationship connecting the two nodes.",
    )

    evidence: str = Field(
        ...,
        min_length=1,
        description="Evidence from the research paper.",
    )

    confidence: str = Field(
        ...,
        max_length=20,
        description="Confidence in the extracted relationship.",
    )

    properties: dict = Field(
        default_factory=dict,
        description="Additional relationship metadata.",
    )


class KnowledgeGraphExtractionResponse(BaseModel):
    """
    Complete structured result returned by the LLM.
    """

    nodes: list[ExtractedKnowledgeNode] = Field(
        default_factory=list,
        description="Knowledge graph nodes extracted from the paper.",
    )

    relationships: list[ExtractedKnowledgeRelationship] = Field(
        default_factory=list,
        description="Knowledge graph relationships extracted from the paper.",
    )