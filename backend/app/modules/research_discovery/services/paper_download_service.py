from pathlib import Path

import requests


class PaperDownloadService:
    def __init__(self, storage_dir: str = "storage/papers"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def download_pdf(
        self,
        pdf_url: str,
        paper_id: str,
    ) -> str:
        response = requests.get(
            pdf_url,
            timeout=60,
        )

        response.raise_for_status()

        file_path = self.storage_dir / f"{paper_id}.pdf"

        file_path.write_bytes(response.content)

        return str(file_path)