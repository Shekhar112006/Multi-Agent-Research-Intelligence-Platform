"""
Chunk service.
"""

from app.core.logging.logger import get_logger
from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.paper_chunks.processing.text_splitter import TextSplitter
from app.modules.paper_chunks.repositories.paper_chunk_repository import (
    PaperChunkRepository,
)


logger = get_logger(__name__)


class ChunkService:
    """
    Creates and stores chunks for a paper.
    """

    def __init__(self, db):
        self.repository = PaperChunkRepository(db)
        self.splitter = TextSplitter()

    def create_chunks(
        self,
        paper,
        text: str,
    ) -> list[PaperChunk]:
        """
        Split paper text and persist the resulting chunks.
        """

        logger.info(
            "Creating chunks | paper_id=%s",
            paper.id,
        )

        existing_chunks = self.repository.get_by_paper_id(
            paper.id
        )

        if existing_chunks:
            logger.info(
                "Chunks already exist | paper_id=%s | chunks=%d",
                paper.id,
                len(existing_chunks),
            )
            return existing_chunks

        chunk_texts = self.splitter.split(text)

        logger.info(
            "Text split completed | paper_id=%s | chunks=%d",
            paper.id,
            len(chunk_texts),
        )

        chunks = [
            PaperChunk(
                paper_id=paper.id,
                chunk_index=index,
                text=chunk_text,
            )
            for index, chunk_text in enumerate(chunk_texts)
        ]

        self.repository.create_many(chunks)

        logger.info(
            "Chunks persisted | paper_id=%s | chunks=%d",
            paper.id,
            len(chunks),
        )

        return chunks