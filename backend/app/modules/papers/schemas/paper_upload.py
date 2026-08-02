"""
Schema for paper upload response.
"""

from pydantic import BaseModel


class PaperUpload(BaseModel):
    """
    Response after uploading a paper.
    """

    title: str
    project_id: str