"""
Base Pydantic schema for users.

This schema contains fields shared across
multiple user-related schemas.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """
    Common user fields.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        examples=["Shekhar Sharma"],
    )

    email: EmailStr = Field(
        ...,
        examples=["shekhar@example.com"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )