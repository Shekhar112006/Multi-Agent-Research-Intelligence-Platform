from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.generation.services.generation_service import (
    GenerationService,
)
from app.modules.papers.repositories.paper_repository import (
    PaperRepository,
)
from app.modules.rag.schemas.rag_response import RAGResponse
from app.modules.rag.schemas.rag_source import RAGSource
from app.modules.rag.services.context_builder import ContextBuilder
from app.modules.retrieval.services.retrieval_service import (
    RetrievalService,
)


class RAGService:
    """
    Orchestrates the complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        db: Session,
        retrieval_service: RetrievalService | None = None,
        generation_service: GenerationService | None = None,
    ):
        self.retrieval_service = (
            retrieval_service or RetrievalService()
        )

        self.generation_service = (
            generation_service or GenerationService()
        )

        self.context_builder = ContextBuilder()

        self.paper_repository = PaperRepository(db)

    def answer(
        self,
        question: str,
        project_id: str | None = None,
        limit: int = 5,
        min_score: float | None = 0.40,
    ) -> RAGResponse:

        # 1. Retrieve relevant chunks
        results = self.retrieval_service.search(
            query=question,
            limit=limit,
            project_id=project_id,
            min_score=min_score,
        )

        # 2. Build LLM context
        context = self.context_builder.build(results)

        # 3. Generate answer
        answer = self.generation_service.generate(
            question=question,
            context=context,
        )

        # 4. Load unique papers only once
        papers = {}

        for result in results:
            paper_id = UUID(result.paper_id)

            if paper_id not in papers:
                papers[paper_id] = (
                    self.paper_repository.get_by_id(paper_id)
                )

        # 5. Build source metadata
        sources = []

        for result in results:
            paper = papers.get(UUID(result.paper_id))

            if paper is None:
                continue

            sources.append(
                RAGSource(
                    paper_id=result.paper_id,
                    project_id=result.project_id,
                    title=paper.title,
                    original_filename=paper.original_filename,
                    chunk_index=result.chunk_index,
                    score=result.score,
                )
            )

        # 6. Return complete RAG response
        return RAGResponse(
            answer=answer,
            sources=sources,
        )