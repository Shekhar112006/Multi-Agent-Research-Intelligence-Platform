from app.modules.retrieval.services.retrieval_service import RetrievalService
from app.modules.generation.services.generation_service import GenerationService


class RAGService:
    """
    Orchestrates the complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        generation_service: GenerationService | None = None,
    ):
        self.retrieval_service = (
            retrieval_service or RetrievalService()
        )

        self.generation_service = (
            generation_service or GenerationService()
        )

    def answer(
        self,
        question: str,
        project_id: str | None = None,
        limit: int = 5,
    ) -> str:

        # 1. Retrieve relevant chunks
        results = self.retrieval_service.search(
            query=question,
            limit=limit,
            project_id=project_id,
        )

        # 2. Build context from retrieved chunks
        context_parts = []

        for result in results:
            context_parts.append(
                f"""
Paper ID: {result.paper_id}
Project ID: {result.project_id}
Chunk: {result.chunk_index}

{result.text}
"""
            )

        context = "\n\n".join(context_parts)

        # 3. Generate answer using retrieved context
        return self.generation_service.generate(
            question=question,
            context=context,
        )