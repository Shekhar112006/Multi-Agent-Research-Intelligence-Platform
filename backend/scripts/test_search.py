from app.modules.embeddings.services.embedding_service import EmbeddingService
from app.modules.embeddings.vector_db.qdrant_service import QdrantService


embedding_service = EmbeddingService()
qdrant_service = QdrantService()

query = "What is the purpose of building systems instead of goals?"

vector = embedding_service.embed(query)

results = qdrant_service.search(
    vector,
    limit=5,
    project_id="b51e31e0-9e09-4936-abbf-3ee3054cad6e",
)

print(f"\nFound {len(results)} results\n")

for result in results:
    print("Score:", result.score)
    print("Paper:", result.payload["paper_id"])
    print("Chunk:", result.payload["chunk_index"])
    print("Text:", result.payload["text"][:300])
    print("-" * 80)