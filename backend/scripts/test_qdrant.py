from app.modules.embeddings.vector_db.qdrant_service import (
    QdrantService,
)

service = QdrantService()

service.create_collection("paper_chunks")

print("Collection created.")