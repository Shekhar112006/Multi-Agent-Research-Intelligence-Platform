from pydantic import BaseModel

from app.modules.rag.schemas.rag_source import RAGSource


class RAGResponse(BaseModel):
    """
    Represents the final RAG response.
    """

    answer: str
    sources: list[RAGSource]