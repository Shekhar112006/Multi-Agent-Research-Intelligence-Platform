"""
Retrieval service.

Responsible for converting a user query into an embedding
and retrieving the most relevant chunks from Qdrant.
"""

from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)
from app.modules.retrieval.schemas.retrieval_result import (
    RetrievalResult,
)


class RetrievalService:
    """
    Application service responsible for semantic retrieval.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(
    self,
    query: str,
    limit: int = 5,
    project_id: str | None = None,
    min_score: float | None = None,
) -> list[RetrievalResult]:

        vector = self.embedding_service.embed(query)

        results = self.qdrant_service.search(
            vector=vector,
            limit=limit,
            project_id=project_id,
        )

        if min_score is not None:
            results = [
                result
                for result in results
                if result.score >= min_score
            ]

        return [
            RetrievalResult(
                paper_id=result.payload["paper_id"],
                project_id=result.payload["project_id"],
                chunk_index=result.payload["chunk_index"],
                text=result.payload["text"],
                score=result.score,
            )
            for result in results
        ]