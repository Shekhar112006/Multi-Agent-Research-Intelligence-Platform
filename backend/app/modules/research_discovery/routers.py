from fastapi import APIRouter, HTTPException, Query

from app.modules.research_discovery.schemas.paper_search_response import (
    PaperSearchResponse,
)
from app.modules.research_discovery.services.paper_discovery_service import (
    PaperDiscoveryService,
)


router = APIRouter(
    prefix="/research",
    tags=["Research Discovery"],
)


@router.get("/papers/search", response_model=PaperSearchResponse)
async def search_research_papers(
    query: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        service = PaperDiscoveryService()

        papers = service.search_papers(
            query=query,
            limit=limit,
        )

        return PaperSearchResponse(
            query=query,
            total=len(papers),
            papers=papers,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Semantic Scholar request failed: {str(exc)}",
        )