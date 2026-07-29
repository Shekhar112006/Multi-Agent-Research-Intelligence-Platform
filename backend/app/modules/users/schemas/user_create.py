"""
Schema for user registration.
"""

from pydantic import Field, SecretStr

from app.modules.users.schemas.user_base import UserBase


class UserCreate(UserBase):
    """
    Request body for creating a new user.
    """

    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["StrongPassword123!"],
    )