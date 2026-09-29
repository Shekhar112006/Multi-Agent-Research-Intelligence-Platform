"""
Repositories for knowledge graph persistence.
"""

from app.modules.knowledge_graph.repositories.knowledge_edge_repository import (
    KnowledgeEdgeRepository,
)
from app.modules.knowledge_graph.repositories.knowledge_node_repository import (
    KnowledgeNodeRepository,
)

__all__ = [
    "KnowledgeEdgeRepository",
    "KnowledgeNodeRepository",
]