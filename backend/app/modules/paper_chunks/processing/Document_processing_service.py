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
from app.modules.papers.models.upload_status import UploadStatus


class DocumentProcessingService:
    """
    Coordinates all document processing tasks.
    """

    def __init__(self, db: Session):
        self.db = db
        self.paper_content_service = PaperContentService(db)
        self.chunk_service = ChunkService(db)
        print(">>> DocumentProcessingService.process()")

    def process(
        self,
        paper,
    ):
        """
        Process an uploaded paper.
        """

        paper.upload_status = UploadStatus.PROCESSING
        self.db.commit()

        # Extract and store text
        content = self.paper_content_service.extract_and_store(
            paper,
        )
        print(f">>> Content length: {len(content.text)}")

        # Create chunks
        self.chunk_service.create_chunks(
            paper,
            content.text,
        )
        print(">>> Returned from ChunkService")

        paper.upload_status = UploadStatus.PROCESSED
        self.db.commit()