"""
Qdrant vector database service.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct


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

    def upsert_chunks(
        self,
        points: list[dict],
    ) -> None:
        """
        Store chunk vectors in Qdrant.
        """

        self.client.upsert(
            collection_name="paper_chunks",
            points=[
                PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point["payload"],
                )
                for point in points
            ],
        )

    def search(
        self,
        vector: list[float],
        limit: int = 5,
        project_id: str | None = None,
    ):
        """
        Search for the most similar chunks.

        If project_id is provided, only chunks
        belonging to that project are searched.
        """

        query_filter = None

        if project_id:
            query_filter = {
                "must": [
                    {
                        "key": "project_id",
                        "match": {
                            "value": project_id,
                        },
                    }
                ]
            }

        return self.client.query_points(
            collection_name="paper_chunks",
            query=vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
        ).points