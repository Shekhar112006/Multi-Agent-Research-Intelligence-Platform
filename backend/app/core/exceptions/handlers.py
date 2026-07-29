"""
Global exception handlers.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions.auth import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.core.exceptions.auth import (
    AuthenticationError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.core.exceptions.auth import EmailAlreadyExistsError


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    """

    @app.exception_handler(EmailAlreadyExistsError)
    async def email_exists_handler(
        request: Request,
        exc: EmailAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_handler(
        request: Request,
        exc: AuthenticationError,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "detail": str(exc),
            },
        )