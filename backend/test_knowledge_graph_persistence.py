"""
Manual integration test for knowledge graph extraction and persistence.
"""
import app.core.database.models
import uuid

from app.core.database.session import SessionLocal
from app.modules.knowledge_graph.services.knowledge_graph_extraction_service import (
    KnowledgeGraphExtractionService,
)
from app.modules.knowledge_graph.services.knowledge_graph_service import (
    KnowledgeGraphService,
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


def main() -> None:
    """
    Extract knowledge and persist it into PostgreSQL.
    """

    extraction_service = KnowledgeGraphExtractionService()

    extraction = extraction_service.extract(
        paper_context
    )

    db = SessionLocal()

    try:
        graph_service = KnowledgeGraphService(db)

        paper_id = None

        nodes, edges = graph_service.persist_extraction(
            extraction=extraction,
            source_paper_id=paper_id,
        )

        print("\n=== PERSISTED NODES ===")

        for node in nodes:
            print(
                f"{node.node_type.value}: "
                f"{node.label} "
                f"-> {node.id}"
            )

        print("\n=== PERSISTED EDGES ===")

        for edge in edges:
            print(
                f"{edge.relationship_type.value}: "
                f"{edge.source_node_id} "
                f"-> "
                f"{edge.target_node_id}"
            )

        print(
            f"\nTotal nodes: {len(nodes)}"
        )

        print(
            f"Total edges: {len(edges)}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()
