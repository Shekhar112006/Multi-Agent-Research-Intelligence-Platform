"""
Chunk service.
"""

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.paper_chunks.processing.text_splitter import TextSplitter
from app.modules.paper_chunks.repositories.paper_chunk_repository import (
    PaperChunkRepository,
)


class ChunkService:
    """
    Creates and stores chunks for a paper.
    """

    def __init__(self, db):
        print(">>> ChunkService initialized")
        self.repository = PaperChunkRepository(db)
        self.splitter = TextSplitter()

    def create_chunks(
        self,
        paper,
        text: str,
    ) -> None:
        print(">>> ChunkService started")

        chunk_texts = self.splitter.split(text)

        print(f">>> chunk_texts type: {type(chunk_texts)}")
        print(f">>> total chunks: {len(chunk_texts)}")

        chunks = []

        for index, chunk_text in enumerate(chunk_texts):
            chunks.append(
                PaperChunk(
                    paper_id=paper.id,
                    chunk_index=index,
                    text=chunk_text,
                )
            )

        print(f">>> built {len(chunks)} PaperChunk objects")

        self.repository.create_many(chunks)

        print(">>> repository.create_many finished")