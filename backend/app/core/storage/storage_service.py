"""
Storage service for saving uploaded files.
"""

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class StorageService:
    """
    Handles file storage operations.
    """

    STORAGE_DIR = Path("storage/papers")

    def __init__(self) -> None:
        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_pdf(
        self,
        file: UploadFile,
    ) -> tuple[str, str]:
        """
        Save an uploaded PDF.

        Returns:
            (stored_filename, file_path)
        """

        extension = Path(file.filename).suffix

        stored_filename = f"{uuid4()}{extension}"

        file_path = self.STORAGE_DIR / stored_filename

        contents = await file.read()

        file_path.write_bytes(contents)

        return (
            stored_filename,
            str(file_path),
        )