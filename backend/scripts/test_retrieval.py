from app.modules.retrieval.services.retrieval_service import RetrievalService


retrieval_service = RetrievalService()

query = "What is the purpose of meditation?"

project_id = "b51e31e0-9e09-4936-abbf-3ee3054cad6e"


results = retrieval_service.search(
    query=query,
    project_id=project_id,
    limit=5,
)


print(f"\nFound {len(results)} results\n")


for result in results:
    print("Score:", result.score)
    print("Project:", result.project_id)
    print("Paper:", result.paper_id)
    print("Chunk:", result.chunk_index)
    print("Text:", result.text[:300])
    print("-" * 80)