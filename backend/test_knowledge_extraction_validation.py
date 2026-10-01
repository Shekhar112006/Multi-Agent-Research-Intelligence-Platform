"""
Validation test for knowledge graph extraction schemas.
"""

from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    ExtractedKnowledgeRelationship,
)


def main() -> None:
    """
    Verify that invalid confidence values are rejected.
    """

    try:
        ExtractedKnowledgeRelationship(
            source_label="Paper",
            target_label="Dense Retrieval",
            relationship_type="uses",
            evidence="The paper uses dense retrieval.",
            confidence="banana",
        )

    except ValueError:
        print("PASS: Invalid confidence was rejected.")
        return

    print("FAIL: Invalid confidence was accepted.")


if __name__ == "__main__":
    main()
