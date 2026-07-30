"""
Schema for updating a project.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.modules.projects.models.project_status import ProjectStatus


class ProjectUpdate(BaseModel):
    """
    Partial project update.
    """

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    status: ProjectStatus | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )