from app.modules.embeddings.services.embedding_service import (
    EmbeddingService,
)

service = EmbeddingService()

vector = service.embed(
    "Artificial Intelligence is transforming research."
)

print(len(vector))
print(vector[:10])