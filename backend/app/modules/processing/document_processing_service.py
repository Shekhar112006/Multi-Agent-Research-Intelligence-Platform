"""
Document processing orchestrator.
"""

from sqlalchemy.orm import Session

from app.core.logging.logger import get_logger
from app.modules.embeddings.services.indexing_service import (
    IndexingService,
)
from app.modules.paper_chunks.services.chunk_service import (
    ChunkService,
)
from app.modules.paper_contents.services.paper_content_service import (
    PaperContentService,
)
from app.modules.papers.models.upload_status import UploadStatus


logger = get_logger(__name__)


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

        logger.info(
            "Starting document processing | paper_id=%s",
            paper.id,
        )

        paper.upload_status = UploadStatus.PROCESSING
        self.db.commit()

        try:
            logger.info(
                "Extracting paper text | paper_id=%s",
                paper.id,
            )

            content = self.paper_content_service.extract_and_store(
                paper,
            )

            logger.info(
                "Paper text extracted | paper_id=%s | characters=%d",
                paper.id,
                len(content.text),
            )

            chunks = self.chunk_service.create_chunks(
                paper,
                content.text,
            )

            logger.info(
                "Paper chunks created | paper_id=%s | chunks=%d",
                paper.id,
                len(chunks),
            )

            self.indexing_service.index_chunks(
                chunks,
            )

            logger.info(
                "Paper chunks indexed | paper_id=%s | chunks=%d",
                paper.id,
                len(chunks),
            )

            paper.upload_status = UploadStatus.PROCESSED

            logger.info(
                "Document processing completed | paper_id=%s",
                paper.id,
            )

        except Exception:
            self.db.rollback()

            paper.upload_status = UploadStatus.FAILED

            logger.exception(
                "Document processing failed | paper_id=%s",
                paper.id,
            )

            self.db.commit()

            raise