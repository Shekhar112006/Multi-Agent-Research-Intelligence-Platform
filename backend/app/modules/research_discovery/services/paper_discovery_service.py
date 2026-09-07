from app.modules.research_discovery.clients.semantic_scholar_client import (
    SemanticScholarClient,
)


class PaperDiscoveryService:
    def __init__(
        self,
        client: SemanticScholarClient | None = None,
    ):
        self.client = client or SemanticScholarClient()

    def search_papers(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        return self.client.search_papers(
            query=query,
            limit=limit,
        )