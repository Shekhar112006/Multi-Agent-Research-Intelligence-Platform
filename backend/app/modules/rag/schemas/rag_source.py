from pydantic import BaseModel


class RAGSource(BaseModel):
    """
    Represents a source used to generate a RAG answer.
    """

    paper_id: str
    project_id: str
    title: str
    original_filename: str
    chunk_index: int
    score: float