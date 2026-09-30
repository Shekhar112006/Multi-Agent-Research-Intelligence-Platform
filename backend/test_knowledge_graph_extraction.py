"""
Manual test for AI knowledge graph extraction.
"""

from app.modules.knowledge_graph.services.knowledge_graph_extraction_service import (
    KnowledgeGraphExtractionService,
)


paper_context = """
The paper presents a Retrieval-Augmented Generation system for
knowledge-intensive natural language processing tasks.

The system uses dense retrieval to retrieve relevant passages
from an external knowledge source before generating an answer.

The experiments evaluate the system using Exact Match and
F1 metrics on the Natural Questions dataset.

The paper reports that retrieval provides useful external
knowledge to the language generation component.
"""


service = KnowledgeGraphExtractionService()

result = service.extract(paper_context)

print("\n=== EXTRACTED NODES ===")

for node in result.nodes:
    print(
        f"{node.node_type.value}: "
        f"{node.label}"
    )

print("\n=== EXTRACTED RELATIONSHIPS ===")

for relationship in result.relationships:
    print(
        f"{relationship.source_label}"
        f" --{relationship.relationship_type.value}--> "
        f"{relationship.target_label}"
    )

    print(
        f"Evidence: {relationship.evidence}"
    )

    print(
        f"Confidence: {relationship.confidence}"
    )

