"""
Project API endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.projects.schemas.project_create import ProjectCreate
from app.modules.projects.schemas.project_response import ProjectResponse
from app.modules.projects.schemas.project_update import ProjectUpdate
from app.modules.projects.services.project_service import ProjectService
from app.modules.users.models.users import User


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new project.
    """

    service = ProjectService(db)

    return service.create_project(
        owner_id=current_user.id,
        project_data=project_data,
    )




@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List current user's projects.
    """

    service = ProjectService(db)

    return service.list_projects(
        owner_id=current_user.id,
    )



@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve one project.
    """

    service = ProjectService(db)

    return service.get_project(
        owner_id=current_user.id,
        project_id=project_id,
    )



@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a project.
    """

    service = ProjectService(db)

    return service.update_project(
        owner_id=current_user.id,
        project_id=project_id,
        project_data=project_data,
    )



@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a project.
    """

    service = ProjectService(db)

    service.delete_project(
        owner_id=current_user.id,
        project_id=project_id,
    )