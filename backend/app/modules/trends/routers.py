"""
API routes for research trend analysis.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.trends.schemas.trend_request import TrendRequest
from app.modules.trends.schemas.trend_response import TrendResponse
from app.modules.trends.services.trend_analysis_service import (
    TrendAnalysisService,
)


router = APIRouter(
    prefix="/projects/{project_id}/trends",
    tags=["Research Trends"],
)


@router.post(
    "",
    response_model=TrendResponse,
)
async def analyze_research_trends(
    project_id: UUID,
    request: TrendRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze research trends across selected papers.
    """

    try:
        service = TrendAnalysisService(db)

        research_signals = await service.collect_research_signals(
            project_id=project_id,
            paper_ids=request.paper_ids,
        )

        trends = service.analyze_trends(
            research_signals=research_signals,
        )

        return TrendResponse(
            project_id=str(project_id),
            trends=trends,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Trend analysis failed: {str(exc)}",
        )
