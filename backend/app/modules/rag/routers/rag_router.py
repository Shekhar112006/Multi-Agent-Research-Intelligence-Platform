"""
RAG API endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.rag.schemas.rag_request import RAGRequest
from app.modules.rag.schemas.rag_response import RAGResponse
from app.modules.rag.services.rag_service import RAGService
from app.modules.users.models.users import User


router = APIRouter(
    prefix="/projects",
    tags=["RAG"],
)


@router.post(
    "/{project_id}/rag/ask",
    response_model=RAGResponse,
)
def ask_question(
    project_id: UUID,
    request: RAGRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Ask a question against the research documents
    belonging to a project.
    """

    service = RAGService(db)

    return service.answer(
        question=request.question,
        project_id=str(project_id),
        limit=15,
        min_score=0.20,
    )