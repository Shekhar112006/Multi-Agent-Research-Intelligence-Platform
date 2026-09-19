"""
Service for retrieving relevant chunks for paper comparison.
"""

from uuid import UUID

from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)


class ComparisonRetrievalService:
    """
    Retrieves semantically relevant chunks separately for each paper.
    """

    COMPARISON_QUERIES = {
        "methodology": (
            "research methodology research design "
            "participants sample data collection "
            "analysis procedure"
        ),
        "datasets": (
            "dataset data source participants sample population "
            "experimental data"
        ),
        "evaluation_metrics": (
            "evaluation metrics measurements accuracy performance "
            "evaluation criteria assessment"
        ),
        "results": (
            "research results findings outcomes performance "
            "experimental results quantitative qualitative findings"
        ),
        "limitations": (
            "research limitations weaknesses constraints "
            "study limitations future work"
        ),
        "claims": (
            "main claims conclusions contributions findings "
            "research objectives"
        ),
    }

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def retrieve_for_paper(
        self,
        *,
        project_id: UUID,
        paper_id: UUID,
        query: str,
        limit: int = 3,
    ) -> list[dict]:
        """
        Retrieve relevant chunks from one specific paper.
        """

        embedding = self.embedding_service.embed(query)

        results = self.qdrant_service.search(
            vector=embedding,
            limit=limit,
            project_id=str(project_id),
            paper_id=str(paper_id),
        )

        return [
            {
                "chunk_index": result.payload.get("chunk_index"),
                "text": result.payload.get("text", ""),
                "score": result.score,
            }
            for result in results
        ]

    def retrieve_comparison_context(
        self,
        *,
        project_id: UUID,
        paper_id: UUID,
        limit_per_dimension: int = 3,
    ) -> dict[str, list[dict]]:
        """
        Retrieve relevant chunks for each comparison dimension.
        """

        comparison_context = {}

        for dimension, query in self.COMPARISON_QUERIES.items():
            comparison_context[dimension] = self.retrieve_for_paper(
                project_id=project_id,
                paper_id=paper_id,
                query=query,
                limit=limit_per_dimension,
            )

        return comparison_context