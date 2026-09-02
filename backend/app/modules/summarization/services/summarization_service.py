from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.generation.services.generation_service import GenerationService


class SummarizationService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.generation_service = GenerationService()

    async def summarize(
        self,
        project_id: str,
        paper_id: str,
    ) -> str:

        result = await self.db.execute(
            select(PaperChunk)
            .where(
                PaperChunk.paper_id == paper_id,
            )
            .order_by(PaperChunk.chunk_index)
        )

        chunks = result.scalars().all()

        if not chunks:
            raise ValueError("No chunks found for this paper")

        text = "\n\n".join(chunk.text for chunk in chunks)

        prompt = f"""
You are a research paper summarization assistant.

Summarize the following research paper.

Include:
1. Research problem
2. Main objective
3. Methodology
4. Main findings
5. Conclusion
6. Key contribution

Use ONLY the information present in the paper.
Do not invent information.

Paper:

{text}
"""

        return self.generation_service.generate(prompt)