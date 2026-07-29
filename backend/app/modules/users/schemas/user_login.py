"""
Schema for user login.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class UserLogin(BaseModel):
    """
    Login request schema.
    """

    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )