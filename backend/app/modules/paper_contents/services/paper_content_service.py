"""
Paper content service.
"""

from sqlalchemy.orm import Session

from app.modules.paper_contents.models.paper_content import PaperContent
from app.modules.paper_contents.repositories.paper_content_repository import (
    PaperContentRepository,
)
from app.modules.papers.processing.pdf_extractor import PDFExtractor


class PaperContentService:
    """
    Handles extracted paper content.
    """

    def __init__(self, db: Session):
        self.repository = PaperContentRepository(db)
        self.extractor = PDFExtractor()

    def extract_and_store(
        self,
        paper,
    ) -> PaperContent:
        """
        Extract text from a paper and create or update stored content.
        """

        result = self.extractor.extract(
            paper.file_path,
        )

        existing_content = self.repository.get_by_paper_id(
            paper.id,
        )

        if existing_content:
            return self.repository.update(
                existing_content,
                page_count=result["pages"],
                text=result["text"],
            )

        content = PaperContent(
            paper_id=paper.id,
            page_count=result["pages"],
            text=result["text"],
        )

        return self.repository.create(content)