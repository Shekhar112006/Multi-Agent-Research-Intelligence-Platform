"""
Authentication token response schema.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT response.
    """

    access_token: str
    token_type: str = "bearer"