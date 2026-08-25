"""
Embedding indexing service.
"""

from app.core.logging.logger import get_logger
from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)


logger = get_logger(__name__)


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
        """
        Index paper chunks into Qdrant.
        """

        logger.info(
            "Generating embeddings | chunks=%d",
            len(chunks),
        )

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

        logger.info(
            "Sending vectors to Qdrant | vectors=%d",
            len(points),
        )

        self.qdrant_service.upsert_chunks(
            points,
        )

        logger.info(
            "Vectors indexed successfully | vectors=%d",
            len(points),
        )