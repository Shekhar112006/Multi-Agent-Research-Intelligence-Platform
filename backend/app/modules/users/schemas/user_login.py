"""
User login request schema.
"""

from pydantic import BaseModel, EmailStr, SecretStr


class UserLogin(BaseModel):
    """
    User login payload.
    """

    email: EmailStr
    password: SecretStr