"""
API routes for research contradiction detection.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.contradictions.schemas.contradiction_response import (
    ContradictionResponse,
)
from app.modules.contradictions.services.contradiction_service import (
    ContradictionService,
)


router = APIRouter(
    prefix="/projects/{project_id}/contradictions",
    tags=["Contradictions"],
)


@router.post(
    "/{paper_a_id}/{paper_b_id}",
    response_model=ContradictionResponse,
)
async def detect_contradictions(
    project_id: UUID,
    paper_a_id: UUID,
    paper_b_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Detect contradictions between two research papers.
    """

    if paper_a_id == paper_b_id:
        raise HTTPException(
            status_code=400,
            detail="Paper IDs must be different.",
        )

    try:
        service = ContradictionService(db)

        contradictions = await service.detect_contradictions(
            project_id=project_id,
            paper_a_id=paper_a_id,
            paper_b_id=paper_b_id,
        )

        return ContradictionResponse(
            project_id=str(project_id),
            contradictions=contradictions,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )