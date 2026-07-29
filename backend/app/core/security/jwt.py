"""
JWT utilities.

Provides helper functions for creating
and verifying JSON Web Tokens.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config.settings import settings


def create_access_token(
    subject: str,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: Usually the user's ID.

    Returns:
        Encoded JWT.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(
    token: str,
) -> dict | None:
    """
    Decode and validate a JWT.

    Args:
        token: JWT string.

    Returns:
        Decoded payload if valid,
        otherwise None.
    """

    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

    except JWTError:
        return None