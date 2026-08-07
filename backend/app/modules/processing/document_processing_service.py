"""
Document processing orchestrator.
"""

from sqlalchemy.orm import Session

from app.modules.paper_contents.services.paper_content_service import (
    PaperContentService,
)
from app.modules.paper_chunks.services.chunk_service import (
    ChunkService,
)

from app.modules.embeddings.services.indexing_service import (
    IndexingService,
)

from app.modules.papers.models.upload_status import UploadStatus


class DocumentProcessingService:
    """
    Coordinates all document processing tasks.
    """

    def __init__(self, db: Session):
        self.db = db
        self.paper_content_service = PaperContentService(db)
        self.chunk_service = ChunkService(db)
        self.indexing_service = IndexingService()

    def process(
        self,
        paper,
    ):
        """
        Process an uploaded paper.
        """

        paper.upload_status = UploadStatus.PROCESSING
        self.db.commit()

        try:
            # Extract full text
            content = self.paper_content_service.extract_and_store(
                paper,
            )

            # Split into chunks
            chunks = self.chunk_service.create_chunks(
                paper,
                content.text,
            )

            # Index into Qdrant
            self.indexing_service.index_chunks(
                chunks,
            )

            # Mark as processed
            paper.upload_status = UploadStatus.PROCESSED

        except Exception:
            paper.upload_status = UploadStatus.FAILED
            raise

        finally:
            self.db.commit()