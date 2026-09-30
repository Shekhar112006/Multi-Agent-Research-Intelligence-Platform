"""
Service for AI-driven knowledge graph extraction.
"""

import json

from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    KnowledgeGraphExtractionResponse,
)
from app.modules.generation.clients.ollama_client import OllamaClient
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

        return KnowledgeGraphExtractionResponse.model_validate(result)

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

Rules:
1. Do not invent entities.
2. Do not invent relationships.
3. Use concise, canonical labels.
4. Every relationship must include evidence from the context.
5. Confidence must be one of:
   - high
   - medium
   - low
6. Return only valid JSON.
7. Follow exactly this structure:

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
