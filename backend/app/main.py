"""
Application entry point.

Creates and configures the FastAPI application.
"""
from app.api import api_router
from fastapi import FastAPI
from app.core.exceptions.handlers import register_exception_handlers
from app.core.config.settings import settings
from app.core.lifespan.lifespan import lifespan
from app.modules.projects.routers.project_router import router as project_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router)