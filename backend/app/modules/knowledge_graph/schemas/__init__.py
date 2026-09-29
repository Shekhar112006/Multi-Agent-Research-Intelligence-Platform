"""
Schemas for knowledge graph API operations.
"""

from app.modules.knowledge_graph.schemas.knowledge_edge_request import (
    KnowledgeEdgeCreateRequest,
)
from app.modules.knowledge_graph.schemas.knowledge_node_request import (
    KnowledgeNodeCreateRequest,
)
from app.modules.knowledge_graph.schemas.knowledge_node_response import (
    KnowledgeNodeResponse,
)

__all__ = [
    "KnowledgeNodeCreateRequest",
    "KnowledgeNodeResponse",
    "KnowledgeEdgeCreateRequest",
]