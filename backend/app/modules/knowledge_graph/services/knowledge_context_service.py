"""
Service for building structured paper context for knowledge graph extraction.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.papers.models.paper import Paper


class KnowledgeContextService:
    """
    Builds a structured research-paper context for knowledge graph extraction.
    """

    def __init__(self, db: Session):
        """
        Initialize the context service.
        """

        self.db = db

    def build_paper_context(
        self,
        paper_id: str,
    ) -> str:
        """
        Build structured context containing paper metadata
        and ordered paper chunks.
        """

        paper_result = self.db.execute(
            select(Paper).where(
                Paper.id == paper_id,
            )
        )

        paper = paper_result.scalar_one_or_none()

        if paper is None:
            raise ValueError("Paper not found")

        chunks_result = self.db.execute(
            select(PaperChunk)
            .where(
                PaperChunk.paper_id == paper_id,
            )
            .order_by(PaperChunk.chunk_index)
        )

        chunks = chunks_result.scalars().all()

        if not chunks:
            raise ValueError("No chunks found for this paper")

        chunk_text = "\n\n".join(
            f"[Chunk {chunk.chunk_index}]\n{chunk.text}"
            for chunk in chunks
        )

        return f"""
Research Paper Metadata:

Title:
{paper.title}

Authors:
{paper.authors or "Not available"}

Publication Year:
{paper.publication_year or "Not available"}

Abstract:
{paper.abstract or "Not available"}

Research Paper Content:

{chunk_text}
""".strip()