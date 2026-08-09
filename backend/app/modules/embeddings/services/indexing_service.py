"""
Embedding indexing service.
"""

from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)


class IndexingService:
    """
    Generates embeddings and stores them in Qdrant.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def index_chunks(
        self,
        chunks,
    ) -> None:
        print(f">>> Indexing {len(chunks)} chunks")
        """
        Index paper chunks into Qdrant.
        """

        points = []

        for chunk in chunks:

            embedding = self.embedding_service.embed(
                chunk.text,
            )

            points.append(
                {
                    "id": str(chunk.id),
                    "vector": embedding,
                    "payload": {
                        "project_id": str(chunk.paper.project_id),
                        "paper_id": str(chunk.paper_id),
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                    },  
                }
            )
        print(f">>> Sending {len(points)} vectors to Qdrant")
        self.qdrant_service.upsert_chunks(
            points,
        )