"""
API routes for knowledge graph operations.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.modules.knowledge_graph.schemas import (
    KnowledgeEdgeCreateRequest,
    KnowledgeNodeCreateRequest,
    KnowledgeNodeResponse,
)
from app.modules.knowledge_graph.services import KnowledgeGraphService
from app.modules.knowledge_graph.services import (
    KnowledgeContextService,
    KnowledgeGraphService,
)
from app.modules.knowledge_graph.services.knowledge_graph_extraction_service import (
    KnowledgeGraphExtractionService,
)

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

@router.post(
    "/papers/{paper_id}/extract",
    status_code=status.HTTP_201_CREATED,
)
def extract_paper_knowledge_graph(
    paper_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """
    Extract and persist a knowledge graph from a research paper.
    """

    context_service = KnowledgeContextService(db)
    extraction_service = KnowledgeGraphExtractionService()
    graph_service = KnowledgeGraphService(db)

    try:
        paper_context = context_service.build_paper_context(
            paper_id=paper_id,
        )

        extraction = extraction_service.extract(
            paper_context=paper_context,
        )

        nodes, edges = graph_service.persist_extraction(
            extraction=extraction,
            source_paper_id=paper_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return {
        "paper_id": paper_id,
        "nodes_created": len(nodes),
        "edges_created": len(edges),
        "nodes": nodes,
        "edges": edges,
    }