from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.summarization.schemas.summary_response import SummaryResponse
from app.modules.summarization.services.summarization_service import (
    SummarizationService,
)

router = APIRouter(
    prefix="/projects/{project_id}/papers",
    tags=["Summarization"],
)


@router.post(
    "/{paper_id}/summarize",
    response_model=SummaryResponse,
)
async def summarize_paper(
    project_id: str,
    paper_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        service = SummarizationService(db)

        summary = await service.summarize(
            project_id=project_id,
            paper_id=paper_id,
        )

        return SummaryResponse(
            paper_id=paper_id,
            summary=summary,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )