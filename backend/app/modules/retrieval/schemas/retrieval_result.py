"""
Retrieval result schema.
"""

from pydantic import BaseModel


class RetrievalResult(BaseModel):
    """
    Represents one retrieved document chunk.
    """

    paper_id: str
    project_id: str
    chunk_index: int
    text: str
    score: float