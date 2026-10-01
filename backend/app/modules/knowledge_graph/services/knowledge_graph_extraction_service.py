"""
Service for AI-driven knowledge graph extraction.
"""

import json

from app.modules.generation.clients.ollama_client import OllamaClient
from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    ExtractedKnowledgeNode,
    ExtractedKnowledgeRelationship,
    KnowledgeGraphExtractionResponse,
)


class KnowledgeGraphExtractionService:
    """
    Uses an LLM to extract structured knowledge graph
    entities and relationships from research information.
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
        Extract knowledge graph nodes and relationships
        from the supplied research paper context.
        """

        prompt = self._build_prompt(paper_context)

        raw_response = self.ollama_client.generate(
            prompt=prompt,
            response_format="json",
        )

        try:
            result = json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Ollama returned invalid JSON for knowledge graph extraction."
            ) from exc

        result = self._remove_invalid_relationships(result)

        return KnowledgeGraphExtractionResponse.model_validate(result)

    def extract_in_batches(
        self,
        paper_title: str,
        paper_chunks: list[str],
        batch_size: int = 4,
    ) -> KnowledgeGraphExtractionResponse:
        """
        Extract knowledge graph information from paper chunks
        in smaller batches and merge the results.
        """

        if not paper_chunks:
            raise ValueError(
                "At least one paper chunk is required for extraction."
            )

        if batch_size < 1:
            raise ValueError(
                "Batch size must be at least 1."
            )

        all_nodes: list[ExtractedKnowledgeNode] = []
        all_relationships: list[ExtractedKnowledgeRelationship] = []

        for start in range(0, len(paper_chunks), batch_size):
            batch = paper_chunks[start:start + batch_size]

            batch_context = f"""
                Paper title:
                {paper_title}

                The following content belongs to this paper:

                {"\n\n".join(
                    f"[Chunk {start + index}]\n{chunk}"
                    for index, chunk in enumerate(batch)
                )}
                """.strip()

            result = self.extract(
                paper_context=batch_context,
            )

            all_nodes.extend(result.nodes)
            all_relationships.extend(result.relationships)

        merged_nodes = self._deduplicate_nodes(
            all_nodes,
        )

        merged_relationships = self._deduplicate_relationships(
            all_relationships,
        )

        return KnowledgeGraphExtractionResponse(
            nodes=merged_nodes,
            relationships=merged_relationships,
        )

    def _remove_invalid_relationships(
        self,
        result: dict,
    ) -> dict:
        """
        Remove relationships whose source or target node
        does not exist in the extracted node list.
        """

        nodes = result.get("nodes", [])
        relationships = result.get("relationships", [])

        node_labels = {
            node.get("label")
            for node in nodes
            if isinstance(node, dict)
            and isinstance(node.get("label"), str)
        }

        valid_relationships = []

        for relationship in relationships:
            if not isinstance(relationship, dict):
                continue

            source_label = relationship.get("source_label")
            target_label = relationship.get("target_label")

            if source_label not in node_labels:
                continue

            if target_label not in node_labels:
                continue

            valid_relationships.append(relationship)

        result["relationships"] = valid_relationships

        return result

    def _deduplicate_nodes(
        self,
        nodes: list[ExtractedKnowledgeNode],
    ) -> list[ExtractedKnowledgeNode]:
        """
        Remove duplicate nodes produced by different batches.
        """

        unique_nodes: dict[tuple[str, str], ExtractedKnowledgeNode] = {}

        for node in nodes:
            key = (
                node.node_type.value,
                node.label.strip().lower(),
            )

            if key not in unique_nodes:
                unique_nodes[key] = node

        return list(unique_nodes.values())

    def _deduplicate_relationships(
        self,
        relationships: list[ExtractedKnowledgeRelationship],
    ) -> list[ExtractedKnowledgeRelationship]:
        """
        Remove duplicate relationships produced by different batches.
        """

        unique_relationships: dict[
            tuple[str, str, str],
            ExtractedKnowledgeRelationship,
        ] = {}

        for relationship in relationships:
            key = (
                relationship.source_label.strip().lower(),
                relationship.target_label.strip().lower(),
                relationship.relationship_type.value,
            )

            if key not in unique_relationships:
                unique_relationships[key] = relationship

        return list(unique_relationships.values())

    def _build_prompt(
        self,
        paper_context: str,
    ) -> str:
        """
        Build a controlled extraction prompt for the LLM.
        """

        return f"""
You are a research knowledge graph extraction system.

Analyze the supplied research paper information and extract
only entities and relationships that are explicitly supported
by the provided information.

Allowed node types:
- paper
- claim
- method
- dataset
- metric
- topic

Allowed relationship types:
- uses
- studies
- supports
- contradicts
- evaluates_with
- related_to

IMPORTANT:
The relationship_type value MUST be exactly one of these strings:
"uses"
"studies"
"supports"
"contradicts"
"evaluates_with"
"related_to"

Do NOT use variations such as:
- evaluates
- evaluated_by
- evaluate
- assesses
- tests

If the paper evaluates a method using a dataset or metric,
use exactly "evaluates_with".

Rules:
1. Do not invent entities.
2. Do not invent relationships.

3. The paper title supplied in the context is the canonical
   label for the paper.

4. Never use generic labels such as "Paper" as a relationship
   endpoint. If referring to the paper, use its exact title.

5. Every relationship endpoint MUST exactly match one of the
   node labels returned in the nodes array.

6. Use concise, canonical labels.

7. Every relationship must include evidence from the context.

8. Use "contradicts" ONLY when two distinct research claims
   explicitly conflict with each other.

9. Do NOT use "contradicts" for:
   - a paper mentioning a problem
   - a paper reporting hallucinations
   - a paper criticizing a baseline
   - a negative result
   - a limitation
   - a topic being discussed

10. Every relationship must represent a meaningful semantic
    connection supported by the evidence.

11. Do not create a relationship merely because two entities
    appear in the same sentence.

12. If the evidence does not clearly support a relationship,
    omit the relationship.

13. A metric node should represent an evaluation metric,
    measurement, or performance criterion. Do not treat
    general phenomena such as "hallucinations" as a metric
    unless the context explicitly uses it as an evaluation
    measure.

14. Confidence must be one of:
    - high
    - medium
    - low

15. Return only valid JSON.

16. Follow exactly this structure:

{{
  "nodes": [
    {{
      "node_type": "method",
      "label": "Dense Retrieval",
      "entity_id": null,
      "properties": {{}}
    }}
  ],
  "relationships": [
    {{
      "source_label": "Paper",
      "target_label": "Dense Retrieval",
      "relationship_type": "uses",
      "evidence": "The paper uses dense retrieval.",
      "confidence": "high",
      "properties": {{}}
    }}
  ]
}}

Research paper information:

{paper_context}
"""