"""
Semantic search service.
"""

from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)


class SearchService:
    """
    Handles semantic search over paper chunks.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Search for chunks semantically similar to the query.
        """

        query_vector = self.embedding_service.embed(query)

        results = self.qdrant_service.search(
            vector=query_vector,
            limit=limit,
        )

        return [
            {
                "score": result.score,
                "paper_id": result.payload["paper_id"],
                "chunk_index": result.payload["chunk_index"],
                "text": result.payload["text"],
            }
            for result in results
        ]