"""
Service for AI-driven knowledge graph extraction.

The service is intentionally optimized for local LLM inference.

Design:
    Paper chunks
        ↓
    LLM extracts relevant entities + minimal evidence
        ↓
    Pydantic validation
        ↓
    Python creates deterministic paper relationships
        ↓
    Deduplication
        ↓
    KnowledgeGraphExtractionResponse
"""

import json
import re

from app.modules.generation.clients.ollama_client import OllamaClient
from app.modules.knowledge_graph.models.knowledge_edge import (
    KnowledgeRelationshipType,
)
from app.modules.knowledge_graph.models.knowledge_node import (
    KnowledgeNodeType,
)
from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    ExtractedKnowledgeNode,
    ExtractedKnowledgeRelationship,
    KnowledgeConfidence,
    KnowledgeGraphExtractionResponse,
)


class KnowledgeGraphExtractionService:
    """
    Extract research entities from paper text and convert them
    into a deterministic knowledge graph structure.

    The LLM is responsible only for identifying entities and
    providing evidence.

    Python is responsible for creating predictable relationships.
    """

    def __init__(
        self,
        ollama_client: OllamaClient | None = None,
    ):
        """
        Initialize the extraction service.
        """

        self.ollama_client = (
            ollama_client
            if ollama_client is not None
            else OllamaClient()
        )

    def extract(
        self,
        paper_context: str,
    ) -> KnowledgeGraphExtractionResponse:
        """
        Extract entities and relationships from one supplied context.

        This method is kept for compatibility with existing callers.

        If the context contains a paper title, the LLM may return a
        paper node. Batch extraction uses a more optimized path.
        """

        if not paper_context or not paper_context.strip():
            raise ValueError("Paper context is required.")

        prompt = self._build_prompt(paper_context)

        raw_response = self.ollama_client.generate(
            prompt=prompt,
            response_format="json",
        )

        result = self._parse_response(raw_response)

        return self._validate_result(result)

    def extract_in_batches(
        self,
        paper_title: str,
        paper_chunks: list[str],
        batch_size: int = 2,
    ) -> KnowledgeGraphExtractionResponse:
        """
        Extract knowledge from paper chunks in small batches.

        The paper node is created deterministically by Python rather
        than asking the LLM to recreate it for every batch.

        Default batch size is intentionally small because local
        Ollama inference is the current bottleneck.
        """

        if not paper_title or not paper_title.strip():
            raise ValueError(
                "Paper title is required for knowledge graph extraction."
            )

        if not paper_chunks:
            raise ValueError(
                "At least one paper chunk is required for extraction."
            )

        if batch_size < 1:
            raise ValueError(
                "Batch size must be at least 1."
            )

        paper_title = paper_title.strip()

        all_nodes: list[ExtractedKnowledgeNode] = []

        for start in range(0, len(paper_chunks), batch_size):
            batch = paper_chunks[start:start + batch_size]

            cleaned_chunks = [
                chunk.strip()
                for chunk in batch
                if isinstance(chunk, str) and chunk.strip()
            ]

            if not cleaned_chunks:
                continue

            batch_text = "\n\n".join(
                f"[Chunk {start + index}]\n{chunk}"
                for index, chunk in enumerate(cleaned_chunks)
            )

            prompt = self._build_batch_prompt(
                paper_title=paper_title,
                batch_text=batch_text,
            )

            raw_response = self.ollama_client.generate(
                prompt=prompt,
                response_format="json",
            )

            result = self._parse_response(raw_response)

            batch_nodes = self._validate_nodes(
                result.get("nodes", [])
            )

            all_nodes.extend(batch_nodes)

        merged_nodes = self._deduplicate_nodes(all_nodes)

        paper_node = ExtractedKnowledgeNode(
            node_type=KnowledgeNodeType.PAPER,
            label=paper_title,
            entity_id=None,
            properties={},
        )

        final_nodes = [
            paper_node,
            *[
                node
                for node in merged_nodes
                if node.node_type != KnowledgeNodeType.PAPER
            ],
        ]

        relationships = self._build_paper_relationships(
            paper_title=paper_title,
            nodes=final_nodes,
        )

        relationships = self._deduplicate_relationships(
            relationships
        )

        return KnowledgeGraphExtractionResponse(
            nodes=final_nodes,
            relationships=relationships,
        )

    def _parse_response(
        self,
        raw_response: str,
    ) -> dict:
        """
        Parse and sanitize raw LLM JSON.
        """

        try:
            result = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Ollama returned invalid JSON for knowledge graph extraction."
            ) from exc

        if not isinstance(result, dict):
            raise ValueError(
                "Ollama returned an invalid knowledge graph response."
            )

        return result

    def _validate_result(
        self,
        result: dict,
    ) -> KnowledgeGraphExtractionResponse:
        """
        Validate a complete LLM-generated graph response.
        """

        nodes = self._validate_nodes(
            result.get("nodes", [])
        )

        relationships = self._validate_relationships(
            result.get("relationships", [])
        )

        valid_labels = {
            node.label.strip()
            for node in nodes
        }

        relationships = [
            relationship
            for relationship in relationships
            if relationship.source_label in valid_labels
            and relationship.target_label in valid_labels
        ]

        return KnowledgeGraphExtractionResponse(
            nodes=nodes,
            relationships=relationships,
        )

    def _validate_nodes(
        self,
        nodes: object,
    ) -> list[ExtractedKnowledgeNode]:
        """
        Sanitize and validate LLM-generated nodes.

        Invalid nodes are ignored instead of causing the entire
        extraction request to fail.
        """

        if not isinstance(nodes, list):
            return []

        validated_nodes: list[ExtractedKnowledgeNode] = []

        for node in nodes:
            if not isinstance(node, dict):
                continue

            label = node.get("label")

            if not isinstance(label, str):
                continue

            label = self._clean_label(label)

            if not label:
                continue

            node_type = node.get("node_type")

            if not isinstance(node_type, str):
                continue

            node_type = node_type.strip().lower()

            allowed_types = {
                item.value.lower(): item
                for item in KnowledgeNodeType
            }

            if node_type not in allowed_types:
                continue

            properties = node.get("properties")

            if not isinstance(properties, dict):
                properties = {}

            evidence = properties.get("evidence")

            if isinstance(evidence, str):
                evidence = self._clean_evidence(evidence)

                if evidence:
                    properties["evidence"] = evidence
                else:
                    properties.pop("evidence", None)

            relation = properties.get("relation")

            if isinstance(relation, str):
                properties["relation"] = relation.strip().lower()

            entity_id = node.get("entity_id")

            validated_nodes.append(
                ExtractedKnowledgeNode(
                    node_type=allowed_types[node_type],
                    label=label,
                    entity_id=entity_id,
                    properties=properties,
                )
            )

        return validated_nodes

    def _validate_relationships(
        self,
        relationships: object,
    ) -> list[ExtractedKnowledgeRelationship]:
        """
        Sanitize and validate LLM-generated relationships.
        """

        if not isinstance(relationships, list):
            return []

        validated_relationships: list[
            ExtractedKnowledgeRelationship
        ] = []

        for relationship in relationships:
            if not isinstance(relationship, dict):
                continue

            source_label = relationship.get("source_label")
            target_label = relationship.get("target_label")
            evidence = relationship.get("evidence")

            if not isinstance(source_label, str):
                continue

            if not isinstance(target_label, str):
                continue

            if not isinstance(evidence, str):
                continue

            source_label = self._clean_label(source_label)
            target_label = self._clean_label(target_label)
            evidence = self._clean_evidence(evidence)

            if not source_label:
                continue

            if not target_label:
                continue

            if not evidence:
                continue

            relationship_type = relationship.get(
                "relationship_type"
            )

            if not isinstance(relationship_type, str):
                continue

            relationship_type = relationship_type.strip().lower()

            allowed_relationships = {
                item.value.lower(): item
                for item in KnowledgeRelationshipType
            }

            if relationship_type not in allowed_relationships:
                continue

            confidence = relationship.get(
                "confidence",
                KnowledgeConfidence.MEDIUM.value,
            )

            if isinstance(confidence, str):
                confidence = confidence.strip().lower()

            allowed_confidence = {
                item.value.lower(): item
                for item in KnowledgeConfidence
            }

            if confidence not in allowed_confidence:
                confidence = KnowledgeConfidence.MEDIUM

            properties = relationship.get("properties")

            if not isinstance(properties, dict):
                properties = {}

            validated_relationships.append(
                ExtractedKnowledgeRelationship(
                    source_label=source_label,
                    target_label=target_label,
                    relationship_type=allowed_relationships[
                        relationship_type
                    ],
                    evidence=evidence,
                    confidence=allowed_confidence[confidence],
                    properties=properties,
                )
            )

        return validated_relationships

    def _build_paper_relationships(
        self,
        paper_title: str,
        nodes: list[ExtractedKnowledgeNode],
    ) -> list[ExtractedKnowledgeRelationship]:
        """
        Create deterministic Paper → Entity relationships.

        The LLM does not need to generate these predictable edges.
        """

        relationships: list[
            ExtractedKnowledgeRelationship
        ] = []

        for node in nodes:
            if node.node_type == KnowledgeNodeType.PAPER:
                continue

            relation_type = self._relationship_for_node(node)

            if relation_type is None:
                continue

            evidence = node.properties.get("evidence")

            if not isinstance(evidence, str) or not evidence.strip():
                evidence = (
                    f"{node.label} is identified in the supplied "
                    f"research paper content."
                )

            confidence = self._confidence_for_node(node)

            relationships.append(
                ExtractedKnowledgeRelationship(
                    source_label=paper_title,
                    target_label=node.label,
                    relationship_type=relation_type,
                    evidence=evidence,
                    confidence=confidence,
                    properties={},
                )
            )

        return relationships

    def _relationship_for_node(
        self,
        node: ExtractedKnowledgeNode,
    ) -> KnowledgeRelationshipType | None:
        """
        Map node type to its deterministic paper relationship.
        """

        mapping = {
            KnowledgeNodeType.METHOD: (
                KnowledgeRelationshipType.USES
            ),
            KnowledgeNodeType.DATASET: (
                KnowledgeRelationshipType.EVALUATES_WITH
            ),
            KnowledgeNodeType.METRIC: (
                KnowledgeRelationshipType.EVALUATES_WITH
            ),
            KnowledgeNodeType.TOPIC: (
                KnowledgeRelationshipType.RELATED_TO
            ),
            KnowledgeNodeType.CLAIM: (
                KnowledgeRelationshipType.SUPPORTS
            ),
        }

        if node.node_type == KnowledgeNodeType.DATASET:
            relation = node.properties.get("relation")

            if relation == "studies":
                return KnowledgeRelationshipType.STUDIES

            return KnowledgeRelationshipType.EVALUATES_WITH

        return mapping.get(node.node_type)

    def _confidence_for_node(
        self,
        node: ExtractedKnowledgeNode,
    ) -> KnowledgeConfidence:
        """
        Convert optional node confidence into the graph confidence enum.
        """

        confidence = node.properties.get("confidence")

        if isinstance(confidence, str):
            confidence = confidence.strip().lower()

            for item in KnowledgeConfidence:
                if item.value == confidence:
                    return item

        return KnowledgeConfidence.MEDIUM

    def _deduplicate_nodes(
        self,
        nodes: list[ExtractedKnowledgeNode],
    ) -> list[ExtractedKnowledgeNode]:
        """
        Remove duplicate nodes across chunks.

        Node identity is based on node type + normalized label.
        """

        unique_nodes: dict[
            tuple[str, str],
            ExtractedKnowledgeNode,
        ] = {}

        for node in nodes:
            normalized_label = self._normalize_label(
                node.label
            )

            key = (
                node.node_type.value,
                normalized_label,
            )

            if key not in unique_nodes:
                unique_nodes[key] = node
                continue

            existing = unique_nodes[key]

            merged_properties = dict(
                existing.properties
            )

            for key_name, value in node.properties.items():
                if key_name not in merged_properties:
                    merged_properties[key_name] = value

            if (
                not merged_properties.get("evidence")
                and node.properties.get("evidence")
            ):
                merged_properties["evidence"] = (
                    node.properties["evidence"]
                )

            unique_nodes[key] = ExtractedKnowledgeNode(
                node_type=existing.node_type,
                label=existing.label,
                entity_id=(
                    existing.entity_id
                    or node.entity_id
                ),
                properties=merged_properties,
            )

        return list(unique_nodes.values())

    def _deduplicate_relationships(
        self,
        relationships: list[
            ExtractedKnowledgeRelationship
        ],
    ) -> list[ExtractedKnowledgeRelationship]:
        """
        Remove duplicate relationships.

        Evidence from the first occurrence is retained.
        """

        unique_relationships: dict[
            tuple[str, str, str],
            ExtractedKnowledgeRelationship,
        ] = {}

        for relationship in relationships:
            key = (
                self._normalize_label(
                    relationship.source_label
                ),
                self._normalize_label(
                    relationship.target_label
                ),
                relationship.relationship_type.value,
            )

            if key not in unique_relationships:
                unique_relationships[key] = relationship

        return list(unique_relationships.values())

    def _clean_label(
        self,
        label: str,
    ) -> str:
        """
        Normalize an entity label without changing its meaning.
        """

        label = re.sub(
            r"\s+",
            " ",
            label,
        )

        label = label.strip(
            " \t\n\r\"'`.,:;|-"
        )

        return label

    def _clean_evidence(
        self,
        evidence: str,
    ) -> str:
        """
        Normalize evidence text.
        """

        evidence = re.sub(
            r"\s+",
            " ",
            evidence,
        )

        return evidence.strip()

    def _normalize_label(
        self,
        label: str,
    ) -> str:
        """
        Normalize labels for duplicate comparison.
        """

        return re.sub(
            r"\s+",
            " ",
            label.strip().lower(),
        )

    def _build_batch_prompt(
        self,
        paper_title: str,
        batch_text: str,
    ) -> str:
        """
        Build the optimized prompt used for batch extraction.

        Important:
        The model does NOT create the paper node.
        Python creates it deterministically.
        """

        return f"""
You are a research knowledge extraction system.

Extract ONLY entities explicitly supported by the supplied text.

DO NOT summarize the paper.
DO NOT explain your reasoning.
DO NOT create a paper node.
DO NOT create relationships.
DO NOT invent information.

Extract these node types only:

1. method
Named methods, models, algorithms, frameworks, or techniques
actually used, implemented, applied, or evaluated.

2. dataset
Named datasets actually used in experiments or research.

For datasets, set:
"relation": "evaluates_with"
when used for evaluation/experiments.

Set:
"relation": "studies"
when the dataset itself is the research subject.

Do not extract generic tasks as datasets.

3. metric
Specific measurable evaluation metrics.

Examples:
Exact Match
F1
Accuracy
Precision
Recall
BLEU
ROUGE
MRR
NDCG
MAP
Perplexity

Do not create vague metrics such as:
performance
better results
state-of-the-art
quality

4. topic
Meaningful research areas or subjects explicitly supported
by the text.

5. claim
Only meaningful research claims that are directly supported
by the supplied text.

For every extracted node:

- label must be concise
- evidence must be short
- evidence must be directly supported by the supplied text
- confidence must be high, medium, or low
- omit uncertain entities

Use this exact JSON format:

{{
  "nodes": [
    {{
      "node_type": "method",
      "label": "RAG",
      "entity_id": null,
      "properties": {{
        "evidence": "The text states that RAG is used.",
        "confidence": "high"
      }}
    }}
  ]
}}

If nothing useful is present:

{{
  "nodes": []
}}

IMPORTANT:
Return ONLY JSON.
Do not return markdown.
Do not return explanations.
Do not create relationships.

PAPER TITLE:
{paper_title}

PAPER CONTENT:
{batch_text}
""".strip()

    def _build_prompt(
        self,
        paper_context: str,
    ) -> str:
        """
        Build a compatibility prompt for direct extraction.

        This method is retained for existing callers that use extract().
        """

        return f"""
You are extracting structured research knowledge.

Extract ONLY information explicitly supported by the supplied text.

Allowed node types:
paper, method, dataset, metric, topic, claim

Allowed relationships:
uses, studies, supports, evaluates_with, related_to, contradicts

Rules:

- Create exactly one paper node using the supplied paper title.
- Extract named methods actually used by the paper.
- Extract named datasets actually used.
- Extract specific evaluation metrics.
- Extract meaningful research topics.
- Extract meaningful claims only when supported by evidence.
- Use contradictions only for explicit conflicting claims.
- Never invent information.
- Every relationship requires evidence.
- Every relationship endpoint must exactly match a node label.
- Omit uncertain information.

Return ONLY JSON.

Format:

{{
  "nodes": [
    {{
      "node_type": "paper",
      "label": "EXACT PAPER TITLE",
      "entity_id": null,
      "properties": {{}}
    }}
  ],
  "relationships": []
}}

If nothing useful can be extracted:

{{
  "nodes": [],
  "relationships": []
}}

PAPER CONTENT:
{paper_context}
""".strip()