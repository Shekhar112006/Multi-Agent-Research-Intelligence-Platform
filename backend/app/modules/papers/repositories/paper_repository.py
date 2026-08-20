"""
Repository for paper database operations.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.papers.models.paper import Paper


class PaperRepository:
    """
    Handles database operations for papers.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        paper: Paper,
    ) -> Paper:

        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)

        return paper

    def get_by_id(
        self,
        paper_id: UUID,
    ) -> Paper | None:

        return (
            self.db.query(Paper)
            .filter(Paper.id == paper_id)
            .first()
        )