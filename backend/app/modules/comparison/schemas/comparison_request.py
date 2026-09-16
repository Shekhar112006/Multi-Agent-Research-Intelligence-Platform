from uuid import UUID

from pydantic import BaseModel, Field


class ComparisonRequest(BaseModel):
    paper_ids: list[UUID] = Field(
        min_length=2,
        max_length=10,
    )