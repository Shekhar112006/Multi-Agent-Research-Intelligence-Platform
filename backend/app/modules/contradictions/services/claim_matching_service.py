"""
Service for matching semantically related claims.
"""

from app.modules.embeddings.services.embedding_service import EmbeddingService


class ClaimMatchingService:
    """
    Finds potentially related claims using semantic similarity.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ):
        self.embedding_service = (
            embedding_service
            if embedding_service is not None
            else EmbeddingService()
        )

    def similarity(
        self,
        embedding_a: list[float],
        embedding_b: list[float],
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        The embedding service already returns normalized vectors,
        so their dot product represents cosine similarity.
        """
        return sum(
            a * b
            for a, b in zip(embedding_a, embedding_b)
        )

    def find_matches(
        self,
        claims_a: list[dict],
        claims_b: list[dict],
        threshold: float = 0.70,
    ) -> list[dict]:
        """
        Find potentially related claims between two papers.

        Each claim is embedded exactly once. The resulting embeddings
        are then reused when comparing every possible claim pair.
        """

        if not claims_a or not claims_b:
            return []

        embeddings_a = [
            self.embedding_service.embed(claim["claim"])
            for claim in claims_a
        ]

        embeddings_b = [
            self.embedding_service.embed(claim["claim"])
            for claim in claims_b
        ]

        matches = []

        for claim_a, embedding_a in zip(claims_a, embeddings_a):
            for claim_b, embedding_b in zip(claims_b, embeddings_b):

                score = self.similarity(
                    embedding_a,
                    embedding_b,
                )

                if score >= threshold:
                    matches.append(
                        {
                            "claim_a": claim_a,
                            "claim_b": claim_b,
                            "similarity": score,
                        }
                    )

        return matches