"""
Response schema for projects.
"""

from datetime import datetime
from uuid import UUID

from app.modules.projects.models.project_status import ProjectStatus
from app.modules.projects.schemas.project_base import ProjectBase


class ProjectResponse(ProjectBase):
    """
    Returned project data.
    """

    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime