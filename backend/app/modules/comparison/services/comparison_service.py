"""
Service for multi-paper comparison.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.papers.models.paper import Paper
from app.modules.papers.repositories.paper_repository import PaperRepository

from app.modules.paper_contents.repositories.paper_content_repository import (
    PaperContentRepository,
)
from app.modules.comparison.services.comparison_generation_service import (
    ComparisonGenerationService,
)


class ComparisonService:
    """
    Handles business logic for comparing research papers.
    """

    def __init__(self, db: Session):
        self.repository = PaperRepository(db)
        self.content_repository = PaperContentRepository(db)
        self.generation_service = ComparisonGenerationService()

    def get_papers_for_comparison(
        self,
        *,
        project_id: UUID,
        paper_ids: list[UUID],
    ) -> list[Paper]:
        """
        Retrieve and validate papers selected for comparison.
        """

        if len(paper_ids) < 2:
            raise ValueError(
                "At least two papers are required for comparison."
            )

        unique_paper_ids = list(dict.fromkeys(paper_ids))

        if len(unique_paper_ids) < 2:
            raise ValueError(
                "At least two different papers are required for comparison."
            )

        papers = self.repository.get_by_ids(
            unique_paper_ids,
        )

        if len(papers) != len(unique_paper_ids):
            found_ids = {
                paper.id
                for paper in papers
            }

            missing_ids = [
                paper_id
                for paper_id in unique_paper_ids
                if paper_id not in found_ids
            ]

            raise ValueError(
                f"Paper(s) not found: {missing_ids}"
            )

        invalid_papers = [
            paper
            for paper in papers
            if paper.project_id != project_id
        ]

        if invalid_papers:
            raise ValueError(
                "All papers must belong to the requested project."
            )

        return papers

    def build_comparison_data(
        self,
        *,
        project_id: UUID,
        paper_ids: list[UUID],
    ) -> list[dict]:
        """
        Build comparison input using the actual paper content.
        """

        papers = self.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=paper_ids,
        )

        comparison_data = []

        for paper in papers:
            content = self.content_repository.get_by_paper_id(
                paper.id,
            )

            if content is None:
                raise ValueError(
                    f"Paper content not found for paper: {paper.id}"
                )

            comparison_data.append(
                {
                    "paper_id": str(paper.id),
                    "title": paper.title,
                    "text": content.text,
                }
            )

        return comparison_data

    def compare_papers(
        self,
        *,
        project_id: UUID,
        paper_ids: list[UUID],
    ) -> dict:
        """
        Generate an AI-powered comparison of selected papers.
        """

        comparison_data = self.build_comparison_data(
            project_id=project_id,
            paper_ids=paper_ids,
        )

        return self.generation_service.compare(
            comparison_data=comparison_data,
        )