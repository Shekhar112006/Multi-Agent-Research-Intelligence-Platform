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
        "1fdf8b05-35f5-47a6-bc3b-3eec4d1be288"
    ),
    UUID(
        "f5856354-a43e-46fb-8e1f-fa11f94b000b"
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