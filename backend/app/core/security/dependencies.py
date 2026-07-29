"""
Authentication dependencies.
"""

from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions.auth import AuthenticationError
from app.core.security.jwt import decode_access_token
from app.modules.users.models.users import User
from app.modules.users.repositories.user_repository import UserRepository

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Return the currently authenticated user.
    """

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise AuthenticationError()

    subject = payload.get("sub")

    if subject is None:
        raise AuthenticationError()

    repository = UserRepository(db)

    user = repository.get_by_id(
        UUID(subject)
    )

    if user is None:
        raise AuthenticationError()

    return user