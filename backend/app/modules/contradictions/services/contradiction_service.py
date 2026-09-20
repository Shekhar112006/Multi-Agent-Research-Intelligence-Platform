"""
Service for detecting contradictions between research papers.
"""

from uuid import UUID

from app.modules.claims.services.claim_extraction_service import (
    ClaimExtractionService,
)
from app.modules.contradictions.services.claim_matching_service import (
    ClaimMatchingService,
)
from app.modules.contradictions.services.contradiction_generation_service import (
    ContradictionGenerationService,
)


class ContradictionService:
    """
    Coordinates claim extraction, semantic matching,
    and AI-powered contradiction detection.
    """

    def __init__(self, db):
        self.db = db

        self.claim_service = ClaimExtractionService(db)
        self.matching_service = ClaimMatchingService()
        self.generation_service = ContradictionGenerationService()

    async def detect_contradictions(
        self,
        project_id: UUID,
        paper_a_id: UUID,
        paper_b_id: UUID,
    ) -> list[dict]:
        """
        Detect contradictions between two research papers.
        """

        claims_a = await self.claim_service.extract_claims(
            project_id=str(project_id),
            paper_id=str(paper_a_id),
        )

        claims_b = await self.claim_service.extract_claims(
            project_id=str(project_id),
            paper_id=str(paper_b_id),
        )

        if not claims_a:
            raise ValueError(
                f"No claims found for paper {paper_a_id}"
            )

        if not claims_b:
            raise ValueError(
                f"No claims found for paper {paper_b_id}"
            )

        matches = self.matching_service.find_matches(
            claims_a=claims_a,
            claims_b=claims_b,
        )

        if not matches:
            return []

        contradictions = self.generation_service.analyze(
            matches=matches,
        )

        for contradiction in contradictions:
            contradiction["paper_a_id"] = str(paper_a_id)
            contradiction["paper_b_id"] = str(paper_b_id)

        return contradictions