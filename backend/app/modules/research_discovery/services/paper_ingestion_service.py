from pathlib import Path

from sqlalchemy.orm import Session

from app.modules.research_discovery.clients.semantic_scholar_client import (
    SemanticScholarClient,
)
from app.modules.research_discovery.services.paper_download_service import (
    PaperDownloadService,
)
from app.modules.research_discovery.services.paper_persistence_service import (
    PaperPersistenceService,
)
from app.modules.paper_contents.services.paper_content_service import (
    PaperContentService,
)


class PaperIngestionService:
    def __init__(
        self,
        db: Session,
        client: SemanticScholarClient | None = None,
        download_service: PaperDownloadService | None = None,
        persistence_service: PaperPersistenceService | None = None,
        content_service: PaperContentService | None = None,
    ):
        self.db = db
        self.client = client or SemanticScholarClient()
        self.download_service = (
            download_service or PaperDownloadService()
        )
        self.persistence_service = (
            persistence_service or PaperPersistenceService(db)
        )
        self.content_service = (
            content_service or PaperContentService(db)
        )   

    def ingest_paper(
        self,
        project_id,
        paper_id: str,
    ):
        # 1. Get complete metadata from Semantic Scholar
        paper_data = self.client.get_paper(
            paper_id=paper_id,
        )

        # 2. Get Open Access PDF URL
        open_access_pdf = paper_data.get("openAccessPdf") or {}
        pdf_url = open_access_pdf.get("url")

        if not pdf_url:
            raise ValueError(
                "No Open Access PDF is available for this paper."
            )

        # 3. Download PDF
        file_path = self.download_service.download_pdf(
            pdf_url=pdf_url,
            paper_id=paper_id,
        )

        # 4. Determine downloaded file size
        file_size = Path(file_path).stat().st_size

        # 5. Persist paper + metadata
        paper = self.persistence_service.create_paper(
            project_id=project_id,
            paper_data=paper_data,
            file_path=file_path,
            file_size=file_size,
        )

        self.content_service.extract_and_store(
            paper,
        )

        return paper
