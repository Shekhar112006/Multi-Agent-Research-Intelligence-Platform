"""
Qdrant vector database service.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class QdrantService:
    """
    Handles vector database operations.
    """

    def __init__(self):
        self.client = QdrantClient(
            host="localhost",
            port=6333,
        )

    def create_collection(
        self,
        collection_name: str,
    ) -> None:

        collections = self.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        if collection_name in names:
            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )