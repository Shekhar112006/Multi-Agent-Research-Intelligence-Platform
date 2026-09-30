
"""
Service layer for knowledge graph operations.
"""

import uuid

from sqlalchemy.orm import Session

from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeEdge,
    KnowledgeRelationshipType,
)
from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNode,
    KnowledgeNodeType,
)
from app.modules.knowledge_graph.repositories.knowledge_edge_repository import (
    KnowledgeEdgeRepository,
)
from app.modules.knowledge_graph.repositories.knowledge_node_repository import (
    KnowledgeNodeRepository,
)
from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    KnowledgeGraphExtractionResponse,
)


class KnowledgeGraphService:
    """
    Provides business logic for building and querying the
    research knowledge graph.
    """

    def __init__(self, db: Session):
        """
        Initialize the knowledge graph service.
        """

        self.node_repository = KnowledgeNodeRepository(db)
        self.edge_repository = KnowledgeEdgeRepository(db)

    def get_or_create_node(
        self,
        node_type: KnowledgeNodeType,
        label: str,
        entity_id: uuid.UUID | None = None,
        properties: dict | None = None,
    ) -> KnowledgeNode:
        """
        Retrieve an existing graph node or create a new one.
        """

        existing_node = None

        if entity_id is not None:
            existing_node = self.node_repository.get_by_entity(
                node_type=node_type,
                entity_id=entity_id,
            )

        if existing_node is None:
            existing_node = self.node_repository.get_by_label(
                node_type=node_type,
                label=label,
            )

        if existing_node is not None:
            return existing_node

        return self.node_repository.create(
            node_type=node_type,
            label=label,
            entity_id=entity_id,
            properties=properties,
        )

    def get_or_create_edge(
        self,
        source_node_id: uuid.UUID,
        target_node_id: uuid.UUID,
        relationship_type: KnowledgeRelationshipType,
        evidence: str | None = None,
        confidence: str | None = None,
        source_paper_id: uuid.UUID | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Retrieve an existing graph relationship or create a new one.
        """

        existing_edge = self.edge_repository.get_existing(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship_type=relationship_type,
        )

        if existing_edge is not None:
            return existing_edge

        return self.edge_repository.create(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relationship_type=relationship_type,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=source_paper_id,
            properties=properties,
        )

    def add_paper_method_relationship(
        self,
        paper_id: uuid.UUID,
        method_label: str,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create a USES relationship between a paper and a method.
        """

        paper_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.PAPER,
            label=f"Paper {paper_id}",
            entity_id=paper_id,
        )

        method_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.METHOD,
            label=method_label,
            properties=properties,
        )

        return self.get_or_create_edge(
            source_node_id=paper_node.id,
            target_node_id=method_node.id,
            relationship_type=KnowledgeRelationshipType.USES,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_id,
        )

    def add_paper_dataset_relationship(
        self,
        paper_id: uuid.UUID,
        dataset_label: str,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create a STUDIES relationship between a paper and a dataset.
        """

        paper_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.PAPER,
            label=f"Paper {paper_id}",
            entity_id=paper_id,
        )

        dataset_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.DATASET,
            label=dataset_label,
            properties=properties,
        )

        return self.get_or_create_edge(
            source_node_id=paper_node.id,
            target_node_id=dataset_node.id,
            relationship_type=KnowledgeRelationshipType.STUDIES,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_id,
        )

    def add_paper_metric_relationship(
        self,
        paper_id: uuid.UUID,
        metric_label: str,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create an EVALUATES_WITH relationship between a paper and a metric.
        """

        paper_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.PAPER,
            label=f"Paper {paper_id}",
            entity_id=paper_id,
        )

        metric_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.METRIC,
            label=metric_label,
            properties=properties,
        )

        return self.get_or_create_edge(
            source_node_id=paper_node.id,
            target_node_id=metric_node.id,
            relationship_type=KnowledgeRelationshipType.EVALUATES_WITH,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_id,
        )

    def add_paper_topic_relationship(
        self,
        paper_id: uuid.UUID,
        topic_label: str,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create a RELATED_TO relationship between a paper and a topic.
        """

        paper_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.PAPER,
            label=f"Paper {paper_id}",
            entity_id=paper_id,
        )

        topic_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.TOPIC,
            label=topic_label,
            properties=properties,
        )

        return self.get_or_create_edge(
            source_node_id=paper_node.id,
            target_node_id=topic_node.id,
            relationship_type=KnowledgeRelationshipType.RELATED_TO,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_id,
        )

    def add_paper_claim_relationship(
        self,
        paper_id: uuid.UUID,
        claim_id: uuid.UUID,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create a SUPPORTS relationship between a paper and a claim.
        """

        paper_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.PAPER,
            label=f"Paper {paper_id}",
            entity_id=paper_id,
        )

        claim_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.CLAIM,
            label=f"Claim {claim_id}",
            entity_id=claim_id,
            properties=properties,
        )

        return self.get_or_create_edge(
            source_node_id=paper_node.id,
            target_node_id=claim_node.id,
            relationship_type=KnowledgeRelationshipType.SUPPORTS,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_id,
        )
    
    def add_claim_contradiction_relationship(
        self,
        claim_a_id: uuid.UUID,
        claim_b_id: uuid.UUID,
        paper_a_id: uuid.UUID | None = None,
        evidence: str | None = None,
        confidence: str | None = None,
        properties: dict | None = None,
    ) -> KnowledgeEdge:
        """
        Create a CONTRADICTS relationship between two claims.
        """

        claim_a_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.CLAIM,
            label=f"Claim {claim_a_id}",
            entity_id=claim_a_id,
        )

        claim_b_node = self.get_or_create_node(
            node_type=KnowledgeNodeType.CLAIM,
            label=f"Claim {claim_b_id}",
            entity_id=claim_b_id,
        )

        return self.get_or_create_edge(
            source_node_id=claim_a_node.id,
            target_node_id=claim_b_node.id,
            relationship_type=KnowledgeRelationshipType.CONTRADICTS,
            evidence=evidence,
            confidence=confidence,
            source_paper_id=paper_a_id,
            properties=properties,
        )

    def persist_extraction(
        self,
        extraction: KnowledgeGraphExtractionResponse,
        source_paper_id: uuid.UUID | None = None,
    ) -> tuple[list[KnowledgeNode], list[KnowledgeEdge]]:
        """
        Persist an AI-generated knowledge graph extraction.

        Creates or reuses nodes first, then resolves relationship
        labels to node IDs before creating or reusing edges.
        """

        node_map: dict[str, KnowledgeNode] = {}

        for extracted_node in extraction.nodes:
            node = self.get_or_create_node(
                node_type=extracted_node.node_type,
                label=extracted_node.label,
                entity_id=extracted_node.entity_id,
                properties=extracted_node.properties,
            )

            node_map[extracted_node.label] = node

        persisted_edges: list[KnowledgeEdge] = []

        for relationship in extraction.relationships:
            source_node = node_map.get(
                relationship.source_label
            )
            target_node = node_map.get(
                relationship.target_label
            )

            if source_node is None or target_node is None:
                continue

            edge = self.get_or_create_edge(
                source_node_id=source_node.id,
                target_node_id=target_node.id,
                relationship_type=relationship.relationship_type,
                evidence=relationship.evidence,
                confidence=relationship.confidence,
                source_paper_id=source_paper_id,
                properties=relationship.properties,
            )

            persisted_edges.append(edge)

        return list(node_map.values()), persisted_edges
