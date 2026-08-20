"""
Paper service.
"""

from fastapi import UploadFile
from sqlalchemy.orm import Session
from uuid import UUID

from app.modules.users.models.users import User

from app.core.exceptions.auth import AuthenticationError
from app.core.storage.storage_service import StorageService
from app.modules.papers.models.paper import Paper
from app.modules.papers.models.upload_status import UploadStatus
from app.modules.papers.repositories.paper_repository import PaperRepository
from app.modules.projects.repositories.project_repository import ProjectRepository
from app.modules.processing.document_processing_service import (
    DocumentProcessingService,
)


class PaperService:
    """
    Handles paper-related business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = PaperRepository(db)
        self.project_repository = ProjectRepository(db)
        self.storage = StorageService()
        self.processing_service = DocumentProcessingService(db)

    async def upload(
        self,
        *,
        project_id:UUID,
        current_user:User,
        title: str,
        file: UploadFile,
    ) -> Paper:
        """
        Upload a paper for a project.
        """

        project = self.project_repository.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found")

        if project.owner_id != current_user.id:
            raise AuthenticationError()

        stored_filename, file_path = await self.storage.save_pdf(file)

        paper = Paper(
            project_id=project_id,
            title=title,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=file_path,
            mime_type=file.content_type,
            file_size=file.size,
            upload_status=UploadStatus.UPLOADED,
        )

        paper = self.repository.create(paper)

        self.processing_service.process(
            paper,
        )

        return paper

    def get_by_id(
        self,
        paper_id: UUID,
    ) -> Paper | None:

        return self.repository.get_by_id(paper_id)