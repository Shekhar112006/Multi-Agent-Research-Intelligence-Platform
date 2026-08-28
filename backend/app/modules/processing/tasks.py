"""
Background document processing tasks.
"""

from app.core.celery.celery_app import celery_app
from app.core.database import SessionLocal
from app.modules.papers.repositories.paper_repository import PaperRepository
from app.modules.processing.document_processing_service import (
    DocumentProcessingService,
)


@celery_app.task
def process_document(paper_id: str) -> None:
    """
    Process an uploaded paper in the background.
    """

    db = SessionLocal()

    try:
        repository = PaperRepository(db)

        paper = repository.get_by_id(paper_id)

        if paper is None:
            raise ValueError(
                f"Paper {paper_id} not found"
            )

        service = DocumentProcessingService(db)

        service.process(paper)

    finally:
        db.close()