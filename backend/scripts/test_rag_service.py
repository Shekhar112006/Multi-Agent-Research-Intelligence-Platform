from app.modules.rag.services.rag_service import RAGService


rag_service = RAGService()


question = "What is the purpose of meditation?"


answer = rag_service.answer(
    question=question,
    project_id="b51e31e0-9e09-4936-abbf-3ee3054cad6e",
    limit=2,
)


print("\n===== FINAL RAG ANSWER =====\n")
print(answer)