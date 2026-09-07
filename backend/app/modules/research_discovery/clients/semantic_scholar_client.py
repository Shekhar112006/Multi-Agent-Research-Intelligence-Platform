import os
import time

import requests


class SemanticScholarClient:
    def __init__(
        self,
        base_url: str = "https://api.semanticscholar.org/graph/v1",
    ):
        self.base_url = base_url
        self.api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    def search_papers(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict]:
        headers = {}

        if self.api_key:
            headers["x-api-key"] = self.api_key

        for attempt in range(3):
            response = requests.get(
                f"{self.base_url}/paper/search",
                params={
                    "query": query,
                    "limit": limit,
                    "fields": (
                        "paperId,title,abstract,authors,year,"
                        "citationCount,url,openAccessPdf"
                    ),
                },
                headers=headers,
                timeout=30,
            )

            if response.status_code != 429:
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])

            if attempt < 2:
                retry_after = response.headers.get("Retry-After")

                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** attempt

                time.sleep(wait_time)

        response.raise_for_status()

        return []