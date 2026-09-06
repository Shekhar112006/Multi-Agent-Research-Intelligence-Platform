import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.generation.services.generation_service import GenerationService


class GapDetectionService:
    def __init__(self, db: Session):
        self.db = db
        self.generation_service = GenerationService()

    async def detect_gaps(
        self,
        project_id: str,
        paper_id: str,
    ) -> list[dict]:

        result = self.db.execute(
            select(PaperChunk)
            .where(PaperChunk.paper_id == paper_id)
            .order_by(PaperChunk.chunk_index)
        )

        chunks = result.scalars().all()

        if not chunks:
            raise ValueError("No chunks found for this paper")

        text = "\n\n".join(chunk.text for chunk in chunks)

        gap_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "gap": {"type": "string"},
                    "evidence": {"type": "string"},
                    "type": {"type": "string"},
                    "importance": {"type": "string"},
                },
                "required": [
                    "gap",
                    "evidence",
                    "type",
                    "importance",
                ],
            },
        }

        prompt = """
You are an expert research assistant.

Analyze the following research paper and identify important
research gaps.

A research gap is something that is missing, insufficiently
studied, weakly evaluated, limited, or unresolved in the research.

For every gap provide:

1. gap - clearly describe the missing or unresolved area
2. evidence - explain what in the paper supports this gap
3. type - classify the gap as methodological, data, evaluation,
   theoretical, application, or other
4. importance - low, medium, or high

Only identify gaps that can reasonably be supported by the paper.
Do not invent information.

Return only valid JSON matching the requested schema.

Paper:
"""

        response = self.generation_service.generate(
            prompt,
            text,
            response_format=gap_schema,
        ).strip()

        gaps = json.loads(response)

        if isinstance(gaps, dict):
            gaps = [gaps]

        return gaps