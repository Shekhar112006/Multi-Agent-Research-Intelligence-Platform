"""
Service for research trend analysis.
"""

import json
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.claims.services.claim_extraction_service import (
    ClaimExtractionService,
)
from app.modules.generation.services.generation_service import (
    GenerationService,
)
from app.modules.papers.repositories.paper_repository import PaperRepository


class TrendAnalysisService:
    """
    Collects research signals and identifies
    research trends across multiple papers.
    """

    def __init__(self, db: Session):
        self.db = db
        self.paper_repository = PaperRepository(db)
        self.claim_service = ClaimExtractionService(db)
        self.generation_service = GenerationService()

    async def collect_research_signals(
        self,
        project_id: UUID,
        paper_ids: list[UUID],
    ) -> list[dict]:
        """
        Collect claims and metadata from selected papers.
        """

        papers = self.paper_repository.get_by_ids(paper_ids)

        if not papers:
            raise ValueError("No papers found")

        signals = []

        for paper in papers:

            claims = await self.claim_service.extract_claims(
                project_id=str(project_id),
                paper_id=str(paper.id),
            )

            signals.append(
                {
                    "paper_id": str(paper.id),
                    "title": paper.title,
                    "publication_year": paper.publication_year,
                    "claims": claims,
                }
            )

        return signals

    def analyze_trends(
        self,
        research_signals: list[dict],
    ) -> list[dict]:
        """
        Identify research trends from collected research signals.
        """

        if not research_signals:
            return []

        context_parts = []

        for signal in research_signals:

            claims_text = "\n".join(
                f"- {claim['claim']}"
                for claim in signal["claims"]
            )

            context_parts.append(
                f"""
PAPER ID:
{signal["paper_id"]}

TITLE:
{signal["title"]}

PUBLICATION YEAR:
{signal["publication_year"]}

RESEARCH CLAIMS:
{claims_text}
"""
            )

        context = "\n".join(context_parts)

        question = """
You are a research trend analysis system.

Analyze the research papers and their claims provided below.

Identify recurring research themes or patterns across the papers.

Return ONLY valid JSON using this structure:

{
    "trends": [
        {
            "topic": "string",
            "description": "string",
            "evidence": "string",
            "supporting_papers": ["paper_id"],
            "direction": "emerging",
            "confidence": "high"
        }
    ]
}

Rules:

1. Identify trends supported by multiple papers whenever possible.
2. Do not invent research findings.
3. Use only the provided paper information.
4. Do not treat a single isolated claim as a strong trend.
5. A trend should represent a recurring research topic, method,
   finding, or direction across the provided papers.
6. direction must be one of:
   - emerging
   - stable
   - declining
7. confidence must be one of:
   - high
   - medium
   - low
8. supporting_papers must contain the IDs of papers that support
   the identified trend.
9. Keep descriptions and evidence concise.
10. Return an empty trends list if no meaningful trends can be identified.
"""

        response = self.generation_service.generate(
            question=question,
            context=context,
            response_format={"type": "object"},
        ).strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        result = json.loads(response)

        if not isinstance(result, dict):
            return []

        trends = result.get("trends", [])

        if not isinstance(trends, list):
            return []

        validated_trends = []

        for trend in trends:
            if not isinstance(trend, dict):
                continue

            supporting_papers = trend.get("supporting_papers", [])

            if not isinstance(supporting_papers, list):
                continue

            # A research trend must be supported by
            # at least two different papers.
            unique_papers = set(supporting_papers)

            if len(unique_papers) < 2:
                continue

            trend["supporting_papers"] = list(unique_papers)

            validated_trends.append(trend)

        return validated_trends