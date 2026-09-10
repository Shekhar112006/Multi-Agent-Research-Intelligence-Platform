from fastapi import APIRouter, HTTPException, Query

from app.modules.research_discovery.schemas.paper_search_response import (
    PaperSearchResponse,
)
from app.modules.research_discovery.services.paper_discovery_service import (
    PaperDiscoveryService,
)
from app.modules.research_discovery.services.paper_download_service import (
    PaperDownloadService,
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

@router.post("/papers/{paper_id}/download")
async def download_research_paper(
    paper_id: str,
    pdf_url: str,
):
    try:
        service = PaperDownloadService()

        file_path = service.download_pdf(
            pdf_url=pdf_url,
            paper_id=paper_id,
        )

        return {
            "paper_id": paper_id,
            "message": "Paper downloaded successfully",
            "file_path": file_path,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Paper download failed: {str(exc)}",
        )