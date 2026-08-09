"""
Search router.
"""

from fastapi import APIRouter, Query

from app.modules.search.schemas.search_schema import SearchResponse
from app.modules.search.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get(
    "",
    response_model=SearchResponse,
)
def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
):
    service = SearchService()

    results = service.search(
        query=q,
        limit=limit,
    )

    return SearchResponse(
        query=q,
        results=results,
    )