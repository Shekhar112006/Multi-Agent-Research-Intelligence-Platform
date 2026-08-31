from app.core.database.session import SessionLocal
from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.embeddings.services.indexing_service import IndexingService
from sqlalchemy import select


db = SessionLocal()

try:
    chunks = db.execute(
        select(PaperChunk)
        .order_by(PaperChunk.paper_id, PaperChunk.chunk_index)
    ).scalars().all()

    print(f"PostgreSQL chunks found: {len(chunks)}")

    indexing_service = IndexingService()
    indexing_service.index_chunks(chunks)

    print("Qdrant indexing completed.")

finally:
    db.close()
