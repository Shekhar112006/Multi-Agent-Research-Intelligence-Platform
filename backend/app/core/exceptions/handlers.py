"""
Global exception handlers.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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