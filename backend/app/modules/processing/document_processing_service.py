"""
Document processing orchestrator.
"""

from sqlalchemy.orm import Session

from app.modules.paper_contents.services.paper_content_service import (
    PaperContentService,
)
from app.modules.papers.models.upload_status import UploadStatus


class DocumentProcessingService:
    """
    Coordinates all document processing tasks.
    """

    def __init__(self, db: Session):
        self.db = db
        self.paper_content_service = PaperContentService(db)

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
            self.paper_content_service.extract_and_store(
                paper,
            )

            paper.upload_status = UploadStatus.PROCESSED

        except Exception:
            paper.upload_status = UploadStatus.FAILED
            raise

        finally:
            self.db.commit()