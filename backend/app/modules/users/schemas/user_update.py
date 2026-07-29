"""
Schema for updating user information.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserUpdate(BaseModel):
    """
    User update schema.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    email: EmailStr | None = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )