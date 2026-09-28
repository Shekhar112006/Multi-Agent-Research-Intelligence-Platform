"""
Request schemas for research trend analysis.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class TrendRequest(BaseModel):
    """
    Request for analyzing trends across selected papers.
    """

    paper_ids: list[UUID] = Field(
        ...,
        min_length=2,
        description="IDs of at least two papers to analyze.",
    )
