"""
Repository for paper content database operations.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.paper_contents.models.paper_content import PaperContent


class PaperContentRepository:
    """
    Handles database operations for paper contents.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        content: PaperContent,
    ) -> PaperContent:
        """
        Create paper content.
        """

        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)

        return content

    def get_by_paper_id(
        self,
        paper_id,
    ) -> PaperContent | None:
        """
        Return paper content by paper ID.
        """

        statement = select(PaperContent).where(
            PaperContent.paper_id == paper_id
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def update(
        self,
        content: PaperContent,
        page_count: int,
        text: str,
    ) -> PaperContent:
        """
        Update existing paper content.
        """

        content.page_count = page_count
        content.text = text

        self.db.commit()
        self.db.refresh(content)

        return content