"""
Schema returned to API clients.
"""

from datetime import datetime
from uuid import UUID

from app.modules.users.models.enums import UserRole
from app.modules.users.schemas.user_base import UserBase


class UserResponse(UserBase):
    """
    User response schema.
    """

    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime