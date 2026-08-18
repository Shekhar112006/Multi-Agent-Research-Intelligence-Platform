from app.modules.rag.services.context_builder import ContextBuilder
from app.modules.retrieval.schemas.retrieval_result import RetrievalResult


results = [
    RetrievalResult(
        paper_id="paper-123",
        project_id="project-456",
        chunk_index=10,
        text="Meditation helps refine and use generated energy.",
        score=0.91,
    ),
    RetrievalResult(
        paper_id="paper-123",
        project_id="project-456",
        chunk_index=11,
        text="The practice is described as part of internal cultivation.",
        score=0.84,
    ),
]


builder = ContextBuilder()

context = builder.build(results)

print("\n===== GENERATED CONTEXT =====\n")
print(context)