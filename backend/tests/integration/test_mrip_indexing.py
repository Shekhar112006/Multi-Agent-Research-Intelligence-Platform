import uuid
from pathlib import Path

import app.core.database.models

from qdrant_client.models import PointIdsList
from sqlalchemy import select

from app.core.database.session import SessionLocal
from app.modules.papers.models.paper import Paper
from app.modules.paper_contents.models.paper_content import PaperContent
from app.modules.paper_chunks.services.chunk_service import ChunkService
from app.modules.embeddings.services.indexing_service import IndexingService


PROJECT_ID = uuid.UUID(
    "e6a740b0-720a-497d-b25b-bac302d8eeaa"
)

PDF_PATH = "storage/papers/test_extraction.pdf"


def test_chunking_and_qdrant_indexing():
    db = SessionLocal()

    paper = None
    chunks = []
    indexing_service = None

    try:
        # ---------------------------------------------------------
        # 1. Create temporary Paper
        # ---------------------------------------------------------
        paper = Paper(
            project_id=PROJECT_ID,
            title="MRIP Indexing Integration Test",
            original_filename="test_extraction.pdf",
            stored_filename="test_indexing_test.pdf",
            file_path=PDF_PATH,
            mime_type="application/pdf",
            file_size=Path(PDF_PATH).stat().st_size,
        )

        db.add(paper)
        db.commit()
        db.refresh(paper)

        print(f"Paper created: {paper.id}")

        # ---------------------------------------------------------
        # 2. Create PaperContent
        # ---------------------------------------------------------
        content = PaperContent(
            paper_id=paper.id,
            page_count=1,
            text=(
                "MRIP indexing integration test. "
                "This document tests chunking, embedding, "
                "and Qdrant vector indexing."
            ),
        )

        db.add(content)
        db.commit()

        # ---------------------------------------------------------
        # 3. Create chunks
        # ---------------------------------------------------------
        chunk_service = ChunkService(db)

        chunks = chunk_service.create_chunks(
            paper=paper,
            text=content.text,
        )

        print(f"Chunks created: {len(chunks)}")

        # ---------------------------------------------------------
        # 4. Generate embeddings + index in Qdrant
        # ---------------------------------------------------------
        indexing_service = IndexingService()

        indexing_service.index_chunks(chunks)

        print("Indexing completed successfully")

        # ---------------------------------------------------------
        # 5. Verify Qdrant
        # ---------------------------------------------------------
        qdrant_client = indexing_service.qdrant_service.client

        results = qdrant_client.retrieve(
            collection_name="paper_chunks",
            ids=[str(chunk.id) for chunk in chunks],
            with_payload=True,
            with_vectors=False,
        )

        print(f"Qdrant results: {len(results)}")

        assert len(chunks) > 0
        assert len(results) == len(chunks)

        for result in results:
            assert result.payload["paper_id"] == str(paper.id)

        print("Qdrant payload verification passed")

    finally:
        # ---------------------------------------------------------
        # 6. Delete test vectors from Qdrant
        # ---------------------------------------------------------
        if indexing_service is not None and chunks:
            try:
                qdrant_client = indexing_service.qdrant_service.client

                qdrant_client.delete(
                    collection_name="paper_chunks",
                    points_selector=PointIdsList(
                        points=[
                            str(chunk.id)
                            for chunk in chunks
                        ],
                    ),
                )

                print("Qdrant test vectors deleted")

            except Exception as exc:
                print(
                    f"Qdrant cleanup failed: {exc}"
                )

        # ---------------------------------------------------------
        # 7. Delete temporary database records
        # ---------------------------------------------------------
        if paper is not None:
            from app.modules.paper_chunks.models.paper_chunk import (
                PaperChunk,
            )

            db.query(PaperChunk).filter(
                PaperChunk.paper_id == paper.id
            ).delete(
                synchronize_session=False
            )

            db.query(PaperContent).filter(
                PaperContent.paper_id == paper.id
            ).delete(
                synchronize_session=False
            )

            db.query(Paper).filter(
                Paper.id == paper.id
            ).delete(
                synchronize_session=False
            )

            db.commit()

            print("Temporary database records deleted")

        db.close()