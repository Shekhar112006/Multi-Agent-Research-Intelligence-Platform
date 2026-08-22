from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    """
    Request body for asking a question against a research project.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the research documents.",
    )