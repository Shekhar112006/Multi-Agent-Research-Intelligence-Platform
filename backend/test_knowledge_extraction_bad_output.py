

"""
Test intentionally invalid LLM knowledge graph output.
"""

from pydantic import ValidationError

from app.modules.knowledge_graph.schemas.knowledge_extraction import (
    KnowledgeGraphExtractionResponse,
)


def main() -> None:
    """
    Verify that intentionally invalid LLM output is rejected.
    """

    bad_output = {
        "nodes": [
            {
                "node_type": "paper",
                "label": "RAG",
            }
        ],
        "relationships": [
            {
                "source_label": "RAG",
                "target_label": "Unknown Dataset",
                "relationship_type": "evaluates",
                "evidence": "",
                "confidence": "banana",
            }
        ],
    }

    try:
        KnowledgeGraphExtractionResponse.model_validate(
            bad_output
        )

    except ValidationError:
        print(
            "PASS: Intentionally invalid LLM output was rejected."
        )
        return

    print(
        "FAIL: Invalid LLM output was accepted."
    )


if __name__ == "__main__":
    main()
