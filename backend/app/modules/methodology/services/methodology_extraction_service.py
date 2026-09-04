import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.generation.services.generation_service import GenerationService
from app.modules.paper_chunks.models.paper_chunk import PaperChunk


class MethodologyExtractionService:
    def __init__(self, db: Session):
        self.db = db
        self.generation_service = GenerationService()

    async def extract_methodology(
        self,
        project_id: str,
        paper_id: str,
    ) -> dict:
        result = self.db.execute(
            select(PaperChunk)
            .where(PaperChunk.paper_id == paper_id)
            .order_by(PaperChunk.chunk_index)
        )

        chunks = result.scalars().all()

        if not chunks:
            raise ValueError("No chunks found for this paper")

        text = "\n\n".join(chunk.text for chunk in chunks)

        prompt = f"""
You are a research methodology extraction system.

Read the research paper text below and extract ONLY methodology information
explicitly supported by the paper.

Return EXACTLY this JSON object:

{{
  "research_type": "",
  "research_design": "",
  "participants": "",
  "sample_size": "",
  "data_collection": "",
  "tools_instruments": "",
  "analysis_method": "",
  "evaluation_metrics": [],
  "limitations": []
}}

Rules:
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT write explanations.
- Do NOT invent information.
- Use ONLY information present in the paper.
- If information is not mentioned, use an empty string or [].
- Keep each field concise.
- evaluation_metrics must be a JSON array.
- limitations must be a JSON array.

PAPER TEXT:

{text}
"""

        response = self.generation_service.generate(prompt, text).strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            methodology = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid methodology JSON returned by model") from exc

        if not isinstance(methodology, dict):
            raise ValueError("Invalid methodology response")

        return methodology