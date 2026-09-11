from fastapi import APIRouter, Depends, HTTPException, Query
from app.modules.research_discovery.schemas.paper_search_response import (
    PaperSearchResponse,
)
from app.modules.research_discovery.services.paper_discovery_service import (
    PaperDiscoveryService,
)
from app.modules.research_discovery.services.paper_download_service import (
    PaperDownloadService,
)
from pathlib import Path

from app.core.database import get_db
from app.modules.research_discovery.services.paper_download_service import (
    PaperDownloadService,
)
from app.modules.research_discovery.services.paper_persistence_service import (
    PaperPersistenceService,
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

@router.post("/papers/{paper_id}/ingest")
async def ingest_research_paper(
    paper_id: str,
    project_id: str,
    title: str,
    abstract: str | None = None,
    pdf_url: str | None = None,
    db=Depends(get_db),
):
    if not pdf_url:
        raise HTTPException(
            status_code=400,
            detail="Open Access PDF URL is required",
        )

    try:
        download_service = PaperDownloadService()

        file_path = download_service.download_pdf(
            pdf_url=pdf_url,
            paper_id=paper_id,
        )

        file_size = Path(file_path).stat().st_size

        paper_data = {
            "paperId": paper_id,
            "title": title,
            "abstract": abstract,
            "authors": [],
            "year": None,
            "citationCount": 0,
            "url": None,
            "openAccessPdf": {
                "url": pdf_url,
            },
        }

        persistence_service = PaperPersistenceService(db)

        paper = persistence_service.create_paper(
            project_id=project_id,
            paper_data=paper_data,
            file_path=file_path,
            file_size=file_size,
        )

        return {
            "message": "Research paper ingested successfully",
            "paper_id": str(paper.id),
            "semantic_scholar_id": paper.semantic_scholar_id,
            "title": paper.title,
            "file_path": paper.file_path,
            "file_size": paper.file_size,
            "upload_status": paper.upload_status,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Research paper ingestion failed: {str(exc)}",
        )