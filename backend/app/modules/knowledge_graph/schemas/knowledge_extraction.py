"""
Schemas for AI-driven knowledge graph extraction.
"""

import uuid

from pydantic import BaseModel, Field, model_validator

from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeRelationshipType,
)
from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNodeType,
)
import enum


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

class KnowledgeConfidence(str, enum.Enum):
    """
    Supported confidence levels for extracted relationships.
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


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

    confidence: KnowledgeConfidence = Field(
        ...,
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

    @model_validator(mode="after")
    def validate_relationship_endpoints(self):
        """
        Ensure every relationship references an extracted node.
        """

        node_labels = {
            node.label
            for node in self.nodes
        }

        for relationship in self.relationships:
            if relationship.source_label not in node_labels:
                raise ValueError(
                    f"Relationship source node does not exist: "
                    f"{relationship.source_label}"
                )

            if relationship.target_label not in node_labels:
                raise ValueError(
                    f"Relationship target node does not exist: "
                    f"{relationship.target_label}"
                )

        return self