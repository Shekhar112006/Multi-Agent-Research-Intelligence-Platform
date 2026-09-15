from pathlib import Path
from app.modules.research_discovery.services.paper_ingestion_service import (
    PaperIngestionService,
)



class FakeSemanticScholarClient:
    def get_paper(self, paper_id: str) -> dict:
        return {
            "paperId": paper_id,
            "title": "Test Research Paper",
            "abstract": "This is a test research paper.",
            "authors": [
                {"name": "Test Author"},
            ],
            "year": 2025,
            "citationCount": 10,
            "url": "https://example.com/paper",
            "openAccessPdf": {
                "url": "https://example.com/paper.pdf",
            },
        }


def test_ingestion_service_uses_injected_client():
    fake_client = FakeSemanticScholarClient()

    service = PaperIngestionService(
        db=None,
        client=fake_client,
    )

    paper_data = service.client.get_paper(
        paper_id="test-paper-123",
    )

    assert paper_data["paperId"] == "test-paper-123"
    assert paper_data["title"] == "Test Research Paper"
    assert paper_data["openAccessPdf"]["url"].endswith(".pdf")

class FakeDownloadService:
    def download_pdf(
        self,
        pdf_url: str,
        paper_id: str,
    ) -> str:
        file_path = f"storage/papers/{paper_id}.pdf"

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fake pdf content")

        return file_path


class FakePersistenceService:
    def __init__(self):
        self.received_data = None
        self.received_file_path = None
        self.received_file_size = None

    def create_paper(
        self,
        project_id,
        paper_data: dict,
        file_path: str,
        file_size: int,
    ):
        self.received_data = paper_data
        self.received_file_path = file_path
        self.received_file_size = file_size

        return type(
            "FakePaper",
            (),
            {
                "id": "database-paper-id",
                "semantic_scholar_id": paper_data["paperId"],
                "title": paper_data["title"],
                "file_path": file_path,
                "file_size": file_size,
            },
        )()

class FakeContentService:
    def __init__(self):
        self.received_paper = None

    def extract_and_store(self, paper):
        self.received_paper = paper

        return type(
            "FakeContent",
            (),
            {
                "text": "Test chunk content",
            },
        )()

class FakeChunkService:
    def __init__(self):
        self.received_paper = None
        self.received_text = None

    def create_chunks(
        self,
        paper,
        text: str,
    ):
        self.received_paper = paper
        self.received_text = text

        return [
            type(
                "FakeChunk",
                (),
                {
                    "id": "chunk-1",
                    "text": "Test chunk content",
                },
            )()
        ]


class FakeIndexingService:
    def __init__(self):
        self.received_chunks = None

    def index_chunks(
        self,
        chunks,
    ):
        self.received_chunks = chunks

def test_ingest_paper_workflow():
    fake_client = FakeSemanticScholarClient()
    fake_download_service = FakeDownloadService()
    fake_persistence_service = FakePersistenceService()
    fake_content_service = FakeContentService()
    fake_chunk_service = FakeChunkService()
    fake_indexing_service = FakeIndexingService()

    service = PaperIngestionService(
        db=None,
        client=fake_client,
        download_service=fake_download_service,
        persistence_service=fake_persistence_service,
        content_service=fake_content_service,
        chunk_service=fake_chunk_service,
        indexing_service=fake_indexing_service,
    )

    paper = service.ingest_paper(
        project_id="project-123",
        paper_id="test-paper-123",
    )

    assert paper.semantic_scholar_id == "test-paper-123"
    assert paper.title == "Test Research Paper"

    assert (
        fake_persistence_service.received_file_path
        == "storage/papers/test-paper-123.pdf"
    )

    assert (
        fake_persistence_service.received_data["title"]
        == "Test Research Paper"
    )

    assert fake_content_service.received_paper is paper

    assert fake_chunk_service.received_paper is paper

    assert (
        fake_chunk_service.received_text
        == "Test chunk content"
    )

    assert len(fake_indexing_service.received_chunks) == 1

    assert (
        fake_indexing_service.received_chunks[0].text
        == "Test chunk content"
    )