"""
Centralized logging configuration.

This module provides a reusable logger for the entire application.
All modules should obtain loggers from here instead of configuring
logging independently.
"""

import logging
import sys

from app.core.config.settings import settings


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """
    Configure the application's root logger.

    This function should be called once during application startup.
    """

    logging.basicConfig(
        level=settings.log_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Usually pass __name__.

    Returns:
        Configured Logger instance.
    """
    return logging.getLogger(name)