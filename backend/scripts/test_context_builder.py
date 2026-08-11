from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)
from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)
from app.modules.retrieval.services.context_builder import (
    ContextBuilder,
)


embedding_service = EmbeddingService()
qdrant_service = QdrantService()
context_builder = ContextBuilder()


query = "What is the purpose of building systems instead of goals?"

vector = embedding_service.embed(query)

results = qdrant_service.search(
    vector,
    limit=5,
    project_id="b51e31e0-9e09-4936-abbf-3ee3054cad6e",
)

context = context_builder.build(results)

print("\n===== GENERATED CONTEXT =====\n")
print(context)