from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.methodology.schemas.methodology_response import MethodologyResponse
from app.modules.methodology.services.methodology_extraction_service import (
    MethodologyExtractionService,
)


router = APIRouter(
    prefix="/projects/{project_id}/papers",
    tags=["Methodology"],
)


@router.post("/{paper_id}/methodology", response_model=MethodologyResponse)
async def extract_methodology(
    project_id: str,
    paper_id: str,
    db: Session = Depends(get_db),
):
    try:
        service = MethodologyExtractionService(db)

        methodology = await service.extract_methodology(
            project_id=project_id,
            paper_id=paper_id,
        )

        return MethodologyResponse(
            paper_id=paper_id,
            methodology=methodology,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
            )