from sqlalchemy import select

from app.core.database.database import SessionLocal
from app.modules.paper_contents.services.paper_content_service import (
    PaperContentService,
)
from app.modules.papers.models.paper import Paper

db = SessionLocal()

try:
    statement = select(Paper)

    paper = db.execute(statement).scalar_one()

    service = PaperContentService(db)

    content = service.extract_and_store(paper)

    print("Paper ID:", content.paper_id)
    print("Pages:", content.page_count)
    print("Characters:", len(content.text))

finally:
    db.close()