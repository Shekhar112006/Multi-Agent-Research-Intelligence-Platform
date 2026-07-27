"""
Application entry point.

Creates and configures the FastAPI application.
"""

from fastapi import FastAPI

from app.api import api_router
from app.core.config.settings import settings
from app.core.lifespan.lifespan import lifespan

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(api_router)