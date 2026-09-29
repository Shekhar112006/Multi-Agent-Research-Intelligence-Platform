"""
API routes for knowledge graph operations.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.modules.knowledge_graph.schemas import (
    KnowledgeEdgeCreateRequest,
    KnowledgeNodeCreateRequest,
    KnowledgeNodeResponse,
)
from app.modules.knowledge_graph.services import KnowledgeGraphService


router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph"],
)


@router.post(
    "/nodes",
    response_model=KnowledgeNodeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_node(
    request: KnowledgeNodeCreateRequest,
    db: Session = Depends(get_db),
) -> KnowledgeNodeResponse:
    """
    Create or retrieve a knowledge graph node.
    """

    service = KnowledgeGraphService(db)

    node = service.get_or_create_node(
        node_type=request.node_type,
        label=request.label,
        entity_id=request.entity_id,
        properties=request.properties,
    )

    return node

@router.post(
    "/edges",
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_edge(
    request: KnowledgeEdgeCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Create or retrieve a knowledge graph relationship.
    """

    service = KnowledgeGraphService(db)

    return service.get_or_create_edge(
        source_node_id=request.source_node_id,
        target_node_id=request.target_node_id,
        relationship_type=request.relationship_type,
        evidence=request.evidence,
        confidence=request.confidence,
        source_paper_id=request.source_paper_id,
        properties=request.properties,
    )