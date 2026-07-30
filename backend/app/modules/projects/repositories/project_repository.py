"""
Repository for project database operations.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.projects.models.project import Project
from app.modules.projects.schemas.project_create import ProjectCreate
from app.modules.projects.schemas.project_update import ProjectUpdate


class ProjectRepository:
    """
    Handles project database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_project(
        self,
        owner_id: UUID,
        project_data: ProjectCreate,
    ) -> Project:
        """
        Create a new project.
        """

        project = Project(
            owner_id=owner_id,
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def get_by_id(
        self,
        project_id: UUID,
    ) -> Project | None:
        """
        Retrieve a project by ID.
        """

        statement = select(Project).where(
            Project.id == project_id
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def list_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Project]:
        """
        Return all projects owned by a user.
        """

        statement = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .order_by(Project.created_at.desc())
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def update(
        self,
        project: Project,
        project_data: ProjectUpdate,
    ) -> Project:
        """
        Update an existing project.
        """

        updates = project_data.model_dump(
            exclude_unset=True,
        )

        for field, value in updates.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)

        return project

    def delete(
        self,
        project: Project,
    ) -> None:
        """
        Delete a project.
        """

        self.db.delete(project)
        self.db.commit()