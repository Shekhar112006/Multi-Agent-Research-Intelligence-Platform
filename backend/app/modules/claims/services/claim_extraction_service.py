import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.generation.services.generation_service import GenerationService


class ClaimExtractionService:

    def __init__(self, db: Session):
        self.db = db
        self.generation_service = GenerationService()

    async def extract_claims(
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

        # Keep batches small enough for local LLM inference.
        batch_size = 2

        all_claims = []

        for i in range(0, len(chunks), batch_size):

            batch = chunks[i:i + batch_size]

            text = "\n\n".join(chunk.text for chunk in batch)

            prompt = """
You are extracting important research claims from a research paper.

Return ONLY a valid JSON array.

Every item MUST be an object with exactly these fields:

{
  "claim": "research claim",
  "evidence": "evidence supporting the claim",
  "type": "finding",
  "importance": "high"
}

Allowed type values:
finding
contribution
method
result
conclusion

Allowed importance values:
high
medium
low

Rules:
1. Use ONLY information in the provided text.
2. Do not invent facts.
3. Extract only important research claims.
4. Do not extract definitions or general background statements.
5. Return at most 5 claims.
6. If there are no important claims, return [].
7. Do NOT use Markdown.
8. Do NOT write anything before or after the JSON array.

Paper section:

"""

            response = self.generation_service.generate(
                prompt,
                text,
            ).strip()

            # Remove Markdown fences if the model adds them.
            if response.startswith("```"):
                response = response.replace("```json", "")
                response = response.replace("```", "")
                response = response.strip()

            try:
                claims = json.loads(response)
                if isinstance(claims, dict):
                    claims = [claims]
            except json.JSONDecodeError:
                continue

            if not isinstance(claims, list):
                continue

            for claim in claims:

                if not isinstance(claim, dict):
                    continue

                required_fields = {
                    "claim",
                    "evidence",
                    "type",
                    "importance",
                }

                if not required_fields.issubset(claim.keys()):
                    continue

                all_claims.append(claim)

        return all_claims