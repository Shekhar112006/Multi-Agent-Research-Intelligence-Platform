from uuid import UUID

from app.core.database import SessionLocal
import app.core.database.models
from app.modules.comparison.services.comparison_service import (
    ComparisonService,
)


PROJECT_ID = UUID(
    "fd4be799-3398-4152-bbc0-b07bf166a2c5"
)

PAPER_IDS = [
    UUID(
        "cc5c735a-0c5f-4659-aeed-50751593d921"
    ),
    UUID(
        "7485cbfa-66f3-452f-b8aa-8c830911b88b"
    ),
]


def test_real_ai_comparison():
    db = SessionLocal()

    try:
        service = ComparisonService(db)

        result = service.compare_papers(
            project_id=PROJECT_ID,
            paper_ids=PAPER_IDS,
        )

        print("\nAI COMPARISON RESULT:")
        print(result)

        assert isinstance(result, dict)
        assert "papers" in result
        assert "analysis" in result

    finally:
        db.close()