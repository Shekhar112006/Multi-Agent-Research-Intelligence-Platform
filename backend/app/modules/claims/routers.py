from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.claims.schemas.claim_response import ClaimResponse
from app.modules.claims.services.claim_extraction_service import (
    ClaimExtractionService,
)

router = APIRouter(
    prefix="/projects/{project_id}/papers",
    tags=["Claims"],
)


@router.post(
    "/{paper_id}/claims",
    response_model=ClaimResponse,
)
async def extract_claims(
    project_id: str,
    paper_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        service = ClaimExtractionService(db)

        claims = await service.extract_claims(
            project_id=project_id,
            paper_id=paper_id,
        )

        return ClaimResponse(
            paper_id=paper_id,
            claims=claims,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )