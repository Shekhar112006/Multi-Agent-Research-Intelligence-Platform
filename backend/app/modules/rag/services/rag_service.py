from app.modules.retrieval.services.retrieval_service import RetrievalService
from app.modules.generation.services.generation_service import GenerationService
from app.modules.rag.services.context_builder import ContextBuilder


class RAGService:
    """
    Orchestrates the complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        generation_service: GenerationService | None = None,
        context_builder: ContextBuilder | None = None,
    ):
        self.retrieval_service = (
            retrieval_service or RetrievalService()
        )

        self.generation_service = (
            generation_service or GenerationService()
        )

        self.context_builder = (
            context_builder or ContextBuilder()
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

        # 2. Build LLM context
        context = self.context_builder.build(results)

        # 3. Generate answer
        return self.generation_service.generate(
            question=question,
            context=context,
        )