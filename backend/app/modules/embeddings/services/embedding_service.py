"""
Embedding generation service.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates vector embeddings from text.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()