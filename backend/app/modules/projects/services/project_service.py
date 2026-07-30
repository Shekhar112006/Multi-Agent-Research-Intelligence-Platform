"""
Business logic for projects.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.projects.models.project import Project
from app.modules.projects.repositories.project_repository import ProjectRepository
from app.modules.projects.schemas.project_create import ProjectCreate
from app.modules.projects.schemas.project_update import ProjectUpdate


class ProjectService:
    """
    Handles project business logic.
    """

    def __init__(self, db: Session):
        self.repository = ProjectRepository(db)

    def create_project(
        self,
        owner_id: UUID,
        project_data: ProjectCreate,
    ) -> Project:
        """
        Create a project for a user.
        """

        return self.repository.create_project(
            owner_id=owner_id,
            project_data=project_data,
        )

    def get_project(
        self,
        owner_id: UUID,
        project_id: UUID,
    ) -> Project:
        """
        Return a user's project.
        """

        project = self.repository.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found.")

        if project.owner_id != owner_id:
            raise PermissionError("Access denied.")

        return project

    def list_projects(
        self,
        owner_id: UUID,
    ) -> list[Project]:
        """
        Return all projects owned by a user.
        """

        return self.repository.list_by_owner(owner_id)

    def update_project(
        self,
        owner_id: UUID,
        project_id: UUID,
        project_data: ProjectUpdate,
    ) -> Project:
        """
        Update a project.
        """

        project = self.get_project(
            owner_id=owner_id,
            project_id=project_id,
        )

        return self.repository.update(
            project,
            project_data,
        )

    def delete_project(
        self,
        owner_id: UUID,
        project_id: UUID,
    ) -> None:
        """
        Delete a project.
        """

        project = self.get_project(
            owner_id=owner_id,
            project_id=project_id,
        )

        self.repository.delete(project)