"""
Repository for paper database operations.
"""

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