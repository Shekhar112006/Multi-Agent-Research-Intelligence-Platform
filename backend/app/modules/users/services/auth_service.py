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

from app.core.exceptions.auth import InvalidCredentialsError
from app.core.security.jwt import create_access_token
from app.core.security.password import verify_password
from app.modules.users.schemas.token import Token
from app.modules.users.schemas.user_login import UserLogin


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

    def login(
        self,
        user_data: UserLogin,
    ) -> Token:
        """
        Authenticate a user.
        """

        user = self.repository.get_by_email(
            user_data.email
        )

        if user is None:
            raise InvalidCredentialsError()

        is_valid = verify_password(
            user_data.password.get_secret_value(),
            user.hashed_password,
        )

        if not is_valid:
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=str(user.id),
        )

        return Token(
            access_token=access_token,
        )