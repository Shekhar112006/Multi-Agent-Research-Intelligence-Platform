from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.gaps.schemas.gap_response import GapResponse
from app.modules.gaps.services.gap_detection_service import GapDetectionService


router = APIRouter(
    prefix="/projects/{project_id}/papers",
    tags=["Research Gaps"],
)


@router.post("/{paper_id}/gaps", response_model=GapResponse)
async def detect_research_gaps(
    project_id: str,
    paper_id: str,
    db: Session = Depends(get_db),
):
    try:
        service = GapDetectionService(db)

        gaps = await service.detect_gaps(
            project_id=project_id,
            paper_id=paper_id,
        )

        return GapResponse(
            paper_id=paper_id,
            gaps=gaps,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )