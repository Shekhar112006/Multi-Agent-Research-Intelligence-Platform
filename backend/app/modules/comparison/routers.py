"""
Comparison API routes.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.comparison.schemas.comparison_request import (
    ComparisonRequest,
)
from app.modules.comparison.services.comparison_service import (
    ComparisonService,
)


router = APIRouter(
    prefix="/projects/{project_id}/compare",
    tags=["Paper Comparison"],
)


@router.post("")
async def compare_papers(
    project_id: UUID,
    request: ComparisonRequest,
    db: Session = Depends(get_db),
):
    try:
        service = ComparisonService(db)

        papers = service.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=request.paper_ids,
        )

        return {
            "project_id": str(project_id),
            "papers": [
                {
                    "paper_id": str(paper.id),
                    "title": paper.title,
                }
                for paper in papers
            ],
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )