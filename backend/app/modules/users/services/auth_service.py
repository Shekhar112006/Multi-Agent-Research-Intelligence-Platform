"""
Authentication service.

Contains the business logic for user
registration and authentication.
"""

from sqlalchemy.orm import Session
from app.core.exceptions.auth import EmailAlreadyExistsError
from app.core.security.password import hash_password
from app.modules.users.models.users import User
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.schemas.user_create import UserCreate


class AuthService:
    """
    Service responsible for authentication logic.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(
        self,
        user_data: UserCreate,
    ) -> User:
        """
        Register a new user.

        Args:
            user_data: Registration request.

        Returns:
            Newly created user.
        """

        existing_user = self.repository.get_by_email(
            user_data.email
        )

        if existing_user is not None:
            raise EmailAlreadyExistsError()

        hashed_password = hash_password(
            user_data.password.get_secret_value()
        )

        return self.repository.create_user(
            user_data=user_data,
            hashed_password=hashed_password,
        )