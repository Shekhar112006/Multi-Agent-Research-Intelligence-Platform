from uuid import UUID

# Register all SQLAlchemy models first.
import app.core.database.models  # noqa: F401

from app.core.database.session import SessionLocal
from app.modules.papers.repositories.paper_repository import PaperRepository


paper_id = UUID(
    "7b984131-5aa8-4d2a-b446-6fa8c9656454"
)

db = SessionLocal()

try:
    repository = PaperRepository(db)

    paper = repository.get_by_id(paper_id)

    if paper is None:
        print("Paper not found")
    else:
        print("\n===== PAPER =====\n")
        print(f"ID: {paper.id}")
        print(f"Title: {paper.title}")
        print(f"Original filename: {paper.original_filename}")
        print(f"Project ID: {paper.project_id}")

finally:
    db.close()