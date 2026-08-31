"""
Repository for paper chunk database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
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
    ) -> list[PaperChunk]:
        print(f">>> Repository received {len(chunks)} chunks")

        self.db.add_all(chunks)
        self.db.commit()

        print(">>> Commit complete")

        return chunks

    def get_by_paper_id(
        self,
        paper_id,
    ) -> list[PaperChunk]:
        statement = select(PaperChunk).where(
            PaperChunk.paper_id == paper_id
        ).order_by(
            PaperChunk.chunk_index
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())