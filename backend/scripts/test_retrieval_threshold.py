from app.modules.retrieval.services.retrieval_service import RetrievalService


service = RetrievalService()

results = service.search(
    query="What is the purpose of meditation?",
    project_id="b51e31e0-9e09-4936-abbf-3ee3054cad6e",
    limit=5,
    min_score=0.40,
)

print(f"\nFound {len(results)} results\n")

for result in results:
    print(
        f"Score: {result.score:.4f} | "
        f"Chunk: {result.chunk_index}"
    )