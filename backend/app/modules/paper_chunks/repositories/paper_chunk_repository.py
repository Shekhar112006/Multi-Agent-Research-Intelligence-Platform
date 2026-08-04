"""
Repository for paper chunk database operations.
"""

from sqlalchemy.orm import Session

from app.modules.paper_chunks.models.paper_chunk import PaperChunk


class PaperChunkRepository:
    """
    Handles paper chunk database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_many(
        self,
        chunks: list[PaperChunk],
    ) -> None:
        print(f">>> Repository received {len(chunks)} chunks")

        self.db.add_all(chunks)
        self.db.commit()

        print(">>> Commit complete")