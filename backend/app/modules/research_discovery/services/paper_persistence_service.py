from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.papers.models.paper import Paper
from app.modules.papers.models.upload_status import UploadStatus


class PaperPersistenceService:
    def __init__(self, db: Session):
        self.db = db

    def create_paper(
        self,
        project_id,
        paper_data: dict,
        file_path: str,
        file_size: int,
    ) -> Paper:
        semantic_scholar_id = paper_data["paperId"]

        existing_paper = self.db.execute(
            select(Paper).where(
                Paper.semantic_scholar_id == semantic_scholar_id
            )
        ).scalar_one_or_none()

        if existing_paper:
            return existing_paper

        authors = paper_data.get("authors", [])

        author_names = [
            author.get("name", "")
            for author in authors
            if author.get("name")
        ]

        paper = Paper(
            project_id=project_id,
            title=paper_data.get("title") or "Untitled Paper",
            semantic_scholar_id=semantic_scholar_id,
            abstract=paper_data.get("abstract"),
            authors=", ".join(author_names),
            publication_year=paper_data.get("year"),
            citation_count=paper_data.get("citationCount", 0),
            source_url=paper_data.get("url"),
            pdf_url=(
                paper_data.get("openAccessPdf") or {}
            ).get("url"),
            original_filename=f"{semantic_scholar_id}.pdf",
            stored_filename=f"{semantic_scholar_id}.pdf",
            file_path=file_path,
            mime_type="application/pdf",
            file_size=file_size,
            upload_status=UploadStatus.UPLOADED,
        )

        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)

        return paper