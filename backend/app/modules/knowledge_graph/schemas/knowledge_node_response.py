"""
Response schema for knowledge graph nodes.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNodeType,
)


class KnowledgeNodeResponse(BaseModel):
    """
    Represents a knowledge graph node returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    node_type: KnowledgeNodeType
    entity_id: uuid.UUID | None
    label: str
    properties: dict
    created_at: datetime
    updated_at: datetime