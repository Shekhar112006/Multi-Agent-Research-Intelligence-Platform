"""
Repository for user database operations.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.models.users import User
from app.modules.users.schemas.user_create import UserCreate


class UserRepository:
    """
    Handles all database operations related to users.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email address.

        Returns:
            User instance if found, otherwise None.
        """

        statement = select(User).where(User.email == email)

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def create_user(
        self,
        user_data: UserCreate,
        hashed_password: str,
    ) -> User:
        """
        Create a new user.

        Args:
            user_data: Validated user registration data.
            hashed_password: Securely hashed password.

        Returns:
            Newly created User instance.
        """

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self.db.add(user)

        try:
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception:
            self.db.rollback()
            raise