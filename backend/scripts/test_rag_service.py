import app.core.database.models  # noqa: F401

from app.core.database import SessionLocal
from app.modules.rag.services.rag_service import RAGService


db = SessionLocal()

try:
    rag_service = RAGService(db)

    response = rag_service.answer(
        question="What is the purpose of meditation?",
        project_id="b51e31e0-9e09-4936-abbf-3ee3054cad6e",
        limit=5,
        min_score=0.40,
    )

    print("\n===== FINAL RAG ANSWER =====\n")
    print(response.answer)

    print("\n===== SOURCES =====\n")

    for source in response.sources:
        print(
            f"Title: {source.title}\n"
            f"Filename: {source.original_filename}\n"
            f"Chunk: {source.chunk_index}\n"
            f"Score: {source.score:.4f}\n"
        )

finally:
    db.close()