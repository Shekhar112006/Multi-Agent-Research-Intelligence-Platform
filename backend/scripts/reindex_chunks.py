from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.database import models  # noqa: F401

from app.modules.paper_chunks.models.paper_chunk import PaperChunk
from app.modules.embeddings.services.indexing_service import IndexingService


def main():
    db = SessionLocal()

    try:
        chunks = db.scalars(
            select(PaperChunk)
        ).all()

        print(f">>> Found {len(chunks)} chunks")

        if not chunks:
            print(">>> No chunks found")
            return

        indexing_service = IndexingService()

        indexing_service.index_chunks(chunks)

        print(">>> Re-indexing complete")

    finally:
        db.close()


if __name__ == "__main__":
    main()