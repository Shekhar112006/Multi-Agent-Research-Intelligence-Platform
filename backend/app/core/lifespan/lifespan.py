"""
Application lifespan management.

This module defines startup and shutdown events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging.logger import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    """

    setup_logging()

    logger.info("Starting MRIP Backend...")

    yield

    logger.info("Shutting down MRIP Backend...")