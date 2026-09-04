"""
Application entry point.

Creates and configures the FastAPI application.
"""

from fastapi import FastAPI

from app.api import api_router
from app.core.config.settings import settings
from app.core.exceptions.handlers import register_exception_handlers
from app.core.lifespan.lifespan import lifespan
from app.modules.papers.routers.paper_router import router as paper_router
from app.modules.search.routers.search_router import router as search_router
from app.modules.rag.routers.rag_router import router as rag_router
from app.modules.summarization.routers import router as summarization_router
from app.modules.claims.routers import router as claims_router
from app.modules.methodology.routers import router as methodology_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router)
app.include_router(paper_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(summarization_router)
app.include_router(claims_router)
app.include_router(methodology_router)