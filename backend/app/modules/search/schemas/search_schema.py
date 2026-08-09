"""
Search schemas.
"""

from uuid import UUID

from pydantic import BaseModel


class SearchResult(BaseModel):
    score: float
    paper_id: UUID
    chunk_index: int
    text: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]